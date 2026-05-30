"""Three-Universe Architecture for Asset Classification.

Discovery Universe: Everything known (millions of assets)
Candidate Universe: Assets passing minimum thresholds (tens of thousands)
Alpha Universe: Rare subset with intervention potential (hundreds)
"""

from dataclasses import dataclass
from typing import Dict, List, Optional, Set
from enum import Enum
import re


class Universe(Enum):
    """Universe classification levels."""
    DISCOVERY = "discovery"  # Everything known
    CANDIDATE = "candidate"  # Passes minimum thresholds
    ALPHA = "alpha"  # High intervention potential


@dataclass
class AssetMetrics:
    """Comprehensive asset metrics for universe classification."""
    # Basic metrics
    stars: int = 0
    forks: int = 0
    contributors: int = 0
    open_issues: int = 0
    closed_issues: int = 0
    releases: int = 0
    
    # Activity metrics
    last_commit_days: int = 9999
    last_release_days: int = 9999
    commits_last_30d: int = 0
    commits_last_90d: int = 0
    
    # Ecosystem metrics
    transitive_dependencies: int = 0
    indirect_ecosystem_reach: int = 0
    downstream_revenue_exposure: float = 0.0
    integration_density: float = 0.0
    
    # Maintainer metrics
    bus_factor: int = 1
    maintainer_availability: float = 0.0
    contributor_concentration: float = 1.0  # 1.0 = single contributor
    
    # Technical metrics
    unresolved_security_backlog: int = 0
    api_surface_stability: float = 0.5  # 0.0 = unstable, 1.0 = stable
    migration_cost: float = 0.0  # 0.0 = easy, 1.0 = impossible
    ecosystem_replacement_difficulty: float = 0.5
    
    # Quality metrics
    has_ci: bool = False
    has_tests: bool = False
    has_documentation: bool = False
    license_valid: bool = False
    buildable: bool = False
    
    # Market signals
    weekly_downloads: int = 0
    monthly_active_users: int = 0
    growth_rate_30d: float = 0.0
    growth_rate_90d: float = 0.0


@dataclass
class InterventionOpportunity:
    """Intervention opportunity analysis."""
    intervention_type: str
    current_state_score: float  # 0-100
    achievable_state_score: float  # 0-100
    value_delta: float  # achievable - current
    effort_days_estimate: int
    expected_value_per_day: float  # value_delta / effort_days
    confidence: float  # 0-1
    evidence: List[str]


