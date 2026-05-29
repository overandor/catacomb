"""Intervention Recommender - Recommend transformation paths for software assets."""
import numpy as np
from typing import Dict, List, Tuple, Optional
from enum import Enum


class InterventionType(Enum):
    DOCUMENTATION_OVERHAUL = "documentation_overhaul"
    BUILD_SYSTEM_SETUP = "build_system_setup"
    PACKAGING_PUBLICATION = "packaging_publication"
    CI_CD_SETUP = "ci_cd_setup"
    TEST_COVERAGE = "test_coverage"
    API_DESIGN = "api_design"
    MARKETING_OUTREACH = "marketing_outreach"
    FEATURE_ADDITION = "feature_addition"
    PERFORMANCE_OPTIMIZATION = "performance_optimization"
    SECURITY_AUDIT = "security_audit"
    LICENSE_CLARIFICATION = "license_clarification"
    CONTRIBUTOR_GUIDE = "contributor_guide"
    EXAMPLES_TUTORIALS = "examples_tutorials"
    PLUGIN_ARCHITECTURE = "plugin_architecture"
    ECOSYSTEM_INTEGRATION = "ecosystem_integration"


class TransformationPath:
    """Represents a recommended intervention path."""
    
    def __init__(
        self,
        intervention_type: InterventionType,
        name: str,
        description: str,
        probability: float,
        effort_days: int,
        expected_outcome: Dict[str, float],
        risk_level: float,
        priority: float
    ):
        self.intervention_type = intervention_type
        self.name = name
        self.description = description
        self.probability = probability
        self.effort_days = effort_days
        self.expected_outcome = expected_outcome
        self.risk_level = risk_level
        self.priority = priority
    
    def to_dict(self) -> Dict:
        return {
            "intervention_type": self.intervention_type.value,
            "name": self.name,
            "description": self.description,
            "probability": self.probability,
            "effort_days": self.effort_days,
            "expected_outcome": self.expected_outcome,
            "risk_level": self.risk_level,
            "priority": self.priority,
            "roi": self.probability * self.expected_outcome.get("value_created", 0) / (self.effort_days + 1)
        }


