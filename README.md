# Catacomb

**Innovation Allocation Engine**

Catacomb finds under-recognized software assets and ranks the highest-value engineering interventions to unlock them.

## What It Does

Catacomb is an intervention intelligence system that:

1. **Discovers hidden infrastructure** - Identifies critical but under-recognized software assets through ecosystem analysis
2. **Ranks interventions by value** - Calculates Expected Value Created Per Engineering Day, not popularity
3. **Tracks outcomes** - Closed-loop intervention lifecycle with before/after metrics and verification
4. **Learns from history** - Mines GitHub PRs for verified intervention outcomes to improve predictions

## Key Product: Catacomb Radar

The Radar tab shows hidden infrastructure ranked by **Expected Value Created Per Engineering Day**. This answers:

> "Given 30 engineering days, where should effort be deployed to create the most future value?"

## Architecture

### Three-Tier Universe Model

- **Discovery Universe**: All known assets (millions)
- **Candidate Universe**: Assets passing minimum thresholds (not archived, valid license, buildable)
- **Alpha Universe**: High intervention potential (low recognition, strong foundations, ecosystem leverage)

### Value Delta Calculation

```
Value Delta = Achievable State - Current State

Achievable State = Current State × Intervention Multipliers

Intervention Multipliers:
- Documentation improvement: 1.3×
- Packaging completion: 1.5×
- CI addition: 1.4×
- API stabilization: 1.6×
- Dependency modernization: 1.2×
- Ecosystem integration: 2.0×
```

### Ecosystem KPIs

- Transitive dependency count
- Indirect ecosystem reach
- Maintainer bus factor
- Contributor concentration
- Unresolved security backlog
- Ecosystem replacement difficulty
- Downstream revenue exposure
- Migration cost

### Closed-Loop Intervention System

**Outcome Ledger v2** tracks:
- Before state (metrics before intervention)
- Predicted outcome (expected value, probability, risk)
- After state (metrics after intervention)
- Verification status (verified by GitHub PR link)
- Prediction accuracy (for model training)

**Intervention Types:**
- Documentation
- Build system
- Feature expansion
- Performance
- Migration
- Packaging
- API
- SaaS
- AI integration
- Security
- Dependency cleanup

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

- `GET /api/discover/quality` - High-value repositories
- `GET /api/discover/trending` - Fastest acceleration
- `GET /api/discover/promising` - Alpha Universe (undervalued assets only)
- `GET /api/radar` - Hidden infrastructure ranked by value per engineering day
- `POST /api/database/populate` - Batch populate database with appraisals

## Product Positioning

Catacomb is not a repository explorer. It is an **innovation allocation engine** that:

- Values **actions on repos** more than repos themselves
- Ranks by **Expected Value Created Per Engineering Day**, not stars or forks
- Prioritizes **verified intervention outcomes** over dataset size
- Focuses on **hidden infrastructure** that nobody is looking at

The goal is to consistently answer: *"Where should engineering effort be deployed to create the most future value?"*
