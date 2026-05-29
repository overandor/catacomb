"""Innovation Cluster Discovery - Detect software ecosystems and innovation patterns."""
import numpy as np
from sklearn.cluster import DBSCAN, AgglomerativeClustering
from sklearn.metrics import silhouette_score
from typing import Dict, List, Tuple, Optional
import json


class InnovationCluster:
    """Represents a cluster of related software assets."""
    
    def __init__(self, cluster_id: str, name: str, members: List[str]):
        self.cluster_id = cluster_id
        self.name = name
        self.members = members
        self.embedding = None
        self.opportunity_score = 0.0
        self.maturity_score = 0.0
        self.gap_analysis = {}
    
    def to_dict(self) -> Dict:
        return {
            "cluster_id": self.cluster_id,
            "name": self.name,
            "members": self.members,
            "member_count": len(self.members),
            "embedding": self.embedding.tolist() if self.embedding is not None else None,
            "opportunity_score": self.opportunity_score,
            "maturity_score": self.maturity_score,
            "gap_analysis": self.gap_analysis
        }


class InnovationClusterDiscovery:
    """Discover innovation clusters from asset embeddings."""
    
    def __init__(self, embedding_dim: int = 256):
        self.embedding_dim = embedding_dim
        self.clusters = {}
        self.cluster_labels = {}
    
    def discover_clusters(
        self,
        embeddings: Dict[str, np.ndarray],
        method: str = "dbscan",
        min_cluster_size: int = 3,
        similarity_threshold: float = 0.7
    ) -> Dict[str, InnovationCluster]:
        """
        Discover innovation clusters from asset embeddings.
        
        Args:
            embeddings: Dict mapping repo_id to embedding vector
            method: Clustering method ("dbscan" or "hierarchical")
            min_cluster_size: Minimum members per cluster
            similarity_threshold: Cosine similarity threshold for DBSCAN
        
        Returns:
            Dict mapping cluster_id to InnovationCluster
        """
        repo_ids = list(embeddings.keys())
        embedding_matrix = np.array([embeddings[rid] for rid in repo_ids])
        
        # Normalize embeddings for cosine similarity
        embedding_matrix = embedding_matrix / np.linalg.norm(embedding_matrix, axis=1, keepdims=True)
        
        if method == "dbscan":
            labels = self._dbscan_clustering(embedding_matrix, similarity_threshold, min_cluster_size)
        else:
            labels = self._hierarchical_clustering(embedding_matrix, min_cluster_size)
        
        # Group repos by cluster
        cluster_members = {}
        for repo_id, label in zip(repo_ids, labels):
            if label == -1:  # Noise
                continue
            if label not in cluster_members:
                cluster_members[label] = []
            cluster_members[label].append(repo_id)
        
        # Create InnovationCluster objects
        clusters = {}
        for label, members in cluster_members.items():
            if len(members) >= min_cluster_size:
                cluster_id = f"cluster_{label}"
                cluster_name = self._generate_cluster_name(members, embeddings)
                cluster = InnovationCluster(cluster_id, cluster_name, members)
                
                # Compute cluster embedding (centroid)
                member_embeddings = np.array([embeddings[m] for m in members])
                cluster.embedding = np.mean(member_embeddings, axis=0)
                
                # Compute cluster metrics
                cluster.opportunity_score = self._compute_opportunity_score(members, embeddings)
                cluster.maturity_score = self._compute_maturity_score(members, embeddings)
                
                clusters[cluster_id] = cluster
        
        self.clusters = clusters
        self.cluster_labels = dict(zip(repo_ids, labels))
        
        return clusters
    
    def _dbscan_clustering(
        self,
        embeddings: np.ndarray,
        similarity_threshold: float,
        min_samples: int
    ) -> np.ndarray:
        """DBSCAN clustering using cosine similarity."""
        # Convert similarity threshold to distance
        eps = 1 - similarity_threshold
        
        clustering = DBSCAN(eps=eps, min_samples=min_samples, metric='cosine')
        labels = clustering.fit_predict(embeddings)
        return labels
    
    def _hierarchical_clustering(
        self,
        embeddings: np.ndarray,
        min_cluster_size: int
    ) -> np.ndarray:
        """Hierarchical clustering with distance threshold."""
        # Estimate number of clusters
        n_samples = len(embeddings)
        n_clusters = max(2, n_samples // min_cluster_size)
        
        clustering = AgglomerativeClustering(
            n_clusters=n_clusters,
            metric='cosine',
            linkage='average'
        )
        labels = clustering.fit_predict(embeddings)
        return labels
    
    def _generate_cluster_name(
        self,
        members: List[str],
        embeddings: Dict[str, np.ndarray]
    ) -> str:
        """Generate a semantic name for the cluster based on member analysis."""
        # In production, this would use:
        # - Topic modeling of READMEs
        # - Common keywords in descriptions
        # - Shared dependencies
        # - Semantic analysis
        
        # For now, use a heuristic based on member count
        if len(members) >= 10:
            return f"Large Innovation Cluster ({len(members)} members)"
        elif len(members) >= 5:
            return f"Medium Innovation Cluster ({len(members)} members)"
        else:
            return f"Small Innovation Cluster ({len(members)} members)"
    
    def _compute_opportunity_score(
        self,
        members: List[str],
        embeddings: Dict[str, np.ndarray]
    ) -> float:
        """
        Compute opportunity score for a cluster.
        
        Higher score = more intervention potential.
        """
        # Factors:
        # - Cluster size (more members = larger ecosystem)
        # - Embedding diversity (more diverse = more opportunity)
        # - Average intervention potential dimension
        
        member_embeddings = np.array([embeddings[m] for m in members])
        
        # Cluster size factor
        size_factor = min(1.0, len(members) / 10.0)
        
        # Diversity factor (variance in embeddings)
        diversity_factor = np.mean(np.var(member_embeddings, axis=0))
        diversity_factor = min(1.0, diversity_factor * 10)
        
        # Intervention potential (dimension 160-191)
        intervention_dim = member_embeddings[:, 160:191]
        avg_intervention_potential = np.mean(intervention_dim)
        
        opportunity_score = (
            size_factor * 0.3 +
            diversity_factor * 0.3 +
            avg_intervention_potential * 0.4
        )
        
        return min(1.0, opportunity_score)
    
    def _compute_maturity_score(
        self,
        members: List[str],
        embeddings: Dict[str, np.ndarray]
    ) -> float:
        """
        Compute maturity score for a cluster.
        
        Higher score = more mature ecosystem.
        """
        member_embeddings = np.array([embeddings[m] for m in members])
        
        # Architecture maturity (dimension 32-63)
        arch_maturity = np.mean(member_embeddings[:, 32:63])
        
        # Ecosystem centrality (dimension 64-95)
        ecosystem_centrality = np.mean(member_embeddings[:, 64:95])
        
        # Maintainer quality (dimension 128-159)
        maintainer_quality = np.mean(member_embeddings[:, 128:159])
        
        maturity_score = (
            arch_maturity * 0.4 +
            ecosystem_centrality * 0.3 +
            maintainer_quality * 0.3
        )
        
        return min(1.0, maturity_score)
    
    def analyze_cluster_gaps(
        self,
        cluster: InnovationCluster,
        known_patterns: Dict[str, List[str]] = None
    ) -> Dict[str, List[str]]:
        """
        Analyze gaps in an innovation cluster.
        
        Identifies missing components that would complete the ecosystem.
        """
        if known_patterns is None:
            known_patterns = {
                "Software Asset Capital Markets": [
                    "GitHub Scanner Product",
                    "Developer Capitalization Dashboard",
                    "Software Asset Registry",
                    "Solana Proof Layer",
                    "Local Discovery Agent"
                ],
                "ZK Proof Systems": [
                    "ZK Compiler",
                    "ZK Verifier",
                    "ZK Prover",
                    "ZK Circuit Library"
                ],
                "AI Infrastructure": [
                    "Model Registry",
                    "Training Pipeline",
                    "Inference Engine",
                    "Monitoring System"
                ]
            }
        
        # In production, this would:
        # 1. Match cluster to known patterns
        # 2. Identify which pattern components are missing
        # 3. Suggest interventions to fill gaps
        
        # For now, return placeholder
        cluster.gap_analysis = {
            "missing_components": [],
            "suggested_interventions": [],
            "opportunity_areas": []
        }
        
        return cluster.gap_analysis
    
    def find_similar_clusters(
        self,
        target_cluster: InnovationCluster,
        top_k: int = 5
    ) -> List[Tuple[str, float]]:
        """
        Find clusters similar to a target cluster.
        
        Returns list of (cluster_id, similarity_score) tuples.
        """
        if target_cluster.embedding is None:
            return []
        
        similarities = []
        for cluster_id, cluster in self.clusters.items():
            if cluster_id == target_cluster.cluster_id:
                continue
            if cluster.embedding is None:
                continue
            
            # Cosine similarity
            similarity = np.dot(
                target_cluster.embedding,
                cluster.embedding
            ) / (
                np.linalg.norm(target_cluster.embedding) *
                np.linalg.norm(cluster.embedding)
            )
            similarities.append((cluster_id, similarity))
        
        # Sort by similarity
        similarities.sort(key=lambda x: x[1], reverse=True)
        
        return similarities[:top_k]
    
    def get_cluster_for_repo(self, repo_id: str) -> Optional[str]:
        """Get the cluster ID for a specific repository."""
        return self.cluster_labels.get(repo_id)
    
    def get_cluster_summary(self) -> Dict:
        """Get summary statistics of all clusters."""
        return {
            "total_clusters": len(self.clusters),
            "total_members": sum(len(c.members) for c in self.clusters.values()),
            "avg_cluster_size": np.mean([len(c.members) for c in self.clusters.values()]) if self.clusters else 0,
            "avg_opportunity_score": np.mean([c.opportunity_score for c in self.clusters.values()]) if self.clusters else 0,
            "avg_maturity_score": np.mean([c.maturity_score for c in self.clusters.values()]) if self.clusters else 0,
            "clusters": {cid: c.to_dict() for cid, c in self.clusters.items()}
        }
    
    def export_clusters(self, filepath: str):
        """Export clusters to JSON file."""
        data = self.get_cluster_summary()
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)
    
    def load_clusters(self, filepath: str):
        """Load clusters from JSON file."""
        with open(filepath, 'r') as f:
            data = json.load(f)
        
        self.clusters = {}
        for cluster_id, cluster_data in data["clusters"].items():
            cluster = InnovationCluster(
                cluster_id,
                cluster_data["name"],
                cluster_data["members"]
            )
            cluster.embedding = np.array(cluster_data["embedding"]) if cluster_data["embedding"] else None
            cluster.opportunity_score = cluster_data["opportunity_score"]
            cluster.maturity_score = cluster_data["maturity_score"]
            cluster.gap_analysis = cluster_data.get("gap_analysis", {})
            self.clusters[cluster_id] = cluster
        
        # Rebuild cluster_labels
        self.cluster_labels = {}
        for cluster_id, cluster in self.clusters.items():
            for member in cluster.members:
                self.cluster_labels[member] = int(cluster_id.split("_")[1])