class UniverseClassifier:
    """Classifies assets into Discovery, Candidate, and Alpha universes."""
    
    # Candidate Universe thresholds
    CANDIDATE_MIN_STARS = 10
    CANDIDATE_MIN_CONTRIBUTORS = 1
    CANDIDATE_MAX_LAST_COMMIT_DAYS = 365
    CANDIDATE_REQUIRES_LICENSE = True
    CANDIDATE_REQUIRES_BUILDABLE = True
    CANDIDATE_MIN_ECOSYSTEM_PRESENCE = 5  # transitive dependencies or downloads
    
    # Alpha Universe thresholds
    ALPHA_MAX_STARS = 5000  # Exclude already-popular projects
    ALPHA_MIN_VALUE_DELTA = 30  # Minimum value delta (0-100 scale)
    ALPHA_MIN_EXPECTED_VALUE_PER_DAY = 0.5  # Minimum EV per engineering day
    ALPHA_MIN_CONFIDENCE = 0.4  # Minimum confidence in prediction
    ALPHA_MAX_CONTRIBUTOR_CONCENTRATION = 0.8  # Exclude single-dev dominated projects
    ALPHA_MIN_ECOSYSTEM_LEVERAGE = 10  # Minimum transitive dependencies
    
    def __init__(self):
        self.discovery_count = 0
        self.candidate_count = 0
        self.alpha_count = 0
    
    def classify(self, asset_id: str, metrics: AssetMetrics, 
                 intervention_opportunities: List[InterventionOpportunity]) -> Universe:
        """Classify an asset into a universe."""
        self.discovery_count += 1
        
        # Check Candidate Universe thresholds
        if not self._passes_candidate_thresholds(metrics):
            return Universe.DISCOVERY
        
        self.candidate_count += 1
        
        # Check Alpha Universe thresholds
        if self._passes_alpha_thresholds(metrics, intervention_opportunities):
            self.alpha_count += 1
            return Universe.ALPHA
        
        return Universe.CANDIDATE
    
    def _passes_candidate_thresholds(self, metrics: AssetMetrics) -> bool:
        """Check if asset passes Candidate Universe thresholds."""
        checks = [
            metrics.stars >= self.CANDIDATE_MIN_STARS,
            metrics.contributors >= self.CANDIDATE_MIN_CONTRIBUTORS,
            metrics.last_commit_days <= self.CANDIDATE_MAX_LAST_COMMIT_DAYS,
            not self.CANDIDATE_REQUIRES_LICENSE or metrics.license_valid,
            not self.CANDIDATE_REQUIRES_BUILDABLE or metrics.buildable,
            (metrics.transitive_dependencies + metrics.weekly_downloads) >= self.CANDIDATE_MIN_ECOSYSTEM_PRESENCE
        ]
        return all(checks)
    
    def _passes_alpha_thresholds(self, metrics: AssetMetrics, 
                                  opportunities: List[InterventionOpportunity]) -> bool:
        """Check if asset passes Alpha Universe thresholds."""
        # Exclude already-popular projects
        if metrics.stars > self.ALPHA_MAX_STARS:
            return False
        
        # Check for high-value intervention opportunities
        if not opportunities:
            return False
        
        best_opportunity = max(opportunities, key=lambda x: x.expected_value_per_day)
        
        checks = [
            best_opportunity.value_delta >= self.ALPHA_MIN_VALUE_DELTA,
            best_opportunity.expected_value_per_day >= self.ALPHA_MIN_EXPECTED_VALUE_PER_DAY,
            best_opportunity.confidence >= self.ALPHA_MIN_CONFIDENCE,
            metrics.contributor_concentration <= self.ALPHA_MAX_CONTRIBUTOR_CONCENTRATION,
            metrics.transitive_dependencies >= self.ALPHA_MIN_ECOSYSTEM_LEVERAGE
        ]
        return all(checks)
    
    def calculate_value_delta(self, metrics: AssetMetrics, 
                             intervention_type: str) -> InterventionOpportunity:
        """Calculate value delta for a specific intervention type."""
        current_score = self._calculate_current_state_score(metrics)
        achievable_score = self._calculate_achievable_state_score(metrics, intervention_type)
        value_delta = achievable_score - current_score
        effort_days = self._estimate_effort_days(metrics, intervention_type)
        expected_value_per_day = value_delta / effort_days if effort_days > 0 else 0
        confidence = self._calculate_confidence(metrics, intervention_type)
        evidence = self._generate_evidence(metrics, intervention_type)
        
        return InterventionOpportunity(
            intervention_type=intervention_type,
            current_state_score=current_score,
            achievable_state_score=achievable_score,
            value_delta=value_delta,
            effort_days_estimate=effort_days,
            expected_value_per_day=expected_value_per_day,
            confidence=confidence,
            evidence=evidence
        )
    
    def _calculate_current_state_score(self, metrics: AssetMetrics) -> float:
        """Calculate current state score (0-100)."""
        score = 0.0
        
        # Quality score (30 points)
        if metrics.has_ci: score += 10
        if metrics.has_tests: score += 10
        if metrics.has_documentation: score += 10
        
        # Ecosystem score (25 points)
        if metrics.transitive_dependencies > 0: score += 10
        if metrics.weekly_downloads > 0: score += 10
        if metrics.indirect_ecosystem_reach > 1000: score += 5
        
        # Maintainer health (20 points)
        score += min(20, metrics.bus_factor * 5)
        score += metrics.maintainer_availability * 10
        
        # Activity (15 points)
        if metrics.commits_last_30d > 0: score += 10
        if metrics.releases > 0: score += 5
        
        # Security (10 points)
        if metrics.unresolved_security_backlog == 0: score += 10
        elif metrics.unresolved_security_backlog < 5: score += 5
        
        return min(100, score)
    
    def _calculate_achievable_state_score(self, metrics: AssetMetrics, 
                                          intervention_type: str) -> float:
        """Calculate achievable state score after intervention (0-100)."""
        current = self._calculate_current_state_score(metrics)
        improvement = 0.0
        
        if intervention_type == "documentation":
            if not metrics.has_documentation:
                improvement += 15
            improvement += 10  # Documentation impact
        
        elif intervention_type == "build_system":
            if not metrics.has_ci:
                improvement += 15
            if not metrics.has_tests:
                improvement += 15
            improvement += 10  # Build system impact
        
        elif intervention_type == "packaging":
            improvement += 20  # Packaging impact
            if metrics.weekly_downloads == 0:
                improvement += 10  # New distribution channel
        
        elif intervention_type == "api":
            if metrics.api_surface_stability < 0.5:
                improvement += 20
            improvement += 15  # API impact
        
        elif intervention_type == "security":
            if metrics.unresolved_security_backlog > 0:
                improvement += min(20, metrics.unresolved_security_backlog * 2)
            improvement += 10  # Security impact
        
        elif intervention_type == "dependency_cleanup":
            improvement += 15  # Modernization impact
            if metrics.transitive_dependencies > 50:
                improvement += 10  # Large ecosystem benefit
        
        elif intervention_type == "performance":
            improvement += 15  # Performance impact
            if metrics.weekly_downloads > 10000:
                improvement += 10  # High-impact performance
        
        elif intervention_type == "migration":
            improvement += 20  # Migration impact
            if metrics.ecosystem_replacement_difficulty > 0.5:
                improvement += 10  # High-value migration
        
        return min(100, current + improvement)
    
    def _estimate_effort_days(self, metrics: AssetMetrics, intervention_type: str) -> int:
        """Estimate effort in engineering days for intervention."""
        base_effort = {
            "documentation": 7,
            "build_system": 14,
            "packaging": 10,
            "api": 21,
            "security": 14,
            "dependency_cleanup": 7,
            "performance": 21,
            "migration": 30
        }
        
        effort = base_effort.get(intervention_type, 14)
        
        # Adjust for project size
        if metrics.stars > 1000:
            effort = int(effort * 1.5)
        elif metrics.stars > 100:
            effort = int(effort * 1.2)
        
        # Adjust for complexity
        if metrics.transitive_dependencies > 100:
            effort = int(effort * 1.3)
        
        return effort
    
    def _calculate_confidence(self, metrics: AssetMetrics, intervention_type: str) -> float:
        """Calculate confidence in value delta prediction (0-1)."""
        confidence = 0.5
        
        # Higher confidence with more data
        if metrics.stars > 100:
            confidence += 0.1
        if metrics.contributors > 5:
            confidence += 0.1
        if metrics.commits_last_90d > 50:
            confidence += 0.1
        
        # Higher confidence for certain intervention types
        if intervention_type in ["documentation", "build_system", "packaging"]:
            confidence += 0.1
        
        # Lower confidence for complex interventions
        if intervention_type in ["migration", "performance"]:
            confidence -= 0.1
        
        return min(1.0, max(0.0, confidence))
    
    def _generate_evidence(self, metrics: AssetMetrics, intervention_type: str) -> List[str]:
        """Generate evidence list for intervention opportunity."""
        evidence = []
        
        if not metrics.has_documentation and intervention_type == "documentation":
            evidence.append("No documentation found")
        
        if not metrics.has_ci and intervention_type == "build_system":
            evidence.append("No CI/CD detected")
        
        if metrics.unresolved_security_backlog > 0 and intervention_type == "security":
            evidence.append(f"{metrics.unresolved_security_backlog} unresolved security issues")
        
        if metrics.transitive_dependencies > 50:
            evidence.append(f"High dependency count: {metrics.transitive_dependencies}")
        
        if metrics.bus_factor == 1:
            evidence.append("Single maintainer (bus factor = 1)")
        
        if metrics.weekly_downloads > 0:
            evidence.append(f"Active usage: {metrics.weekly_downloads} weekly downloads")
        
        if metrics.growth_rate_90d > 0.1:
            evidence.append(f"Growing: {metrics.growth_rate_90d:.1%} 90d growth rate")
        
        return evidence
    
    def get_universe_stats(self) -> Dict[str, int]:
        """Get universe classification statistics."""
        return {
            "discovery": self.discovery_count,
            "candidate": self.candidate_count,
            "alpha": self.alpha_count
        }
