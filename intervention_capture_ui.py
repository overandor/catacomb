"""Intervention Capture UI - Fast data-entry workflow for logging interventions."""
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from outcome_ledger_v2 import OutcomeLedger, InterventionStatus, VerificationStatus
from innovation_elo import InnovationElo, EloEntityType
from transformation_tracking import TransformationTracker
from github_intervention_miner import GitHubInterventionMiner, seed_mined_interventions
from datetime import datetime
import json
import threading

app = Flask(__name__)
app.secret_key = 'catacomb-intervention-capture'

# Initialize systems
ledger = OutcomeLedger("outcome_ledger.db")
elo_system = InnovationElo()
transformation_tracker = TransformationTracker()

# Global variable for mining status
mining_status = {"in_progress": False, "progress": 0, "total": 0, "message": ""}


@app.route('/')
def index():
    """Dashboard showing all interventions."""
    # Get all interventions from SQLite
    import sqlite3
    conn = sqlite3.connect(ledger.db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM interventions ORDER BY created_at DESC")
    rows = cursor.fetchall()
    columns = [desc[0] for desc in cursor.description]
    
    records = []
    for row in rows:
        record = dict(zip(columns, row))
        # Parse JSON fields
        for json_field in ['before_state', 'predicted_outcome', 'after_state', 'outcome_metrics', 'prediction_accuracy']:
            if record[json_field]:
                record[json_field] = json.loads(record[json_field])
        records.append(record)
    
    conn.close()
    
    # Get stats
    total = len(records)
    completed = len([r for r in records if r['status'] == InterventionStatus.COMPLETED.value])
    verified = len([r for r in records if r['verification_status'] == VerificationStatus.VERIFIED.value])
    
    return render_template('index.html', 
                         records=records, 
                         total=total, 
                         completed=completed, 
                         verified=verified)


@app.route('/capture', methods=['GET', 'POST'])
def capture():
    """Fast intervention capture form."""
    if request.method == 'POST':
        try:
            # Extract form data
            asset_id = request.form.get('asset_id')
            asset_type = request.form.get('asset_type')
            asset_name = request.form.get('asset_name')
            developer_id = request.form.get('developer_id')
            developer_username = request.form.get('developer_username')
            intervention_type = request.form.get('intervention_type')
            intervention_description = request.form.get('intervention_description')
            planned_effort_days = int(request.form.get('planned_effort_days', 0))
            predicted_value = float(request.form.get('predicted_value', 0))
            predicted_probability = float(request.form.get('predicted_probability', 0))
            predicted_risk = float(request.form.get('predicted_risk', 0))
            
            # Get before state from form (JSON string)
            before_state_json = request.form.get('before_state', '{}')
            before_state = json.loads(before_state_json)
            
            # Create intervention record
            record_id = ledger.create_intervention(
                asset_id=asset_id,
                asset_type=asset_type,
                asset_name=asset_name,
                developer_id=developer_id,
                developer_username=developer_username,
                before_state=before_state,
                intervention_type=intervention_type,
                intervention_description=intervention_description,
                planned_effort_days=planned_effort_days,
                predicted_value=predicted_value,
                predicted_probability=predicted_probability,
                predicted_risk=predicted_risk
            )
            
            flash(f'Intervention captured successfully! Record ID: {record_id}', 'success')
            return redirect(url_for('index'))
            
        except Exception as e:
            flash(f'Error capturing intervention: {str(e)}', 'error')
            return redirect(url_for('capture'))
    
    return render_template('capture.html')


@app.route('/quick_capture', methods=['GET', 'POST'])
def quick_capture():
    """Ultra-fast capture for GitHub repos (minimal fields)."""
    if request.method == 'POST':
        try:
            # Minimal required fields
            repo_id = request.form.get('repo_id')  # owner/repo format
            intervention_type = request.form.get('intervention_type')
            planned_effort_days = int(request.form.get('planned_effort_days', 0))
            predicted_value = float(request.form.get('predicted_value', 0))
            developer_username = request.form.get('developer_username')
            
            # Parse repo_id
            owner, repo = repo_id.split('/')
            
            # Auto-generate other fields
            asset_id = repo_id
            asset_type = "github_repo"
            asset_name = repo
            developer_id = f"github:{developer_username}"
            intervention_description = f"{intervention_type} on {repo_id}"
            predicted_probability = 0.7  # Default
            predicted_risk = 0.3  # Default
            
            # Minimal before state
            before_state = {
                "repo_id": repo_id,
                "owner": owner,
                "repo": repo
            }
            
            # Create record
            record_id = ledger.create_intervention(
                asset_id=asset_id,
                asset_type=asset_type,
                asset_name=asset_name,
                developer_id=developer_id,
                developer_username=developer_username,
                before_state=before_state,
                intervention_type=intervention_type,
                intervention_description=intervention_description,
                planned_effort_days=planned_effort_days,
                predicted_value=predicted_value,
                predicted_probability=predicted_probability,
                predicted_risk=predicted_risk
            )
            
            flash(f'Quick capture successful! Record ID: {record_id}', 'success')
            return redirect(url_for('quick_capture'))
            
        except Exception as e:
            flash(f'Error: {str(e)}', 'error')
            return redirect(url_for('quick_capture'))
    
    return render_template('quick_capture.html')


@app.route('/record/<record_id>')
def view_record(record_id):
    """View a specific intervention record."""
    record = ledger.get_intervention(record_id)
    
    if not record:
        flash('Record not found', 'error')
        return redirect(url_for('index'))
    
    # Get developer Elo rating
    developer_rating = elo_system.get_entity_rating(record['developer_id'], EloEntityType.DEVELOPER)
    
    return render_template('view_record.html', record=record, developer_rating=developer_rating)


@app.route('/start/<record_id>', methods=['POST'])
def start_intervention(record_id):
    """Mark intervention as started."""
    try:
        actual_effort_days = request.form.get('actual_effort_days')
        actual_effort_days = int(actual_effort_days) if actual_effort_days else None
        
        ledger.start_intervention(record_id, actual_effort_days)
        flash('Intervention started', 'success')
    except Exception as e:
        flash(f'Error: {str(e)}', 'error')
    
    return redirect(url_for('view_record', record_id=record_id))


@app.route('/complete/<record_id>', methods=['POST'])
def complete_intervention(record_id):
    """Mark intervention as completed with outcome data."""
    try:
        # Extract outcome data
        after_state_json = request.form.get('after_state', '{}')
        after_state = json.loads(after_state_json)
        
        outcome_metrics_json = request.form.get('outcome_metrics', '{}')
        outcome_metrics = json.loads(outcome_metrics_json)
        
        actual_effort_days = request.form.get('actual_effort_days')
        actual_effort_days = int(actual_effort_days) if actual_effort_days else None
        
        # Complete intervention
        ledger.complete_intervention(
            record_id,
            after_state,
            outcome_metrics,
            actual_effort_days
        )
        
        # Update Elo ratings
        record = ledger.get_intervention(record_id)
        if record and record.get('outcome_metrics'):
            actual_value = record['outcome_metrics'].get('actual_value', 0)
            elo_system.update_from_intervention(
                record['developer_id'],
                record['intervention_type'],
                record['predicted_value'],
                actual_value
            )
        
        flash('Intervention completed and Elo ratings updated', 'success')
    except Exception as e:
        flash(f'Error: {str(e)}', 'error')
    
    return redirect(url_for('view_record', record_id=record_id))


@app.route('/verify/<record_id>', methods=['POST'])
def verify_intervention(record_id):
    """Verify an intervention outcome."""
    try:
        verifier_id = request.form.get('verifier_id')
        verifier_username = verifier_id.split(':')[-1] if ':' in verifier_id else verifier_id
        status = request.form.get('status')
        notes = request.form.get('notes')
        
        ledger.verify_outcome(
            record_id,
            verifier_id,
            verifier_username,
            status,
            notes
        )
        flash('Intervention verified', 'success')
    except Exception as e:
        flash(f'Error: {str(e)}', 'error')
    
    return redirect(url_for('view_record', record_id=record_id))


@app.route('/leaderboard')
def leaderboard():
    """Developer leaderboard based on Elo ratings."""
    developers = elo_system.get_developer_leaderboard(limit=20)
    interventions = elo_system.get_intervention_type_leaderboard(limit=10)
    
    return render_template('leaderboard.html', developers=developers, interventions=interventions)


@app.route('/stats')
def stats():
    """System statistics."""
    # Get learning metrics from SQLite
    import sqlite3
    conn = sqlite3.connect(ledger.db_path)
    cursor = conn.cursor()
    
    # Get completed interventions
    cursor.execute("SELECT COUNT(*) FROM interventions WHERE status = ?", (InterventionStatus.COMPLETED.value,))
    total_completed = cursor.fetchone()[0]
    
    # Get verified interventions
    cursor.execute("SELECT COUNT(*) FROM interventions WHERE verification_status = ?", (VerificationStatus.VERIFIED.value,))
    total_verified = cursor.fetchone()[0]
    
    # Get average prediction accuracy
    cursor.execute("SELECT prediction_accuracy FROM interventions WHERE status = ? AND prediction_accuracy IS NOT NULL", (InterventionStatus.COMPLETED.value,))
    accuracies = []
    for row in cursor.fetchall():
        if row[0]:
            acc = json.loads(row[0])
            accuracies.append(acc.get('overall_error', 0))
    
    avg_value_accuracy = 1 - sum(accuracies) / len(accuracies) if accuracies else 0
    
    # Get intervention success rates
    cursor.execute("""
        SELECT intervention_type, COUNT(*) as total, 
               SUM(CASE WHEN verification_status = ? THEN 1 ELSE 0 END) as successful
        FROM interventions 
        WHERE status = ?
        GROUP BY intervention_type
    """, (VerificationStatus.VERIFIED.value, InterventionStatus.COMPLETED.value))
    
    intervention_success_rates = {}
    for row in cursor.fetchall():
        intervention_type, total, successful = row
        intervention_success_rates[intervention_type] = {
            "total": total,
            "successful": successful,
            "success_rate": successful / total if total > 0 else 0
        }
    
    conn.close()
    
    learning_metrics = {
        "total_completed": total_completed,
        "avg_value_accuracy": avg_value_accuracy,
        "avg_probability_accuracy": avg_value_accuracy,  # Simplified
        "overall_accuracy": avg_value_accuracy,
        "intervention_success_rates": intervention_success_rates
    }
    
    return render_template('stats.html', metrics=learning_metrics)


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
    repo_input = request.form.get('repos', '')  # Comma-separated repos
    limit_per_repo = int(request.form.get('limit_per_repo', 20))
    
    if not github_token:
        return jsonify({"error": "GitHub token required"}), 400
    
    # Parse repos
    repos = []
    if repo_input:
        for repo in repo_input.split(','):
            repo = repo.strip()
            if '/' in repo:
                owner, name = repo.split('/', 1)
                repos.append((owner, name))
    
    # Default repos if none provided
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
    
    # Update status
    mining_status["in_progress"] = True
    mining_status["progress"] = 0
    mining_status["total"] = len(repos)
    mining_status["message"] = "Initializing miner..."
    
    # Start mining in background thread
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
            
            # Seed interventions
            seeded = seed_mined_interventions(
                all_interventions,
                ledger,
                elo_system,
                transformation_tracker
            )
            
            # Save Elo and patterns
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


if __name__ == '__main__':
    app.run(debug=True, port=5000)
