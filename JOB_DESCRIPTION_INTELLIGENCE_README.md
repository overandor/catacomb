# Catacomb: Innovation Allocation and Software Asset Underwriting Engine

## Overview

Catacomb is an innovation allocation and software asset underwriting engine. It discovers undervalued software assets, predicts valuable interventions, tracks verified outcomes, and translates software work into professional review cards, financeability grades, and liquidation pathways.

## Product Tiers

### 1. Catacomb Radar (Public)
- **Purpose:** Discover innovation alpha
- **Features:** Asset discovery, innovation alpha detection, basic analytics
- **Access:** Public, no authentication
- **Pricing:** Free

### 2. Catacomb Underwriter (Professional)
- **Purpose:** Convert software assets into reviewable finance/collateral packages
- **Features:** Professional evaluation, grading, capital translation, review cards, liquidification planning
- **Access:** Professional, authentication required
- **Pricing:** $49-$499/month

### 3. Catacomb Mine (Admin)
- **Purpose:** Extract PRs, interventions, outcomes, and transformation laws
- **Features:** Job description mining, competency graph management, outcome tracking, system configuration
- **Access:** Admin, approval required
- **Pricing:** $2,499-$4,999/month

See [PRODUCT_TIERS.md](PRODUCT_TIERS.md) for complete details.

## The Developer Asset Underwriter

The Job-Description Intelligence Engine manufactures the missing professional layer between software builders and capital. It understands software from the developer side, evaluates risk like an auditor, routes assets like a broker, and translates proof into collateral language.

**The product's strongest claim:** CollateralOps manufactures the missing professional layer between software builders and capital.

## Core Concept

The missing professional is not one job title. It is a synthetic role created from many overlapping professions:

**Developer Asset Underwriter**

This is the person who understands software like a senior developer, evaluates risk like an auditor, thinks about liquidity like a broker, and translates work into collateral language without becoming bank-first.

## Architecture

### 1. Role Taxonomy (22 Role Families)

The system mines job descriptions across these role families to extract professional judgment:

- Software Due Diligence Engineer
- Technical M&A Analyst
- Startup CTO Advisor
- Venture Studio Technical Lead
- Software Acquisition Analyst
- Open-Source Compliance Specialist
- Application Security Auditor
- DevOps/SRE Reviewer
- Technical Product Manager
- IP Commercialization Analyst
- Technology Transfer Officer
- Patent Licensing Analyst
- Innovation Scout
- Micro-SaaS Acquisition Analyst
- Revenue-Based Finance Underwriter
- Asset-Based Lending Analyst
- Collateral Analyst
- AI Governance Analyst
- AI Agent Evaluator
- Software Asset Manager
- Technical Program Manager
- Developer Relations Lead
- Platform Ecosystem Analyst

### 2. Competency Graph

The system builds a graph: `role → competency → signal → evidence → scoring rule → artifact`

Example:
```
Software Due Diligence Engineer
→ production readiness
→ tests, CI, deployment, architecture, maintainability
→ package files, test logs, GitHub Actions, Dockerfile
→ score production readiness
→ technical diligence memo
```

### 3. Synthetic Committee

The product behaves like a committee, not one model. Each evaluator has a job:

- **Engineering Evaluator**: Determines whether the asset is real software, scaffold, prototype, or production-grade
- **Execution Evaluator**: Checks whether it runs, builds, tests, deploys, exposes endpoints, or produces outputs
- **Security Evaluator**: Flags secrets, unsafe patterns, private keys, dangerous dependencies, PII, or risky behavior
- **License and Originality Evaluator**: Checks license clarity, fork risk, copied code, template dependence, ownership ambiguity
- **Market Evaluator**: Determines who would need the asset, what category it belongs to, and whether it has buyer relevance
- **Collateral Evaluator**: Determines whether the asset can support a credit memo, liquidation route, monitoring plan, collateral support range
- **Liquidation Evaluator**: Finds the practical path to cash: sale, licensing, API, service, report, buyer outreach, broker submission
- **Agent Labor Evaluator**: Determines whether AI-agent work created capitalizable assets or just generated cleanup burden

