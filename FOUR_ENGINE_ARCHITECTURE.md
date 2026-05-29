# Four-Engine Architecture

## The Fundamental Shift

Catacomb has evolved into a new category of developer tools.

**Traditional tools answer:**
- What exists?
- What is popular?
- What should I use?

**Catacomb answers:**
- What is undervalued?
- What future is reachable?
- Where should effort be invested?

This is a fundamentally different optimization problem.

---

## Architecture Overview

The system now naturally splits into **4 engines**:

```
Evidence Engine → Simulation Engine → Allocation Engine → Market Engine
```

Each engine has a distinct responsibility and outputs specific artifacts.

---

## Engine 1: Evidence Engine

**Ground truth data collection.**

### Inputs
- GitHub
- HuggingFace
- npm
- PyPI
- crates.io
- arXiv
- Docker
- Package registries

### Outputs
- Asset Genome (40 dimensions)
- Trajectory
- Utility
- Quality
- Risk

### Philosophy
**No opinions. Only evidence.**

The Evidence Engine collects raw data and converts it into structured evidence without making predictions or recommendations.

### Components

**AssetScanner**
- Scans assets from multiple sources
- Normalizes data into unified Asset objects
- Supports 12 asset types (GitHub, HuggingFace, npm, PyPI, crates.io, Docker, APIs, research papers, benchmarks, agent workflows)

**GenomeGenerator**
- Generates 40-dimensional genome vectors
- Technical genome (10): complexity, architecture, buildability, dependency health, language quality, code/test/CI/docs quality, maintainability
- Economic genome (10): adoption, demand, monetization, replacement cost, market size, growth rate, revenue potential, cost structure, competitive advantage, network effects
- Social genome (10): contributor growth, maintainer reputation, ecosystem influence, community engagement, social proof, trust, collaboration, influence, network centrality, community health
- Innovation genome (10): novelty, defensibility, category uniqueness, research depth, innovation potential, breakthrough, originality, paradigm shift, disruption, future relevance

**InnovationMarketMap**
- Global asset graph
- Similarity search (cosine similarity on genomes)
- Discovery: isolated, neglected, emerging, infrastructure, ecosystem assets

### Usage

```python
from four_engine_architecture import EvidenceEngine, AssetType

evidence = EvidenceEngine()

# Collect single asset
asset = evidence.collect_asset(
    AssetType.GITHUB_REPO,
    "owner/repo",
    raw_data={"stars": 1000, "forks": 50, ...}
)

# Collect batch
assets = evidence.collect_assets_batch([
    {"asset_type": "github_repo", "asset_id": "owner/repo1"},
    {"asset_type": "huggingface_model", "asset_id": "org/model1"},
    {"asset_type": "npm_package", "asset_id": "package1"}
])

# Get evidence summary
summary = evidence.get_evidence_summary(asset)
```

---

## Engine 2: Simulation Engine

**Counterfactual generation.**

### Function
For every asset, generate futures.

### Example

**Current:** Rust parser library

**Future A:** Crates.io release  
**Future B:** WASM package  
**Future C:** AI integration  
**Future D:** Commercial API  
**Future E:** Developer platform

### Each Future Gets
- Probability
- Cost (effort days)
- Time to realization
- Expected adoption
- Expected value
- Risk

### Philosophy
**This becomes the moat.**

The ability to generate and evaluate counterfactual futures is Catacomb's competitive advantage. No other tool does this.

### Components

**CounterfactualEngine**
- 14 intervention templates
- Generates future states based on asset genome
- Adjusts parameters (effort, probability, upside, risk) based on genome
- Compares futures across assets

**FutureState**
- Represents a counterfactual future
- Calculates expected return and ROI
- Tracks probability, time, effort, risk

**FutureStateComparator**
- Finds highest ROI intervention across assets
- Finds fastest high-value intervention
- Finds lowest-risk intervention

### Intervention Templates

1. Documentation Overhaul (7 days, 90% probability, 30% upside)
2. Build System Modernization (14 days, 80% probability, 50% upside)
3. Feature Expansion (21 days, 70% probability, 60% upside)
4. SaaS Conversion (60 days, 50% probability, 90% upside)
5. AI Integration (45 days, 60% probability, 85% upside)
6. Infrastructure Repositioning (30 days, 70% probability, 80% upside)
7. Community Building (21 days, 80% probability, 70% upside)
8. Rust WASM Layer (14 days, 85% probability, 75% upside)
9. AI Agent Wrapper (30 days, 65% probability, 80% upside)
10. Commercial API (35 days, 55% probability, 85% upside)
11. Package Ecosystem (14 days, 80% probability, 65% upside)
12. Open-Core Company (90 days, 40% probability, 95% upside)
13. Model Fine-Tuning (21 days, 70% probability, 70% upside)
14. Dataset Curation (14 days, 85% probability, 60% upside)

