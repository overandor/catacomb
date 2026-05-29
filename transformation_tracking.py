"""Transformation tracking - repo → intervention → outcome → pattern."""
from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass, field
from collections import defaultdict
import statistics


@dataclass
class TransformationPattern:
    """A discovered pattern from transformations."""
    pattern_id: str
    asset_type: str
    intervention_type: str
    context: Dict[str, Any]  # Additional context (language, category, etc.)
    
    # Statistics
    sample_count: int = 0
    avg_adoption_multiplier: float = 1.0
    avg_revenue_multiplier: float = 1.0
    avg_contributor_multiplier: float = 1.0
    
    # Confidence metrics
    confidence_interval: Tuple[float, float] = (0.0, 0.0)
    success_rate: float = 0.0
    
    # Metadata
    created_at: str = field(default_factory=lambda: "")
    updated_at: str = field(default_factory=lambda: "")
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "pattern_id": self.pattern_id,
            "asset_type": self.asset_type,
            "intervention_type": self.intervention_type,
            "context": self.context,
            "sample_count": self.sample_count,
            "avg_adoption_multiplier": self.avg_adoption_multiplier,
            "avg_revenue_multiplier": self.avg_revenue_multiplier,
            "avg_contributor_multiplier": self.avg_contributor_multiplier,
            "confidence_interval": self.confidence_interval,
            "success_rate": self.success_rate,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }


