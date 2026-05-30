#!/usr/bin/env python3
"""
Financeability Engine - Measures how close an asset is to being accepted by money.

The Financeability Score is the main KPI. It is separate from valuation.
A repo can have high strategic value but low financeability.

This engine:
1. Decomposes the score into sub-dimensions
2. Identifies exact blockers
3. Recommends next actions with estimated score impact
4. Calculates before/after deltas
"""

from __future__ import annotations

from decimal import Decimal
from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass, field
from datetime import datetime

from collateral_packet import AssetRecord, ProofLevel, CapitalReadinessState


@dataclass
class FinanceabilitySubscore:
    """A component of the overall financeability score."""
    name: str
    score: int  # 0-100
    weight: float
    weighted_contribution: float
    blockers: List[str] = field(default_factory=list)
    evidence_present: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "score": self.score,
            "weight": self.weight,
            "weighted_contribution": round(self.weighted_contribution, 2),
            "blockers": self.blockers,
            "evidence_present": self.evidence_present,
        }


@dataclass
class ImprovementAction:
    """A specific action that can increase financeability."""
    action_id: str
    description: str
    category: str  # critical_blocker, high_value, commercial, proof
    estimated_score_increase: int
    estimated_collateral_support_increase_usd: Decimal
    effort_estimate: str  # hours/days
    prerequisite_actions: List[str] = field(default_factory=list)
    evidence_required: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "action_id": self.action_id,
            "description": self.description,
            "category": self.category,
            "estimated_score_increase": self.estimated_score_increase,
            "estimated_collateral_support_increase_usd": str(self.estimated_collateral_support_increase_usd),
            "effort_estimate": self.effort_estimate,
            "prerequisite_actions": self.prerequisite_actions,
            "evidence_required": self.evidence_required,
        }


@dataclass
class FinanceabilityReport:
    """Complete financeability analysis for an asset."""
    asset_id: str
    asset_name: str
    overall_score: int
    proof_level: str
    capital_readiness_state: str
    subscores: List[FinanceabilitySubscore]
    blockers: List[str]
    improvement_queue: List[ImprovementAction]
    current_collateral_support_usd: Decimal
    potential_collateral_support_usd: Decimal
    one_best_next_action: Optional[ImprovementAction] = None
    generated_at: datetime = field(default_factory=datetime.now)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "asset_id": self.asset_id,
            "asset_name": self.asset_name,
            "overall_score": self.overall_score,
            "proof_level": self.proof_level,
            "capital_readiness_state": self.capital_readiness_state,
            "subscores": [s.to_dict() for s in self.subscores],
            "blockers": self.blockers,
            "improvement_queue": [a.to_dict() for a in self.improvement_queue],
            "current_collateral_support_usd": str(self.current_collateral_support_usd),
            "potential_collateral_support_usd": str(self.potential_collateral_support_usd),
            "one_best_next_action": self.one_best_next_action.to_dict() if self.one_best_next_action else None,
            "generated_at": self.generated_at.isoformat(),
        }


