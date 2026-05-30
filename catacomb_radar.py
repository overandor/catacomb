"""Catacomb Radar - Hidden Infrastructure Discovery.

Identifies and ranks hidden infrastructure assets by:
- Expected Value Created Per Engineering Day
- Low recognition but high utility
- Strong dependency position
- Intervention potential
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Set
from datetime import datetime, timedelta
import json
from universe_classifier import UniverseClassifier, AssetMetrics, InterventionOpportunity, Universe


@dataclass
class RadarSignal:
    """A radar signal representing a hidden infrastructure opportunity."""
    asset_id: str
    asset_name: str
    asset_type: str  # github_repo, huggingface_model, npm_package, etc.
    
    # Universe classification
    universe: Universe
    
    # Value metrics
    current_value: float  # Current state score
    achievable_value: float  # Post-intervention state score
    value_delta: float  # The gap
    expected_value_per_day: float  # Key ranking metric
    
    # Intervention details
    best_intervention: str
    effort_days_estimate: int
    confidence: float
    
    # Hidden infrastructure indicators
    transitive_dependencies: int
    indirect_ecosystem_reach: int
    bus_factor: int
    unresolved_security_backlog: int
    contributor_concentration: float
    ecosystem_replacement_difficulty: float
    downstream_revenue_exposure: float
    
    # Evidence
    evidence: List[str] = field(default_factory=list)
    
    # Metadata
    last_updated: datetime = field(default_factory=datetime.utcnow)
    signal_strength: float = 0.0  # 0-1, composite score


class CatacombRadar:
    """Radar system for discovering hidden infrastructure opportunities."""
    
    def __init__(self):
        self.classifier = UniverseClassifier()
        self.signals: List[RadarSignal] = []
        self.signal_history: Dict[str, List[RadarSignal]] = {}
    
    def scan_asset(self, asset_id: str, asset_name: str, asset_type: str,
                  metrics: AssetMetrics) -> Optional[RadarSignal]:
        """Scan an asset and generate radar signal if it qualifies."""
        # Calculate intervention opportunities
        intervention_types = [
            "documentation", "build_system", "packaging", "api",
            "security", "dependency_cleanup", "performance", "migration"
        ]
        
        opportunities = []
        for intv_type in intervention_types:
            opportunity = self.classifier.calculate_value_delta(metrics, intv_type)
            opportunities.append(opportunity)
        
        # Classify universe
        universe = self.classifier.classify(asset_id, metrics, opportunities)
        
        # Only generate signal for Alpha universe
        if universe != Universe.ALPHA:
            return None
        
        # Get best opportunity
        best_opportunity = max(opportunities, key=lambda x: x.expected_value_per_day)
        
        # Calculate signal strength
        signal_strength = self._calculate_signal_strength(metrics, best_opportunity)
        
        # Create radar signal
        signal = RadarSignal(
            asset_id=asset_id,
            asset_name=asset_name,
            asset_type=asset_type,
            universe=universe,
            current_value=best_opportunity.current_state_score,
            achievable_value=best_opportunity.achievable_state_score,
            value_delta=best_opportunity.value_delta,
            expected_value_per_day=best_opportunity.expected_value_per_day,
            best_intervention=best_opportunity.intervention_type,
            effort_days_estimate=best_opportunity.effort_days_estimate,
            confidence=best_opportunity.confidence,
            transitive_dependencies=metrics.transitive_dependencies,
            indirect_ecosystem_reach=metrics.indirect_ecosystem_reach,
            bus_factor=metrics.bus_factor,
            unresolved_security_backlog=metrics.unresolved_security_backlog,
            contributor_concentration=metrics.contributor_concentration,
            ecosystem_replacement_difficulty=metrics.ecosystem_replacement_difficulty,
            downstream_revenue_exposure=metrics.downstream_revenue_exposure,
            evidence=best_opportunity.evidence,
            signal_strength=signal_strength
        )
        
        # Store signal
        self.signals.append(signal)
        if asset_id not in self.signal_history:
            self.signal_history[asset_id] = []
        self.signal_history[asset_id].append(signal)
        
        return signal
    
    def _calculate_signal_strength(self, metrics: AssetMetrics, 
                                  opportunity: InterventionOpportunity) -> float:
        """Calculate composite signal strength (0-1)."""
        strength = 0.0
        
        # Expected value per day (40% weight)
        ev_normalized = min(1.0, opportunity.expected_value_per_day / 2.0)
        strength += ev_normalized * 0.4
        
        # Hidden infrastructure indicators (30% weight)
        hidden_score = 0.0
        if metrics.transitive_dependencies > 50:
            hidden_score += 0.3
        if metrics.bus_factor == 1:
            hidden_score += 0.3
        if metrics.unresolved_security_backlog > 0:
            hidden_score += 0.2
        if metrics.downstream_revenue_exposure > 1000000:
            hidden_score += 0.2
        strength += hidden_score * 0.3
        
        # Confidence (20% weight)
        strength += opportunity.confidence * 0.2
        
        # Ecosystem leverage (10% weight)
        ecosystem_score = min(1.0, metrics.transitive_dependencies / 100.0)
        strength += ecosystem_score * 0.1
        
        return min(1.0, strength)
    
    def get_top_signals(self, limit: int = 50) -> List[RadarSignal]:
        """Get top radar signals ranked by expected value per day."""
        return sorted(self.signals, key=lambda x: x.expected_value_per_day, reverse=True)[:limit]
    
    def get_signals_by_intervention(self, intervention_type: str) -> List[RadarSignal]:
        """Get signals filtered by intervention type."""
        return [s for s in self.signals if s.best_intervention == intervention_type]
    
    def get_signals_by_ecosystem(self, min_transitive_deps: int = 10) -> List[RadarSignal]:
        """Get signals with high ecosystem leverage."""
        return [s for s in self.signals if s.transitive_dependencies >= min_transitive_deps]
    
    def get_signals_by_bus_factor(self, max_bus_factor: int = 2) -> List[RadarSignal]:
        """Get signals with critical bus factor."""
        return [s for s in self.signals if s.bus_factor <= max_bus_factor]
    
    def get_signals_by_security(self, min_backlog: int = 1) -> List[RadarSignal]:
        """Get signals with security backlog."""
        return [s for s in self.signals if s.unresolved_security_backlog >= min_backlog]
    
    def calculate_portfolio_allocation(self, total_engineering_days: int) -> Dict[str, Dict]:
        """Calculate optimal portfolio allocation for given engineering budget."""
        top_signals = self.get_top_signals(limit=100)
        
        allocation = []
        remaining_days = total_engineering_days
        
        for signal in top_signals:
            if remaining_days <= 0:
                break
            
            effort = min(signal.effort_days_estimate, remaining_days)
            expected_value = signal.expected_value_per_day * effort
            
            allocation.append({
                "asset_id": signal.asset_id,
                "asset_name": signal.asset_name,
                "intervention": signal.best_intervention,
                "effort_days": effort,
                "expected_value": expected_value,
                "confidence": signal.confidence,
                "signal_strength": signal.signal_strength
            })
            
            remaining_days -= effort
        
        return {
            "total_signals": len(top_signals),
            "allocated_signals": len(allocation),
            "total_effort_days": total_engineering_days,
            "allocated_effort_days": total_engineering_days - remaining_days,
            "total_expected_value": sum(a["expected_value"] for a in allocation),
            "allocations": allocation
        }
    
    def export_signals(self, filepath: str):
        """Export radar signals to JSON file."""
        signals_data = []
        for signal in self.signals:
            signals_data.append({
                "asset_id": signal.asset_id,
                "asset_name": signal.asset_name,
                "asset_type": signal.asset_type,
                "universe": signal.universe.value,
                "current_value": signal.current_value,
                "achievable_value": signal.achievable_value,
                "value_delta": signal.value_delta,
                "expected_value_per_day": signal.expected_value_per_day,
                "best_intervention": signal.best_intervention,
                "effort_days_estimate": signal.effort_days_estimate,
                "confidence": signal.confidence,
                "transitive_dependencies": signal.transitive_dependencies,
                "indirect_ecosystem_reach": signal.indirect_ecosystem_reach,
                "bus_factor": signal.bus_factor,
                "unresolved_security_backlog": signal.unresolved_security_backlog,
                "contributor_concentration": signal.contributor_concentration,
                "ecosystem_replacement_difficulty": signal.ecosystem_replacement_difficulty,
                "downstream_revenue_exposure": signal.downstream_revenue_exposure,
                "evidence": signal.evidence,
                "last_updated": signal.last_updated.isoformat(),
                "signal_strength": signal.signal_strength
            })
        
        with open(filepath, 'w') as f:
            json.dump(signals_data, f, indent=2)
    
    def get_radar_summary(self) -> Dict:
        """Get radar summary statistics."""
        if not self.signals:
            return {
                "total_signals": 0,
                "universe_stats": self.classifier.get_universe_stats(),
                "top_interventions": [],
                "avg_expected_value_per_day": 0,
                "avg_confidence": 0
            }
        
        # Count by intervention type
        intervention_counts = {}
        for signal in self.signals:
            intv = signal.best_intervention
            intervention_counts[intv] = intervention_counts.get(intv, 0) + 1
        
        # Calculate averages
        avg_ev_per_day = sum(s.expected_value_per_day for s in self.signals) / len(self.signals)
        avg_confidence = sum(s.confidence for s in self.signals) / len(self.signals)
        
        return {
            "total_signals": len(self.signals),
            "universe_stats": self.classifier.get_universe_stats(),
            "intervention_distribution": intervention_counts,
            "avg_expected_value_per_day": avg_ev_per_day,
            "avg_confidence": avg_confidence,
            "top_signal": self.signals[0] if self.signals else None
        }
