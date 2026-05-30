import sys
import os

# Add parent directory to path to import modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Flask, jsonify, render_template, request, redirect, url_for, flash
from flask_cors import CORS
from outcome_ledger_v2 import OutcomeLedger, InterventionStatus, VerificationStatus
from innovation_elo import InnovationElo, EloEntityType
from transformation_tracking import TransformationTracker
from github_intervention_miner import GitHubInterventionMiner, seed_mined_interventions
from catacomb_radar import CatacombRadar, RadarSignal
from universe_classifier import UniverseClassifier, AssetMetrics, Universe
from prediction_accuracy import PredictionAccuracyTracker
from package_ecosystem_miner import PackageEcosystemMiner, seed_package_interventions
from datetime import datetime
import json
import threading

app = Flask(__name__, template_folder='../templates', static_folder='../static')
CORS(app)
app.secret_key = os.environ.get('SECRET_KEY', 'catacomb-intervention-capture')

# Initialize systems with environment-aware database path
if os.environ.get('VERCEL'):
    db_path = '/tmp/outcome_ledger.db'
else:
    db_path = os.environ.get('DATABASE_PATH', 'outcome_ledger.db')
ledger = OutcomeLedger(db_path)
elo_system = InnovationElo()
transformation_tracker = TransformationTracker()
radar = CatacombRadar()
classifier = UniverseClassifier()
accuracy_tracker = PredictionAccuracyTracker()
package_miner = PackageEcosystemMiner(db_path)

# Load existing predictions from ledger
accuracy_tracker.load_records_from_ledger(ledger)

# Global variable for mining status
mining_status = {"in_progress": False, "progress": 0, "total": 0, "message": ""}

# Import all routes from intervention_capture_ui
# Copy the route handlers here for Vercel compatibility

@app.route('/')
def index():
    """Sophisticated landing page."""
    return render_template('landing.html')

