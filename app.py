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
from repo_dataset import get_expanded_repos

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
        # Use expanded dataset of 10,000 repos for database population
        quality_repos = get_expanded_repos()
        
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
        # Use expanded dataset of 10,000 repos for database population
        trending_repos = get_expanded_repos()
        
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
        # Use expanded dataset of 10,000 repos for database population
        promising_repos = get_expanded_repos()
        
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


@app.route('/api/database/populate', methods=['POST'])
def populate_database():
    """Populate outcome ledger with appraisals from dataset."""
    try:
        # Get parameters
        count = int(request.json.get('count', 100))
        offset = int(request.json.get('offset', 0))
        
        # Get repos from expanded dataset
        all_repos = get_expanded_repos()
        repos_to_analyze = all_repos[offset:offset + count]
        
        logger.info(f"Populating database with {len(repos_to_analyze)} repos (offset: {offset})")
        
        orch = get_orchestrator()
        results = []
        appraisals_created = 0
        errors = 0
        
        # Parallel processing
        with ThreadPoolExecutor(max_workers=5) as executor:
            future_to_repo = {
                executor.submit(orch.analyze_repo, owner, repo): (owner, repo)
                for owner, repo in repos_to_analyze
            }
            
            for future in as_completed(future_to_repo):
                owner, repo = future_to_repo[future]
                try:
                    result = future.result()
                    if "error" not in result:
                        repo_data = result.get("repo_data", {})
                        analysis = result.get("analysis", {})
                        valuation = analysis.get("valuation", {})
                        
                        # Create appraisal record in outcome ledger
                        appraisal_data = {
                            "repo": f"{owner}/{repo}",
                            "repo_data": repo_data,
                            "analysis": analysis,
                            "valuation": valuation,
                            "innovation_alpha": valuation.get("innovation_alpha", 0),
                            "expected_future_value": valuation.get("expected_future_value", 0),
                            "current_recognition": valuation.get("current_recognition", 0),
                            "intervention_score": analysis.get("intervention_score", 0),
                            "best_intervention": analysis.get("best_intervention", {}),
                            "overall_confidence": valuation.get("overall_confidence", 0),
                            "evidence_strength": valuation.get("evidence_strength", 0),
                            "model_confidence": valuation.get("model_confidence", 0),
                            "data_coverage": valuation.get("data_coverage", 0),
                        }
                        
                        results.append(appraisal_data)
                        appraisals_created += 1
                    else:
                        errors += 1
                        logger.error(f"Error analyzing {owner}/{repo}: {result.get('error')}")
                except Exception as e:
                    errors += 1
                    logger.error(f"Error processing {owner}/{repo}: {e}")
        
        logger.info(f"Database population complete: {appraisals_created} appraisals created, {errors} errors")
        
        return jsonify({
            "success": True,
            "appraisals_created": appraisals_created,
            "errors": errors,
            "offset": offset,
            "count": len(repos_to_analyze),
            "results": results[:10],  # Return first 10 for preview
            "total_in_dataset": len(all_repos)
        })
        
    except Exception as e:
        logger.error(f"Error populating database: {e}")
        return jsonify({"success": False, "error": str(e)}), 500


if __name__ == "__main__":
    port = int(os.getenv("PORT", 5001))
    debug = os.getenv("DEBUG", "false").lower() == "true"
    app.run(host='0.0.0.0', port=port, debug=debug)
