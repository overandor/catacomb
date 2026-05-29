"""Asset abstraction layer - unified interface for all innovation assets."""
from typing import Dict, Any, List, Optional
from enum import Enum
from datetime import datetime
import numpy as np


class AssetType(Enum):
    """Types of innovation assets."""
    GITHUB_REPO = "github_repo"
    HUGGINGFACE_MODEL = "huggingface_model"
    HUGGINGFACE_DATASET = "huggingface_dataset"
    HUGGINGFACE_SPACE = "huggingface_space"
    NPM_PACKAGE = "npm_package"
    PYPI_PACKAGE = "pypi_package"
    CRATES_IO_PACKAGE = "crates_io_package"
    DOCKER_IMAGE = "docker_image"
    API = "api"
    RESEARCH_PAPER = "research_paper"
    BENCHMARK = "benchmark"
    AGENT_WORKFLOW = "agent_workflow"


class Asset:
    """Unified abstraction for all innovation assets."""
    
    def __init__(
        self,
        asset_id: str,
        asset_type: AssetType,
        name: str,
        owner: str,
        metadata: Dict[str, Any] = None
    ):
        self.asset_id = asset_id
        self.asset_type = asset_type
        self.name = name
        self.owner = owner
        self.metadata = metadata or {}
        self.genome = None  # AssetGenome instance
        self.counterfactuals = []  # List of FutureState instances
        self.current_value = 0.0
        self.expected_future_value = 0.0
        self.innovation_alpha = 0.0
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert asset to dictionary."""
        return {
            "asset_id": self.asset_id,
            "asset_type": self.asset_type.value,
            "name": self.name,
            "owner": self.owner,
            "metadata": self.metadata,
            "genome": self.genome.to_dict() if self.genome else None,
            "current_value": self.current_value,
            "expected_future_value": self.expected_future_value,
            "innovation_alpha": self.innovation_alpha
        }
    
    def calculate_innovation_alpha(self):
        """Calculate innovation alpha = Expected Future Value - Current Recognition."""
        self.innovation_alpha = self.expected_future_value - self.current_value


class AssetGenome:
    """High-dimensional representation of software creation."""
    
    def __init__(
        self,
        technical_genome: np.ndarray = None,
        economic_genome: np.ndarray = None,
        social_genome: np.ndarray = None,
        innovation_genome: np.ndarray = None
    ):
        self.technical_genome = technical_genome or np.zeros(10)
        self.economic_genome = economic_genome or np.zeros(10)
        self.social_genome = social_genome or np.zeros(10)
        self.innovation_genome = innovation_genome or np.zeros(10)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert genome to dictionary."""
        return {
            "technical_genome": self.technical_genome.tolist(),
            "economic_genome": self.economic_genome.tolist(),
            "social_genome": self.social_genome.tolist(),
            "innovation_genome": self.innovation_genome.tolist()
        }
    
    def similarity(self, other: 'AssetGenome') -> float:
        """Calculate cosine similarity between genomes."""
        combined_self = np.concatenate([
            self.technical_genome,
            self.economic_genome,
            self.social_genome,
            self.innovation_genome
        ])
        combined_other = np.concatenate([
            other.technical_genome,
            other.economic_genome,
            other.social_genome,
            other.innovation_genome
        ])
        
        # Cosine similarity
        dot_product = np.dot(combined_self, combined_other)
        norm_self = np.linalg.norm(combined_self)
        norm_other = np.linalg.norm(combined_other)
        
        if norm_self == 0 or norm_other == 0:
            return 0.0
        
        return dot_product / (norm_self * norm_other)


