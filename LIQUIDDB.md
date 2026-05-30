# Catacomb LiquidDB Specification

## Purpose

LiquidDB mode turns Catacomb from a command-line scanner into a portable software-asset ledger.

The database is not just cache. It is the asset container for repository facts, agent evidence, intervention paths, score histories, output reports, contributor events, and snapshot CIDs.

## Core File

```text
catacomb.db
```

The `.db` file should be SQLite for the MVP because it is portable, inspectable, easy to back up, and easy to snapshot.

## Asset Doctrine

A Catacomb database has value only when it contains evidence-backed, reproducible, useful records.

Non-zero value requires at least one of:

1. Ranked repository opportunities.
2. Evidence packets with exact measured fields.
3. Deterministic hashes of agent inputs and outputs.
4. Intervention plans with effort, probability, upside, and risk.
5. Scan provenance: query, timestamp, source, token/no-token mode, and result count.
6. Artifact outputs: reports, JSON manifests, ranked CSVs, or dashboard pages.
7. Snapshot history proving the state of the database over time.

## Tables

### scan_sessions

A scan session is a batch run initiated by a user, scheduler, API call, or worker.

```sql
CREATE TABLE scan_sessions (
  id TEXT PRIMARY KEY,
  query_type TEXT NOT NULL,
  query_value TEXT NOT NULL,
  status TEXT NOT NULL,
  started_at TEXT NOT NULL,
  finished_at TEXT,
  target_count INTEGER DEFAULT 0,
  best_score REAL DEFAULT 0,
  mean_score REAL DEFAULT 0,
  input_hash TEXT,
  output_hash TEXT,
  manifest_hash TEXT,
  notes TEXT
);
```

### targets

Repository or software artifact under analysis.

```sql
CREATE TABLE targets (
  id TEXT PRIMARY KEY,
  owner TEXT,
  repo TEXT,
  full_name TEXT UNIQUE,
  url TEXT,
  license TEXT,
  primary_language TEXT,
  stars INTEGER DEFAULT 0,
  forks INTEGER DEFAULT 0,
  open_issues INTEGER DEFAULT 0,
  last_commit_at TEXT,
  readme_hash TEXT,
  created_at TEXT NOT NULL,
  updated_at TEXT NOT NULL
);
```

### evidence_packets

Every deterministic agent output should become an evidence packet.

```sql
CREATE TABLE evidence_packets (
  id TEXT PRIMARY KEY,
  scan_id TEXT NOT NULL,
  target_id TEXT NOT NULL,
  agent_name TEXT NOT NULL,
  score REAL NOT NULL,
  confidence REAL NOT NULL,
  evidence_json TEXT NOT NULL,
  input_hash TEXT NOT NULL,
  output_hash TEXT NOT NULL,
  created_at TEXT NOT NULL,
  FOREIGN KEY(scan_id) REFERENCES scan_sessions(id),
  FOREIGN KEY(target_id) REFERENCES targets(id)
);
```

### intervention_paths

Deterministic transformation routes.

```sql
CREATE TABLE intervention_paths (
  id TEXT PRIMARY KEY,
  scan_id TEXT NOT NULL,
  target_id TEXT NOT NULL,
  name TEXT NOT NULL,
  description TEXT,
  effort_days INTEGER,
  probability REAL,
  upside REAL,
  risk_penalty REAL,
  intervention_score REAL,
  steps_json TEXT,
  output_hash TEXT NOT NULL,
  created_at TEXT NOT NULL,
  FOREIGN KEY(scan_id) REFERENCES scan_sessions(id),
  FOREIGN KEY(target_id) REFERENCES targets(id)
);
```

### capitalization_reports

Human-readable and machine-readable reports explaining the opportunity.

```sql
CREATE TABLE capitalization_reports (
  id TEXT PRIMARY KEY,
  scan_id TEXT NOT NULL,
  target_id TEXT NOT NULL,
  revival_score REAL,
  best_intervention_id TEXT,
  nonzero_value_reason TEXT,
  risk_disclosures TEXT,
  report_markdown TEXT,
  report_json TEXT,
  report_hash TEXT NOT NULL,
  created_at TEXT NOT NULL,
  FOREIGN KEY(scan_id) REFERENCES scan_sessions(id),
  FOREIGN KEY(target_id) REFERENCES targets(id)
);
```

### artifacts

Exports produced by Catacomb.

```sql
CREATE TABLE artifacts (
  id TEXT PRIMARY KEY,
  scan_id TEXT,
  target_id TEXT,
  artifact_type TEXT NOT NULL,
  path TEXT,
  cid TEXT,
  sha256 TEXT,
  size_bytes INTEGER,
  compression TEXT,
  created_at TEXT NOT NULL
);
```

### snapshots

Compressed database snapshots and their content-addressed proofs.

```sql
CREATE TABLE snapshots (
  id TEXT PRIMARY KEY,
  parent_snapshot_id TEXT,
  db_sha256 TEXT NOT NULL,
  compressed_sha256 TEXT,
  cid TEXT,
  provider TEXT,
  compression TEXT,
  size_bytes INTEGER,
  manifest_hash TEXT NOT NULL,
  created_at TEXT NOT NULL,
  deleted_local_staging INTEGER DEFAULT 0
);
```

### contributors

Addresses, accounts, or users who triggered scans, validated outputs, or produced useful deltas.

```sql
CREATE TABLE contributors (
  id TEXT PRIMARY KEY,
  contributor_type TEXT NOT NULL,
  identifier TEXT NOT NULL,
  first_seen_at TEXT NOT NULL,
  last_seen_at TEXT NOT NULL,
  reputation_score REAL DEFAULT 0
);
```

### contribution_events

Contribution ledger for Proof-of-Wave compatibility.

```sql
CREATE TABLE contribution_events (
  id TEXT PRIMARY KEY,
  scan_id TEXT,
  snapshot_id TEXT,
  contributor_id TEXT NOT NULL,
  event_type TEXT NOT NULL,
  tx_hash TEXT,
  weight REAL DEFAULT 0,
  evidence_json TEXT,
  created_at TEXT NOT NULL,
  FOREIGN KEY(contributor_id) REFERENCES contributors(id)
);
```

## Manifest Format

Every scan and snapshot should have a manifest:

```json
{
  "protocol": "catacomb.liquiddb",
  "version": "0.1.0",
  "scan_id": "scan_...",
  "snapshot_id": "snap_...",
  "target_count": 100,
  "best_score": 87.2,
  "mean_score": 51.4,
  "db_sha256": "...",
  "compressed_sha256": "...",
  "cid": "...",
  "manifest_hash": "...",
  "created_at": "2026-05-29T00:00:00Z"
}
```

## Snapshot Flow

```text
catacomb scan
→ write catacomb.db
→ compute scan manifest
→ VACUUM database
→ hash database
→ compress database
→ hash compressed artifact
→ upload to IPFS or other storage
→ record CID
→ optionally delete local compressed staging file
```

## Browser/API Surface

Suggested endpoints:

```text
/db/catacomb
/db/catacomb.json
/db/catacomb.md
/scan/{scan_id}
/scan/{scan_id}.json
/repo/{owner}/{repo}
/repo/{owner}/{repo}.json
/snapshot/{snapshot_id}
/snapshot/{snapshot_id}.json
/llms.txt
```

## Startup Meaning

LiquidDB makes Catacomb portable, ownable, auditable, and monetizable.

Without LiquidDB, Catacomb is a scanner.
With LiquidDB, Catacomb becomes a software-opportunity asset ledger.