class TransformationTracker:
    """
    Tracks transformations and discovers patterns.
    
    Don't track repos. Track transformations.
    
    Repo → Intervention → Outcome → Pattern
    
    Eventually:
    - Rust Library + WASM Layer = 3.8x adoption
    - Developer Tool + AI Wrapper = 0.7x adoption
    - CLI + Cloud SaaS = 8.2x revenue
    
    These become reusable laws.
    """
    
    def __init__(self):
        self.transformations: List[Dict[str, Any]] = []
        self.patterns: Dict[str, TransformationPattern] = {}
    
    def record_transformation(
        self,
        asset_id: str,
        asset_type: str,
        intervention_type: str,
        context: Dict[str, Any],
        before_metrics: Dict[str, Any],
        after_metrics: Dict[str, Any]
    ):
        """
        Record a transformation.
        
        Args:
            asset_id: ID of the asset
            asset_type: Type of asset (github_repo, npm_package, etc.)
            intervention_type: Type of intervention
            context: Additional context (language, category, etc.)
            before_metrics: Metrics before intervention (stars, downloads, revenue, contributors)
            after_metrics: Metrics after intervention
        """
        # Calculate multipliers
        stars_before = before_metrics.get("stars", 1)
        stars_after = after_metrics.get("stars", 1)
        adoption_multiplier = stars_after / stars_before if stars_before > 0 else 1.0
        
        revenue_before = before_metrics.get("revenue", 1)
        revenue_after = after_metrics.get("revenue", 1)
        revenue_multiplier = revenue_after / revenue_before if revenue_before > 0 else 1.0
        
        contributors_before = before_metrics.get("contributors", 1)
        contributors_after = after_metrics.get("contributors", 1)
        contributor_multiplier = contributors_after / contributors_before if contributors_before > 0 else 1.0
        
        transformation = {
            "asset_id": asset_id,
            "asset_type": asset_type,
            "intervention_type": intervention_type,
            "context": context,
            "before_metrics": before_metrics,
            "after_metrics": after_metrics,
            "adoption_multiplier": adoption_multiplier,
            "revenue_multiplier": revenue_multiplier,
            "contributor_multiplier": contributor_multiplier,
            "timestamp": ""
        }
        
        self.transformations.append(transformation)
        
        # Update patterns
        self._update_patterns(transformation)
    
    def _generate_pattern_key(self, asset_type: str, intervention_type: str, context: Dict[str, Any]) -> str:
        """Generate a key for pattern identification."""
        # Include key context factors
        language = context.get("language", "any")
        category = context.get("category", "any")
        
        return f"{asset_type}:{intervention_type}:{language}:{category}"
    
    def _update_patterns(self, transformation: Dict[str, Any]):
        """Update pattern statistics from a transformation."""
        key = self._generate_pattern_key(
            transformation["asset_type"],
            transformation["intervention_type"],
            transformation["context"]
        )
        
        if key not in self.patterns:
            self.patterns[key] = TransformationPattern(
                pattern_id=key,
                asset_type=transformation["asset_type"],
                intervention_type=transformation["intervention_type"],
                context=transformation["context"]
            )
        
        pattern = self.patterns[key]
        pattern.sample_count += 1
        
        # Update averages using incremental formula
        n = pattern.sample_count
        old_avg_adoption = pattern.avg_adoption_multiplier
        old_avg_revenue = pattern.avg_revenue_multiplier
        old_avg_contributor = pattern.avg_contributor_multiplier
        
        new_avg_adoption = old_avg_adoption + (transformation["adoption_multiplier"] - old_avg_adoption) / n
        new_avg_revenue = old_avg_revenue + (transformation["revenue_multiplier"] - old_avg_revenue) / n
        new_avg_contributor = old_avg_contributor + (transformation["contributor_multiplier"] - old_avg_contributor) / n
        
        pattern.avg_adoption_multiplier = new_avg_adoption
        pattern.avg_revenue_multiplier = new_avg_revenue
        pattern.avg_contributor_multiplier = new_avg_contributor
        
        # Calculate confidence interval (simple std dev)
        pattern.confidence_interval = self._calculate_confidence_interval(key)
        
        # Calculate success rate (adoption > 1.0)
        pattern.success_rate = self._calculate_success_rate(key)
    
    def _calculate_confidence_interval(self, pattern_key: str) -> Tuple[float, float]:
        """Calculate 95% confidence interval for adoption multiplier."""
        pattern = self.patterns[pattern_key]
        
        # Get all adoption multipliers for this pattern
        multipliers = [
            t["adoption_multiplier"]
            for t in self.transformations
            if self._generate_pattern_key(t["asset_type"], t["intervention_type"], t["context"]) == pattern_key
        ]
        
        if len(multipliers) < 2:
            return (0.0, 0.0)
        
        # Calculate standard deviation
        std_dev = statistics.stdev(multipliers)
        
        # 95% confidence interval
        margin_of_error = 1.96 * (std_dev / len(multipliers) ** 0.5)
        
        return (
            pattern.avg_adoption_multiplier - margin_of_error,
            pattern.avg_adoption_multiplier + margin_of_error
        )
    
    def _calculate_success_rate(self, pattern_key: str) -> float:
        """Calculate success rate (adoption > 1.0)."""
        pattern = self.patterns[pattern_key]
        
        # Get all transformations for this pattern
        transformations = [
            t for t in self.transformations
            if self._generate_pattern_key(t["asset_type"], t["intervention_type"], t["context"]) == pattern_key
        ]
        
        if not transformations:
            return 0.0
        
        successful = sum(1 for t in transformations if t["adoption_multiplier"] > 1.0)
        
        return successful / len(transformations)
    
    def get_pattern(self, asset_type: str, intervention_type: str, context: Dict[str, Any]) -> Optional[TransformationPattern]:
        """Get a specific pattern."""
        key = self._generate_pattern_key(asset_type, intervention_type, context)
        return self.patterns.get(key)
    
    def get_all_patterns(self, min_samples: int = 3) -> List[TransformationPattern]:
        """Get all patterns with minimum sample count."""
        return [
            pattern for pattern in self.patterns.values()
            if pattern.sample_count >= min_samples
        ]
    
    def get_high_impact_patterns(self, min_adoption: float = 2.0, min_samples: int = 3) -> List[TransformationPattern]:
        """Get patterns with high adoption impact."""
        return [
            pattern for pattern in self.patterns.values()
            if pattern.avg_adoption_multiplier >= min_adoption
            and pattern.sample_count >= min_samples
        ]
    
    def get_high_revenue_patterns(self, min_revenue: float = 2.0, min_samples: int = 3) -> List[TransformationPattern]:
        """Get patterns with high revenue impact."""
        return [
            pattern for pattern in self.patterns.values()
            if pattern.avg_revenue_multiplier >= min_revenue
            and pattern.sample_count >= min_samples
        ]
    
    def predict_outcome(
        self,
        asset_type: str,
        intervention_type: str,
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Predict outcome based on historical patterns.
        
        Returns:
            Dict with predicted multipliers and confidence
        """
        pattern = self.get_pattern(asset_type, intervention_type, context)
        
        if not pattern or pattern.sample_count < 3:
            return {
                "error": "Insufficient data for prediction",
                "sample_count": pattern.sample_count if pattern else 0
            }
        
        return {
            "predicted_adoption_multiplier": pattern.avg_adoption_multiplier,
            "predicted_revenue_multiplier": pattern.avg_revenue_multiplier,
            "predicted_contributor_multiplier": pattern.avg_contributor_multiplier,
            "confidence_interval": pattern.confidence_interval,
            "success_rate": pattern.success_rate,
            "sample_count": pattern.sample_count,
            "confidence": min(pattern.sample_count / 10, 1.0)  # Confidence based on sample count
        }
    
    def find_similar_patterns(
        self,
        asset_type: str,
        context: Dict[str, Any],
        threshold: float = 0.7
    ) -> List[TransformationPattern]:
        """Find patterns similar to given context."""
        similar = []
        
        for pattern in self.patterns.values():
            if pattern.asset_type != asset_type:
                continue
            
            # Simple similarity based on context overlap
            similarity = self._calculate_context_similarity(context, pattern.context)
            
            if similarity >= threshold:
                similar.append((pattern, similarity))
        
        # Sort by similarity
        similar.sort(key=lambda x: x[1], reverse=True)
        
        return [pattern for pattern, _ in similar]
    
    def _calculate_context_similarity(self, context_a: Dict[str, Any], context_b: Dict[str, Any]) -> float:
        """Calculate similarity between two contexts."""
        if not context_a or not context_b:
            return 0.0
        
        # Check key fields
        language_match = context_a.get("language") == context_b.get("language")
        category_match = context_a.get("category") == context_b.get("category")
        
        matches = sum([language_match, category_match])
        total = 2
        
        return matches / total if total > 0 else 0.0
    
    def get_reusable_laws(self, min_confidence: float = 0.8, min_samples: int = 5) -> List[Dict[str, Any]]:
        """
        Get reusable laws from transformation patterns.
        
        A "law" is a pattern with:
        - High confidence (success rate)
        - Sufficient samples
        - Clear impact
        """
        laws = []
        
        for pattern in self.patterns.values():
            if pattern.sample_count >= min_samples and pattern.success_rate >= min_confidence:
                law = {
                    "law": f"{pattern.asset_type} + {pattern.intervention_type} = {pattern.avg_adoption_multiplier:.1f}x adoption",
                    "pattern": pattern.to_dict(),
                    "strength": pattern.success_rate * pattern.sample_count / 10  # Combined metric
                }
                laws.append(law)
        
        # Sort by strength
        laws.sort(key=lambda x: x["strength"], reverse=True)
        
        return laws
    
    def export_patterns(self, filepath: str):
        """Export patterns to file."""
        import json
        data = {
            "transformations": self.transformations,
            "patterns": {key: pattern.to_dict() for key, pattern in self.patterns.items()}
        }
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)
    
    def import_patterns(self, filepath: str):
        """Import patterns from file."""
        import json
        with open(filepath, 'r') as f:
            data = json.load(f)
        
        self.transformations = data.get("transformations", [])
        
        for key, pattern_data in data.get("patterns", {}).items():
            pattern = TransformationPattern(
                pattern_id=pattern_data["pattern_id"],
                asset_type=pattern_data["asset_type"],
                intervention_type=pattern_data["intervention_type"],
                context=pattern_data["context"],
                sample_count=pattern_data["sample_count"],
                avg_adoption_multiplier=pattern_data["avg_adoption_multiplier"],
                avg_revenue_multiplier=pattern_data["avg_revenue_multiplier"],
                avg_contributor_multiplier=pattern_data["avg_contributor_multiplier"],
                confidence_interval=tuple(pattern_data["confidence_interval"]),
                success_rate=pattern_data["success_rate"],
                created_at=pattern_data["created_at"],
                updated_at=pattern_data["updated_at"]
            )
            self.patterns[key] = pattern


class PatternDiscovery:
    """Discovers high-level patterns from transformation data."""
    
    def __init__(self, tracker: TransformationTracker):
        self.tracker = tracker
    
    def discover_language_specific_patterns(self) -> Dict[str, List[TransformationPattern]]:
        """Discover patterns specific to programming languages."""
        language_patterns = defaultdict(list)
        
        for pattern in self.tracker.patterns.values():
            language = pattern.context.get("language", "unknown")
            language_patterns[language].append(pattern)
        
        return dict(language_patterns)
    
    def discover_category_specific_patterns(self) -> Dict[str, List[TransformationPattern]]:
        """Discover patterns specific to categories."""
        category_patterns = defaultdict(list)
        
        for pattern in self.tracker.patterns.values():
            category = pattern.context.get("category", "unknown")
            category_patterns[category].append(pattern)
        
        return dict(category_patterns)
    
    def discover_intervention_effectiveness(self) -> Dict[str, Dict[str, float]]:
        """Discover which interventions are most effective for each asset type."""
        effectiveness = defaultdict(lambda: defaultdict(list))
        
        for pattern in self.tracker.patterns.values():
            asset_type = pattern.asset_type
            intervention_type = pattern.intervention_type
            
            effectiveness[asset_type][intervention_type].append(pattern.avg_adoption_multiplier)
        
        # Calculate averages
        results = {}
        for asset_type, interventions in effectiveness.items():
            results[asset_type] = {}
            for intervention_type, multipliers in interventions.items():
                results[asset_type][intervention_type] = statistics.mean(multipliers)
        
        return results
    
    def find_counterintuitive_patterns(self) -> List[Dict[str, Any]]:
        """Find patterns that contradict conventional wisdom."""
        counterintuitive = []
        
        for pattern in self.tracker.patterns.values():
            # Example: complex interventions with low effort but high impact
            if pattern.avg_adoption_multiplier > 2.0 and pattern.sample_count >= 3:
                counterintuitive.append({
                    "pattern": pattern.to_dict(),
                    "insight": f"{pattern.intervention_type} unexpectedly effective for {pattern.asset_type}"
                })
        
        return counterintuitive
