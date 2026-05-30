# Catacomb Roadmap

## Phase 0: Protocol Identity

Goal: define Catacomb as a deterministic software-asset capitalization engine.

Completed:

- Startup status document.
- Protocol specification.
- LiquidDB specification.
- Wave export specification.
- SQLite schema.

## Phase 1: LiquidDB MVP

Goal: make scan results durable and portable.

Tasks:

- Add `catacomb db init` command.
- Add scan-session persistence.
- Store targets, evidence packets, intervention paths, and reports.
- Add JSON export for each scan.
- Add deterministic canonical JSON hashing helper.
- Add tests for score and hash determinism.

Exit criteria:

- A topic scan writes a complete scan session into `catacomb.db`.
- The same input produces stable hashes.
- A user can query historical scans.

## Phase 2: Snapshot Engine

Goal: make Catacomb outputs verifiable artifacts.

Tasks:

- Add `catacomb snapshot create`.
- VACUUM database before snapshot.
- Hash raw `.db` file.
- Compress snapshot artifact.
- Hash compressed artifact.
- Emit `manifest.json`.
- Optionally delete local staging after publish.

Exit criteria:

- Each scan wave can produce a compressed database snapshot and manifest.

## Phase 3: IPFS / CID Publishing

Goal: make Catacomb scan waves content-addressed.

Tasks:

- Add local Kubo IPFS publisher.
- Add Pinata publisher.
- Record CID in `snapshots` table.
- Add `catacomb snapshot history`.
- Add `/latest` manifest convention.

Exit criteria:

- A scan wave can be published to IPFS and recovered from CID metadata.

## Phase 4: API and Browser Surface

Goal: turn Catacomb into a browser-readable and machine-readable service.

Tasks:

- Add FastAPI or Flask API.
- Add `/db/catacomb` browser page.
- Add `/db/catacomb.json` manifest.
- Add `/scan/{scan_id}`.
- Add `/repo/{owner}/{repo}`.
- Add `/llms.txt`.

Exit criteria:

- Humans, apps, and agents can read the same Catacomb data through URLs.

## Phase 5: Wave/Contribution Layer

Goal: make useful scans attributable to workers and contributors.

Tasks:

- Add contributor table integration.
- Add scan-trigger contribution events.
- Add validation contribution events.
- Add contribution weights.
- Add contributor-root manifest field.
- Add reward-safe export file for future token contracts.

Exit criteria:

- Each wave can identify who contributed useful work and why.

## Phase 6: Hosted Product

Goal: launch Catacomb as a software-opportunity intelligence product.

Tasks:

- Add dashboard.
- Add saved watchlists.
- Add recurring scans.
- Add paid API tier.
- Add CSV/JSON/PDF reports.
- Add private repo/user-approved folder scanning.
- Add design-partner workflow.

Exit criteria:

- Catacomb can produce sellable due-diligence reports and recurring hidden-asset feeds.

## Phase 7: Overandor Integration

Goal: connect Catacomb to the broader Overandor Proof-of-Wave stack.

Tasks:

- Export wave manifests.
- Export contributor roots.
- Export snapshot hashes.
- Define WaveCommit contract interface.
- Keep tokens as receipts/credits, not investment promises.

Exit criteria:

- Catacomb can serve as the first real worker/data engine for Overandor.
