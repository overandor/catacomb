"""Four-Engine Architecture: Evidence, Simulation, Allocation, Market."""
from typing import Dict, Any, List, Optional
from asset_layer import Asset, AssetType, AssetScanner, GenomeGenerator, InnovationMarketMap
from counterfactual_engine import CounterfactualEngine, FutureState
from innovation_allocation import InnovationAllocationEngine, AllocationPortfolio
from outcome_ledger import OutcomeLedger, InterventionRecord, InterventionStatus
from developer_capitalization import DeveloperCapitalization, DeveloperProfile


class EvidenceEngine:
    """
    Engine 1: Evidence Collection
    
    Ground truth data collection from multiple sources.
    
    Inputs:
    - GitHub
    - HuggingFace
    - npm
    - PyPI
    - crates.io
    - arXiv
    - Docker
    - Package registries
    
    Outputs:
    - Asset Genome
    - Trajectory
    - Utility
    - Quality
    - Risk
    
    No opinions. Only evidence.
    """
    
    def __init__(self):
        self.asset_scanner = AssetScanner()
        self.genome_generator = GenomeGenerator()
        self.market_map = InnovationMarketMap()
    
    def collect_asset(self, asset_type: AssetType, asset_id: str, raw_data: Dict[str, Any] = None) -> Asset:
        """Collect and analyze an asset from its source."""
        # Scan asset
        asset = self.asset_scanner.scan_asset(asset_type, asset_id)
        
        if not asset:
            return None
        
        # Generate genome
        if raw_data:
            self.genome_generator.generate_genome(asset, raw_data)
        
        # Add to market map
        self.market_map.add_asset(asset)
        
        return asset
    
    def collect_assets_batch(self, asset_specs: List[Dict[str, Any]]) -> List[Asset]:
        """Collect multiple assets in batch."""
        assets = []
        
        for spec in asset_specs:
            asset_type = AssetType(spec["asset_type"])
            asset_id = spec["asset_id"]
            raw_data = spec.get("raw_data")
            
            asset = self.collect_asset(asset_type, asset_id, raw_data)
            if asset:
                assets.append(asset)
        
        return assets
    
    def get_evidence_summary(self, asset: Asset) -> Dict[str, Any]:
        """Get evidence summary for an asset."""
        if not asset.genome:
            return {"error": "No genome generated"}
        
        return {
            "asset_id": asset.asset_id,
            "asset_type": asset.asset_type.value,
            "technical_genome": asset.genome.technical_genome.tolist(),
            "economic_genome": asset.genome.economic_genome.tolist(),
            "social_genome": asset.genome.social_genome.tolist(),
            "innovation_genome": asset.genome.innovation_genome.tolist(),
            "current_value": asset.current_value
        }


class SimulationEngine:
    """
    Engine 2: Counterfactual Simulation
    
    Generates future states for assets.
    
    For every asset, generate futures:
    - Future A: Documentation overhaul
    - Future B: Rust rewrite
    - Future C: AI integration
    - Future D: Commercial API
    - Future E: Package ecosystem
    - Future F: Open-core company
    
    Each future gets:
    - probability
    - cost
    - time
    - expected adoption
    - expected value
    - risk
    
    This becomes the moat.
    """
    
    def __init__(self):
        self.counterfactual_engine = CounterfactualEngine()
    
    def simulate_futures(self, asset: Asset, max_futures: int = 6) -> List[FutureState]:
        """Simulate counterfactual future states for an asset."""
        return self.counterfactual_engine.generate_counterfactuals(asset, max_futures)
    
    def simulate_batch(self, assets: List[Asset]) -> Dict[str, List[FutureState]]:
        """Simulate futures for multiple assets."""
        results = {}
        
        for asset in assets:
            futures = self.simulate_futures(asset)
            results[asset.asset_id] = futures
        
        return results
    
    def get_best_future(self, asset: Asset) -> Optional[FutureState]:
        """Get the best future state for an asset."""
        return self.counterfactual_engine.evaluate_best_future(asset)
    
    def compare_futures(self, asset: Asset) -> Dict[str, Any]:
        """Compare all future states for an asset."""
        return self.counterfactual_engine.compare_futures(asset)
    
    def find_highest_roi_across_assets(self, assets: List[Asset]) -> Optional[Dict[str, Any]]:
        """Find the highest ROI intervention across all assets."""
        return self.counterfactual_engine.find_highest_roi_intervention(assets)


