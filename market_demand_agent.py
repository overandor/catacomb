"""Market Demand Agent - Category growth, jobs, funding, package trends, developer discussion."""
from typing import Dict, Any
import requests
from datetime import datetime, timedelta
from base_agent import BaseAgent, AgentOutput


class MarketDemandAgent(BaseAgent):
    """Deterministically assesses market demand without LLMs."""
    
    def __init__(self, github_token: str = None):
        super().__init__("MarketDemand")
        self.github_token = github_token
        self.headers = {"Accept": "application/vnd.github.v3+json"}
        if self.github_token:
            self.headers["Authorization"] = f"token {self.github_token}"
    
    def _assess_category_growth(self, repo_data: Dict[str, Any]) -> Dict[str, Any]:
        """Assess category growth based on language/topic popularity."""
        evidence = {}
        
        language = repo_data.get("language")
        topics = repo_data.get("topics", [])
        stars = repo_data.get("stars", 0)
        forks = repo_data.get("forks", 0)
        
        evidence["language"] = language
        evidence["topics"] = topics
        evidence["stars"] = stars
        evidence["forks"] = forks
        
        # High-growth languages (2024-2026 trends)
        high_growth_languages = [
            "Rust", "Go", "TypeScript", "Python", "Kotlin", "Swift",
            "Dart", "Zig", "Julia", "Elixir"
        ]
        
        # Stable/mature languages
        stable_languages = [
            "Java", "C++", "C#", "JavaScript", "Ruby", "PHP"
        ]
        
        # Declining languages
        declining_languages = [
            "Objective-C", "Perl", "CoffeeScript", "ActionScript"
        ]
        
        growth_score = 50  # Base
        
        if language in high_growth_languages:
            growth_score += 30
        elif language in stable_languages:
            growth_score += 10
        elif language in declining_languages:
            growth_score -= 20
        
        # High-growth topics
        high_growth_topics = [
            "ai", "machine-learning", "llm", "blockchain", "web3",
            "rust", "kubernetes", "microservices", "serverless",
            "graphql", "react", "vue", "svelte", "tensorflow",
            "pytorch", "cybersecurity", "devops", "observability"
        ]
        
        topic_growth = sum(1 for t in topics if t and t.lower() in high_growth_topics)
        growth_score += topic_growth * 5
        
        # Star/fork ratio indicates organic growth
        if stars > 0 and forks > 0:
            fork_star_ratio = forks / stars
            if fork_star_ratio > 0.5:  # High engagement
                growth_score += 10
            elif fork_star_ratio > 0.3:
                growth_score += 5
        
        growth_score = max(0, min(growth_score, 100))
        evidence["category_growth_score"] = growth_score
        
        return {
            "score": growth_score,
            "evidence": evidence
        }
    
    def _assess_job_signals(self, repo_data: Dict[str, Any]) -> Dict[str, Any]:
        """Assess job demand based on language and topic popularity (proxy)."""
        evidence = {}
        
        language = repo_data.get("language")
        topics = repo_data.get("topics", [])
        
        evidence["language"] = language
        evidence["topics"] = topics
        
        # High job demand languages (based on 2024-2025 market data)
        high_demand_languages = {
            "Python": 95,
            "JavaScript": 90,
            "Java": 85,
            "TypeScript": 85,
            "Go": 80,
            "Rust": 75,
            "C++": 75,
            "C#": 70,
            "Kotlin": 65,
            "Swift": 60
        }
        
        # High job demand topics
        high_demand_topics = [
            "machine-learning", "ai", "data-science", "cloud",
            "kubernetes", "docker", "devops", "security",
            "blockchain", "web3", "mobile", "react", "node"
        ]
        
        job_score = high_demand_languages.get(language, 50)
        
        # Boost for high-demand topics
        topic_boost = sum(1 for t in topics if t and t.lower() in high_demand_topics)
        job_score += topic_boost * 3
        
        job_score = min(job_score, 100)
        evidence["job_demand_score"] = job_score
        
        return {
            "score": job_score,
            "evidence": evidence
        }
    
    def _assess_funding_signals(self, repo_data: Dict[str, Any]) -> Dict[str, Any]:
        """Assess funding interest based on category (proxy)."""
        evidence = {}
        
        topics = repo_data.get("topics", [])
        language = repo_data.get("language")
        
        evidence["topics"] = topics
        evidence["language"] = language
        
        # High-funding categories
        high_funding_categories = [
            "ai", "machine-learning", "llm", "blockchain", "web3",
            "fintech", "healthtech", "cleantech", "security",
            "infrastructure", "developer-tools", "database"
        ]
        
        funding_score = 30  # Base
        
        # Boost for high-funding topics
        funding_boost = sum(1 for t in topics if t and t.lower() in high_funding_categories)
        funding_score += funding_boost * 15
        
        # Infrastructure languages get funding
        if language in ["Rust", "Go", "C++"]:
            funding_score += 10
        
        funding_score = min(funding_score, 100)
        evidence["funding_signal_score"] = funding_score
        
        return {
            "score": funding_score,
            "evidence": evidence
        }
    
    def _assess_package_trends(self, repo_data: Dict[str, Any]) -> Dict[str, Any]:
        """Assess package ecosystem growth (proxy via language popularity)."""
        evidence = {}
        
        language = repo_data.get("language")
        has_package = any([
            repo_data.get("has_package_json", False),
            repo_data.get("has_requirements_txt", False),
            repo_data.get("has_setup_py", False),
            repo_data.get("has_pyproject_toml", False),
            repo_data.get("has_cargo_toml", False),
            repo_data.get("has_go_mod", False)
        ])
        
        evidence["language"] = language
        evidence["has_package_manager"] = has_package
        
        # Package ecosystem health by language
        ecosystem_health = {
            "JavaScript": 95,  # npm
            "TypeScript": 95,  # npm
            "Python": 90,  # PyPI
            "Rust": 85,  # crates.io
            "Go": 85,  # Go modules
            "Ruby": 80,  # RubyGems
            "Java": 75,  # Maven
            "PHP": 75,  # Composer
            "C#": 70,  # NuGet
            "C++": 50   # Fragmented
        }
        
        package_score = ecosystem_health.get(language, 50)
        
        # Boost if has package manager
        if has_package:
            package_score += 10
        
        package_score = min(package_score, 100)
        evidence["package_trend_score"] = package_score
        
        return {
            "score": package_score,
            "evidence": evidence
        }
    
    def _assess_developer_discussion(self, repo_data: Dict[str, Any]) -> Dict[str, Any]:
        """Assess developer discussion via GitHub activity signals."""
        evidence = {}
        
        stars = repo_data.get("stars", 0)
        forks = repo_data.get("forks", 0)
        open_issues = repo_data.get("open_issues", 0)
        commits_last_year = repo_data.get("commits_last_year", 0)
        contributors = repo_data.get("contributors", 0)
        
        evidence["stars"] = stars
        evidence["forks"] = forks
        evidence["open_issues"] = open_issues
        evidence["commits_last_year"] = commits_last_year
        evidence["contributors"] = contributors
        
        discussion_score = 0
        
        # Stars indicate visibility
        if stars > 1000:
            discussion_score += 25
        elif stars > 100:
            discussion_score += 15
        elif stars > 10:
            discussion_score += 5
        
        # Forks indicate active use
        if forks > 100:
            discussion_score += 25
        elif forks > 10:
            discussion_score += 15
        elif forks > 1:
            discussion_score += 5
        
        # Issues indicate discussion
        if open_issues > 50:
            discussion_score += 20
        elif open_issues > 10:
            discussion_score += 10
        elif open_issues > 0:
            discussion_score += 5
        
        # Recent commits indicate active discussion
        if commits_last_year > 50:
            discussion_score += 20
        elif commits_last_year > 10:
            discussion_score += 10
        elif commits_last_year > 0:
            discussion_score += 5
        
        # Contributors indicate community
        if contributors > 10:
            discussion_score += 10
        elif contributors > 3:
            discussion_score += 5
        
        discussion_score = min(discussion_score, 100)
        evidence["developer_discussion_score"] = discussion_score
        
        return {
            "score": discussion_score,
            "evidence": evidence
        }
    
    def analyze(self, repo_data: Dict[str, Any]) -> AgentOutput:
        """
        Analyze market demand across multiple dimensions.
        """
        evidence = {}
        
        # Assess all dimensions
        category_growth = self._assess_category_growth(repo_data)
        job_signals = self._assess_job_signals(repo_data)
        funding_signals = self._assess_funding_signals(repo_data)
        package_trends = self._assess_package_trends(repo_data)
        developer_discussion = self._assess_developer_discussion(repo_data)
        
        # Store evidence
        evidence["category_growth"] = category_growth["evidence"]
        evidence["job_signals"] = job_signals["evidence"]
        evidence["funding_signals"] = funding_signals["evidence"]
        evidence["package_trends"] = package_trends["evidence"]
        evidence["developer_discussion"] = developer_discussion["evidence"]
        
        # Calculate overall market demand score
        # Weighted combination
        demand_score = (
            0.25 * category_growth["score"] +
            0.20 * job_signals["score"] +
            0.15 * funding_signals["score"] +
            0.20 * package_trends["score"] +
            0.20 * developer_discussion["score"]
        )
        
        evidence["overall_market_demand"] = demand_score
        
        # Confidence based on data availability
        has_language = bool(repo_data.get("language"))
        has_topics = bool(repo_data.get("topics"))
        has_activity = repo_data.get("stars", 0) > 0 or repo_data.get("forks", 0) > 0
        
        confidence = 0.5
        if has_language:
            confidence += 0.2
        if has_topics:
            confidence += 0.2
        if has_activity:
            confidence += 0.1
        
        return AgentOutput(
            score=round(demand_score, 2),
            evidence=evidence,
            confidence=confidence,
            hash=""
        )
