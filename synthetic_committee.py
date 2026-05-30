#!/usr/bin/env python3
"""
Synthetic Committee - Professional evaluation system for software assets.

The product should not behave like one model. It should behave like a committee.
Each evaluator has a job:

- Engineering Evaluator: Determines whether the asset is real software, scaffold, prototype, or production-grade
- Execution Evaluator: Checks whether it runs, builds, tests, deploys, exposes endpoints, or produces outputs
- Security Evaluator: Flags secrets, unsafe patterns, private keys, dangerous dependencies, PII, or risky behavior
- License and Originality Evaluator: Checks license clarity, fork risk, copied code, template dependence, ownership ambiguity
- Market Evaluator: Determines who would need the asset, what category it belongs to, and whether it has buyer relevance
- Collateral Evaluator: Determines whether the asset can support a credit memo, liquidation route, monitoring plan, collateral support range
- Liquidation Evaluator: Finds the practical path to cash: sale, licensing, API, service, report, buyer outreach, broker submission
- Agent Labor Evaluator: Determines whether AI-agent work created capitalizable assets or just generated cleanup burden

This committee creates the professional atmosphere.
"""

from enum import Enum
from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass, field
from datetime import datetime
import json


class EvaluationGrade(Enum):
    """Professional evaluation grades."""
    A_PLUS = "A+"
    A = "A"
    A_MINUS = "A-"
    B_PLUS = "B+"
    B = "B"
    B_MINUS = "B-"
    C_PLUS = "C+"
    C = "C"
    C_MINUS = "C-"
    D = "D"
    F = "F"


class AssetClassification(Enum):
    """
    Asset classification layer - the root of trust.
    
    This is where most "AI valuation" tools will fail.
    The system must distinguish between these types.
    """
    REAL_PRODUCTION_SYSTEM = "real_production_system"
    WORKING_PROTOTYPE = "working_prototype"
    RESEARCH_PROTOTYPE = "research_prototype"
    INTERNAL_TOOL = "internal_tool"
    API_SERVICE = "api_service"
    FRONTEND_PRODUCT = "frontend_product"
    BACKEND_SERVICE = "backend_service"
    SMART_CONTRACT_PROTOCOL = "smart_contract_protocol"
    TRADING_ENGINE = "trading_engine"
    DATA_PIPELINE = "data_pipeline"
    HUGGING_FACE_SPACE = "hugging_face_space"
    PROMPT_SYSTEM = "prompt_system"
    AGENT_WORKFLOW = "agent_workflow"
    DOCUMENTATION_PACKAGE = "documentation_package"
    VALUATION_LEDGER = "valuation_ledger"
    PROOF_LEDGER = "proof_ledger"
    SALES_OUTREACH_TOOL = "sales_outreach_tool"
    FORK_TEMPLATE = "fork_template"
    SCAFFOLD = "scaffold"
    DUPLICATE = "duplicate"
    JUNK = "junk"
    RISK_BLOCKED = "risk_blocked"


@dataclass
class EvaluationResult:
    """Result from a single evaluator."""
    evaluator_name: str
    grade: EvaluationGrade
    score: float  # 0-100
    confidence: float  # 0-1
    findings: List[str]
    blockers: List[str]
    recommendations: List[str]
    evidence: Dict[str, Any] = field(default_factory=dict)
    evaluated_at: datetime = field(default_factory=datetime.now)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "evaluator_name": self.evaluator_name,
            "grade": self.grade.value,
            "score": self.score,
            "confidence": self.confidence,
            "findings": self.findings,
            "blockers": self.blockers,
            "recommendations": self.recommendations,
            "evidence": self.evidence,
            "evaluated_at": self.evaluated_at.isoformat(),
        }


