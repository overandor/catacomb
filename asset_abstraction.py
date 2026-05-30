#!/usr/bin/env python3
"""
Asset Abstraction Layer - Unified interface for all software asset types.

This module defines the abstraction layer that treats all software assets uniformly:
- Repository
- Model
- Dataset
- API
- Research Paper
- Agent
- Prompt Corpus
- Workflow

All assets share:
- Asset ID
- Asset Type
- Asset Genome (metadata, structure, dependencies)
- Current State (metrics, recognition, usage)
- Future States (potential interventions, achievable value)
- Intervention History
- Outcome Ledger
"""

from enum import Enum
from typing import Dict, Any, List, Optional, Set
from dataclasses import dataclass, field
from datetime import datetime
import json


class AssetType(Enum):
    """Types of software assets."""
    REPOSITORY = "repository"
    MODEL = "model"
    DATASET = "dataset"
    API = "api"
    RESEARCH_PAPER = "research_paper"
    AGENT = "agent"
    PROMPT_CORPUS = "prompt_corpus"
    WORKFLOW = "workflow"


class AssetSource(Enum):
    """Sources of software assets."""
    GITHUB = "github"
    HUGGING_FACE = "hugging_face"
    ARXIV = "arxiv"
    PYPI = "pypi"
    NPM = "npm"
    CRATES_IO = "crates_io"
    CUSTOM = "custom"


@dataclass
class AssetGenome:
    """
    Asset Genome - Structural and metadata signature of an asset.
    
    The genome captures:
    - Structural properties (language, framework, architecture)
    - Dependency graph (direct and transitive dependencies)
    - Usage patterns (downloads, imports, citations)
    - Community signals (contributors, maintainers, engagement)
    - Technical metrics (code quality, test coverage, documentation)
    """
    asset_id: str
    asset_type: AssetType
    
    # Structural properties
    primary_language: str
    frameworks: List[str] = field(default_factory=list)
    architecture: str = "unknown"
    
    # Dependency graph
    direct_dependencies: List[str] = field(default_factory=list)
    transitive_dependencies: List[str] = field(default_factory=list)
    dependency_count: int = 0
    
    # Usage patterns
    monthly_downloads: int = 0
    import_count: int = 0
    citation_count: int = 0
    fork_count: int = 0
    star_count: int = 0
    
    # Community signals
    contributors: int = 0
    maintainers: int = 0
    active_contributors_30d: int = 0
    commit_frequency_30d: float = 0.0
    
    # Technical metrics
    code_quality_score: float = 0.0
    test_coverage: float = 0.0
    documentation_coverage: float = 0.0
    ci_cd_configured: bool = False
    
    # Timestamps
    created_at: Optional[datetime] = None
    last_updated: Optional[datetime] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "asset_id": self.asset_id,
            "asset_type": self.asset_type.value,
            "primary_language": self.primary_language,
            "frameworks": self.frameworks,
            "architecture": self.architecture,
            "direct_dependencies": self.direct_dependencies,
            "transitive_dependencies": self.transitive_dependencies,
            "dependency_count": self.dependency_count,
            "monthly_downloads": self.monthly_downloads,
            "import_count": self.import_count,
            "citation_count": self.citation_count,
            "fork_count": self.fork_count,
            "star_count": self.star_count,
            "contributors": self.contributors,
            "maintainers": self.maintainers,
            "active_contributors_30d": self.active_contributors_30d,
            "commit_frequency_30d": self.commit_frequency_30d,
            "code_quality_score": self.code_quality_score,
            "test_coverage": self.test_coverage,
            "documentation_coverage": self.documentation_coverage,
            "ci_cd_configured": self.ci_cd_configured,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "last_updated": self.last_updated.isoformat() if self.last_updated else None,
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'AssetGenome':
        """Create from dictionary."""
        return cls(
            asset_id=data["asset_id"],
            asset_type=AssetType(data["asset_type"]),
            primary_language=data["primary_language"],
            frameworks=data.get("frameworks", []),
            architecture=data.get("architecture", "unknown"),
            direct_dependencies=data.get("direct_dependencies", []),
            transitive_dependencies=data.get("transitive_dependencies", []),
            dependency_count=data.get("dependency_count", 0),
            monthly_downloads=data.get("monthly_downloads", 0),
            import_count=data.get("import_count", 0),
            citation_count=data.get("citation_count", 0),
            fork_count=data.get("fork_count", 0),
            star_count=data.get("star_count", 0),
            contributors=data.get("contributors", 0),
            maintainers=data.get("maintainers", 0),
            active_contributors_30d=data.get("active_contributors_30d", 0),
            commit_frequency_30d=data.get("commit_frequency_30d", 0.0),
            code_quality_score=data.get("code_quality_score", 0.0),
            test_coverage=data.get("test_coverage", 0.0),
            documentation_coverage=data.get("documentation_coverage", 0.0),
            ci_cd_configured=data.get("ci_cd_configured", False),
            created_at=datetime.fromisoformat(data["created_at"]) if data.get("created_at") else None,
            last_updated=datetime.fromisoformat(data["last_updated"]) if data.get("last_updated") else None,
        )


