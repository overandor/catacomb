# Catacomb vNext Architecture

## The Fundamental Shift

Catacomb has evolved from **repository analysis** to **innovation state transitions**.

### Before: Developer → Repo → Analysis → Intervention

**Question:** Which repo should I revive?

**Output:** Repository ranking by intervention score

### After: Developer → Asset Graph → Future States → Optimal Capital Allocation

**Question:** Where should one month of engineering effort be invested to maximize future innovation value?

**Output:** 
| Asset  | Intervention     | Cost | Success Probability | Expected Value |
| ------ | ---------------- | ---- | ------------------- | -------------- |
| Repo A | SaaS Conversion  | 45d  | 0.42                | High           |
| Repo B | Rust WASM Layer  | 14d  | 0.71                | Very High      |
| Repo C | AI Agent Wrapper | 30d  | 0.28                | Medium         |

The asset is merely the vehicle. The intervention is the investment.

---

## Core Architecture

### Layer 1: Asset Abstraction

**Unified interface for all innovation assets:**

```python
class Asset:
    asset_id: str
    asset_type: AssetType  # GitHub, HuggingFace, npm, PyPI, crates.io, Docker, API, etc.
    name: str
    owner: str
    genome: AssetGenome
    counterfactuals: List[FutureState]
    current_value: float
    expected_future_value: float
    innovation_alpha: float
```

**Asset Types:**
- GitHub repos
- HuggingFace models, datasets, spaces
- npm packages
- PyPI packages
- crates.io packages
- Docker images
- APIs
- Research papers
- Benchmarks
- Agent workflows

### Layer 2: Asset Genome

**High-dimensional representation of software creation (40 dimensions):**

**Technical Genome (10 dimensions)**
- complexity, architecture, buildability, dependency graph
- language quality, code coverage, test quality, CI quality
- docs quality, maintainability

**Economic Genome (10 dimensions)**
- adoption, demand, monetization vectors, replacement cost
- market size, growth rate, revenue potential, cost structure
- competitive advantage, network effects

**Social Genome (10 dimensions)**
- contributor growth, maintainer reputation, ecosystem influence
- community engagement, social proof, trust score
- collaboration index, influence score, network centrality, community health

**Innovation Genome (10 dimensions)**
- novelty, defensibility, category uniqueness, research depth
- innovation potential, breakthrough score, originality
- paradigm shift, disruption potential, future relevance

**Similarity Search:**
```python
# Find all projects structurally similar to early Supabase
similar_assets = market_map.find_similar_assets(supabase_asset, threshold=0.7)

# Find all Rust infrastructure projects with FastAPI-like trajectories
rust_infrastructure = market_map.find_infrastructure_assets()
fastapi_trajectory = [a for a in rust_infrastructure if a.genome.trajectory == "accelerating"]
```

### Layer 3: Counterfactual Engine

**Generates and evaluates future states:**

For every asset, generate futures:

- Future A: Documentation overhaul
- Future B: Rust rewrite
- Future C: AI integration
- Future D: Commercial API
- Future E: Package ecosystem
- Future F: Open-core company

Each future receives:
- Expected Value
- Probability
- Time to realization
- Effort required
- Risk

**Output:**
```python
{
    "intervention": "Rust WASM Layer",
    "expected_value": 0.75,
    "probability": 0.85,
    "time_days": 14,
    "effort_days": 14,
    "risk": 0.2,
    "expected_return": 0.6375,
    "roi": 0.0455
}
```

**Catacomb no longer predicts the repo. Catacomb predicts the reachable future states.**

### Layer 4: Innovation Allocation Engine

**Optimal capital allocation across assets:**

**Input:** 
- All assets
- All interventions
- All trajectories
- Total engineering days available

**Output:**
```python
{
    "allocations": [
        {
            "asset_id": "owner/repo",
            "intervention": "Rust WASM Layer",
            "effort_days": 14,
            "expected_value": 0.75,
            "probability": 0.85,
            "roi": 0.0455
        }
    ],
    "total_effort_days": 100,
    "total_expected_value": 2.5,
    "total_expected_return": 1.8,
    "average_roi": 0.032
}
```

