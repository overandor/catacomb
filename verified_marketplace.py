"""Verified Intervention Marketplace - reputation system with Innovation Elo."""
from flask import Flask, render_template, request, redirect, url_for, flash
from outcome_ledger import OutcomeLedger, InterventionStatus, VerificationStatus
from innovation_elo import InnovationElo, EloEntityType, PredictionAccuracyTracker
from transformation_tracking import TransformationTracker, PatternDiscovery
from datetime import datetime
import json

app = Flask(__name__)
app.secret_key = 'catacomb-marketplace'

# Initialize systems
ledger = OutcomeLedger("outcome_ledger.json")
elo_system = InnovationElo()
accuracy_tracker = PredictionAccuracyTracker()
transformation_tracker = TransformationTracker()
pattern_discovery = PatternDiscovery(transformation_tracker)


@app.route('/')
def index():
    """Marketplace homepage."""
    # Get featured interventions
    completed_records = [r for r in ledger.records.values() if r.status == InterventionStatus.COMPLETED]
    verified_records = [r for r in completed_records if r.verification_status == VerificationStatus.VERIFIED]
    
    # Sort by innovation alpha (predicted - actual difference)
    featured = sorted(
        verified_records,
        key=lambda r: abs(r.predicted_value - (r.outcome_metrics.get("actual_value", 0) if r.outcome_metrics else 0)),
        reverse=True
    )[:10]
    
    # Get top developers
    top_developers = elo_system.get_developer_leaderboard(limit=10)
    
    # Get reusable laws
    laws = transformation_tracker.get_reusable_laws(min_confidence=0.7, min_samples=3)
    
    return render_template('marketplace_index.html',
                         featured=featured,
                         top_developers=top_developers,
                         laws=laws)


@app.route('/interventions')
def interventions():
    """Browse all interventions."""
    records = list(ledger.records.values())
    
    # Filter by status
    status_filter = request.args.get('status')
    if status_filter:
        records = [r for r in records if r.status.value == status_filter]
    
    # Filter by verification
    verification_filter = request.args.get('verification')
    if verification_filter:
        records = [r for r in records if r.verification_status.value == verification_filter]
    
    # Sort by created_at
    records.sort(key=lambda r: r.created_at, reverse=True)
    
    return render_template('interventions.html', records=records)


@app.route('/developers')
def developers():
    """Browse developers by reputation."""
    developers = elo_system.get_developer_leaderboard(limit=50)
    
    return render_template('developers.html', developers=developers)


@app.route('/developer/<developer_id>')
def developer_profile(developer_id):
    """View developer profile."""
    rating = elo_system.get_entity_rating(developer_id, EloEntityType.DEVELOPER)
    percentile = elo_system.get_percentile(developer_id, EloEntityType.DEVELOPER)
    
    # Get developer's interventions
    developer_records = ledger.get_developer_records(developer_id)
    
    # Calculate stats
    completed = [r for r in developer_records if r.status == InterventionStatus.COMPLETED]
    verified = [r for r in completed if r.verification_status == VerificationStatus.VERIFIED]
    
    # Calculate average prediction accuracy
    accuracies = []
    for record in completed:
        accuracy = record.calculate_prediction_accuracy()
        if accuracy:
            accuracies.append(accuracy.get("overall_accuracy", 0))
    
    avg_accuracy = sum(accuracies) / len(accuracies) if accuracies else 0
    
    return render_template('developer_profile.html',
                         developer_id=developer_id,
                         rating=rating,
                         percentile=percentile,
                         total_interventions=len(developer_records),
                         completed=len(completed),
                         verified=len(verified),
                         avg_accuracy=avg_accuracy,
                         records=developer_records)


@app.route('/laws')
def laws():
    """Browse reusable transformation laws."""
    all_laws = transformation_tracker.get_reusable_laws(min_confidence=0.6, min_samples=2)
    
    # Group by asset type
    by_asset_type = {}
    for law in all_laws:
        asset_type = law["pattern"]["asset_type"]
        if asset_type not in by_asset_type:
            by_asset_type[asset_type] = []
        by_asset_type[asset_type].append(law)
    
    return render_template('laws.html', laws=all_laws, by_asset_type=by_asset_type)


@app.route('/verify')
def verify_queue():
    """Queue of interventions awaiting verification."""
    pending_records = [
        r for r in ledger.records.values()
        if r.status == InterventionStatus.COMPLETED
        and r.verification_status == VerificationStatus.PENDING
    ]
    
    # Sort by completion date (oldest first)
    pending_records.sort(key=lambda r: r.end_date or r.created_at)
    
    return render_template('verify_queue.html', records=pending_records)


@app.route('/verify/<record_id>', methods=['POST'])
def verify_record(record_id):
    """Verify an intervention outcome."""
    try:
        verifier_id = request.form.get('verifier_id')
        status = request.form.get('status')
        notes = request.form.get('notes')
        
        ledger.verify_outcome(record_id, verifier_id, status, notes)
        
        # Update Elo if verified
        record = ledger.get_record(record_id)
        if record and record.outcome_metrics and status == "verified":
            actual_value = record.outcome_metrics.get('actual_value', 0)
            elo_system.update_from_intervention(
                record.developer_id,
                record.intervention_type,
                record.predicted_value,
                actual_value
            )
            
            # Record transformation
            transformation_tracker.record_transformation(
                asset_id=record.asset_id,
                asset_type=record.asset_type,
                intervention_type=record.intervention_type,
                context=record.before_state.get("context", {}),
                before_metrics={
                    "stars": record.before_state.get("stars", 0),
                    "revenue": record.before_state.get("revenue", 0),
                    "contributors": record.before_state.get("contributors", 0)
                },
                after_metrics={
                    "stars": (record.before_state.get("stars", 0) + (record.actual_stars_delta or 0)),
                    "revenue": (record.before_state.get("revenue", 0) + (record.actual_revenue_delta or 0)),
                    "contributors": (record.before_state.get("contributors", 0) + (record.actual_contributors_delta or 0))
                }
            )
        
        flash('Intervention verified successfully', 'success')
    except Exception as e:
        flash(f'Error: {str(e)}', 'error')
    
    return redirect(url_for('verify_queue'))


@app.route('/leaderboard')
def leaderboard():
    """Full leaderboard."""
    developers = elo_system.get_developer_leaderboard(limit=100)
    interventions = elo_system.get_intervention_type_leaderboard(limit=20)
    
    return render_template('marketplace_leaderboard.html',
                         developers=developers,
                         interventions=interventions)


@app.route('/stats')
def stats():
    """Marketplace statistics."""
    learning_metrics = ledger.calculate_learning_metrics()
    
    # Get transformation stats
    patterns = transformation_tracker.get_all_patterns(min_samples=3)
    
    # Get Elo distribution
    elo_distribution = elo_system.get_rating_distribution(EloEntityType.DEVELOPER)
    
    return render_template('marketplace_stats.html',
                         learning_metrics=learning_metrics,
                         pattern_count=len(patterns),
                         elo_distribution=elo_distribution)


if __name__ == '__main__':
    app.run(debug=True, port=5001)
