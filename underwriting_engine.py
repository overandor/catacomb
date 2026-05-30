#!/usr/bin/env python3
"""
Underwriting Engine - Conservative institutional appraisal for software assets.

Core rule: The engine asks "What number can survive diligence?" not
"What is the biggest number we can justify?"

Generates six separate values:
1. Replacement Cost
2. As-Is Sale Value
3. Productized Value
4. Liquidation Value
5. Collateral Support Value
6. Financeability Score

Collateral Support Value formula:
CSV = Liquidation Value
      x Ownership Confidence
      x Technical Verification
      x Marketability
      x Legal Cleanliness
      x Security Cleanliness
      x Recovery Confidence
"""

from __future__ import annotations

from decimal import Decimal, ROUND_HALF_EVEN
from typing import Dict, Any, Optional, Tuple
from datetime import datetime

from collateral_packet import (
    AssetRecord,
    ValuationSet,
    DeductionSchedule,
    RiskRegister,
    ProofLevel,
)


class UnderwritingEngine:
    """
    Institutional-grade appraisal engine.

    Conservative by design. Transparent about deductions.
    Never produces a single flashy number.
    """

    # Base labor cost per line of code by language (USD)
    # Based on industry benchmarks, conservatively estimated
    LOC_COST_RATES = {
        "rust": Decimal("2.50"),
        "go": Decimal("2.20"),
        "typescript": Decimal("1.80"),
        "python": Decimal("1.50"),
        "javascript": Decimal("1.40"),
        "java": Decimal("1.80"),
        "c++": Decimal("2.80"),
        "c#": Decimal("1.90"),
        "ruby": Decimal("1.60"),
        "php": Decimal("1.20"),
        "swift": Decimal("2.00"),
        "kotlin": Decimal("1.90"),
        "scala": Decimal("2.20"),
        "solidity": Decimal("3.00"),
        "unknown": Decimal("1.50"),
    }

    # Complexity multipliers for file count and framework depth
    COMPLEXITY_BANDS = [
        (0, 10, Decimal("1.0")),
        (10, 50, Decimal("1.2")),
        (50, 200, Decimal("1.4")),
        (200, 1000, Decimal("1.6")),
        (1000, 5000, Decimal("1.8")),
        (5000, float("inf"), Decimal("2.0")),
    ]

    def __init__(self, conservatism_factor: Decimal = Decimal("0.85")):
        """
        Args:
            conservatism_factor: Global multiplier applied to all values.
                                 Default 0.85 means all values are discounted 15%
                                 to account for unknown risks.
        """
        self.conservatism_factor = conservatism_factor

    def appraise(self, asset: AssetRecord, repo_data: Dict[str, Any]) -> ValuationSet:
        """
        Run full six-value appraisal on an asset.

        Args:
            asset: The AssetRecord with proof data populated.
            repo_data: Raw GitHub/repo data for additional signals.

        Returns:
            ValuationSet with six separate values and confidence bands.
        """
        # --- 1. Replacement Cost ---
        replacement_cost = self._calculate_replacement_cost(asset, repo_data)

        # --- 2. As-Is Sale Value ---
        as_is_value = self._calculate_as_is_sale_value(asset, repo_data, replacement_cost)

        # --- 3. Productized Value ---
        productized_value = self._calculate_productized_value(asset, as_is_value)

        # --- 4. Liquidation Value ---
        liquidation_value = self._calculate_liquidation_value(asset, as_is_value)

        # --- 5. Collateral Support Value ---
        collateral_support = self._calculate_collateral_support_value(
            asset, liquidation_value
        )

        # --- 6. Financeability Score ---
        financeability = self._calculate_financeability_score(asset, collateral_support)

        # Apply global conservatism
        replacement_cost = self._apply_conservatism(replacement_cost)
        as_is_value = self._apply_conservatism(as_is_value)
        productized_value = self._apply_conservatism(productized_value)
        liquidation_value = self._apply_conservatism(liquidation_value)
        collateral_support = self._apply_conservatism(collateral_support)

        # Build ranges (asymmetric: upside limited, downside emphasized)
        rc_range = self._build_range(replacement_cost, Decimal("0.70"), Decimal("1.30"))
        ais_range = self._build_range(as_is_value, Decimal("0.50"), Decimal("1.20"))
        liq_range = self._build_range(liquidation_value, Decimal("0.40"), Decimal("1.10"))
        cs_range = self._build_range(collateral_support, Decimal("0.30"), Decimal("1.05"))

        return ValuationSet(
            replacement_cost_usd=Decimal(str(int(replacement_cost))),
            as_is_sale_value_usd=Decimal(str(int(as_is_value))),
            productized_value_usd=Decimal(str(int(productized_value))),
            liquidation_value_usd=Decimal(str(int(liquidation_value))),
            collateral_support_value_usd=Decimal(str(int(collateral_support))),
            financeability_score=financeability,
            replacement_cost_range=rc_range,
            as_is_sale_range=ais_range,
            liquidation_range=liq_range,
            collateral_support_range=cs_range,
            generated_at=datetime.now(),
        )

    def generate_deduction_schedule(
        self, asset: AssetRecord, base_strategic_value: Decimal
    ) -> DeductionSchedule:
        """
        Generate transparent deduction schedule showing why collateral support
        is lower than strategic value.
        """
        deductions = []
        remaining = base_strategic_value

        # No revenue
        if not asset.revenue_evidence:
            pct = Decimal("0.35")
            amount = remaining * pct
            deductions.append({
                "reason": "No verified revenue or paid usage evidence",
                "percentage": float(pct * 100),
                "amount_usd": str(int(amount)),
                "severity": "high",
            })
            remaining -= amount

        # No build proof
        if asset.build_status != "passed":
            pct = Decimal("0.20")
            amount = remaining * pct
            deductions.append({
                "reason": "Build not verified or failed",
                "percentage": float(pct * 100),
                "amount_usd": str(int(amount)),
                "severity": "high",
            })
            remaining -= amount

        # No license
        if asset.license_status != "clean":
            pct = Decimal("0.10")
            amount = remaining * pct
            deductions.append({
                "reason": "License unclear or missing",
                "percentage": float(pct * 100),
                "amount_usd": str(int(amount)),
                "severity": "medium",
            })
            remaining -= amount

        # No buyer interest
        if not asset.buyer_universe:
            pct = Decimal("0.25")
            amount = remaining * pct
            deductions.append({
                "reason": "No buyer interest or market evidence",
                "percentage": float(pct * 100),
                "amount_usd": str(int(amount)),
                "severity": "high",
            })
            remaining -= amount

        # Thin liquidation market
        if asset.risk_register.liquidation_risk in ["medium", "high"]:
            pct = Decimal("0.30")
            amount = remaining * pct
            deductions.append({
                "reason": "Thin or uncertain liquidation market",
                "percentage": float(pct * 100),
                "amount_usd": str(int(amount)),
                "severity": "high",
            })
            remaining -= amount

        # Single owner / bus factor
        if len(asset.contributor_list) <= 1:
            pct = Decimal("0.10")
            amount = remaining * pct
            deductions.append({
                "reason": "Single owner / contributor risk",
                "percentage": float(pct * 100),
                "amount_usd": str(int(amount)),
                "severity": "medium",
            })
            remaining -= amount

        # Secret risk
        if asset.secret_scan_status == "detected":
            pct = Decimal("0.40")
            amount = remaining * pct
            deductions.append({
                "reason": "Secrets or credentials detected",
                "percentage": float(pct * 100),
                "amount_usd": str(int(amount)),
                "severity": "critical",
            })
            remaining -= amount

        # Fork contamination
        if asset.fork_status in ["fork", "template_derived"]:
            pct = Decimal("0.15")
            amount = remaining * pct
            deductions.append({
                "reason": "Fork or template-derived asset",
                "percentage": float(pct * 100),
                "amount_usd": str(int(amount)),
                "severity": "medium",
            })
            remaining -= amount

        # Low documentation
        if asset.documentation_score < 40:
            pct = Decimal("0.15")
            amount = remaining * pct
            deductions.append({
                "reason": "Documentation score below 40/100",
                "percentage": float(pct * 100),
                "amount_usd": str(int(amount)),
                "severity": "medium",
            })
            remaining -= amount

        return DeductionSchedule(
            base_strategic_value=base_strategic_value,
            deductions=deductions,
            final_collateral_support=Decimal(str(int(max(0, remaining)))),
        )

    def _calculate_replacement_cost(
        self, asset: AssetRecord, repo_data: Dict[str, Any]
    ) -> Decimal:
        """
        What would it cost to recreate this work from scratch?
        Rewards engineering labor and complexity.
        """
        # Estimate LOC from file count and size
        estimated_loc = self._estimate_loc(asset.file_count, asset.total_size_bytes)

        # Base rate by primary language
        lang = (asset.primary_language or "unknown").lower()
        rate = self.LOC_COST_RATES.get(lang, self.LOC_COST_RATES["unknown"])

        base_cost = Decimal(str(estimated_loc)) * rate

        # Complexity multiplier by file count
        complexity_mult = Decimal("1.0")
        for low, high, mult in self.COMPLEXITY_BANDS:
            if low <= asset.file_count < high:
                complexity_mult = mult
                break

        # Framework depth bonus
        framework_bonus = Decimal("0")
        if asset.framework_stack:
            framework_bonus = Decimal(str(len(asset.framework_stack) * 2500))

        # Architecture quality from documentation score
        arch_mult = Decimal("1.0")
        if asset.documentation_score >= 70:
            arch_mult = Decimal("1.15")
        elif asset.documentation_score >= 40:
            arch_mult = Decimal("1.05")

        total = (base_cost * complexity_mult + framework_bonus) * arch_mult

        # Cap extreme values for sanity
        total = min(total, Decimal("5000000"))
        return total.quantize(Decimal("0.01"), rounding=ROUND_HALF_EVEN)

    def _calculate_as_is_sale_value(
        self, asset: AssetRecord, repo_data: Dict[str, Any], replacement_cost: Decimal
    ) -> Decimal:
        """
        What could someone plausibly pay today without more work?
        This is usually much lower than replacement cost.
        """
        # Base: fraction of replacement cost
        base = replacement_cost * Decimal("0.25")

        # Stars signal market interest
        stars = repo_data.get("stars", 0)
        if stars > 1000:
            base += Decimal(str(stars)) * Decimal("10")
        elif stars > 100:
            base += Decimal(str(stars)) * Decimal("5")
        elif stars > 10:
            base += Decimal(str(stars)) * Decimal("2")

        # Forks indicate active reuse potential
        forks = repo_data.get("forks", 0)
        if forks > 100:
            base += Decimal("5000")
        elif forks > 10:
            base += Decimal("1000")

        # Revenue evidence is king
        if asset.revenue_evidence:
            monthly_revenue = sum(
                r.get("monthly_amount", 0) for r in asset.revenue_evidence
            )
            if monthly_revenue > 0:
                # 3-6x monthly revenue for quick sale
                base += Decimal(str(monthly_revenue)) * Decimal("4")

        # Build proof increases buyer confidence
        if asset.build_status == "passed":
            base *= Decimal("1.20")
        elif asset.build_status == "failed":
            base *= Decimal("0.60")

        # License cleanliness
        if asset.license_status == "clean":
            base *= Decimal("1.15")
        else:
            base *= Decimal("0.80")

        # Cap at replacement cost
        base = min(base, replacement_cost)
        return base.quantize(Decimal("0.01"), rounding=ROUND_HALF_EVEN)

    def _calculate_productized_value(
        self, asset: AssetRecord, as_is_value: Decimal
    ) -> Decimal:
        """
        What could this be worth after packaging, deployment, docs, and polish?
        This is the upside case.
        """
        # Base: 2-4x as-is value depending on potential
        mult = Decimal("2.5")

        if asset.deployment_status == "live":
            mult += Decimal("0.5")
        if asset.documentation_score >= 60:
            mult += Decimal("0.3")
        if asset.test_status == "passed":
            mult += Decimal("0.3")
        if asset.buyer_universe:
            mult += Decimal("0.2")

        total = as_is_value * mult
        return total.quantize(Decimal("0.01"), rounding=ROUND_HALF_EVEN)

    def _calculate_liquidation_value(
        self, asset: AssetRecord, as_is_value: Decimal
    ) -> Decimal:
        """
        What could it sell for under pressure?
        This is the lender's recovery number.
        Typically 25-50% of as-is value.
        """
        base = as_is_value * Decimal("0.35")

        # Adjust based on liquidation risk
        if asset.risk_register.liquidation_risk == "low":
            base *= Decimal("1.30")
        elif asset.risk_register.liquidation_risk == "medium":
            base *= Decimal("1.00")
        elif asset.risk_register.liquidation_risk == "high":
            base *= Decimal("0.60")

        # Buyer universe strength
        buyer_count = len(asset.buyer_universe)
        if buyer_count >= 20:
            base *= Decimal("1.20")
        elif buyer_count >= 5:
            base *= Decimal("1.05")
        else:
            base *= Decimal("0.80")

        return base.quantize(Decimal("0.01"), rounding=ROUND_HALF_EVEN)

    def _calculate_collateral_support_value(
        self, asset: AssetRecord, liquidation_value: Decimal
    ) -> Decimal:
        """
        What portion of liquidation value can support a loan?

        Formula:
        CSV = Liquidation Value
              x Ownership Confidence
              x Technical Verification
              x Marketability
              x Legal Cleanliness
              x Security Cleanliness
              x Recovery Confidence
        """
        # Ownership confidence (0.0 - 1.0)
        ownership_conf = self._ownership_confidence(asset)

        # Technical verification (0.0 - 1.0)
        tech_verification = self._technical_verification(asset)

        # Marketability (0.0 - 1.0)
        marketability = self._marketability(asset)

        # Legal cleanliness (0.0 - 1.0)
        legal_clean = self._legal_cleanliness(asset)

        # Security cleanliness (0.0 - 1.0)
        security_clean = self._security_cleanliness(asset)

        # Recovery confidence (0.0 - 1.0)
        recovery_conf = self._recovery_confidence(asset)

        csv = (
            liquidation_value
            * ownership_conf
            * tech_verification
            * marketability
            * legal_clean
            * security_clean
            * recovery_conf
        )

        return csv.quantize(Decimal("0.01"), rounding=ROUND_HALF_EVEN)

    def _calculate_financeability_score(
        self, asset: AssetRecord, collateral_support: Decimal
    ) -> int:
        """
        How close is this asset to being accepted by a lender, buyer, or broker?
        0-100 score based on proof coverage.
        """
        score = 0

        # Ownership clarity (0-15)
        if asset.owner_claim and len(asset.owner_claim) > 3:
            score += 8
        if asset.fork_status == "original":
            score += 7
        elif asset.fork_status == "unknown":
            score += 3

        # Build proof (0-15)
        if asset.build_status == "passed":
            score += 15
        elif asset.build_status == "attempted":
            score += 8
        elif asset.build_status == "failed":
            score += 3

        # Test proof (0-10)
        if asset.test_status == "passed":
            score += 10
        elif asset.test_status == "attempted":
            score += 5

        # Documentation (0-10)
        score += int(asset.documentation_score / 10)

        # License cleanliness (0-10)
        if asset.license_status == "clean":
            score += 10
        elif asset.license_status == "ambiguous":
            score += 5

        # Secret cleanliness (0-10)
        if asset.secret_scan_status == "passed":
            score += 10
        elif asset.secret_scan_status == "unknown":
            score += 5

        # Deployment proof (0-10)
        if asset.deployment_status == "live":
            score += 10
        elif asset.deployment_status == "configured":
            score += 5

        # Marketability / buyer universe (0-10)
        buyer_count = len(asset.buyer_universe)
        if buyer_count >= 20:
            score += 10
        elif buyer_count >= 10:
            score += 7
        elif buyer_count >= 5:
            score += 5
        elif buyer_count >= 1:
            score += 2

        # Revenue evidence (0-10)
        if asset.revenue_evidence:
            score += 10

        # Liquidation path (0-5)
        if asset.liquidation_route:
            score += 5

        # Hash manifest (0-5)
        if asset.hash_manifest:
            score += 5

        return min(100, score)

    def _ownership_confidence(self, asset: AssetRecord) -> Decimal:
        """0.0 - 1.0 scale."""
        if not asset.owner_claim:
            return Decimal("0.30")
        if asset.risk_register.ownership_risk == "low":
            return Decimal("0.90")
        elif asset.risk_register.ownership_risk == "medium":
            return Decimal("0.70")
        return Decimal("0.50")

    def _technical_verification(self, asset: AssetRecord) -> Decimal:
        """0.0 - 1.0 scale."""
        if asset.build_status == "passed" and asset.test_status == "passed":
            return Decimal("0.90")
        elif asset.build_status == "passed":
            return Decimal("0.70")
        elif asset.build_status == "attempted":
            return Decimal("0.50")
        return Decimal("0.30")

    def _marketability(self, asset: AssetRecord) -> Decimal:
        """0.0 - 1.0 scale."""
        buyer_count = len(asset.buyer_universe)
        if buyer_count >= 20:
            return Decimal("0.80")
        elif buyer_count >= 10:
            return Decimal("0.60")
        elif buyer_count >= 5:
            return Decimal("0.45")
        elif buyer_count >= 1:
            return Decimal("0.30")
        return Decimal("0.20")

    def _legal_cleanliness(self, asset: AssetRecord) -> Decimal:
        """0.0 - 1.0 scale."""
        if asset.license_status == "clean":
            return Decimal("0.95")
        elif asset.license_status == "ambiguous":
            return Decimal("0.70")
        return Decimal("0.50")

    def _security_cleanliness(self, asset: AssetRecord) -> Decimal:
        """0.0 - 1.0 scale."""
        if asset.secret_scan_status == "passed":
            return Decimal("0.95")
        elif asset.secret_scan_status == "unknown":
            return Decimal("0.80")
        return Decimal("0.40")

    def _recovery_confidence(self, asset: AssetRecord) -> Decimal:
        """0.0 - 1.0 scale."""
        if asset.liquidation_route and asset.liquidation_route.buyer_list:
            return Decimal("0.75")
        if asset.buyer_universe:
            return Decimal("0.55")
        return Decimal("0.40")

    def _estimate_loc(self, file_count: int, total_size_bytes: int) -> int:
        """Rough LOC estimate from file count and total size."""
        if file_count == 0:
            return 0
        avg_file_size = total_size_bytes / file_count
        # Rough estimate: average 50 bytes per LOC
        loc_per_file = max(10, int(avg_file_size / 50))
        return file_count * loc_per_file

    def _apply_conservatism(self, value: Decimal) -> Decimal:
        return (value * self.conservatism_factor).quantize(
            Decimal("0.01"), rounding=ROUND_HALF_EVEN
        )

    def _build_range(
        self, value: Decimal, lower_pct: Decimal, upper_pct: Decimal
    ) -> Tuple[Decimal, Decimal]:
        low = (value * lower_pct).quantize(Decimal("0.01"), rounding=ROUND_HALF_EVEN)
        high = (value * upper_pct).quantize(Decimal("0.01"), rounding=ROUND_HALF_EVEN)
        return (low, high)