class AllocationEngine:
    """
    Engine 3: Capital Allocation
    
    The most important component.
    
    Inputs:
    - 100 engineering days
    - $10k budget
    - 2 developers
    - 1 designer
    
    Output:
    - Invest: 40 days -> Asset A
    - Invest: 25 days -> Asset B
    - Invest: 35 days -> Asset C
    
    This is portfolio theory applied to software.
    Not repo discovery. Capital allocation.
    """
    
    def __init__(self):
        self.allocation_engine = InnovationAllocationEngine()
        self.developer_cap = DeveloperCapitalization()
    
    def optimize_allocation(
        self,
        assets: List[Asset],
        total_effort_days: int,
        risk_tolerance: float = 0.5,
        min_roi: float = 0.01,
        diversification: bool = True
    ) -> AllocationPortfolio:
        """Optimize allocation of effort across assets."""
        return self.allocation_engine.optimize_allocation(
            assets,
            total_effort_days,
            risk_tolerance,
            min_roi,
            diversification
        )
    
    def optimize_by_category(
        self,
        assets: List[Asset],
        total_effort_days: int,
        category_allocations: Dict[str, float]
    ) -> Dict[str, AllocationPortfolio]:
        """Optimize allocation by category."""
        return self.allocation_engine.optimize_by_category(
            assets,
            total_effort_days,
            category_allocations
        )
    
    def find_efficient_frontier(
        self,
        assets: List[Asset],
        total_effort_days: int,
        risk_levels: List[float] = None
    ) -> List[tuple]:
        """Find efficient frontier of risk-return tradeoffs."""
        return self.allocation_engine.find_efficient_frontier(
            assets,
            total_effort_days,
            risk_levels
        )
    
    def compare_strategies(
        self,
        assets: List[Asset],
        total_effort_days: int
    ) -> Dict[str, AllocationPortfolio]:
        """Compare different allocation strategies."""
        return self.allocation_engine.compare_strategies(assets, total_effort_days)
    
    def optimize_developer_portfolio(
        self,
        developer_profile: DeveloperProfile,
        available_effort_days: int,
        strategy: str = "balanced"
    ) -> Dict[str, Any]:
        """Optimize allocation for a developer's portfolio."""
        return self.developer_cap.optimize_developer_portfolio(
            developer_profile,
            available_effort_days,
            strategy
        )


