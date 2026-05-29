"""Developer Capitalization - treats developer as a portfolio of assets."""
from typing import Dict, Any, List
from asset_layer import Asset, AssetType
from counterfactual_engine import CounterfactualEngine
from innovation_allocation import InnovationAllocationEngine, Allocation
from dataclasses import dataclass


@dataclass
class DeveloperProfile:
    """Developer profile as a portfolio of assets."""
    developer_id: str
    username: str
    assets: List[Asset]
    launchable_assets: List[Asset]
    intervention_opportunities: List[Dict[str, Any]]
    expected_portfolio_value: float
    highest_leverage_intervention: Dict[str, Any]
    reputation_score: float
    ecosystem_influence: float
    innovation_alpha: float
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert profile to dictionary."""
        return {
            "developer_id": self.developer_id,
            "username": self.username,
            "total_assets": len(self.assets),
            "launchable_assets": len(self.launchable_assets),
            "intervention_opportunities": len(self.intervention_opportunities),
            "expected_portfolio_value": self.expected_portfolio_value,
            "highest_leverage_intervention": self.highest_leverage_intervention,
            "reputation_score": self.reputation_score,
            "ecosystem_influence": self.ecosystem_influence,
            "innovation_alpha": self.innovation_alpha,
            "assets": [asset.to_dict() for asset in self.assets]
        }


class DeveloperCapitalization:
    """Analyzes developers as portfolios of innovation assets."""
    
    def __init__(self):
        self.counterfactual_engine = CounterfactualEngine()
        self.allocation_engine = InnovationAllocationEngine()
    
    def analyze_developer(
        self,
        developer_id: str,
        username: str,
        assets: List[Asset]
    ) -> DeveloperProfile:
        """
        Analyze a developer as a portfolio.
        
        Args:
            developer_id: Unique developer identifier
            username: Developer username
            assets: List of assets owned by developer
        
        Returns:
            Developer profile with portfolio metrics
        """
        # Generate counterfactuals for all assets
        for asset in assets:
            if not asset.counterfactuals:
                self.counterfactual_engine.generate_counterfactuals(asset)
        
        # Calculate portfolio metrics
        launchable_assets = self._identify_launchable_assets(assets)
        intervention_opportunities = self._identify_intervention_opportunities(assets)
        expected_portfolio_value = self._calculate_portfolio_value(assets)
        highest_leverage_intervention = self._find_highest_leverage_intervention(assets)
        reputation_score = self._calculate_reputation_score(assets)
        ecosystem_influence = self._calculate_ecosystem_influence(assets)
        innovation_alpha = self._calculate_developer_innovation_alpha(assets)
        
        profile = DeveloperProfile(
            developer_id=developer_id,
            username=username,
            assets=assets,
            launchable_assets=launchable_assets,
            intervention_opportunities=intervention_opportunities,
            expected_portfolio_value=expected_portfolio_value,
            highest_leverage_intervention=highest_leverage_intervention,
            reputation_score=reputation_score,
            ecosystem_influence=ecosystem_influence,
            innovation_alpha=innovation_alpha
        )
        
        return profile
    
    def _identify_launchable_assets(self, assets: List[Asset]) -> List[Asset]:
        """Identify assets that are launchable (ready for intervention)."""
        launchable = []
        
        for asset in assets:
            if not asset.genome:
                continue
            
            # Launchable if: good technical quality + some adoption + room for growth
            technical_quality = asset.genome.technical_genome.mean()
            adoption = asset.genome.economic_genome[0]  # adoption
            growth_potential = asset.genome.economic_genome[5]  # growth_rate
            
            if technical_quality > 0.6 and adoption > 0.3 and growth_potential > 0.5:
                launchable.append(asset)
        
        return launchable
    
    def _identify_intervention_opportunities(self, assets: List[Asset]) -> List[Dict[str, Any]]:
        """Identify high-value intervention opportunities."""
        opportunities = []
        
        for asset in assets:
            if not asset.counterfactuals:
                continue
            
            for future in asset.counterfactuals:
                if future.roi() > 0.02 and future.expected_value > 0.5:
                    opportunities.append({
                        "asset_id": asset.asset_id,
                        "asset_name": asset.name,
                        "intervention": future.intervention,
                        "roi": future.roi(),
                        "expected_value": future.expected_value,
                        "effort_days": future.effort_days,
                        "probability": future.probability
                    })
        
        # Sort by ROI
        opportunities.sort(key=lambda x: x["roi"], reverse=True)
        
        return opportunities
    
    def _calculate_portfolio_value(self, assets: List[Asset]) -> float:
        """Calculate expected portfolio value."""
        total_value = 0.0
        
        for asset in assets:
            if asset.counterfactuals:
                # Use best future state
                best_future = max(asset.counterfactuals, key=lambda f: f.expected_value)
                total_value += best_future.expected_value * best_future.probability
            else:
                # Use current value
                total_value += asset.current_value
        
        return total_value
    
    def _find_highest_leverage_intervention(self, assets: List[Asset]) -> Dict[str, Any]:
        """Find the highest leverage intervention across all assets."""
        best_intervention = None
        best_roi = 0.0
        
        for asset in assets:
            if not asset.counterfactuals:
                continue
            
            for future in asset.counterfactuals:
                roi = future.roi()
                if roi > best_roi:
                    best_roi = roi
                    best_intervention = {
                        "asset_id": asset.asset_id,
                        "asset_name": asset.name,
                        "intervention": future.intervention,
                        "expected_value": future.expected_value,
                        "effort_days": future.effort_days,
                        "roi": roi,
                        "probability": future.probability
                    }
        
        return best_intervention or {}
    
    def _calculate_reputation_score(self, assets: List[Asset]) -> float:
        """Calculate developer reputation based on asset quality and impact."""
        if not assets:
            return 0.0
        
        reputation_scores = []
        
        for asset in assets:
            if asset.genome:
                # Social genome components for reputation
                maintainer_reputation = asset.genome.social_genome[1]  # maintainer_reputation
                ecosystem_influence = asset.genome.social_genome[2]  # ecosystem_influence
                trust_score = asset.genome.social_genome[5]  # trust_score
                
                asset_reputation = (maintainer_reputation + ecosystem_influence + trust_score) / 3
                reputation_scores.append(asset_reputation)
        
        if not reputation_scores:
            return 0.0
        
        return sum(reputation_scores) / len(reputation_scores)
    
    def _calculate_ecosystem_influence(self, assets: List[Asset]) -> float:
        """Calculate developer's influence in the ecosystem."""
        if not assets:
            return 0.0
        
        influence_scores = []
        
        for asset in assets:
            if asset.genome:
                # Social and economic genome for influence
                network_centrality = asset.genome.social_genome[8]  # network_centrality
                influence_score = asset.genome.social_genome[7]  # influence_score
                network_effects = asset.genome.economic_genome[9]  # network_effects
                
                asset_influence = (network_centrality + influence_score + network_effects) / 3
                influence_scores.append(asset_influence)
        
        if not influence_scores:
            return 0.0
        
        return sum(influence_scores) / len(influence_scores)
    
    def _calculate_developer_innovation_alpha(self, assets: List[Asset]) -> float:
        """Calculate developer's innovation alpha (undervalued assets)."""
        if not assets:
            return 0.0
        
        alpha_scores = []
        
        for asset in assets:
            alpha_scores.append(asset.innovation_alpha)
        
        if not alpha_scores:
            return 0.0
        
        return sum(alpha_scores) / len(alpha_scores)
    
    def optimize_developer_portfolio(
        self,
        developer_profile: DeveloperProfile,
        available_effort_days: int,
        strategy: str = "balanced"
    ) -> Dict[str, Any]:
        """
        Optimize allocation of effort for a developer's portfolio.
        
        Args:
            developer_profile: Developer profile
            available_effort_days: Engineering days available
            strategy: Allocation strategy
        
        Returns:
            Optimal allocation for developer
        """
        # Use innovation allocation engine
        portfolio = self.allocation_engine.optimize_allocation(
            developer_profile.assets,
            available_effort_days,
            risk_tolerance=0.5,
            min_roi=0.01,
            diversification=True
        )
        
        return {
            "developer_id": developer_profile.developer_id,
            "username": developer_profile.username,
            "available_effort_days": available_effort_days,
            "strategy": strategy,
            "allocation": portfolio.to_dict(),
            "expected_value_addition": portfolio.total_expected_return
        }
    
    def compare_developers(
        self,
        developer_profiles: List[DeveloperProfile]
    ) -> Dict[str, Any]:
        """
        Compare multiple developers by their portfolio metrics.
        
        Args:
            developer_profiles: List of developer profiles
        
        Returns:
            Comparison metrics
        """
        comparison = {
            "developers": [],
            "rankings": {
                "by_portfolio_value": [],
                "by_innovation_alpha": [],
                "by_reputation": [],
                "by_ecosystem_influence": []
            }
        }
        
        for profile in developer_profiles:
            comparison["developers"].append({
                "developer_id": profile.developer_id,
                "username": profile.username,
                "total_assets": len(profile.assets),
                "launchable_assets": len(profile.launchable_assets),
                "intervention_opportunities": len(profile.intervention_opportunities),
                "expected_portfolio_value": profile.expected_portfolio_value,
                "innovation_alpha": profile.innovation_alpha,
                "reputation_score": profile.reputation_score,
                "ecosystem_influence": profile.ecosystem_influence
            })
        
        # Generate rankings
        comparison["rankings"]["by_portfolio_value"] = sorted(
            comparison["developers"],
            key=lambda x: x["expected_portfolio_value"],
            reverse=True
        )
        
        comparison["rankings"]["by_innovation_alpha"] = sorted(
            comparison["developers"],
            key=lambda x: x["innovation_alpha"],
            reverse=True
        )
        
        comparison["rankings"]["by_reputation"] = sorted(
            comparison["developers"],
            key=lambda x: x["reputation_score"],
            reverse=True
        )
        
        comparison["rankings"]["by_ecosystem_influence"] = sorted(
            comparison["developers"],
            key=lambda x: x["ecosystem_influence"],
            reverse=True
        )
        
        return comparison
    
    def find_undervalued_developers(
        self,
        developer_profiles: List[DeveloperProfile],
        alpha_threshold: float = 0.3
    ) -> List[DeveloperProfile]:
        """
        Find developers with high innovation alpha (undervalued).
        
        Args:
            developer_profiles: List of developer profiles
            alpha_threshold: Minimum innovation alpha threshold
        
        Returns:
            List of undervalued developers
        """
        undervalued = [
            profile for profile in developer_profiles
            if profile.innovation_alpha > alpha_threshold
        ]
        
        # Sort by innovation alpha
        undervalued.sort(key=lambda p: p.innovation_alpha, reverse=True)
        
        return undervalued


class DeveloperScanner:
    """Scans developer profiles from various sources."""
    
    def __init__(self):
        pass
    
    def scan_github_developer(self, username: str) -> Dict[str, Any]:
        """Scan a GitHub developer's profile."""
        # Placeholder - would implement GitHub API integration
        return {
            "developer_id": f"github:{username}",
            "username": username,
            "source": "github",
            "assets": []  # Would fetch repos
        }
    
    def scan_huggingface_developer(self, username: str) -> Dict[str, Any]:
        """Scan a HuggingFace developer's profile."""
        # Placeholder - would implement HuggingFace API integration
        return {
            "developer_id": f"huggingface:{username}",
            "username": username,
            "source": "huggingface",
            "assets": []  # Would fetch models, datasets
        }