@dataclass
class CurrentState:
    """
    Current State of an asset - Recognition and current value.
    
    Captures:
    - Recognition metrics (stars, downloads, citations)
    - Current value (derived from recognition and utility)
    - Market position (category rank, competitive landscape)
    - Health indicators (maintenance, security, stability)
    """
    asset_id: str
    
    # Recognition metrics
    recognition_score: float = 0.0
    global_rank: int = 0
    category_rank: int = 0
    
    # Current value
    current_value: float = 0.0
    utility_score: float = 0.0
    
    # Market position
    category: str = "unknown"
    competitive_landscape: List[str] = field(default_factory=list)
    
    # Health indicators
    maintenance_health: float = 0.0  # 0-1
    security_health: float = 0.0  # 0-1
    stability_score: float = 0.0  # 0-1
    
    # Ecosystem position
    transitive_users: int = 0
    downstream_revenue_exposure: float = 0.0
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "asset_id": self.asset_id,
            "recognition_score": self.recognition_score,
            "global_rank": self.global_rank,
            "category_rank": self.category_rank,
            "current_value": self.current_value,
            "utility_score": self.utility_score,
            "category": self.category,
            "competitive_landscape": self.competitive_landscape,
            "maintenance_health": self.maintenance_health,
            "security_health": self.security_health,
            "stability_score": self.stability_score,
            "transitive_users": self.transitive_users,
            "downstream_revenue_exposure": self.downstream_revenue_exposure,
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'CurrentState':
        """Create from dictionary."""
        return cls(
            asset_id=data["asset_id"],
            recognition_score=data.get("recognition_score", 0.0),
            global_rank=data.get("global_rank", 0),
            category_rank=data.get("category_rank", 0),
            current_value=data.get("current_value", 0.0),
            utility_score=data.get("utility_score", 0.0),
            category=data.get("category", "unknown"),
            competitive_landscape=data.get("competitive_landscape", []),
            maintenance_health=data.get("maintenance_health", 0.0),
            security_health=data.get("security_health", 0.0),
            stability_score=data.get("stability_score", 0.0),
            transitive_users=data.get("transitive_users", 0),
            downstream_revenue_exposure=data.get("downstream_revenue_exposure", 0.0),
        )


@dataclass
class FutureState:
    """
    Future State of an asset - Potential after interventions.
    
    Captures:
    - Achievable value after specific interventions
    - Required effort (engineering days, cost)
    - Success probability
    - Risk factors
    - Time to achieve
    """
    asset_id: str
    intervention_type: str
    
    # Value projection
    achievable_value: float = 0.0
    value_delta: float = 0.0
    value_delta_percent: float = 0.0
    
    # Effort required
    engineering_days: int = 0
    estimated_cost: float = 0.0
    
    # Probability and risk
    success_probability: float = 0.0
    risk_score: float = 0.0
    
    # Timeframe
    time_to_achieve_days: int = 0
    
    # Value per engineering day
    value_per_day: float = 0.0
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "asset_id": self.asset_id,
            "intervention_type": self.intervention_type,
            "achievable_value": self.achievable_value,
            "value_delta": self.value_delta,
            "value_delta_percent": self.value_delta_percent,
            "engineering_days": self.engineering_days,
            "estimated_cost": self.estimated_cost,
            "success_probability": self.success_probability,
            "risk_score": self.risk_score,
            "time_to_achieve_days": self.time_to_achieve_days,
            "value_per_day": self.value_per_day,
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'FutureState':
        """Create from dictionary."""
        return cls(
            asset_id=data["asset_id"],
            intervention_type=data["intervention_type"],
            achievable_value=data.get("achievable_value", 0.0),
            value_delta=data.get("value_delta", 0.0),
            value_delta_percent=data.get("value_delta_percent", 0.0),
            engineering_days=data.get("engineering_days", 0),
            estimated_cost=data.get("estimated_cost", 0.0),
            success_probability=data.get("success_probability", 0.0),
            risk_score=data.get("risk_score", 0.0),
            time_to_achieve_days=data.get("time_to_achieve_days", 0),
            value_per_day=data.get("value_per_day", 0.0),
        )


