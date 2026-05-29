"""Innovation Knowledge Graph - nodes: developers, repos, packages, interventions, outcomes."""
from typing import Dict, Any, List, Set, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum
import json


class NodeType(Enum):
    """Types of nodes in the knowledge graph."""
    DEVELOPER = "developer"
    REPOSITORY = "repository"
    PACKAGE = "package"
    MODEL = "model"
    DATASET = "dataset"
    COMPANY = "company"
    INTERVENTION = "intervention"
    OUTCOME = "outcome"


class EdgeType(Enum):
    """Types of edges in the knowledge graph."""
    CREATED = "created"
    FORKED = "forked"
    DEPENDS_ON = "depends_on"
    TRANSFORMED_INTO = "transformed_into"
    GENERATED = "generated"
    INSPIRED = "inspired"
    ACQUIRED = "acquired"
    CONTRIBUTED_TO = "contributed_to"
    OWNED_BY = "owned_by"
    RELATED_TO = "related_to"


@dataclass
class Node:
    """A node in the knowledge graph."""
    node_id: str
    node_type: NodeType
    properties: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "node_id": self.node_id,
            "node_type": self.node_type.value,
            "properties": self.properties
        }


@dataclass
class Edge:
    """An edge in the knowledge graph."""
    edge_id: str
    source_node_id: str
    target_node_id: str
    edge_type: EdgeType
    properties: Dict[str, Any] = field(default_factory=dict)
    weight: float = 1.0
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "edge_id": self.edge_id,
            "source_node_id": self.source_node_id,
            "target_node_id": self.target_node_id,
            "edge_type": self.edge_type.value,
            "properties": self.properties,
            "weight": self.weight
        }


