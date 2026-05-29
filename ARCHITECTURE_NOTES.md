# Catacomb Architecture Notes

## Main Flow (CLI + Web UI)

The primary Catacomb system uses a **3-layer architecture** with real GitHub API data:

**Entry Points:**
- `catacomb.py` - CLI interface
- `app.py` - Flask web server

**Orchestrator:**
- `orchestrator.py` - Coordinates the analysis pipeline

**3-Layer Engine (`layers.py`):**
1. **Evidence Layer** - Factual measurements from GitHub API
   - `repo_scanner.py` - Real GitHub API calls
   - `buildability_agent.py` - Real git clone and build checks
   - `code_quality_agent.py` - Real code analysis
   - `language_layer.py` - Language detection

2. **Opportunity Layer** - Assessment of latent potential
   - `novelty_agent.py` - Real GitHub API search for similar repos
   - `market_demand_agent.py` - Real GitHub API data with heuristic scoring
   - `revival_agent.py` - Real GitHub API data with heuristic scoring
   - `trajectory_agent.py` - Trajectory analysis
   - `utility_agent.py` - Utility assessment
   - `venture_agent.py` - Venture potential
   - `ml_prediction_agent.py` - Heuristic-based predictions using real data

3. **Strategy Layer** - Intervention path generation
   - `strategy_agent.py` - Generates intervention paths based on real data

**No mock data in main flow.** All agents use real GitHub API data or deterministic heuristics based on real data.

## Separate 4-Engine Architecture (Archived)

The following files implemented a **separate 4-engine architecture** that was **not used** in the main CLI/web flow. They have been moved to `archived_four_engine/` directory to avoid confusion:

- `four_engine_architecture.py` - Orchestrator for 4-engine system
- `asset_layer.py` - Asset genome and scanning (with placeholders for external APIs)
- `counterfactual_engine.py` - Counterfactual simulation
- `innovation_allocation.py` - Capital allocation optimization
- `outcome_ledger.py` - Intervention outcome tracking
- `developer_capitalization.py` - Developer reputation system
- `historical_transformations.py` - Historical transformation analysis

**Status:** These files contained placeholders for external APIs (HuggingFace, npm, PyPI, crates.io) and were not integrated with the main Catacomb flow. They represented a future/visionary architecture but are not currently used. Archived to `archived_four_engine/` directory.

## ML Models

**ML Prediction Agent (`ml_prediction_agent.py`):**
- Uses heuristic-based predictions as a placeholder for trained ML models
- Heuristics are based on **real GitHub API data** (stars, forks, commits, contributors, etc.)
- This is acceptable - heuristics are not mock data, they are deterministic scoring based on real inputs

**Intervention ML Agent (`intervention_ml_agent.py`):**
- Uses heuristic-based intervention value prediction
- Now requires real `opportunity_data` parameter (no mock data allowed)
- Heuristics based on real repo data from GitHub API

## Summary

✅ **Main flow is clean** - All agents use real GitHub API data or deterministic heuristics based on real data
✅ **No mock data in production flow** - intervention_ml_agent.py now requires real opportunity_data
⚠️ **4-engine architecture is separate** - Contains placeholders but not used in main flow
