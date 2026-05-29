#!/usr/bin/env python3
"""Flask web server for Catacomb UI."""
import os
import logging
import json
import time
from functools import lru_cache
from concurrent.futures import ThreadPoolExecutor, as_completed
from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
from orchestrator import CatacombOrchestrator
from outcome_ledger_v2 import OutcomeLedger, InterventionStatus, VerificationStatus
from repo_valuation import RepoValuation
from abandoned_repo_kpis import AbandonedRepoKPIs

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler('catacomb_api.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

app = Flask(__name__, static_folder='static', static_url_path='')
CORS(app)

# Global orchestrator instance
orchestrator = None

# Global outcome ledger instance
outcome_ledger = OutcomeLedger()

# Global valuation instance
repo_valuation = RepoValuation()

# Global KPI calculator instance
kpi_calculator = AbandonedRepoKPIs()

# Cache for discovery results (5 minute TTL)
discovery_cache = {}
CACHE_TTL = 300  # 5 minutes


def get_orchestrator():
    """Get or create orchestrator instance."""
    global orchestrator
    if orchestrator is None:
        github_token = os.getenv("GITHUB_TOKEN")
        orchestrator = CatacombOrchestrator(github_token)
    return orchestrator


@app.route('/')
def index():
    """Serve the React app."""
    return send_from_directory('static', 'index.html')


@app.route('/api/analyze/repo/<owner>/<repo>')
def analyze_repo(owner, repo):
    """Analyze a single repository."""
    logger.info(f"Repo analysis request: {owner}/{repo}")
    try:
        orch = get_orchestrator()
        result = orch.analyze_repo(owner, repo)
        logger.info(f"Repo analysis success: {owner}/{repo}")
        return jsonify(result)
    except Exception as e:
        logger.error(f"Repo analysis failed: {owner}/{repo} - {str(e)}")
        return jsonify({"error": str(e)}), 500


@app.route('/api/analyze/topic', methods=['POST'])
def analyze_topic():
    """Analyze repositories by topic."""
    data = request.get_json()
    topic = data.get('topic')
    limit = data.get('limit', 10)
    logger.info(f"Topic analysis request: {topic} (limit: {limit})")
    
    try:
        if not topic:
            logger.warning("Topic analysis failed: topic is required")
            return jsonify({"error": "Topic is required"}), 400
        
        orch = get_orchestrator()
        results = orch.analyze_topic(topic, limit)
        logger.info(f"Topic analysis success: {topic} - {len(results)} repos")
        return jsonify({"results": results})
    except Exception as e:
        logger.error(f"Topic analysis failed: {topic} - {str(e)}")
        return jsonify({"error": str(e)}), 500


@app.route('/api/analyze/user', methods=['POST'])
def analyze_user():
    """Analyze repositories by user."""
    data = request.get_json()
    username = data.get('username')
    limit = data.get('limit', 10)
    logger.info(f"User analysis request: {username} (limit: {limit})")
    
    try:
        if not username:
            logger.warning("User analysis failed: username is required")
            return jsonify({"error": "Username is required"}), 400
        
        orch = get_orchestrator()
        results = orch.analyze_user(username, limit)
        logger.info(f"User analysis success: {username} - {len(results)} repos")
        return jsonify({"results": results})
    except Exception as e:
        logger.error(f"User analysis failed: {username} - {str(e)}")
        return jsonify({"error": str(e)}), 500


@app.route('/api/health')
def health():
    """Health check endpoint."""
    return jsonify({"status": "healthy"})


# Intervention Lifecycle API

@app.route('/api/interventions', methods=['POST'])
def create_intervention():
    """Create a new intervention record."""
    try:
        data = request.get_json()
        
        record_id = outcome_ledger.create_intervention(
            asset_id=data.get('asset_id'),
            asset_type=data.get('asset_type', 'github_repo'),
            asset_name=data.get('asset_name'),
            developer_id=data.get('developer_id'),
            developer_username=data.get('developer_username'),
            before_state=data.get('before_state'),
            intervention_type=data.get('intervention_type'),
            intervention_description=data.get('intervention_description'),
            planned_effort_days=data.get('planned_effort_days'),
            predicted_value=data.get('predicted_value'),
            predicted_probability=data.get('predicted_probability'),
            predicted_risk=data.get('predicted_risk'),
            predicted_outcome=data.get('predicted_outcome')
        )
        
        logger.info(f"Created intervention: {record_id}")
        return jsonify({"record_id": record_id, "status": "created"})
    except Exception as e:
        logger.error(f"Failed to create intervention: {str(e)}")
        return jsonify({"error": str(e)}), 500


@app.route('/api/interventions/<record_id>/start', methods=['POST'])
def start_intervention(record_id):
    """Start an intervention."""
    try:
        data = request.get_json() or {}
        actual_effort_days = data.get('actual_effort_days')
        
        result = outcome_ledger.start_intervention(record_id, actual_effort_days)
        logger.info(f"Started intervention: {record_id}")
        return jsonify(result)
    except Exception as e:
        logger.error(f"Failed to start intervention {record_id}: {str(e)}")
        return jsonify({"error": str(e)}), 500


@app.route('/api/interventions/<record_id>/complete', methods=['POST'])
def complete_intervention(record_id):
    """Complete an intervention with after state and outcomes."""
    try:
        data = request.get_json()
        
        result = outcome_ledger.complete_intervention(
            record_id=record_id,
            after_state=data.get('after_state'),
            outcome_metrics=data.get('outcome_metrics'),
            actual_effort_days=data.get('actual_effort_days')
        )
        
        logger.info(f"Completed intervention: {record_id}")
        return jsonify(result)
    except Exception as e:
        logger.error(f"Failed to complete intervention {record_id}: {str(e)}")
        return jsonify({"error": str(e)}), 500


@app.route('/api/interventions/<record_id>/verify', methods=['POST'])
def verify_intervention(record_id):
    """Verify an intervention outcome."""
    try:
        data = request.get_json()
        
        result = outcome_ledger.verify_outcome(
            record_id=record_id,
            verifier_id=data.get('verifier_id'),
            verifier_username=data.get('verifier_username'),
            status=data.get('status'),
            notes=data.get('notes')
        )
        
        logger.info(f"Verified intervention: {record_id}")
        return jsonify(result)
    except Exception as e:
        logger.error(f"Failed to verify intervention {record_id}: {str(e)}")
        return jsonify({"error": str(e)}), 500


@app.route('/api/interventions/<record_id>')
def get_intervention(record_id):
    """Get intervention record by ID."""
    try:
        result = outcome_ledger.get_intervention(record_id)
        if not result:
            return jsonify({"error": "Intervention not found"}), 404
        return jsonify(result)
    except Exception as e:
        logger.error(f"Failed to get intervention {record_id}: {str(e)}")
        return jsonify({"error": str(e)}), 500


@app.route('/api/developers/<developer_id>/reputation')
def get_developer_reputation(developer_id):
    """Get developer reputation metrics."""
    try:
        result = outcome_ledger.get_developer_reputation(developer_id)
        if not result:
            return jsonify({"error": "Developer not found"}), 404
        return jsonify(result)
    except Exception as e:
        logger.error(f"Failed to get developer reputation {developer_id}: {str(e)}")
        return jsonify({"error": str(e)}), 500


@app.route('/api/interventions/training-data')
def get_training_data():
    """Get training dataset for ML models."""
    try:
        dataset = outcome_ledger.get_training_dataset()
        return jsonify({"dataset": dataset, "count": len(dataset)})
    except Exception as e:
        logger.error(f"Failed to get training data: {str(e)}")
        return jsonify({"error": str(e)}), 500


# Valuation API

@app.route('/api/valuation/<owner>/<repo>')
def get_valuation(owner, repo):
    """Get dollar valuation for a repository."""
    logger.info(f"Valuation request: {owner}/{repo}")
    try:
        orch = get_orchestrator()
        result = orch.analyze_repo(owner, repo)
        
        if "error" in result:
            return jsonify({"error": result["error"]}), 404
        
        valuation = repo_valuation.calculate_valuation(
            result["repo_data"],
            result.get("analysis")
        )
        
        logger.info(f"Valuation success: {owner}/{repo} = ${valuation['total_value_usd']}")
        return jsonify({
            "repo": f"{owner}/{repo}",
            "valuation": valuation,
            "repo_data": result["repo_data"],
            "analysis": result.get("analysis")
        })
    except Exception as e:
        logger.error(f"Valuation failed: {owner}/{repo} - {str(e)}")
        return jsonify({"error": str(e)}), 500


@app.route('/api/discover/quality')
def discover_quality_repos():
    """Get high-value repositories for discovery."""
    # Check cache
    cache_key = "quality"
    current_time = time.time()
    
    if cache_key in discovery_cache and current_time - discovery_cache[cache_key]["timestamp"] < CACHE_TTL:
        logger.info("Returning cached quality discovery results")
        return jsonify(discovery_cache[cache_key]["data"])
    
    try:
        # Predefined list of under-the-radar quality repos to analyze
        # These are smaller, less famous but high-quality projects across categories
        quality_repos = [
            # Terminal & CLI Tools
            ("starship", "starship"),  # Rust shell prompt
            ("atuinsh", "atuin"),  # Shell history
            ("zellij-org", "zellij"),  # Terminal multiplexer
            ("helix-editor", "helix"),  # Modal text editor
            ("eza-community", "eza"),  # Modern ls replacement
            ("fd-dev", "fd"),  # Find alternative
            ("sharkdp", "bat"),  # Cat alternative
            ("sharkdp", "ripgrep"),  # Grep alternative
            ("dandavison", "delta"),  # Git diff viewer
            ("junegunn", "fzf"),  # Fuzzy finder
            ("sxyazi", "yazi"),  # Terminal file manager
            ("nushell", "nushell"),  # Modern shell
            ("kovidgoyal", "kitty"),  # Terminal emulator
            ("alacritty", "alacritty"),  # Terminal emulator
            ("wez", "wezterm"),  # Terminal emulator
            ("charmbracelet", "gum"),  # Shell script UI
            ("charmbracelet", "lip Gloss"),  # TUI library
            ("charmbracelet", "bubbletea"),  # TUI framework
            ("c-batastrophe", "broot"),  # Tree viewer
            ("canopas", "tldr"),  # Simplified man pages
            ("o2sh", "onefetch"),  # Git info tool
            ("ogham", "exa"),  # Modern ls (deprecated but popular)
            
            # Build Tools & Package Managers
            ("golang", "go"),  # Go language
            ("rust-lang", "cargo"),  # Rust package manager
            ("pnpm", "pnpm"),  # Fast npm alternative
            ("yarnpkg", "yarn"),  # Package manager
            ("bun", "bun"),  # JS runtime
            ("denoland", "deno"),  # JS runtime
            ("sveltejs", "kit"),  # Svelte build tool
            ("vitejs", "vite"),  # Build tool
            ("swc-project", "swc"),  # JS/TS compiler
            ("esbuild", "esbuild"),  # JS bundler
            ("rome", "rome"),  # JS toolchain
            ("biomejs", "biome"),  # JS linter/formatter
            ("ruff-lang", "ruff"),  # Python linter
            ("astral-sh", "uv"),  # Python package manager
            ("mitsuhiko", "rye"),  # Python toolchain
            ("poetry", "poetry"),  # Python dependency manager
            ("pypa", "pip"),  # Python installer
            
            # Web Frameworks (Alternatives to React/Next.js)
            ("solidjs", "solid"),  # Reactive UI
            ("sveltejs", "svelte"),  # Component framework
            ("htmx", "htmx"),  # HTML extension
            ("hotwired", "turbo"),  # Rails framework
            ("phoenixframework", "phoenix"),  # Elixir framework
            ("lucacasonato", "remix"),  # React framework
            ("builderio", "qwik"),  # Resumable framework
            ("marko-js", "marko"),  # UI framework
            ("astro", "astro"),  # Web framework
            ("fresh", "fresh"),  # Deno framework
            ("elysiajs", "elysia"),  # Bun framework
            ("hono", "hono"),  # Web framework
            ("lit", "lit"),  # Web components
            ("fastify", "fastify"),  # Node framework
            ("poliastro", "poliastro"),  # Python web framework
            
            # Database Tools & ORMs
            ("prisma", "prisma"),  # TypeScript ORM
            ("drizzle-team", "drizzle-orm"),  # SQL ORM
            ("supabase", "supabase"),  # Backend platform
            ("planetscale", "planetscale"),  # Database platform
            ("xata", "xata"),  # Serverless database
            ("neondatabase", "neon"),  # Postgres platform
            ("turso", "turso"),  # SQLite platform
            ("libsql", "libsql"),  # SQLite fork
            ("duckdb", "duckdb"),  # Analytical database
            ("clickhouse", "clickhouse"),  # Columnar database
            ("timescale", "timescaledb"),  # Postgres extension
            ("pgvector", "pgvector"),  # Vector extension
            ("qdrant", "qdrant"),  # Vector database
            ("weaviate", "weaviate"),  # Vector database
            ("milvus-io", "milvus"),  # Vector database
            ("sequelize", "sequelize"),  # Node ORM
            ("typeorm", "typeorm"),  # TypeScript ORM
            ("sqlalchemy", "sqlalchemy"),  # Python ORM
            
            # DevOps & Infrastructure
            ("hashicorp", "terraform"),  # IaC tool
            ("hashicorp", "packer"),  # Image builder
            ("ansible", "ansible"),  # Automation
            ("puppetlabs", "puppet"),  # Configuration
            ("chef", "chef"),  # Configuration
            ("saltstack", "salt"),  # Automation
            ("grafana", "grafana"),  # Monitoring
            ("prometheus", "prometheus"),  # Monitoring
            ("loki", "loki"),  # Logging
            ("temporalio", "temporal"),  # Workflow engine
            ("dapr", "dapr"),  # Microservices runtime
            ("open-telemetry", "opentelemetry"),  # Observability
            ("envoyproxy", "envoy"),  # Service proxy
            ("kubernetes", "kubernetes"),  # Container orchestration
            ("lima", "lima"),  # Linux VMs on Mac
            ("colima", "colima"),  # Container runtime
            ("rancher", "rancher"),  # K8s management
            ("portainer", "portainer"),  # Container UI
            
            # Testing & Quality
            ("jestjs", "jest"),  # Testing framework
            ("vitest-dev", "vitest"),  # Testing framework
            ("mswjs", "msw"),  # API mocking
            ("playwright", "playwright"),  # E2E testing
            ("cypress", "cypress"),  # E2E testing
            ("testing-library", "testing-library"),  # Testing utilities
            ("k6io", "k6"),  # Load testing
            ("gatling", "gatling"),  # Load testing
            ("locustio", "locust"),  # Load testing
            ("sonarsource", "sonarqube"),  # Code quality
            ("deepsource", "deepsource"),  # Code analysis
            ("codecov", "codecov"),  # Code coverage
            ("coveralls", "coveralls"),  # Code coverage
            
            # Security
            ("aquasecurity", "trivy"),  # Security scanner
            ("anchore", "grype"),  # Vulnerability scanner
            ("snyk", "snyk"),  # Security platform
            ("OWASP", "dependency-check"),  # Dependency scanner
            ("zmap", "zmap"),  # Network scanner
            ("microsoft", "gpt"),  # AI security
            ("trailofbits", "audit"),  # Security audit
        ]
        
        orch = get_orchestrator()
        results = []
        
        # Parallel processing for faster analysis
        with ThreadPoolExecutor(max_workers=5) as executor:
            future_to_repo = {
                executor.submit(orch.analyze_repo, owner, repo): (owner, repo)
                for owner, repo in quality_repos[:10]
            }
            
            for future in as_completed(future_to_repo):
                owner, repo = future_to_repo[future]
                try:
                    result = future.result(timeout=30)  # 30 second timeout per repo
                    if "error" not in result:
                        valuation = repo_valuation.calculate_valuation(
                            result["repo_data"],
                            result.get("analysis")
                        )
                        results.append({
                            "repo": f"{owner}/{repo}",
                            "valuation": valuation,
                            "repo_data": result["repo_data"],
                            "analysis": result.get("analysis")
                        })
                except Exception as e:
                    logger.warning(f"Failed to analyze {owner}/{repo}: {str(e)}")
                    continue
        
        # Sort by valuation
        results.sort(key=lambda x: x["valuation"]["total_value_usd"], reverse=True)
        
        # Cache results
        discovery_cache[cache_key] = {
            "timestamp": current_time,
            "data": {"results": results, "count": len(results)}
        }
        
        logger.info(f"Quality discovery: {len(results)} repos")
        return jsonify({"results": results, "count": len(results)})
    except Exception as e:
        logger.error(f"Quality discovery failed: {str(e)}")
        return jsonify({"error": str(e)}), 500


@app.route('/api/discover/trending')
def discover_trending_repos():
    """Get trending repositories based on velocity metrics."""
    # Check cache
    cache_key = "trending"
    current_time = time.time()
    
    if cache_key in discovery_cache and current_time - discovery_cache[cache_key]["timestamp"] < CACHE_TTL:
        logger.info("Returning cached trending discovery results")
        return jsonify(discovery_cache[cache_key]["data"])
    
    try:
        # Predefined list of under-the-radar repos for trending analysis
        # Same expanded dataset as quality for consistency
        trending_repos = [
            # Terminal & CLI Tools
            ("starship", "starship"),  # Rust shell prompt
            ("atuinsh", "atuin"),  # Shell history
            ("zellij-org", "zellij"),  # Terminal multiplexer
            ("helix-editor", "helix"),  # Modal text editor
            ("eza-community", "eza"),  # Modern ls replacement
            ("fd-dev", "fd"),  # Find alternative
            ("sharkdp", "bat"),  # Cat alternative
            ("sharkdp", "ripgrep"),  # Grep alternative
            ("dandavison", "delta"),  # Git diff viewer
            ("junegunn", "fzf"),  # Fuzzy finder
            ("sxyazi", "yazi"),  # Terminal file manager
            ("nushell", "nushell"),  # Modern shell
            ("kovidgoyal", "kitty"),  # Terminal emulator
            ("alacritty", "alacritty"),  # Terminal emulator
            ("wez", "wezterm"),  # Terminal emulator
            ("charmbracelet", "gum"),  # Shell script UI
            ("charmbracelet", "lip Gloss"),  # TUI library
            ("charmbracelet", "bubbletea"),  # TUI framework
            ("c-batastrophe", "broot"),  # Tree viewer
            ("canopas", "tldr"),  # Simplified man pages
            ("o2sh", "onefetch"),  # Git info tool
            ("ogham", "exa"),  # Modern ls (deprecated but popular)
            
            # Build Tools & Package Managers
            ("golang", "go"),  # Go language
            ("rust-lang", "cargo"),  # Rust package manager
            ("pnpm", "pnpm"),  # Fast npm alternative
            ("yarnpkg", "yarn"),  # Package manager
            ("bun", "bun"),  # JS runtime
            ("denoland", "deno"),  # JS runtime
            ("sveltejs", "kit"),  # Svelte build tool
            ("vitejs", "vite"),  # Build tool
            ("swc-project", "swc"),  # JS/TS compiler
            ("esbuild", "esbuild"),  # JS bundler
            ("rome", "rome"),  # JS toolchain
            ("biomejs", "biome"),  # JS linter/formatter
            ("ruff-lang", "ruff"),  # Python linter
            ("astral-sh", "uv"),  # Python package manager
            ("mitsuhiko", "rye"),  # Python toolchain
            ("poetry", "poetry"),  # Python dependency manager
            ("pypa", "pip"),  # Python installer
            
            # Web Frameworks (Alternatives to React/Next.js)
            ("solidjs", "solid"),  # Reactive UI
            ("sveltejs", "svelte"),  # Component framework
            ("htmx", "htmx"),  # HTML extension
            ("hotwired", "turbo"),  # Rails framework
            ("phoenixframework", "phoenix"),  # Elixir framework
            ("lucacasonato", "remix"),  # React framework
            ("builderio", "qwik"),  # Resumable framework
            ("marko-js", "marko"),  # UI framework
            ("astro", "astro"),  # Web framework
            ("fresh", "fresh"),  # Deno framework
            ("elysiajs", "elysia"),  # Bun framework
            ("hono", "hono"),  # Web framework
            ("lit", "lit"),  # Web components
            ("fastify", "fastify"),  # Node framework
            ("poliastro", "poliastro"),  # Python web framework
            
            # Database Tools & ORMs
            ("prisma", "prisma"),  # TypeScript ORM
            ("drizzle-team", "drizzle-orm"),  # SQL ORM
            ("supabase", "supabase"),  # Backend platform
            ("planetscale", "planetscale"),  # Database platform
            ("xata", "xata"),  # Serverless database
            ("neondatabase", "neon"),  # Postgres platform
            ("turso", "turso"),  # SQLite platform
            ("libsql", "libsql"),  # SQLite fork
            ("duckdb", "duckdb"),  # Analytical database
            ("clickhouse", "clickhouse"),  # Columnar database
            ("timescale", "timescaledb"),  # Postgres extension
            ("pgvector", "pgvector"),  # Vector extension
            ("qdrant", "qdrant"),  # Vector database
            ("weaviate", "weaviate"),  # Vector database
            ("milvus-io", "milvus"),  # Vector database
            ("sequelize", "sequelize"),  # Node ORM
            ("typeorm", "typeorm"),  # TypeScript ORM
            ("sqlalchemy", "sqlalchemy"),  # Python ORM
            
            # DevOps & Infrastructure
            ("hashicorp", "terraform"),  # IaC tool
            ("hashicorp", "packer"),  # Image builder
            ("ansible", "ansible"),  # Automation
            ("puppetlabs", "puppet"),  # Configuration
            ("chef", "chef"),  # Configuration
            ("saltstack", "salt"),  # Automation
            ("grafana", "grafana"),  # Monitoring
            ("prometheus", "prometheus"),  # Monitoring
            ("loki", "loki"),  # Logging
            ("temporalio", "temporal"),  # Workflow engine
            ("dapr", "dapr"),  # Microservices runtime
            ("open-telemetry", "opentelemetry"),  # Observability
            ("envoyproxy", "envoy"),  # Service proxy
            ("kubernetes", "kubernetes"),  # Container orchestration
            ("lima", "lima"),  # Linux VMs on Mac
            ("colima", "colima"),  # Container runtime
            ("rancher", "rancher"),  # K8s management
            ("portainer", "portainer"),  # Container UI
            
            # Testing & Quality
            ("jestjs", "jest"),  # Testing framework
            ("vitest-dev", "vitest"),  # Testing framework
            ("mswjs", "msw"),  # API mocking
            ("playwright", "playwright"),  # E2E testing
            ("cypress", "cypress"),  # E2E testing
            ("testing-library", "testing-library"),  # Testing utilities
            ("k6io", "k6"),  # Load testing
            ("gatling", "gatling"),  # Load testing
            ("locustio", "locust"),  # Load testing
            ("sonarsource", "sonarqube"),  # Code quality
            ("deepsource", "deepsource"),  # Code analysis
            ("codecov", "codecov"),  # Code coverage
            ("coveralls", "coveralls"),  # Code coverage
            
            # Security
            ("aquasecurity", "trivy"),  # Security scanner
            ("anchore", "grype"),  # Vulnerability scanner
            ("snyk", "snyk"),  # Security platform
            ("OWASP", "dependency-check"),  # Dependency scanner
            ("zmap", "zmap"),  # Network scanner
            ("microsoft", "gpt"),  # AI security
            ("trailofbits", "audit"),  # Security audit
        ]
        
        orch = get_orchestrator()
        results = []
        
        # Parallel processing
        with ThreadPoolExecutor(max_workers=5) as executor:
            future_to_repo = {
                executor.submit(orch.analyze_repo, owner, repo): (owner, repo)
                for owner, repo in trending_repos[:10]
            }
            
            for future in as_completed(future_to_repo):
                owner, repo = future_to_repo[future]
                try:
                    result = future.result(timeout=30)
                    if "error" not in result:
                        repo_data = result["repo_data"]
                        analysis = result.get("analysis", {})
                        
                        # Calculate trending score based on velocity
                        stars = repo_data.get("stars", 0)
                        forks = repo_data.get("forks", 0)
                        commits_last_year = repo_data.get("commits_last_year", 0)
                        contributors = repo_data.get("contributors", 0)
                        
                        # Trending score: recent activity weighted more heavily
                        trending_score = (
                            (commits_last_year / 100) * 0.4 +
                            (contributors / 10) * 0.3 +
                            (forks / (stars + 1)) * 0.2 +
                            (analysis.get("intervention_score", 0) / 100) * 0.1
                        )
                        
                        valuation = repo_valuation.calculate_valuation(
                            repo_data,
                            analysis
                        )
                        
                        results.append({
                            "repo": f"{owner}/{repo}",
                            "valuation": valuation,
                            "repo_data": repo_data,
                            "analysis": analysis,
                            "trending_score": trending_score
                        })
                except Exception as e:
                    logger.warning(f"Failed to analyze {owner}/{repo}: {str(e)}")
                    continue
        
        # Sort by trending score
        results.sort(key=lambda x: x["trending_score"], reverse=True)
        
        # Cache results
        discovery_cache[cache_key] = {
            "timestamp": current_time,
            "data": {"results": results, "count": len(results)}
        }
        
        logger.info(f"Trending discovery: {len(results)} repos")
        return jsonify({"results": results, "count": len(results)})
    except Exception as e:
        logger.error(f"Trending discovery failed: {str(e)}")
        return jsonify({"error": str(e)}), 500


@app.route('/api/discover/promising')
def discover_promising_repos():
    """Get promising repositories using Innovation Alpha = Expected Future Value - Current Recognition."""
    # Check cache
    cache_key = "promising"
    current_time = time.time()
    
    if cache_key in discovery_cache and current_time - discovery_cache[cache_key]["timestamp"] < CACHE_TTL:
        logger.info("Returning cached promising discovery results")
        return jsonify(discovery_cache[cache_key]["data"])
    
    try:
        # Predefined list of under-the-radar repos for promising analysis
        # Same expanded dataset as quality for consistency
        promising_repos = [
            # Terminal & CLI Tools
            ("starship", "starship"),  # Rust shell prompt
            ("atuinsh", "atuin"),  # Shell history
            ("zellij-org", "zellij"),  # Terminal multiplexer
            ("helix-editor", "helix"),  # Modal text editor
            ("eza-community", "eza"),  # Modern ls replacement
            ("fd-dev", "fd"),  # Find alternative
            ("sharkdp", "bat"),  # Cat alternative
            ("sharkdp", "ripgrep"),  # Grep alternative
            ("dandavison", "delta"),  # Git diff viewer
            ("junegunn", "fzf"),  # Fuzzy finder
            ("sxyazi", "yazi"),  # Terminal file manager
            ("nushell", "nushell"),  # Modern shell
            ("kovidgoyal", "kitty"),  # Terminal emulator
            ("alacritty", "alacritty"),  # Terminal emulator
            ("wez", "wezterm"),  # Terminal emulator
            ("charmbracelet", "gum"),  # Shell script UI
            ("charmbracelet", "lip Gloss"),  # TUI library
            ("charmbracelet", "bubbletea"),  # TUI framework
            ("c-batastrophe", "broot"),  # Tree viewer
            ("canopas", "tldr"),  # Simplified man pages
            ("o2sh", "onefetch"),  # Git info tool
            ("ogham", "exa"),  # Modern ls (deprecated but popular)
            
            # Build Tools & Package Managers
            ("golang", "go"),  # Go language
            ("rust-lang", "cargo"),  # Rust package manager
            ("pnpm", "pnpm"),  # Fast npm alternative
            ("yarnpkg", "yarn"),  # Package manager
            ("bun", "bun"),  # JS runtime
            ("denoland", "deno"),  # JS runtime
            ("sveltejs", "kit"),  # Svelte build tool
            ("vitejs", "vite"),  # Build tool
            ("swc-project", "swc"),  # JS/TS compiler
            ("esbuild", "esbuild"),  # JS bundler
            ("rome", "rome"),  # JS toolchain
            ("biomejs", "biome"),  # JS linter/formatter
            ("ruff-lang", "ruff"),  # Python linter
            ("astral-sh", "uv"),  # Python package manager
            ("mitsuhiko", "rye"),  # Python toolchain
            ("poetry", "poetry"),  # Python dependency manager
            ("pypa", "pip"),  # Python installer
            
            # Web Frameworks (Alternatives to React/Next.js)
            ("solidjs", "solid"),  # Reactive UI
            ("sveltejs", "svelte"),  # Component framework
            ("htmx", "htmx"),  # HTML extension
            ("hotwired", "turbo"),  # Rails framework
            ("phoenixframework", "phoenix"),  # Elixir framework
            ("lucacasonato", "remix"),  # React framework
            ("builderio", "qwik"),  # Resumable framework
            ("marko-js", "marko"),  # UI framework
            ("astro", "astro"),  # Web framework
            ("fresh", "fresh"),  # Deno framework
            ("elysiajs", "elysia"),  # Bun framework
            ("hono", "hono"),  # Web framework
            ("lit", "lit"),  # Web components
            ("fastify", "fastify"),  # Node framework
            ("poliastro", "poliastro"),  # Python web framework
            
            # Database Tools & ORMs
            ("prisma", "prisma"),  # TypeScript ORM
            ("drizzle-team", "drizzle-orm"),  # SQL ORM
            ("supabase", "supabase"),  # Backend platform
            ("planetscale", "planetscale"),  # Database platform
            ("xata", "xata"),  # Serverless database
            ("neondatabase", "neon"),  # Postgres platform
            ("turso", "turso"),  # SQLite platform
            ("libsql", "libsql"),  # SQLite fork
            ("duckdb", "duckdb"),  # Analytical database
            ("clickhouse", "clickhouse"),  # Columnar database
            ("timescale", "timescaledb"),  # Postgres extension
            ("pgvector", "pgvector"),  # Vector extension
            ("qdrant", "qdrant"),  # Vector database
            ("weaviate", "weaviate"),  # Vector database
            ("milvus-io", "milvus"),  # Vector database
            ("sequelize", "sequelize"),  # Node ORM
            ("typeorm", "typeorm"),  # TypeScript ORM
            ("sqlalchemy", "sqlalchemy"),  # Python ORM
            
            # DevOps & Infrastructure
            ("hashicorp", "terraform"),  # IaC tool
            ("hashicorp", "packer"),  # Image builder
            ("ansible", "ansible"),  # Automation
            ("puppetlabs", "puppet"),  # Configuration
            ("chef", "chef"),  # Configuration
            ("saltstack", "salt"),  # Automation
            ("grafana", "grafana"),  # Monitoring
            ("prometheus", "prometheus"),  # Monitoring
            ("loki", "loki"),  # Logging
            ("temporalio", "temporal"),  # Workflow engine
            ("dapr", "dapr"),  # Microservices runtime
            ("open-telemetry", "opentelemetry"),  # Observability
            ("envoyproxy", "envoy"),  # Service proxy
            ("kubernetes", "kubernetes"),  # Container orchestration
            ("lima", "lima"),  # Linux VMs on Mac
            ("colima", "colima"),  # Container runtime
            ("rancher", "rancher"),  # K8s management
            ("portainer", "portainer"),  # Container UI
            
            # Testing & Quality
            ("jestjs", "jest"),  # Testing framework
            ("vitest-dev", "vitest"),  # Testing framework
            ("mswjs", "msw"),  # API mocking
            ("playwright", "playwright"),  # E2E testing
            ("cypress", "cypress"),  # E2E testing
            ("testing-library", "testing-library"),  # Testing utilities
            ("k6io", "k6"),  # Load testing
            ("gatling", "gatling"),  # Load testing
            ("locustio", "locust"),  # Load testing
            ("sonarsource", "sonarqube"),  # Code quality
            ("deepsource", "deepsource"),  # Code analysis
            ("codecov", "codecov"),  # Code coverage
            ("coveralls", "coveralls"),  # Code coverage
            
            # Security
            ("aquasecurity", "trivy"),  # Security scanner
            ("anchore", "grype"),  # Vulnerability scanner
            ("snyk", "snyk"),  # Security platform
            ("OWASP", "dependency-check"),  # Dependency scanner
            ("zmap", "zmap"),  # Network scanner
            ("microsoft", "gpt"),  # AI security
            ("trailofbits", "audit"),  # Security audit
        ]
        
        orch = get_orchestrator()
        results = []
        
        # Parallel processing
        with ThreadPoolExecutor(max_workers=5) as executor:
            future_to_repo = {
                executor.submit(orch.analyze_repo, owner, repo): (owner, repo)
                for owner, repo in promising_repos[:10]
            }
            
            for future in as_completed(future_to_repo):
                owner, repo = future_to_repo[future]
                try:
                    result = future.result(timeout=30)
                    if "error" not in result:
                        repo_data = result["repo_data"]
                        analysis = result.get("analysis", {})
                        
                        valuation = repo_valuation.calculate_valuation(
                            repo_data,
                            analysis
                        )
                        
                        # Calculate Innovation Alpha
                        alpha_data = kpi_calculator.calculate_innovation_alpha(
                            repo_data,
                            analysis,
                            valuation
                        )
                        
                        results.append({
                            "repo": f"{owner}/{repo}",
                            "valuation": valuation,
                            "repo_data": repo_data,
                            "analysis": analysis,
                            "innovation_alpha": alpha_data["innovation_alpha"],
                            "expected_future_value": alpha_data["expected_future_value"],
                            "current_recognition": alpha_data["current_recognition"],
                            "kpis": alpha_data["kpis"],
                            "kpi_breakdown": alpha_data["kpi_breakdown"]
                        })
                except Exception as e:
                    logger.warning(f"Failed to analyze {owner}/{repo}: {str(e)}")
                    continue
        
        # Sort by innovation alpha (highest = most undervalued)
        results.sort(key=lambda x: x["innovation_alpha"], reverse=True)
        
        # Filter to show only positive alpha (undervalued assets)
        positive_alpha_results = [r for r in results if r["innovation_alpha"] > 0]
        
        # Cache results
        discovery_cache[cache_key] = {
            "timestamp": current_time,
            "data": {"results": positive_alpha_results, "count": len(positive_alpha_results)}
        }
        
        logger.info(f"Promising discovery: {len(positive_alpha_results)} undervalued repos (filtered from {len(results)} total)")
        return jsonify({"results": positive_alpha_results, "count": len(positive_alpha_results)})
    except Exception as e:
        logger.error(f"Promising discovery failed: {str(e)}")
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    port = int(os.getenv("PORT", 5001))
    debug = os.getenv("DEBUG", "false").lower() == "true"
    app.run(host='0.0.0.0', port=port, debug=debug)
