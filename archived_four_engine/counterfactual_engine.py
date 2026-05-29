"""Counterfactual Engine - generates and evaluates future states of assets."""
from typing import Dict, Any, List
from asset_layer import Asset, FutureState, AssetGenome
import numpy as np


class CounterfactualEngine:
    """Generates and evaluates counterfactual future states for assets."""
    
    def __init__(self):
        self.intervention_templates = self._load_intervention_templates()
    
    def _load_intervention_templates(self) -> List[Dict[str, Any]]:
        """Load intervention templates for different asset types."""
        return [
            {
                "name": "Documentation Overhaul",
                "base_effort_days": 7,
                "base_probability": 0.9,
                "base_upside": 0.3,
                "applicable_types": ["github_repo", "huggingface_model", "npm_package", "pypi_package"]
            },
            {
                "name": "Build System Modernization",
                "base_effort_days": 14,
                "base_probability": 0.8,
                "base_upside": 0.5,
                "applicable_types": ["github_repo", "crates_io_package"]
            },
            {
                "name": "Feature Expansion",
                "base_effort_days": 21,
                "base_probability": 0.7,
                "base_upside": 0.6,
                "applicable_types": ["github_repo", "huggingface_model", "api"]
            },
            {
                "name": "SaaS Conversion",
                "base_effort_days": 60,
                "base_probability": 0.5,
                "base_upside": 0.9,
                "applicable_types": ["github_repo", "api", "huggingface_model"]
            },
            {
                "name": "AI Integration",
                "base_effort_days": 45,
                "base_probability": 0.6,
                "base_upside": 0.85,
                "applicable_types": ["github_repo", "api", "agent_workflow"]
            },
            {
                "name": "Infrastructure Repositioning",
                "base_effort_days": 30,
                "base_probability": 0.7,
                "base_upside": 0.8,
                "applicable_types": ["github_repo", "npm_package", "pypi_package", "crates_io_package"]
            },
            {
                "name": "Community Building",
                "base_effort_days": 21,
                "base_probability": 0.8,
                "base_upside": 0.7,
                "applicable_types": ["github_repo", "huggingface_model", "agent_workflow"]
            },
            {
                "name": "Rust WASM Layer",
                "base_effort_days": 14,
                "base_probability": 0.85,
                "base_upside": 0.75,
                "applicable_types": ["github_repo", "crates_io_package"]
            },
            {
                "name": "AI Agent Wrapper",
                "base_effort_days": 30,
                "base_probability": 0.65,
                "base_upside": 0.8,
                "applicable_types": ["api", "huggingface_model", "github_repo"]
            },
            {
                "name": "Commercial API",
                "base_effort_days": 35,
                "base_probability": 0.55,
                "base_upside": 0.85,
                "applicable_types": ["github_repo", "api", "huggingface_model"]
            },
            {
                "name": "Package Ecosystem",
                "base_effort_days": 14,
                "base_probability": 0.8,
                "base_upside": 0.65,
                "applicable_types": ["github_repo", "npm_package", "pypi_package", "crates_io_package"]
            },
            {
                "name": "Open-Core Company",
                "base_effort_days": 90,
                "base_probability": 0.4,
                "base_upside": 0.95,
                "applicable_types": ["github_repo", "huggingface_model", "api"]
            },
            {
                "name": "Model Fine-Tuning",
                "base_effort_days": 21,
                "base_probability": 0.7,
                "base_upside": 0.7,
                "applicable_types": ["huggingface_model", "huggingface_dataset"]
            },
            {
                "name": "Dataset Curation",
                "base_effort_days": 14,
                "base_probability": 0.85,
                "base_upside": 0.6,
                "applicable_types": ["huggingface_dataset", "github_repo"]
            },
            {
                "name": "Benchmark Integration",
                "base_effort_days": 7,
                "base_probability": 0.9,
                "base_upside": 0.4,
                "applicable_types": ["github_repo", "huggingface_model", "benchmark"]
            }
        ]
    
    def generate_counterfactuals(self, asset: Asset, max_futures: int = 6) -> List[FutureState]:
        """
        Generate counterfactual future states for an asset.
        
        Args:
            asset: The asset to generate futures for
            max_futures: Maximum number of futures to generate
        
        Returns:
            List of FutureState objects
        """
        if not asset.genome:
            return []
        
        futures = []
        
        # Get applicable interventions
        applicable_templates = [
            template for template in self.intervention_templates
            if asset.asset_type.value in template["applicable_types"]
        ]
        
        for template in applicable_templates[:max_futures]:
            future = self._generate_future_state(asset, template)
            if future:
                futures.append(future)
        
        # Sort by expected return
        futures.sort(key=lambda f: f.expected_return(), reverse=True)
        
        asset.counterfactuals = futures
        
        return futures
    
    def _generate_future_state(self, asset: Asset, template: Dict[str, Any]) -> FutureState:
        """Generate a single future state based on template and asset genome."""
        if not asset.genome:
            return None
        
        # Adjust parameters based on asset genome
        effort_adjustment = self._calculate_effort_adjustment(asset, template)
        probability_adjustment = self._calculate_probability_adjustment(asset, template)
        upside_adjustment = self._calculate_upside_adjustment(asset, template)
        risk_adjustment = self._calculate_risk_adjustment(asset, template)
        
        # Calculate adjusted values
        effort_days = int(template["base_effort_days"] * effort_adjustment)
        probability = min(template["base_probability"] * probability_adjustment, 1.0)
        upside = min(template["base_upside"] * upside_adjustment, 1.0)
        risk = max(min(risk_adjustment, 1.0), 0.0)
        
        # Calculate expected value (normalized 0-1)
        expected_value = upside * probability * (1 - risk)
        
        # Time to realization (effort + market adoption time)
        time_days = effort_days + int(30 * (1 - probability))  # More uncertain = longer time
        
        return FutureState(
            intervention=template["name"],
            expected_value=expected_value,
            probability=probability,
            time_days=time_days,
            effort_days=effort_days,
            risk=risk,
            description=f"{template['name']} for {asset.name}"
        )
    
    def _calculate_effort_adjustment(self, asset: Asset, template: Dict[str, Any]) -> float:
        """Calculate effort adjustment based on asset genome."""
        if not asset.genome:
            return 1.0
        
        # Technical complexity affects effort
        complexity = asset.genome.technical_genome[0]  # complexity
        buildability = asset.genome.technical_genome[2]  # buildability
        maintainability = asset.genome.technical_genome[9]  # maintainability
        
        # Higher complexity = more effort
        effort_factor = 1.0 + (complexity - 0.5) * 0.5
        
        # Better buildability = less effort
        effort_factor *= (1.0 - (buildability - 0.5) * 0.3)
        
        # Better maintainability = less effort
        effort_factor *= (1.0 - (maintainability - 0.5) * 0.2)
        
        return max(0.5, min(effort_factor, 2.0))
    
    def _calculate_probability_adjustment(self, asset: Asset, template: Dict[str, Any]) -> float:
        """Calculate probability adjustment based on asset genome."""
        if not asset.genome:
            return 1.0
        
        # Social factors affect probability
        community_engagement = asset.genome.social_genome[3]  # community_engagement
        trust_score = asset.genome.social_genome[5]  # trust_score
        network_centrality = asset.genome.social_genome[8]  # network_centrality
        
        # Better community = higher probability
        prob_factor = 1.0 + (community_engagement - 0.5) * 0.4
        
        # Higher trust = higher probability
        prob_factor *= (1.0 + (trust_score - 0.5) * 0.3)
        
        # Better network position = higher probability
        prob_factor *= (1.0 + (network_centrality - 0.5) * 0.2)
        
        return max(0.5, min(prob_factor, 1.5))
    
    def _calculate_upside_adjustment(self, asset: Asset, template: Dict[str, Any]) -> float:
        """Calculate upside adjustment based on asset genome."""
        if not asset.genome:
            return 1.0
        
        # Economic and innovation factors affect upside
        market_size = asset.genome.economic_genome[4]  # market_size
        growth_rate = asset.genome.economic_genome[5]  # growth_rate
        network_effects = asset.genome.economic_genome[9]  # network_effects
        innovation_potential = asset.genome.innovation_genome[4]  # innovation_potential
        disruption_potential = asset.genome.innovation_genome[8]  # disruption_potential
        
        # Larger market = higher upside
        upside_factor = 1.0 + (market_size - 0.5) * 0.5
        
        # Higher growth = higher upside
        upside_factor *= (1.0 + (growth_rate - 0.5) * 0.4)
        
        # Network effects = higher upside
        upside_factor *= (1.0 + (network_effects - 0.5) * 0.3)
        
        # Innovation potential = higher upside
        upside_factor *= (1.0 + (innovation_potential - 0.5) * 0.3)
        
        # Disruption potential = higher upside
        upside_factor *= (1.0 + (disruption_potential - 0.5) * 0.4)
        
        return max(0.5, min(upside_factor, 2.0))
    
    def _calculate_risk_adjustment(self, asset: Asset, template: Dict[str, Any]) -> float:
        """Calculate risk adjustment based on asset genome."""
        if not asset.genome:
            return 0.5
        
        # Technical and economic factors affect risk
        technical_debt = 1.0 - asset.genome.technical_genome[9]  # maintainability inverted
        dependency_health = asset.genome.technical_genome[3]  # dependency_health
        competitive_advantage = asset.genome.economic_genome[8]  # competitive_advantage
        defensibility = asset.genome.innovation_genome[1]  # defensibility
        
        # Higher technical debt = higher risk
        risk = 0.3 + (technical_debt * 0.3)
        
        # Poor dependency health = higher risk
        risk += (1.0 - dependency_health) * 0.2
        
        # Lower competitive advantage = higher risk
        risk += (1.0 - competitive_advantage) * 0.2
        
        # Lower defensibility = higher risk
        risk += (1.0 - defensibility) * 0.2
        
        return max(0.1, min(risk, 0.9))
    
    def evaluate_best_future(self, asset: Asset) -> FutureState:
        """Evaluate and return the best future state for an asset."""
        if not asset.counterfactuals:
            self.generate_counterfactuals(asset)
        
        if not asset.counterfactuals:
            return None
        
        # Sort by ROI (expected return / effort)
        asset.counterfactuals.sort(key=lambda f: f.roi(), reverse=True)
        
        return asset.counterfactuals[0]
    
    def compare_futures(self, asset: Asset) -> Dict[str, Any]:
        """Compare all future states for an asset."""
        if not asset.counterfactuals:
            self.generate_counterfactuals(asset)
        
        if not asset.counterfactuals:
            return {}
        
        comparison = {
            "total_futures": len(asset.counterfactuals),
            "best_by_roi": max(asset.counterfactuals, key=lambda f: f.roi()).to_dict(),
            "best_by_expected_value": max(asset.counterfactuals, key=lambda f: f.expected_value).to_dict(),
            "lowest_risk": min(asset.counterfactuals, key=lambda f: f.risk).to_dict(),
            "fastest": min(asset.counterfactuals, key=lambda f: f.time_days).to_dict(),
            "all_futures": [f.to_dict() for f in asset.counterfactuals]
        }
        
        return comparison