**Strategies:**
- Max ROI (high risk, concentrated)
- Balanced (moderate risk, diversified)
- Conservative (low risk, diversified)
- Fast wins (short time horizon)

**Efficient Frontier:**
Risk-return tradeoff analysis across different risk tolerance levels.

### Layer 5: Developer Capitalization

**Developer as portfolio:**

```python
{
    "developer_id": "github:alice",
    "username": "alice",
    "total_assets": 84,
    "launchable_assets": 9,
    "intervention_opportunities": 17,
    "expected_portfolio_value": 4200000,
    "highest_leverage_intervention": {
        "intervention": "Rust Database Layer",
        "expected_value": 800000,
        "effort_days": 45
    },
    "reputation_score": 0.75,
    "ecosystem_influence": 0.68,
    "innovation_alpha": 0.42
}
```

**The developer becomes a portfolio.**

### Layer 6: Innovation Market Map

**Global innovation asset graph:**

**Discovery:**
- Isolated assets (no relationships)
- Neglected assets (high innovation alpha, low recognition)
- Emerging assets (accelerating trajectories)
- Infrastructure assets (high dependency potential)
- Ecosystem assets (category-specific)

**Relationships:**
- Dependency relationships
- Maintainer relationships
- Category relationships
- Similarity relationships

---

## Key Metrics

### Innovation Alpha

**The most important metric.**

```
Innovation Alpha = Expected Future Value − Current Recognition
```

Large positive values indicate:
- Ignored projects
- Hidden builders
- Neglected infrastructure
- Undiscovered categories

These become targets.

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

---

## Component Overview

### asset_layer.py
- **Asset**: Unified abstraction for all innovation assets
- **AssetType**: Enum of asset types (GitHub, HuggingFace, npm, etc.)
- **AssetGenome**: 40-dimensional genome vector
- **AssetScanner**: Scans assets from different sources
- **GenomeGenerator**: Generates genome from raw data
- **InnovationMarketMap**: Global asset graph with similarity search

### counterfactual_engine.py
- **CounterfactualEngine**: Generates future states for assets
- **FutureState**: Represents a counterfactual future
- **FutureStateComparator**: Compares futures across assets
- **Intervention Templates**: 14 intervention types with base parameters

### innovation_allocation.py
- **InnovationAllocationEngine**: Optimizes effort allocation
- **Allocation**: Single allocation record
- **AllocationPortfolio**: Portfolio of allocations
- **CapitalAllocationQuestion**: Answers "where should effort be invested?"
- **Strategies**: Max ROI, balanced, conservative, fast wins
- **Efficient Frontier**: Risk-return tradeoff analysis

### developer_capitalization.py
- **DeveloperProfile**: Developer as portfolio
- **DeveloperCapitalization**: Analyzes developer portfolios
- **DeveloperScanner**: Scans developer profiles
- **Comparison**: Compare multiple developers
- **Undervalued Developers**: Find high alpha developers

---

## Usage Examples

### Example 1: Optimal Allocation

```python
from asset_layer import Asset, AssetType, AssetScanner
from counterfactual_engine import CounterfactualEngine
from innovation_allocation import InnovationAllocationEngine

# Scan assets
scanner = AssetScanner()
assets = [
    scanner.scan_asset(AssetType.GITHUB_REPO, "owner/repo1"),
    scanner.scan_asset(AssetType.HUGGINGFACE_MODEL, "org/model1"),
    scanner.scan_asset(AssetType.NPM_PACKAGE, "package1")
]

# Generate genomes
genome_generator = GenomeGenerator()
for asset in assets:
    genome_generator.generate_genome(asset, raw_data)

# Generate counterfactuals
counterfactual_engine = CounterfactualEngine()
for asset in assets:
    counterfactual_engine.generate_counterfactuals(asset)

# Optimize allocation
allocation_engine = InnovationAllocationEngine()
portfolio = allocation_engine.optimize_allocation(
    assets=assets,
    total_effort_days=100,
    risk_tolerance=0.5,
    diversification=True
)

print(f"Optimal allocation: {portfolio.to_dict()}")
```