class EngineeringEvaluator:
    """
    Engineering Evaluator - Determines asset substance.
    
    Evaluates whether the asset is:
    - Real software
    - A scaffold
    - A prototype
    - Production-grade
    """

    def __init__(self):
        self.name = "Engineering Evaluator"

    def evaluate(self, asset_data: Dict[str, Any]) -> EvaluationResult:
        """Evaluate engineering substance."""
        findings = []
        blockers = []
        recommendations = []
        evidence = {}
        
        # Extract engineering signals
        file_count = asset_data.get("file_count", 0)
        primary_language = asset_data.get("primary_language", "")
        has_tests = asset_data.get("has_tests", False)
        has_ci_cd = asset_data.get("has_ci_cd", False)
        has_documentation = asset_data.get("has_documentation", False)
        code_quality_score = asset_data.get("code_quality_score", 0)
        architecture_complexity = asset_data.get("architecture_complexity", "unknown")
        
        evidence = {
            "file_count": file_count,
            "primary_language": primary_language,
            "has_tests": has_tests,
            "has_ci_cd": has_ci_cd,
            "has_documentation": has_documentation,
            "code_quality_score": code_quality_score,
            "architecture_complexity": architecture_complexity,
        }
        
        # Score calculation
        score = 0
        
        # File count (0-20 points)
        if file_count > 50:
            score += 20
            findings.append("Substantial codebase with 50+ files")
        elif file_count > 20:
            score += 15
            findings.append("Moderate codebase with 20-50 files")
        elif file_count > 10:
            score += 10
            findings.append("Small codebase with 10-20 files")
        elif file_count > 0:
            score += 5
            findings.append("Minimal codebase with <10 files")
        else:
            blockers.append("No code files detected")
            findings.append("No code files detected - may be scaffold or empty")
        
        # Tests (0-20 points)
        if has_tests:
            score += 20
            findings.append("Test infrastructure present")
        else:
            recommendations.append("Add test suite to improve engineering grade")
            findings.append("No test infrastructure detected")
        
        # CI/CD (0-15 points)
        if has_ci_cd:
            score += 15
            findings.append("CI/CD pipeline configured")
        else:
            recommendations.append("Configure CI/CD pipeline for production readiness")
            findings.append("No CI/CD pipeline detected")
        
        # Documentation (0-15 points)
        if has_documentation:
            score += 15
            findings.append("Documentation present")
        else:
            recommendations.append("Add comprehensive documentation")
            findings.append("Limited or no documentation")
        
        # Code quality (0-30 points)
        score += code_quality_score * 0.3
        if code_quality_score > 70:
            findings.append("High code quality score")
        elif code_quality_score > 50:
            findings.append("Moderate code quality score")
        else:
            recommendations.append("Improve code quality through refactoring and linting")
            findings.append("Low code quality score")
        
        # Determine grade
        grade = self._score_to_grade(score)
        
        # Classification
        if score < 20:
            classification = AssetClassification.SCAFFOLD
        elif score < 40:
            classification = AssetClassification.RESEARCH_PROTOTYPE
        elif score < 60:
            classification = AssetClassification.WORKING_PROTOTYPE
        elif score < 80:
            classification = AssetClassification.INTERNAL_TOOL
        else:
            classification = AssetClassification.REAL_PRODUCTION_SYSTEM
        
        evidence["classification"] = classification.value
        
        return EvaluationResult(
            evaluator_name=self.name,
            grade=grade,
            score=score,
            confidence=0.85,
            findings=findings,
            blockers=blockers,
            recommendations=recommendations,
            evidence=evidence,
        )

    def _score_to_grade(self, score: float) -> EvaluationGrade:
        """Convert score to grade."""
        if score >= 90:
            return EvaluationGrade.A_PLUS
        elif score >= 85:
            return EvaluationGrade.A
        elif score >= 80:
            return EvaluationGrade.A_MINUS
        elif score >= 75:
            return EvaluationGrade.B_PLUS
        elif score >= 70:
            return EvaluationGrade.B
        elif score >= 65:
            return EvaluationGrade.B_MINUS
        elif score >= 60:
            return EvaluationGrade.C_PLUS
        elif score >= 50:
            return EvaluationGrade.C
        elif score >= 40:
            return EvaluationGrade.C_MINUS
        elif score >= 30:
            return EvaluationGrade.D
        else:
            return EvaluationGrade.F


