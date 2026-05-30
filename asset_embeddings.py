#!/usr/bin/env python3
"""
Asset Embeddings System - Vector search for software asset similarity.

This module provides:
- Asset embedding generation from genome, state, and intervention data
- Vector similarity search across asset types
- Semantic search for interventions and opportunities
- Integration with vector database (SQLite + vector extension or numpy-based)
"""

import sqlite3
import json
import numpy as np
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field
from datetime import datetime
import hashlib
from asset_abstraction import Asset, AssetGenome, CurrentState, FutureState, InnovationAlpha


@dataclass
class AssetEmbedding:
    """
    Asset embedding with metadata.
    
    Combines:
    - Genome embedding (structural metadata)
    - State embedding (recognition, value, health)
    - Intervention embedding (future states, alpha)
    """
    asset_id: str
    asset_type: str
    
    # Embedding vectors (768-dim from sentence-transformers or custom)
    genome_embedding: np.ndarray = field(default_factory=lambda: np.zeros(768))
    state_embedding: np.ndarray = field(default_factory=lambda: np.zeros(768))
    intervention_embedding: np.ndarray = field(default_factory=lambda: np.zeros(768))
    
    # Combined embedding (weighted sum)
    combined_embedding: np.ndarray = field(default_factory=lambda: np.zeros(768))
    
    # Weights for combination
    genome_weight: float = 0.3
    state_weight: float = 0.3
    intervention_weight: float = 0.4
    
    # Timestamps
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary (embedding as list)."""
        return {
            "asset_id": self.asset_id,
            "asset_type": self.asset_type,
            "genome_embedding": self.genome_embedding.tolist(),
            "state_embedding": self.state_embedding.tolist(),
            "intervention_embedding": self.intervention_embedding.tolist(),
            "combined_embedding": self.combined_embedding.tolist(),
            "genome_weight": self.genome_weight,
            "state_weight": self.state_weight,
            "intervention_weight": self.intervention_weight,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'AssetEmbedding':
        """Create from dictionary."""
        return cls(
            asset_id=data["asset_id"],
            asset_type=data["asset_type"],
            genome_embedding=np.array(data["genome_embedding"]),
            state_embedding=np.array(data["state_embedding"]),
            intervention_embedding=np.array(data["intervention_embedding"]),
            combined_embedding=np.array(data["combined_embedding"]),
            genome_weight=data.get("genome_weight", 0.3),
            state_weight=data.get("state_weight", 0.3),
            intervention_weight=data.get("intervention_weight", 0.4),
            created_at=datetime.fromisoformat(data["created_at"]),
            updated_at=datetime.fromisoformat(data["updated_at"]),
        )


class AssetEmbeddingGenerator:
    """
    Generate embeddings from asset data.
    
    Uses feature engineering to create embeddings from:
    - Genome: language, frameworks, dependencies, community signals
    - State: recognition, value, health, ecosystem position
    - Intervention: future states, alpha, effort, probability
    """
    
    def __init__(self, embedding_dim: int = 768):
        self.embedding_dim = embedding_dim
    
    def _normalize_features(self, features: Dict[str, float]) -> np.ndarray:
        """Normalize features to [0, 1] and pad to embedding_dim."""
        # Extract values
        values = list(features.values())
        
        # Normalize to [0, 1]
        if values:
            min_val = min(values)
            max_val = max(values)
            if max_val > min_val:
                values = [(v - min_val) / (max_val - min_val) for v in values]
            else:
                values = [0.5] * len(values)
        
        # Pad or truncate to embedding_dim
        arr = np.array(values, dtype=np.float32)
        if len(arr) < self.embedding_dim:
            arr = np.pad(arr, (0, self.embedding_dim - len(arr)), 'constant')
        elif len(arr) > self.embedding_dim:
            arr = arr[:self.embedding_dim]
        
        return arr
    
    def generate_genome_embedding(self, genome: AssetGenome) -> np.ndarray:
        """Generate embedding from asset genome."""
        features = {
            # Language (one-hot encoded as numeric)
            "lang_python": 1.0 if genome.primary_language == "python" else 0.0,
            "lang_javascript": 1.0 if genome.primary_language == "javascript" else 0.0,
            "lang_typescript": 1.0 if genome.primary_language == "typescript" else 0.0,
            "lang_rust": 1.0 if genome.primary_language == "rust" else 0.0,
            "lang_go": 1.0 if genome.primary_language == "go" else 0.0,
            "lang_cpp": 1.0 if genome.primary_language == "c++" else 0.0,
            "lang_java": 1.0 if genome.primary_language == "java" else 0.0,
            "lang_other": 1.0 if genome.primary_language not in ["python", "javascript", "typescript", "rust", "go", "c++", "java"] else 0.0,
            
            # Frameworks (count)
            "framework_count": min(genome.frameworks, 10) / 10.0,
            
            # Dependencies
            "dependency_count": min(genome.dependency_count, 100) / 100.0,
            
            # Usage patterns (log-normalized)
            "monthly_downloads": np.log1p(genome.monthly_downloads) / 20.0,
            "import_count": np.log1p(genome.import_count) / 10.0,
            "citation_count": np.log1p(genome.citation_count) / 10.0,
            "fork_count": np.log1p(genome.fork_count) / 10.0,
            "star_count": np.log1p(genome.star_count) / 10.0,
            
            # Community signals
            "contributors": min(genome.contributors, 100) / 100.0,
            "maintainers": min(genome.maintainers, 10) / 10.0,
            "active_contributors_30d": min(genome.active_contributors_30d, 50) / 50.0,
            "commit_frequency_30d": min(genome.commit_frequency_30d, 100) / 100.0,
            
            # Technical metrics
            "code_quality_score": genome.code_quality_score,
            "test_coverage": genome.test_coverage,
            "documentation_coverage": genome.documentation_coverage,
            "ci_cd_configured": 1.0 if genome.ci_cd_configured else 0.0,
        }
        
        return self._normalize_features(features)
    
    def generate_state_embedding(self, state: CurrentState) -> np.ndarray:
        """Generate embedding from current state."""
        features = {
            # Recognition
            "recognition_score": state.recognition_score / 100.0,
            "global_rank": 1.0 - min(state.global_rank, 10000) / 10000.0,
            "category_rank": 1.0 - min(state.category_rank, 1000) / 1000.0,
            
            # Value
            "current_value": np.log1p(state.current_value) / 10.0,
            "utility_score": state.utility_score / 100.0,
            
            # Health
            "maintenance_health": state.maintenance_health,
            "security_health": state.security_health,
            "stability_score": state.stability_score,
            
            # Ecosystem
            "transitive_users": np.log1p(state.transitive_users) / 10.0,
            "downstream_revenue_exposure": np.log1p(state.downstream_revenue_exposure) / 10.0,
        }
        
        return self._normalize_features(features)
    
    def generate_intervention_embedding(self, future_states: List[FutureState], alpha: Optional[InnovationAlpha]) -> np.ndarray:
        """Generate embedding from future states and alpha."""
        if not future_states:
            return np.zeros(self.embedding_dim)
        
        # Aggregate across all future states
        total_value_delta = sum(fs.value_delta for fs in future_states)
        avg_value_per_day = np.mean([fs.value_per_day for fs in future_states])
        total_engineering_days = sum(fs.engineering_days for fs in future_states)
        avg_success_probability = np.mean([fs.success_probability for fs in future_states])
        avg_risk_score = np.mean([fs.risk_score for fs in future_states])
        
        # Alpha features
        alpha_value = alpha.alpha if alpha else 0.0
        alpha_confidence = alpha.confidence if alpha else 0.0
        alpha_evidence = alpha.evidence_strength if alpha else 0.0
        
        features = {
            # Value projections
            "total_value_delta": np.log1p(abs(total_value_delta)) / 10.0,
            "avg_value_per_day": min(avg_value_per_day, 10) / 10.0,
            "total_engineering_days": min(total_engineering_days, 365) / 365.0,
            
            # Probability and risk
            "avg_success_probability": avg_success_probability,
            "avg_risk_score": avg_risk_score,
            
            # Alpha
            "alpha_value": np.tanh(alpha_value / 50.0),  # Normalize to [-1, 1]
            "alpha_confidence": alpha_confidence,
            "alpha_evidence": alpha_evidence,
            
            # Intervention count
            "intervention_count": min(len(future_states), 10) / 10.0,
        }
        
        return self._normalize_features(features)
    
    def generate_embedding(self, asset: Asset) -> AssetEmbedding:
        """Generate complete embedding for an asset."""
        genome_emb = self.generate_genome_embedding(asset.genome)
        state_emb = self.generate_state_embedding(asset.current_state)
        intervention_emb = self.generate_intervention_embedding(asset.future_states, asset.innovation_alpha)
        
        # Combined embedding (weighted sum)
        combined = (
            asset.genome_weight * genome_emb +
            asset.state_weight * state_emb +
            asset.intervention_weight * intervention_emb
        )
        
        return AssetEmbedding(
            asset_id=asset.asset_id,
            asset_type=asset.asset_type.value,
            genome_embedding=genome_emb,
            state_embedding=state_emb,
            intervention_embedding=intervention_emb,
            combined_embedding=combined,
            genome_weight=asset.genome_weight,
            state_weight=asset.state_weight,
            intervention_weight=asset.intervention_weight,
        )


class VectorDatabase:
    """
    Vector database for asset embeddings.
    
    Uses SQLite with numpy-based similarity search.
    For production, consider:
    - SQLite with vector extension (sqlite-vss)
    - Milvus, Weaviate, Qdrant
    - Pinecone (managed)
    """
    
    def __init__(self, db_path: str = "asset_embeddings.db"):
        self.db_path = db_path
        self._init_db()
    
    def _init_db(self):
        """Initialize database schema."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS embeddings (
                asset_id TEXT PRIMARY KEY,
                asset_type TEXT NOT NULL,
                genome_embedding BLOB NOT NULL,
                state_embedding BLOB NOT NULL,
                intervention_embedding BLOB NOT NULL,
                combined_embedding BLOB NOT NULL,
                genome_weight REAL DEFAULT 0.3,
                state_weight REAL DEFAULT 0.3,
                intervention_weight REAL DEFAULT 0.4,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            )
        """)
        
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_asset_type ON embeddings(asset_type)
        """)
        
        conn.commit()
        conn.close()
    
    def _serialize_embedding(self, embedding: np.ndarray) -> bytes:
        """Serialize numpy array to bytes."""
        return embedding.tobytes()
    
    def _deserialize_embedding(self, data: bytes) -> np.ndarray:
        """Deserialize bytes to numpy array."""
        return np.frombuffer(data, dtype=np.float32)
    
    def store_embedding(self, embedding: AssetEmbedding) -> None:
        """Store an embedding in the database."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT OR REPLACE INTO embeddings
            (asset_id, asset_type, genome_embedding, state_embedding, intervention_embedding,
             combined_embedding, genome_weight, state_weight, intervention_weight, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            embedding.asset_id,
            embedding.asset_type,
            self._serialize_embedding(embedding.genome_embedding),
            self._serialize_embedding(embedding.state_embedding),
            self._serialize_embedding(embedding.intervention_embedding),
            self._serialize_embedding(embedding.combined_embedding),
            embedding.genome_weight,
            embedding.state_weight,
            embedding.intervention_weight,
            embedding.created_at.isoformat(),
            embedding.updated_at.isoformat(),
        ))
        
        conn.commit()
        conn.close()
    
    def get_embedding(self, asset_id: str) -> Optional[AssetEmbedding]:
        """Retrieve an embedding by asset ID."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT * FROM embeddings WHERE asset_id = ?
        """, (asset_id,))
        
        row = cursor.fetchone()
        conn.close()
        
        if not row:
            return None
        
        return AssetEmbedding(
            asset_id=row["asset_id"],
            asset_type=row["asset_type"],
            genome_embedding=self._deserialize_embedding(row["genome_embedding"]),
            state_embedding=self._deserialize_embedding(row["state_embedding"]),
            intervention_embedding=self._deserialize_embedding(row["intervention_embedding"]),
            combined_embedding=self._deserialize_embedding(row["combined_embedding"]),
            genome_weight=row["genome_weight"],
            state_weight=row["state_weight"],
            intervention_weight=row["intervention_weight"],
            created_at=datetime.fromisoformat(row["created_at"]),
            updated_at=datetime.fromisoformat(row["updated_at"]),
        )
    
    def get_all_embeddings(self, asset_type: Optional[str] = None) -> List[AssetEmbedding]:
        """Retrieve all embeddings, optionally filtered by type."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        if asset_type:
            cursor.execute("""
                SELECT * FROM embeddings WHERE asset_type = ?
            """, (asset_type,))
        else:
            cursor.execute("SELECT * FROM embeddings")
        
        rows = cursor.fetchall()
        conn.close()
        
        return [
            AssetEmbedding(
                asset_id=row["asset_id"],
                asset_type=row["asset_type"],
                genome_embedding=self._deserialize_embedding(row["genome_embedding"]),
                state_embedding=self._deserialize_embedding(row["state_embedding"]),
                intervention_embedding=self._deserialize_embedding(row["intervention_embedding"]),
                combined_embedding=self._deserialize_embedding(row["combined_embedding"]),
                genome_weight=row["genome_weight"],
                state_weight=row["state_weight"],
                intervention_weight=row["intervention_weight"],
                created_at=datetime.fromisoformat(row["created_at"]),
                updated_at=datetime.fromisoformat(row["updated_at"]),
            )
            for row in rows
        ]
    
    def cosine_similarity(self, a: np.ndarray, b: np.ndarray) -> float:
        """Calculate cosine similarity between two vectors."""
        dot_product = np.dot(a, b)
        norm_a = np.linalg.norm(a)
        norm_b = np.linalg.norm(b)
        
        if norm_a == 0 or norm_b == 0:
            return 0.0
        
        return dot_product / (norm_a * norm_b)
    
    def search_similar(
        self,
        query_embedding: np.ndarray,
        limit: int = 10,
        asset_type: Optional[str] = None,
        min_similarity: float = 0.0
    ) -> List[Tuple[AssetEmbedding, float]]:
        """
        Search for similar assets by embedding.
        
        Returns list of (embedding, similarity_score) tuples.
        """
        embeddings = self.get_all_embeddings(asset_type)
        
        results = []
        for emb in embeddings:
            similarity = self.cosine_similarity(query_embedding, emb.combined_embedding)
            if similarity >= min_similarity:
                results.append((emb, similarity))
        
        # Sort by similarity (descending)
        results.sort(key=lambda x: x[1], reverse=True)
        
        return results[:limit]
    
    def search_by_asset(
        self,
        asset_id: str,
        limit: int = 10,
        asset_type: Optional[str] = None,
        min_similarity: float = 0.0
    ) -> List[Tuple[AssetEmbedding, float]]:
        """Search for assets similar to a given asset ID."""
        query_emb = self.get_embedding(asset_id)
        if not query_emb:
            return []
        
        return self.search_similar(
            query_emb.combined_embedding,
            limit=limit,
            asset_type=asset_type,
            min_similarity=min_similarity
        )


