# Catacomb Protocol

## Definition

Catacomb is a deterministic software-asset discovery and intervention protocol.

It identifies repositories with buried value, scores them through evidence-producing agents, ranks possible interventions, and emits verifiable reports that can become LiquidDB snapshots, IPFS-published scan waves, or startup due-diligence artifacts.

## Core Primitive

```text
software artifact
→ evidence extraction
→ deterministic scoring
→ intervention modeling
→ transformation plan
→ capitalizable opportunity
```

## Protocol Objects

### Repository Target

A repository, folder, package, model, dataset, or codebase being evaluated.

Required fields:

```text
owner
repo
url
license
stars
forks
issues
pull_requests
last_commit
languages
package_manifests
readme_hash
source_hashes
```

### Evidence Packet

A deterministic packet of measured facts.

```text
evidence_id
target_id
agent_id
input_hash
output_hash
score
confidence
fields_used
timestamp
```

### Intervention Path

A proposed transformation route.

```text
path_id
target_id
name
description
effort_days
probability
upside
risk_penalty
intervention_score
steps
```

### Scan Wave

A batch of repository evaluations that can be snapshotted and published.

```text
scan_id
query_type
query_value
target_count
best_score
mean_score
created_at
manifest_hash
snapshot_cid
```

### Capitalization Report

The human-readable and machine-readable output explaining why a repository has intervention value.

```text
report_id
target_id
revival_score
best_intervention
nonzero_value_reason
risk_disclosures
hash
```

## Agent Layers

### Layer 1: Evidence

Measures what exists.

- Repo Scanner
- Buildability Agent
- Code Quality Agent
- Language Layer

### Layer 2: Opportunity

Measures latent potential.

- Revival Agent
- Novelty Agent
- Market Demand Agent
- Utility Agent
- Venture Agent
- Trajectory Agent
- ML Prediction Agent

### Layer 3: Strategy

Generates action paths.

- Strategy Agent
- Intervention Path Ranker
- Capitalization Report Writer

## Determinism Rule

Every agent output must include:

```text
score: 0-100
evidence: exact fields used
confidence: 0-1
hash: sha256(canonical_json(input) + canonical_json(output))
```

No opaque score should be accepted into the protocol without a field-level evidence packet.

## Revival Score

Initial scoring formula:

```text
Revival Score =
0.15 Technical Quality
+ 0.15 Buildability
+ 0.15 Novelty
+ 0.15 Market Demand
+ 0.15 Underexposure
+ 0.10 Abandonment Signal
+ 0.10 Forkability
+ 0.10 Transformation Potential
- Risk Penalty
```

## Non-Zero Value Doctrine

Catacomb does not claim a repository is worth money simply because it exists.

Catacomb claims non-zero opportunity value only when evidence supports at least one of these:

1. Existing user demand.
2. Under-maintained but useful code.
3. Package/dependency position.
4. Strong technical foundation.
5. Fixable buildability gap.
6. Market demand for the category.
7. Clear intervention path.
8. Low-cost transformation into a usable product or library.

## LiquidDB Mode

Catacomb scan results can be written into a portable SQLite database:

```text
catacomb.db
```

Suggested tables:

```text
targets
evidence_packets
agent_outputs
intervention_paths
scan_waves
capitalization_reports
artifacts
cid_history
contributor_events
```

## Snapshot Mode

A scan wave can be converted into a compressed snapshot:

```text
catacomb-scan-{scan_id}.db.zst
```

Then:

```text
compress → hash → upload to IPFS → record CID → publish manifest
```

## Proof-of-Wave Compatibility

Catacomb can become a worker in the broader Overandor protocol.

A useful scan wave can be treated as a data-liquidity wave:

```text
scan wave
→ evidence packets
→ intervention reports
→ LiquidDB snapshot
→ IPFS CID
→ on-chain WaveCommit
→ contributor/work receipts
```

## Safety Rules

- Do not claim guaranteed investment returns.
- Do not classify unaudited scores as appraisals unless methodology and risk are disclosed.
- Do not scan private repositories or user folders without explicit permission.
- Do not treat copied code as owned software capital.
- Do not tokenize public repository claims without respecting licenses and ownership boundaries.

## Startup Thesis

Catacomb is the search engine for buried software capital.

It turns the open-source universe and private user-approved codebases into ranked maps of possible intervention value.
