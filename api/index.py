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

# Global variable for mining status
mining_status = {"in_progress": False, "progress": 0, "total": 0, "message": ""}

# Import all routes from intervention_capture_ui
# Copy the route handlers here for Vercel compatibility

@app.route('/')
def index():
    """Dashboard showing all interventions."""
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

@app.route('/api/health')
def health():
    return jsonify({"status": "ok"})

# Vercel serverless handler
def handler(event, context):
    return app(event, context)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
