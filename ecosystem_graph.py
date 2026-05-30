#!/usr/bin/env python3
"""
Ecosystem Graph Discovery - Analyzes relationships between software assets.

Builds a graph of:
- Dependencies (package dependencies, imports)
- Contributors (shared developers across projects)
- Topics (shared tags/categories)
- Fork relationships
- Star correlations
- Commit patterns
"""

import sqlite3
import json
import networkx as nx
from typing import Dict, List, Set, Tuple, Optional
from dataclasses import dataclass
from enum import Enum
from collections import defaultdict


class RelationshipType(Enum):
    """Types of relationships between assets."""
    DEPENDENCY = "dependency"
    CONTRIBUTOR = "contributor"
    TOPIC = "topic"
    FORK = "fork"
    STAR_CORRELATION = "star_correlation"
    COMMIT_PATTERN = "commit_pattern"
    SIMILARITY = "similarity"


@dataclass
class AssetNode:
    """Node representing a software asset."""
    asset_id: str
    asset_type: str
    name: str
    stars: int
    forks: int
    contributors: int
    topics: List[str]
    language: str


@dataclass
class RelationshipEdge:
    """Edge representing a relationship between assets."""
    source: str
    target: str
    relationship_type: RelationshipType
    weight: float
    metadata: Dict


