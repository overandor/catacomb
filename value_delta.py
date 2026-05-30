"""Value Delta calculation: Achievable State - Current State."""

from typing import Dict, Any, List
import logging

logger = logging.getLogger(__name__)


class InterventionImpact:
    """Impact of specific interventions on repository value."""
    
    # Intervention types and their expected value multipliers
    INTERVENTION_MULTIPLIERS = {
        "documentation_improvement": 1.3,  # 30% value increase
        "packaging_completion": 1.5,  # 50% value increase
        "ci_addition": 1.4,  # 40% value increase
        "api_stabilization": 1.6,  # 60% value increase
        "dependency_modernization": 1.2,  # 20% value increase
        "test_coverage": 1.3,  # 30% value increase
        "security_fixes": 1.5,  # 50% value increase
        "performance_optimization": 1.4,  # 40% value increase
        "migration_to_newer_platform": 1.8,  # 80% value increase
        "ecosystem_integration": 2.0,  # 100% value increase
    }
    
    # Effort estimates in engineering days
    INTERVENTION_EFFORT_DAYS = {
        "documentation_improvement": 5,
        "packaging_completion": 10,
        "ci_addition": 7,
        "api_stabilization": 15,
        "dependency_modernization": 8,
        "test_coverage": 12,
        "security_fixes": 10,
        "performance_optimization": 20,
        "migration_to_newer_platform": 30,
        "ecosystem_integration": 25,
    }


class ValueDeltaCalculator:
    """Calculate Value Delta = Achievable State - Current State."""
    
    def __init__(self):
        self.impact = InterventionImpact()
    
    def calculate_current_state_value(self, repo_data: Dict[str, Any]) -> float:
        """
        Calculate current state value based on repository metrics.
        
        Factors:
        - Stars (recognition)
        - Forks (adoption)
        - Recent activity (vitality)
        - Technical quality (tests, CI, documentation)
        - Ecosystem leverage (dependents)
        """
        stars = repo_data.get("stars", 0)
        forks = repo_data.get("forks", 0)
        watchers = repo_data.get("watchers", 0)
        open_issues = repo_data.get("open_issues", 0)
        
        # Recognition score (log scale to avoid dominance by popular repos)
        recognition_score = self._log_scale(stars + 1) * 0.3
        
        # Adoption score
        adoption_score = self._log_scale(forks + 1) * 0.2
        
        # Vitality score (recent commits, open issues indicate activity)
        recent_commits = repo_data.get("recent_commits", 0)
        vitality_score = min(self._log_scale(recent_commits + 1), 5) * 0.15
        
        # Technical quality score
        has_tests = repo_data.get("has_tests", False)
        has_ci = repo_data.get("has_ci", False)
        has_readme = repo_data.get("has_readme", False)
        has_package = repo_data.get("has_package_file", False)
        
        quality_score = 0
        if has_tests: quality_score += 0.25
        if has_ci: quality_score += 0.25
        if has_readme: quality_score += 0.25
        if has_package: quality_score += 0.25
        quality_score *= 0.2
        
        # Ecosystem leverage score
        dependents = repo_data.get("dependents", 0)
        ecosystem_score = self._log_scale(dependents + 1) * 0.15
        
        current_value = recognition_score + adoption_score + vitality_score + quality_score + ecosystem_score
        
        return current_value
    
    def calculate_achievable_state_value(self, repo_data: Dict[str, Any], interventions: List[str]) -> float:
        """
        Calculate achievable state value after interventions.
        
        Each intervention has a multiplier effect on current value.
        """
        current_value = self.calculate_current_state_value(repo_data)
        
        # Apply intervention multipliers (cumulative)
        multiplier = 1.0
        for intervention in interventions:
            if intervention in self.impact.INTERVENTION_MULTIPLIERS:
                multiplier *= self.impact.INTERVENTION_MULTIPLIERS[intervention]
        
        achievable_value = current_value * multiplier
        
        return achievable_value
    
    def calculate_value_delta(self, repo_data: Dict[str, Any], interventions: List[str]) -> Dict[str, Any]:
        """
        Calculate Value Delta = Achievable State - Current State.
        
        Returns:
        - current_value: Current state value
        - achievable_value: Value after interventions
        - value_delta: Absolute increase
        - value_delta_percent: Percentage increase
        - total_effort_days: Total engineering effort required
        - value_per_day: Value created per engineering day
        """
        current_value = self.calculate_current_state_value(repo_data)
        achievable_value = self.calculate_achievable_state_value(repo_data, interventions)
        
        value_delta = achievable_value - current_value
        value_delta_percent = (value_delta / current_value * 100) if current_value > 0 else 0
        
        # Calculate total effort
        total_effort_days = sum(
            self.impact.INTERVENTION_EFFORT_DAYS.get(intervention, 10)
            for intervention in interventions
        )
        
        # Value per engineering day
        value_per_day = value_delta / total_effort_days if total_effort_days > 0 else 0
        
        return {
            "current_value": current_value,
            "achievable_value": achievable_value,
            "value_delta": value_delta,
            "value_delta_percent": value_delta_percent,
            "total_effort_days": total_effort_days,
            "value_per_day": value_per_day,
            "interventions": interventions,
        }
    
    def _log_scale(self, value: float) -> float:
        """Log scale to prevent dominance by large values."""
        import math
        return math.log10(value + 1)
    
    def recommend_interventions(self, repo_data: Dict[str, Any], max_effort_days: int = 30) -> List[Dict[str, Any]]:
        """
        Recommend optimal interventions within effort budget.
        
        Returns list of (intervention, value_delta, effort_days) sorted by value_per_day.
        """
        recommendations = []
        
        # Check current state
        has_tests = repo_data.get("has_tests", False)
        has_ci = repo_data.get("has_ci", False)
        has_readme = repo_data.get("has_readme", False)
        has_package = repo_data.get("has_package_file", False)
        
        # Identify missing interventions
        missing_interventions = []
        if not has_readme:
            missing_interventions.append("documentation_improvement")
        if not has_package:
            missing_interventions.append("packaging_completion")
        if not has_ci:
            missing_interventions.append("ci_addition")
        if not has_tests:
            missing_interventions.append("test_coverage")
        
        # Always consider high-impact interventions
        high_impact = ["api_stabilization", "ecosystem_integration", "migration_to_newer_platform"]
        
        # Evaluate all combinations within budget
        from itertools import combinations
        
        all_interventions = list(set(missing_interventions + high_impact))
        
        for r in range(1, len(all_interventions) + 1):
            for combo in combinations(all_interventions, r):
                total_effort = sum(
                    self.impact.INTERVENTION_EFFORT_DAYS.get(i, 10)
                    for i in combo
                )
                
                if total_effort <= max_effort_days:
                    delta = self.calculate_value_delta(repo_data, list(combo))
                    recommendations.append({
                        "interventions": list(combo),
                        "value_delta": delta["value_delta"],
                        "value_delta_percent": delta["value_delta_percent"],
                        "total_effort_days": total_effort,
                        "value_per_day": delta["value_per_day"],
                    })
        
        # Sort by value per day
        recommendations.sort(key=lambda x: x["value_per_day"], reverse=True)
        
        return recommendations[:10]  # Return top 10
