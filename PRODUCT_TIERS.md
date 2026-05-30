# Catacomb Product Tiers

## Overview

Catacomb is now an innovation allocation and software asset underwriting engine. It discovers undervalued software assets, predicts valuable interventions, tracks verified outcomes, and translates software work into professional review cards, financeability grades, and liquidation pathways.

The product is split into three tiers:

## 1. Catacomb Radar (Public)

**Purpose:** Discover innovation alpha

**Target Users:** Developers, researchers, open-source maintainers

**Access Level:** Public, no authentication required

### Features

**Asset Discovery**
- Public repository scanning
- Innovation alpha detection
- Trending repositories
- Category-based exploration
- Search and filtering

**Basic Analytics**
- Star/fork growth tracking
- Activity metrics
- Contributor insights
- Technology stack analysis

**Intervention Suggestions**
- Basic intervention recommendations
- Potential impact estimates
- Effort vs. value analysis

**Limitations**
- No professional grading
- No financeability scores
- No collateral evaluation
- No review card generation
- No audit trail access
- Rate-limited API access

### Pricing
- Free for public use
- Rate-limited to 100 requests/hour
- No API key required

### Use Cases
- Discover interesting repositories
- Identify trending technologies
- Find intervention opportunities
- Research innovation patterns

---

## 2. Catacomb Underwriter (Professional)

**Purpose:** Convert software assets into reviewable finance/collateral packages

**Target Users:** Software developers, indie hackers, small studios, IP consultants

**Access Level:** Professional, authentication required

### Features

**All Radar Features** (plus)

**Professional Evaluation**
- Synthetic committee evaluation (8 evaluators)
- Production/Commercial/Collateral grading
- Financeability scoring (0-100)
- Proof level assessment
- Strategic value classification

**Capital Translation**
- Developer → finance language translation
- Professional review card generation
- Evidence link verification
- Standardized collateral language

**Liquidification Planning**
- Monetization route identification
- Buyer universe generation
- Sale difficulty assessment
- Timeline and price estimation
- Required cleanup and packaging

**Asset Desk**
- Portfolio balance sheet
- Asset register
- Financeability queue
- Risk-blocked assets view
- Buyer-ready assets view
- Collateral packet candidates

**Next Action Engine**
- Single best next action recommendation
- Action priority assignment
- Success criteria definition
- Alternative approaches

**Audit Trail**
- Per-asset audit log
- Decision traceability
- Evidence verification logs
- Exportable audit reports

**Limitations**
- No job description mining
- No competency graph editing
- No system configuration
- No admin access
- Limited to own assets

### Pricing
- $49/month for individual developers
- $199/month for small teams (up to 5 users)
- $499/month for studios (up to 20 users)
- API access included
- 1,000 evaluations/month included

### Use Cases
- Prepare software assets for sale
- Generate professional review cards
- Identify monetization routes
- Build asset portfolio
- Present to investors/lenders

---

## 3. Catacomb Mine (Admin)

**Purpose:** Extract PRs, interventions, outcomes, and transformation laws

**Target Users:** Venture studios, M&A advisors, IP brokers, enterprise teams

**Access Level:** Admin, authentication and approval required

### Features

**All Underwriter Features** (plus)

**Job Description Mining**
- Multi-source job description collection
- Role-family targeted mining
- Corpus management
- Competency extraction
- Professional judgment synthesis

**Competency Graph Management**
- Edit competency graph
- Add new role families
- Update scoring rules
- Configure evidence requirements
- Custom evaluator tuning

**Advanced Analytics**
- Outcome tracking and analysis
- Transformation law extraction
- Market trend analysis
- Buyer behavior tracking
- Liquidation outcome data

**System Configuration**
- Evaluator configuration
- Scoring rubric customization
- Evidence requirement editing
- Disclaimer template management
- API rate limit configuration

**Enterprise Features**
- SSO authentication
- Role-based access control
- Team management
- Custom integrations
- Dedicated support
- SLA guarantees

**Data Export**
- Full audit log export
- Competency graph export
- Job corpus export
- Outcome database export
- Custom report generation

