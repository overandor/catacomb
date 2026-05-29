#!/usr/bin/env python3
"""
GitHub Intervention Miner - Extracts intervention traces from GitHub activity.

This module mines GitHub repositories for completed interventions:
- Merged PRs (features, refactors, migrations, docs)
- Releases (version launches, breaking changes)
- Issue closures (feature requests, bug fixes)
- CI/CD additions
- Package publications

Extracts:
- Intervention type
- Before state (metrics before intervention)
- After state (metrics after intervention)
- Merged PR details
- Release date
- Author
- Affected files
- Stars/forks/contributors before and after
- Verification link

Classifies interventions into:
- documentation
- build system
- feature expansion
- performance
- migration
- packaging
- API
- SaaS
- AI integration
- security
- dependency cleanup
"""

import sys
sys.path.insert(0, '/Users/alep/Downloads/02_AI_Agents/catacomb')

from outcome_ledger_v2 import OutcomeLedger, VerificationStatus
from innovation_elo import InnovationElo
from transformation_tracking import TransformationTracker
from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime, timedelta
import requests
import time
import re
import json


class InterventionClassifier:
    """Classifies interventions into categories based on PR/issue content."""
    
    INTERVENTION_TYPES = [
        "documentation",
        "build_system",
        "feature_expansion",
        "performance",
        "migration",
        "packaging",
        "api",
        "saas",
        "ai_integration",
        "security",
        "dependency_cleanup"
    ]
    
    KEYWORD_PATTERNS = {
        "documentation": [
            r"doc", r"readme", r"docs", r"documentation", r"comment", r"guide",
            r"tutorial", r"example", r"md", r".md", r"changelog"
        ],
        "build_system": [
            r"build", r"ci", r"cd", r"workflow", r"action", r"makefile", r"cmake",
            r"gradle", r"maven", r"webpack", r"vite", r"rollup", r"esbuild"
        ],
        "feature_expansion": [
            r"feat", r"feature", r"add", r"new", r"implement", r"support",
            r"enable", r"introduce", r"extend"
        ],
        "performance": [
            r"perf", r"performance", r"optimize", r"optimization", r"speed",
            r"fast", r"slow", r"latency", r"throughput", r"cache"
        ],
        "migration": [
            r"migrate", r"migration", r"upgrade", r"update", r"rewrite", r"refactor",
            r"port", r"convert", r"transition"
        ],
        "packaging": [
            r"package", r"publish", r"npm", r"pypi", r"crate", r"gem", r"wheel",
            r"setup\.py", r"package\.json", r"cargo\.toml"
        ],
        "api": [
            r"api", r"endpoint", r"rest", r"graphql", r"rpc", r"interface",
            r"client", r"sdk", r"library"
        ],
        "saas": [
            r"cloud", r"saas", r"host", r"hosting", r"managed", r"service",
            r"platform", r"enterprise"
        ],
        "ai_integration": [
            r"ai", r"ml", r"model", r"llm", r"gpt", r"gpt-\d", r"embedding", r"vector",
            r"neural", r"transformer", r"inference", r"openai", r"anthropic", r"claude"
        ],
        "security": [
            r"security", r"vuln", r"cve", r"fix", r"patch", r"secure", r"auth",
            r"permission", r"access"
        ],
        "dependency_cleanup": [
            r"dep", r"depend", r"upgrade", r"update", r"remove", r"cleanup",
            r"audit", r"lockfile"
        ]
    }
    
    @classmethod
    def classify(cls, title: str, description: str = "", files_changed: List[str] = None) -> str:
        """
        Classify an intervention based on title, description, and files changed.
        
        Args:
            title: PR/issue title
            description: PR/issue description
            files_changed: List of files changed in PR
            
        Returns:
            Intervention type string
        """
        text = f"{title} {description}".lower()
        
        if files_changed:
            files_text = " ".join(files_changed).lower()
            text += " " + files_text
        
        scores = {}
        for intervention_type, patterns in cls.KEYWORD_PATTERNS.items():
            score = 0
            for pattern in patterns:
                if re.search(pattern, text, re.IGNORECASE):
                    score += 1
            scores[intervention_type] = score
        
        # Return type with highest score, default to feature_expansion
        if not scores or max(scores.values()) == 0:
            return "feature_expansion"
        
        return max(scores, key=scores.get)


