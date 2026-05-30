"""Expanded KPIs for ecosystem and dependency analysis."""

from typing import Dict, Any, List
import logging

logger = logging.getLogger(__name__)


class EcosystemKPIs:
    """Advanced KPIs for identifying hidden infrastructure and ecosystem leverage."""
    
    @staticmethod
    def calculate_transitive_dependency_count(repo_data: Dict[str, Any]) -> int:
        """
        Estimate transitive dependency count.
        
        This measures how many projects depend on this repo directly or indirectly.
        High values indicate critical infrastructure.
        """
        direct_dependents = repo_data.get("dependents", 0)
        
        # Estimate transitive dependents (conservative multiplier)
        # In reality, this would require dependency graph analysis
        transitive_multiplier = 3.0  # Each direct dependent has ~3 transitive dependents
        transitive_count = int(direct_dependents * transitive_multiplier)
        
        return transitive_count
    
    @staticmethod
    def calculate_indirect_ecosystem_reach(repo_data: Dict[str, Any]) -> float:
        """
        Calculate indirect ecosystem reach.
        
        Measures the total user base reached through dependency chains.
        """
        transitive_count = EcosystemKPIs.calculate_transitive_dependency_count(repo_data)
        
        # Estimate users per dependent (conservative)
        users_per_dependent = 100
        indirect_reach = transitive_count * users_per_dependent
        
        return float(indirect_reach)
    
    @staticmethod
    def calculate_maintainer_bus_factor(repo_data: Dict[str, Any]) -> float:
        """
        Calculate bus factor (number of maintainers needed before project is at risk).
        
        Higher bus factor = more resilient.
        Lower bus factor = single point of failure.
        """
        contributors = repo_data.get("contributors", 0)
        
        # Bus factor: number of contributors responsible for 50%+ of commits
        # Simplified: assume top 20% of contributors do 80% of work
        critical_contributors = max(1, int(contributors * 0.2))
        
        bus_factor = critical_contributors
        
        return float(bus_factor)
    
    @staticmethod
    def calculate_contributor_concentration(repo_data: Dict[str, Any]) -> float:
        """
        Calculate contributor concentration (Herfindahl-Hirschman Index).
        
        0 = perfectly distributed
        1 = single contributor
        """
        contributors = repo_data.get("contributors", 0)
        
        if contributors <= 1:
            return 1.0  # Single point of failure
        
        # Simplified: assume power law distribution
        # Top contributor does 40%, next 20%, next 10%, etc.
        concentration = 0.0
        remaining = 1.0
        for i in range(min(contributors, 10)):
            share = remaining * 0.5
            concentration += share ** 2
            remaining -= share
        
        return concentration
    
    @staticmethod
    def calculate_unresolved_security_backlog(repo_data: Dict[str, Any]) -> int:
        """
        Estimate unresolved security backlog.
        
        High values indicate neglected security posture.
        """
        open_issues = repo_data.get("open_issues", 0)
        
        # Estimate security issues (conservative 5% of open issues)
        security_backlog = int(open_issues * 0.05)
        
        return security_backlog
    
    @staticmethod
    def calculate_ecosystem_replacement_difficulty(repo_data: Dict[str, Any]) -> float:
        """
        Calculate ecosystem replacement difficulty.
        
        0 = easy to replace
        1 = impossible to replace (critical infrastructure)
        """
        transitive_count = EcosystemKPIs.calculate_transitive_dependency_count(repo_data)
        indirect_reach = EcosystemKPIs.calculate_indirect_ecosystem_reach(repo_data)
        
        # Factors:
        # - High transitive count = hard to replace
        # - High indirect reach = hard to replace
        # - Unique functionality = hard to replace (simplified)
        
        # Normalize to 0-1
        transitive_score = min(transitive_count / 1000, 1.0)
        reach_score = min(indirect_reach / 100000, 1.0)
        
        replacement_difficulty = (transitive_score + reach_score) / 2
        
        return replacement_difficulty
    
    @staticmethod
    def calculate_downstream_revenue_exposure(repo_data: Dict[str, Any]) -> float:
        """
        Estimate downstream revenue exposure.
        
        Rough estimate of revenue at risk if this project fails.
        """
        indirect_reach = EcosystemKPIs.calculate_indirect_ecosystem_reach(repo_data)
        
        # Assume $1000 annual value per user (conservative)
        revenue_per_user = 1000
        revenue_exposure = indirect_reach * revenue_per_user
        
        return float(revenue_exposure)
    
    @staticmethod
    def calculate_integration_density(repo_data: Dict[str, Any]) -> float:
        """
        Calculate integration density.
        
        Measures how deeply integrated this project is in the ecosystem.
        """
        stars = repo_data.get("stars", 0)
        forks = repo_data.get("forks", 0)
        dependents = repo_data.get("dependents", 0)
        
        # Integration density = (forks + dependents) / stars
        # High values = heavily integrated relative to popularity
        if stars > 0:
            integration_density = (forks + dependents) / stars
        else:
            integration_density = 0.0
        
        return integration_density
    
    @staticmethod
    def calculate_api_surface_stability(repo_data: Dict[str, Any]) -> float:
        """
        Calculate API surface stability.
        
        0 = unstable (frequent breaking changes)
        1 = stable (mature API)
        """
        # Simplified: use age and release frequency
        created_at = repo_data.get("created_at", "")
        releases = repo_data.get("releases", 0)
        
        if not created_at:
            return 0.5  # Unknown
        
        # Calculate project age in years
        from datetime import datetime
        try:
            created_date = datetime.fromisoformat(created_at.replace('Z', '+00:00'))
            age_years = (datetime.now(created_date.tzinfo) - created_date).days / 365.25
        except:
            age_years = 1.0
        
        # Stability increases with age and release frequency
        if age_years < 0.5:
            stability = 0.2  # Very new
        elif age_years < 2:
            stability = 0.5  # Maturing
        else:
            stability = 0.8  # Mature
        
        # Adjust for release frequency
        if releases > 10:
            stability = min(stability + 0.1, 1.0)
        
        return stability
    
    @staticmethod
    def calculate_migration_cost(repo_data: Dict[str, Any]) -> float:
        """
        Estimate migration cost if this project needs to be replaced.
        
        Higher values = more expensive to migrate away from.
        """
        transitive_count = EcosystemKPIs.calculate_transitive_dependency_count(repo_data)
        replacement_difficulty = EcosystemKPIs.calculate_ecosystem_replacement_difficulty(repo_data)
        api_stability = EcosystemKPIs.calculate_api_surface_stability(repo_data)
        
        # Migration cost factors:
        # - High transitive count = expensive
        # - High replacement difficulty = expensive
        # - Low API stability = expensive (breaking changes)
        
        # Normalize to engineering days
        base_cost = transitive_count * 0.5  # 0.5 days per dependent
        difficulty_multiplier = 1.0 + replacement_difficulty
        stability_penalty = (1.0 - api_stability) * 100  # Unstable APIs cost more
        
        migration_cost_days = (base_cost * difficulty_multiplier) + stability_penalty
        
        return migration_cost_days
    
    @staticmethod
    def calculate_all_kpis(repo_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Calculate all ecosystem KPIs for a repository.
        """
        return {
            "transitive_dependency_count": EcosystemKPIs.calculate_transitive_dependency_count(repo_data),
            "indirect_ecosystem_reach": EcosystemKPIs.calculate_indirect_ecosystem_reach(repo_data),
            "maintainer_bus_factor": EcosystemKPIs.calculate_maintainer_bus_factor(repo_data),
            "contributor_concentration": EcosystemKPIs.calculate_contributor_concentration(repo_data),
            "unresolved_security_backlog": EcosystemKPIs.calculate_unresolved_security_backlog(repo_data),
            "ecosystem_replacement_difficulty": EcosystemKPIs.calculate_ecosystem_replacement_difficulty(repo_data),
            "downstream_revenue_exposure": EcosystemKPIs.calculate_downstream_revenue_exposure(repo_data),
            "integration_density": EcosystemKPIs.calculate_integration_density(repo_data),
            "api_surface_stability": EcosystemKPIs.calculate_api_surface_stability(repo_data),
            "migration_cost_days": EcosystemKPIs.calculate_migration_cost(repo_data),
        }
    
    @staticmethod
    def calculate_hidden_infrastructure_score(repo_data: Dict[str, Any]) -> float:
        """
        Calculate hidden infrastructure score.
        
        Identifies critical infrastructure that is under-recognized.
        
        High score = critical but under-recognized infrastructure.
        """
        kpis = EcosystemKPIs.calculate_all_kpis(repo_data)
        
        # Factors that indicate hidden infrastructure:
        # - High transitive dependencies (critical)
        # - High replacement difficulty (hard to replace)
        # - High downstream revenue exposure (economic impact)
        # - Low bus factor (fragile)
        # - High migration cost (expensive to replace)
        # - Low recognition (undervalued)
        
        stars = repo_data.get("stars", 0)
        
        # Recognition penalty (lower stars = higher hidden score)
        recognition_penalty = 1.0 - min(stars / 10000, 1.0)
        
        # Infrastructure strength
        infrastructure_strength = (
            (kpis["transitive_dependency_count"] / 100) * 0.3 +
            kpis["ecosystem_replacement_difficulty"] * 0.2 +
            (kpis["downstream_revenue_exposure"] / 1000000) * 0.2 +
            (1.0 - kpis["maintainer_bus_factor"] / 10) * 0.15 +
            (kpis["migration_cost_days"] / 1000) * 0.15
        )
        
        hidden_score = infrastructure_strength * recognition_penalty
        
        return min(hidden_score, 1.0)
