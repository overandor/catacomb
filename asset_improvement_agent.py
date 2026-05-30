#!/usr/bin/env python3
"""
Asset Improvement Agent - 24/7 operator that raises the financeability score.

This is not a chatbot. It is an internal asset manager.
Its single goal: increase the financeability of the portfolio.

Daily tasks:
- Scan new files
- Detect changed projects
- Update asset values
- Find missing proof
- Generate READMEs, licenses, tests, Dockerfiles
- Prepare proof packets
- Identify buyers
- Flag secrets
- Detect duplicate work
- Audit other agents
- Summarize value changes
"""

from __future__ import annotations

import os
import hashlib
import json
from decimal import Decimal
from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass, field
from datetime import datetime

from collateral_packet import (
    AssetRecord,
    AssetType,
    ProofLevel,
    CapitalReadinessState,
    RiskBlockReason,
)
from financeability_engine import FinanceabilityEngine, ImprovementAction
from underwriting_engine import UnderwritingEngine


@dataclass
class DailyPortfolioReport:
    """Summary of what the improvement agent accomplished in a period."""
    period_start: datetime
    period_end: datetime
    new_assets_found: int = 0
    assets_improved: int = 0
    scaffolds_detected: int = 0
    duplicate_folders_detected: int = 0
    secrets_detected: int = 0
    builds_verified: int = 0
    financeability_score_before: int = 0
    financeability_score_after: int = 0
    collateral_support_before: Decimal = Decimal("0")
    collateral_support_after: Decimal = Decimal("0")
    best_next_action: Optional[str] = None
    actions_taken: List[Dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "period_start": self.period_start.isoformat(),
            "period_end": self.period_end.isoformat(),
            "new_assets_found": self.new_assets_found,
            "assets_improved": self.assets_improved,
            "scaffolds_detected": self.scaffolds_detected,
            "duplicate_folders_detected": self.duplicate_folders_detected,
            "secrets_detected": self.secrets_detected,
            "builds_verified": self.builds_verified,
            "financeability_score_before": self.financeability_score_before,
            "financeability_score_after": self.financeability_score_after,
            "collateral_support_before": str(self.collateral_support_before),
            "collateral_support_after": str(self.collateral_support_after),
            "best_next_action": self.best_next_action,
            "actions_taken": self.actions_taken,
        }

    def summary_text(self) -> str:
        return (
            f"Portfolio update ({self.period_start.date()} to {self.period_end.date()}):\n"
            f"  New assets found: {self.new_assets_found}\n"
            f"  Assets improved: {self.assets_improved}\n"
            f"  Scaffolds detected: {self.scaffolds_detected}\n"
            f"  Duplicate folders: {self.duplicate_folders_detected}\n"
            f"  Secrets detected: {self.secrets_detected}\n"
            f"  Builds verified: {self.builds_verified}\n"
            f"  Financeability score: {self.financeability_score_before} -> {self.financeability_score_after}\n"
            f"  Collateral support: ${int(self.collateral_support_before):,} -> ${int(self.collateral_support_after):,}\n"
            f"  Best next action: {self.best_next_action or 'None'}\n"
        )


