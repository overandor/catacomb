# ML Training Guide for Catacomb

## Overview

Catacomb includes ML models for predicting **intervention value creation**, not repository popularity. The system has evolved from predicting "will this repo get stars?" to "which interventions create value?"

## Architecture Evolution

### Level 1: Popularity Model (Deprecated)
- Predicted star growth and GitHub popularity
- Commodity problem, limited differentiation

### Level 2: Utility Model (Current)
- Predicts actual developer usage, dependency potential
- Separates popular-but-useless from useful-but-invisible

### Level 3: Intervention Model (Current Focus)
- Trains on: repo state → intervention → outcome
- Learns: which interventions create value
- Goal: maximize expected value per unit effort

### Level 4: Venture Model (Implemented)
- Predicts startup formation, funding, acquisition
- Machine-learning venture scout

## Components

### Deterministic Agents (No ML Required)
1. **TrajectoryAgent** - Velocity, acceleration, growth direction
2. **UtilityAgent** - Dependency potential, integration potential, replacement cost
3. **VentureAgent** - Startup/funding/acquisition probability

### ML Components
1. **InterventionMLAgent** - Predicts intervention value creation
2. **InterventionOutcomeDataset** - Historical transformation data
3. **InterventionModelTrainer** - Trains on intervention-outcome pairs
4. **HistoricalTransformations** - Dataset structure for before/after analysis

## Historical Transformation Dataset

The best training data is **historical transformations**, not GitHub snapshots.

### Example Transformations

**Next.js**
- Before: 500 stars, basic framework
- Intervention: Feature expansion (SSR, API routes)
- After: 120,000 stars, became startup

**Supabase**
- Before: 1,000 stars, open source Firebase
- Intervention: SaaS conversion
- After: 65,000 stars, Series B funding

**LangChain**
- Before: 100 stars, LLM framework
- Intervention: AI integration
- After: 85,000 stars, Series A funding

### Dataset Structure

```python
{
    "repo_id": "vercel/next.js",
    "before_state": {
        "stars": 500,
        "forks": 50,
        "contributors": 5,
        "commits_last_year": 100,
        # ... 28 features
    },
    "intervention": "feature_expansion",
    "intervention_date": "2016-10-25",
    "after_state": {
        "stars": 120000,
        "forks": 25000,
        # ... outcome state
    },
    "outcome_metrics": {
        "star_growth": 23900.0,
        "contributor_growth": 400.0,
        "adoption": 0.95,
        "ecosystem_impact": 0.98
    }
}
```

## Intervention Model Training

### Feature Engineering (23 features)

**Repo State (11)**
- stars, forks, issues, contributors, commits
- has_readme, has_ci, has_tests, has_dockerfile
- days_since_commit, archived

**Intervention Type (10)**
- One-hot encoded: documentation, build_system, feature_expansion, saas_conversion, ai_integration, infrastructure_repositioning, community_building, modernization, packaging, momentum_amplification

**Intervention Fit (1)**
- Calculated fit score between repo state and intervention type

### Labels

**Outcome Metrics (0-1)**
- `star_growth`: Normalized star increase
- `contributor_growth`: Normalized contributor increase
- `adoption`: Actual usage adoption
- `ecosystem_impact`: Impact on ecosystem

### Training Pipeline

#### Step 1: Collect Historical Transformations

```python
from historical_transformations import HistoricalTransformationDataset, load_example_dataset

# Load example transformations
dataset = load_example_dataset()

# Or add custom transformations
from historical_transformations import HistoricalTransformation

transformation = HistoricalTransformation(
    repo_id="owner/repo",
    before_state=repo_before,
    intervention="feature_expansion",
    intervention_date="2020-01-01",
    after_state=repo_after,
    outcome_metrics={
        "star_growth": 10.0,
        "contributor_growth": 5.0,
        "adoption": 0.8,
        "ecosystem_impact": 0.7
    }
)
dataset.add_transformation(transformation)

# Save dataset
dataset.save("transformations.json")
```

#### Step 2: Train Intervention Model

```python
from intervention_ml_agent import InterventionModelTrainer

# Load dataset
dataset = HistoricalTransformationDataset()
dataset.load("transformations.json")

# Get training examples
training_data = dataset.get_training_examples()

# Train model
trainer = InterventionModelTrainer()
metrics = trainer.train(training_data)

print(f"MSE: {metrics['mse']}, R²: {metrics['r2']}")

# Save model
trainer.save_model("intervention_model.joblib")
```