class ExecutionEvaluator:
    """
    Execution Evaluator - Checks whether the asset actually works.
    
    Evaluates:
    - Does it build?
    - Does it run?
    - Does it produce outputs?
    - Does it expose endpoints?
    - Is it deployable?
    """

    def __init__(self):
        self.name = "Execution Evaluator"

    def evaluate(self, asset_data: Dict[str, Any]) -> EvaluationResult:
        """Evaluate execution proof."""
        findings = []
        blockers = []
        recommendations = []
        evidence = {}
        
        # Extract execution signals
        build_status = asset_data.get("build_status", "unknown")
        test_status = asset_data.get("test_status", "unknown")
        deployment_status = asset_data.get("deployment_status", "unknown")
        has_endpoints = asset_data.get("has_endpoints", False)
        has_demo = asset_data.get("has_demo", False)
        runtime_errors = asset_data.get("runtime_errors", [])
        
        evidence = {
            "build_status": build_status,
            "test_status": test_status,
            "deployment_status": deployment_status,
            "has_endpoints": has_endpoints,
            "has_demo": has_demo,
            "runtime_errors": runtime_errors,
        }
        
        score = 0
        
        # Build status (0-30 points)
        if build_status == "passed":
            score += 30
            findings.append("Build passes successfully")
        elif build_status == "failed":
            blockers.append("Build fails - asset not executable")
            findings.append("Build fails - critical blocker")
        else:
            recommendations.append("Verify build configuration")
            findings.append("Build status unknown or not tested")
        
        # Test status (0-25 points)
        if test_status == "passed":
            score += 25
            findings.append("Tests pass successfully")
        elif test_status == "failed":
            score += 10
            findings.append("Tests fail - execution risk")
            recommendations.append("Fix failing tests")
        else:
            recommendations.append("Add and run tests")
            findings.append("No test execution evidence")
        
        # Deployment status (0-25 points)
        if deployment_status == "deployed":
            score += 25
            findings.append("Asset is deployed and accessible")
        elif deployment_status == "deployable":
            score += 15
            findings.append("Asset is deployable")
            recommendations.append("Deploy to production environment")
        else:
            recommendations.append("Configure deployment pipeline")
            findings.append("No deployment evidence")
        
        # Endpoints (0-10 points)
        if has_endpoints:
            score += 10
            findings.append("API endpoints exposed")
        else:
            findings.append("No API endpoints detected")
        
        # Demo (0-10 points)
        if has_demo:
            score += 10
            findings.append("Working demo available")
        else:
            recommendations.append("Create interactive demo")
            findings.append("No demo available")
        
        # Runtime errors (penalty)
        if runtime_errors:
            error_penalty = min(20, len(runtime_errors) * 5)
            score -= error_penalty
            findings.append(f"{len(runtime_errors)} runtime errors detected")
            recommendations.append("Resolve runtime errors")
        
        score = max(0, score)
        grade = self._score_to_grade(score)
        
        return EvaluationResult(
            evaluator_name=self.name,
            grade=grade,
            score=score,
            confidence=0.9,
            findings=findings,
            blockers=blockers,
            recommendations=recommendations,
            evidence=evidence,
        )

    def _score_to_grade(self, score: float) -> EvaluationGrade:
        """Convert score to grade."""
        if score >= 90:
            return EvaluationGrade.A_PLUS
        elif score >= 80:
            return EvaluationGrade.A
        elif score >= 70:
            return EvaluationGrade.A_MINUS
        elif score >= 60:
            return EvaluationGrade.B_PLUS
        elif score >= 50:
            return EvaluationGrade.B
        elif score >= 40:
            return EvaluationGrade.B_MINUS
        elif score >= 30:
            return EvaluationGrade.C_PLUS
        elif score >= 20:
            return EvaluationGrade.C
        elif score >= 10:
            return EvaluationGrade.C_MINUS
        else:
            return EvaluationGrade.F


class SecurityEvaluator:
    """
    Security Evaluator - Flags security risks.
    
    Evaluates:
    - Secrets exposure
    - Private keys
    - Unsafe patterns
    - Dangerous dependencies
    - PII exposure
    - Risky behavior
    """

    def __init__(self):
        self.name = "Security Evaluator"

    def evaluate(self, asset_data: Dict[str, Any]) -> EvaluationResult:
        """Evaluate security posture."""
        findings = []
        blockers = []
        recommendations = []
        evidence = {}
        
        # Extract security signals
        secrets_detected = asset_data.get("secrets_detected", [])
        private_keys_detected = asset_data.get("private_keys_detected", [])
        vulnerable_dependencies = asset_data.get("vulnerable_dependencies", [])
        unsafe_patterns = asset_data.get("unsafe_patterns", [])
        pii_detected = asset_data.get("pii_detected", [])
        
        evidence = {
            "secrets_detected": secrets_detected,
            "private_keys_detected": private_keys_detected,
            "vulnerable_dependencies": vulnerable_dependencies,
            "unsafe_patterns": unsafe_patterns,
            "pii_detected": pii_detected,
        }
        
        score = 100
        
        # Secrets (critical blocker)
        if secrets_detected:
            score -= 30
            blockers.append("Secrets detected in code")
            findings.append(f"{len(secrets_detected)} secrets detected")
            recommendations.append("Remove all secrets and use environment variables")
        
        # Private keys (critical blocker)
        if private_keys_detected:
            score -= 40
            blockers.append("Private keys detected")
            findings.append(f"{len(private_keys_detected)} private keys detected")
            recommendations.append("Remove all private keys immediately")
        
        # Vulnerable dependencies
        if vulnerable_dependencies:
            vuln_penalty = min(20, len(vulnerable_dependencies) * 5)
            score -= vuln_penalty
            findings.append(f"{len(vulnerable_dependencies)} vulnerable dependencies")
            recommendations.append("Update or replace vulnerable dependencies")
        else:
            findings.append("No vulnerable dependencies detected")
        
        # Unsafe patterns
        if unsafe_patterns:
            pattern_penalty = min(15, len(unsafe_patterns) * 3)
            score -= pattern_penalty
            findings.append(f"{len(unsafe_patterns)} unsafe patterns detected")
            recommendations.append("Refactor unsafe code patterns")
        else:
            findings.append("No obvious unsafe patterns")
        
        # PII exposure
        if pii_detected:
            pii_penalty = min(10, len(pii_detected) * 2)
            score -= pii_penalty
            findings.append(f"{len(pii_detected)} potential PII exposures")
            recommendations.append("Review and secure PII handling")
        else:
            findings.append("No obvious PII exposure")
        
        score = max(0, score)
        grade = self._score_to_grade(score)
        
        # Risk block if critical issues
        if secrets_detected or private_keys_detected:
            evidence["risk_blocked"] = True
            evidence["risk_block_reason"] = "secrets_or_keys_detected"
        
        return EvaluationResult(
            evaluator_name=self.name,
            grade=grade,
            score=score,
            confidence=0.95,
            findings=findings,
            blockers=blockers,
            recommendations=recommendations,
            evidence=evidence,
        )

    def _score_to_grade(self, score: float) -> EvaluationGrade:
        """Convert score to grade."""
        if score >= 95:
            return EvaluationGrade.A_PLUS
        elif score >= 85:
            return EvaluationGrade.A
        elif score >= 75:
            return EvaluationGrade.A_MINUS
        elif score >= 65:
            return EvaluationGrade.B_PLUS
        elif score >= 55:
            return EvaluationGrade.B
        elif score >= 45:
            return EvaluationGrade.B_MINUS
        elif score >= 35:
            return EvaluationGrade.C_PLUS
        elif score >= 25:
            return EvaluationGrade.C
        elif score >= 15:
            return EvaluationGrade.C_MINUS
        else:
            return EvaluationGrade.F