### 4. Asset Classification

The system distinguishes between 16+ asset types:

- Real production system
- Working prototype
- Research prototype
- Internal tool
- API service
- Frontend product
- Backend service
- Smart contract/protocol
- Trading engine
- Data pipeline
- Hugging Face Space
- Prompt system
- Agent workflow
- Documentation package
- Valuation ledger
- Proof ledger
- Sales/outreach tool
- Fork/template
- Scaffold
- Duplicate
- Junk
- Risk-blocked

### 5. Professional Scoring System

Separate grades, not one number:

**Production Grade** (A+ to F)
- How real, maintainable, executable, and technically complete the asset is

**Commercial Grade** (A+ to F)
- How useful, understandable, sellable, and productizable it is

**Collateral Grade** (A+ to F)
- How recoverable, transferable, monitorable, and lender-readable it is

**Financeability Score** (0-100)
- The final readiness score for capital recognition

**100-point base rubric:**
- Engineering substance: 20
- Execution proof: 15
- Originality and ownership: 15
- Security and license cleanliness: 15
- Market usefulness: 15
- Liquidation path: 10
- Documentation and packaging: 5
- Revenue/adoption proof: 5

### 6. Capital Translation Layer

Converts developer language to finance language:

**Developer:** "This is a local Python app that scans repos and estimates value."

**Capital:** "This is a software asset appraisal tool with potential use in developer portfolio audits, IP diligence, and buyer packet generation. Current strategic value exceeds collateral support because recoverability is limited by lack of revenue proof, reviewer validation, and buyer outcome history."

### 7. Liquidification Layer

Answers: How does this asset move toward cash?

Monetization routes:
- Sell as standalone codebase
- Package as micro-SaaS
- Turn into hosted API
- Turn into Hugging Face Space
- License to strategic buyer
- Sell as data/report package
- Submit to IP broker
- Submit to venture studio
- Submit to accelerator
- Offer to software M&A buyer
- Open-source with paid services
- Bundle with related repos
- Archive as non-financeable

### 8. Professional Review Card

Every asset ends with a card like this:

```
Asset: Repo Appraiser Pro

Classification:
Software asset appraisal and proof-packet generator

Production Grade:
B

Commercial Grade:
B+

Collateral Grade:
C+

Financeability Score:
61/100

Proof Level:
Level 3 — Clean / partially verified

Strategic Value:
High

Buyer-Today Value:
Moderate

Collateral Support:
Conservative and conditional

Main Blockers:
No outcome database
No human reviewer layer
No verified buyer response
Build/deployment proof incomplete

Best Next Action:
Generate three sample paid audit packets and record buyer response.

Likely Route:
IP consultants, venture studios, developer tooling buyers, software M&A advisors.

Packet Readiness:
Buyer-ready after packaging.
Lender-ready only after review and outcome evidence.
```

### 9. Asset Desk UI

The UI looks like an asset desk, not a file explorer:

Main views:
- Portfolio Balance Sheet
- Asset Register
- Financeability Queue
- Risk-Blocked Assets
- Buyer-Ready Assets
- Lender-Ready Assets
- Collateral Packet Candidates
- Agent Work Accounting
- Outcome Ledger

Dashboard example:
```
You have 121 discovered software objects.

17 are real assets.
31 are scaffolds.
12 are duplicates.
9 are risk-blocked.
6 are buyer-ready.
3 are collateral-packet candidates.
0 are fully financeable today.

Best next action:
Verify build and deployment proof for the top 3 assets.
```

### 10. One Best Next Action

The system ends with ONE main action, not twenty vague recommendations:

- "Add a reproducible build log and deployment URL."
- "Resolve license ambiguity before generating a buyer packet."
- "Bundle this with two related repos and package as a single API product."
- "Send the buyer memo to 20 qualified targets and record responses."
- "Do not monetize yet. Remove secrets and separate original code from forked code."