### Example 2: Developer Portfolio Analysis

```python
from developer_capitalization import DeveloperCapitalization, DeveloperScanner

# Scan developer
dev_scanner = DeveloperScanner()
dev_data = dev_scanner.scan_github_developer("username")

# Analyze as portfolio
dev_cap = DeveloperCapitalization()
profile = dev_cap.analyze_developer(
    developer_id=dev_data["developer_id"],
    username=dev_data["username"],
    assets=dev_data["assets"]
)

print(f"Developer portfolio value: ${profile.expected_portfolio_value:,.0f}")
print(f"Highest leverage intervention: {profile.highest_leverage_intervention}")
```

### Example 3: Innovation Market Discovery

```python
from asset_layer import InnovationMarketMap

# Build market map
market_map = InnovationMarketMap()
for asset in assets:
    market_map.add_asset(asset)

# Discover opportunities
isolated = market_map.find_isolated_assets()
neglected = market_map.find_neglected_assets(threshold=0.3)
emerging = market_map.find_emerging_assets()
infrastructure = market_map.find_infrastructure_assets()

print(f"Neglected assets: {len(neglected)}")
print(f"Emerging assets: {len(emerging)}")
```

---

## Architecture Evolution

### v1: Repository Analysis
- 7 deterministic agents
- Repo-focused
- Intervention scoring
- CLI interface

### v2: Multi-Agent Pipeline
- 10 deterministic agents
- Trajectory, Utility, Venture agents
- ML for intervention prediction
- Historical transformation training

### vNext: Innovation State Transions
- Asset abstraction (unified interface)
- Genome-based similarity search
- Counterfactual future states
- Optimal capital allocation
- Developer capitalization
- Innovation market map

---

## The End State

Catacomb stops looking like GitHub analytics and starts looking like a **Bloomberg Terminal for intellectual capital**.

Where:
- Software, models, datasets, packages, agents, and research are treated as assets
- Assets compete for scarce engineering attention
- The system answers: "What is the optimal allocation of human effort across the software ecosystem?"

This is a **deterministic venture scout for software innovation**.

---

## Implementation Status

### Completed
- ✅ Asset abstraction layer
- ✅ Asset genome (40 dimensions)
- ✅ Counterfactual engine (14 intervention types)
- ✅ Innovation allocation engine
- ✅ Developer capitalization
- ✅ Innovation alpha metric
- ✅ Innovation market map

### Pending
- ⏳ Multi-asset source integrations (HuggingFace, npm, PyPI, crates.io APIs)
- ⏳ Genome generation from actual asset data
- ⏳ Counterfactual ML training on historical transformations
- ⏳ Portfolio optimization algorithms (knapsack, genetic algorithms)
- ⏳ Real-time market map updates
- ⏳ Developer reputation calculation from actual data

---

## Next Steps

1. **Integrate Asset Layer with Existing Agents**
   - Map repo_scanner output to Asset objects
   - Generate genomes from agent outputs
   - Replace repo-centric data flow with asset-centric flow

2. **Implement Multi-Asset Scanners**
   - HuggingFace API integration
   - npm registry API
   - PyPI API
   - crates.io API

3. **Train Counterfactual Models**
   - Use historical transformation dataset
   - Train on intervention-outcome pairs
   - Improve future state predictions

4. **Build Portfolio Optimization**
   - Implement knapsack solver
   - Add genetic algorithm for complex constraints
   - Multi-objective optimization (risk, return, time)

5. **Create Innovation Market UI**
   - Asset graph visualization
   - Portfolio dashboard
   - Allocation recommendations
   - Developer portfolio views

---

## Key Insight

The shift from **repository scoring** to **intervention scoring** was the first major innovation.

The shift from **intervention scoring** to **innovation state transitions** is the second.

Catacomb now operates on **innovation capital allocation**, not repository analysis. This is the fundamental architectural breakthrough that transforms the system from a tool into a platform.