class MarketEngine:
    """
    Engine 4: Innovation Market
    
    The eventual network.
    
    Users can:
    - publish interventions
    - claim ownership
    - show outcomes
    - verify transformations
    - discover opportunities
    
    Eventually:
    Developer → Asset Portfolio → Interventions → Outcomes → Reputation
    
    The reputation system becomes more valuable than stars.
    """
    
    def __init__(self, ledger_path: str = "outcome_ledger.json"):
        self.ledger = OutcomeLedger(ledger_path)
        self.developer_cap = DeveloperCapitalization()
    
    def publish_intervention(
        self,
        asset_id: str,
        asset_type: str,
        asset_name: str,
        developer_id: str,
        developer_username: str,
        before_state: Dict[str, Any],
        intervention_type: str,
        intervention_description: str,
        planned_effort_days: int,
        predicted_value: float,
        predicted_probability: float,
        predicted_risk: float
    ) -> InterventionRecord:
        """Publish a new intervention to the market."""
        return self.ledger.create_intervention(
            asset_id=asset_id,
            asset_type=asset_type,
            asset_name=asset_name,
            developer_id=developer_id,
            developer_username=developer_username,
            before_state=before_state,
            intervention_type=intervention_type,
            intervention_description=intervention_description,
            planned_effort_days=planned_effort_days,
            predicted_value=predicted_value,
            predicted_probability=predicted_probability,
            predicted_risk=predicted_risk
        )
    
    def claim_ownership(self, record_id: str, developer_id: str) -> InterventionRecord:
        """Claim ownership of an intervention."""
        record = self.ledger.get_record(record_id)
        if not record:
            raise ValueError(f"Record {record_id} not found")
        
        # Update record to show ownership claim
        record.developer_id = developer_id
        self.ledger._save()
        
        return record
    
    def start_intervention(self, record_id: str, actual_effort_days: int = None) -> InterventionRecord:
        """Mark intervention as started."""
        return self.ledger.start_intervention(record_id, actual_effort_days)
    
    def report_outcome(
        self,
        record_id: str,
        after_state: Dict[str, Any],
        outcome_metrics: Dict[str, Any],
        actual_effort_days: int = None
    ) -> InterventionRecord:
        """Report intervention outcome."""
        return self.ledger.complete_intervention(
            record_id,
            after_state,
            outcome_metrics,
            actual_effort_days
        )
    
    def verify_transformation(
        self,
        record_id: str,
        verifier_id: str,
        status: str,
        notes: str = None
    ) -> InterventionRecord:
        """Verify a transformation outcome."""
        from outcome_ledger import VerificationStatus
        
        verification_status = VerificationStatus(status)
        return self.ledger.verify_outcome(
            record_id,
            verifier_id,
            verification_status,
            notes
        )
    
    def discover_opportunities(
        self,
        min_innovation_alpha: float = 0.3,
        max_effort_days: int = 30
    ) -> List[Dict[str, Any]]:
        """Discover high-opportunity interventions."""
        # Get all records
        all_records = list(self.ledger.records.values())
        
        # Filter for opportunities
        opportunities = []
        for record in all_records:
            if record.status == InterventionStatus.PLANNED:
                # Calculate innovation alpha
                alpha = record.predicted_value - 0.5  # Simplified
                
                if alpha > min_innovation_alpha and record.planned_effort_days <= max_effort_days:
                    opportunities.append({
                        "record_id": record.record_id,
                        "asset_id": record.asset_id,
                        "asset_name": record.asset_name,
                        "intervention": record.intervention_type,
                        "predicted_value": record.predicted_value,
                        "effort_days": record.planned_effort_days,
                        "innovation_alpha": alpha
                    })
        
        # Sort by innovation alpha
        opportunities.sort(key=lambda x: x["innovation_alpha"], reverse=True)
        
        return opportunities
    
    def get_developer_reputation(self, developer_id: str) -> Dict[str, Any]:
        """Get developer reputation from intervention outcomes."""
        return self.ledger.get_developer_reputation(developer_id)
    
    def get_leaderboard(self, metric: str = "total_value_created") -> List[Dict[str, Any]]:
        """Get developer leaderboard."""
        # Get all unique developers
        developer_ids = set()
        for record in self.ledger.records.values():
            developer_ids.add(record.developer_id)
        
        # Calculate reputation for each
        leaderboard = []
        for developer_id in developer_ids:
            reputation = self.get_developer_reputation(developer_id)
            leaderboard.append({
                "developer_id": developer_id,
                "reputation": reputation
            })
        
        # Sort by metric
        leaderboard.sort(key=lambda x: x["reputation"].get(metric, 0), reverse=True)
        
        return leaderboard
    
    def get_learning_metrics(self) -> Dict[str, Any]:
        """Get learning metrics from outcome ledger."""
        return self.ledger.calculate_learning_metrics()
    
    def get_training_dataset(self) -> List[Dict[str, Any]]:
        """Get training dataset for ML models."""
        return self.ledger.get_training_dataset()