class FutureStateComparator:
    """Compare future states across multiple assets."""
    
    def __init__(self):
        pass
    
    def find_highest_roi_intervention(self, assets: List[Asset]) -> Dict[str, Any]:
        """Find the highest ROI intervention across all assets."""
        all_futures = []
        
        for asset in assets:
            if asset.counterfactuals:
                for future in asset.counterfactuals:
                    all_futures.append({
                        "asset_id": asset.asset_id,
                        "asset_name": asset.name,
                        "future": future
                    })
        
        if not all_futures:
            return None
        
        # Sort by ROI
        all_futures.sort(key=lambda x: x["future"].roi(), reverse=True)
        
        best = all_futures[0]
        
        return {
            "asset_id": best["asset_id"],
            "asset_name": best["asset_name"],
            "intervention": best["future"].intervention,
            "roi": best["future"].roi(),
            "expected_value": best["future"].expected_value,
            "effort_days": best["future"].effort_days,
            "probability": best["future"].probability
        }
    
    def find_fastest_high_value_intervention(self, assets: List[Asset], min_value: float = 0.5) -> Dict[str, Any]:
        """Find the fastest intervention with minimum expected value."""
        all_futures = []
        
        for asset in assets:
            if asset.counterfactuals:
                for future in asset.counterfactuals:
                    if future.expected_value >= min_value:
                        all_futures.append({
                            "asset_id": asset.asset_id,
                            "asset_name": asset.name,
                            "future": future
                        })
        
        if not all_futures:
            return None
        
        # Sort by time
        all_futures.sort(key=lambda x: x["future"].time_days)
        
        best = all_futures[0]
        
        return {
            "asset_id": best["asset_id"],
            "asset_name": best["asset_name"],
            "intervention": best["future"].intervention,
            "time_days": best["future"].time_days,
            "expected_value": best["future"].expected_value,
            "effort_days": best["future"].effort_days
        }
    
    def find_lowest_risk_intervention(self, assets: List[Asset], min_value: float = 0.4) -> Dict[str, Any]:
        """Find the lowest risk intervention with minimum expected value."""
        all_futures = []
        
        for asset in assets:
            if asset.counterfactuals:
                for future in asset.counterfactuals:
                    if future.expected_value >= min_value:
                        all_futures.append({
                            "asset_id": asset.asset_id,
                            "asset_name": asset.name,
                            "future": future
                        })
        
        if not all_futures:
            return None
        
        # Sort by risk (ascending)
        all_futures.sort(key=lambda x: x["future"].risk)
        
        best = all_futures[0]
        
        return {
            "asset_id": best["asset_id"],
            "asset_name": best["asset_name"],
            "intervention": best["future"].intervention,
            "risk": best["future"].risk,
            "expected_value": best["future"].expected_value,
            "probability": best["future"].probability
        }