class InnovationKnowledgeGraph:
    """
    Innovation Knowledge Graph.
    
    Nodes:
    - Developers
    - Repositories
    - Packages
    - Models
    - Datasets
    - Companies
    - Interventions
    - Outcomes
    
    Edges:
    - created
    - forked
    - depends_on
    - transformed_into
    - generated
    - inspired
    - acquired
    - contributed_to
    - owned_by
    - related_to
    
    Now Catacomb can discover second-order opportunities.
    
    Example:
    Repo A depends on Package B
    Package B abandoned
    Intervention on B creates value for A
    
    Most scanners never see this.
    """
    
    def __init__(self):
        self.nodes: Dict[str, Node] = {}
        self.edges: Dict[str, Edge] = {}
        self.adjacency_list: Dict[str, List[Tuple[str, EdgeType, float]]] = defaultdict(list)
    
    def add_node(self, node: Node):
        """Add a node to the graph."""
        self.nodes[node.node_id] = node
    
    def add_edge(self, edge: Edge):
        """Add an edge to the graph."""
        self.edges[edge.edge_id] = edge
        
        # Update adjacency list
        self.adjacency_list[edge.source_node_id].append(
            (edge.target_node_id, edge.edge_type, edge.weight)
        )
    
    def get_node(self, node_id: str) -> Optional[Node]:
        """Get a node by ID."""
        return self.nodes.get(node_id)
    
    def get_neighbors(
        self,
        node_id: str,
        edge_type: EdgeType = None,
        max_depth: int = 1
    ) -> List[Tuple[str, EdgeType, float]]:
        """Get neighbors of a node."""
        if node_id not in self.adjacency_list:
            return []
        
        if edge_type:
            return [
                (target, et, weight)
                for target, et, weight in self.adjacency_list[node_id]
                if et == edge_type
            ]
        
        return self.adjacency_list[node_id]
    
    def find_path(
        self,
        source_id: str,
        target_id: str,
        max_length: int = 5
    ) -> Optional[List[Tuple[str, EdgeType]]]:
        """Find a path between two nodes using BFS."""
        if source_id not in self.nodes or target_id not in self.nodes:
            return None
        
        if source_id == target_id:
            return []
        
        from collections import deque
        
        queue = deque([(source_id, [])])
        visited = {source_id}
        
        while queue:
            current, path = queue.popleft()
            
            if len(path) >= max_length:
                continue
            
            for neighbor, edge_type, _ in self.adjacency_list[current]:
                if neighbor == target_id:
                    return path + [(current, edge_type)]
                
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append((neighbor, path + [(current, edge_type)]))
        
        return None
    
    def find_second_order_opportunities(
        self,
        node_id: str,
        opportunity_threshold: float = 0.5
    ) -> List[Dict[str, Any]]:
        """
        Find second-order opportunities.
        
        Example:
        Repo A depends on Package B
        Package B abandoned
        Intervention on B creates value for A
        """
        opportunities = []
        
        # Get all dependencies
        dependencies = self.get_neighbors(node_id, EdgeType.DEPENDS_ON)
        
        for dep_id, _, _ in dependencies:
            dep_node = self.get_node(dep_id)
            if not dep_node:
                continue
            
            # Check if dependency is abandoned or has low quality
            is_abandoned = dep_node.properties.get("abandoned", False)
            quality = dep_node.properties.get("quality", 1.0)
            
            if is_abandoned or quality < 0.5:
                # This is an opportunity
                # Find interventions that could help
                interventions = self.get_neighbors(dep_id, EdgeType.TRANSFORMED_INTO)
                
                for intervention_id, _, _ in interventions:
                    intervention_node = self.get_node(intervention_id)
                    if intervention_node:
                        expected_value = intervention_node.properties.get("expected_value", 0)
                        
                        if expected_value >= opportunity_threshold:
                            opportunities.append({
                                "source_asset": node_id,
                                "dependency": dep_id,
                                "intervention": intervention_id,
                                "expected_value": expected_value,
                                "reason": "Dependency improvement creates value for dependent assets"
                            })
        
        return opportunities
    
    def find_influence_paths(
        self,
        source_id: str,
        max_depth: int = 3
    ) -> List[List[Tuple[str, EdgeType]]]:
        """Find all paths from source up to max_depth."""
        if source_id not in self.nodes:
            return []
        
        paths = []
        
        def dfs(current_id: str, path: List[Tuple[str, EdgeType]], depth: int):
            if depth >= max_depth:
                paths.append(path)
                return
            
            for neighbor, edge_type, _ in self.adjacency_list[current_id]:
                if not any(n[0] == neighbor for n in path):  # Avoid cycles
                    dfs(neighbor, path + [(current_id, edge_type)], depth + 1)
        
        dfs(source_id, [], 0)
        
        return paths
    
    def calculate_centrality(self, node_id: str) -> Dict[str, float]:
        """Calculate centrality metrics for a node."""
        if node_id not in self.nodes:
            return {}
        
        # Degree centrality
        degree = len(self.adjacency_list[node_id])
        total_nodes = len(self.nodes)
        degree_centrality = degree / total_nodes if total_nodes > 0 else 0
        
        # Betweenness centrality (simplified)
        betweenness = 0
        for source in self.nodes:
            for target in self.nodes:
                if source != target and source != node_id and target != node_id:
                    path = self.find_path(source, target)
                    if path and any(n[0] == node_id for n in path):
                        betweenness += 1
        
        betweenness_centrality = betweenness / (total_nodes * (total_nodes - 1)) if total_nodes > 1 else 0
        
        return {
            "degree_centrality": degree_centrality,
            "betweenness_centrality": betweenness_centrality
        }
    
    def find_clusters(self, min_size: int = 3) -> List[List[str]]:
        """Find clusters of connected nodes."""
        visited = set()
        clusters = []
        
        for node_id in self.nodes:
            if node_id not in visited:
                # BFS to find connected component
                cluster = []
                queue = [node_id]
                visited.add(node_id)
                
                while queue:
                    current = queue.pop(0)
                    cluster.append(current)
                    
                    for neighbor, _, _ in self.adjacency_list[current]:
                        if neighbor not in visited:
                            visited.add(neighbor)
                            queue.append(neighbor)
                
                if len(cluster) >= min_size:
                    clusters.append(cluster)
        
        return clusters
    
    def find_bridge_nodes(self) -> List[str]:
        """Find nodes that, if removed, would disconnect the graph."""
        bridges = []
        
        for node_id in self.nodes:
            # Temporarily remove node
            neighbors = self.adjacency_list[node_id]
            self.adjacency_list[node_id] = []
            
            # Check if graph becomes disconnected
            clusters = self.find_clusters(min_size=1)
            
            # Restore node
            self.adjacency_list[node_id] = neighbors
            
            # If more clusters than before, this is a bridge
            if len(clusters) > 1:
                bridges.append(node_id)
        
        return bridges
    
    def subgraph(self, node_ids: Set[str]) -> 'InnovationKnowledgeGraph':
        """Extract a subgraph containing only specified nodes."""
        subgraph = InnovationKnowledgeGraph()
        
        # Add nodes
        for node_id in node_ids:
            if node_id in self.nodes:
                subgraph.add_node(self.nodes[node_id])
        
        # Add edges
        for edge_id, edge in self.edges.items():
            if edge.source_node_id in node_ids and edge.target_node_id in node_ids:
                subgraph.add_edge(edge)
        
        return subgraph
    
    def export_to_json(self, filepath: str):
        """Export graph to JSON."""
        data = {
            "nodes": [node.to_dict() for node in self.nodes.values()],
            "edges": [edge.to_dict() for edge in self.edges.values()]
        }
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)
    
    def import_from_json(self, filepath: str):
        """Import graph from JSON."""
        with open(filepath, 'r') as f:
            data = json.load(f)
        
        for node_data in data["nodes"]:
            node = Node(
                node_id=node_data["node_id"],
                node_type=NodeType(node_data["node_type"]),
                properties=node_data["properties"]
            )
            self.add_node(node)
        
        for edge_data in data["edges"]:
            edge = Edge(
                edge_id=edge_data["edge_id"],
                source_node_id=edge_data["source_node_id"],
                target_node_id=edge_data["target_node_id"],
                edge_type=EdgeType(edge_data["edge_type"]),
                properties=edge_data["properties"],
                weight=edge_data.get("weight", 1.0)
            )
            self.add_edge(edge)


