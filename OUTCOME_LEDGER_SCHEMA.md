# Outcome Ledger Schema

## Purpose

Track predictions, interventions, and observed outcomes to enable Catacomb to learn from real-world results.

## Core Entities

### InterventionRecord

```json
{
  "record_id": "uuid",
  "created_at": "ISO8601 timestamp",
  "updated_at": "ISO8601 timestamp",
  
  // Asset identification
  "asset_id": "owner/repo",
  "asset_type": "github_repo",
  "asset_name": "repository name",
  
  // Developer identification
  "developer_id": "developer_uuid",
  "developer_username": "github_username",
  
  // Before state (snapshot at prediction time)
  "before_state": {
    "stars": 1000,
    "forks": 200,
    "open_issues": 50,
    "commits_last_year": 150,
    "contributors": 10,
    "language": "Python",
    "license": "MIT",
    "has_readme": true,
    "has_ci": true,
    "has_tests": true,
    "created_at": "ISO8601",
    "pushed_at": "ISO8601"
  },
  
  // Prediction
  "intervention_type": "documentation_overhaul",
  "intervention_description": "Comprehensive documentation overhaul",
  "planned_effort_days": 7,
  "predicted_value": 0.85,
  "predicted_probability": 0.9,
  "predicted_risk": 0.1,
  "predicted_outcome": {
    "star_growth": 0.5,
    "contributor_growth": 0.3,
    "fork_growth": 0.2
  },
  
  // Execution
  "status": "planned | in_progress | completed | verified | failed",
  "started_at": "ISO8601 timestamp",
  "completed_at": "ISO8601 timestamp",
  "actual_effort_days": 8,
  
  // After state (snapshot after intervention)
  "after_state": {
    "stars": 1500,
    "forks": 250,
    "open_issues": 45,
    "commits_last_year": 200,
    "contributors": 15,
    "language": "Python",
    "license": "MIT",
    "has_readme": true,
    "has_ci": true,
    "has_tests": true,
    "created_at": "ISO8601",
    "pushed_at": "ISO8601"
  },
  
  // Observed outcome
  "outcome_metrics": {
    "star_growth": 0.5,
    "contributor_growth": 0.5,
    "fork_growth": 0.25,
    "issue_closure_rate": 0.1,
    "time_to_first_contribution": 30
  },
  
  // Verification
  "verifications": [
    {
      "verifier_id": "verifier_uuid",
      "verifier_username": "github_username",
      "status": "verified | disputed",
      "notes": "Intervention successfully implemented",
      "verified_at": "ISO8601 timestamp"
    }
  ],
  
  // Learning
  "prediction_accuracy": {
    "value_error": 0.05,
    "probability_error": 0.1,
    "risk_error": 0.05
  },
  
  // Hash for reproducibility
  "before_hash": "sha256(before_state)",
  "after_hash": "sha256(after_state)",
  "intervention_hash": "sha256(intervention_details)"
}
```

### DeveloperProfile

```json
{
  "developer_id": "uuid",
  "username": "github_username",
  "created_at": "ISO8601 timestamp",
  
  // Reputation metrics
  "total_interventions": 10,
  "successful_interventions": 8,
  "failed_interventions": 1,
  "disputed_interventions": 1,
  
  // Value created
  "total_value_created": 5.2,
  "avg_value_per_intervention": 0.52,
  
  // Accuracy
  "prediction_accuracy": 0.85,
  "effort_accuracy": 0.9,
  
  // Specialization
  "top_intervention_types": ["documentation", "build_system"],
  "top_languages": ["Python", "Rust"],
  "top_categories": ["infrastructure", "developer-tools"]
}
```

### AssetHistory

```json
{
  "asset_id": "owner/repo",
  "snapshots": [
    {
      "timestamp": "ISO8601",
      "stars": 1000,
      "forks": 200,
      "open_issues": 50,
      "commits_last_year": 150,
      "contributors": 10
    }
  ],
  "interventions": ["record_id_1", "record_id_2"]
}
```

## API Operations

### Create Intervention

```http
POST /api/interventions
Content-Type: application/json

{
  "asset_id": "owner/repo",
  "developer_id": "developer_uuid",
  "intervention_type": "documentation_overhaul",
  "intervention_description": "...",
  "planned_effort_days": 7,
  "predicted_value": 0.85,
  "predicted_probability": 0.9,
  "predicted_risk": 0.1
}
```

### Start Intervention

```http
POST /api/interventions/{record_id}/start
Content-Type: application/json

{
  "actual_effort_days": 8
}
```

### Complete Intervention

```http
POST /api/interventions/{record_id}/complete
Content-Type: application/json

{
  "after_state": {...},
  "outcome_metrics": {...}
}
```

### Verify Intervention

```http
POST /api/interventions/{record_id}/verify
Content-Type: application/json

{
  "verifier_id": "verifier_uuid",
  "status": "verified",
  "notes": "..."
}
```

### Get Developer Reputation

```http
GET /api/developers/{developer_id}/reputation
```

### Get Training Dataset

```http
GET /api/interventions/training-data
```

Returns all completed interventions with before/after states for ML training.

## Learning Loop

1. **Predict** - Catacomb generates intervention prediction
2. **Record** - Intervention recorded with before state snapshot
3. **Execute** - Developer implements intervention
4. **Snapshot** - After state captured after intervention
5. **Measure** - Outcome metrics calculated
6. **Verify** - Community verifies intervention success
7. **Learn** - Model retrained with new intervention-outcome pairs

## Storage

- Primary storage: SQLite (for simplicity and portability)
- Backup: JSON export
- Future: PostgreSQL for production scale

## Privacy

- Developer IDs are UUIDs, not GitHub IDs
- Only public GitHub metrics are stored
- No private repository data
- Opt-out mechanism for developers