class EcosystemGraph:
    """Graph-based discovery of asset relationships."""
    
    def __init__(self, db_path: str = "outcome_ledger.db"):
        self.db_path = db_path
        self.graph = nx.DiGraph()
        self.assets: Dict[str, AssetNode] = {}
        self.relationships: List[RelationshipEdge] = []
        
    def load_assets_from_ledger(self) -> List[AssetNode]:
        """Load assets from the outcome ledger."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT DISTINCT 
                asset_id,
                asset_type,
                asset_name,
                before_state
            FROM interventions
            WHERE before_state IS NOT NULL
        """)
        
        rows = cursor.fetchall()
        conn.close()
        
        assets = []
        for row in rows:
            asset_id, asset_type, asset_name, before_state_json = row
            before_state = json.loads(before_state_json)
            
            asset = AssetNode(
                asset_id=asset_id,
                asset_type=asset_type,
                asset_name=asset_name,
                stars=before_state.get('stars', 0),
                forks=before_state.get('forks', 0),
                contributors=before_state.get('contributors', 0),
                topics=before_state.get('topics', []),
                language=before_state.get('language', 'Unknown')
            )
            
            assets.append(asset)
            self.assets[asset_id] = asset
            self.graph.add_node(asset_id, **asset.__dict__)
        
        return assets
    
    def discover_contributor_relationships(self, threshold: int = 1) -> List[RelationshipEdge]:
        """Discover relationships based on shared contributors."""
        # Build contributor -> assets mapping
        contributor_to_assets = defaultdict(set)
        
        for asset_id, asset in self.assets.items():
            # Simulate contributor data (in real system, would query GitHub API)
            contributors = self._get_contributors_for_asset(asset_id)
            for contributor in contributors:
                contributor_to_assets[contributor].add(asset_id)
        
        # Find shared contributors
        relationships = []
        for contributor, asset_ids in contributor_to_assets.items():
            if len(asset_ids) > 1:
                asset_list = list(asset_ids)
                for i in range(len(asset_list)):
                    for j in range(i + 1, len(asset_list)):
                        source, target = asset_list[i], asset_list[j]
                        
                        # Weight based on number of shared contributors
                        weight = 1.0 / len(asset_ids)
                        
                        edge = RelationshipEdge(
                            source=source,
                            target=target,
                            relationship_type=RelationshipType.CONTRIBUTOR,
                            weight=weight,
                            metadata={"contributor": contributor}
                        )
                        relationships.append(edge)
                        self.graph.add_edge(source, target, relationship="contributor", weight=weight)
        
        self.relationships.extend(relationships)
        return relationships
    
    def discover_topic_relationships(self) -> List[RelationshipEdge]:
        """Discover relationships based on shared topics."""
        topic_to_assets = defaultdict(set)
        
        for asset_id, asset in self.assets.items():
            for topic in asset.topics:
                topic_to_assets[topic.lower()].add(asset_id)
        
        relationships = []
        for topic, asset_ids in topic_to_assets.items():
            if len(asset_ids) > 1:
                asset_list = list(asset_ids)
                for i in range(len(asset_list)):
                    for j in range(i + 1, len(asset_list)):
                        source, target = asset_list[i], asset_list[j]
                        
                        # Weight based on topic specificity (rare topics = higher weight)
                        weight = 1.0 / len(asset_ids)
                        
                        edge = RelationshipEdge(
                            source=source,
                            target=target,
                            relationship_type=RelationshipType.TOPIC,
                            weight=weight,
                            metadata={"topic": topic}
                        )
                        relationships.append(edge)
                        self.graph.add_edge(source, target, relationship="topic", weight=weight)
        
        self.relationships.extend(relationships)
        return relationships
    
    def discover_fork_relationships(self) -> List[RelationshipEdge]:
        """Discover fork relationships between assets."""
        # In a real system, would query GitHub API for fork relationships
        # Here we simulate based on similar names and metadata
        
        relationships = []
        asset_list = list(self.assets.items())
        
        for i, (id1, asset1) in enumerate(asset_list):
            for id2, asset2 in asset_list[i+1:]:
                # Check if one might be a fork of the other
                if self._is_likely_fork(asset1, asset2):
                    # Determine direction (older -> newer)
                    if asset1.stars >= asset2.stars:
                        source, target = id1, id2
                    else:
                        source, target = id2, id1
                    
                    edge = RelationshipEdge(
                        source=source,
                        target=target,
                        relationship_type=RelationshipType.FORK,
                        weight=1.0,
                        metadata={"reason": "similar_metadata"}
                    )
                    relationships.append(edge)
                    self.graph.add_edge(source, target, relationship="fork", weight=1.0)
        
        self.relationships.extend(relationships)
        return relationships
    
    def discover_similarity_relationships(self) -> List[RelationshipEdge]:
        """Discover relationships based on asset similarity."""
        relationships = []
        asset_list = list(self.assets.items())
        
        for i, (id1, asset1) in enumerate(asset_list):
            for id2, asset2 in asset_list[i+1:]:
                similarity = self._calculate_similarity(asset1, asset2)
                
                if similarity > 0.5:  # Threshold for significant similarity
                    edge = RelationshipEdge(
                        source=id1,
                        target=id2,
                        relationship_type=RelationshipType.SIMILARITY,
                        weight=similarity,
                        metadata={"similarity_score": similarity}
                    )
                    relationships.append(edge)
                    self.graph.add_edge(id1, id2, relationship="similarity", weight=similarity)
        
        self.relationships.extend(relationships)
        return relationships
    
    def _get_contributors_for_asset(self, asset_id: str) -> Set[str]:
        """Get contributors for an asset (simulated)."""
        # In real system, would query GitHub API
        # Here we simulate based on asset_id
        base = asset_id.split('/')[0] if '/' in asset_id else asset_id
        return {f"{base}_contributor_{i}" for i in range(5)}
    
    def _is_likely_fork(self, asset1: AssetNode, asset2: AssetNode) -> bool:
        """Check if two assets are likely fork-related."""
        # Similar language
        if asset1.language != asset2.language:
            return False
        
        # Similar topics
        topic_overlap = len(set(asset1.topics) & set(asset2.topics))
        if topic_overlap < 2:
            return False
        
        # One has significantly fewer stars (likely fork)
        star_ratio = min(asset1.stars, asset2.stars) / max(asset1.stars, asset2.stars)
        if star_ratio > 0.3:  # Not a clear fork relationship
            return False
        
        return True
    
    def _calculate_similarity(self, asset1: AssetNode, asset2: AssetNode) -> float:
        """Calculate similarity score between two assets."""
        score = 0.0
        
        # Language match
        if asset1.language == asset2.language:
            score += 0.3
        
        # Topic overlap
        topic_overlap = len(set(asset1.topics) & set(asset2.topics))
        if topic_overlap > 0:
            score += 0.3 * (topic_overlap / max(len(asset1.topics), len(asset2.topics)))
        
        # Similar star count (log scale)
        if asset1.stars > 0 and asset2.stars > 0:
            log_stars1 = np.log(asset1.stars + 1)
            log_stars2 = np.log(asset2.stars + 1)
            star_similarity = 1 - abs(log_stars1 - log_stars2) / max(log_stars1, log_stars2)
            score += 0.2 * star_similarity
        
        # Similar contributor count
        if asset1.contributors > 0 and asset2.contributors > 0:
            contrib_similarity = 1 - abs(asset1.contributors - asset2.contributors) / max(asset1.contributors, asset2.contributors)
            score += 0.2 * contrib_similarity
        
        return min(score, 1.0)
    
    def get_related_assets(self, asset_id: str, 
                          relationship_types: Optional[List[RelationshipType]] = None,
                          max_depth: int = 2) -> Dict[str, List[str]]:
        """Get assets related to a given asset."""
        if asset_id not in self.graph:
            return {}
        
        related = defaultdict(set)
        
        # BFS to find related assets
        visited = {asset_id}
        queue = [(asset_id, 0)]
        
        while queue:
            current, depth = queue.pop(0)
            
            if depth >= max_depth:
                continue
            
            for neighbor in self.graph.neighbors(current):
                if neighbor in visited:
                    continue
                
                visited.add(neighbor)
                edge_data = self.graph.get_edge_data(current, neighbor)
                rel_type = edge_data.get('relationship', 'unknown')
                
                if relationship_types is None or rel_type in [rt.value for rt in relationship_types]:
                    related[rel_type].add(neighbor)
                    queue.append((neighbor, depth + 1))
        
        return {k: list(v) for k, v in related.items()}
    
    def get_central_assets(self, top_n: int = 10) -> List[Tuple[str, float]]:
        """Get most central assets in the ecosystem."""
        # Calculate betweenness centrality
        centrality = nx.betweenness_centrality(self.graph)
        
        # Sort by centrality
        sorted_assets = sorted(centrality.items(), key=lambda x: x[1], reverse=True)
        
        return sorted_assets[:top_n]
    
    def get_communities(self) -> List[List[str]]:
        """Detect communities in the ecosystem graph."""
        # Use Louvain community detection
        try:
            import community as community_louvain
            communities = community_louvain.best_partition(self.graph.to_undirected())
            
            # Group by community ID
            community_groups = defaultdict(list)
            for node, comm_id in communities.items():
                community_groups[comm_id].append(node)
            
            return list(community_groups.values())
        except ImportError:
            # Fallback to connected components
            return [list(c) for c in nx.connected_components(self.graph.to_undirected())]
    
    def get_graph_stats(self) -> Dict:
        """Get statistics about the ecosystem graph."""
        return {
            "num_nodes": self.graph.number_of_nodes(),
            "num_edges": self.graph.number_of_edges(),
            "num_relationships": len(self.relationships),
            "avg_degree": sum(dict(self.graph.degree()).values()) / max(self.graph.number_of_nodes(), 1),
            "is_connected": nx.is_connected(self.graph.to_undirected()),
            "num_components": nx.number_connected_components(self.graph.to_undirected())
        }
    
    def export_graph(self, format: str = "json") -> str:
        """Export graph in specified format."""
        if format == "json":
            data = nx.node_link_data(self.graph)
            return json.dumps(data, indent=2)
        elif format == "gexf":
            return "\n".join(nx.generate_gexf(self.graph))
        else:
            raise ValueError(f"Unsupported format: {format}")