### Pricing
- $2,499/month for venture studios
- $4,999/month for enterprise teams
- Custom pricing for large organizations
- Unlimited evaluations
- Priority support
- Custom integrations

### Use Cases
- Build proprietary underwriting system
- Extract transformation laws
- Analyze market outcomes
- Train custom evaluators
- Build moat with proprietary data

---

## Feature Matrix

| Feature | Radar (Public) | Underwriter (Pro) | Mine (Admin) |
|---------|----------------|-------------------|--------------|
| Asset Discovery | ✅ | ✅ | ✅ |
| Innovation Alpha | ✅ | ✅ | ✅ |
| Basic Analytics | ✅ | ✅ | ✅ |
| Intervention Suggestions | ✅ | ✅ | ✅ |
| Professional Evaluation | ❌ | ✅ | ✅ |
| Grading (Production/Commercial/Collateral) | ❌ | ✅ | ✅ |
| Financeability Scoring | ❌ | ✅ | ✅ |
| Capital Translation | ❌ | ✅ | ✅ |
| Review Card Generation | ❌ | ✅ | ✅ |
| Liquidification Planning | ❌ | ✅ | ✅ |
| Asset Desk | ❌ | ✅ | ✅ |
| Next Action Engine | ❌ | ✅ | ✅ |
| Audit Trail | ❌ | ✅ (per-asset) | ✅ (full) |
| Job Description Mining | ❌ | ❌ | ✅ |
| Competency Graph Editing | ❌ | ❌ | ✅ |
| Outcome Tracking | ❌ | ❌ | ✅ |
| System Configuration | ❌ | ❌ | ✅ |
| SSO Authentication | ❌ | ❌ | ✅ |
| Custom Integrations | ❌ | ❌ | ✅ |

---

## API Access

### Radar API
- Public endpoint
- No authentication
- Rate-limited
- Basic discovery data

### Underwriter API
- API key required
- Professional evaluation endpoints
- Review card generation
- Asset desk data
- Audit trail access (own assets)

### Mine API
- API key + additional auth
- Full system access
- Job mining endpoints
- Competency graph API
- Outcome data export
- System configuration

---

## Migration Path

### From Radar to Underwriter
Users can upgrade from Radar to Underwriter by:
1. Creating a professional account
2. Linking existing Radar assets
3. Enabling professional evaluation
4. Accessing review cards and liquidification plans

### From Underwriter to Mine
Users can upgrade from Underwriter to Mine by:
1. Applying for Mine access
2. Demonstrating use case
3. Signing enterprise agreement
4. Receiving admin credentials
5. Accessing advanced features

---

## Technical Implementation

### Authentication

**Radar:** No authentication required

**Underwriter:** 
- Email/password or OAuth (GitHub, Google)
- API key for programmatic access
- Session-based authentication

**Mine:**
- SSO (SAML, OIDC)
- Multi-factor authentication
- IP whitelisting
- Role-based access control

### Data Isolation

**Radar:** Public data only, no user-specific data

**Underwriter:** User-isolated data, audit logs per user

**Mine:** Organization-level isolation, shared competency graph, full audit access

### Rate Limits

**Radar:** 100 requests/hour

**Underwriter:** 1,000 evaluations/month (included), additional $0.10/evaluation

**Mine:** Unlimited evaluations

---

## Brand Positioning

### Radar
*"Discover innovation alpha"*
- Free, public, accessible
- Entry point to the ecosystem
- Builds user base and data

### Underwriter
*"Convert software into capital"*
- Professional, credible, actionable
- Core revenue product
- Builder-side capital translation

### Mine
*"Extract transformation laws"*
- Enterprise, proprietary, data-driven
- High-value, high-touch
- Competitive moat through data

---

## The Moat

**Radar Moat:** User base, public data, brand recognition

**Underwriter Moat:** Professional credibility, standardized review cards, capital translation

**Mine Moat:** Job description corpus, outcome database, transformation laws, proprietary competency graph

The real moat becomes: **verified intervention outcomes + professional underwriting corpus + financeability review cards**