class LicenseOriginalityEvaluator:
    """
    License and Originality Evaluator - Checks IP clarity.
    
    Evaluates:
    - License clarity
    - Fork risk
    - Copied code
    - Template dependence
    - Ownership ambiguity
    """

    def __init__(self):
        self.name = "License and Originality Evaluator"

    def evaluate(self, asset_data: Dict[str, Any]) -> EvaluationResult:
        """Evaluate license and originality."""
        findings = []
        blockers = []
        recommendations = []
        evidence = {}
        
        # Extract license signals
        has_license = asset_data.get("has_license", False)
        license_type = asset_data.get("license_type", "unknown")
        is_fork = asset_data.get("is_fork", False)
        fork_source = asset_data.get("fork_source", None)
        copied_code_ratio = asset_data.get("copied_code_ratio", 0)
        template_dependence = asset_data.get("template_dependence", False)
        ownership_clarity = asset_data.get("ownership_clarity", "unknown")
        
        evidence = {
            "has_license": has_license,
            "license_type": license_type,
            "is_fork": is_fork,
            "fork_source": fork_source,
            "copied_code_ratio": copied_code_ratio,
            "template_dependence": template_dependence,
            "ownership_clarity": ownership_clarity,
        }
        
        score = 0
        
        # License presence (0-30 points)
        if has_license:
            score += 30
            findings.append(f"License present: {license_type}")
            
            # License type bonus
            if license_type in ["MIT", "Apache-2.0", "BSD-3-Clause"]:
                score += 10
                findings.append("Permissive license - commercial-friendly")
            elif license_type in ["GPL-3.0", "AGPL-3.0"]:
                score += 5
                findings.append("Copyleft license - review commercial implications")
                recommendations.append("Review copyleft license implications for commercial use")
        else:
            blockers.append("No license file detected")
            findings.append("No license file - ownership unclear")
            recommendations.append("Add appropriate license file")
        
        # Fork status (0-20 points)
        if not is_fork:
            score += 20
            findings.append("Original work (not a fork)")
        else:
            score += 5
            findings.append(f"Fork of {fork_source}")
            recommendations.append("Clarify original contributions vs forked code")
            if ownership_clarity == "unknown":
                blockers.append("Fork with unclear ownership")
        
        # Originality (0-25 points)
        if copied_code_ratio < 0.1:
            score += 25
            findings.append("High originality (>90% original code)")
        elif copied_code_ratio < 0.3:
            score += 15
            findings.append("Moderate originality (>70% original code)")
        elif copied_code_ratio < 0.5:
            score += 5
            findings.append("Low originality (>50% original code)")
            recommendations.append("Increase original code contribution")
        else:
            findings.append("Very low originality (<50% original code)")
            blockers.append("Excessive copied code")
        
        # Template dependence (0-15 points)
        if not template_dependence:
            score += 15
            findings.append("No obvious template dependence")
        else:
            score += 5
            findings.append("Template-based project detected")
            recommendations.append("Clarify custom contributions vs template")
        
        # Ownership clarity (0-10 points)
        if ownership_clarity == "clear":
            score += 10
            findings.append("Ownership is clear")
        elif ownership_clarity == "likely_clear":
            score += 5
            findings.append("Ownership likely clear")
            recommendations.append("Add contributor attribution")
        else:
            findings.append("Ownership unclear")
            recommendations.append("Clarify ownership through attribution and documentation")
        
        grade = self._score_to_grade(score)
        
        return EvaluationResult(
            evaluator_name=self.name,
            grade=grade,
            score=score,
            confidence=0.8,
            findings=findings,
            blockers=blockers,
            recommendations=recommendations,
            evidence=evidence,
        )

    def _score_to_grade(self, score: float) -> EvaluationGrade:
        """Convert score to grade."""
        if score >= 90:
            return EvaluationGrade.A_PLUS
        elif score >= 80:
            return EvaluationGrade.A
        elif score >= 70:
            return EvaluationGrade.A_MINUS
        elif score >= 60:
            return EvaluationGrade.B_PLUS
        elif score >= 50:
            return EvaluationGrade.B
        elif score >= 40:
            return EvaluationGrade.B_MINUS
        elif score >= 30:
            return EvaluationGrade.C_PLUS
        elif score >= 20:
            return EvaluationGrade.C
        elif score >= 10:
            return EvaluationGrade.C_MINUS
        else:
            return EvaluationGrade.F