class FutureState:
    """A counterfactual future state of an asset."""
    
    def __init__(
        self,
        intervention: str,
        expected_value: float,
        probability: float,
        time_days: int,
        effort_days: int,
        risk: float,
        description: str = ""
    ):
        self.intervention = intervention
        self.expected_value = expected_value
        self.probability = probability
        self.time_days = time_days
        self.effort_days = effort_days
        self.risk = risk
        self.description = description
    
    def expected_return(self) -> float:
        """Calculate expected return = Expected Value × Probability."""
        return self.expected_value * self.probability
    
    def roi(self) -> float:
        """Calculate ROI = Expected Return / Effort."""
        if self.effort_days == 0:
            return 0.0
        return self.expected_return() / self.effort_days
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert future state to dictionary."""
        return {
            "intervention": self.intervention,
            "expected_value": self.expected_value,
            "probability": self.probability,
            "time_days": self.time_days,
            "effort_days": self.effort_days,
            "risk": self.risk,
            "expected_return": self.expected_return(),
            "roi": self.roi(),
            "description": self.description
        }


class AssetScanner:
    """Scans and normalizes data from different asset sources."""
    
    def __init__(self):
        self.scanners = {
            AssetType.GITHUB_REPO: self._scan_github_repo,
            AssetType.HUGGINGFACE_MODEL: self._scan_huggingface_model,
            AssetType.NPM_PACKAGE: self._scan_npm_package,
            AssetType.PYPI_PACKAGE: self._scan_pypi_package,
            AssetType.CRATES_IO_PACKAGE: self._scan_crates_io_package,
        }
    
    def scan_asset(self, asset_type: AssetType, asset_id: str) -> Optional[Asset]:
        """Scan an asset from its source."""
        scanner = self.scanners.get(asset_type)
        if not scanner:
            return None
        
        return scanner(asset_id)
    
    def _scan_github_repo(self, repo_id: str) -> Optional[Asset]:
        """Scan GitHub repository."""
        # Placeholder - would use existing repo_scanner
        owner, repo = repo_id.split("/")
        return Asset(
            asset_id=repo_id,
            asset_type=AssetType.GITHUB_REPO,
            name=repo,
            owner=owner,
            metadata={"source": "github"}
        )
    
    def _scan_huggingface_model(self, model_id: str) -> Optional[Asset]:
        """Scan HuggingFace model."""
        # Placeholder - would implement HuggingFace API integration
        owner, model = model_id.split("/")
        return Asset(
            asset_id=model_id,
            asset_type=AssetType.HUGGINGFACE_MODEL,
            name=model,
            owner=owner,
            metadata={"source": "huggingface"}
        )
    
    def _scan_npm_package(self, package_name: str) -> Optional[Asset]:
        """Scan npm package."""
        # Placeholder - would implement npm API integration
        return Asset(
            asset_id=package_name,
            asset_type=AssetType.NPM_PACKAGE,
            name=package_name,
            owner="npm",
            metadata={"source": "npm"}
        )
    
    def _scan_pypi_package(self, package_name: str) -> Optional[Asset]:
        """Scan PyPI package."""
        # Placeholder - would implement PyPI API integration
        return Asset(
            asset_id=package_name,
            asset_type=AssetType.PYPI_PACKAGE,
            name=package_name,
            owner="pypi",
            metadata={"source": "pypi"}
        )
    
    def _scan_crates_io_package(self, package_name: str) -> Optional[Asset]:
        """Scan crates.io package."""
        # Placeholder - would implement crates.io API integration
        return Asset(
            asset_id=package_name,
            asset_type=AssetType.CRATES_IO_PACKAGE,
            name=package_name,
            owner="crates",
            metadata={"source": "crates_io"}
        )


class GenomeGenerator:
    """Generates asset genomes from asset data."""
    
    def __init__(self):
        pass
    
    def generate_genome(self, asset: Asset, raw_data: Dict[str, Any]) -> AssetGenome:
        """Generate genome for an asset."""
        technical = self._generate_technical_genome(asset, raw_data)
        economic = self._generate_economic_genome(asset, raw_data)
        social = self._generate_social_genome(asset, raw_data)
        innovation = self._generate_innovation_genome(asset, raw_data)
        
        genome = AssetGenome(technical, economic, social, innovation)
        asset.genome = genome
        
        return genome
    
    def _generate_technical_genome(self, asset: Asset, raw_data: Dict[str, Any]) -> np.ndarray:
        """Generate technical genome vector."""
        # 10 dimensions: complexity, architecture, buildability, dependency_graph, 
        # language_quality, code_coverage, test_quality, ci_quality, docs_quality, maintainability
        genome = np.zeros(10)
        
        # Placeholder - would extract from raw_data
        genome[0] = raw_data.get("complexity", 0.5)
        genome[1] = raw_data.get("architecture_score", 0.5)
        genome[2] = raw_data.get("buildability", 0.5)
        genome[3] = raw_data.get("dependency_health", 0.5)
        genome[4] = raw_data.get("language_quality", 0.5)
        genome[5] = raw_data.get("code_coverage", 0.5)
        genome[6] = raw_data.get("test_quality", 0.5)
        genome[7] = raw_data.get("ci_quality", 0.5)
        genome[8] = raw_data.get("docs_quality", 0.5)
        genome[9] = raw_data.get("maintainability", 0.5)
        
        return genome
    
    def _generate_economic_genome(self, asset: Asset, raw_data: Dict[str, Any]) -> np.ndarray:
        """Generate economic genome vector."""
        # 10 dimensions: adoption, demand, monetization_vectors, replacement_cost,
        # market_size, growth_rate, revenue_potential, cost_structure, competitive_advantage, network_effects
        genome = np.zeros(10)
        
        # Placeholder - would extract from raw_data
        genome[0] = raw_data.get("adoption", 0.5)
        genome[1] = raw_data.get("demand", 0.5)
        genome[2] = raw_data.get("monetization_vectors", 0.5)
        genome[3] = raw_data.get("replacement_cost", 0.5)
        genome[4] = raw_data.get("market_size", 0.5)
        genome[5] = raw_data.get("growth_rate", 0.5)
        genome[6] = raw_data.get("revenue_potential", 0.5)
        genome[7] = raw_data.get("cost_structure", 0.5)
        genome[8] = raw_data.get("competitive_advantage", 0.5)
        genome[9] = raw_data.get("network_effects", 0.5)
        
        return genome
    
    def _generate_social_genome(self, asset: Asset, raw_data: Dict[str, Any]) -> np.ndarray:
        """Generate social genome vector."""
        # 10 dimensions: contributor_growth, maintainer_reputation, ecosystem_influence,
        # community_engagement, social_proof, trust_score, collaboration_index, influence_score,
        # network_centrality, community_health
        genome = np.zeros(10)
        
        # Placeholder - would extract from raw_data
        genome[0] = raw_data.get("contributor_growth", 0.5)
        genome[1] = raw_data.get("maintainer_reputation", 0.5)
        genome[2] = raw_data.get("ecosystem_influence", 0.5)
        genome[3] = raw_data.get("community_engagement", 0.5)
        genome[4] = raw_data.get("social_proof", 0.5)
        genome[5] = raw_data.get("trust_score", 0.5)
        genome[6] = raw_data.get("collaboration_index", 0.5)
        genome[7] = raw_data.get("influence_score", 0.5)
        genome[8] = raw_data.get("network_centrality", 0.5)
        genome[9] = raw_data.get("community_health", 0.5)
        
        return genome
    
    def _generate_innovation_genome(self, asset: Asset, raw_data: Dict[str, Any]) -> np.ndarray:
        """Generate innovation genome vector."""
        # 10 dimensions: novelty, defensibility, category_uniqueness, research_depth,
        # innovation_potential, breakthrough_score, originality, paradigm_shift, disruption_potential, future_relevance
        genome = np.zeros(10)
        
        # Placeholder - would extract from raw_data
        genome[0] = raw_data.get("novelty", 0.5)
        genome[1] = raw_data.get("defensibility", 0.5)
        genome[2] = raw_data.get("category_uniqueness", 0.5)
        genome[3] = raw_data.get("research_depth", 0.5)
        genome[4] = raw_data.get("innovation_potential", 0.5)
        genome[5] = raw_data.get("breakthrough_score", 0.5)
        genome[6] = raw_data.get("originality", 0.5)
        genome[7] = raw_data.get("paradigm_shift", 0.5)
        genome[8] = raw_data.get("disruption_potential", 0.5)
        genome[9] = raw_data.get("future_relevance", 0.5)
        
        return genome


class InnovationMarketMap:
    """Global innovation asset graph."""
    
    def __init__(self):
        self.assets: Dict[str, Asset] = {}
        self.relationships: List[Dict[str, Any]] = []
    
    def add_asset(self, asset: Asset):
        """Add an asset to the market map."""
        self.assets[asset.asset_id] = asset
    
    def add_relationship(self, asset_id_1: str, asset_id_2: str, relationship_type: str, strength: float):
        """Add a relationship between two assets."""
        self.relationships.append({
            "asset_id_1": asset_id_1,
            "asset_id_2": asset_id_2,
            "relationship_type": relationship_type,
            "strength": strength
        })
    
    def find_similar_assets(self, asset: Asset, threshold: float = 0.7) -> List[Asset]:
        """Find assets similar to given asset based on genome similarity."""
        if not asset.genome:
            return []
        
        similar = []
        for other_asset_id, other_asset in self.assets.items():
            if other_asset_id == asset.asset_id:
                continue
            if not other_asset.genome:
                continue
            
            similarity = asset.genome.similarity(other_asset.genome)
            if similarity >= threshold:
                similar.append((other_asset, similarity))
        
        # Sort by similarity
        similar.sort(key=lambda x: x[1], reverse=True)
        
        return [asset for asset, _ in similar]
    
    def find_isolated_assets(self) -> List[Asset]:
        """Find assets with no relationships (isolated)."""
        related_asset_ids = set()
        for rel in self.relationships:
            related_asset_ids.add(rel["asset_id_1"])
            related_asset_ids.add(rel["asset_id_2"])
        
        isolated = [
            asset for asset_id, asset in self.assets.items()
            if asset_id not in related_asset_ids
        ]
        
        return isolated
    
    def find_neglected_assets(self, threshold: float = 0.3) -> List[Asset]:
        """Find assets with high innovation alpha but low current recognition."""
        neglected = [
            asset for asset in self.assets.values()
            if asset.innovation_alpha > threshold
        ]
        
        # Sort by innovation alpha
        neglected.sort(key=lambda x: x.innovation_alpha, reverse=True)
        
        return neglected
    
    def find_emerging_assets(self, trajectory_threshold: float = 0.6) -> List[Asset]:
        """Find assets with accelerating trajectories."""
        # Placeholder - would use trajectory data
        emerging = []
        for asset in self.assets.values():
            if asset.genome and asset.genome.technical_genome[5] > trajectory_threshold:
                emerging.append(asset)
        
        return emerging
    
    def find_infrastructure_assets(self, threshold: float = 0.7) -> List[Asset]:
        """Find assets that are infrastructure (high dependency potential)."""
        infrastructure = []
        for asset in self.assets.values():
            if asset.genome and asset.genome.economic_genome[3] > threshold:
                infrastructure.append(asset)
        
        return infrastructure
    
    def find_ecosystem_assets(self, ecosystem_name: str) -> List[Asset]:
        """Find assets in a specific ecosystem."""
        # Placeholder - would use metadata
        return []