### Usage

```python
from four_engine_architecture import SimulationEngine

simulation = SimulationEngine()

# Simulate futures for single asset
futures = simulation.simulate_futures(asset, max_futures=6)

# Get best future
best = simulation.get_best_future(asset)

# Compare all futures
comparison = simulation.compare_futures(asset)

# Find highest ROI across all assets
best_roi = simulation.find_highest_roi_across_assets(assets)
```

---

## Engine 3: Allocation Engine

**The most important component.**

### Inputs
- 100 engineering days
- $10k budget
- 2 developers
- 1 designer

### Output
```
Invest:
40 days → Asset A
25 days → Asset B
35 days → Asset C
```

### Philosophy
**This is portfolio theory applied to software.**

Not repo discovery. Capital allocation.

### Components

**InnovationAllocationEngine**
- Optimizes effort allocation across assets
- Greedy allocation (can be upgraded to knapsack optimization)
- Strategies: max ROI, balanced, conservative, fast wins
- Efficient frontier analysis (risk-return tradeoffs)
- Category-based allocation
- Sensitivity analysis

**Allocation**
- Single allocation record
- Tracks asset, intervention, effort, expected value, probability, ROI, risk

**AllocationPortfolio**
- Portfolio of allocations
- Calculates portfolio-level metrics (total effort, total expected value, average ROI, average risk)

**CapitalAllocationQuestion**
- Answers: "Where should effort be invested?"
- Generates human-readable summaries and recommendations

### Strategies

**Max ROI**
- High risk tolerance (0.8)
- High minimum ROI (0.02)
- No diversification
- Concentrated bets

**Balanced**
- Moderate risk tolerance (0.5)
- Moderate minimum ROI (0.01)
- Diversified across assets
- Balanced risk-return

**Conservative**
- Low risk tolerance (0.3)
- Low minimum ROI (0.005)
- Diversified across assets
- Risk-averse

**Fast Wins**
- Moderate risk tolerance (0.6)
- Moderate minimum ROI (0.01)
- Diversified
- Short time horizon

### Usage

```python
from four_engine_architecture import AllocationEngine

allocation = AllocationEngine()

# Optimize allocation
portfolio = allocation.optimize_allocation(
    assets=assets,
    total_effort_days=100,
    risk_tolerance=0.5,
    diversification=True
)

# Optimize by category
category_portfolio = allocation.optimize_by_category(
    assets=assets,
    total_effort_days=100,
    category_allocations={"infrastructure": 0.4, "ai": 0.6}
)

# Find efficient frontier
frontier = allocation.find_efficient_frontier(
    assets=assets,
    total_effort_days=100,
    risk_levels=[0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
)

# Compare strategies
strategies = allocation.compare_strategies(assets, total_effort_days=100)
```

---

## Engine 4: Market Engine

**The eventual network.**

### Capabilities
Users can:
- Publish interventions
- Claim ownership
- Show outcomes
- Verify transformations
- Discover opportunities

### Eventual Flow
```
Developer
  ↓
Asset Portfolio
  ↓
Interventions
  ↓
Outcomes
  ↓
Reputation
```

### Philosophy
**The reputation system becomes more valuable than stars.**

### Components

**OutcomeLedger**
- Tracks intervention records
- Records before state, intervention, after state, outcome metrics
- Calculates prediction accuracy
- Generates training datasets
- Calculates developer reputation

**InterventionRecord**
- Complete record of intervention lifecycle
- Tracks: before state, intervention, predictions, after state, outcomes, verification
- Calculates prediction accuracy (value, probability, risk)

**InterventionDataset**
- Proprietary dataset of intervention-outcome pairs
- Calculates intervention effectiveness
- Finds best interventions by value per day

**MarketEngine**
- Publish interventions
- Claim ownership
- Start interventions
- Report outcomes
- Verify transformations
- Discover opportunities
- Get developer reputation
- Leaderboard
- Learning metrics

### Verification System

Outcomes can be verified by other developers:
- Pending → Verified → Disputed → Rejected

Verification builds trust in the dataset.

### Usage

