#!/usr/bin/env python3
"""
Buyer Packet Generator - Opportunity-oriented collateral packet for acquirers.

Tone: opportunity-focused, not lender-conservative.
Buyers want to know: What does this do? Can I use it? Can I monetize it?
"""

from __future__ import annotations

from decimal import Decimal
from typing import Dict, Any, List, Optional
from datetime import datetime

from collateral_packet import (
    AssetRecord,
    SoftwareCollateralPacket,
    ValuationSet,
    BuyerUniverseEntry,
    LiquidationRoute,
    MonitoringPlan,
)
from underwriting_engine import UnderwritingEngine


class BuyerPacketGenerator:
    """
    Generates buyer-facing acquisition packets.

    Different from lender packet:
    - Emphasizes utility and upside
    - Shows integration path
    - Includes 30-day productization plan
    - Uses opportunity language, not credit language
    """

    def __init__(self, underwriting_engine: Optional[UnderwritingEngine] = None):
        self.underwriting = underwriting_engine or UnderwritingEngine()

    def generate(
        self,
        asset: AssetRecord,
        repo_data: Optional[Dict[str, Any]] = None,
        asking_price: Optional[Decimal] = None,
    ) -> SoftwareCollateralPacket:
        """
        Generate a buyer packet.

        Args:
            asset: The AssetRecord to package.
            repo_data: Optional raw repository data.
            asking_price: Optional explicit asking price. If not provided,
                          defaults to as-is sale value midpoint.
        """
        repo_data = repo_data or {}

        if not asset.valuation:
            asset.valuation = self.underwriting.appraise(asset, repo_data)

        if not asset.deduction_schedule:
            base_strategic = asset.valuation.replacement_cost_usd
            asset.deduction_schedule = self.underwriting.generate_deduction_schedule(
                asset, base_strategic
            )

        if asking_price is None and asset.valuation:
            low, high = asset.valuation.as_is_sale_range
            asking_price = (low + high) / Decimal("2")

        # Build buyer-specific memo
        buyer_memo = self._generate_buyer_memo(asset, asking_price)
        outreach_plan = self._generate_outreach_plan(asset)
        productization_plan = self._generate_30_day_plan(asset)

        packet = SoftwareCollateralPacket(
            asset_record=asset,
            owner_identity={
                "owner_claim": asset.owner_claim,
                "contact_preference": "via CollateralOps data room",
            },
            ownership_declaration=asset.owner_claim or "Ownership declared by seller.",
            file_hash_manifest=asset.hash_manifest,
            commit_snapshot=asset.git_commit_snapshot,
            build_log=asset.build_status,
            test_log=asset.test_status,
            dependency_manifest=asset.framework_stack,
            readme_docs_review={
                "score": asset.documentation_score,
                "summary": self._docs_summary(asset),
            },
            endpoint_verification={
                "deployment_url": asset.deployment_url,
                "status": asset.deployment_status,
            },
            demo_link=asset.deployment_url,
            valuation=asset.valuation,
            comparable_assets=self._generate_comparables(asset),
            buyer_universe=asset.buyer_universe,
            outreach_plan=outreach_plan,
            sale_memo=buyer_memo,
            productization_plan=productization_plan,
            nda_checklist=[
                "Source code access NDA",
                "Revenue data NDA",
                "Customer list NDA",
                "Non-solicitation clause",
            ],
            legal_disclaimers=self._buyer_disclaimers(),
        )

        packet.seal()
        return packet

    def _generate_buyer_memo(
        self, asset: AssetRecord, asking_price: Optional[Decimal]
    ) -> str:
        """Write the acquisition memo."""
        v = asset.valuation

        lines = [
            "SOFTWARE ACQUISITION MEMO",
            "=" * 60,
            f"Asset: {asset.asset_name}",
            f"Type:  {asset.asset_type.value}",
            f"URL:   {asset.repo_url or 'N/A'}",
            "",
            "PROBLEM SOLVED",
            "-" * 60,
            self._infer_problem_solved(asset),
            "",
            "PRODUCT FUNCTION",
            "-" * 60,
            self._infer_product_function(asset),
            "",
            "TECHNICAL STACK",
            "-" * 60,
            f"Language:   {asset.primary_language}",
            f"Frameworks: {', '.join(asset.framework_stack) if asset.framework_stack else 'None detected'}",
            f"Files:      {asset.file_count}",
            f"Size:       {asset.total_size_bytes:,} bytes",
            "",
            "CURRENT STATUS",
            "-" * 60,
            f"Build:      {asset.build_status}",
            f"Tests:      {asset.test_status}",
            f"Deployment: {asset.deployment_status}",
            f"License:    {asset.license_status}",
            "",
            "INTEGRATION PATH",
            "-" * 60,
            self._integration_path(asset),
            "",
            "REPLACEMENT COST",
            "-" * 60,
        ]

        if v:
            lines.append(f"Estimated cost to rebuild: ${int(v.replacement_cost_usd):,}")
            lines.append(f"Asking price range:        ${int(v.as_is_sale_value_usd):,}")
            if asking_price:
                lines.append(f"Current asking price:      ${int(asking_price):,}")
        else:
            lines.append("Valuation pending.")

        lines.extend([
            "",
            "RISKS",
            "-" * 60,
            f"Ownership clarity:  {asset.risk_register.ownership_risk}",
            f"Originality:          {asset.risk_register.originality_risk}",
            f"Security:             {asset.risk_register.security_risk}",
            f"License:              {asset.risk_register.license_risk}",
            "",
            "30-DAY PRODUCTIZATION PLAN",
            "-" * 60,
            self._generate_30_day_plan(asset),
            "",
            "CONTACT",
            "-" * 60,
            "Request data room access via CollateralOps.",
            "=" * 60,
        ])

        return "\n".join(lines)

    def _generate_outreach_plan(self, asset: AssetRecord) -> str:
        """Suggest how to reach buyers for this asset."""
        lines = [
            f"Buyer Outreach Plan for {asset.asset_name}",
            "",
            "1. PREPARE MATERIALS",
            "   - One-page summary (problem, solution, stack, status)",
            "   - Demo video or deployment URL",
            "   - Financial summary (if revenue exists)",
            "",
            "2. IDENTIFY BUYER CATEGORIES",
        ]
        categories = set(b.buyer_category for b in asset.buyer_universe)
        for cat in categories:
            lines.append(f"   - {cat}")
        if not categories:
            lines.append("   - (No buyer categories identified yet)")

        lines.extend([
            "",
            "3. OUTREACH SEQUENCE",
            "   Day 1: Send non-confidential summary to 20 targets",
            "   Day 7: Follow up with interested parties",
            "   Day 14: Send NDA + data room access to qualified buyers",
            "   Day 21: Schedule calls / demos",
            "   Day 30: Collect LOIs or offers",
            "",
            "4. CHANNELS",
            "   - Direct email to strategic acquirers",
            "   - Micro-SaaS marketplaces (if applicable)",
            "   - IP broker introduction",
            "   - AngelList / venture studio outreach",
            "   - Developer community announcements",
        ])
        return "\n".join(lines)

    def _generate_30_day_plan(self, asset: AssetRecord) -> str:
        """Suggest what a buyer should do in the first 30 days."""
        lines = [
            "Week 1: Due Diligence",
            "  - Review code structure and architecture",
            "  - Verify build and test suite locally",
            "  - Confirm license cleanliness",
            "  - Check for secrets or credentials",
            "",
            "Week 2: Integration Assessment",
            "  - Map APIs and data models to existing stack",
            "  - Identify breaking changes or refactoring needs",
            "  - Evaluate hosting and infrastructure requirements",
            "",
            "Week 3: Value Validation",
            "  - Interview potential users or customers",
            "  - Verify revenue or usage claims",
            "  - Assess competitive positioning",
            "",
            "Week 4: Decision and Offer",
            "  - Finalize valuation and offer terms",
            "  - Prepare transition plan (code, docs, domain, accounts)",
            "  - Negotiate support period (30-90 days recommended)",
        ]
        return "\n".join(lines)

    def _infer_problem_solved(self, asset: AssetRecord) -> str:
        """Infer the problem from asset metadata."""
        name = asset.asset_name.lower()
        if "bot" in name or "trading" in name:
            return "Automated trading or signal generation for financial markets."
        elif "api" in name or "service" in name:
            return "Backend service or API for integration workflows."
        elif "ui" in name or "frontend" in name or "app" in name:
            return "User-facing application or interface component."
        elif "scrap" in name or "crawl" in name:
            return "Data collection, scraping, or aggregation pipeline."
        elif "ml" in name or "ai" in name or "model" in name:
            return "Machine learning model, inference system, or AI workflow."
        elif "collateral" in name or "packet" in name:
            return "Software asset appraisal, proof generation, or financial packaging."
        else:
            return "Software utility or system; specific use case requires further review."

    def _infer_product_function(self, asset: AssetRecord) -> str:
        """Infer product function from metadata."""
        return self._infer_problem_solved(asset)

    def _integration_path(self, asset: AssetRecord) -> str:
        """Suggest how a buyer might integrate this asset."""
        lines = [
            f"Language: {asset.primary_language}",
        ]
        if asset.deployment_status == "live":
            lines.append("Asset is deployed and running. Integration may proceed via API or webhook.")
        elif asset.build_status == "passed":
            lines.append("Asset builds successfully. Buyer can deploy to their own infrastructure.")
        else:
            lines.append("Build status unverified. Buyer should expect initial engineering investment.")

        lines.append(f"Frameworks used: {', '.join(asset.framework_stack) if asset.framework_stack else 'None'}")
        lines.append("Recommended: containerize with Docker and deploy to existing cloud environment.")
        return "\n".join(lines)

    def _docs_summary(self, asset: AssetRecord) -> str:
        if asset.documentation_score >= 70:
            return "Strong documentation. Onboarding expected to be smooth."
        elif asset.documentation_score >= 40:
            return "Partial documentation. Some reverse-engineering may be required."
        return "Documentation weak. Buyer should budget for knowledge transfer and code exploration."

    def _generate_comparables(self, asset: AssetRecord) -> List[Dict[str, Any]]:
        """Generate rough comparable assets."""
        # In a real system, this would query a comparable asset database.
        # For now, return placeholder structure.
        return [
            {
                "type": "comparable_placeholder",
                "note": "Comparable asset database requires outcome data. "
                        "Populate via post-sale reporting to improve accuracy.",
            }
        ]

    def _buyer_disclaimers(self) -> str:
        return (
            "BUYER NOTICE:\n\n"
            "1. This packet is provided for preliminary due diligence only.\n"
            "2. All valuations are estimates, not guarantees.\n"
            "3. The seller declares ownership; independent verification is recommended.\n"
            "4. Build, test, and secret scan proof should be independently reproduced.\n"
            "5. CollateralOps does not warrant merchantability, fitness for purpose, or infringement status.\n"
            "6. Negotiate appropriate support and transition terms directly with seller.\n\n"
            "Appraisal is not liquidity. Past packet sales do not guarantee future outcomes."
        )
