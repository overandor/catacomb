# Catacomb Deterministic Agent Stack

**7 deterministic agents. No vibes. Evidence or shut up.**

## MVP Agents (4)

1. **Repo Scanner Agent** - Collects repo facts: stars, forks, commits, issues, PRs, license, languages, files, README, package manifests
2. **Buildability Agent** - Checks if it can install, build, test, run, and reproduce
3. **Revival Agent** - Determines whether it is underdeveloped, abandoned, underexposed, forkable, and worth reviving
4. **Strategy Agent** - Generates the deterministic takeover path: fork, contact maintainer, rebuild, reposition, monetize, launch

## Future Agents (3)

5. **Code Quality Agent** - Scores structure, complexity, dependency health, docs, tests, CI, maintainability
6. **Novelty Agent** - Compares category, keywords, embeddings, repo similarity, package similarity, and duplicate risk
7. **Market Demand Agent** - Measures category demand from GitHub trends, package downloads, job/funding signals, search/category momentum

## Deterministic Output

Every agent outputs:
```text
score: 0–100
evidence: exact fields used
confidence: 0–1
hash: sha256(input + output)
```

## Revival Score Formula

```
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

## Usage

```bash
# Install dependencies
pip install -r requirements.txt

# Set GitHub token (optional, for higher rate limits)
export GITHUB_TOKEN=your_token

# Scan by topic
python catacomb.py topic "machine-learning"

# Scan by username
python catacomb.py user "username"

# Scan specific repo
python catacomb.py repo "owner/repo"
```

## Output

Ranked list of repos with revival scores and deterministic evidence.