## Components

### Core Files

1. **job_description_intelligence.py** - Role taxonomy, job description corpus, competency graph
2. **synthetic_committee.py** - 8 evaluators (Engineering, Execution, Security, License, Market, Collateral, Liquidation, Agent Labor)
3. **professional_scoring.py** - Professional grading system (Production, Commercial, Collateral, Financeability)
4. **capital_translation.py** - Developer → finance language translation
5. **liquidification_layer.py** - Monetization routes and liquidification plans
6. **professional_review_card.py** - Professional review card generator
7. **asset_desk_ui.py** - Asset desk dashboard and views
8. **next_action_engine.py** - One best next action recommendation
9. **job_description_miner.py** - Job description mining and corpus management
10. **developer_asset_underwriter.py** - Main orchestrator integrating all components

## Usage

### Basic Asset Evaluation

```python
from developer_asset_underwriter import DeveloperAssetUnderwriter

# Initialize the system
underwriter = DeveloperAssetUnderwriter()

# Prepare asset data
asset_data = {
    "asset_id": "example_repo_1",
    "asset_name": "Repo Appraiser Pro",
    "classification": "real_production_system",
    "primary_language": "python",
    "file_count": 45,
    "has_tests": True,
    "has_ci_cd": True,
    "has_documentation": True,
    "code_quality_score": 75,
    "build_status": "passed",
    "test_status": "passed",
    "deployment_status": "deployable",
    "has_license": True,
    "license_type": "MIT",
    # ... more asset data
}

# Evaluate the asset
evaluation = underwriter.evaluate_asset(
    asset_data,
    developer_description="This is a local Python app that scans repos and estimates value"
)

# Export review card
print(underwriter.export_evaluation_report(evaluation, format="text"))
```

### Portfolio Evaluation

```python
# Evaluate multiple assets
portfolio_result = underwriter.evaluate_portfolio(asset_data_list)

# Access dashboard
print(portfolio_result["portfolio_summary"])
print(portfolio_result["best_next_action"])
print(portfolio_result["priority_assets"])
```

### Job Description Mining

```python
# Mine job descriptions to build competency graph
mining_result = underwriter.mine_job_descriptions(
    role_families=["software_due_diligence_engineer", "ip_commercialization_analyst"]
)

# Build competency graph from corpus
competency_graph = underwriter.build_competency_graph_from_corpus()
```

### Asset Desk Views

```python
# Generate specific views
balance_sheet = underwriter.generate_asset_desk_view(
    "portfolio_balance_sheet",
    evaluations
)

asset_register = underwriter.generate_asset_desk_view(
    "asset_register",
    evaluations
)

buyer_ready = underwriter.generate_asset_desk_view(
    "buyer_ready_assets",
    evaluations
)
```

## The Professional Feel

The system creates professional judgment, not generic text:

- **Not:** "AI thinks this is valuable"
- **Yes:** "This asset was reviewed against a professional competency graph derived from technical diligence, software commercialization, compliance, and collateral underwriting roles."

The developer is not begging a lender to understand code. The developer is presenting standardized evidence.

## Builder-Side Capital Translation

The ideological center: **Builder-side capital translation**

The product is not built to help banks discount developers. It is built to help developers become legible to capital without losing control.

The product says: "Your work may have value, but capital does not recognize raw complexity. We convert your work into proof, packets, risks, values, and routes."

That preserves the developer's position and creates the power shift.

## The Moat

The job corpus becomes a moat:

**First version:** Job descriptions define professional judgment
**Better version:** Outcomes from real transactions

**Loop:**
```
job descriptions → professional judgment → evaluator scores → packets → 
outcomes → scoring improvement → better buyer matching → better underwriting
```

At first, use the labor market's definition of professional competence. Later, use your own transaction outcomes.

That is the moat. The job corpus creates the synthetic professional. The outcome corpus makes it smarter than the market.
