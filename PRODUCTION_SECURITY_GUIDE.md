# Production Security Guide

## GitHub Token Security

### Current Status
✅ **No hardcoded tokens found** - All GitHub tokens are handled via environment variables or runtime parameters
✅ **Proper pattern** - Tokens are passed as function parameters or read from `os.getenv("GITHUB_TOKEN")`
✅ **Deployment config** - `render.yaml` correctly uses environment variables

### Security Best Practices

1. **Never commit tokens to git**
   - Tokens should always be in environment variables
   - Use `.env` files for local development (add to `.gitignore`)
   - Use secret management in production (Render/Fly/Railway secrets)

2. **Token rotation**
   - Rotate GitHub personal access tokens regularly
   - Use short-lived tokens when possible
   - Implement token expiration monitoring

3. **Token scope minimization**
   - Use minimum required scopes (e.g., `public_repo` for public repos only)
   - Avoid using tokens with admin/deployment scopes unless necessary

4. **Token storage in production**
   - Use platform secret management (Render Secrets, Fly Secrets, Railway Variables)
   - Never store tokens in database or application code
   - Use secrets injection at container startup

### Recommended Token Scopes

| Use Case | Required Scope |
|----------|----------------|
| Public repo scanning | `public_repo` |
| Private repo scanning | `repo` |
| Intervention mining | `repo` |
| PR analysis | `repo` |

### Environment Variable Configuration

```bash
# Local development
export GITHUB_TOKEN=ghp_xxxxxxxxxxxxxxxxxxxxxxxxx

# Production (Render/Fly/Railway)
# Configure via platform dashboard or CLI
```

## Audit Log Security

### Implementation Status
✅ **Audit log created** - `audit_log.py` provides immutable decision tracking
✅ **Entry hashing** - Each entry has a hash for integrity verification
✅ **Decision traceability** - Every grade, score, and recommendation is logged

### Audit Log Best Practices

1. **Immutable storage**
   - Audit logs should be write-once
   - Consider append-only database tables
   - Implement hash chain verification

2. **Retention policy**
   - Keep audit logs for minimum 7 years (financial regulations)
   - Implement archiving for old logs
   - Provide export functionality for compliance

3. **Access control**
   - Restrict audit log access to admin roles
   - Log all audit log access attempts
   - Implement audit log for the audit log (meta-audit)

## Evidence Link Verification

### Implementation Status
✅ **Evidence links added** - Review cards now include verifiable evidence links
✅ **Link extraction** - System extracts repo URLs, deployment URLs, build/test status

### Evidence Verification Requirements

1. **Link validation**
   - Verify all evidence links are accessible
   - Check for link rot periodically
   - Implement link health monitoring

2. **Evidence integrity**
   - Store hashes of evidence artifacts
   - Verify evidence hasn't changed since evaluation
   - Implement evidence versioning

3. **Evidence provenance**
   - Track source of each evidence item
   - Log evidence collection timestamp
   - Verify evidence chain of custody

## Disclaimer Requirements

### Implementation Status
✅ **Standard disclaimers added** - Review cards include mandatory disclaimers
✅ **Contextual disclaimers** - Additional disclaimers based on risk blocks and financeability

### Required Disclaimers

All review cards must include:
- "This is a draft appraisal and diligence support document"
- "Not legal advice, not tax advice, not a guaranteed sale value, not a loan approval"
- "Human review is recommended before financial decisions"
- "Appraisal is not liquidity"
- "Grades based on available evidence and may change"

## Safeguards Against Hallucinated Claims

### Implementation Status
⚠️ **In progress** - Need to implement evidence-based scoring safeguards

### Required Safeguards

1. **Evidence-based scoring**
   - Every score must have corresponding evidence
   - Scores without evidence should default to conservative values
   - Implement confidence intervals for all scores

2. **Claim verification**
   - Financeability claims must be backed by verifiable evidence
   - Market value estimates must have comparable assets
   - Buyer universe must be based on actual market data

3. **Conservative defaults**
   - When evidence is missing, assume worst case
   - Financeability score should be conservative without full evidence
   - Grade inflation should be prevented

### Implementation Plan

```python
# Add to professional_scoring.py
class EvidenceBasedScoring:
    def score_with_evidence(self, scores: Dict[str, float], evidence: Dict[str, Any]) -> Dict[str, float]:
        """Apply evidence-based scoring safeguards."""
        adjusted_scores = {}
        
        for component, score in scores.items():
            component_evidence = evidence.get(component, {})
            
            if not component_evidence:
                # No evidence - apply conservative penalty
                adjusted_scores[component] = score * 0.5
            elif component_evidence.get("verified", False):
                # Verified evidence - full score
                adjusted_scores[component] = score
            else:
                # Unverified evidence - partial score
                adjusted_scores[component] = score * 0.7
        
        return adjusted_scores
```

## Authentication and Role Separation

### Implementation Status
⚠️ **Not implemented** - Need to add authentication system

### Required Roles

1. **Public (Radar)**
   - Read-only access to public asset discovery
   - Limited evaluation features
   - No access to sensitive data

2. **Professional (Underwriter)**
   - Full evaluation capabilities
   - Review card generation
   - Portfolio management
   - Audit log access for own assets

3. **Admin (Mine)**
   - Full system access
   - Job description mining
   - Competency graph management
   - All audit logs
   - System configuration

### Authentication Implementation

```python
# Proposed authentication structure
class UserRole(Enum):
    PUBLIC = "public"
    PROFESSIONAL = "professional"
    ADMIN = "admin"

class AuthManager:
    def check_permission(self, user_role: UserRole, required_role: UserRole) -> bool:
        """Check if user has required permission."""
        role_hierarchy = {
            UserRole.PUBLIC: 0,
            UserRole.PROFESSIONAL: 1,
            UserRole.ADMIN: 2,
        }
        return role_hierarchy[user_role] >= role_hierarchy[required_role]
```

## Database Security

### Implementation Status
⚠️ **Not implemented** - Currently using local files, need Postgres migration

### Migration Requirements

1. **PostgreSQL setup**
   - Use managed Postgres (Render/Fly/Railway)
   - Enable SSL/TLS connections
   - Configure connection pooling

2. **Schema design**
   - Assets table with evidence links
   - Evaluations table with audit trail
   - Users table with role-based access
   - Audit log table with hash chain

3. **Data encryption**
   - Encrypt sensitive fields at rest
   - Use TLS for data in transit
   - Implement key rotation

## Deployment Security

### Platform-Specific Security

**Render:**
- Use Render Secrets for environment variables
- Enable automatic deploys from protected branches
- Configure build-time secrets

**Fly.io:**
- Use `fly secrets set` for sensitive data
- Enable private networking
- Configure volume encryption

**Railway:**
- Use Railway Variables for secrets
- Enable private services
- Configure deployment restrictions

### CI/CD Security

1. **Branch protection**
   - Require PR approval for main branch
   - Require status checks for deployment
   - Block secrets in PRs

2. **Secrets in CI**
   - Use platform secret management
   - Never log secrets in CI output
   - Rotate CI secrets regularly

## Compliance Checklist

- [ ] GitHub tokens stored in environment variables only
- [ ] No hardcoded credentials in code
- [ ] Audit log implemented and immutable
- [ ] All review cards include disclaimers
- [ ] Evidence links verified and accessible
- [ ] Authentication system implemented
- [ ] Role-based access control enforced
- [ ] Database encryption enabled
- [ ] TLS enabled for all connections
- [ ] Secret rotation policy documented
- [ ] Incident response plan documented
- [ ] Data retention policy documented
- [ ] Privacy policy documented