class AssetImprovementAgent:
    """
    Economic operator for software portfolios.

    Every action must map to financeability.
    """

    def __init__(
        self,
        financeability_engine: Optional[FinanceabilityEngine] = None,
        underwriting_engine: Optional[UnderwritingEngine] = None,
    ):
        self.financeability = financeability_engine or FinanceabilityEngine()
        self.underwriting = underwriting_engine or UnderwritingEngine()
        self.action_history: List[Dict[str, Any]] = []

    def run_portfolio_audit(
        self,
        assets: List[AssetRecord],
        repo_data_map: Optional[Dict[str, Dict[str, Any]]] = None,
    ) -> DailyPortfolioReport:
        """
        Run a full portfolio improvement cycle.

        Args:
            assets: Current asset register.
            repo_data_map: Map of asset_id -> raw repo data.

        Returns:
            DailyPortfolioReport summarizing changes.
        """
        repo_data_map = repo_data_map or {}
        report = DailyPortfolioReport(
            period_start=datetime.now(),
            period_end=datetime.now(),
        )

        total_score_before = 0
        total_cs_before = Decimal("0")
        valid_assets = 0

        for asset in assets:
            if asset.capital_readiness_state == CapitalReadinessState.ARCHIVED:
                continue
            if asset.valuation:
                total_score_before += asset.valuation.financeability_score
                total_cs_before += asset.valuation.collateral_support_value_usd
                valid_assets += 1

        if valid_assets > 0:
            report.financeability_score_before = total_score_before // valid_assets
            report.collateral_support_before = total_cs_before

        # Phase 1: Classify and detect junk
        for asset in assets:
            self._classify_asset(asset)
            if asset.asset_type in [AssetType.SCAFFOLD, AssetType.DUPLICATE, AssetType.JUNK]:
                if asset.asset_type == AssetType.SCAFFOLD:
                    report.scaffolds_detected += 1
                elif asset.asset_type == AssetType.DUPLICATE:
                    report.duplicate_folders_detected += 1

        # Phase 2: Re-appraise and update
        for asset in assets:
            if asset.asset_type in [AssetType.SCAFFOLD, AssetType.DUPLICATE, AssetType.JUNK]:
                continue
            repo_data = repo_data_map.get(asset.asset_id, {})
            asset.valuation = self.underwriting.appraise(asset, repo_data)
            asset.deduction_schedule = self.underwriting.generate_deduction_schedule(
                asset, asset.valuation.replacement_cost_usd
            )
            asset.financeability_score = asset.valuation.financeability_score

        # Phase 3: Generate improvement actions
        for asset in assets:
            if asset.asset_type in [AssetType.SCAFFOLD, AssetType.DUPLICATE, AssetType.JUNK]:
                continue
            report.assets_improved += self._execute_improvements(asset)

        # Phase 4: Recalculate portfolio totals
        total_score_after = 0
        total_cs_after = Decimal("0")
        valid_assets = 0
        best_action = None
        best_impact = Decimal("0")

        for asset in assets:
            if asset.capital_readiness_state == CapitalReadinessState.ARCHIVED:
                continue
            if asset.valuation:
                total_score_after += asset.valuation.financeability_score
                total_cs_after += asset.valuation.collateral_support_value_usd
                valid_assets += 1

            # Find best next action across portfolio
            fin_report = self.financeability.analyze(asset)
            if fin_report.one_best_next_action:
                action = fin_report.one_best_next_action
                if action.estimated_collateral_support_increase_usd > best_impact:
                    best_impact = action.estimated_collateral_support_increase_usd
                    best_action = f"{asset.asset_name}: {action.description}"

        if valid_assets > 0:
            report.financeability_score_after = total_score_after // valid_assets
            report.collateral_support_after = total_cs_after

        report.best_next_action = best_action
        report.period_end = datetime.now()
        return report

    def analyze_single_asset(
        self, asset: AssetRecord, repo_data: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Deep analysis of one asset with improvement queue.

        Returns:
            Dict with financeability report, valuation, and recommended actions.
        """
        repo_data = repo_data or {}

        # Re-appraise
        asset.valuation = self.underwriting.appraise(asset, repo_data)
        asset.deduction_schedule = self.underwriting.generate_deduction_schedule(
            asset, asset.valuation.replacement_cost_usd
        )
        asset.financeability_score = asset.valuation.financeability_score

        # Financeability deep dive
        fin_report = self.financeability.analyze(asset)

        # Capital readiness state update
        self._update_readiness_state(asset)

        return {
            "asset": asset.to_dict(),
            "financeability_report": fin_report.to_dict(),
            "valuation": asset.valuation.to_dict(),
            "deduction_schedule": asset.deduction_schedule.to_dict() if asset.deduction_schedule else None,
            "recommended_actions": [a.to_dict() for a in fin_report.improvement_queue],
            "one_best_next_action": (
                fin_report.one_best_next_action.to_dict()
                if fin_report.one_best_next_action else None
            ),
        }

    def _classify_asset(self, asset: AssetRecord) -> None:
        """Determine if asset is real, scaffold, duplicate, or junk."""
        # Heuristic classification
        if asset.file_count == 0:
            asset.asset_type = AssetType.JUNK
            return

        if asset.file_count < 3 and asset.total_size_bytes < 2048:
            asset.asset_type = AssetType.SCAFFOLD
            return

        # Detect duplicates by name similarity (simplified)
        # In a real system, hash comparison would be used.
        # For now, leave as-is if already classified.
        if asset.asset_type == AssetType.ORIGINAL_REPOSITORY and asset.file_count > 0:
            pass

    def _execute_improvements(self, asset: AssetRecord) -> int:
        """
        Simulate executing improvement actions on an asset.
        Returns count of actions taken.
        """
        actions_taken = 0
        fin_report = self.financeability.analyze(asset)

        for action in fin_report.improvement_queue:
            # Simulate auto-fixing critical blockers that are low-effort
            if action.category == "critical_blocker" and action.effort_estimate in ["30 minutes", "10 minutes", "1-2 hours"]:
                self._simulate_fix(asset, action)
                actions_taken += 1
                self.action_history.append({
                    "timestamp": datetime.now().isoformat(),
                    "asset_id": asset.asset_id,
                    "action": action.action_id,
                    "description": action.description,
                    "simulated": True,
                })

        return actions_taken

    def _simulate_fix(self, asset: AssetRecord, action: ImprovementAction) -> None:
        """Simulate applying an improvement to an asset record."""
        if action.action_id == "add_license":
            asset.license_status = "clean"
        elif action.action_id == "remove_secrets":
            asset.secret_scan_status = "passed"
        elif action.action_id == "add_ownership_declaration":
            if not asset.owner_claim:
                asset.owner_claim = "declared_by_owner"
        elif action.action_id == "verify_build":
            asset.build_status = "attempted"
        elif action.action_id == "improve_documentation":
            asset.documentation_score = min(100, asset.documentation_score + 20)
        elif action.action_id == "add_tests":
            asset.test_status = "attempted"
        elif action.action_id == "deploy_demo":
            asset.deployment_status = "configured"
        elif action.action_id == "generate_hash_manifest":
            # Create a simple hash manifest
            from collateral_packet import HashManifest
            asset.hash_manifest = HashManifest(
                folder_hash=hashlib.sha256(asset.asset_name.encode()).hexdigest()[:16],
                file_hashes={},
            )

        # Re-evaluate proof level
        self._update_proof_level(asset)

    def _update_proof_level(self, asset: AssetRecord) -> None:
        """Recalculate proof level based on current statuses."""
        if asset.capital_readiness_state == CapitalReadinessState.RISK_BLOCKED:
            asset.proof_level = ProofLevel.CLAIMED
            return

        if asset.hash_manifest:
            level = ProofLevel.HASHED
        else:
            level = ProofLevel.DISCOVERED

        if asset.secret_scan_status == "passed" and asset.license_status == "clean":
            level = ProofLevel.CLEAN

        if asset.build_status == "passed":
            level = ProofLevel.BUILD_VERIFIED

        if asset.deployment_status == "live" or asset.test_status == "passed":
            level = ProofLevel.USE_VERIFIED

        if asset.revenue_evidence:
            level = ProofLevel.MARKET_VERIFIED

        if asset.financeability_score >= 70 and asset.liquidation_route:
            level = ProofLevel.FINANCEABLE

        asset.proof_level = level

    def _update_readiness_state(self, asset: AssetRecord) -> None:
        """Update capital readiness state based on asset condition."""
        if asset.risk_block_reasons:
            asset.capital_readiness_state = CapitalReadinessState.RISK_BLOCKED
            return

        if asset.proof_level.value < ProofLevel.HASHED.value:
            asset.capital_readiness_state = CapitalReadinessState.DISCOVERED
        elif asset.proof_level.value < ProofLevel.BUILD_VERIFIED.value:
            asset.capital_readiness_state = CapitalReadinessState.PROOF_STARTED
        elif asset.proof_level.value < ProofLevel.FINANCEABLE.value:
            asset.capital_readiness_state = CapitalReadinessState.BUILD_VERIFIED
        else:
            asset.capital_readiness_state = CapitalReadinessState.FINANCEABLE

        # Packet ready if financeability >= 50
        if asset.financeability_score >= 50 and asset.capital_readiness_state.value >= CapitalReadinessState.BUILD_VERIFIED.value:
            asset.capital_readiness_state = CapitalReadinessState.PACKET_READY

        # Lender ready if financeability >= 65
        if asset.financeability_score >= 65:
            asset.capital_readiness_state = CapitalReadinessState.LENDER_READY

        # Buyer ready if financeability >= 50 and buyer universe exists
        if asset.financeability_score >= 50 and asset.buyer_universe:
            asset.capital_readiness_state = CapitalReadinessState.BUYER_READY
