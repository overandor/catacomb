# Collateral Support Schedule — Agent Labor Accounting Record

**Record ID:** `ala-2026-05-30-cascade-wasm-001`  
**Date:** 2026-05-30  
**Asset:** DollarFS / MEMBRA Company OS  
**System:** CollateralOps v0.1.1

---

## Schedule Philosophy

Collateral support is released in **tranches** as proof conditions are met.  
No single tranche is fully released until all preceding conditions are verified.

---

## Tranche 1: Code Verification ($1,000 – $2,500)

**Conditions:**
- [x] DollarFS secure scanner created and tested
- [x] 10 regression tests pass locally
- [x] Underwriting engine patched to use secure metrics
- [x] Commit `395852a` tagged `dollarfs-v0.1.1`

**Evidence required:**
- `test_results.txt` showing 10/10 passed
- `git_commit_proof.txt` showing commit hash and diff stat

**Release:** $1,500 (conservative)

---

## Tranche 2: Build + Deployment Verification ($1,500 – $3,500)

**Conditions:**
- [x] WASM builds successfully (479KB .wasm)
- [x] Node E2E tests pass (6/6)
- [x] Vite build passes (157KB bundle)
- [ ] Vercel deployment protection disabled
- [ ] Hugging Face Space build verified

**Evidence required:**
- `wasm_build_receipt.txt`
- Live URL responding with 200 OK
- Deployment status JSON confirming "operational"

**Release:** $2,500 (upon live verification)

---

## Tranche 3: API Product Surface ($2,000 – $4,000)

**Conditions:**
- [x] 7 new POST routes operational
- [x] CSV/JSON export working
- [x] Balance-sheet feed serving data
- [ ] API documentation published
- [ ] Rate limits and auth defined

**Evidence required:**
- `api_route_manifest.json`
- Live curl examples for each route
- Swagger / OpenAPI spec

**Release:** $3,000 (upon public API docs)

---

## Tranche 4: Ownership + Legal ($1,000 – $2,000)

**Conditions:**
- [ ] Legal review confirms MIT license is valid
- [ ] Ownership of agent output clarified (human operator vs. agent)
- [ ] Contributor agreement in place
- [ ] No third-party IP contamination

**Evidence required:**
- Legal opinion letter
- Clean IP scan report
- Signed contributor agreements

**Release:** $1,500 (upon legal clearance)

---

## Tranche 5: Market / Buyer Evidence ($1,500 – $3,000)

**Conditions:**
- [ ] Buyer memo distributed to 3+ targets
- [ ] At least 1 expressed interest or LOI
- [ ] Comparable transaction identified
- [ ] Liquidation route documented

**Evidence required:**
- Buyer memo with recipient list
- LOI or email evidence of interest
- Comparable transaction data

**Release:** $2,000 (upon LOI or verifiable interest)

---

## Total Collateral Support Range

| Scenario | Support (USD) | Probability |
|---|---|---|
| **Pessimistic (Tranche 1 only)** | $1,500 | 20% |
| **Base case (Tranches 1-3)** | $7,000 | 50% |
| **Optimistic (All tranches)** | $10,500 | 20% |
| **Full monetization** | $15,000+ | 10% |

**Weighted expected collateral support:** ~$7,200

---

## Conservative Facility Recommendation

- **Maximum facility size:** $3,500 (50% of base case)
- **LTV:** 35% of capitalizable work ($8,900)
- **Term:** 12 months, with quarterly re-appraisal
- **Covenants:** Must close 2 tranche conditions per quarter
- **Default recovery:** Asset sale to strategic acquirer or PE

---

*This schedule is produced by CollateralOps v0.1.1. It is a conservative, condition-based framework. It is not an offer of credit. All conditions must be independently verified before any capital is released.*
