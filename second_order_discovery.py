"""Second-order opportunity discovery - dependency graph analysis."""
from typing import Dict, Any, List, Set, Optional, Tuple
from dataclasses import dataclass
from innovation_knowledge_graph import InnovationKnowledgeGraph, NodeType, EdgeType


@dataclass
class SecondOrderOpportunity:
    """A second-order opportunity discovered through dependency analysis."""
    opportunity_id: str
    source_asset: str
    dependency_asset: str
    intervention_target: str
    opportunity_type: str
    expected_value: float
    propagation_factor: float  # How much value propagates to dependents
    reasoning: str
    affected_dependents: List[str]
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "opportunity_id": self.opportunity_id,
            "source_asset": self.source_asset,
            "dependency_asset": self.dependency_asset,
            "intervention_target": self.intervention_target,
            "opportunity_type": self.opportunity_type,
            "expected_value": self.expected_value,
            "propagation_factor": self.propagation_factor,
            "reasoning": self.reasoning,
            "affected_dependents": self.affected_dependents
        }


class SecondOrderDiscovery:
    """
    Discovers second-order opportunities through dependency graph analysis.
    
    Most scanners never see this:
    
    Repo A depends on Package B
    Package B abandoned
    Intervention on B creates value for A
    
    This module discovers these hidden opportunities.
    """
    
    def __init__(self, graph: InnovationKnowledgeGraph):
        self.graph = graph
    
    def find_dependency_opportunities(
        self,
        min_impact: float = 0.5,
        max_depth: int = 2
    ) -> List[SecondOrderOpportunity]:
        """
        Find opportunities where improving a dependency creates value for dependents.
        
        Args:
            min_impact: Minimum expected value threshold
            max_depth: Maximum depth to search in dependency graph
        
        Returns:
            List of second-order opportunities
        """
        opportunities = []
        
        # Get all nodes
        for node_id in self.graph.nodes:
            node = self.graph.get_node(node_id)
            if not node:
                continue
            
            # Check if this is a package or repository
            if node.node_type not in [NodeType.PACKAGE, NodeType.REPOSITORY]:
                continue
            
            # Check if node is abandoned or low quality
            is_abandoned = node.properties.get("abandoned", False)
            quality = node.properties.get("quality", 1.0)
            last_updated = node.properties.get("last_updated", "")
            
            if is_abandoned or quality < 0.5:
                # Find dependents
                dependents = self._find_dependents(node_id)
                
                if not dependents:
                    continue
                
                # Calculate propagation factor (more dependents = higher impact)
                propagation_factor = min(len(dependents) / 10, 1.0)
                
                # Find interventions for this asset
                interventions = self.graph.get_neighbors(node_id, EdgeType.TRANSFORMED_INTO)
                
                for intervention_id, _, _ in interventions:
                    intervention_node = self.graph.get_node(intervention_id)
                    if intervention_node:
                        expected_value = intervention_node.properties.get("expected_value", 0)
                        
                        # Adjust expected value by propagation factor
                        propagated_value = expected_value * (1 + propagation_factor)
                        
                        if propagated_value >= min_impact:
                            opportunity = SecondOrderOpportunity(
                                opportunity_id=f"dep_{node_id}_{intervention_id}",
                                source_asset=node_id,
                                dependency_asset=node_id,
                                intervention_target=intervention_id,
                                opportunity_type="dependency_improvement",
                                expected_value=propagated_value,
                                propagation_factor=propagation_factor,
                                reasoning=f"Improving {node_id} creates value for {len(dependents)} dependent assets",
                                affected_dependents=dependents
                            )
                            opportunities.append(opportunity)
        
        # Sort by expected value
        opportunities.sort(key=lambda x: x.expected_value, reverse=True)
        
        return opportunities
    
    def _find_dependents(self, node_id: str) -> List[str]:
        """Find all nodes that depend on this node."""
        dependents = []
        
        for other_node_id in self.graph.nodes:
            # Check if other_node depends on node_id
            neighbors = self.graph.get_neighbors(other_node_id, EdgeType.DEPENDS_ON)
            for neighbor_id, _, _ in neighbors:
                if neighbor_id == node_id:
                    dependents.append(other_node_id)
                    break
        
        return dependents
    
    def find_transitive_opportunities(
        self,
        max_depth: int = 3,
        min_impact: float = 0.3
    ) -> List[SecondOrderOpportunity]:
        """
        Find opportunities through transitive dependencies.
        
        Example:
        A depends on B depends on C
        Improving C creates value for B and A
        """
        opportunities = []
        
        for node_id in self.graph.nodes:
            node = self.graph.get_node(node_id)
            if not node:
                continue
            
            # Find all transitive dependents
            transitive_dependents = self._find_transitive_dependents(node_id, max_depth)
            
            if len(transitive_dependents) < 2:  # Need at least 2 levels
                continue
            
            # Calculate cumulative impact
            cumulative_impact = sum(
                dep.get("impact", 1.0)
                for dep in transitive_dependents
            )
            
            if cumulative_impact >= min_impact:
                # Find interventions
                interventions = self.graph.get_neighbors(node_id, EdgeType.TRANSFORMED_INTO)
                
                for intervention_id, _, _ in interventions:
                    intervention_node = self.graph.get_node(intervention_id)
                    if intervention_node:
                        expected_value = intervention_node.properties.get("expected_value", 0)
                        propagated_value = expected_value * (1 + cumulative_impact / 10)
                        
                        opportunity = SecondOrderOpportunity(
                            opportunity_id=f"trans_{node_id}_{intervention_id}",
                            source_asset=node_id,
                            dependency_asset=node_id,
                            intervention_target=intervention_id,
                            opportunity_type="transitive_improvement",
                            expected_value=propagated_value,
                            propagation_factor=cumulative_impact / 10,
                            reasoning=f"Improving {node_id} creates value through {len(transitive_dependents)} transitive dependencies",
                            affected_dependents=[dep["node_id"] for dep in transitive_dependents]
                        )
                        opportunities.append(opportunity)
        
        opportunities.sort(key=lambda x: x.expected_value, reverse=True)
        
        return opportunities
    
    def _find_transitive_dependents(
        self,
        node_id: str,
        max_depth: int
    ) -> List[Dict[str, Any]]:
        """Find all transitive dependents up to max_depth."""
        transitive = []
        visited = {node_id}
        
        def dfs(current_id: str, depth: int, impact: float):
            if depth >= max_depth:
                return
            
            dependents = self._find_dependents(current_id)
            
            for dep_id in dependents:
                if dep_id not in visited:
                    visited.add(dep_id)
                    transitive.append({
                        "node_id": dep_id,
                        "depth": depth + 1,
                        "impact": impact * 0.9  # Impact decays with depth
                    })
                    dfs(dep_id, depth + 1, impact * 0.9)
        
        dfs(node_id, 0, 1.0)
        
        return transitive
    
    def find_ecosystem_opportunities(
        self,
        min_cluster_size: int = 3,
        min_impact: float = 0.4
    ) -> List[SecondOrderOpportunity]:
        """
        Find opportunities at the ecosystem level.
        
        Identifies clusters of related assets where intervention on one
        creates value for the entire cluster.
        """
        opportunities = []
        
        # Find clusters
        clusters = self.graph.find_clusters(min_cluster_size)
        
        for cluster in clusters:
            # Calculate cluster health
            cluster_health = self._calculate_cluster_health(cluster)
            
            if cluster_health < 0.5:  # Unhealthy cluster = opportunity
                # Find intervention opportunities in cluster
                for node_id in cluster:
                    interventions = self.graph.get_neighbors(node_id, EdgeType.TRANSFORMED_INTO)
                    
                    for intervention_id, _, _ in interventions:
                        intervention_node = self.graph.get_node(intervention_id)
                        if intervention_node:
                            expected_value = intervention_node.properties.get("expected_value", 0)
                            
                            # Boost expected value by cluster size
                            cluster_boost = len(cluster) / 10
                            propagated_value = expected_value * (1 + cluster_boost)
                            
                            if propagated_value >= min_impact:
                                opportunity = SecondOrderOpportunity(
                                    opportunity_id=f"eco_{node_id}_{intervention_id}",
                                    source_asset=node_id,
                                    dependency_asset=node_id,
                                    intervention_target=intervention_id,
                                    opportunity_type="ecosystem_improvement",
                                    expected_value=propagated_value,
                                    propagation_factor=cluster_boost,
                                    reasoning=f"Improving {node_id} strengthens cluster of {len(cluster)} related assets",
                                    affected_dependents=cluster
                                )
                                opportunities.append(opportunity)
        
        opportunities.sort(key=lambda x: x.expected_value, reverse=True)
        
        return opportunities
    
    def _calculate_cluster_health(self, cluster: List[str]) -> float:
        """Calculate health score for a cluster."""
        if not cluster:
            return 0.0
        
        health_scores = []
        
        for node_id in cluster:
            node = self.graph.get_node(node_id)
            if node:
                quality = node.properties.get("quality", 1.0)
                is_abandoned = node.properties.get("abandoned", False)
                
                if is_abandoned:
                    health = 0.0
                else:
                    health = quality
                
                health_scores.append(health)
        
        if not health_scores:
            return 0.0
        
        return sum(health_scores) / len(health_scores)
    
    def find_bottleneck_opportunities(
        self,
        min_impact: float = 0.5
    ) -> List[SecondOrderOpportunity]:
        """
        Find bottleneck assets that block multiple downstream assets.
        
        A bottleneck is an asset that many other assets depend on.
        Improving a bottleneck creates outsized value.
        """
        opportunities = []
        
        # Find bridge nodes (bottlenecks)
        bridge_nodes = self.graph.find_bridge_nodes()
        
        for node_id in bridge_nodes:
            node = self.graph.get_node(node_id)
            if not node:
                continue
            
            # Count dependents
            dependents = self._find_dependents(node_id)
            dependent_count = len(dependents)
            
            if dependent_count < 3:  # Need significant impact
                continue
            
            # Calculate bottleneck impact
            bottleneck_impact = dependent_count / 10
            
            # Find interventions
            interventions = self.graph.get_neighbors(node_id, EdgeType.TRANSFORMED_INTO)
            
            for intervention_id, _, _ in interventions:
                intervention_node = self.graph.get_node(intervention_id)
                if intervention_node:
                    expected_value = intervention_node.properties.get("expected_value", 0)
                    propagated_value = expected_value * (1 + bottleneck_impact)
                    
                    if propagated_value >= min_impact:
                        opportunity = SecondOrderOpportunity(
                            opportunity_id=f"bot_{node_id}_{intervention_id}",
                            source_asset=node_id,
                            dependency_asset=node_id,
                            intervention_target=intervention_id,
                            opportunity_type="bottleneck_improvement",
                            expected_value=propagated_value,
                            propagation_factor=bottleneck_impact,
                            reasoning=f"{node_id} is a bottleneck for {dependent_count} dependent assets",
                            affected_dependents=dependents
                        )
                        opportunities.append(opportunity)
        
        opportunities.sort(key=lambda x: x.expected_value, reverse=True)
        
        return opportunities
    
    def find_influence_cascade_opportunities(
        self,
        min_impact: float = 0.4
    ) -> List[SecondOrderOpportunity]:
        """
        Find opportunities where intervention creates cascading value.
        
        Similar to transitive opportunities but focuses on influence paths
        rather than dependency paths.
        """
        opportunities = []
        
        for node_id in self.graph.nodes:
            node = self.graph.get_node(node_id)
            if not node:
                continue
            
            # Find influence paths
            influence_paths = self.graph.find_influence_paths(node_id, max_depth=3)
            
            for path in influence_paths:
                if len(path) < 2:
                    continue
                
                # Calculate cascade potential
                cascade_potential = len(path) / 10
                
                # Find interventions
                interventions = self.graph.get_neighbors(node_id, EdgeType.TRANSFORMED_INTO)
                
                for intervention_id, _, _ in interventions:
                    intervention_node = self.graph.get_node(intervention_id)
                    if intervention_node:
                        expected_value = intervention_node.properties.get("expected_value", 0)
                        propagated_value = expected_value * (1 + cascade_potential)
                        
                        if propagated_value >= min_impact:
                            opportunity = SecondOrderOpportunity(
                                opportunity_id=f"cas_{node_id}_{intervention_id}",
                                source_asset=node_id,
                                dependency_asset=node_id,
                                intervention_target=intervention_id,
                                opportunity_type="influence_cascade",
                                expected_value=propagated_value,
                                propagation_factor=cascade_potential,
                                reasoning=f"Intervention on {node_id} cascades through {len(path)} influence steps",
                                affected_dependents=[n[0] for n in path]
                            )
                            opportunities.append(opportunity)
        
        opportunities.sort(key=lambda x: x.expected_value, reverse=True)
        
        return opportunities
    
    def get_all_opportunities(
        self,
        min_impact: float = 0.3
    ) -> Dict[str, List[SecondOrderOpportunity]]:
        """
        Get all types of second-order opportunities.
        
        Returns:
            Dict mapping opportunity type to list of opportunities
        """
        return {
            "dependency_opportunities": self.find_dependency_opportunities(min_impact),
            "transitive_opportunities": self.find_transitive_opportunities(min_impact=min_impact),
            "ecosystem_opportunities": self.find_ecosystem_opportunities(min_impact=min_impact),
            "bottleneck_opportunities": self.find_bottleneck_opportunities(min_impact),
            "influence_cascade_opportunities": self.find_influence_cascade_opportunities(min_impact)
        }
    
    def rank_opportunities_by_impact(
        self,
        min_impact: float = 0.3
    ) -> List[SecondOrderOpportunity]:
        """
        Rank all opportunities by impact.
        
        Combines all opportunity types and sorts by expected value.
        """
        all_opportunities = []
        
        all_opportunities.extend(self.find_dependency_opportunities(min_impact))
        all_opportunities.extend(self.find_transitive_opportunities(min_impact=min_impact))
        all_opportunities.extend(self.find_ecosystem_opportunities(min_impact))
        all_opportunities.extend(self.find_bottleneck_opportunities(min_impact))
        all_opportunities.extend(self.find_influence_cascade_opportunities(min_impact))
        
        # Sort by expected value
        all_opportunities.sort(key=lambda x: x.expected_value, reverse=True)
        
        return all_opportunities
    
    def get_opportunity_summary(self, min_impact: float = 0.3) -> Dict[str, Any]:
        """Get summary of all discovered opportunities."""
        all_opportunities = self.get_all_opportunities(min_impact)
        
        total_count = sum(len(ops) for ops in all_opportunities.values())
        
        # Count by type
        type_counts = {
            op_type: len(ops)
            for op_type, ops in all_opportunities.items()
        }
        
        # Calculate average expected value
        ranked = self.rank_opportunities_by_impact(min_impact)
        avg_value = sum(op.expected_value for op in ranked) / len(ranked) if ranked else 0
        
        # Get top opportunity
        top_opportunity = ranked[0] if ranked else None
        
        return {
            "total_opportunities": total_count,
            "by_type": type_counts,
            "average_expected_value": avg_value,
            "top_opportunity": top_opportunity.to_dict() if top_opportunity else None
        }
