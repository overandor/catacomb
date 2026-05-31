# Risk Flags — Agent Labor Accounting Record

**Record ID:** `ala-2026-05-30-cascade-wasm-001`  
**Date:** 2026-05-30  
**System:** CollateralOps v0.1.1 / DollarFS v0.1.1

---

## Operational Risks

| # | Risk | Severity | Mitigation | Status |
|---|---|---|---|---|
| 1 | **Vercel deployment protection active** | Medium | Team admin disables or waits for rate limit reset | Open |
| 2 | **Hugging Face Space build unverified** | Medium | Check HF dashboard after initial build | Open |
| 3 | **WASM worker.html CORS in production** | Low | Serve from same origin or configure CORS headers | Open |
| 4 | **No CI/CD pipeline for automated tests** | Medium | Add GitHub Actions for pytest + wasm-pack | Open |
| 5 | **Local test environment only** | Medium | Move to cloud CI for auditable build receipts | Open |

## Security Risks

| # | Risk | Severity | Mitigation | Status |
|---|---|---|---|---|
| 6 | **DollarFS fallback trusts GitHub API size** | Medium | Implement clone-and-scan for all remote repos | Open |
| 7 | **No GPG-signed commits** | Low | Enable commit signing for audit trail | Open |
| 8 | **No immutable ledger anchoring** | Medium | Anchor proof hashes to Solana / IPFS | Open |
| 9 | **Secret scan passed but not automated** | Low | Integrate secret scanner in CI | Open |
| 9a | **Hugging Face token exposed in session log** | **Critical** | Revoke leaked token immediately; create new token; update Space secret; enforce token hygiene policy | **Open** |
| 9b | **OpenRouter API key exposed in .env.example** | **Critical** | Revoke key at https://openrouter.ai/keys; rotate immediately | **Open** |
| 9c | **Groq API key exposed in .env.example** | **Critical** | Revoke key at https://console.groq.com/keys; rotate immediately | **Open** |
| 9d | **Same Groq key hardcoded in groq_supervisor_247.py** | **Critical** | Replace with env var lookup (done); rotate key immediately | **Mitigating** |
| 9e | **Same Groq key hardcoded in groq_supervisor_fixed.py** | **Critical** | Replace with env var lookup (done); rotate key immediately | **Mitigating** |

## Legal / Ownership Risks

| # | Risk | Severity | Mitigation | Status |
|---|---|---|---|---|
| 10 | **Agent labor ownership unclear** | High | Legal review: who owns Cascade's output? | Open |
| 11 | **MIT license present but not notarized** | Low | Register copyright if commercially valuable | Open |
| 12 | **No contributor agreements** | Medium | Add CLA for external contributors | Open |

## Financial Risks

| # | Risk | Severity | Mitigation | Status |
|---|---|---|---|---|
| 13 | **No verified revenue or paid usage** | High | Launch pilot with paying lender / buyer | Open |
| 14 | **Collateral support is unilateral estimate** | Medium | Get independent third-party appraisal | Open |
| 15 | **Tokenization is Phase 2, not now** | Low | Do not issue tokens until proof packets mature | Mitigated |

---

## Risk Summary

- **Critical risks:** 5 (HF token + OpenRouter key + Groq key in .env.example + Groq key hardcoded in 2 Python files)
- **High risks:** 3 (ownership, revenue, deployment)
- **Medium risks:** 6
- **Low risks:** 6
- **Mitigated risks:** 1

**Overall risk posture:** ELEVATED (5 critical security incidents open, 2 mitigating)
**Recommendation:** 
1. Rotate ALL exposed tokens immediately: HF, OpenRouter, Groq.
2. Verify no other `.env` or `.env.example` files contain real keys.
3. Run `git filter-repo` or BFG to remove keys from git history (aider-trading-bot commit eb0225f).
4. Do not book as collateral until all critical + at least 2 high-severity risks are closed.