class FinanceabilityEngine:
    """
    Professional-grade financeability analysis.

    Tone: slightly harsh, conservative, developer-side.
    Never flatters. Always tells the truth about what blocks money.
    """

    # Rubric weights (must sum to 1.0)
    RUBRIC = {
        "ownership_clarity": 0.15,
        "originality_clarity": 0.10,
        "build_proof": 0.15,
        "documentation_quality": 0.10,
        "marketability": 0.15,
        "liquidation_path": 0.10,
        "security_cleanliness": 0.10,
        "revenue_evidence": 0.10,
        "reviewer_confidence": 0.05,
    }

    def analyze(self, asset: AssetRecord) -> FinanceabilityReport:
        """
        Run complete financeability analysis on an asset.
        """
        subscores = self._calculate_subscores(asset)
        overall = int(sum(s.weighted_contribution for s in subscores))

        blockers = self._identify_blockers(asset, subscores)
        improvement_queue = self._generate_improvement_queue(asset, subscores)

        # Pick the one best next action
        one_best = None
        if improvement_queue:
            # Prioritize: critical blockers first, then highest score/collateral ROI
            critical = [a for a in improvement_queue if a.category == "critical_blocker"]
            if critical:
                one_best = max(critical, key=lambda x: x.estimated_collateral_support_increase_usd)
            else:
                one_best = max(improvement_queue, key=lambda x: x.estimated_collateral_support_increase_usd)

        current_cs = asset.valuation.collateral_support_value_usd if asset.valuation else Decimal("0")
        potential_cs = self._estimate_potential_collateral_support(asset, improvement_queue)

        return FinanceabilityReport(
            asset_id=asset.asset_id,
            asset_name=asset.asset_name,
            overall_score=min(100, overall),
            proof_level=asset.proof_level.name,
            capital_readiness_state=asset.capital_readiness_state.value,
            subscores=subscores,
            blockers=blockers,
            improvement_queue=improvement_queue,
            current_collateral_support_usd=current_cs,
            potential_collateral_support_usd=potential_cs,
            one_best_next_action=one_best,
        )

    def _calculate_subscores(self, asset: AssetRecord) -> List[FinanceabilitySubscore]:
        """Compute each dimension of financeability."""
        subscores = []

        # 1. Ownership clarity (0-100)
        ownership_score = 0
        ownership_blockers = []
        ownership_evidence = []
        if asset.owner_claim:
            ownership_score += 40
            ownership_evidence.append("Owner claimed")
        else:
            ownership_blockers.append("No ownership declaration")
        if asset.fork_status == "original":
            ownership_score += 40
            ownership_evidence.append("Original work")
        elif asset.fork_status == "unknown":
            ownership_score += 15
            ownership_blockers.append("Originality not verified")
        else:
            ownership_blockers.append("Fork or template-derived")
        if len(asset.contributor_list) > 1:
            ownership_score += 10
            ownership_evidence.append("Multiple contributors documented")
        if asset.risk_register.ownership_risk == "low":
            ownership_score += 10
        elif asset.risk_register.ownership_risk == "high":
            ownership_blockers.append("High ownership risk flagged")
        ownership_score = min(100, ownership_score)
        subscores.append(FinanceabilitySubscore(
            name="Ownership Clarity",
            score=ownership_score,
            weight=self.RUBRIC["ownership_clarity"],
            weighted_contribution=ownership_score * self.RUBRIC["ownership_clarity"],
            blockers=ownership_blockers,
            evidence_present=ownership_evidence,
        ))

        # 2. Originality clarity (0-100)
        orig_score = 0
        orig_blockers = []
        orig_evidence = []
        if asset.fork_status == "original":
            orig_score += 60
            orig_evidence.append("Original codebase")
        elif asset.fork_status == "clean_fork_with_changes":
            orig_score += 30
            orig_evidence.append("Fork with substantial changes")
        elif asset.fork_status == "template_derived":
            orig_score += 20
            orig_blockers.append("Template-derived")
        else:
            orig_blockers.append("Originality unclear")
        if asset.originality_score >= 60:
            orig_score += 30
            orig_evidence.append("High originality score")
        elif asset.originality_score >= 30:
            orig_score += 10
        if asset.risk_register.originality_risk == "low":
            orig_score += 10
        elif asset.risk_register.originality_risk == "high":
            orig_blockers.append("High originality risk")
        orig_score = min(100, orig_score)
        subscores.append(FinanceabilitySubscore(
            name="Originality Clarity",
            score=orig_score,
            weight=self.RUBRIC["originality_clarity"],
            weighted_contribution=orig_score * self.RUBRIC["originality_clarity"],
            blockers=orig_blockers,
            evidence_present=orig_evidence,
        ))

        # 3. Build proof (0-100)
        build_score = 0
        build_blockers = []
        build_evidence = []
        if asset.build_status == "passed":
            build_score += 50
            build_evidence.append("Build verified")
        elif asset.build_status == "attempted":
            build_score += 25
            build_blockers.append("Build attempted but not fully verified")
        else:
            build_blockers.append("No build proof")
        if asset.test_status == "passed":
            build_score += 30
            build_evidence.append("Tests passing")
        elif asset.test_status == "attempted":
            build_score += 10
            build_blockers.append("Tests attempted but not fully passing")
        else:
            build_blockers.append("No test proof")
        if asset.deployment_status == "live":
            build_score += 20
            build_evidence.append("Live deployment")
        elif asset.deployment_status == "configured":
            build_score += 10
        build_score = min(100, build_score)
        subscores.append(FinanceabilitySubscore(
            name="Build and Execution Proof",
            score=build_score,
            weight=self.RUBRIC["build_proof"],
            weighted_contribution=build_score * self.RUBRIC["build_proof"],
            blockers=build_blockers,
            evidence_present=build_evidence,
        ))

        # 4. Documentation quality (0-100)
        doc_score = asset.documentation_score
        doc_blockers = []
        doc_evidence = []
        if doc_score >= 70:
            doc_evidence.append("Strong documentation")
        elif doc_score >= 40:
            doc_blockers.append("Documentation incomplete")
        else:
            doc_blockers.append("Documentation weak or missing")
        subscores.append(FinanceabilitySubscore(
            name="Documentation Quality",
            score=doc_score,
            weight=self.RUBRIC["documentation_quality"],
            weighted_contribution=doc_score * self.RUBRIC["documentation_quality"],
            blockers=doc_blockers,
            evidence_present=doc_evidence,
        ))

        # 5. Marketability (0-100)
        market_score = 0
        market_blockers = []
        market_evidence = []
        buyer_count = len(asset.buyer_universe)
        if buyer_count >= 20:
            market_score += 40
            market_evidence.append("Strong buyer universe (20+)")
        elif buyer_count >= 10:
            market_score += 30
            market_evidence.append("Moderate buyer universe")
        elif buyer_count >= 5:
            market_score += 20
            market_evidence.append("Small buyer universe")
        elif buyer_count >= 1:
            market_score += 10
            market_blockers.append("Buyer universe thin")
        else:
            market_blockers.append("No buyer universe identified")
        if asset.revenue_evidence:
            market_score += 40
            market_evidence.append("Revenue evidence present")
        else:
            market_blockers.append("No revenue evidence")
        if asset.marketability_score > 0:
            market_score += min(20, asset.marketability_score // 5)
        market_score = min(100, market_score)
        subscores.append(FinanceabilitySubscore(
            name="Marketability",
            score=market_score,
            weight=self.RUBRIC["marketability"],
            weighted_contribution=market_score * self.RUBRIC["marketability"],
            blockers=market_blockers,
            evidence_present=market_evidence,
        ))

        # 6. Liquidation path (0-100)
        liq_score = 0
        liq_blockers = []
        liq_evidence = []
        if asset.liquidation_route:
            liq_score += 40
            liq_evidence.append("Liquidation route defined")
            if asset.liquidation_route.buyer_list:
                liq_score += 20
                liq_evidence.append("Specific buyers identified")
        else:
            liq_blockers.append("No liquidation route prepared")
        if asset.risk_register.liquidation_risk == "low":
            liq_score += 30
            liq_evidence.append("Low liquidation risk")
        elif asset.risk_register.liquidation_risk == "medium":
            liq_score += 15
        else:
            liq_blockers.append("High liquidation risk")
        if len(asset.buyer_universe) >= 10:
            liq_score += 10
        liq_score = min(100, liq_score)
        subscores.append(FinanceabilitySubscore(
            name="Liquidation Path",
            score=liq_score,
            weight=self.RUBRIC["liquidation_path"],
            weighted_contribution=liq_score * self.RUBRIC["liquidation_path"],
            blockers=liq_blockers,
            evidence_present=liq_evidence,
        ))

        # 7. Security cleanliness (0-100)
        sec_score = 0
        sec_blockers = []
        sec_evidence = []
        if asset.secret_scan_status == "passed":
            sec_score += 50
            sec_evidence.append("Secret scan passed")
        elif asset.secret_scan_status == "unknown":
            sec_score += 25
            sec_blockers.append("Secret scan not performed")
        else:
            sec_blockers.append("Secrets or credentials detected")
        if asset.risk_register.security_risk == "low":
            sec_score += 30
            sec_evidence.append("Low security risk")
        elif asset.risk_register.security_risk == "medium":
            sec_score += 15
            sec_blockers.append("Medium security risk")
        else:
            sec_blockers.append("High security risk")
        if asset.license_status == "clean":
            sec_score += 20
            sec_evidence.append("License clean")
        elif asset.license_status == "ambiguous":
            sec_score += 10
            sec_blockers.append("License ambiguous")
        else:
            sec_blockers.append("License risky")
        sec_score = min(100, sec_score)
        subscores.append(FinanceabilitySubscore(
            name="Security and License Cleanliness",
            score=sec_score,
            weight=self.RUBRIC["security_cleanliness"],
            weighted_contribution=sec_score * self.RUBRIC["security_cleanliness"],
            blockers=sec_blockers,
            evidence_present=sec_evidence,
        ))

        # 8. Revenue evidence (0-100)
        rev_score = 0
        rev_blockers = []
        rev_evidence = []
        if asset.revenue_evidence:
            rev_score += 60
            rev_evidence.append("Revenue evidence present")
            # Additional points for verified vs self-reported
            verified = sum(1 for r in asset.revenue_evidence if r.get("verified", False))
            if verified > 0:
                rev_score += 30
                rev_evidence.append("Verified revenue")
            else:
                rev_blockers.append("Revenue self-reported only")
        else:
            rev_blockers.append("No revenue or usage evidence")
        if asset.deployment_status == "live":
            rev_score += 10
        rev_score = min(100, rev_score)
        subscores.append(FinanceabilitySubscore(
            name="Revenue and Adoption Proof",
            score=rev_score,
            weight=self.RUBRIC["revenue_evidence"],
            weighted_contribution=rev_score * self.RUBRIC["revenue_evidence"],
            blockers=rev_blockers,
            evidence_present=rev_evidence,
        ))

        # 9. Reviewer confidence (0-100)
        revw_score = 0
        revw_blockers = []
        revw_evidence = []
        if asset.reviewer_signatures:
            revw_score += 60
            revw_evidence.append("Human reviewer signatures present")
            if any(r.get("role") == "valuation_reviewer" for r in asset.reviewer_signatures):
                revw_score += 20
                revw_evidence.append("Valuation reviewed")
            if any(r.get("role") == "security_reviewer" for r in asset.reviewer_signatures):
                revw_score += 20
                revw_evidence.append("Security reviewed")
        else:
            revw_blockers.append("No human review")
        revw_score = min(100, revw_score)
        subscores.append(FinanceabilitySubscore(
            name="Reviewer Confidence",
            score=revw_score,
            weight=self.RUBRIC["reviewer_confidence"],
            weighted_contribution=revw_score * self.RUBRIC["reviewer_confidence"],
            blockers=revw_blockers,
            evidence_present=revw_evidence,
        ))

        return subscores

    def _identify_blockers(self, asset: AssetRecord, subscores: List[FinanceabilitySubscore]) -> List[str]:
        """Consolidate all blockers from subscores."""
        blockers = []
        for sub in subscores:
            blockers.extend(sub.blockers)
        # Add capital readiness blockers
        if asset.capital_readiness_state == CapitalReadinessState.RISK_BLOCKED:
            blockers.append("Asset is risk-blocked and cannot be monetized until fixed")
        return list(set(blockers))

    def _generate_improvement_queue(
        self, asset: AssetRecord, subscores: List[FinanceabilitySubscore]
    ) -> List[ImprovementAction]:
        """Generate prioritized improvement actions with estimated impact."""
        queue = []
        current_cs = asset.valuation.collateral_support_value_usd if asset.valuation else Decimal("0")

        # Critical blockers first
        if asset.secret_scan_status != "passed":
            queue.append(ImprovementAction(
                action_id="remove_secrets",
                description="Remove exposed secrets, credentials, or private keys; re-run scan",
                category="critical_blocker",
                estimated_score_increase=10,
                estimated_collateral_support_increase_usd=current_cs * Decimal("0.25"),
                effort_estimate="2-4 hours",
                evidence_required=["Secret scan report showing clean"],
            ))

        if not asset.owner_claim:
            queue.append(ImprovementAction(
                action_id="add_ownership_declaration",
                description="Add signed ownership declaration and contributor agreement",
                category="critical_blocker",
                estimated_score_increase=8,
                estimated_collateral_support_increase_usd=current_cs * Decimal("0.15"),
                effort_estimate="1-2 hours",
                evidence_required=["Ownership declaration document"],
            ))

        if asset.license_status != "clean":
            queue.append(ImprovementAction(
                action_id="add_license",
                description="Add explicit LICENSE file and verify no conflicting obligations",
                category="critical_blocker",
                estimated_score_increase=7,
                estimated_collateral_support_increase_usd=current_cs * Decimal("0.12"),
                effort_estimate="30 minutes",
                evidence_required=["LICENSE file in repo root"],
            ))

        if asset.build_status not in ["passed", "attempted"]:
            queue.append(ImprovementAction(
                action_id="verify_build",
                description="Create reproducible build instructions and run build in clean environment",
                category="critical_blocker",
                estimated_score_increase=8,
                estimated_collateral_support_increase_usd=current_cs * Decimal("0.20"),
                effort_estimate="4-8 hours",
                evidence_required=["Build log showing success"],
            ))

        # High-value improvements
        if asset.documentation_score < 60:
            queue.append(ImprovementAction(
                action_id="improve_documentation",
                description="Write or improve README, API docs, and deployment instructions",
                category="high_value",
                estimated_score_increase=6,
                estimated_collateral_support_increase_usd=current_cs * Decimal("0.10"),
                effort_estimate="4-12 hours",
                evidence_required=["README quality score >= 60"],
            ))

        if asset.test_status != "passed":
            queue.append(ImprovementAction(
                action_id="add_tests",
                description="Add test suite with meaningful coverage and CI integration",
                category="high_value",
                estimated_score_increase=5,
                estimated_collateral_support_increase_usd=current_cs * Decimal("0.08"),
                effort_estimate="8-24 hours",
                evidence_required=["Test log showing pass"],
            ))

        if asset.deployment_status != "live":
            queue.append(ImprovementAction(
                action_id="deploy_demo",
                description="Deploy demo or staging instance and add deployment URL",
                category="high_value",
                estimated_score_increase=6,
                estimated_collateral_support_increase_usd=current_cs * Decimal("0.15"),
                effort_estimate="4-8 hours",
                evidence_required=["Live deployment URL"],
            ))

        # Commercial improvements
        if not asset.buyer_universe:
            queue.append(ImprovementAction(
                action_id="identify_buyers",
                description="Research and document 10-20 potential acquirers or licensees",
                category="commercial",
                estimated_score_increase=5,
                estimated_collateral_support_increase_usd=current_cs * Decimal("0.10"),
                effort_estimate="2-4 hours",
                evidence_required=["Buyer universe list with categories"],
            ))

        if not asset.revenue_evidence:
            queue.append(ImprovementAction(
                action_id="add_revenue_evidence",
                description="Add usage metrics, Stripe dashboard screenshot, or paid user proof",
                category="commercial",
                estimated_score_increase=10,
                estimated_collateral_support_increase_usd=current_cs * Decimal("0.30"),
                effort_estimate="1-2 hours",
                evidence_required=["Revenue or usage evidence document"],
            ))

        if not asset.liquidation_route:
            queue.append(ImprovementAction(
                action_id="create_liquidation_plan",
                description="Document forced-sale route: buyers, brokers, timeline, recovery estimate",
                category="commercial",
                estimated_score_increase=5,
                estimated_collateral_support_increase_usd=current_cs * Decimal("0.08"),
                effort_estimate="2-4 hours",
                evidence_required=["Liquidation route document"],
            ))

        # Proof improvements
        if not asset.hash_manifest:
            queue.append(ImprovementAction(
                action_id="generate_hash_manifest",
                description="Generate SHA-256 file hash manifest for tamper evidence",
                category="proof",
                estimated_score_increase=3,
                estimated_collateral_support_increase_usd=current_cs * Decimal("0.05"),
                effort_estimate="10 minutes",
                evidence_required=["Hash manifest JSON"],
            ))

        return queue

    def _estimate_potential_collateral_support(
        self, asset: AssetRecord, queue: List[ImprovementAction]
    ) -> Decimal:
        """Estimate collateral support if all improvements are completed."""
        current = asset.valuation.collateral_support_value_usd if asset.valuation else Decimal("0")
        total_increase = sum(a.estimated_collateral_support_increase_usd for a in queue)
        return current + total_increase