```python
from four_engine_architecture import MarketEngine

market = MarketEngine()

# Publish intervention
record = market.publish_intervention(
    asset_id="owner/repo",
    asset_type="github_repo",
    asset_name="repo",
    developer_id="github:alice",
    developer_username="alice",
    before_state={"stars": 100, ...},
    intervention_type="Rust WASM Layer",
    intervention_description="Add WASM support",
    planned_effort_days=14,
    predicted_value=0.75,
    predicted_probability=0.85,
    predicted_risk=0.2
)

# Start intervention
market.start_intervention(record.record_id, actual_effort_days=14)

# Report outcome
market.report_outcome(
    record.record_id,
    after_state={"stars": 280, ...},
    outcome_metrics={
        "actual_value": 0.8,
        "success": True,
        "value_created": 180,  # star growth
        "actual_risk": 0.15
    }
)

# Verify transformation
market.verify_transformation(
    record.record_id,
    verifier_id="github:bob",
    status="verified",
    notes="Verified star growth from 100 to 280"
)

# Discover opportunities
opportunities = market.discover_opportunities(
    min_innovation_alpha=0.3,
    max_effort_days=30
)

# Get developer reputation
reputation = market.get_developer_reputation("github:alice")

# Get leaderboard
leaderboard = market.get_leaderboard(metric="total_value_created")

# Get learning metrics
metrics = market.get_learning_metrics()
```

---

## The Outcome Ledger

**The biggest missing piece.**

### Problem
Right now the system predicts value. It does not learn from reality.

### Solution
Every intervention becomes:
```
Before State
Intervention
After State
Result
```

### Example

**Repo:** xyz/parser  
**Intervention:** WASM Port  
**Cost:** 14 days

**6 months later:**
- Stars: +180%
- Contributors: +60%
- Downloads: +1200%
- Revenue: $8,000

### Impact
Now Catacomb learns.

Without this, every prediction model eventually drifts.

With this, you create a proprietary intervention dataset that nobody else has.

### The True Asset

The true asset isn't the repo scanner. It isn't the agents. It isn't the scoring.

**It is the dataset:**
```
Asset → Intervention → Outcome → Future Value
```

If you accumulate enough of these records, Catacomb becomes an **innovation prediction system** rather than a **repository analysis system**.

At that point you're not competing with GitHub analytics tools. You're building a **market intelligence layer for software evolution itself**.

---

## CatacombOrchestrator

**Main orchestrator for the 4-engine architecture.**

Coordinates: Evidence → Simulation → Allocation → Market

### Methods

**analyze_asset**
- Full analysis pipeline for single asset
- Evidence → Simulation → Return results

**optimize_portfolio**
- Optimize portfolio allocation across assets
- Evidence → Simulation → Allocation → Return portfolio

**execute_intervention_lifecycle**
- Execute full intervention lifecycle
- Evidence → Simulation → Market (publish) → Return record

**get_system_health**
- Get system health metrics
- Learning metrics, developer count, leaderboard

### Usage

```python
from four_engine_architecture import CatacombOrchestrator

orchestrator = CatacombOrchestrator()

# Analyze single asset
analysis = orchestrator.analyze_asset(
    AssetType.GITHUB_REPO,
    "owner/repo",
    raw_data={"stars": 1000, ...}
)

# Optimize portfolio
portfolio = orchestrator.optimize_portfolio(
    asset_specs=[
        {"asset_type": "github_repo", "asset_id": "owner/repo1"},
        {"asset_type": "huggingface_model", "asset_id": "org/model1"}
    ],
    total_effort_days=100,
    strategy="balanced"
)

# Execute intervention lifecycle
lifecycle = orchestrator.execute_intervention_lifecycle(
    asset_type=AssetType.GITHUB_REPO,
    asset_id="owner/repo",
    developer_id="github:alice",
    developer_username="alice",
    intervention_type="Rust WASM Layer",
    intervention_description="Add WASM support",
    planned_effort_days=14,
    raw_data={"stars": 100, ...}
)

# Get system health
health = orchestrator.get_system_health()
```

---

## Data Flow

```
┌─────────────────┐
│  Evidence Engine │
│                 │
│  - Collect      │
│  - Genome       │
│  - Market Map   │
└────────┬────────┘
         │
         ↓
┌─────────────────┐
│ Simulation      │
│ Engine          │
│                 │
│  - Futures      │
│  - Counterfacts │
│  - Comparison   │
└────────┬────────┘
         │
         ↓
┌─────────────────┐
│ Allocation      │
│ Engine          │
│                 │
│  - Optimize     │
│  - Portfolio    │
│  - Strategies   │
└────────┬────────┘
         │
         ↓
┌─────────────────┐
│ Market Engine   │
│                 │
│  - Publish     │
│  - Outcomes     │
│  - Verify      │
│  - Reputation   │
└────────┬────────┘
         │
         ↓
┌─────────────────┐
│ Outcome Ledger  │
│                 │
│  - Learn        │
│  - Retrain      │
│  - Dataset      │
└─────────────────┘
```

