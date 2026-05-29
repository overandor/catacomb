"""Abandoned Promising Repo KPIs - 20 additional metrics for detecting high-potential abandoned repos."""
import numpy as np
from typing import Dict, Any, List
from datetime import datetime, timedelta


class AbandonedRepoKPIs:
    """20 KPIs for measuring abandoned promising repositories."""
    
    def __init__(self):
        self.kpi_weights = {
            # Abandonment indicators (5 KPIs)
            "last_commit_age_months": 0.15,
            "activity_gap_score": 0.12,
            "issue_staleness": 0.10,
            "pr_response_time": 0.08,
            "release_staleness": 0.10,
            
            # Technical debt (4 KPIs)
            "dependency_freshness": 0.08,
            "code_age_score": 0.07,
            "test_coverage_ratio": 0.06,
            "documentation_completeness": 0.05,
            
            # Ecosystem metrics (4 KPIs)
            "downstream_usage": 0.10,
            "dependency_centrality": 0.08,
            "fork_activity": 0.07,
            "contributor_retention": 0.06,
            
            # Maintainer availability (3 KPIs)
            "maintainer_engagement": 0.08,
            "issue_resolution_rate": 0.07,
            "community_health": 0.06,
            
            # Market signals (4 KPIs)
            "star_velocity": 0.09,
            "fork_velocity": 0.07,
            "watch_velocity": 0.06,
            "language_trend": 0.05
        }
    
    def calculate_innovation_alpha(
        self,
        repo_data: Dict[str, Any],
        analysis: Dict[str, Any] = None,
        valuation: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """
        Calculate Innovation Alpha = Expected Future Value - Current Recognition.
        
        This identifies undervalued assets with high potential.
        """
        kpis = self.calculate_all_kpis(repo_data, analysis)
        
        # Current Recognition (inverse of popularity)
        stars = repo_data.get("stars", 0)
        forks = repo_data.get("forks", 0)
        contributors = repo_data.get("contributors", 0)
        
        # Normalize recognition (0-1, where 1 = most recognized)
        recognition_score = min(1.0, (stars + forks * 2 + contributors * 5) / 10000)
        
        # Expected Future Value (based on KPIs)
        kpi_breakdown = self.get_kpi_breakdown(kpis)
        ecosystem_value = kpi_breakdown["ecosystem_metrics"]["score"]
        market_potential = kpi_breakdown["market_signals"]["score"]
        technical_quality = kpi_breakdown["technical_debt"]["score"]
        
        expected_future_value = (
            ecosystem_value * 0.4 +
            market_potential * 0.35 +
            technical_quality * 0.25
        )
        
        # Innovation Alpha = Expected Future Value - Current Recognition
        # Higher alpha = more undervalued
        innovation_alpha = expected_future_value - recognition_score
        
        # Ensure alpha is in reasonable range
        innovation_alpha = max(-1.0, min(1.0, innovation_alpha))
        
        return {
            "innovation_alpha": innovation_alpha,
            "expected_future_value": expected_future_value,
            "current_recognition": recognition_score,
            "kpis": kpis,
            "kpi_breakdown": kpi_breakdown
        }
    
    def calculate_all_kpis(self, repo_data: Dict[str, Any], analysis: Dict[str, Any] = None) -> Dict[str, Any]:
        """Calculate all 20 KPIs for a repository."""
        kpis = {}
        
        # Abandonment indicators
        kpis["last_commit_age_months"] = self._last_commit_age_months(repo_data)
        kpis["activity_gap_score"] = self._activity_gap_score(repo_data)
        kpis["issue_staleness"] = self._issue_staleness(repo_data)
        kpis["pr_response_time"] = self._pr_response_time(repo_data)
        kpis["release_staleness"] = self._release_staleness(repo_data)
        
        # Technical debt
        kpis["dependency_freshness"] = self._dependency_freshness(repo_data)
        kpis["code_age_score"] = self._code_age_score(repo_data)
        kpis["test_coverage_ratio"] = self._test_coverage_ratio(repo_data)
        kpis["documentation_completeness"] = self._documentation_completeness(repo_data)
        
        # Ecosystem metrics
        kpis["downstream_usage"] = self._downstream_usage(repo_data)
        kpis["dependency_centrality"] = self._dependency_centrality(repo_data)
        kpis["fork_activity"] = self._fork_activity(repo_data)
        kpis["contributor_retention"] = self._contributor_retention(repo_data)
        
        # Maintainer availability
        kpis["maintainer_engagement"] = self._maintainer_engagement(repo_data)
        kpis["issue_resolution_rate"] = self._issue_resolution_rate(repo_data)
        kpis["community_health"] = self._community_health(repo_data)
        
        # Market signals
        kpis["star_velocity"] = self._star_velocity(repo_data)
        kpis["fork_velocity"] = self._fork_velocity(repo_data)
        kpis["watch_velocity"] = self._watch_velocity(repo_data)
        kpis["language_trend"] = self._language_trend(repo_data)
        
        # Calculate overall abandoned promising score
        kpis["abandoned_promising_score"] = self._calculate_overall_score(kpis)
        
        return kpis
    
    def _last_commit_age_months(self, repo_data: Dict[str, Any]) -> float:
        """KPI 1: Months since last commit (higher = more abandoned)."""
        pushed_at = repo_data.get("pushed_at")
        if not pushed_at:
            return 36.0  # Default to 3 years if unknown
        
        try:
            last_commit = datetime.fromisoformat(pushed_at.replace('Z', '+00:00'))
            age_months = (datetime.utcnow() - last_commit).days / 30
            return min(36.0, age_months)  # Cap at 3 years
        except:
            return 36.0
    
    def _activity_gap_score(self, repo_data: Dict[str, Any]) -> float:
        """KPI 2: Gap between expected and actual activity (higher = more abandoned)."""
        commits_last_year = repo_data.get("commits_last_year", 0)
        stars = repo_data.get("stars", 0)
        
        # Expected commits based on star count
        expected_commits = min(100, stars * 0.5)
        
        if expected_commits == 0:
            return 0.0
        
        gap = (expected_commits - commits_last_year) / expected_commits
        return max(0.0, min(1.0, gap))
    
    def _issue_staleness(self, repo_data: Dict[str, Any]) -> float:
        """KPI 3: Average age of open issues (higher = more abandoned)."""
        open_issues = repo_data.get("open_issues", 0)
        
        if open_issues == 0:
            return 0.0
        
        # Estimate staleness based on commit activity
        commits_last_year = repo_data.get("commits_last_year", 0)
        
        if commits_last_year > 50:
            return 0.1  # Active
        elif commits_last_year > 10:
            return 0.5  # Moderate
        else:
            return 0.9  # Stale
    
    def _pr_response_time(self, repo_data: Dict[str, Any]) -> float:
        """KPI 4: Estimated PR response time (higher = more abandoned)."""
        # Estimate based on commit activity
        commits_last_year = repo_data.get("commits_last_year", 0)
        
        if commits_last_year > 100:
            return 0.1  # Fast response
        elif commits_last_year > 50:
            return 0.3  # Moderate
        elif commits_last_year > 10:
            return 0.6  # Slow
        else:
            return 0.9  # Very slow
    
    def _release_staleness(self, repo_data: Dict[str, Any]) -> float:
        """KPI 5: Months since last release (higher = more abandoned)."""
        # Estimate based on commit activity and stars
        commits_last_year = repo_data.get("commits_last_year", 0)
        stars = repo_data.get("stars", 0)
        
        if stars > 1000 and commits_last_year < 10:
            return 0.9  # Popular but inactive
        elif commits_last_year > 50:
            return 0.1  # Active
        elif commits_last_year > 10:
            return 0.4  # Moderate
        else:
            return 0.8  # Inactive
    
    def _dependency_freshness(self, repo_data: Dict[str, Any]) -> float:
        """KPI 6: Freshness of dependencies (lower = more outdated)."""
        # Estimate based on language and age
        language = repo_data.get("language", "").lower()
        last_commit_age = self._last_commit_age_months(repo_data)
        
        # Some languages have more stable dependencies
        stable_languages = ["go", "rust", "java"]
        
        if language in stable_languages:
            return max(0.0, 1.0 - (last_commit_age / 48))  # More lenient
        else:
            return max(0.0, 1.0 - (last_commit_age / 24))  # Stricter
    
    def _code_age_score(self, repo_data: Dict[str, Any]) -> float:
        """KPI 7: Age of codebase (higher = older, potentially more stable)."""
        created_at = repo_data.get("created_at")
        if not created_at:
            return 0.5
        
        try:
            created = datetime.fromisoformat(created_at.replace('Z', '+00:00'))
            age_years = (datetime.utcnow() - created).days / 365
            return min(1.0, age_years / 10)  # Normalize to 0-1 (10 years = 1.0)
        except:
            return 0.5
    
    def _test_coverage_ratio(self, repo_data: Dict[str, Any]) -> float:
        """KPI 8: Test coverage (higher = better quality)."""
        has_tests = repo_data.get("has_tests", False)
        has_ci = repo_data.get("has_ci", False)
        
        if has_tests and has_ci:
            return 0.9
        elif has_tests:
            return 0.6
        elif has_ci:
            return 0.4
        else:
            return 0.1
    
    def _documentation_completeness(self, repo_data: Dict[str, Any]) -> float:
        """KPI 9: Documentation completeness (higher = better)."""
        has_readme = repo_data.get("has_readme", False)
        stars = repo_data.get("stars", 0)
        
        if has_readme and stars > 100:
            return 0.9
        elif has_readme:
            return 0.6
        else:
            return 0.1
    
    def _downstream_usage(self, repo_data: Dict[str, Any]) -> float:
        """KPI 10: Number of downstream dependents (higher = more valuable)."""
        forks = repo_data.get("forks", 0)
        stars = repo_data.get("stars", 0)
        
        # Estimate downstream usage from fork ratio
        fork_ratio = forks / (stars + 1)
        
        if fork_ratio > 0.5:
            return 0.9
        elif fork_ratio > 0.3:
            return 0.6
        elif fork_ratio > 0.1:
            return 0.3
        else:
            return 0.1
    
    def _dependency_centrality(self, repo_data: Dict[str, Any]) -> float:
        """KPI 11: Centrality in dependency graph (higher = more critical)."""
        stars = repo_data.get("stars", 0)
        forks = repo_data.get("forks", 0)
        
        # Estimate centrality from popularity
        if stars > 10000:
            return 0.9
        elif stars > 1000:
            return 0.7
        elif stars > 100:
            return 0.5
        elif stars > 10:
            return 0.3
        else:
            return 0.1
    
    def _fork_activity(self, repo_data: Dict[str, Any]) -> float:
        """KPI 12: Recent fork activity (higher = more interest)."""
        forks = repo_data.get("forks", 0)
        commits_last_year = repo_data.get("commits_last_year", 0)
        
        if forks > 100 and commits_last_year > 50:
            return 0.9
        elif forks > 50 and commits_last_year > 20:
            return 0.6
        elif forks > 10:
            return 0.3
        else:
            return 0.1
    
    def _contributor_retention(self, repo_data: Dict[str, Any]) -> float:
        """KPI 13: Contributor retention rate (higher = healthier)."""
        contributors = repo_data.get("contributors", 0)
        commits_last_year = repo_data.get("commits_last_year", 0)
        
        if contributors > 10 and commits_last_year > 100:
            return 0.9
        elif contributors > 5 and commits_last_year > 50:
            return 0.6
        elif contributors > 1:
            return 0.4
        else:
            return 0.1
    
    def _maintainer_engagement(self, repo_data: Dict[str, Any]) -> float:
        """KPI 14: Maintainer engagement level (higher = more active)."""
        commits_last_year = repo_data.get("commits_last_year", 0)
        open_issues = repo_data.get("open_issues", 0)
        
        if commits_last_year > 100:
            return 0.9
        elif commits_last_year > 50:
            return 0.6
        elif commits_last_year > 10:
            return 0.3
        else:
            return 0.1
    
    def _issue_resolution_rate(self, repo_data: Dict[str, Any]) -> float:
        """KPI 15: Issue resolution rate (higher = better)."""
        open_issues = repo_data.get("open_issues", 0)
        commits_last_year = repo_data.get("commits_last_year", 0)
        
        if open_issues > 0:
            resolution_rate = commits_last_year / (open_issues * 2)
            return min(1.0, resolution_rate)
        else:
            return 0.5  # Neutral if no issues
    
    def _community_health(self, repo_data: Dict[str, Any]) -> float:
        """KPI 16: Overall community health (higher = healthier)."""
        contributors = repo_data.get("contributors", 0)
        forks = repo_data.get("forks", 0)
        stars = repo_data.get("stars", 0)
        
        # Health score based on engagement
        engagement = (contributors + forks) / (stars + 1)
        
        if engagement > 0.5:
            return 0.9
        elif engagement > 0.3:
            return 0.6
        elif engagement > 0.1:
            return 0.4
        else:
            return 0.2
    
    def _star_velocity(self, repo_data: Dict[str, Any]) -> float:
        """KPI 17: Star growth velocity (higher = more momentum)."""
        commits_last_year = repo_data.get("commits_last_year", 0)
        stars = repo_data.get("stars", 0)
        
        if stars == 0:
            return 0.0
        
        # Estimate velocity from recent activity
        velocity = commits_last_year / stars
        
        if velocity > 0.5:
            return 0.9
        elif velocity > 0.2:
            return 0.6
        elif velocity > 0.1:
            return 0.3
        else:
            return 0.1
    
    def _fork_velocity(self, repo_data: Dict[str, Any]) -> float:
        """KPI 18: Fork growth velocity (higher = more momentum)."""
        forks = repo_data.get("forks", 0)
        stars = repo_data.get("stars", 0)
        commits_last_year = repo_data.get("commits_last_year", 0)
        
        if stars == 0:
            return 0.0
        
        fork_ratio = forks / stars
        activity = commits_last_year / 100
        
        velocity = fork_ratio * activity
        
        if velocity > 0.3:
            return 0.9
        elif velocity > 0.1:
            return 0.6
        elif velocity > 0.05:
            return 0.3
        else:
            return 0.1
    
    def _watch_velocity(self, repo_data: Dict[str, Any]) -> float:
        """KPI 19: Watcher growth velocity (estimated from stars)."""
        stars = repo_data.get("stars", 0)
        commits_last_year = repo_data.get("commits_last_year", 0)
        
        if stars == 0:
            return 0.0
        
        # Estimate watchers as 10% of stars
        watchers = stars * 0.1
        velocity = commits_last_year / (watchers + 1)
        
        if velocity > 1.0:
            return 0.9
        elif velocity > 0.5:
            return 0.6
        elif velocity > 0.2:
            return 0.3
        else:
            return 0.1
    
    def _language_trend(self, repo_data: Dict[str, Any]) -> float:
        """KPI 20: Language trendiness (higher = more popular language)."""
        language = repo_data.get("language", "").lower()
        
        trending_languages = ["rust", "go", "typescript", "kotlin", "swift", "python"]
        stable_languages = ["java", "c++", "c#", "javascript", "ruby"]
        declining_languages = ["php", "perl", "objective-c"]
        
        if language in trending_languages:
            return 0.9
        elif language in stable_languages:
            return 0.6
        elif language in declining_languages:
            return 0.3
        else:
            return 0.5
    
    def _calculate_overall_score(self, kpis: Dict[str, float]) -> float:
        """Calculate overall abandoned promising score."""
        score = 0.0
        
        for kpi_name, kpi_value in kpis.items():
            if kpi_name in self.kpi_weights:
                weight = self.kpi_weights[kpi_name]
                score += kpi_value * weight
        
        return min(1.0, score)
    
    def get_kpi_breakdown(self, kpis: Dict[str, float]) -> Dict[str, Dict[str, Any]]:
        """Get detailed breakdown of KPIs by category."""
        breakdown = {
            "abandonment_indicators": {
                "kpis": ["last_commit_age_months", "activity_gap_score", "issue_staleness", "pr_response_time", "release_staleness"],
                "score": np.mean([kpis[k] for k in ["last_commit_age_months", "activity_gap_score", "issue_staleness", "pr_response_time", "release_staleness"]])
            },
            "technical_debt": {
                "kpis": ["dependency_freshness", "code_age_score", "test_coverage_ratio", "documentation_completeness"],
                "score": np.mean([kpis[k] for k in ["dependency_freshness", "code_age_score", "test_coverage_ratio", "documentation_completeness"]])
            },
            "ecosystem_metrics": {
                "kpis": ["downstream_usage", "dependency_centrality", "fork_activity", "contributor_retention"],
                "score": np.mean([kpis[k] for k in ["downstream_usage", "dependency_centrality", "fork_activity", "contributor_retention"]])
            },
            "maintainer_availability": {
                "kpis": ["maintainer_engagement", "issue_resolution_rate", "community_health"],
                "score": np.mean([kpis[k] for k in ["maintainer_engagement", "issue_resolution_rate", "community_health"]])
            },
            "market_signals": {
                "kpis": ["star_velocity", "fork_velocity", "watch_velocity", "language_trend"],
                "score": np.mean([kpis[k] for k in ["star_velocity", "fork_velocity", "watch_velocity", "language_trend"]])
            }
        }
        
        return breakdown