@app.route('/dashboard')
def dashboard():
    """Legacy dashboard showing all interventions."""
    import sqlite3
    conn = sqlite3.connect(ledger.db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM interventions ORDER BY created_at DESC")
    rows = cursor.fetchall()
    columns = [desc[0] for desc in cursor.description]
    
    records = []
    for row in rows:
        record = dict(zip(columns, row))
        for json_field in ['before_state', 'predicted_outcome', 'after_state', 'outcome_metrics', 'prediction_accuracy']:
            if record[json_field]:
                record[json_field] = json.loads(record[json_field])
        records.append(record)
    
    conn.close()
    
    total = len(records)
    completed = len([r for r in records if r['status'] == InterventionStatus.COMPLETED.value])
    verified = len([r for r in records if r['verification_status'] == VerificationStatus.VERIFIED.value])
    
    return render_template('index.html', records=records, total=total, completed=completed, verified=verified)

@app.route('/mine')
def mine():
    """GitHub intervention mining interface."""
    return render_template('mine.html', mining_status=mining_status)

@app.route('/mine/start', methods=['POST'])
def start_mining():
    """Start GitHub intervention mining in background thread."""
    global mining_status
    
    if mining_status["in_progress"]:
        return jsonify({"error": "Mining already in progress"}), 400
    
    github_token = request.form.get('github_token')
    repo_input = request.form.get('repos', '')
    limit_per_repo = int(request.form.get('limit_per_repo', 20))
    
    if not github_token:
        return jsonify({"error": "GitHub token required"}), 400
    
    repos = []
    if repo_input:
        for repo in repo_input.split(','):
            repo = repo.strip()
            if '/' in repo:
                owner, name = repo.split('/', 1)
                repos.append((owner, name))
    
    if not repos:
        repos = [
            ("vercel", "next.js"),
            ("facebook", "react"),
            ("vuejs", "vue"),
            ("sveltejs", "svelte"),
            ("microsoft", "typescript"),
            ("golang", "go"),
            ("rust-lang", "rust"),
            ("docker", "docker"),
            ("kubernetes", "kubernetes"),
            ("tensorflow", "tensorflow"),
            ("pytorch", "pytorch"),
            ("openai", "openai-python"),
            ("langchain-ai", "langchain"),
            ("supabase", "supabase"),
            ("prisma", "prisma")
        ]
    
    mining_status["in_progress"] = True
    mining_status["progress"] = 0
    mining_status["total"] = len(repos)
    mining_status["message"] = "Initializing miner..."
    
    def mine_thread():
        global mining_status
        try:
            miner = GitHubInterventionMiner(github_token)
            
            all_interventions = []
            for i, (owner, repo) in enumerate(repos):
                mining_status["message"] = f"Mining {owner}/{repo}..."
                mining_status["progress"] = i
                
                try:
                    interventions = miner.mine_repository(owner, repo, limit_per_repo)
                    all_interventions.extend(interventions)
                except Exception as e:
                    mining_status["message"] = f"Error mining {owner}/{repo}: {str(e)}"
            
            mining_status["message"] = f"Seeding {len(all_interventions)} interventions..."
            
            seeded = seed_mined_interventions(
                all_interventions,
                ledger,
                elo_system,
                transformation_tracker
            )
            
            elo_system.save_to_file("elo_ratings.json")
            transformation_tracker.export_patterns("transformation_patterns.json")
            
            mining_status["message"] = f"Completed: {seeded} interventions seeded"
            mining_status["progress"] = len(repos)
            
        except Exception as e:
            mining_status["message"] = f"Error: {str(e)}"
        finally:
            mining_status["in_progress"] = False
    
    thread = threading.Thread(target=mine_thread)
    thread.daemon = True
    thread.start()
    
    return jsonify({"status": "started", "repos_count": len(repos)})

@app.route('/mine/status')
def mining_status_api():
    """Get current mining status."""
    return jsonify(mining_status)

@app.route('/api/mine/packages', methods=['POST'])
def start_package_mining():
    """Start mining package ecosystems (npm, PyPI, crates.io)."""
    data = request.get_json()
    npm_packages = data.get('npm_packages', 10)
    pypi_packages = data.get('pypi_packages', 10)
    crates = data.get('crates', 10)
    limit_per_package = data.get('limit_per_package', 10)
    
    mining_status["in_progress"] = True
    mining_status["message"] = "Mining package ecosystems..."
    mining_status["progress"] = 0
    mining_status["total"] = npm_packages + pypi_packages + crates
    
    def mine_packages():
        try:
            from package_ecosystem_miner import HIGH_VALUE_NPM_PACKAGES, HIGH_VALUE_PYPI_PACKAGES, HIGH_VALUE_CRATES
            
            npm_count = package_miner.mine_npm_packages(
                HIGH_VALUE_NPM_PACKAGES[:npm_packages], 
                limit_per_package=limit_per_package
            )
            mining_status["progress"] = npm_packages
            mining_status["message"] = f"Mined {npm_count} npm interventions"
            
            pypi_count = package_miner.mine_pypi_packages(
                HIGH_VALUE_PYPI_PACKAGES[:pypi_packages],
                limit_per_package=limit_per_package
            )
            mining_status["progress"] = npm_packages + pypi_packages
            mining_status["message"] = f"Mined {npm_count} npm, {pypi_count} PyPI interventions"
            
            crates_count = package_miner.mine_crates_packages(
                HIGH_VALUE_CRATES[:crates],
                limit_per_package=limit_per_package
            )
            mining_status["progress"] = npm_packages + pypi_packages + crates
            mining_status["message"] = f"Mined {npm_count} npm, {pypi_count} PyPI, {crates_count} crate interventions"
            
            mining_status["in_progress"] = False
            mining_status["message"] = f"Package mining complete: {npm_count + pypi_count + crates_count} total interventions"
            
        except Exception as e:
            mining_status["in_progress"] = False
            mining_status["message"] = f"Error: {str(e)}"
    
    thread = threading.Thread(target=mine_packages)
    thread.daemon = True
    thread.start()
    
    return jsonify({"status": "started", "message": "Package mining started"})

@app.route('/radar')
def catacomb_radar():
    """Catacomb Radar - Hidden infrastructure opportunities."""
    top_signals = radar.get_top_signals(limit=50)
    summary = radar.get_radar_summary()
    return render_template('radar.html', signals=top_signals, summary=summary)

@app.route('/alpha')
def alpha_page():
    """Innovation Alpha - Undervalued software assets."""
    return render_template('alpha.html')

@app.route('/interventions')
def interventions_page():
    """Intervention Intelligence - Ranked by value per engineering day."""
    return render_template('interventions.html')

@app.route('/ledger')
def ledger_page():
    """Institutional Audit Ledger - Trust layer."""
    return render_template('ledger.html')

@app.route('/swipe')
def swipe_page():
    """Premium Asset Discovery - Swipe interface."""
    return render_template('swipe.html')

@app.route('/api/radar/summary')
def radar_summary_api():
    """Get radar summary statistics."""
    return jsonify(radar.get_radar_summary())

@app.route('/api/radar/signals')
def radar_signals_api():
    """Get all radar signals."""
    limit = request.args.get('limit', 50, type=int)
    return jsonify([{
        "asset_id": s.asset_id,
        "asset_name": s.asset_name,
        "asset_type": s.asset_type,
        "expected_value_per_day": s.expected_value_per_day,
        "best_intervention": s.best_intervention,
        "effort_days_estimate": s.effort_days_estimate,
        "confidence": s.confidence,
        "signal_strength": s.signal_strength,
        "evidence": s.evidence
    } for s in radar.get_top_signals(limit)])

@app.route('/api/radar/allocate', methods=['POST'])
def radar_allocation_api():
    """Calculate optimal portfolio allocation."""
    data = request.get_json()
    total_days = data.get('total_engineering_days', 30)
    allocation = radar.calculate_portfolio_allocation(total_days)
    return jsonify(allocation)

@app.route('/api/v1/stats')
def api_stats():
    """Comprehensive system statistics."""
    import sqlite3
    conn = sqlite3.connect(ledger.db_path)
    cursor = conn.cursor()
    
    # Count total interventions
    cursor.execute("SELECT COUNT(*) FROM interventions")
    total_interventions = cursor.fetchone()[0]
    
    # Count verified
    cursor.execute("SELECT COUNT(*) FROM interventions WHERE verification_status = ?", (VerificationStatus.VERIFIED.value,))
    verified = cursor.fetchone()[0]
    
    # Count completed
    cursor.execute("SELECT COUNT(*) FROM interventions WHERE status = ?", (InterventionStatus.COMPLETED.value,))
    completed = cursor.fetchone()[0]
    
    # Average predicted value
    cursor.execute("SELECT AVG(CAST(json_extract(predicted_outcome, '$.value') AS FLOAT)) FROM interventions WHERE predicted_outcome IS NOT NULL")
    avg_predicted = cursor.fetchone()[0] or 0
    
    # Average actual value
    cursor.execute("SELECT AVG(CAST(json_extract(outcome_metrics, '$.actual_value') AS FLOAT)) FROM interventions WHERE outcome_metrics IS NOT NULL")
    avg_actual = cursor.fetchone()[0] or 0
    
    # Unique assets
    cursor.execute("SELECT COUNT(DISTINCT asset_id) FROM interventions")
    unique_assets = cursor.fetchone()[0]
    
    # Top intervention types
    cursor.execute("SELECT intervention_type, COUNT(*) as count FROM interventions GROUP BY intervention_type ORDER BY count DESC LIMIT 5")
    top_types = [{"type": row[0], "count": row[1]} for row in cursor.fetchall()]
    
    conn.close()
    
    return jsonify({
        "total_interventions": total_interventions,
        "verified_interventions": verified,
        "completed_interventions": completed,
        "average_predicted_value": round(avg_predicted, 2),
        "average_actual_value": round(avg_actual, 2),
        "unique_assets": unique_assets,
        "top_intervention_types": top_types,
        "prediction_accuracy": accuracy_tracker.get_accuracy_report(),
        "radar_summary": radar.get_radar_summary(),
        "timestamp": datetime.utcnow().isoformat()
    })

@app.route('/api/v1/interventions')
def api_interventions():
    """Paginated list of all interventions."""
    import sqlite3
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    status_filter = request.args.get('status')
    type_filter = request.args.get('type')
    
    conn = sqlite3.connect(ledger.db_path)
    cursor = conn.cursor()
    
    query = "SELECT * FROM interventions WHERE 1=1"
    params = []
    
    if status_filter:
        query += " AND status = ?"
        params.append(status_filter)
    if type_filter:
        query += " AND intervention_type = ?"
        params.append(type_filter)
    
    query += " ORDER BY created_at DESC LIMIT ? OFFSET ?"
    params.extend([per_page, (page - 1) * per_page])
    
    cursor.execute(query, params)
    rows = cursor.fetchall()
    columns = [desc[0] for desc in cursor.description]
    
    records = []
    for row in rows:
        record = dict(zip(columns, row))
        for json_field in ['before_state', 'predicted_outcome', 'after_state', 'outcome_metrics']:
            if record.get(json_field):
                try:
                    record[json_field] = json.loads(record[json_field])
                except:
                    pass
        records.append(record)
    
    # Get total count
    count_query = "SELECT COUNT(*) FROM interventions WHERE 1=1"
    count_params = []
    if status_filter:
        count_query += " AND status = ?"
        count_params.append(status_filter)
    if type_filter:
        count_query += " AND intervention_type = ?"
        count_params.append(type_filter)
    
    cursor.execute(count_query, count_params)
    total = cursor.fetchone()[0]
    
    conn.close()
    
    return jsonify({
        "interventions": records,
        "pagination": {
            "page": page,
            "per_page": per_page,
            "total": total,
            "pages": (total + per_page - 1) // per_page
        }
    })

@app.route('/api/v1/assets')
def api_assets():
    """List of tracked assets with metrics."""
    import sqlite3
    conn = sqlite3.connect(ledger.db_path)
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT 
            asset_id,
            asset_name,
            asset_type,
            COUNT(*) as intervention_count,
            AVG(CAST(json_extract(predicted_outcome, '$.value') AS FLOAT)) as avg_predicted_value,
            MAX(created_at) as last_intervention
        FROM interventions 
        GROUP BY asset_id 
        ORDER BY intervention_count DESC
    """)
    
    rows = cursor.fetchall()
    assets = []
    for row in rows:
        assets.append({
            "asset_id": row[0],
            "asset_name": row[1],
            "asset_type": row[2],
            "intervention_count": row[3],
            "avg_predicted_value": round(row[4] or 0, 2),
            "last_intervention": row[5]
        })
    
    conn.close()
    return jsonify({"assets": assets, "total": len(assets)})

@app.route('/api/v1/intervention/<intervention_id>')
def api_intervention_detail(intervention_id):
    """Get detailed information about a specific intervention."""
    import sqlite3
    conn = sqlite3.connect(ledger.db_path)
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM interventions WHERE id = ?", (intervention_id,))
    row = cursor.fetchone()
    
    if not row:
        conn.close()
        return jsonify({"error": "Intervention not found"}), 404
    
    columns = [desc[0] for desc in cursor.description]
    record = dict(zip(columns, row))
    
    for json_field in ['before_state', 'predicted_outcome', 'after_state', 'outcome_metrics']:
        if record.get(json_field):
            try:
                record[json_field] = json.loads(record[json_field])
            except:
                pass
    
    conn.close()
    return jsonify(record)

@app.route('/api/health')
def health():
    return jsonify({"status": "ok", "version": "2.0", "timestamp": datetime.utcnow().isoformat()})

@app.route('/api/accuracy/report')
def accuracy_report_api():
    """Get prediction accuracy report."""
    return jsonify(accuracy_tracker.get_accuracy_report())

@app.route('/api/accuracy/baseline', methods=['POST'])
def set_baseline_api():
    """Set current metrics as baseline for drift calculation."""
    accuracy_tracker.set_baseline()
    return jsonify({"status": "baseline_set", "timestamp": datetime.utcnow().isoformat()})

# Google OAuth
from authlib.integrations.flask_client import OAuth

oauth = OAuth(app)

google = oauth.register(
    name='google',
    client_id=os.environ.get('GOOGLE_CLIENT_ID', ''),
    client_secret=os.environ.get('GOOGLE_CLIENT_SECRET', ''),
    access_token_url='https://accounts.google.com/o/oauth2/token',
    access_token_params=None,
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    authorize_params=None,
    api_base_url='https://www.googleapis.com/oauth2/v1/',
    client_kwargs={
        'scope': 'openid email profile',
        'token_endpoint_auth_method': 'client_secret_basic',
    },
    jwks_uri='https://www.googleapis.com/oauth2/v3/certs',
)

@app.route('/login')
def login():
    """Initiate Google OAuth login."""
    redirect_uri = url_for('authorize', _external=True)
    # Handle Vercel HTTPS proxy
    if os.environ.get('VERCEL'):
        redirect_uri = redirect_uri.replace('http://', 'https://')
    return google.authorize_redirect(redirect_uri)

@app.route('/auth/google/callback')
def authorize():
    """Handle Google OAuth callback."""
    try:
        token = google.authorize_access_token()
        resp = google.get('userinfo')
        user_info = resp.json()
        
        # Store user info in cookie (JWT-like simple approach for Vercel)
        import base64
        user_data = json.dumps({
            'email': user_info.get('email'),
            'name': user_info.get('name'),
            'picture': user_info.get('picture'),
            'sub': user_info.get('id')
        })
        
        response = redirect('/radar')
        response.set_cookie('catacomb_user', base64.b64encode(user_data.encode()).decode(), 
                           max_age=86400, httponly=True, samesite='Lax')
        return response
    except Exception as e:
        flash(f'Authentication failed: {str(e)}', 'error')
        return redirect('/')

@app.route('/logout')
def logout():
    """Clear user session."""
    response = redirect('/')
    response.set_cookie('catacomb_user', '', expires=0)
    return response

@app.route('/api/user')
def api_user():
    """Get current user info from cookie."""
    import base64
    user_cookie = request.cookies.get('catacomb_user')
    if not user_cookie:
        return jsonify({"authenticated": False})
    
    try:
        user_data = json.loads(base64.b64decode(user_cookie).decode())
        return jsonify({"authenticated": True, "user": user_data})
    except:
        return jsonify({"authenticated": False})

# Vercel serverless handler
def handler(event, context):
    return app(event, context)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
