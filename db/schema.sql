-- Catacomb LiquidDB schema v0.1.0
-- Portable SQLite ledger for software-asset discovery, evidence packets, scan waves, and snapshot history.

PRAGMA foreign_keys = ON;
PRAGMA journal_mode = WAL;

CREATE TABLE IF NOT EXISTS scan_sessions (
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

CREATE TABLE IF NOT EXISTS targets (
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

CREATE TABLE IF NOT EXISTS evidence_packets (
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
  FOREIGN KEY(scan_id) REFERENCES scan_sessions(id) ON DELETE CASCADE,
  FOREIGN KEY(target_id) REFERENCES targets(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS intervention_paths (
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
  FOREIGN KEY(scan_id) REFERENCES scan_sessions(id) ON DELETE CASCADE,
  FOREIGN KEY(target_id) REFERENCES targets(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS capitalization_reports (
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
  FOREIGN KEY(scan_id) REFERENCES scan_sessions(id) ON DELETE CASCADE,
  FOREIGN KEY(target_id) REFERENCES targets(id) ON DELETE CASCADE,
  FOREIGN KEY(best_intervention_id) REFERENCES intervention_paths(id) ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS artifacts (
  id TEXT PRIMARY KEY,
  scan_id TEXT,
  target_id TEXT,
  artifact_type TEXT NOT NULL,
  path TEXT,
  cid TEXT,
  sha256 TEXT,
  size_bytes INTEGER,
  compression TEXT,
  created_at TEXT NOT NULL,
  FOREIGN KEY(scan_id) REFERENCES scan_sessions(id) ON DELETE SET NULL,
  FOREIGN KEY(target_id) REFERENCES targets(id) ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS snapshots (
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
  deleted_local_staging INTEGER DEFAULT 0,
  FOREIGN KEY(parent_snapshot_id) REFERENCES snapshots(id) ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS contributors (
  id TEXT PRIMARY KEY,
  contributor_type TEXT NOT NULL,
  identifier TEXT NOT NULL,
  first_seen_at TEXT NOT NULL,
  last_seen_at TEXT NOT NULL,
  reputation_score REAL DEFAULT 0,
  UNIQUE(contributor_type, identifier)
);

CREATE TABLE IF NOT EXISTS contribution_events (
  id TEXT PRIMARY KEY,
  scan_id TEXT,
  snapshot_id TEXT,
  contributor_id TEXT NOT NULL,
  event_type TEXT NOT NULL,
  tx_hash TEXT,
  weight REAL DEFAULT 0,
  evidence_json TEXT,
  created_at TEXT NOT NULL,
  FOREIGN KEY(scan_id) REFERENCES scan_sessions(id) ON DELETE SET NULL,
  FOREIGN KEY(snapshot_id) REFERENCES snapshots(id) ON DELETE SET NULL,
  FOREIGN KEY(contributor_id) REFERENCES contributors(id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_scan_sessions_query ON scan_sessions(query_type, query_value);
CREATE INDEX IF NOT EXISTS idx_targets_full_name ON targets(full_name);
CREATE INDEX IF NOT EXISTS idx_evidence_scan_target ON evidence_packets(scan_id, target_id);
CREATE INDEX IF NOT EXISTS idx_evidence_agent ON evidence_packets(agent_name);
CREATE INDEX IF NOT EXISTS idx_intervention_score ON intervention_paths(intervention_score DESC);
CREATE INDEX IF NOT EXISTS idx_reports_revival_score ON capitalization_reports(revival_score DESC);
CREATE INDEX IF NOT EXISTS idx_snapshots_cid ON snapshots(cid);
CREATE INDEX IF NOT EXISTS idx_contribution_scan ON contribution_events(scan_id);
