# Catacomb Wave Export

## Purpose

Wave Export turns a Catacomb scan into a verifiable data-liquidity wave.

A wave is a batch of useful repository intelligence: scanned targets, evidence packets, intervention paths, capitalization reports, contributor events, and a snapshot manifest.

## Wave Definition

```text
Catacomb Wave =
  scan session
  + ranked repo targets
  + deterministic evidence packets
  + intervention plans
  + capitalization reports
  + contributor ledger
  + compressed LiquidDB snapshot
  + IPFS CID or content-addressed storage pointer
```

## Why This Matters

A single scan output is temporary.
A wave is persistent.

A wave can be:

- inspected by humans,
- parsed by agents,
- downloaded as a `.db`,
- verified by hash,
- pinned to IPFS,
- referenced by URL,
- used as a due-diligence artifact,
- and eventually anchored on-chain as a receipt.

## Wave Manifest

```json
{
  "protocol": "catacomb.wave",
  "version": "0.1.0",
  "wave_id": "wave_20260529_001",
  "parent_wave_id": null,
  "scan_id": "scan_20260529_001",
  "db_snapshot": {
    "filename": "catacomb-wave_20260529_001.db.zst",
    "sha256": "...",
    "size_bytes": 123456,
    "compression": "zst",
    "cid": "bafy..."
  },
  "metrics": {
    "targets_scanned": 100,
    "evidence_packets": 700,
    "intervention_paths": 320,
    "capitalization_reports": 100,
    "best_revival_score": 91.2,
    "mean_revival_score": 54.8
  },
  "roots": {
    "target_root": "...",
    "evidence_root": "...",
    "intervention_root": "...",
    "contributor_root": "..."
  },
  "justification": {
    "model": "deterministic-or-llm-route",
    "report_hash": "...",
    "summary": "This wave has non-zero value because it contains ranked repository opportunities with evidence-backed intervention paths."
  },
  "created_at": "2026-05-29T00:00:00Z"
}
```

## Non-Zero Value Justification

Each wave should include a short report explaining why it has non-zero value.

The report must be bounded by deterministic facts.

Acceptable claims:

- Number of repositories scanned.
- Number of evidence packets produced.
- Number of intervention paths generated.
- Presence of high-scoring candidates.
- Presence of clear build/revival/monetization paths.
- Freshness of scan.
- Reproducibility of hashes and manifests.

Unsafe claims:

- Guaranteed profit.
- Guaranteed liquidity.
- Ownership of public repositories not owned by the user.
- Investment return promises.
- Token price predictions.

## Worker Model

A contributor can be treated as a worker when they perform useful actions:

- trigger a scan,
- provide a target list,
- validate a result,
- submit a correction,
- improve an intervention path,
- run a buildability check,
- publish a snapshot,
- pin a CID,
- or execute a successful repo transformation.

## Contribution Weight

Contribution weight should be computed from observable work, not vibes.

```text
contribution_weight =
  scan_trigger_weight
  + verified_target_weight
  + validation_weight
  + build_check_weight
  + correction_weight
  + transformation_weight
  - spam_penalty
  - duplicate_penalty
```

## On-Chain Compatibility

The MVP does not need on-chain deployment.

When ready, a chain contract should store only:

```text
wave_id
parent_wave_id
snapshot_cid
snapshot_hash
manifest_hash
contributor_root
justification_hash
worker_address
timestamp
```

The full data remains in the LiquidDB snapshot.

## Token Safety

If tokens are added, start with utility objects:

1. Wave Receipt — proves a wave exists.
2. Work Credit — redeemable for scans, API calls, exports, or dashboard access.
3. Membership Receipt — proves participation.
4. Reputation Signal — non-transferable worker history.

Do not launch as speculative investment tokens without legal review.

## Liquidity Migration

The latest valid wave becomes the active market surface:

```text
/db/catacomb/latest
```

Historical waves remain addressable:

```text
/db/catacomb/wave/{wave_id}
```

Liquidity migration means attention, usage, API calls, and access demand move from older waves to fresher, higher-quality waves.

## First Wave Target

The first useful Catacomb wave should be:

```text
Query: hidden infrastructure repositories
Targets: 100 repositories
Output: ranked intervention list
Artifacts: catacomb.db, manifest.json, top_25.md, top_25.csv
Snapshot: compressed database with CID
```

## Operator Rule

The wave is valuable only if the underlying evidence is inspectable.

No inspectable evidence, no capitalizable wave.