@dataclass
class InnovationAlpha:
    """
    Innovation Alpha - The mispricing opportunity.
    
    Alpha = Expected Future Value - Current Recognition
    
    Positive alpha = undervalued (opportunity)
    Zero alpha = fairly valued
    Negative alpha = overvalued (avoid)
    """
    asset_id: str
    
    # Core alpha calculation
    expected_future_value: float = 0.0
    current_recognition: float = 0.0
    alpha: float = 0.0
    
    # Alpha breakdown
    recognition_gap: float = 0.0  # How undervalued by recognition
    utility_gap: float = 0.0  # How undervalued by utility
    ecosystem_gap: float = 0.0  # How undervalued by ecosystem position
    
    # Confidence
    confidence: float = 0.0  # 0-1
    evidence_strength: float = 0.0  # 0-1
    
    # Classification
    classification: str = "unknown"  # undervalued, fairly_valued, overvalued, hidden_gem, crowded
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "asset_id": self.asset_id,
            "expected_future_value": self.expected_future_value,
            "current_recognition": self.current_recognition,
            "alpha": self.alpha,
            "recognition_gap": self.recognition_gap,
            "utility_gap": self.utility_gap,
            "ecosystem_gap": self.ecosystem_gap,
            "confidence": self.confidence,
            "evidence_strength": self.evidence_strength,
            "classification": self.classification,
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'InnovationAlpha':
        """Create from dictionary."""
        return cls(
            asset_id=data["asset_id"],
            expected_future_value=data.get("expected_future_value", 0.0),
            current_recognition=data.get("current_recognition", 0.0),
            alpha=data.get("alpha", 0.0),
            recognition_gap=data.get("recognition_gap", 0.0),
            utility_gap=data.get("utility_gap", 0.0),
            ecosystem_gap=data.get("ecosystem_gap", 0.0),
            confidence=data.get("confidence", 0.0),
            evidence_strength=data.get("evidence_strength", 0.0),
            classification=data.get("classification", "unknown"),
        )


@dataclass
class Asset:
    """
    Unified Asset - The core abstraction for all software assets.
    
    An asset has:
    - Identity (ID, type, source)
    - Genome (structural metadata)
    - Current State (recognition, value, health)
    - Future States (potential interventions)
    - Innovation Alpha (mispricing opportunity)
    - Intervention History (past interventions and outcomes)
    """
    asset_id: str
    asset_type: AssetType
    source: AssetSource
    
    # Genome and state
    genome: AssetGenome
    current_state: CurrentState
    
    # Future states and alpha
    future_states: List[FutureState] = field(default_factory=list)
    innovation_alpha: Optional[InnovationAlpha] = None
    
    # Best intervention
    best_intervention: Optional[FutureState] = None
    
    # Timestamps
    discovered_at: datetime = field(default_factory=datetime.now)
    last_analyzed: datetime = field(default_factory=datetime.now)
    
    def calculate_innovation_alpha(self) -> InnovationAlpha:
        """
        Calculate Innovation Alpha = Expected Future Value - Current Recognition.
        
        Alpha represents the mispricing opportunity:
        - Positive alpha: undervalued (opportunity)
        - Zero alpha: fairly valued
        - Negative alpha: overvalued (avoid)
        """
        if not self.future_states:
            # No future states, no alpha
            return InnovationAlpha(
                asset_id=self.asset_id,
                expected_future_value=self.current_state.current_value,
                current_recognition=self.current_state.recognition_score,
                alpha=0.0,
                classification="fairly_valued",
                confidence=0.0,
                evidence_strength=0.0,
            )
        
        # Use the best future state (highest value per day)
        best_future = max(self.future_states, key=lambda x: x.value_per_day)
        
        expected_future_value = best_future.achievable_value
        current_recognition = self.current_state.recognition_score
        alpha = expected_future_value - current_recognition
        
        # Classification
        if alpha > 20:
            classification = "hidden_gem"
        elif alpha > 10:
            classification = "undervalued"
        elif alpha > -10:
            classification = "fairly_valued"
        elif alpha > -20:
            classification = "overvalued"
        else:
            classification = "crowded"
        
        # Confidence based on evidence strength
        evidence_strength = min(
            self.genome.contributors / 10,
            self.genome.monthly_downloads / 1000,
            1.0
        )
        
        confidence = evidence_strength * 0.8
        
        self.innovation_alpha = InnovationAlpha(
            asset_id=self.asset_id,
            expected_future_value=expected_future_value,
            current_recognition=current_recognition,
            alpha=alpha,
            recognition_gap=max(0, 100 - current_recognition),
            utility_gap=max(0, 100 - self.current_state.utility_score),
            ecosystem_gap=max(0, 100 - self.current_state.transitive_users / 100),
            confidence=confidence,
            evidence_strength=evidence_strength,
            classification=classification,
        )
        
        self.best_intervention = best_future
        
        return self.innovation_alpha
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "asset_id": self.asset_id,
            "asset_type": self.asset_type.value,
            "source": self.source.value,
            "genome": self.genome.to_dict(),
            "current_state": self.current_state.to_dict(),
            "future_states": [fs.to_dict() for fs in self.future_states],
            "innovation_alpha": self.innovation_alpha.to_dict() if self.innovation_alpha else None,
            "best_intervention": self.best_intervention.to_dict() if self.best_intervention else None,
            "discovered_at": self.discovered_at.isoformat(),
            "last_analyzed": self.last_analyzed.isoformat(),
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Asset':
        """Create from dictionary."""
        return cls(
            asset_id=data["asset_id"],
            asset_type=AssetType(data["asset_type"]),
            source=AssetSource(data["source"]),
            genome=AssetGenome.from_dict(data["genome"]),
            current_state=CurrentState.from_dict(data["current_state"]),
            future_states=[FutureState.from_dict(fs) for fs in data.get("future_states", [])],
            innovation_alpha=InnovationAlpha.from_dict(data["innovation_alpha"]) if data.get("innovation_alpha") else None,
            best_intervention=FutureState.from_dict(data["best_intervention"]) if data.get("best_intervention") else None,
            discovered_at=datetime.fromisoformat(data["discovered_at"]),
            last_analyzed=datetime.fromisoformat(data["last_analyzed"]),
        )