class MarketEvaluator:
    """
    Market Evaluator - Determines buyer relevance.
    
    Evaluates:
    - Who would need this asset?
    - What category does it belong to?
    - Does it have buyer relevance?
    - What is the market size?
    """

    def __init__(self):
        self.name = "Market Evaluator"

    def evaluate(self, asset_data: Dict[str, Any]) -> EvaluationResult:
        """Evaluate market relevance."""
        findings = []
        blockers = []
        recommendations = []
        evidence = {}
        
        # Extract market signals
        category = asset_data.get("category", "unknown")
        buyer_categories = asset_data.get("buyer_categories", [])
        market_size = asset_data.get("market_size", "unknown")
        competitive_landscape = asset_data.get("competitive_landscape", [])
        unique_value_proposition = asset_data.get("unique_value_proposition", "")
        adoption_signals = asset_data.get("adoption_signals", {})
        
        evidence = {
            "category": category,
            "buyer_categories": buyer_categories,
            "market_size": market_size,
            "competitive_landscape": competitive_landscape,
            "unique_value_proposition": unique_value_proposition,
            "adoption_signals": adoption_signals,
        }
        
        score = 0
        
        # Category clarity (0-15 points)
        if category != "unknown":
            score += 15
            findings.append(f"Clear category: {category}")
        else:
            findings.append("Category unclear")
            recommendations.append("Define clear product category")
        
        # Buyer categories (0-25 points)
        if buyer_categories:
            score += min(25, len(buyer_categories) * 8)
            findings.append(f"{len(buyer_categories)} potential buyer categories identified")
            for bc in buyer_categories[:3]:
                findings.append(f"  - {bc}")
        else:
            findings.append("No buyer categories identified")
            recommendations.append("Identify target buyer categories")
        
        # Market size (0-20 points)
        if market_size == "large":
            score += 20
            findings.append("Large addressable market")
        elif market_size == "medium":
            score += 15
            findings.append("Medium addressable market")
        elif market_size == "niche":
            score += 10
            findings.append("Niche market")
        else:
            findings.append("Market size unknown")
            recommendations.append("Assess market size")
        
        # Competitive landscape (0-15 points)
        if not competitive_landscape:
            score += 15
            findings.append("No direct competitors identified - blue ocean")
        elif len(competitive_landscape) < 3:
            score += 10
            findings.append("Few direct competitors")
        else:
            score += 5
            findings.append(f"{len(competitive_landscape)} competitors identified")
            recommendations.append("Differentiate from competitors")
        
        # Unique value proposition (0-15 points)
        if unique_value_proposition:
            score += 15
            findings.append("Clear unique value proposition")
        else:
            findings.append("Unique value proposition unclear")
            recommendations.append("Articulate unique value proposition")
        
        # Adoption signals (0-10 points)
        stars = adoption_signals.get("stars", 0)
        forks = adoption_signals.get("forks", 0)
        downloads = adoption_signals.get("downloads", 0)
        
        if stars > 1000 or downloads > 10000:
            score += 10
            findings.append("Strong adoption signals")
        elif stars > 100 or downloads > 1000:
            score += 7
            findings.append("Moderate adoption signals")
        elif stars > 10 or downloads > 100:
            score += 4
            findings.append("Early adoption signals")
        else:
            findings.append("Limited adoption signals")
        
        grade = self._score_to_grade(score)
        
        return EvaluationResult(
            evaluator_name=self.name,
            grade=grade,
            score=score,
            confidence=0.7,
            findings=findings,
            blockers=blockers,
            recommendations=recommendations,
            evidence=evidence,
        )

    def _score_to_grade(self, score: float) -> EvaluationGrade:
        """Convert score to grade."""
        if score >= 85:
            return EvaluationGrade.A_PLUS
        elif score >= 75:
            return EvaluationGrade.A
        elif score >= 65:
            return EvaluationGrade.A_MINUS
        elif score >= 55:
            return EvaluationGrade.B_PLUS
        elif score >= 45:
            return EvaluationGrade.B
        elif score >= 35:
            return EvaluationGrade.B_MINUS
        elif score >= 25:
            return EvaluationGrade.C_PLUS
        elif score >= 15:
            return EvaluationGrade.C
        else:
            return EvaluationGrade.F