class GraphBuilder:
    """Builds the innovation knowledge graph from various sources."""
    
    def __init__(self):
        self.graph = InnovationKnowledgeGraph()
    
    def add_developer(self, developer_id: str, username: str, properties: Dict[str, Any] = None):
        """Add a developer node."""
        node = Node(
            node_id=developer_id,
            node_type=NodeType.DEVELOPER,
            properties={"username": username, **(properties or {})}
        )
        self.graph.add_node(node)
    
    def add_repository(self, repo_id: str, name: str, owner: str, properties: Dict[str, Any] = None):
        """Add a repository node."""
        node = Node(
            node_id=repo_id,
            node_type=NodeType.REPOSITORY,
            properties={"name": name, "owner": owner, **(properties or {})}
        )
        self.graph.add_node(node)
    
    def add_package(self, package_id: str, name: str, registry: str, properties: Dict[str, Any] = None):
        """Add a package node."""
        node = Node(
            node_id=package_id,
            node_type=NodeType.PACKAGE,
            properties={"name": name, "registry": registry, **(properties or {})}
        )
        self.graph.add_node(node)
    
    def add_intervention(self, intervention_id: str, intervention_type: str, properties: Dict[str, Any] = None):
        """Add an intervention node."""
        node = Node(
            node_id=intervention_id,
            node_type=NodeType.INTERVENTION,
            properties={"intervention_type": intervention_type, **(properties or {})}
        )
        self.graph.add_node(node)
    
    def add_outcome(self, outcome_id: str, properties: Dict[str, Any] = None):
        """Add an outcome node."""
        node = Node(
            node_id=outcome_id,
            node_type=NodeType.OUTCOME,
            properties=properties or {}
        )
        self.graph.add_node(node)
    
    def add_created_edge(self, developer_id: str, repo_id: str, properties: Dict[str, Any] = None):
        """Add a 'created' edge."""
        edge = Edge(
            edge_id=f"{developer_id}_created_{repo_id}",
            source_node_id=developer_id,
            target_node_id=repo_id,
            edge_type=EdgeType.CREATED,
            properties=properties or {}
        )
        self.graph.add_edge(edge)
    
    def add_depends_on_edge(self, source_id: str, target_id: str, properties: Dict[str, Any] = None):
        """Add a 'depends_on' edge."""
        edge = Edge(
            edge_id=f"{source_id}_depends_on_{target_id}",
            source_node_id=source_id,
            target_node_id=target_id,
            edge_type=EdgeType.DEPENDS_ON,
            properties=properties or {}
        )
        self.graph.add_edge(edge)
    
    def add_transformed_into_edge(self, asset_id: str, intervention_id: str, properties: Dict[str, Any] = None):
        """Add a 'transformed_into' edge."""
        edge = Edge(
            edge_id=f"{asset_id}_transformed_into_{intervention_id}",
            source_node_id=asset_id,
            target_node_id=intervention_id,
            edge_type=EdgeType.TRANSFORMED_INTO,
            properties=properties or {}
        )
        self.graph.add_edge(edge)
    
    def add_generated_edge(self, intervention_id: str, outcome_id: str, properties: Dict[str, Any] = None):
        """Add a 'generated' edge."""
        edge = Edge(
            edge_id=f"{intervention_id}_generated_{outcome_id}",
            source_node_id=intervention_id,
            target_node_id=outcome_id,
            edge_type=EdgeType.GENERATED,
            properties=properties or {}
        )
        self.graph.add_edge(edge)
    
    def build_from_outcome_ledger(self, ledger):
        """Build graph from outcome ledger data."""
        from outcome_ledger import InterventionRecord
        
        for record_id, record in ledger.records.items():
            # Add developer
            self.add_developer(
                record.developer_id,
                record.developer_username
            )
            
            # Add asset
            if record.asset_type == "github_repo":
                self.add_repository(
                    record.asset_id,
                    record.asset_name,
                    record.developer_username
                )
            elif record.asset_type in ["npm_package", "pypi_package", "crates_io_package"]:
                self.add_package(
                    record.asset_id,
                    record.asset_name,
                    record.asset_type
                )
            
            # Add intervention
            self.add_intervention(
                record_id,
                record.intervention_type,
                {
                    "predicted_value": record.predicted_value,
                    "predicted_probability": record.predicted_probability,
                    "predicted_risk": record.predicted_risk
                }
            )
            
            # Add edges
            self.add_created_edge(record.developer_id, record.asset_id)
            self.add_transformed_into_edge(record.asset_id, record_id)
            
            # If completed, add outcome
            if record.status.value == "completed" and record.outcome_metrics:
                outcome_id = f"{record_id}_outcome"
                self.add_outcome(
                    outcome_id,
                    {
                        "actual_value": record.outcome_metrics.get("actual_value", 0),
                        "success": record.outcome_metrics.get("success", False),
                        "stars_delta": record.actual_stars_delta,
                        "downloads_delta": record.actual_downloads_delta,
                        "revenue_delta": record.actual_revenue_delta,
                        "contributors_delta": record.actual_contributors_delta
                    }
                )
                self.add_generated_edge(record_id, outcome_id)
    
    def get_graph(self) -> InnovationKnowledgeGraph:
        """Get the built graph."""
        return self.graph


from collections import defaultdict