class AssetRegistry:
    """
    Asset Registry - Central repository for all software assets.
    
    The registry:
    - Stores all assets across types
    - Maintains asset relationships (dependencies, ecosystem graph)
    - Provides search and discovery
    - Tracks asset lifecycle
    """
    
    def __init__(self):
        self.assets: Dict[str, Asset] = {}
        self.asset_graph: Dict[str, Set[str]] = {}  # asset_id -> dependent asset_ids
        self.reverse_graph: Dict[str, Set[str]] = {}  # asset_id -> assets that depend on this
    
    def register_asset(self, asset: Asset) -> None:
        """Register an asset in the registry."""
        self.assets[asset.asset_id] = asset
        
        # Build dependency graph
        self.asset_graph[asset.asset_id] = set(asset.genome.direct_dependencies)
        
        # Build reverse graph
        for dep in asset.genome.direct_dependencies:
            if dep not in self.reverse_graph:
                self.reverse_graph[dep] = set()
            self.reverse_graph[dep].add(asset.asset_id)
    
    def get_asset(self, asset_id: str) -> Optional[Asset]:
        """Get an asset by ID."""
        return self.assets.get(asset_id)
    
    def get_downstream_assets(self, asset_id: str) -> List[Asset]:
        """Get all assets that depend on this asset."""
        downstream_ids = self.reverse_graph.get(asset_id, set())
        return [self.assets[aid] for aid in downstream_ids if aid in self.assets]
    
    def get_upstream_assets(self, asset_id: str) -> List[Asset]:
        """Get all assets this asset depends on."""
        upstream_ids = self.asset_graph.get(asset_id, set())
        return [self.assets[aid] for aid in upstream_ids if aid in self.assets]
    
    def search_by_type(self, asset_type: AssetType) -> List[Asset]:
        """Search assets by type."""
        return [asset for asset in self.assets.values() if asset.asset_type == asset_type]
    
    def search_by_alpha(self, min_alpha: float = 0.0) -> List[Asset]:
        """Search assets with innovation alpha above threshold."""
        return [
            asset for asset in self.assets.values()
            if asset.innovation_alpha and asset.innovation_alpha.alpha >= min_alpha
        ]
    
    def search_by_category(self, category: str) -> List[Asset]:
        """Search assets by category."""
        return [
            asset for asset in self.assets.values()
            if asset.current_state.category == category
        ]
    
    def get_top_alpha_assets(self, limit: int = 50) -> List[Asset]:
        """Get top assets by innovation alpha."""
        assets_with_alpha = [
            asset for asset in self.assets.values()
            if asset.innovation_alpha
        ]
        assets_with_alpha.sort(key=lambda x: x.innovation_alpha.alpha, reverse=True)
        return assets_with_alpha[:limit]
    
    def get_top_value_per_day(self, limit: int = 50) -> List[Asset]:
        """Get top assets by value per engineering day."""
        assets_with_interventions = [
            asset for asset in self.assets.values()
            if asset.best_intervention
        ]
        assets_with_interventions.sort(key=lambda x: x.best_intervention.value_per_day, reverse=True)
        return assets_with_interventions[:limit]