class CollateralEvaluator:
    """
    Collateral Evaluator - Determines collateral support capability.
    
    Evaluates:
    - Can this support a credit memo?
    - Is there a liquidation route?
    - Is there a monitoring plan?
    - What is the collateral support range?
    """

    def __init__(self):
        self.name = "Collateral Evaluator"

    def evaluate(self, asset_data: Dict[str, Any]) -> EvaluationResult:
        """Evaluate collateral support."""
        findings = []
        blockers = []
        recommendations = []
        evidence = {}
        
        # Extract collateral signals
        has_ownership_clarity = asset_data.get("has_ownership_clarity", False)
        has_liquidation_route = asset_data.get("has_liquidation_route", False)
        has_monitoring_plan = asset_data.get("has_monitoring_plan", False)
        collateral_support_range = asset_data.get("collateral_support_range", (0, 0))
        revenue_evidence = asset_data.get("revenue_evidence", [])
        buyer_universe = asset_data.get("buyer_universe", [])
        
        evidence = {
            "has_ownership_clarity": has_ownership_clarity,
            "has_liquidation_route": has_liquidation_route,
            "has_monitoring_plan": has_monitoring_plan,
            "collateral_support_range": collateral_support_range,
            "revenue_evidence_count": len(revenue_evidence),
            "buyer_universe_size": len(buyer_universe),
        }
        
        score = 0
        
        # Ownership clarity (0-25 points)
        if has_ownership_clarity:
            score += 25
            findings.append("Ownership is clear and documented")
        else:
            blockers.append("Ownership unclear - cannot support collateral")
            findings.append("Ownership unclear")
            recommendations.append("Clarify ownership through documentation")
        
        # Liquidation route (0-30 points)
        if has_liquidation_route:
            score += 30
            findings.append("Clear liquidation route identified")
        else:
            findings.append("No liquidation route identified")
            recommendations.append("Identify liquidation route (sale, license, API, etc.)")
        
        # Monitoring plan (0-20 points)
        if has_monitoring_plan:
            score += 20
            findings.append("Monitoring plan in place")
        else:
            findings.append("No monitoring plan")
            recommendations.append("Create monitoring plan for ongoing collateral tracking")
        
        # Buyer universe (0-15 points)
        if buyer_universe:
            score += min(15, len(buyer_universe) * 3)
            findings.append(f"{len(buyer_universe)} potential buyers identified")
        else:
            findings.append("No buyer universe identified")
            recommendations.append("Identify potential buyers")
        
        # Revenue evidence (0-10 points)
        if revenue_evidence:
            score += 10
            findings.append(f"{len(revenue_evidence)} revenue evidence points")
        else:
            findings.append("No revenue evidence")
            recommendations.append("Document revenue or adoption evidence")
        
        grade = self._score_to_grade(score)
        
        return EvaluationResult(
            evaluator_name=self.name,
            grade=grade,
            score=score,
            confidence=0.75,
            findings=findings,
            blockers=blockers,
            recommendations=recommendations,
            evidence=evidence,
        )

    def _score_to_grade(self, score: float) -> EvaluationGrade:
        """Convert score to grade."""
        if score >= 85:
            return EvaluationGrade.A_PLUS
        elif score >= 75:
            return EvaluationGrade.A
        elif score >= 65:
            return EvaluationGrade.A_MINUS
        elif score >= 55:
            return EvaluationGrade.B_PLUS
        elif score >= 45:
            return EvaluationGrade.B
        elif score >= 35:
            return EvaluationGrade.B_MINUS
        elif score >= 25:
            return EvaluationGrade.C_PLUS
        elif score >= 15:
            return EvaluationGrade.C
        else:
            return EvaluationGrade.F


