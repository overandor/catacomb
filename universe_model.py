"""Three-tier universe model for Catacomb: Discovery → Candidate → Alpha."""

from typing import List, Dict, Any, Tuple
from enum import Enum
import logging

logger = logging.getLogger(__name__)


class UniverseTier(Enum):
    """Universe tier classification."""
    DISCOVERY = "discovery"  # Everything known (millions)
    CANDIDATE = "candidate"  # Passes minimum thresholds (tens of thousands)
    ALPHA = "alpha"  # High intervention potential (hundreds)


class UniverseFilter:
    """Filters for moving repos between universe tiers."""
    
    @staticmethod
    def discovery_to_candidate(repo_data: Dict[str, Any]) -> Tuple[bool, str]:
        """
        Filter Discovery Universe → Candidate Universe.
        
        Minimum thresholds:
        - Not archived
        - Valid license
        - Buildable
        - Measurable ecosystem presence
        - Sufficient evidence
        """
        reasons = []
        
        # Not archived
        if repo_data.get("archived", False):
            return False, "Repository is archived"
        
        # Valid license
        license_info = repo_data.get("license", {})
        if not license_info or license_info.get("key") in ["null", "other", "no-license"]:
            reasons.append("No valid license")
        
        # Buildable (has package file or build config)
        has_package = repo_data.get("has_package_file", False)
        has_build = repo_data.get("has_build_config", False)
        if not (has_package or has_build):
            reasons.append("Not buildable (no package file or build config)")
        
        # Measurable ecosystem presence
        stars = repo_data.get("stars", 0)
        forks = repo_data.get("forks", 0)
        watchers = repo_data.get("watchers", 0)
        
        # Minimum presence threshold (at least some community interest)
        if stars + forks + watchers < 5:
            reasons.append("Insufficient ecosystem presence")
        
        # Sufficient evidence (has README, recent activity)
        has_readme = repo_data.get("has_readme", False)
        recent_commits = repo_data.get("recent_commits", 0)
        
        if not has_readme:
            reasons.append("No README")
        
        if recent_commits < 1:
            reasons.append("No recent commits")
        
        # Pass if no critical failures
        passed = len(reasons) == 0
        
        if not passed:
            return False, f"Failed: {', '.join(reasons)}"
        
        return True, "Passed candidate thresholds"
    
    @staticmethod
    def candidate_to_alpha(repo_data: Dict[str, Any], analysis: Dict[str, Any]) -> Tuple[bool, str]:
        """
        Filter Candidate Universe → Alpha Universe.
        
        Alpha criteria:
        - Low recognition (not popular)
        - Strong technical foundations
        - Ecosystem leverage
        - Intervention potential
        - Evidence of latent demand
        """
        reasons = []
        
        # Low recognition (not popular)
        stars = repo_data.get("stars", 0)
        forks = repo_data.get("forks", 0)
        
        # Alpha threshold: not too popular (avoid blue-chip projects)
        if stars > 10000:
            return False, "Too popular (not undervalued)"
        
        if forks > 1000:
            return False, "Too widely adopted (not undervalued)"
        
        # Strong technical foundations
        has_tests = repo_data.get("has_tests", False)
        has_ci = repo_data.get("has_ci", False)
        language = repo_data.get("language", "")
        
        # Prefer projects with some foundation
        if not (has_tests or has_ci):
            reasons.append("Weak technical foundation (no tests or CI)")
        
        # Ecosystem leverage (many dependents)
        dependents = repo_data.get("dependents", 0)
        if dependents > 0:
            # Good: has downstream users
            pass
        else:
            reasons.append("No ecosystem leverage (no dependents)")
        
        # Intervention potential
        intervention_score = analysis.get("intervention_score", 0)
        if intervention_score < 50:
            reasons.append(f"Low intervention potential (score: {intervention_score})")
        
        # Evidence of latent demand
        open_issues = repo_data.get("open_issues", 0)
        recent_activity = repo_data.get("recent_commits", 0)
        
        if open_issues > 0 and recent_activity > 0:
            # Good: active community with unresolved needs
            pass
        else:
            reasons.append("No evidence of latent demand")
        
        # Innovation Alpha > 0 (undervalued)
        valuation = analysis.get("valuation", {})
        innovation_alpha = valuation.get("innovation_alpha", 0)
        
        if innovation_alpha <= 0:
            return False, f"No Innovation Alpha (alpha: {innovation_alpha})"
        
        # Pass if no critical failures
        passed = len(reasons) == 0
        
        if not passed:
            return False, f"Failed: {', '.join(reasons)}"
        
        return True, f"Alpha candidate (Innovation Alpha: {innovation_alpha:.2f})"


class UniverseModel:
    """Three-tier universe model manager."""
    
    def __init__(self):
        self.discovery_universe = []  # All known assets
        self.candidate_universe = []  # Assets passing minimum thresholds
        self.alpha_universe = []  # High intervention potential assets
    
    def add_to_discovery(self, repo_data: Dict[str, Any]):
        """Add asset to Discovery Universe."""
        self.discovery_universe.append(repo_data)
    
    def evaluate_candidate(self, repo_data: Dict[str, Any]) -> Tuple[bool, str]:
        """Evaluate if asset should be in Candidate Universe."""
        return UniverseFilter.discovery_to_candidate(repo_data)
    
    def evaluate_alpha(self, repo_data: Dict[str, Any], analysis: Dict[str, Any]) -> Tuple[bool, str]:
        """Evaluate if asset should be in Alpha Universe."""
        return UniverseFilter.candidate_to_alpha(repo_data, analysis)
    
    def build_candidate_universe(self, repos: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Build Candidate Universe from Discovery Universe."""
        candidates = []
        
        for repo_data in repos:
            passed, reason = self.evaluate_candidate(repo_data)
            if passed:
                candidates.append(repo_data)
                logger.info(f"Candidate: {repo_data.get('full_name')} - {reason}")
        
        self.candidate_universe = candidates
        logger.info(f"Built Candidate Universe: {len(candidates)} assets from {len(repos)}")
        
        return candidates
    
    def build_alpha_universe(self, repos_with_analysis: List[Tuple[Dict[str, Any], Dict[str, Any]]]) -> List[Dict[str, Any]]:
        """Build Alpha Universe from Candidate Universe."""
        alpha_assets = []
        
        for repo_data, analysis in repos_with_analysis:
            passed, reason = self.evaluate_alpha(repo_data, analysis)
            if passed:
                alpha_assets.append({
                    "repo_data": repo_data,
                    "analysis": analysis,
                    "reason": reason
                })
                logger.info(f"Alpha: {repo_data.get('full_name')} - {reason}")
        
        self.alpha_universe = alpha_assets
        logger.info(f"Built Alpha Universe: {len(alpha_assets)} assets from {len(repos_with_analysis)}")
        
        return alpha_assets
    
    def get_universe_stats(self) -> Dict[str, Any]:
        """Get statistics for all universes."""
        return {
            "discovery_count": len(self.discovery_universe),
            "candidate_count": len(self.candidate_universe),
            "alpha_count": len(self.alpha_universe),
            "candidate_ratio": len(self.candidate_universe) / len(self.discovery_universe) if self.discovery_universe else 0,
            "alpha_ratio": len(self.alpha_universe) / len(self.candidate_universe) if self.candidate_universe else 0,
        }
