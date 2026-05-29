"""Innovation Allocation Engine - optimal capital allocation across assets."""
from typing import Dict, Any, List, Tuple
from asset_layer import Asset, FutureState
from counterfactual_engine import CounterfactualEngine
import numpy as np
from dataclasses import dataclass


@dataclass
class Allocation:
    """A single allocation of effort to an intervention."""
    asset_id: str
    asset_name: str
    intervention: str
    effort_days: int
    expected_value: float
    probability: float
    roi: float
    risk: float


@dataclass
class AllocationPortfolio:
    """A portfolio of allocations."""
    allocations: List[Allocation]
    total_effort_days: int
    total_expected_value: float
    total_expected_return: float
    average_roi: float
    average_risk: float
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert portfolio to dictionary."""
        return {
            "allocations": [
                {
                    "asset_id": a.asset_id,
                    "asset_name": a.asset_name,
                    "intervention": a.intervention,
                    "effort_days": a.effort_days,
                    "expected_value": a.expected_value,
                    "probability": a.probability,
                    "roi": a.roi,
                    "risk": a.risk
                }
                for a in self.allocations
            ],
            "total_effort_days": self.total_effort_days,
            "total_expected_value": self.total_expected_value,
            "total_expected_return": self.total_expected_return,
            "average_roi": self.average_roi,
            "average_risk": self.average_risk
        }


class InnovationAllocationEngine:
    """Optimizes allocation of engineering effort across innovation assets."""
    
    def __init__(self):
        self.counterfactual_engine = CounterfactualEngine()
    
    def optimize_allocation(
        self,
        assets: List[Asset],
        total_effort_days: int,
        risk_tolerance: float = 0.5,
        min_roi: float = 0.01,
        diversification: bool = True
    ) -> AllocationPortfolio:
        """
        Optimize allocation of effort across assets.
        
        Args:
            assets: List of assets to consider
            total_effort_days: Total engineering days available
            risk_tolerance: Risk tolerance (0-1, higher = more risk accepted)
            min_roi: Minimum ROI threshold
            diversification: Whether to diversify across assets
        
        Returns:
            Optimal allocation portfolio
        """
        # Generate counterfactuals for all assets
        for asset in assets:
            if not asset.counterfactuals:
                self.counterfactual_engine.generate_counterfactuals(asset)
        
        # Collect all possible interventions
        all_interventions = []
        for asset in assets:
            if asset.counterfactuals:
                for future in asset.counterfactuals:
                    all_interventions.append({
                        "asset": asset,
                        "future": future
                    })
        
        # Filter by ROI and risk tolerance
        filtered_interventions = [
            i for i in all_interventions
            if i["future"].roi() >= min_roi
            and i["future"].risk <= risk_tolerance
        ]
        
        if not filtered_interventions:
            return AllocationPortfolio([], 0, 0, 0, 0, 0)
        
        # Sort by ROI (descending)
        filtered_interventions.sort(key=lambda x: x["future"].roi(), reverse=True)
        
        # Greedy allocation (can be upgraded to knapsack optimization)
        allocations = []
        remaining_effort = total_effort_days
        
        for intervention in filtered_interventions:
            asset = intervention["asset"]
            future = intervention["future"]
            
            if future.effort_days <= remaining_effort:
                # Can fully allocate
                allocation = Allocation(
                    asset_id=asset.asset_id,
                    asset_name=asset.name,
                    intervention=future.intervention,
                    effort_days=future.effort_days,
                    expected_value=future.expected_value,
                    probability=future.probability,
                    roi=future.roi(),
                    risk=future.risk
                )
                allocations.append(allocation)
                remaining_effort -= future.effort_days
                
                if diversification:
                    # Limit to one intervention per asset
                    filtered_interventions = [
                        i for i in filtered_interventions
                        if i["asset"].asset_id != asset.asset_id
                    ]
            
            if remaining_effort <= 0:
                break
        
        # Calculate portfolio metrics
        portfolio = self._calculate_portfolio_metrics(allocations)
        
        return portfolio
    
    def _calculate_portfolio_metrics(self, allocations: List[Allocation]) -> AllocationPortfolio:
        """Calculate portfolio-level metrics."""
        if not allocations:
            return AllocationPortfolio([], 0, 0, 0, 0, 0)
        
        total_effort = sum(a.effort_days for a in allocations)
        total_expected_value = sum(a.expected_value for a in allocations)
        total_expected_return = sum(a.expected_value * a.probability for a in allocations)
        average_roi = sum(a.roi for a in allocations) / len(allocations)
        average_risk = sum(a.risk for a in allocations) / len(allocations)
        
        return AllocationPortfolio(
            allocations=allocations,
            total_effort_days=total_effort,
            total_expected_value=total_expected_value,
            total_expected_return=total_expected_return,
            average_roi=average_roi,
            average_risk=average_risk
        )
    
    def optimize_by_category(
        self,
        assets: List[Asset],
        total_effort_days: int,
        category_allocations: Dict[str, float]
    ) -> Dict[str, AllocationPortfolio]:
        """
        Optimize allocation by category.
        
        Args:
            assets: List of assets
            total_effort_days: Total effort available
            category_allocations: Dict mapping category to effort percentage (e.g., {"infrastructure": 0.4, "ai": 0.6})
        
        Returns:
            Dict mapping category to allocation portfolio
        """
        # Group assets by category (using asset_type as proxy)
        category_assets = {}
        for asset in assets:
            category = asset.asset_type.value
            if category not in category_assets:
                category_assets[category] = []
            category_assets[category].append(asset)
        
        # Allocate effort by category
        category_portfolios = {}
        for category, percentage in category_allocations.items():
            category_effort = int(total_effort_days * percentage)
            category_asset_list = category_assets.get(category, [])
            
            if category_asset_list:
                portfolio = self.optimize_allocation(
                    category_asset_list,
                    category_effort
                )
                category_portfolios[category] = portfolio
        
        return category_portfolios
    
    def find_efficient_frontier(
        self,
        assets: List[Asset],
        total_effort_days: int,
        risk_levels: List[float] = None
    ) -> List[Tuple[float, AllocationPortfolio]]:
        """
        Find efficient frontier of risk-return tradeoffs.
        
        Args:
            assets: List of assets
            total_effort_days: Total effort available
            risk_levels: List of risk tolerance levels to test
        
        Returns:
            List of (risk_level, portfolio) tuples
        """
        if risk_levels is None:
            risk_levels = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
        
        frontier = []
        
        for risk_level in risk_levels:
            portfolio = self.optimize_allocation(
                assets,
                total_effort_days,
                risk_tolerance=risk_level
            )
            frontier.append((risk_level, portfolio))
        
        return frontier
    
    def compare_strategies(
        self,
        assets: List[Asset],
        total_effort_days: int
    ) -> Dict[str, AllocationPortfolio]:
        """
        Compare different allocation strategies.
        
        Args:
            assets: List of assets
            total_effort_days: Total effort available
        
        Returns:
            Dict mapping strategy name to portfolio
        """
        strategies = {}
        
        # Strategy 1: Maximize ROI (high risk)
        strategies["max_roi"] = self.optimize_allocation(
            assets,
            total_effort_days,
            risk_tolerance=0.8,
            min_roi=0.02,
            diversification=False
        )
        
        # Strategy 2: Balanced (moderate risk, diversified)
        strategies["balanced"] = self.optimize_allocation(
            assets,
            total_effort_days,
            risk_tolerance=0.5,
            min_roi=0.01,
            diversification=True
        )
        
        # Strategy 3: Conservative (low risk)
        strategies["conservative"] = self.optimize_allocation(
            assets,
            total_effort_days,
            risk_tolerance=0.3,
            min_roi=0.005,
            diversification=True
        )
        
        # Strategy 4: Fast wins (short time horizon)
        strategies["fast_wins"] = self.optimize_allocation(
            assets,
            total_effort_days,
            risk_tolerance=0.6,
            min_roi=0.01,
            diversification=True
        )
        
        return strategies
    
    def sensitivity_analysis(
        self,
        assets: List[Asset],
        total_effort_days: int,
        parameter: str,
        values: List[float]
    ) -> List[Tuple[float, AllocationPortfolio]]:
        """
        Perform sensitivity analysis on a parameter.
        
        Args:
            assets: List of assets
            total_effort_days: Total effort available
            parameter: Parameter to vary ("risk_tolerance", "min_roi")
            values: List of parameter values to test
        
        Returns:
            List of (parameter_value, portfolio) tuples
        """
        results = []
        
        for value in values:
            if parameter == "risk_tolerance":
                portfolio = self.optimize_allocation(
                    assets,
                    total_effort_days,
                    risk_tolerance=value
                )
            elif parameter == "min_roi":
                portfolio = self.optimize_allocation(
                    assets,
                    total_effort_days,
                    min_roi=value
                )
            else:
                continue
            
            results.append((value, portfolio))
        
        return results


class CapitalAllocationQuestion:
    """Answers the core question: where should effort be invested?"""
    
    def __init__(self):
        self.engine = InnovationAllocationEngine()
    
    def answer(
        self,
        assets: List[Asset],
        effort_days: int,
        strategy: str = "balanced"
    ) -> Dict[str, Any]:
        """
        Answer: Where should effort be invested?
        
        Args:
            assets: Available assets
            effort_days: Engineering days available
            strategy: Allocation strategy ("max_roi", "balanced", "conservative", "fast_wins")
        
        Returns:
            Detailed answer with recommendations
        """
        # Get strategies
        strategies = self.engine.compare_strategies(assets, effort_days)
        
        # Select requested strategy
        portfolio = strategies.get(strategy, strategies["balanced"])
        
        # Generate answer
        answer = {
            "question": f"Where should {effort_days} days of engineering effort be invested?",
            "strategy": strategy,
            "portfolio": portfolio.to_dict(),
            "summary": self._generate_summary(portfolio),
            "recommendations": self._generate_recommendations(portfolio),
            "alternative_strategies": {
                name: port.to_dict()
                for name, port in strategies.items()
                if name != strategy
            }
        }
        
        return answer
    
    def _generate_summary(self, portfolio: AllocationPortfolio) -> str:
        """Generate human-readable summary."""
        if not portfolio.allocations:
            return "No viable interventions found with given constraints."
        
        top_allocation = portfolio.allocations[0]
        
        summary = f"""
        Invest {portfolio.total_effort_days} days across {len(portfolio.allocations)} interventions.
        Expected return: {portfolio.total_expected_return:.2f}
        Average ROI: {portfolio.average_roi:.4f}
        
        Top intervention: {top_allocation.intervention} on {top_allocation.asset_name}
        Effort: {top_allocation.effort_days} days
        Expected value: {top_allocation.expected_value:.2f}
        Probability: {top_allocation.probability:.0%}
        """
        
        return summary.strip()
    
    def _generate_recommendations(self, portfolio: AllocationPortfolio) -> List[str]:
        """Generate actionable recommendations."""
        recommendations = []
        
        if not portfolio.allocations:
            recommendations.append("Consider relaxing risk tolerance or ROI thresholds.")
            return recommendations
        
        # Top recommendation
        top = portfolio.allocations[0]
        recommendations.append(
            f"Priority: Execute {top.intervention} on {top.asset_name} "
            f"({top.effort_days} days, {top.probability:.0%} success rate)"
        )
        
        # Risk-based recommendations
        if portfolio.average_risk > 0.6:
            recommendations.append("High-risk portfolio: monitor closely and be prepared to pivot.")
        elif portfolio.average_risk < 0.3:
            recommendations.append("Conservative portfolio: consider adding higher-risk interventions for upside.")
        
        # Diversification recommendations
        if len(portfolio.allocations) == 1:
            recommendations.append("Single-asset allocation: consider diversifying to reduce concentration risk.")
        
        # Effort utilization
        if portfolio.total_effort_days < 100:
            recommendations.append(f"Low effort utilization: {portfolio.total_effort_days} days used.")
        
        return recommendations