class LiquidationEvaluator:
    """
    Liquidation Evaluator - Finds the practical path to cash.
    
    Evaluates:
    - Sale as standalone codebase
    - Package as micro-SaaS
    - Turn into hosted API
    - Turn into Hugging Face Space
    - License to strategic buyer
    - Sell as data/report package
    - Submit to IP broker
    - Submit to venture studio
    - Open-source with paid services
    """

    def __init__(self):
        self.name = "Liquidation Evaluator"

    def evaluate(self, asset_data: Dict[str, Any]) -> EvaluationResult:
        """Evaluate liquidation routes."""
        findings = []
        blockers = []
        recommendations = []
        evidence = {}
        
        # Extract liquidation signals
        asset_type = asset_data.get("asset_type", "unknown")
        has_api_potential = asset_data.get("has_api_potential", False)
        has_data_value = asset_data.get("has_data_value", False)
        has_strategic_value = asset_data.get("has_strategic_value", False)
        buyer_difficulty = asset_data.get("buyer_difficulty", "medium")
        expected_timeline = asset_data.get("expected_timeline_days", (30, 90))
        
        evidence = {
            "asset_type": asset_type,
            "has_api_potential": has_api_potential,
            "has_data_value": has_data_value,
            "has_strategic_value": has_strategic_value,
            "buyer_difficulty": buyer_difficulty,
            "expected_timeline_days": expected_timeline,
        }
        
        score = 0
        
        # Asset type suitability (0-20 points)
        if asset_type in [AssetClassification.REAL_PRODUCTION_SYSTEM.value, AssetClassification.API_SERVICE.value]:
            score += 20
            findings.append("Asset type suitable for liquidation")
        elif asset_type in [AssetClassification.WORKING_PROTOTYPE.value, AssetClassification.INTERNAL_TOOL.value]:
            score += 10
            findings.append("Asset type may require work before liquidation")
            recommendations.append("Complete development before liquidation")
        else:
            findings.append("Asset type may not be liquidatable")
            recommendations.append("Consider alternative monetization or archive")
        
        # API potential (0-20 points)
        if has_api_potential:
            score += 20
            findings.append("API monetization route available")
            recommendations.append("Package as hosted API service")
        else:
            findings.append("Limited API potential")
        
        # Data value (0-15 points)
        if has_data_value:
            score += 15
            findings.append("Data/report monetization route available")
            recommendations.append("Package as data or report product")
        else:
            findings.append("Limited data value")
        
        # Strategic value (0-20 points)
        if has_strategic_value:
            score += 20
            findings.append("Strategic buyer route available")
            recommendations.append("Target strategic acquirers")
        else:
            findings.append("Limited strategic value")
        
        # Buyer difficulty (0-15 points)
        if buyer_difficulty == "low":
            score += 15
            findings.append("Buyer outreach expected to be straightforward")
        elif buyer_difficulty == "medium":
            score += 10
            findings.append("Buyer outreach moderately difficult")
        else:
            score += 5
            findings.append("Buyer outreach expected to be difficult")
            recommendations.append("Consider broker or marketplace")
        
        # Timeline (0-10 points)
        avg_timeline = sum(expected_timeline) / 2
        if avg_timeline < 60:
            score += 10
            findings.append("Relatively quick liquidation timeline")
        elif avg_timeline < 120:
            score += 7
            findings.append("Moderate liquidation timeline")
        else:
            score += 3
            findings.append("Long liquidation timeline")
        
        grade = self._score_to_grade(score)
        
        return EvaluationResult(
            evaluator_name=self.name,
            grade=grade,
            score=score,
            confidence=0.7,
            findings=findings,
            blockers=blockers,
            recommendations=recommendations,
            evidence=evidence,
        )

    def _score_to_grade(self, score: float) -> EvaluationGrade:
        """Convert score to grade."""
        if score >= 85:
            return EvaluationGrade.A_PLUS
        elif score >= 75:
            return EvaluationGrade.A
        elif score >= 65:
            return EvaluationGrade.A_MINUS
        elif score >= 55:
            return EvaluationGrade.B_PLUS
        elif score >= 45:
            return EvaluationGrade.B
        elif score >= 35:
            return EvaluationGrade.B_MINUS
        elif score >= 25:
            return EvaluationGrade.C_PLUS
        elif score >= 15:
            return EvaluationGrade.C
        else:
            return EvaluationGrade.F