---

## Key Metrics

### Innovation Alpha
```
Innovation Alpha = Expected Future Value − Current Recognition
```

Large positive values indicate:
- Ignored projects
- Hidden builders
- Neglected infrastructure
- Undiscovered categories

### ROI (Return on Innovation)
```
ROI = (Expected Value × Probability) / Effort Days
```

Measures value creation per unit effort.

### Expected Return
```
Expected Return = Expected Value × Probability
```

Risk-adjusted expected outcome.

### Prediction Accuracy
```
Value Accuracy = 1 - |Predicted Value − Actual Value|
Probability Accuracy = 1 - |Predicted Probability − Actual Success|
Risk Accuracy = 1 - |Predicted Risk − Actual Risk|
Overall Accuracy = (Value + Probability + Risk) / 3
```

Measures how well predictions match reality.

---

## Learning Loop

1. **Predict** (Simulation Engine)
   - Generate counterfactual futures
   - Predict value, probability, risk

2. **Act** (Market Engine)
   - Publish intervention
   - Execute intervention
   - Report outcome

3. **Learn** (Outcome Ledger)
   - Calculate prediction accuracy
   - Update intervention effectiveness
   - Retrain models

4. **Improve** (All Engines)
   - Better genome generation
   - Better future simulation
   - Better allocation optimization
   - Better reputation scoring

---

## Competitive Advantage

### Traditional Tools
- Repository discovery
- Popularity ranking
- Usage recommendations

### Catacomb
- Innovation state transitions
- Counterfactual simulation
- Capital allocation optimization
- Outcome-based learning
- Proprietary intervention dataset

### The Moat
The combination of:
1. Counterfactual simulation (unique)
2. Capital allocation theory applied to software (unique)
3. Outcome ledger with learning (unique)
4. Proprietary intervention dataset (defensible)

---

## Implementation Status

### Completed
- ✅ Outcome Ledger (track intervention results and learn)
- ✅ 4-Engine Architecture (Evidence, Simulation, Allocation, Market)
- ✅ Evidence Engine (multi-source data collection)
- ✅ Simulation Engine (refactored from CounterfactualEngine)
- ✅ Allocation Engine (refactored from InnovationAllocationEngine)
- ✅ Market Engine (publish, claim, verify, reputation)
- ✅ Proprietary intervention dataset from outcomes
- ✅ CatacombOrchestrator (main coordinator)

### Pending
- ⏳ Multi-asset source API integrations (HuggingFace, npm, PyPI, crates.io)
- ⏳ Genome generation from actual agent outputs
- ⏳ Counterfactual ML training on outcome ledger data
- ⏳ Advanced portfolio optimization (knapsack, genetic algorithms)
- ⏳ Real-time market map updates
- ⏳ Outcome-based model retraining pipeline
- ⏳ Verification system UI
- ⏳ Leaderboard UI

---

## Next Steps

1. **Integrate with Existing Agents**
   - Map agent outputs to Evidence Engine
   - Generate genomes from agent evidence
   - Replace repo-centric flow with asset-centric flow

2. **Implement Multi-Asset Scanners**
   - HuggingFace API integration
   - npm registry API
   - PyPI API
   - crates.io API

3. **Train on Outcome Ledger**
   - Use intervention-outcome pairs
   - Improve counterfactual predictions
   - Calibrate probability estimates

4. **Build Portfolio Optimization**
   - Implement knapsack solver
   - Add genetic algorithm
   - Multi-objective optimization

5. **Create Market UI**
   - Intervention publishing
   - Outcome reporting
   - Verification system
   - Leaderboard
   - Developer reputation

---

## The End State

Catacomb becomes a **market intelligence layer for software evolution**.

Where:
- Software, models, datasets, packages, and research are assets
- Assets compete for scarce engineering attention
- The system answers: "What is the optimal allocation of human effort across the software ecosystem?"

This is a **deterministic venture scout for software innovation** with a proprietary dataset that becomes more valuable with every intervention executed.

The true asset is the dataset: **Asset → Intervention → Outcome → Future Value**.
