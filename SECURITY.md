# Security Policy

## Status

Catacomb is an early-stage deterministic software-asset discovery engine. It should be treated as research and due-diligence tooling, not as a guarantee of asset value, investment return, or ownership rights.

## Core Safety Rules

1. Do not scan private repositories, local folders, or proprietary code without explicit permission.
2. Do not upload private scan outputs, `.db` files, or snapshots to public IPFS without review and encryption when required.
3. Do not store API keys, GitHub tokens, private prompts, credentials, secrets, or personally sensitive data in scan artifacts.
4. Do not represent Catacomb scores as guaranteed appraisals.
5. Do not tokenize claims over repositories or codebases without verifying ownership, license, and legal rights.

## In Scope

Security issues involving:

- Credential leakage.
- Unsafe handling of GitHub tokens.
- Private repository exposure.
- Snapshot publication of sensitive data.
- Hash/provenance tampering.
- Malicious manifest injection.
- Arbitrary file overwrite in snapshot/export paths.
- API endpoint authorization bypasses.
- Contribution/reward ledger manipulation.

## Out of Scope

- Claims that a score was economically wrong without a reproducible scoring or evidence bug.
- Market losses from acting on Catacomb reports.
- Public data already available from GitHub or package registries.
- Third-party repository vulnerabilities discovered during scanning unless Catacomb caused disclosure.

## Responsible Disclosure

If you find a vulnerability:

1. Do not publish exploit details in a public issue.
2. Contact the repository owner privately through GitHub.
3. Include affected file, function, version/commit, reproduction steps, and impact.
4. Include whether private data, credentials, or snapshots could be exposed.

## Snapshot Safety

Before publishing a LiquidDB snapshot:

- Review source scope.
- Remove secrets.
- Remove private data unless authorized.
- Confirm license and ownership status.
- Hash the final artifact.
- Record whether the artifact is public, private, encrypted, or unlisted.

## Tokenization Safety

Catacomb outputs may be used as receipts, credits, or evidence artifacts in future Overandor/Proof-of-Wave systems.

Do not market such objects as investment contracts, guaranteed-liquidity instruments, or profit-bearing tokens without legal review.

## Production Rule

Evidence first. Claims second. Liquidity last.