class AgentLaborEvaluator:
    """
    Agent Labor Evaluator - Determines AI-agent work value.
    
    Evaluates:
    - Did AI-agent work create capitalizable assets?
    - Or did it just generate cleanup burden?
    - What is the signal-to-noise ratio?
    - What needs deduplication?
    """

    def __init__(self):
        self.name = "Agent Labor Evaluator"

    def evaluate(self, asset_data: Dict[str, Any]) -> EvaluationResult:
        """Evaluate agent labor value."""
        findings = []
        blockers = []
        recommendations = []
        evidence = {}
        
        # Extract agent labor signals
        is_agent_generated = asset_data.get("is_agent_generated", False)
        agent_activity_logs = asset_data.get("agent_activity_logs", [])
        signal_to_noise_ratio = asset_data.get("signal_to_noise_ratio", 0.5)
        duplicate_ratio = asset_data.get("duplicate_ratio", 0)
        scaffold_ratio = asset_data.get("scaffold_ratio", 0)
        original_contribution_ratio = asset_data.get("original_contribution_ratio", 0)
        
        evidence = {
            "is_agent_generated": is_agent_generated,
            "agent_activity_log_count": len(agent_activity_logs),
            "signal_to_noise_ratio": signal_to_noise_ratio,
            "duplicate_ratio": duplicate_ratio,
            "scaffold_ratio": scaffold_ratio,
            "original_contribution_ratio": original_contribution_ratio,
        }
        
        score = 0
        
        # Agent-generated flag
        if is_agent_generated:
            findings.append("Asset appears to be AI-agent generated")
            
            # Signal-to-noise ratio (0-30 points)
            if signal_to_noise_ratio > 0.7:
                score += 30
                findings.append("High signal-to-noise ratio - valuable agent work")
            elif signal_to_noise_ratio > 0.5:
                score += 20
                findings.append("Moderate signal-to-noise ratio")
            elif signal_to_noise_ratio > 0.3:
                score += 10
                findings.append("Low signal-to-noise ratio - significant cleanup needed")
                recommendations.append("Filter and curate agent-generated content")
            else:
                findings.append("Very low signal-to-noise ratio - mostly noise")
                blockers.append("Agent-generated content is mostly noise")
                recommendations.append("Significant cleanup required before capitalization")
            
            # Duplicate ratio (0-20 points)
            if duplicate_ratio < 0.1:
                score += 20
                findings.append("Low duplicate ratio - good agent originality")
            elif duplicate_ratio < 0.3:
                score += 10
                findings.append("Moderate duplicate ratio")
                recommendations.append("Deduplicate agent-generated content")
            else:
                findings.append("High duplicate ratio - agent generated duplicates")
                recommendations.append("Aggressive deduplication required")
            
            # Scaffold ratio (0-20 points)
            if scaffold_ratio < 0.2:
                score += 20
                findings.append("Low scaffold ratio - substantial custom work")
            elif scaffold_ratio < 0.5:
                score += 10
                findings.append("Moderate scaffold ratio")
                recommendations.append("Remove scaffolding and retain custom work")
            else:
                findings.append("High scaffold ratio - mostly boilerplate")
                blockers.append("Asset is mostly scaffold/template")
                recommendations.append("Extract custom work from scaffolding")
            
            # Original contribution (0-30 points)
            if original_contribution_ratio > 0.7:
                score += 30
                findings.append("High original contribution - capitalizable agent work")
            elif original_contribution_ratio > 0.5:
                score += 20
                findings.append("Moderate original contribution")
            elif original_contribution_ratio > 0.3:
                score += 10
                findings.append("Low original contribution")
                recommendations.append("Increase original agent contribution")
            else:
                findings.append("Very low original contribution")
                blockers.append("Agent work has minimal original value")
        else:
            score += 100
            findings.append("Not agent-generated - human-created asset")
        
        grade = self._score_to_grade(score)
        
        return EvaluationResult(
            evaluator_name=self.name,
            grade=grade,
            score=score,
            confidence=0.8,
            findings=findings,
            blockers=blockers,
            recommendations=recommendations,
            evidence=evidence,
        )

    def _score_to_grade(self, score: float) -> EvaluationGrade:
        """Convert score to grade."""
        if score >= 90:
            return EvaluationGrade.A_PLUS
        elif score >= 80:
            return EvaluationGrade.A
        elif score >= 70:
            return EvaluationGrade.A_MINUS
        elif score >= 60:
            return EvaluationGrade.B_PLUS
        elif score >= 50:
            return EvaluationGrade.B
        elif score >= 40:
            return EvaluationGrade.B_MINUS
        elif score >= 30:
            return EvaluationGrade.C_PLUS
        elif score >= 20:
            return EvaluationGrade.C
        elif score >= 10:
            return EvaluationGrade.C_MINUS
        else:
            return EvaluationGrade.F


class SyntheticCommittee:
    """
    The Synthetic Committee - Professional evaluation system.
    
    Coordinates all evaluators to produce a comprehensive professional assessment.
    """

    def __init__(self):
        self.evaluators = {
            "engineering": EngineeringEvaluator(),
            "execution": ExecutionEvaluator(),
            "security": SecurityEvaluator(),
            "license_originality": LicenseOriginalityEvaluator(),
            "market": MarketEvaluator(),
            "collateral": CollateralEvaluator(),
            "liquidation": LiquidationEvaluator(),
            "agent_labor": AgentLaborEvaluator(),
        }

    def evaluate(self, asset_data: Dict[str, Any]) -> Dict[str, Any]:
        """Run full committee evaluation."""
        results = {}
        
        for evaluator_name, evaluator in self.evaluators.items():
            results[evaluator_name] = evaluator.evaluate(asset_data)
        
        # Aggregate results
        committee_report = self._generate_committee_report(results)
        
        return {
            "evaluator_results": {name: result.to_dict() for name, result in results.items()},
            "committee_report": committee_report,
        }

    def _generate_committee_report(self, results: Dict[str, EvaluationResult]) -> Dict[str, Any]:
        """Generate aggregated committee report."""
        all_blockers = []
        all_recommendations = []
        all_findings = []
        
        for result in results.values():
            all_blockers.extend(result.blockers)
            all_recommendations.extend(result.recommendations)
            all_findings.extend(result.findings)
        
        # Calculate average score
        scores = [result.score for result in results.values()]
        avg_score = sum(scores) / len(scores) if scores else 0
        
        # Count risk blocks
        risk_blocked = any(
            result.evidence.get("risk_blocked", False)
            for result in results.values()
        )
        
        return {
            "average_score": avg_score,
            "risk_blocked": risk_blocked,
            "total_blockers": len(all_blockers),
            "total_recommendations": len(all_recommendations),
            "total_findings": len(all_findings),
            "all_blockers": all_blockers,
            "all_recommendations": list(set(all_recommendations)),  # Deduplicate
            "all_findings": all_findings,
        }