#### Step 3: Use Trained Model

```python
from intervention_ml_agent import InterventionMLAgent

agent = InterventionMLAgent(model_path="intervention_model.joblib")

# Predict value for specific intervention
value = agent.predict_intervention_value(repo_data, "feature_expansion")

# Rank multiple interventions
interventions = [
    {"name": "Documentation Overhaul"},
    {"name": "Feature Expansion"},
    {"name": "SaaS Conversion"}
]
ranked = agent.rank_interventions(repo_data, interventions)
```

## Model Performance

Expected metrics (after sufficient transformation data):

**Intervention Value Prediction**
- MSE: < 0.08
- R²: > 0.65

**Note**: Lower R² is acceptable because:
- Intervention outcomes are highly variable
- Many factors outside repo state affect outcomes
- Model provides probabilistic guidance, not certainty

## Integration with Catacomb

### Opportunity Layer Integration

```python
# In layers.py
class OpportunityLayer:
    def __init__(self, github_token=None, use_ml=True):
        self.trajectory = TrajectoryAgent()
        self.utility = UtilityAgent()
        self.venture = VentureAgent()
        self.intervention_ml = InterventionMLAgent() if use_ml else None
```

### Trajectory-Aware Intervention Paths

The Strategy Layer now generates trajectory-specific interventions:

- **Accelerating**: Momentum Amplification (14 days, 90% upside)
- **Decelerating**: Turnaround Strategy (28 days, 80% upside)
- **Stagnant**: Dormant Awakening (35 days, 75% upside)

### Venture-Enhanced Scoring

Venture predictions boost intervention scores for high-potential repos:

```python
venture_score = opportunity["venture"]["score"]
if venture_score > 75:  # Unicorn candidate
    intervention_score *= 1.3
```

## Data Requirements

**Minimum Transformation Data**: 50 historical transformations
**Recommended**: 200+ transformations
**Ideal**: 500+ transformations across categories

**Key Categories to Cover:**
- Frameworks (Next.js, FastAPI)
- Databases (Supabase)
- AI/ML (LangChain)
- Runtimes (Bun)
- Developer tools

## Fallback Mode

If no trained model is available, the system uses:

1. **TrajectoryAgent**: Heuristic velocity/acceleration
2. **UtilityAgent**: Heuristic dependency/integration potential
3. **VentureAgent**: Heuristic startup/funding probability
4. **InterventionMLAgent**: Heuristic intervention fit scoring

## Advanced Configuration

### Custom Intervention Types

Add new intervention types to `InterventionMLAgent._extract_intervention_features()`:

```python
intervention_types = [
    "documentation", "build_system", "feature_expansion",
    "saas_conversion", "ai_integration", "infrastructure_repositioning",
    "community_building", "modernization", "packaging",
    "momentum_amplification", "your_custom_type"  # Add here
]
```

### Custom Outcome Metrics

Modify `HistoricalTransformation.outcome_metrics` to include:

- Revenue growth
- User acquisition
- Enterprise adoption
- Technical debt reduction

### Alternative Models

Replace RandomForestRegressor with:
- XGBoost (better for tabular data)
- LightGBM (faster training)
- Neural Networks (if sufficient data)
- Causal Forests (for causal inference)

## Troubleshooting

**Low R² on intervention predictions**:
- Expected - intervention outcomes are highly variable
- Focus on ranking quality, not absolute accuracy
- Use model for relative comparison, not absolute prediction

**Overfitting to specific categories**:
- Ensure diverse transformation data
- Use category-specific models
- Add regularization

**Feature importance analysis**:
```python
importances = model.feature_importances_
# Intervention fit should be top feature
# Repo state features should follow
```

## Future Enhancements

- **Causal Inference**: Estimate causal effect of interventions
- **Counterfactual Analysis**: "What if we had done X instead?"
- **Time-Series Prediction**: Predict optimal intervention timing
- **Portfolio Optimization**: Select optimal intervention portfolio
- **Innovation Graph**: Developer → Repo → Intervention → Outcome graph

## Key Insight

The shift from **popularity prediction** to **intervention value prediction** is Catacomb's core innovation. We don't predict which repos will get stars - we predict which actions create value. This is a much harder but more defensible problem.
