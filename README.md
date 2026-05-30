# Catacomb

**Innovation Allocation Engine**

Catacomb discovers under-recognized software assets and ranks the highest-value engineering interventions to unlock them.

## Core Thesis

**Repository discovery is not the product. Innovation allocation is the product.**

Catacomb does not answer "Which repo is valuable?" It answers:

> "Given 30 engineering days, where should effort be deployed to create the most future value?"

## What It Does

Catacomb is an intervention intelligence system that:

1. **Discovers assets** - Identifies software assets across types (repos, models, datasets, APIs, papers, agents, prompts, workflows)
2. **Calculates Innovation Alpha** - Measures mispricing: `Alpha = Expected Future Value - Current Recognition`
3. **Ranks interventions** - Calculates Expected Value Created Per Engineering Day
4. **Tracks outcomes** - Closed-loop intervention lifecycle with before/after metrics and verification
5. **Builds ground truth** - Accumulates verified intervention-outcome pairs as the defensible moat

## Key Product: Catacomb Radar

The Radar tab shows assets ranked by **Expected Value Created Per Engineering Day**.

## Architecture Evolution

### Phase 1: Repository Discovery
```
GitHub Scanner → Repo Ranking → Opportunity Score
```

### Phase 2: Intervention Focus
```
Repo → Intervention → Expected Outcome
```

### Phase 3: Closed-Loop
```
Asset → Intervention → Outcome → Verified Result
```

### Phase 4: Portfolio Allocation
```
Developer → Asset Portfolio → Future States → Capital Allocation
```

### Phase 5: Innovation Market
```
Innovation Market (current target)
```

## Asset Abstraction

Catacomb treats all software assets uniformly:

- **Repository** - GitHub, GitLab, Bitbucket
- **Model** - Hugging Face, PyTorch Hub, TensorFlow Hub
- **Dataset** - Kaggle, Hugging Face Datasets
- **API** - OpenAPI, GraphQL, REST
- **Research Paper** - arXiv, IEEE, ACM
- **Agent** - LangChain, AutoGPT, BabyAGI
- **Prompt Corpus** - PromptBase, FlowGPT
- **Workflow** - n8n, Airflow, Temporal

All assets share:
- **Asset Genome** - Structural metadata, dependencies, community signals
- **Current State** - Recognition, value, health indicators
- **Future States** - Potential interventions, achievable value
- **Innovation Alpha** - Mispricing opportunity
- **Intervention History** - Past interventions and outcomes

## Innovation Alpha

```
Innovation Alpha = Expected Future Value - Current Recognition
```

**Positive alpha** = undervalued (opportunity)
**Zero alpha** = fairly valued
**Negative alpha** = overvalued (avoid)

Example:
```
Expected Future Value = 80
Recognition = 90
Alpha = -10 (already discovered, avoid)

Expected Future Value = 80
Recognition = 15
Alpha = +65 (hidden gem, opportunity)
```

## Ground Truth Moat

The defensible dataset is not:
- GitHub scanning (can be copied)
- LLM reasoning (can be copied)
- Repo valuation (can be copied)
- Opportunity scores (can be copied)

The defensible dataset is:
- **10,000 verified intervention-outcome pairs**

This ground truth cannot be copied quickly and enables:
- Intervention prediction
- Value delta estimation
- Success probability modeling
- Risk assessment

## Future Architecture

```
DollarFS Discover (Private Assets)
↓
Asset Genome
↓
Catacomb Alpha Engine
↓
Intervention Forecast
↓
Outcome Ledger
↓
Evidence Packet
↓
BitNet Proof
↓
Software Asset Registry
↓
Price Discovery
```

This is the first version of a genuine software-capital market.

## Usage

```bash
# Install dependencies
pip install -r requirements.txt

# Set GitHub token (required for mining)
export GITHUB_TOKEN=your_token

# Start the API server
python app.py

# Mine GitHub PRs for verified interventions
python github_intervention_miner.py
```

## API Endpoints

- `GET /api/radar` - Assets ranked by value per engineering day
- `GET /api/discover/promising` - Alpha Universe (undervalued assets only)
- `GET /api/ledger` - Intervention ledger with verification status
- `GET /api/metrics` - System metrics (verified interventions, engineering alpha, etc.)

## Roadmap

1. **Asset Abstraction** - Unified interface for all asset types
2. **Asset Genome** - Structural metadata and dependency graph
3. **Innovation Alpha Discovery** - Mispricing detection across asset types
4. **Outcome Ledger Growth** - Scale to 10,000 verified intervention-outcome pairs
5. **Intervention Prediction** - ML model from verified outcomes
6. **Ecosystem Graph** - Asset relationship discovery
7. **DollarFS Integration** - Private asset discovery
8. **Asset Embeddings** - Similarity search across asset types
9. **Evidence Packets** - BitNet proof integration
10. **Software Asset Registry** - Price discovery

## Product Positioning

Catacomb is not a repository explorer. It is an **innovation allocation engine** that:

- Values **actions on assets** more than assets themselves
- Ranks by **Expected Value Created Per Engineering Day**, not popularity
- Prioritizes **verified intervention outcomes** over dataset size
- Measures **mispricing** (Innovation Alpha), not recognition
- Focuses on **where engineering effort creates the most future value**
