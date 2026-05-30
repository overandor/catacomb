#!/usr/bin/env python3
"""
Lender Packet Generator - Credit-memo style collateral packet for lenders.

Tone: boring, conservative, institutional.
Lenders do not want "revolutionary protocol architecture."
They want Asset ID, Owner, Collateral description, Verification status,
Valuation method, Risk rating, Recovery estimate, Recommended advance rate.
"""

from __future__ import annotations

from decimal import Decimal
from typing import Dict, Any, List, Optional
from datetime import datetime

from collateral_packet import (
    AssetRecord,
    SoftwareCollateralPacket,
    ValuationSet,
    RiskRegister,
    LiquidationRoute,
    MonitoringPlan,
    ProofLevel,
)
from underwriting_engine import UnderwritingEngine


class LenderPacketGenerator:
    """
    Generates lender-readable collateral packets.

    Language used is conservative credit language, not hype.
    Every claim is qualified. Every risk is disclosed.
    """

    def __init__(self, underwriting_engine: Optional[UnderwritingEngine] = None):
        self.underwriting = underwriting_engine or UnderwritingEngine()

    def generate(
        self,
        asset: AssetRecord,
        repo_data: Optional[Dict[str, Any]] = None,
        borrower_verified: bool = False,
    ) -> SoftwareCollateralPacket:
        """
        Generate a complete lender packet for an asset.

        Args:
            asset: The AssetRecord to package.
            repo_data: Optional raw repository data for additional context.
            borrower_verified: Whether borrower identity has been externally verified.

        Returns:
            SoftwareCollateralPacket structured for lender review.
        """
        repo_data = repo_data or {}

        # Ensure valuation exists
        if not asset.valuation:
            asset.valuation = self.underwriting.appraise(asset, repo_data)

        # Ensure deduction schedule exists
        if not asset.deduction_schedule:
            base_strategic = asset.valuation.replacement_cost_usd
            asset.deduction_schedule = self.underwriting.generate_deduction_schedule(
                asset, base_strategic
            )

        # Build liquidation route if missing
        if not asset.liquidation_route:
            asset.liquidation_route = self._build_liquidation_route(asset)

        # Build monitoring plan
        monitoring = self._build_monitoring_plan(asset)

        # Determine LTV recommendation
        ltv = self._recommended_ltv(asset)
        loan_ceiling = self._loan_ceiling(asset)

        # Build risk narrative
        risk_narrative = self._build_risk_narrative(asset)

        packet = SoftwareCollateralPacket(
            asset_record=asset,
            owner_identity={
                "owner_claim": asset.owner_claim,
                "verified": borrower_verified,
                "verification_method": "self_declared" if not borrower_verified else "third_party_kyc",
            },
            ownership_declaration=asset.owner_claim or "No formal ownership declaration on file.",
            employer_client_risk_disclosure=risk_narrative.get("employer_risk", ""),
            contributor_list=asset.contributor_list,
            file_hash_manifest=asset.hash_manifest,
            commit_snapshot=asset.git_commit_snapshot,
            build_log=asset.build_status,
            test_log=asset.test_status,
            secret_scan_report={
                "status": asset.secret_scan_status,
                "findings": [],
                "risk_level": asset.risk_register.security_risk,
            },
            license_scan_report={
                "status": asset.license_status,
                "risk_level": asset.risk_register.license_risk,
            },
            fork_scan_report={
                "status": asset.fork_status,
                "originality_score": asset.originality_score,
            },
            readme_docs_review={
                "documentation_score": asset.documentation_score,
                "assessment": self._docs_assessment(asset.documentation_score),
            },
            endpoint_verification={
                "deployment_status": asset.deployment_status,
                "deployment_url": asset.deployment_url,
            },
            demo_link=asset.deployment_url,
            valuation=asset.valuation,
            deduction_schedule=asset.deduction_schedule,
            confidence_score=int(asset.valuation.financeability_score * 0.6),
            buyer_universe=asset.buyer_universe,
            recommended_loan_to_value=ltv,
            liquidation_route=asset.liquidation_route,
            monitoring_plan=monitoring,
            legal_disclaimers=self._lender_disclaimers(),
        )

        # Set loan ceiling in liquidation route
        if packet.liquidation_route:
            packet.liquidation_route.expected_recovery_band = (
                Decimal("0"),
                loan_ceiling,
            )

        packet.seal()
        return packet

    def _build_liquidation_route(self, asset: AssetRecord) -> LiquidationRoute:
        """Construct a conservative liquidation route."""
        buyers = asset.buyer_universe[:10] if asset.buyer_universe else []
        liq_value = asset.valuation.liquidation_value_usd if asset.valuation else Decimal("0")

        return LiquidationRoute(
            default_trigger="Payment default or material breach of loan covenants",
            access_rights="Legal transfer of repository ownership and documentation; subject to license review",
            asset_transfer_method="GitHub repo transfer + ZIP proof packet + documentation bundle",
            buyer_list=buyers,
            broker_route="IP broker or software M&A advisor (to be engaged at default)",
            auction_route="Private negotiated sale preferred; public auction only if broker route fails",
            expected_timeline_days=(60, 180),
            expected_recovery_band=(Decimal("0"), liq_value),
            legal_review_required=True,
        )

    def _build_monitoring_plan(self, asset: AssetRecord) -> MonitoringPlan:
        """Define ongoing monitoring requirements for the lender."""
        return MonitoringPlan(
            monthly_hash_snapshot=True,
            monthly_build_check=asset.build_status == "passed",
            monthly_secret_scan=True,
            monthly_license_check=True,
            deployment_status_check=asset.deployment_status == "live",
            revenue_adoption_update=bool(asset.revenue_evidence),
            owner_attestation_required=True,
            change_log_required=True,
            risk_flag_update=True,
        )

    def _recommended_ltv(self, asset: AssetRecord) -> str:
        """
        Recommended loan-to-value ratio.
        Very conservative. Most software assets start at 10-20%.
        """
        score = asset.valuation.financeability_score if asset.valuation else 0

        if score >= 80 and asset.revenue_evidence:
            return "20%–35%"
        elif score >= 60:
            return "10%–20%"
        elif score >= 40:
            return "5%–15%"
        elif score >= 20:
            return "5%–10%"
        else:
            return "Not recommended for secured lending until proof improves"

    def _loan_ceiling(self, asset: AssetRecord) -> Decimal:
        """Suggested maximum loan amount."""
        if not asset.valuation:
            return Decimal("0")

        cs = asset.valuation.collateral_support_value_usd
        score = asset.valuation.financeability_score

        if score >= 80:
            multiplier = Decimal("0.35")
        elif score >= 60:
            multiplier = Decimal("0.20")
        elif score >= 40:
            multiplier = Decimal("0.12")
        elif score >= 20:
            multiplier = Decimal("0.07")
        else:
            return Decimal("0")

        return (cs * multiplier).quantize(Decimal("0.01"))

    def _build_risk_narrative(self, asset: AssetRecord) -> Dict[str, str]:
        """Generate institutional risk language."""
        narratives = {}

        # Employer/client risk
        if asset.risk_register.ownership_risk in ["medium", "high"]:
            narratives["employer_risk"] = (
                "Ownership may be subject to employer, client, or third-party claims. "
                "Further legal review is required to confirm clean title before collateralization."
            )
        else:
            narratives["employer_risk"] = (
                "No obvious employer or client ownership risk identified. "
                "Self-declared; independent verification recommended."
            )

        return narratives

    def _docs_assessment(self, score: int) -> str:
        if score >= 70:
            return "Documentation appears adequate for third-party maintenance."
        elif score >= 40:
            return "Documentation is partial. A new developer would face onboarding friction."
        else:
            return "Documentation is weak or missing. Significant reverse-engineering would be required."

    def _lender_disclaimers(self) -> str:
        return (
            "IMPORTANT NOTICE FOR LENDERS:\n\n"
            "1. This packet is a diligence support document, not a loan approval or investment recommendation.\n"
            "2. Appraisal is not liquidity. A file may appraise at $50,000 but immediate liquidity may be $0–$2,000.\n"
            "3. Collateral support value is intentionally conservative and assumes forced-sale conditions.\n"
            "4. All values are estimates based on observed evidence, not guarantees.\n"
            "5. Human legal and technical review is strongly recommended before extending credit.\n"
            "6. The asset must be monitored monthly after financing.\n"
            "7. This is not legal advice, not tax advice, and not a securities offering.\n"
            "8. The borrower remains responsible for maintaining build proof, license cleanliness, and secret hygiene.\n\n"
            "CollateralOps Disclaimer: We convert software work into lender-readable packets. "
            "We do not guarantee values, approve loans, or assume liability for lending decisions."
        )

    def generate_summary_text(self, packet: SoftwareCollateralPacket) -> str:
        """Generate a plain-text credit memo summary."""
        asset = packet.asset_record
        v = asset.valuation

        lines = [
            "=" * 70,
            "SOFTWARE COLLATERAL PACKET — LENDER SUMMARY",
            "=" * 70,
            f"Packet ID:     {packet.packet_id}",
            f"Generated:     {packet.generated_at.isoformat()}",
            f"Packet Hash:   {packet.packet_hash}",
            "",
            "-" * 70,
            "BORROWER AND ASSET",
            "-" * 70,
            f"Asset Name:    {asset.asset_name}",
            f"Asset Type:    {asset.asset_type.value}",
            f"Owner Claim:   {asset.owner_claim}",
            f"Source:        {asset.source_type}",
            f"Repo URL:      {asset.repo_url or 'N/A'}",
            "",
            "-" * 70,
            "VERIFICATION STATUS",
            "-" * 70,
            f"Build:         {asset.build_status}",
            f"Tests:         {asset.test_status}",
            f"License:       {asset.license_status}",
            f"Secrets:       {asset.secret_scan_status}",
            f"Fork/Original: {asset.fork_status}",
            f"Proof Level:   {asset.proof_level.name}",
            "",
            "-" * 70,
            "VALUATION RANGES",
            "-" * 70,
        ]

        if v:
            lines.extend([
                f"Replacement Cost:        ${int(v.replacement_cost_usd):,}",
                f"As-Is Sale Value:        ${int(v.as_is_sale_value_usd):,}",
                f"Productized Value:       ${int(v.productized_value_usd):,}",
                f"Liquidation Value:       ${int(v.liquidation_value_usd):,}",
                f"Collateral Support:      ${int(v.collateral_support_value_usd):,}",
                f"Financeability Score:    {v.financeability_score}/100",
            ])
        else:
            lines.append("Valuation not available.")

        lines.extend([
            "",
            "-" * 70,
            "RISK FINDINGS",
            "-" * 70,
            f"Ownership Risk:          {asset.risk_register.ownership_risk}",
            f"Originality Risk:        {asset.risk_register.originality_risk}",
            f"Build Risk:              {asset.risk_register.build_risk}",
            f"License Risk:            {asset.risk_register.license_risk}",
            f"Secret Risk:             {asset.risk_register.secret_risk}",
            f"Market Risk:             {asset.risk_register.market_risk}",
            f"Liquidation Risk:        {asset.risk_register.liquidation_risk}",
            "",
            "-" * 70,
            "CREDIT RECOMMENDATION",
            "-" * 70,
            f"Recommended LTV:         {packet.recommended_loan_to_value}",
        ])

        if packet.liquidation_route:
            lines.append(
                f"Loan Ceiling Estimate:   ${int(packet.liquidation_route.expected_recovery_band[1]):,}"
            )

        lines.extend([
            "",
            "-" * 70,
            "MONITORING REQUIREMENTS",
            "-" * 70,
            f"Monthly hash snapshot:   {packet.monitoring_plan.monthly_hash_snapshot if packet.monitoring_plan else 'N/A'}",
            f"Monthly build check:     {packet.monitoring_plan.monthly_build_check if packet.monitoring_plan else 'N/A'}",
            f"Owner attestation:       {packet.monitoring_plan.owner_attestation_required if packet.monitoring_plan else 'N/A'}",
            "",
            "=" * 70,
            packet.legal_disclaimers,
            "=" * 70,
        ])

        return "\n".join(lines)