class InterventionRecommender:
    """Recommends transformation paths based on asset genome."""
    
    def __init__(self):
        self.intervention_templates = self._init_intervention_templates()
        self.transformation_laws = {}  # Learned from historical interventions
    
    def _init_intervention_templates(self) -> Dict[InterventionType, Dict]:
        """Initialize intervention templates with base characteristics."""
        return {
            InterventionType.DOCUMENTATION_OVERHAUL: {
                "base_effort_days": 7,
                "base_probability": 0.85,
                "base_risk": 0.1,
                "expected_outcome": {
                    "adoption_delta": 0.3,
                    "contributor_delta": 0.2,
                    "ecosystem_delta": 0.1
                }
            },
            InterventionType.BUILD_SYSTEM_SETUP: {
                "base_effort_days": 5,
                "base_probability": 0.9,
                "base_risk": 0.15,
                "expected_outcome": {
                    "adoption_delta": 0.2,
                    "contributor_delta": 0.15,
                    "ecosystem_delta": 0.05
                }
            },
            InterventionType.PACKAGING_PUBLICATION: {
                "base_effort_days": 3,
                "base_probability": 0.8,
                "base_risk": 0.2,
                "expected_outcome": {
                    "adoption_delta": 0.4,
                    "contributor_delta": 0.1,
                    "ecosystem_delta": 0.2
                }
            },
            InterventionType.CI_CD_SETUP: {
                "base_effort_days": 4,
                "base_probability": 0.85,
                "base_risk": 0.1,
                "expected_outcome": {
                    "adoption_delta": 0.15,
                    "contributor_delta": 0.2,
                    "ecosystem_delta": 0.05
                }
            },
            InterventionType.TEST_COVERAGE: {
                "base_effort_days": 10,
                "base_probability": 0.75,
                "base_risk": 0.15,
                "expected_outcome": {
                    "adoption_delta": 0.2,
                    "contributor_delta": 0.15,
                    "ecosystem_delta": 0.1
                }
            },
            InterventionType.API_DESIGN: {
                "base_effort_days": 14,
                "base_probability": 0.7,
                "base_risk": 0.25,
                "expected_outcome": {
                    "adoption_delta": 0.5,
                    "contributor_delta": 0.3,
                    "ecosystem_delta": 0.3
                }
            },
            InterventionType.MARKETING_OUTREACH: {
                "base_effort_days": 5,
                "base_probability": 0.6,
                "base_risk": 0.3,
                "expected_outcome": {
                    "adoption_delta": 0.4,
                    "contributor_delta": 0.1,
                    "ecosystem_delta": 0.05
                }
            },
            InterventionType.FEATURE_ADDITION: {
                "base_effort_days": 21,
                "base_probability": 0.65,
                "base_risk": 0.35,
                "expected_outcome": {
                    "adoption_delta": 0.6,
                    "contributor_delta": 0.2,
                    "ecosystem_delta": 0.15
                }
            },
            InterventionType.PERFORMANCE_OPTIMIZATION: {
                "base_effort_days": 14,
                "base_probability": 0.75,
                "base_risk": 0.2,
                "expected_outcome": {
                    "adoption_delta": 0.3,
                    "contributor_delta": 0.15,
                    "ecosystem_delta": 0.1
                }
            },
            InterventionType.SECURITY_AUDIT: {
                "base_effort_days": 7,
                "base_probability": 0.8,
                "base_risk": 0.1,
                "expected_outcome": {
                    "adoption_delta": 0.15,
                    "contributor_delta": 0.1,
                    "ecosystem_delta": 0.05
                }
            },
            InterventionType.LICENSE_CLARIFICATION: {
                "base_effort_days": 2,
                "base_probability": 0.95,
                "base_risk": 0.05,
                "expected_outcome": {
                    "adoption_delta": 0.1,
                    "contributor_delta": 0.05,
                    "ecosystem_delta": 0.05
                }
            },
            InterventionType.CONTRIBUTOR_GUIDE: {
                "base_effort_days": 3,
                "base_probability": 0.85,
                "base_risk": 0.1,
                "expected_outcome": {
                    "adoption_delta": 0.15,
                    "contributor_delta": 0.3,
                    "ecosystem_delta": 0.1
                }
            },
            InterventionType.EXAMPLES_TUTORIALS: {
                "base_effort_days": 5,
                "base_probability": 0.8,
                "base_risk": 0.1,
                "expected_outcome": {
                    "adoption_delta": 0.35,
                    "contributor_delta": 0.2,
                    "ecosystem_delta": 0.15
                }
            },
            InterventionType.PLUGIN_ARCHITECTURE: {
                "base_effort_days": 21,
                "base_probability": 0.6,
                "base_risk": 0.4,
                "expected_outcome": {
                    "adoption_delta": 0.7,
                    "contributor_delta": 0.4,
                    "ecosystem_delta": 0.5
                }
            },
            InterventionType.ECOSYSTEM_INTEGRATION: {
                "base_effort_days": 14,
                "base_probability": 0.65,
                "base_risk": 0.3,
                "expected_outcome": {
                    "adoption_delta": 0.5,
                    "contributor_delta": 0.25,
                    "ecosystem_delta": 0.4
                }
            }
        }
    
    def recommend_interventions(
        self,
        asset_genome: Dict,
        top_k: int = 5,
        budget_days: Optional[int] = None
    ) -> List[TransformationPath]:
        """
        Recommend transformation paths for an asset.
        
        Args:
            asset_genome: Asset genome including embedding, features, etc.
            top_k: Number of top recommendations to return
            budget_days: Optional budget constraint in days
        
        Returns:
            List of TransformationPath objects sorted by priority
        """
        paths = []
        
        for intervention_type, template in self.intervention_templates.items():
            # Score this intervention for this asset
            score = self._score_intervention(asset_genome, intervention_type, template)
            
            if score > 0.3:  # Minimum threshold
                # Adjust parameters based on asset characteristics
                adjusted = self._adjust_for_asset(asset_genome, intervention_type, template)
                
                path = TransformationPath(
                    intervention_type=intervention_type,
                    name=self._generate_path_name(intervention_type, asset_genome),
                    description=self._generate_path_description(intervention_type, asset_genome),
                    probability=adjusted["probability"],
                    effort_days=adjusted["effort_days"],
                    expected_outcome=adjusted["expected_outcome"],
                    risk_level=adjusted["risk"],
                    priority=score
                )
                paths.append(path)
        
        # Sort by priority
        paths.sort(key=lambda p: p.priority, reverse=True)
        
        # Apply budget constraint if specified
        if budget_days:
            paths = self._apply_budget_constraint(paths, budget_days)
        
        return paths[:top_k]
    
    def _score_intervention(
        self,
        asset_genome: Dict,
        intervention_type: InterventionType,
        template: Dict
    ) -> float:
        """
        Score an intervention for a specific asset.
        
        Higher score = better fit.
        """
        score = 0.5  # Base score
        
        # Check asset characteristics
        has_readme = asset_genome.get("has_readme", False)
        has_ci = asset_genome.get("has_ci", False)
        has_tests = asset_genome.get("has_tests", False)
        has_package_manager = asset_genome.get("has_package_manager", False)
        has_license = asset_genome.get("license") is not None
        stars = asset_genome.get("stars", 0)
        contributors = asset_genome.get("contributors", 0)
        
        # Adjust based on intervention type
        if intervention_type == InterventionType.DOCUMENTATION_OVERHAUL:
            if not has_readme:
                score += 0.3
            if stars > 100 and not has_readme:
                score += 0.2  # High-star project without docs = high opportunity
        
        elif intervention_type == InterventionType.BUILD_SYSTEM_SETUP:
            if not has_package_manager:
                score += 0.3
            if contributors > 5 and not has_package_manager:
                score += 0.2
        
        elif intervention_type == InterventionType.PACKAGING_PUBLICATION:
            if has_package_manager and not asset_genome.get("is_published", False):
                score += 0.4
            if stars > 50 and has_package_manager:
                score += 0.2
        
        elif intervention_type == InterventionType.CI_CD_SETUP:
            if not has_ci:
                score += 0.3
            if contributors > 3 and not has_ci:
                score += 0.2
        
        elif intervention_type == InterventionType.TEST_COVERAGE:
            if not has_tests:
                score += 0.3
            if stars > 100 and not has_tests:
                score += 0.2
        
        elif intervention_type == InterventionType.API_DESIGN:
            if asset_genome.get("is_library", False):
                score += 0.3
            if stars > 200 and asset_genome.get("is_library", False):
                score += 0.2
        
        elif intervention_type == InterventionType.MARKETING_OUTREACH:
            if stars < 100 and contributors > 2:
                score += 0.3  # Good project, low visibility
            if asset_genome.get("commits_last_year", 0) > 50:
                score += 0.2
        
        elif intervention_type == InterventionType.FEATURE_ADDITION:
            if stars > 500 and contributors > 10:
                score += 0.3  # Mature project, room for growth
            if asset_genome.get("issues", 0) > 50:
                score += 0.2
        
        elif intervention_type == InterventionType.SECURITY_AUDIT:
            if stars > 1000:
                score += 0.3  # High-profile project
            if asset_genome.get("is_infrastructure", False):
                score += 0.2
        
        elif intervention_type == InterventionType.LICENSE_CLARIFICATION:
            if not has_license:
                score += 0.4
            if stars > 50 and not has_license:
                score += 0.2
        
        elif intervention_type == InterventionType.CONTRIBUTOR_GUIDE:
            if contributors > 5 and not asset_genome.get("has_contributing", False):
                score += 0.3
            if stars > 100:
                score += 0.2
        
        elif intervention_type == InterventionType.EXAMPLES_TUTORIALS:
            if asset_genome.get("is_library", False) and not asset_genome.get("has_examples", False):
                score += 0.4
            if stars > 50:
                score += 0.2
        
        elif intervention_type == InterventionType.PLUGIN_ARCHITECTURE:
            if stars > 1000 and asset_genome.get("is_framework", False):
                score += 0.3
            if asset_genome.get("is_infrastructure", False):
                score += 0.2
        
        elif intervention_type == InterventionType.ECOSYSTEM_INTEGRATION:
            if asset_genome.get("downstream_count", 0) > 10:
                score += 0.3
            if asset_genome.get("is_library", False):
                score += 0.2
        
        # Apply transformation law adjustments if available
        law_key = self._get_law_key(asset_genome, intervention_type)
        if law_key in self.transformation_laws:
            law = self.transformation_laws[law_key]
            score *= law.get("multiplier", 1.0)
        
        return min(1.0, score)
    
    def _adjust_for_asset(
        self,
        asset_genome: Dict,
        intervention_type: InterventionType,
        template: Dict
    ) -> Dict:
        """Adjust intervention parameters based on asset characteristics."""
        adjusted = template.copy()
        
        # Adjust effort based on repo size
        size_factor = min(2.0, asset_genome.get("size_kb", 0) / 10000)
        adjusted["effort_days"] = int(template["base_effort_days"] * (1 + size_factor * 0.5))
        
        # Adjust probability based on maintainer quality
        maintainer_quality = asset_genome.get("maintainer_quality", 0.5)
        adjusted["probability"] = template["base_probability"] * (0.5 + maintainer_quality)
        
        # Adjust risk based on code complexity
        complexity = asset_genome.get("code_complexity", 0.5)
        adjusted["risk"] = template["base_risk"] * (0.5 + complexity)
        
        # Scale expected outcomes based on current stars
        stars = asset_genome.get("stars", 1)
        scale_factor = min(2.0, np.log10(stars + 1) / 2)
        
        adjusted["expected_outcome"] = {
            k: v * scale_factor
            for k, v in template["expected_outcome"].items()
        }
        
        return adjusted
    
    def _generate_path_name(
        self,
        intervention_type: InterventionType,
        asset_genome: Dict
    ) -> str:
        """Generate a descriptive name for the transformation path."""
        language = asset_genome.get("language", "Unknown")
        
        names = {
            InterventionType.DOCUMENTATION_OVERHAUL: f"Comprehensive Documentation Overhaul for {language}",
            InterventionType.BUILD_SYSTEM_SETUP: f"{language} Build System Setup",
            InterventionType.PACKAGING_PUBLICATION: f"{language} Package Publication",
            InterventionType.CI_CD_SETUP: "CI/CD Pipeline Setup",
            InterventionType.TEST_COVERAGE: f"{language} Test Coverage Improvement",
            InterventionType.API_DESIGN: f"{language} API Design Refactor",
            InterventionType.MARKETING_OUTREACH: "Marketing & Outreach Campaign",
            InterventionType.FEATURE_ADDITION: "Strategic Feature Addition",
            InterventionType.PERFORMANCE_OPTIMIZATION: f"{language} Performance Optimization",
            InterventionType.SECURITY_AUDIT: "Security Audit & Hardening",
            InterventionType.LICENSE_CLARIFICATION: "License Clarification",
            InterventionType.CONTRIBUTOR_GUIDE: "Contributor Guide Creation",
            InterventionType.EXAMPLES_TUTORIALS: f"{language} Examples & Tutorials",
            InterventionType.PLUGIN_ARCHITECTURE: "Plugin Architecture Implementation",
            InterventionType.ECOSYSTEM_INTEGRATION: "Ecosystem Integration"
        }
        
        return names.get(intervention_type, intervention_type.value)
    
    def _generate_path_description(
        self,
        intervention_type: InterventionType,
        asset_genome: Dict
    ) -> str:
        """Generate a detailed description for the transformation path."""
        descriptions = {
            InterventionType.DOCUMENTATION_OVERHAUL: "Rewrite and expand documentation including API reference, tutorials, and examples",
            InterventionType.BUILD_SYSTEM_SETUP: "Implement modern build system with dependency management and automated builds",
            InterventionType.PACKAGING_PUBLICATION: "Package project for distribution and publish to appropriate package registry",
            InterventionType.CI_CD_SETUP: "Set up continuous integration and deployment pipeline with automated testing",
            InterventionType.TEST_COVERAGE: "Increase test coverage to industry standards with comprehensive test suite",
            InterventionType.API_DESIGN: "Refactor API for better usability, consistency, and developer experience",
            InterventionType.MARKETING_OUTREACH: "Execute marketing campaign to increase visibility and adoption",
            InterventionType.FEATURE_ADDITION: "Add strategic features based on user feedback and market demand",
            InterventionType.PERFORMANCE_OPTIMIZATION: "Optimize performance bottlenecks and improve resource efficiency",
            InterventionType.SECURITY_AUDIT: "Conduct security audit and implement recommended fixes",
            InterventionType.LICENSE_CLARIFICATION: "Clarify licensing terms and ensure compliance",
            InterventionType.CONTRIBUTOR_GUIDE: "Create comprehensive contributor guide and onboarding documentation",
            InterventionType.EXAMPLES_TUTORIALS: "Create practical examples and tutorials for common use cases",
            InterventionType.PLUGIN_ARCHITECTURE: "Implement plugin architecture for extensibility",
            InterventionType.ECOSYSTEM_INTEGRATION: "Integrate with existing ecosystem tools and services"
        }
        
        return descriptions.get(intervention_type, intervention_type.value)
    
    def _get_law_key(self, asset_genome: Dict, intervention_type: InterventionType) -> str:
        """Generate key for looking up transformation laws."""
        category = asset_genome.get("category", "unknown")
        language = asset_genome.get("language", "unknown")
        return f"{category}_{language}_{intervention_type.value}"
    
    def _apply_budget_constraint(
        self,
        paths: List[TransformationPath],
        budget_days: int
    ) -> List[TransformationPath]:
        """Apply budget constraint to intervention recommendations."""
        selected = []
        total_effort = 0
        
        for path in paths:
            if total_effort + path.effort_days <= budget_days:
                selected.append(path)
                total_effort += path.effort_days
        
        return selected
    
    def learn_transformation_law(
        self,
        asset_genome: Dict,
        intervention_type: InterventionType,
        actual_outcome: Dict[str, float]
    ):
        """
        Learn a transformation law from an actual intervention outcome.
        
        Updates the transformation laws database with observed multipliers.
        """
        law_key = self._get_law_key(asset_genome, intervention_type)
        
        if law_key not in self.transformation_laws:
            self.transformation_laws[law_key] = {
                "applications": 0,
                "successes": 0,
                "multiplier": 1.0,
                "confidence": 0.0
            }
        
        law = self.transformation_laws[law_key]
        law["applications"] += 1
        
        # Calculate success based on actual vs expected
        expected_value = sum(actual_outcome.values())
        if expected_value > 0.3:  # Threshold for success
            law["successes"] += 1
        
        # Update multiplier based on success rate
        if law["applications"] > 0:
            success_rate = law["successes"] / law["applications"]
            law["multiplier"] = 0.5 + success_rate  # Range 0.5-1.5
            law["confidence"] = min(1.0, law["applications"] / 10.0)
    
    def get_transformation_laws(self) -> Dict:
        """Get all learned transformation laws."""
        return self.transformation_laws
    
    def export_laws(self, filepath: str):
        """Export transformation laws to JSON."""
        import json
        with open(filepath, 'w') as f:
            json.dump(self.transformation_laws, f, indent=2)
    
    def load_laws(self, filepath: str):
        """Load transformation laws from JSON."""
        import json
        with open(filepath, 'r') as f:
            self.transformation_laws = json.load(f)