# Singleton instance
_graph_instance = None

def get_ecosystem_graph(db_path: str = "outcome_ledger.db") -> EcosystemGraph:
    """Get singleton ecosystem graph instance."""
    global _graph_instance
    if _graph_instance is None:
        _graph_instance = EcosystemGraph(db_path)
        _graph_instance.load_assets_from_ledger()
        _graph_instance.discover_contributor_relationships()
        _graph_instance.discover_topic_relationships()
        _graph_instance.discover_fork_relationships()
        _graph_instance.discover_similarity_relationships()
    return _graph_instance


if __name__ == "__main__":
    import numpy as np
    
    # Test the ecosystem graph
    graph = get_ecosystem_graph()
    
    print(f"Graph stats: {graph.get_graph_stats()}")
    
    print(f"\nCentral assets:")
    for asset_id, centrality in graph.get_central_assets(5):
        print(f"  {asset_id}: {centrality:.3f}")
    
    print(f"\nCommunities:")
    for i, community in enumerate(graph.get_communities()[:3]):
        print(f"  Community {i}: {len(community)} assets")
    
    if graph.assets:
        sample_asset = list(graph.assets.keys())[0]
        print(f"\nRelated assets for {sample_asset}:")
        related = graph.get_related_assets(sample_asset)
        for rel_type, assets in related.items():
            print(f"  {rel_type}: {assets[:3]}")