class AssetSearchEngine:
    """
    High-level search engine for assets using embeddings.
    
    Provides:
    - Semantic search by description
    - Similar asset discovery
    - Intervention recommendation based on similar assets
    """
    
    def __init__(self, vector_db: VectorDatabase, embedding_generator: AssetEmbeddingGenerator):
        self.vector_db = vector_db
        self.embedding_generator = embedding_generator
    
    def index_asset(self, asset: Asset) -> None:
        """Index an asset for search."""
        embedding = self.embedding_generator.generate_embedding(asset)
        self.vector_db.store_embedding(embedding)
    
    def search_similar_assets(
        self,
        asset_id: str,
        limit: int = 10,
        asset_type: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """Find assets similar to a given asset."""
        results = self.vector_db.search_by_asset(
            asset_id,
            limit=limit,
            asset_type=asset_type,
            min_similarity=0.3
        )
        
        return [
            {
                "asset_id": emb.asset_id,
                "asset_type": emb.asset_type,
                "similarity": similarity,
            }
            for emb, similarity in results
        ]
    
    def recommend_interventions(
        self,
        asset_id: str,
        limit: int = 5
    ) -> List[Dict[str, Any]]:
        """
        Recommend interventions based on similar assets.
        
        Finds assets with similar genomes and returns their
        successful interventions.
        """
        # Find similar assets
        similar = self.search_similar_assets(asset_id, limit=20)
        
        # TODO: This would need access to the actual asset data
        # to extract intervention history. For now, return
        # the similar asset IDs.
        
        return similar[:limit]
