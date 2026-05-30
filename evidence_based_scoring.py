#!/usr/bin/env python3
"""
Evidence-Based Scoring - Safeguards against hallucinated financeability claims.

This module implements safeguards to ensure that all scoring decisions are
backed by verifiable evidence, preventing hallucinated or inflated claims.
"""

from typing import Dict, Any, List, Optional
from dataclasses import dataclass


@dataclass
class EvidenceRequirement:
    """
    Defines evidence requirements for a scoring component.
    """
    component_name: str
    required_evidence_types: List[str]
    conservative_multiplier: float  # Score multiplier when evidence is missing
    partial_multiplier: float  # Score multiplier when evidence is partial/unverified


class EvidenceBasedScoring:
    """
    Evidence-based scoring system with safeguards against hallucinated claims.
    
    Ensures that every score has corresponding evidence and applies conservative
    penalties when evidence is missing or unverified.
    """
    
    def __init__(self):
        self.evidence_requirements = {
            "engineering_substance": EvidenceRequirement(
                component_name="engineering_substance",
                required_evidence_types=["file_count", "code_quality_score", "architecture_complexity"],
                conservative_multiplier=0.5,
                partial_multiplier=0.7,
            ),
            "execution_proof": EvidenceRequirement(
                component_name="execution_proof",
                required_evidence_types=["build_status", "test_status", "deployment_status"],
                conservative_multiplier=0.3,
                partial_multiplier=0.6,
            ),
            "originality_ownership": EvidenceRequirement(
                component_name="originality_ownership",
                required_evidence_types=["has_license", "license_type", "ownership_clarity"],
                conservative_multiplier=0.4,
                partial_multiplier=0.7,
            ),
            "security_license_cleanliness": EvidenceRequirement(
                component_name="security_license_cleanliness",
                required_evidence_types=["secrets_detected", "private_keys_detected", "vulnerable_dependencies"],
                conservative_multiplier=0.5,
                partial_multiplier=0.7,
            ),
            "market_usefulness": EvidenceRequirement(
                component_name="market_usefulness",
                required_evidence_types=["category", "buyer_categories", "adoption_signals"],
                conservative_multiplier=0.4,
                partial_multiplier=0.6,
            ),
            "liquidation_path": EvidenceRequirement(
                component_name="liquidation_path",
                required_evidence_types=["has_liquidation_route", "buyer_universe", "expected_timeline"],
                conservative_multiplier=0.3,
                partial_multiplier=0.5,
            ),
            "documentation_packaging": EvidenceRequirement(
                component_name="documentation_packaging",
                required_evidence_types=["has_documentation", "documentation_score"],
                conservative_multiplier=0.5,
                partial_multiplier=0.8,
            ),
            "revenue_adoption_proof": EvidenceRequirement(
                component_name="revenue_adoption_proof",
                required_evidence_types=["revenue_evidence", "adoption_signals"],
                conservative_multiplier=0.2,
                partial_multiplier=0.5,
            ),
        }
    
    def apply_safeguards(
        self,
        raw_scores: Dict[str, float],
        evidence: Dict[str, Any],
    ) -> Dict[str, float]:
        """
        Apply evidence-based scoring safeguards.
        
        Args:
            raw_scores: Raw scores from evaluators (0-100 scale per component)
            evidence: Evidence dictionary with verification status
        
        Returns:
            Adjusted scores with conservative penalties applied
        """
        adjusted_scores = {}
        warnings = []
        
        for component, score in raw_scores.items():
            if component not in self.evidence_requirements:
                # Unknown component - apply conservative penalty
                adjusted_scores[component] = score * 0.5
                warnings.append(f"Unknown component '{component}' - conservative penalty applied")
                continue
            
            requirement = self.evidence_requirements[component]
            component_evidence = evidence.get(component, {})
            
            # Check evidence verification status
            evidence_status = self._check_evidence_status(
                requirement.required_evidence_types,
                component_evidence,
            )
            
            if evidence_status == "verified":
                # All evidence verified - full score
                adjusted_scores[component] = score
            elif evidence_status == "partial":
                # Partial evidence - apply partial multiplier
                adjusted_scores[component] = score * requirement.partial_multiplier
                warnings.append(
                    f"Partial evidence for '{component}' - "
                    f"score reduced to {adjusted_scores[component]:.1f}"
                )
            elif evidence_status == "missing":
                # No evidence - apply conservative multiplier
                adjusted_scores[component] = score * requirement.conservative_multiplier
                warnings.append(
                    f"Missing evidence for '{component}' - "
                    f"score reduced to {adjusted_scores[component]:.1f}"
                )
            else:
                # Unknown status - apply conservative penalty
                adjusted_scores[component] = score * 0.5
                warnings.append(f"Unknown evidence status for '{component}' - conservative penalty applied")
        
        return adjusted_scores, warnings
    
    def _check_evidence_status(
        self,
        required_types: List[str],
        component_evidence: Dict[str, Any],
    ) -> str:
        """
        Check the verification status of evidence.
        
        Returns:
            "verified", "partial", or "missing"
        """
        if not component_evidence:
            return "missing"
        
        verified_count = 0
        total_count = len(required_types)
        
        for evidence_type in required_types:
            evidence_value = component_evidence.get(evidence_type)
            
            if evidence_value is None or evidence_value == "":
                continue
            
            # Check if evidence is verified
            if isinstance(evidence_value, dict):
                if evidence_value.get("verified", False):
                    verified_count += 1
            elif evidence_value:
                # Simple truthy value - count as partial
                verified_count += 0.5
        
        if verified_count == total_count:
            return "verified"
        elif verified_count > 0:
            return "partial"
        else:
            return "missing"
    
    def validate_financeability_claim(
        self,
        financeability_score: float,
        evidence: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Validate a financeability claim against evidence.
        
        Args:
            financeability_score: The claimed financeability score
            evidence: Evidence dictionary
        
        Returns:
            Validation result with status and warnings
        """
        # High financeability requires strong evidence
        if financeability_score >= 80:
            required_evidence = [
                "execution_proof",
                "originality_ownership",
                "security_license_cleanliness",
                "market_usefulness",
            ]
            
            missing = []
            for req in required_evidence:
                if req not in evidence or not evidence[req]:
                    missing.append(req)
            
            if missing:
                return {
                    "valid": False,
                    "reason": "High financeability score requires full evidence",
                    "missing_evidence": missing,
                    "adjusted_score": financeability_score * 0.6,
                }
        
        # Medium financeability requires moderate evidence
        elif financeability_score >= 60:
            required_evidence = [
                "execution_proof",
                "originality_ownership",
            ]
            
            missing = []
            for req in required_evidence:
                if req not in evidence or not evidence[req]:
                    missing.append(req)
            
            if missing:
                return {
                    "valid": False,
                    "reason": "Medium financeability score requires core evidence",
                    "missing_evidence": missing,
                    "adjusted_score": financeability_score * 0.7,
                }
        
        return {
            "valid": True,
            "reason": "Financeability score is supported by available evidence",
            "missing_evidence": [],
            "adjusted_score": financeability_score,
        }
    
    def generate_evidence_report(
        self,
        scores: Dict[str, float],
        evidence: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Generate a comprehensive evidence report.
        
        Args:
            scores: Component scores
            evidence: Evidence dictionary
        
        Returns:
            Evidence report with status for each component
        """
        report = {
            "components": {},
            "overall_evidence_quality": "unknown",
            "warnings": [],
        }
        
        verified_count = 0
        partial_count = 0
        missing_count = 0
        
        for component, score in scores.items():
            if component not in self.evidence_requirements:
                continue
            
            requirement = self.evidence_requirements[component]
            component_evidence = evidence.get(component, {})
            
            evidence_status = self._check_evidence_status(
                requirement.required_evidence_types,
                component_evidence,
            )
            
            report["components"][component] = {
                "score": score,
                "evidence_status": evidence_status,
                "required_evidence": requirement.required_evidence_types,
                "available_evidence": list(component_evidence.keys()),
            }
            
            if evidence_status == "verified":
                verified_count += 1
            elif evidence_status == "partial":
                partial_count += 1
            else:
                missing_count += 1
        
        # Determine overall evidence quality
        total = verified_count + partial_count + missing_count
        if total == 0:
            report["overall_evidence_quality"] = "unknown"
        elif verified_count == total:
            report["overall_evidence_quality"] = "high"
        elif verified_count + partial_count >= total * 0.7:
            report["overall_evidence_quality"] = "moderate"
        else:
            report["overall_evidence_quality"] = "low"
        
        if missing_count > 0:
            report["warnings"].append(f"{missing_count} components have missing evidence")
        
        if partial_count > 0:
            report["warnings"].append(f"{partial_count} components have partial evidence")
        
        return report
