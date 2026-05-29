"""Repo Valuation Model - Assign dollar value to software assets."""
import numpy as np
from typing import Dict, Any, Optional


class RepoValuation:
    """Valuation model for software repositories."""
    
    def __init__(self):
        # Valuation multipliers based on characteristics
        self.base_multiplier = 1000  # Base value in dollars per star-equivalent
    
    def calculate_valuation(
        self,
        repo_data: Dict[str, Any],
        analysis: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """
        Calculate dollar valuation for a repository.
        
        Args:
            repo_data: Repository data from GitHub API
            analysis: Optional analysis data from Catacomb engine
        
        Returns:
            Dict with valuation breakdown
        """
        # Extract key metrics
        stars = repo_data.get("stars", 0)
        forks = repo_data.get("forks", 0)
        contributors = repo_data.get("contributors", 0)
        commits_last_year = repo_data.get("commits_last_year", 0)
        open_issues = repo_data.get("open_issues", 0)
        language = repo_data.get("language", "Unknown")
        has_license = repo_data.get("license") is not None
        has_readme = repo_data.get("has_readme", False)
        has_ci = repo_data.get("has_ci", False)
        has_tests = repo_data.get("has_tests", False)
        
        # Base valuation from stars (with diminishing returns)
        base_value = self._star_valuation(stars)
        
        # Adjustments
        adjustments = {
            "fork_bonus": self._fork_bonus(forks, stars),
            "contributor_bonus": self._contributor_bonus(contributors),
            "activity_bonus": self._activity_bonus(commits_last_year),
            "engagement_bonus": self._engagement_bonus(open_issues, stars),
            "license_bonus": self._license_bonus(has_license),
            "quality_bonus": self._quality_bonus(has_readme, has_ci, has_tests),
            "language_multiplier": self._language_multiplier(language),
            "intervention_multiplier": self._intervention_multiplier(analysis) if analysis else 1.0
        }
        
        # Calculate total valuation
        total_value = base_value
        for bonus_name, bonus_value in adjustments.items():
            if "multiplier" in bonus_name:
                total_value *= bonus_value
            else:
                total_value += bonus_value
        
        # Ensure minimum valuation
        total_value = max(100, total_value)
        
        # Calculate confidence metrics (never 100%)
        confidence_metrics = self._calculate_confidence(repo_data, analysis)
        
        return {
            "total_value_usd": round(total_value),
            "base_value_usd": round(base_value),
            "adjustments": {k: round(v) if isinstance(v, (int, float)) else v for k, v in adjustments.items()},
            "confidence": confidence_metrics["overall_confidence"],
            "evidence_strength": confidence_metrics["evidence_strength"],
            "model_confidence": confidence_metrics["model_confidence"],
            "data_coverage": confidence_metrics["data_coverage"],
            "valuation_breakdown": {
                "star_value": round(base_value),
                "fork_value": round(adjustments["fork_bonus"]),
                "contributor_value": round(adjustments["contributor_bonus"]),
                "activity_value": round(adjustments["activity_bonus"]),
                "engagement_value": round(adjustments["engagement_bonus"]),
                "license_value": round(adjustments["license_bonus"]),
                "quality_value": round(adjustments["quality_bonus"]),
                "language_multiplier": adjustments["language_multiplier"],
                "intervention_multiplier": adjustments["intervention_multiplier"]
            }
        }
    
    def _star_valuation(self, stars: int) -> float:
        """Calculate base value from stars with diminishing returns."""
        if stars == 0:
            return 0
        
        # Logarithmic scaling with base multiplier
        # 1 star = $1,000
        # 10 stars = $10,000
        # 100 stars = $100,000
        # 1,000 stars = $1,000,000
        # 10,000 stars = $10,000,000
        
        return self.base_multiplier * (stars ** 0.7)
    
    def _fork_bonus(self, forks: int, stars: int) -> float:
        """Calculate bonus from fork activity."""
        if stars == 0:
            return 0
        
        fork_ratio = forks / stars
        # High fork ratio indicates active use
        if fork_ratio > 0.5:
            return stars * self.base_multiplier * 0.3
        elif fork_ratio > 0.3:
            return stars * self.base_multiplier * 0.15
        elif fork_ratio > 0.1:
            return stars * self.base_multiplier * 0.05
        return 0
    
    def _contributor_bonus(self, contributors: int) -> float:
        """Calculate bonus from contributor count."""
        # Each contributor adds value
        if contributors > 50:
            return contributors * self.base_multiplier * 0.5
        elif contributors > 20:
            return contributors * self.base_multiplier * 0.4
        elif contributors > 10:
            return contributors * self.base_multiplier * 0.3
        elif contributors > 5:
            return contributors * self.base_multiplier * 0.2
        elif contributors > 1:
            return contributors * self.base_multiplier * 0.1
        return 0
    
    def _activity_bonus(self, commits_last_year: int) -> float:
        """Calculate bonus from commit activity."""
        # Active development increases value
        if commits_last_year > 500:
            return 50000
        elif commits_last_year > 200:
            return 30000
        elif commits_last_year > 100:
            return 15000
        elif commits_last_year > 50:
            return 5000
        elif commits_last_year > 10:
            return 1000
        return 0
    
    def _engagement_bonus(self, open_issues: int, stars: int) -> float:
        """Calculate bonus from issue engagement."""
        if stars == 0:
            return 0
        
        # Issue engagement indicates active use
        issue_ratio = open_issues / stars
        if issue_ratio > 0.5 and open_issues > 10:
            return stars * self.base_multiplier * 0.1
        elif issue_ratio > 0.2 and open_issues > 5:
            return stars * self.base_multiplier * 0.05
        return 0
    
    def _license_bonus(self, has_license: bool) -> float:
        """Calculate bonus from having a license."""
        if has_license:
            return 5000
        return -2000  # Penalty for no license
    
    def _quality_bonus(self, has_readme: bool, has_ci: bool, has_tests: bool) -> float:
        """Calculate bonus from quality indicators."""
        bonus = 0
        if has_readme:
            bonus += 3000
        if has_ci:
            bonus += 5000
        if has_tests:
            bonus += 4000
        return bonus
    
    def _language_multiplier(self, language: str) -> float:
        """Calculate multiplier based on language market demand."""
        language = language.lower() if language else "unknown"
        
        high_demand = ["rust", "go", "typescript", "python", "kotlin", "swift"]
        medium_demand = ["javascript", "java", "c++", "c#", "ruby", "php"]
        low_demand = ["html", "css", "shell", "makefile", "unknown"]
        
        if language in high_demand:
            return 1.5
        elif language in medium_demand:
            return 1.2
        elif language in low_demand:
            return 0.8
        return 1.0
    
    def _intervention_multiplier(self, analysis: Dict[str, Any]) -> float:
        """Calculate multiplier based on intervention potential."""
        if not analysis:
            return 1.0
        
        intervention_score = analysis.get("intervention_score", 0) / 100
        
        # High intervention potential = higher valuation
        if intervention_score > 0.8:
            return 1.3
        elif intervention_score > 0.6:
            return 1.15
        elif intervention_score > 0.4:
            return 1.0
        else:
            return 0.9
    
    def _calculate_confidence(
        self,
        repo_data: Dict[str, Any],
        analysis: Dict[str, Any] = None
    ) -> Dict[str, float]:
        """Calculate confidence metrics (never 100%)."""
        # Evidence Strength: How much data do we have?
        evidence_strength = 50  # Base 50/100
        
        if repo_data.get("stars", 0) > 100:
            evidence_strength += 15
        if repo_data.get("contributors", 0) > 5:
            evidence_strength += 10
        if repo_data.get("commits_last_year", 0) > 50:
            evidence_strength += 10
        if repo_data.get("has_readme", False):
            evidence_strength += 5
        if repo_data.get("has_ci", False):
            evidence_strength += 5
        
        # Model Confidence: How confident is the model in its prediction?
        model_confidence = 60  # Base 60/100
        
        if analysis:
            intervention_score = analysis.get("intervention_score", 0)
            if intervention_score > 80:
                model_confidence += 15
            elif intervention_score > 50:
                model_confidence += 10
            elif intervention_score > 20:
                model_confidence += 5
        
        # Data Coverage: How complete is our data?
        data_coverage = 55  # Base 55/100
        
        required_fields = ["stars", "forks", "contributors", "language", "created_at"]
        missing_fields = sum(1 for field in required_fields if not repo_data.get(field))
        data_coverage -= missing_fields * 5
        
        # Cap at 95% - never 100%
        evidence_strength = min(95, evidence_strength)
        model_confidence = min(95, model_confidence)
        data_coverage = min(95, data_coverage)
        
        # Overall confidence (weighted average)
        overall_confidence = (
            evidence_strength * 0.4 +
            model_confidence * 0.35 +
            data_coverage * 0.25
        )
        
        return {
            "evidence_strength": evidence_strength,
            "model_confidence": model_confidence,
            "data_coverage": data_coverage,
            "overall_confidence": overall_confidence
        }