class CatacombOrchestrator:
    """
    Main orchestrator for the 4-engine architecture.
    
    Coordinates Evidence → Simulation → Allocation → Market
    """
    
    def __init__(self, ledger_path: str = "outcome_ledger.json"):
        self.evidence_engine = EvidenceEngine()
        self.simulation_engine = SimulationEngine()
        self.allocation_engine = AllocationEngine()
        self.market_engine = MarketEngine(ledger_path)
    
    def analyze_asset(self, asset_type: AssetType, asset_id: str, raw_data: Dict[str, Any] = None) -> Dict[str, Any]:
        """Full analysis pipeline for a single asset."""
        # Evidence Engine
        asset = self.evidence_engine.collect_asset(asset_type, asset_id, raw_data)
        
        if not asset:
            return {"error": "Failed to collect asset"}
        
        # Simulation Engine
        futures = self.simulation_engine.simulate_futures(asset)
        best_future = self.simulation_engine.get_best_future(asset)
        
        return {
            "asset": asset.to_dict(),
            "futures": [f.to_dict() for f in futures],
            "best_future": best_future.to_dict() if best_future else None
        }
    
    def optimize_portfolio(
        self,
        asset_specs: List[Dict[str, Any]],
        total_effort_days: int,
        strategy: str = "balanced"
    ) -> Dict[str, Any]:
        """Optimize portfolio allocation across assets."""
        # Evidence Engine - collect all assets
        assets = self.evidence_engine.collect_assets_batch(asset_specs)
        
        if not assets:
            return {"error": "No assets collected"}
        
        # Simulation Engine - generate futures for all
        self.simulation_engine.simulate_batch(assets)
        
        # Allocation Engine - optimize
        portfolio = self.allocation_engine.optimize_allocation(
            assets,
            total_effort_days
        )
        
        return {
            "portfolio": portfolio.to_dict(),
            "total_assets": len(assets),
            "strategy": strategy
        }
    
    def execute_intervention_lifecycle(
        self,
        asset_type: AssetType,
        asset_id: str,
        developer_id: str,
        developer_username: str,
        intervention_type: str,
        intervention_description: str,
        planned_effort_days: int,
        raw_data: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """Execute full intervention lifecycle: plan → start → complete → verify."""
        # Evidence Engine
        asset = self.evidence_engine.collect_asset(asset_type, asset_id, raw_data)
        
        if not asset:
            return {"error": "Failed to collect asset"}
        
        # Simulation Engine
        futures = self.simulation_engine.simulate_futures(asset)
        best_future = self.simulation_engine.get_best_future(asset)
        
        if not best_future:
            return {"error": "No viable futures generated"}
        
        # Market Engine - publish intervention
        record = self.market_engine.publish_intervention(
            asset_id=asset.asset_id,
            asset_type=asset.asset_type.value,
            asset_name=asset.name,
            developer_id=developer_id,
            developer_username=developer_username,
            before_state=asset.to_dict(),
            intervention_type=intervention_type,
            intervention_description=intervention_description,
            planned_effort_days=planned_effort_days,
            predicted_value=best_future.expected_value,
            predicted_probability=best_future.probability,
            predicted_risk=best_future.risk
        )
        
        return {
            "record_id": record.record_id,
            "asset": asset.to_dict(),
            "best_future": best_future.to_dict(),
            "intervention_published": True
        }
    
    def get_system_health(self) -> Dict[str, Any]:
        """Get system health metrics."""
        learning_metrics = self.market_engine.get_learning_metrics()
        leaderboard = self.market_engine.get_leaderboard()
        
        return {
            "learning_metrics": learning_metrics,
            "total_developers": len(leaderboard),
            "top_developer": leaderboard[0] if leaderboard else None
        }