class GitHubInterventionMiner:
    """
    Mines GitHub repositories for intervention traces.
    
    Extracts completed interventions from:
    - Merged PRs
    - Releases
    - Closed issues
    """
    
    def __init__(self, github_token: str = None):
        self.github_token = github_token
        self.classifier = InterventionClassifier()
        self.rate_limit_remaining = 5000
        self.rate_limit_reset = None
    
    def _make_request(self, url: str, params: Dict = None) -> Optional[Dict]:
        """Make authenticated GitHub API request with rate limiting."""
        if not self.github_token:
            print("Warning: No GitHub token provided")
            return None
        
        headers = {"Authorization": f"token {self.github_token}"}
        
        # Check rate limit
        if self.rate_limit_remaining < 10:
            if self.rate_limit_reset:
                wait_time = max(self.rate_limit_reset - time.time(), 1)
                print(f"Rate limit approaching, sleeping {wait_time:.0f}s")
                time.sleep(wait_time)
        
        try:
            response = requests.get(url, headers=headers, params=params)
            response.raise_for_status()
            
            # Update rate limit info
            self.rate_limit_remaining = int(response.headers.get('X-RateLimit-Remaining', 5000))
            self.rate_limit_reset = int(response.headers.get('X-RateLimit-Reset', time.time() + 3600))
            
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"GitHub API error: {e}")
            return None
    
    def fetch_repo_metrics(self, owner: str, repo: str) -> Dict[str, int]:
        """Fetch current metrics for a repository."""
        data = self._make_request(f"https://api.github.com/repos/{owner}/{repo}")
        
        if not data:
            return {"stars": 0, "forks": 0, "contributors": 0}
        
        # Fetch contributors count
        contributors_data = self._make_request(f"https://api.github.com/repos/{owner}/{repo}/contributors")
        contributors_count = len(contributors_data) if contributors_data else 0
        
        return {
            "stars": data.get("stargazers_count", 0),
            "forks": data.get("forks_count", 0),
            "contributors": contributors_count,
            "open_issues": data.get("open_issues_count", 0),
            "language": data.get("language", "unknown")
        }
    
    def fetch_merged_prs(
        self,
        owner: str,
        repo: str,
        limit: int = 100,
        since: str = None
    ) -> List[Dict[str, Any]]:
        """
        Fetch merged PRs from a repository.
        
        Args:
            owner: Repository owner
            repo: Repository name
            limit: Maximum number of PRs to fetch
            since: ISO date string to fetch PRs since
            
        Returns:
            List of PR data
        """
        params = {
            "state": "closed",
            "sort": "updated",
            "direction": "desc",
            "per_page": min(limit, 100)
        }
        
        if since:
            params["since"] = since
        
        url = f"https://api.github.com/repos/{owner}/{repo}/pulls"
        data = self._make_request(url, params)
        
        if not data:
            return []
        
        # Filter only merged PRs
        merged_prs = [pr for pr in data if pr.get("merged_at")]
        
        return merged_prs[:limit]
    
    def fetch_pr_details(self, owner: str, repo: str, pr_number: int) -> Optional[Dict[str, Any]]:
        """Fetch detailed information about a specific PR."""
        url = f"https://api.github.com/repos/{owner}/{repo}/pulls/{pr_number}"
        return self._make_request(url)
    
    def fetch_pr_files(self, owner: str, repo: str, pr_number: int) -> List[str]:
        """Fetch list of files changed in a PR."""
        url = f"https://api.github.com/repos/{owner}/{repo}/pulls/{pr_number}/files"
        data = self._make_request(url)
        
        if not data:
            return []
        
        return [f.get("filename", "") for f in data]
    
    def fetch_releases(
        self,
        owner: str,
        repo: str,
        limit: int = 50
    ) -> List[Dict[str, Any]]:
        """Fetch releases from a repository."""
        params = {"per_page": min(limit, 100)}
        url = f"https://api.github.com/repos/{owner}/{repo}/releases"
        data = self._make_request(url, params)
        
        return data if data else []
    
    def extract_intervention_from_pr(
        self,
        owner: str,
        repo: str,
        pr_data: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        """
        Extract intervention data from a merged PR.
        
        Args:
            owner: Repository owner
            repo: Repository name
            pr_data: PR data from GitHub API
            
        Returns:
            Intervention data dict or None
        """
        pr_number = pr_data.get("number")
        merged_at = pr_data.get("merged_at")
        
        if not merged_at:
            return None
        
        # Fetch PR details and files
        pr_details = self.fetch_pr_details(owner, repo, pr_number)
        files_changed = self.fetch_pr_files(owner, repo, pr_number)
        
        # Classify intervention type
        title = pr_data.get("title", "")
        body = pr_details.get("body", "") if pr_details else ""
        intervention_type = self.classifier.classify(title, body, files_changed)
        
        # Fetch metrics before and after (estimate)
        # In practice, we'd need historical metrics, but for now we estimate
        current_metrics = self.fetch_repo_metrics(owner, repo)
        
        # Estimate before state (subtract some growth)
        # This is a rough estimate - real implementation would use historical data
        before_stars = max(current_metrics["stars"] - 10, 0)
        before_forks = max(current_metrics["forks"] - 2, 0)
        before_contributors = max(current_metrics["contributors"] - 1, 0)
        
        before_state = {
            "stars": before_stars,
            "forks": before_forks,
            "contributors": before_contributors,
            "language": current_metrics["language"],
            "category": self._infer_category(files_changed, current_metrics["language"])
        }
        
        after_state = {
            "stars": current_metrics["stars"],
            "forks": current_metrics["forks"],
            "contributors": current_metrics["contributors"]
        }
        
        return {
            "asset_id": f"{owner}/{repo}",
            "asset_type": "github_repo",
            "asset_name": repo,
            "developer_id": f"github:{pr_data.get('user', {}).get('login', 'unknown')}",
            "developer_username": pr_data.get("user", {}).get("login", "unknown"),
            "before_state": before_state,
            "intervention_type": intervention_type,
            "intervention_description": title,
            "planned_effort_days": self._estimate_effort_days(files_changed, body),
            "predicted_value": self._estimate_value(intervention_type, files_changed),
            "predicted_probability": 0.5,  # Default, would be refined
            "predicted_risk": 0.5,  # Default, would be refined
            "start_date": pr_data.get("created_at", merged_at),
            "end_date": merged_at,
            "after_state": after_state,
            "outcome_metrics": {
                "actual_value": self._calculate_actual_value(before_state, after_state),
                "success": self._determine_success(before_state, after_state),
                "actual_risk": 0.5
            },
            "verification_link": pr_data.get("html_url", ""),
            "pr_number": pr_number,
            "files_changed": files_changed,
            "additions": pr_data.get("additions", 0),
            "deletions": pr_data.get("deletions", 0)
        }
    
    def _infer_category(self, files_changed: List[str], language: str) -> str:
        """Infer project category from files changed and language."""
        if not files_changed:
            return "unknown"
        
        files_text = " ".join(files_changed).lower()
        
        if any(x in files_text for x in ["test", "spec", ".test.", "cypress", "jest"]):
            return "testing"
        if any(x in files_text for x in ["docker", "k8s", "kubernetes", "helm"]):
            return "infrastructure"
        if any(x in files_text for x in ["readme", "doc", "md"]):
            return "documentation"
        if any(x in files_text for x in ["package.json", "setup.py", "cargo.toml", "requirements"]):
            return "tooling"
        
        # Default to language-based category
        if language in ["javascript", "typescript", "python", "go", "rust"]:
            return "framework"
        
        return "unknown"
    
    def _estimate_effort_days(self, files_changed: List[str], body: str) -> int:
        """Estimate effort in days based on PR size."""
        if not files_changed:
            return 1
        
        # Simple heuristic based on number of files
        num_files = len(files_changed)
        
        if num_files <= 2:
            return 1
        elif num_files <= 5:
            return 3
        elif num_files <= 10:
            return 7
        elif num_files <= 20:
            return 14
        else:
            return 30
    
    def _estimate_value(self, intervention_type: str, files_changed: List[str]) -> float:
        """Estimate value based on intervention type and scope."""
        # Base values by type
        base_values = {
            "documentation": 30,
            "build_system": 40,
            "feature_expansion": 50,
            "performance": 60,
            "migration": 55,
            "packaging": 45,
            "api": 55,
            "saas": 70,
            "ai_integration": 65,
            "security": 50,
            "dependency_cleanup": 25
        }
        
        base = base_values.get(intervention_type, 40)
        
        # Adjust by scope (number of files)
        if files_changed:
            scope_multiplier = min(len(files_changed) / 10, 2.0)
            return base * (0.5 + scope_multiplier / 2)
        
        return base
    
    def _calculate_actual_value(self, before_state: Dict, after_state: Dict) -> float:
        """Calculate actual value based on metric changes."""
        star_growth = (after_state["stars"] - before_state["stars"]) / max(before_state["stars"], 1)
        contributor_growth = (after_state["contributors"] - before_state["contributors"]) / max(before_state["contributors"], 1)
        
        # Combined growth score
        value = (star_growth * 50) + (contributor_growth * 50)
        return max(0, min(100, value))
    
    def _determine_success(self, before_state: Dict, after_state: Dict) -> bool:
        """Determine if intervention was successful."""
        star_growth = after_state["stars"] > before_state["stars"]
        contributor_growth = after_state["contributors"] > before_state["contributors"]
        
        # Success if either metric grew
        return star_growth or contributor_growth
    
    def mine_repository(
        self,
        owner: str,
        repo: str,
        limit: int = 50,
        since: str = None
    ) -> List[Dict[str, Any]]:
        """
        Mine a repository for interventions.
        
        Args:
            owner: Repository owner
            repo: Repository name
            limit: Maximum number of interventions to extract
            since: ISO date string to mine since
            
        Returns:
            List of intervention data
        """
        print(f"Mining {owner}/{repo}...")
        
        # Fetch merged PRs
        merged_prs = self.fetch_merged_prs(owner, repo, limit, since)
        
        interventions = []
        for pr_data in merged_prs:
            intervention = self.extract_intervention_from_pr(owner, repo, pr_data)
            if intervention:
                interventions.append(intervention)
                print(f"  ✓ Extracted: {intervention['intervention_type']} - {intervention['intervention_description'][:50]}...")
        
        print(f"  Found {len(interventions)} interventions")
        return interventions
    
    def mine_multiple_repos(
        self,
        repos: List[Tuple[str, str]],
        limit_per_repo: int = 20
    ) -> List[Dict[str, Any]]:
        """
        Mine multiple repositories for interventions.
        
        Args:
            repos: List of (owner, repo) tuples
            limit_per_repo: Maximum interventions per repo
            
        Returns:
            List of all intervention data
        """
        all_interventions = []
        
        for owner, repo in repos:
            try:
                interventions = self.mine_repository(owner, repo, limit_per_repo)
                all_interventions.extend(interventions)
            except Exception as e:
                print(f"Error mining {owner}/{repo}: {e}")
        
        return all_interventions


def seed_mined_interventions(
    interventions: List[Dict[str, Any]],
    ledger: OutcomeLedger,
    elo_system: InnovationElo,
    transformation_tracker: TransformationTracker
) -> int:
    """
    Seed mined interventions into the Outcome Ledger.
    
    Args:
        interventions: List of intervention data from miner
        ledger: OutcomeLedger instance
        elo_system: InnovationElo instance
        transformation_tracker: TransformationTracker instance
        
    Returns:
        Number of interventions seeded
    """
    seeded_count = 0
    
    for i, intervention in enumerate(interventions):
        print(f"Seeding {i+1}/{len(interventions)}: {intervention['asset_name']} ({intervention['intervention_type']})")
        
        # Calculate predicted outcome
        star_growth = (intervention['after_state']['stars'] - intervention['before_state']['stars']) / max(intervention['before_state']['stars'], 1)
        contributor_growth = (intervention['after_state']['contributors'] - intervention['before_state']['contributors']) / max(intervention['before_state']['contributors'], 1)
        
        predicted_outcome = {
            "star_growth": star_growth,
            "contributor_growth": contributor_growth
        }
        
        try:
            # Create intervention record
            record_id = ledger.create_intervention(
                asset_id=intervention["asset_id"],
                asset_type=intervention["asset_type"],
                asset_name=intervention["asset_name"],
                developer_id=intervention["developer_id"],
                developer_username=intervention["developer_username"],
                before_state=intervention["before_state"],
                intervention_type=intervention["intervention_type"],
                intervention_description=intervention["intervention_description"],
                planned_effort_days=intervention["planned_effort_days"],
                predicted_value=intervention["predicted_value"],
                predicted_probability=intervention["predicted_probability"],
                predicted_risk=intervention["predicted_risk"],
                predicted_outcome=predicted_outcome
            )
            
            # Start intervention
            ledger.start_intervention(record_id=record_id)
            
            # Complete intervention
            ledger.complete_intervention(
                record_id=record_id,
                after_state=intervention["after_state"],
                outcome_metrics=intervention["outcome_metrics"]
            )
            
            # Verify outcome
            ledger.verify_outcome(
                record_id=record_id,
                verifier_id="github_miner",
                verifier_username="github_miner",
                status=VerificationStatus.VERIFIED.value,
                notes=f"Auto-verified from GitHub PR: {intervention.get('verification_link', '')}"
            )
            
            # Update Elo system
            elo_system.update_from_intervention(
                developer_id=intervention["developer_id"],
                intervention_type=intervention["intervention_type"],
                predicted_value=intervention["predicted_value"],
                actual_value=intervention["outcome_metrics"]["actual_value"]
            )
            
            # Record transformation pattern
            transformation_tracker.record_transformation(
                asset_id=intervention["asset_id"],
                asset_type=intervention["asset_type"],
                intervention_type=intervention["intervention_type"],
                context=intervention["before_state"],
                before_metrics=intervention["before_state"],
                after_metrics=intervention["after_state"]
            )
            
            seeded_count += 1
            print(f"  ✓ Seeded: {record_id}")
            
        except Exception as e:
            print(f"  ✗ Error seeding: {e}")
    
    return seeded_count


if __name__ == "__main__":
    # Example usage
    import os
    import sys
    
    # Get GitHub token from command line argument or environment
    if len(sys.argv) > 1:
        github_token = sys.argv[1]
    else:
        github_token = os.environ.get("GITHUB_TOKEN")
    
    if not github_token:
        print("Error: GITHUB_TOKEN not provided.")
        print("Usage: python3 github_intervention_miner.py <github_token>")
        print("Or: GITHUB_TOKEN=your_token python3 github_intervention_miner.py")
        sys.exit(1)
    
    # Initialize miner
    miner = GitHubInterventionMiner(github_token)
    
    # Initialize ledger and systems
    ledger = OutcomeLedger("outcome_ledger.db")
    elo_system = InnovationElo()
    transformation_tracker = TransformationTracker()
    
    # Repositories to mine (high-activity open source projects)
    repos_to_mine = [
        ("vercel", "next.js"),
        ("facebook", "react"),
        ("vuejs", "vue"),
        ("sveltejs", "svelte"),
        ("microsoft", "typescript"),
        ("golang", "go"),
        ("rust-lang", "rust"),
        ("docker", "docker"),
        ("kubernetes", "kubernetes"),
        ("tensorflow", "tensorflow"),
        ("pytorch", "pytorch"),
        ("openai", "openai-python"),
        ("langchain-ai", "langchain"),
        ("supabase", "supabase"),
        ("prisma", "prisma")
    ]
    
    # Mine interventions
    print("Starting GitHub intervention mining...")
    interventions = miner.mine_multiple_repos(repos_to_mine, limit_per_repo=20)
    
    print(f"\nTotal interventions extracted: {len(interventions)}")
    
    # Seed into ledger
    if interventions:
        print("\nSeeding interventions into Outcome Ledger...")
        seeded = seed_mined_interventions(interventions, ledger, elo_system, transformation_tracker)
        
        # Save Elo ratings and patterns
        elo_system.save_to_file("elo_ratings.json")
        transformation_tracker.export_patterns("transformation_patterns.json")
        
        print(f"\n✓ Seeded {seeded} interventions")
        print("✓ Elo ratings saved to elo_ratings.json")
        print("✓ Transformation patterns saved to transformation_patterns.json")
    else:
        print("No interventions to seed.")
