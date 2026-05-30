#!/usr/bin/env python3
"""
Professional Review Card Generator - Creates the "professional feel" review cards.

Every asset should end with a card like this:

Asset: Repo Appraiser Pro

Classification:
Software asset appraisal and proof-packet generator

Production Grade:
B

Commercial Grade:
B+

Collateral Grade:
C+

Financeability Score:
61/100

Proof Level:
Level 3 — Clean / partially verified

Strategic Value:
High

Buyer-Today Value:
Moderate

Collateral Support:
Conservative and conditional

Main Blockers:
No outcome database
No human reviewer layer
No verified buyer response
Build/deployment proof incomplete

Best Next Action:
Generate three sample paid audit packets and record buyer response.

Likely Route:
IP consultants, venture studios, developer tooling buyers, software M&A advisors.

Packet Readiness:
Buyer-ready after packaging.
Lender-ready only after review and outcome evidence.

That is the "professional feel." The user sees judgment, not generic text.
"""

from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum


class ProofLevel(Enum):
    """Trust ladder for asset verification."""
    CLAIMED = 0
    DISCOVERED = 1
    HASHED = 2
    CLEAN = 3
    BUILD_VERIFIED = 4
    USE_VERIFIED = 5
    MARKET_VERIFIED = 6
    FINANCEABLE = 7
    
    def display_name(self) -> str:
        """Get display name for proof level."""
        names = {
            ProofLevel.CLAIMED: "Level 0 — Claimed only",
            ProofLevel.DISCOVERED: "Level 1 — Discovered",
            ProofLevel.HASHED: "Level 2 — Hashed",
            ProofLevel.CLEAN: "Level 3 — Clean / partially verified",
            ProofLevel.BUILD_VERIFIED: "Level 4 — Build verified",
            ProofLevel.USE_VERIFIED: "Level 5 — Use verified",
            ProofLevel.MARKET_VERIFIED: "Level 6 — Market verified",
            ProofLevel.FINANCEABLE: "Level 7 — Financeable",
        }
        return names.get(self, "Unknown")


@dataclass
class ProfessionalReviewCard:
    """
    Professional review card for a software asset.
    
    This is the "professional feel" - judgment, not generic text.
    """
    asset_id: str
    asset_name: str
    classification: str
    
    # Grades
    production_grade: str
    commercial_grade: str
    collateral_grade: str
    financeability_score: int
    
    # Proof level
    proof_level: ProofLevel
    
    # Strategic assessment
    strategic_value: str
    buyer_today_value: str
    collateral_support: str
    
    # Blockers
    main_blockers: List[str]
    
    # Action
    best_next_action: str
    
    # Route
    likely_route: List[str]
    
    # Readiness
    packet_readiness: str
    
    # Disclaimers
    disclaimers: List[str] = field(default_factory=list)
    
    # Evidence links
    evidence_links: Dict[str, str] = field(default_factory=dict)
    
    # Metadata
    evaluated_at: datetime = field(default_factory=datetime.now)
    evaluator_version: str = "job_description_intelligence_v1"
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "asset_id": self.asset_id,
            "asset_name": self.asset_name,
            "classification": self.classification,
            "production_grade": self.production_grade,
            "commercial_grade": self.commercial_grade,
            "collateral_grade": self.collateral_grade,
            "financeability_score": self.financeability_score,
            "proof_level": self.proof_level.value,
            "proof_level_display": self.proof_level.display_name(),
            "strategic_value": self.strategic_value,
            "buyer_today_value": self.buyer_today_value,
            "collateral_support": self.collateral_support,
            "main_blockers": self.main_blockers,
            "best_next_action": self.best_next_action,
            "likely_route": self.likely_route,
            "packet_readiness": self.packet_readiness,
            "disclaimers": self.disclaimers,
            "evidence_links": self.evidence_links,
            "evaluated_at": self.evaluated_at.isoformat(),
            "evaluator_version": self.evaluator_version,
        }
    
    def to_markdown(self) -> str:
        """Generate markdown representation of the review card."""
        lines = [
            f"## Asset: {self.asset_name}",
            "",
            f"**Classification:**",
            f"{self.classification}",
            "",
            f"**Production Grade:**",
            f"{self.production_grade}",
            "",
            f"**Commercial Grade:**",
            f"{self.commercial_grade}",
            "",
            f"**Collateral Grade:**",
            f"{self.collateral_grade}",
            "",
            f"**Financeability Score:**",
            f"{self.financeability_score}/100",
            "",
            f"**Proof Level:**",
            f"{self.proof_level.display_name()}",
            "",
            f"**Strategic Value:**",
            f"{self.strategic_value}",
            "",
            f"**Buyer-Today Value:**",
            f"{self.buyer_today_value}",
            "",
            f"**Collateral Support:**",
            f"{self.collateral_support}",
            "",
            f"**Main Blockers:**",
        ]
        
        for blocker in self.main_blockers:
            lines.append(f"- {blocker}")
        
        lines.extend([
            "",
            f"**Best Next Action:**",
            f"{self.best_next_action}",
            "",
            f"**Likely Route:**",
        ])
        
        for route_item in self.likely_route:
            lines.append(f"- {route_item}")
        
        lines.extend([
            "",
            f"**Packet Readiness:**",
            f"{self.packet_readiness}",
            "",
            f"**Evidence Links:**",
        ])
        
        for evidence_type, link in self.evidence_links.items():
            lines.append(f"- {evidence_type}: {link}")
        
        lines.extend([
            "",
            "---",
            "",
            "**DISCLAIMERS:**",
        ])
        
        for disclaimer in self.disclaimers:
            lines.append(f"- {disclaimer}")
        
        lines.extend([
            "",
            f"*Generated by {self.evaluator_version} on {self.evaluated_at.strftime('%Y-%m-%d %H:%M:%S UTC')}*",
        ])
        
        return "\n".join(lines)
    
    def to_text(self) -> str:
        """Generate plain text representation of the review card."""
        lines = [
            f"Asset: {self.asset_name}",
            "",
            f"Classification:",
            f"{self.classification}",
            "",
            f"Production Grade:",
            f"{self.production_grade}",
            "",
            f"Commercial Grade:",
            f"{self.commercial_grade}",
            "",
            f"Collateral Grade:",
            f"{self.collateral_grade}",
            "",
            f"Financeability Score:",
            f"{self.financeability_score}/100",
            "",
            f"Proof Level:",
            f"{self.proof_level.display_name()}",
            "",
            f"Strategic Value:",
            f"{self.strategic_value}",
            "",
            f"Buyer-Today Value:",
            f"{self.buyer_today_value}",
            "",
            f"Collateral Support:",
            f"{self.collateral_support}",
            "",
            f"Main Blockers:",
        ]
        
        for blocker in self.main_blockers:
            lines.append(f"- {blocker}")
        
        lines.extend([
            "",
            f"Best Next Action:",
            f"{self.best_next_action}",
            "",
            f"Likely Route:",
        ])
        
        for route_item in self.likely_route:
            lines.append(f"- {route_item}")
        
        lines.extend([
            "",
            f"Packet Readiness:",
            f"{self.packet_readiness}",
            "",
            f"Evidence Links:",
        ])
        
        for evidence_type, link in self.evidence_links.items():
            lines.append(f"- {evidence_type}: {link}")
        
        lines.extend([
            "",
            "---",
            "",
            "DISCLAIMERS:",
        ])
        
        for disclaimer in self.disclaimers:
            lines.append(f"- {disclaimer}")
        
        lines.extend([
            "",
            f"Generated by {self.evaluator_version} on {self.evaluated_at.strftime('%Y-%m-%d %H:%M:%S UTC')}",
        ])
        
        return "\n".join(lines)


class ProfessionalReviewCardGenerator:
    """
    Generates professional review cards from evaluation results.
    
    This creates the "professional feel" - judgment, not generic text.
    """
    
    def __init__(self):
        self.version = "job_description_intelligence_v1"
    
    def generate_card(
        self,
        asset_data: Dict[str, Any],
        grades: Dict[str, Any],
        committee_results: Dict[str, Any],
        strategic_classification: Dict[str, str],
        liquidification_plan: Dict[str, Any],
        capital_translation: Dict[str, Any],
    ) -> ProfessionalReviewCard:
        """
        Generate a professional review card.
        
        Args:
            asset_data: Asset metadata and classification
            grades: Professional grades
            committee_results: Committee evaluation results
            strategic_classification: Strategic value classification
            liquidification_plan: Liquidification plan
            capital_translation: Capital translation results
        
        Returns:
            ProfessionalReviewCard with complete professional assessment
        """
        # Extract basic information
        asset_id = asset_data.get("asset_id", "unknown")
        asset_name = asset_data.get("asset_name", "Unknown Asset")
        classification = asset_data.get("classification", "Unknown classification")
        
        # Extract grades
        production_grade = grades.get("production_grade", "C")
        commercial_grade = grades.get("commercial_grade", "C")
        collateral_grade = grades.get("collateral_grade", "C")
        financeability_score = grades.get("financeability_score", 0)
        
        # Extract proof level
        proof_level_value = grades.get("proof_level", 0)
        proof_level = ProofLevel(proof_level_value)
        
        # Extract strategic classification
        strategic_value = strategic_classification.get("strategic_value", "Unknown")
        buyer_today_value = strategic_classification.get("buyer_today_value", "Unknown")
        collateral_support = strategic_classification.get("collateral_support", "Unknown")
        
        # Extract blockers
        committee_report = committee_results.get("committee_report", {})
        all_blockers = committee_report.get("all_blockers", [])
        
        # Summarize main blockers (top 5)
        main_blockers = self._summarize_blockers(all_blockers)
        
        # Extract best next action from liquidification plan
        best_next_action = liquidification_plan.get("best_next_action", "Review asset for monetization potential")
        
        # Extract likely route
        buyer_universe = liquidification_plan.get("buyer_universe", [])
        likely_route = buyer_universe[:5] if buyer_universe else ["General software buyers"]
        
        # Determine packet readiness
        packet_readiness = self._determine_packet_readiness(
            grades,
            committee_results,
            liquidification_plan,
        )
        
        # Add standard disclaimers
        disclaimers = self._get_standard_disclaimers(grades, committee_results)
        
        # Add evidence links
        evidence_links = self._extract_evidence_links(asset_data, committee_results)
        
        return ProfessionalReviewCard(
            asset_id=asset_id,
            asset_name=asset_name,
            classification=classification,
            production_grade=production_grade,
            commercial_grade=commercial_grade,
            collateral_grade=collateral_grade,
            financeability_score=financeability_score,
            proof_level=proof_level,
            strategic_value=strategic_value,
            buyer_today_value=buyer_today_value,
            collateral_support=collateral_support,
            main_blockers=main_blockers,
            best_next_action=best_next_action,
            likely_route=likely_route,
            packet_readiness=packet_readiness,
            disclaimers=disclaimers,
            evidence_links=evidence_links,
            evaluator_version=self.version,
        )
    
    def _get_standard_disclaimers(self, grades: Dict[str, Any], committee_results: Dict[str, Any]) -> List[str]:
        """Get standard disclaimers for the review card."""
        disclaimers = [
            "This review card is a draft appraisal and diligence support document.",
            "It is not legal advice, not tax advice, not a guaranteed sale value, and not a loan approval.",
            "Human review is recommended before using this document for financial decisions.",
            "Appraisal is not liquidity. Financeability score does not guarantee marketability.",
            "Grades are based on available evidence and may change with additional information.",
        ]
        
        # Add specific disclaimers based on risk blocks
        risk_blocked = committee_results.get("committee_report", {}).get("risk_blocked", False)
        if risk_blocked:
            disclaimers.append("Asset has risk blockers that must be resolved before any monetization.")
        
        # Add disclaimer if financeability is low
        financeability = grades.get("financeability_score", 0)
        if financeability < 50:
            disclaimers.append("Low financeability score indicates significant development or cleanup required.")
        
        return disclaimers
    
    def _extract_evidence_links(self, asset_data: Dict[str, Any], committee_results: Dict[str, Any]) -> Dict[str, str]:
        """Extract verifiable evidence links from asset data."""
        evidence_links = {}
        
        # Add repo URL if available
        repo_url = asset_data.get("repo_url")
        if repo_url:
            evidence_links["Repository"] = repo_url
        
        # Add deployment URL if available
        deployment_url = asset_data.get("deployment_url")
        if deployment_url:
            evidence_links["Deployment"] = deployment_url
        
        # Add build log reference if available
        build_status = asset_data.get("build_status")
        if build_status == "passed":
            evidence_links["Build Status"] = "Passed - see CI/CD logs"
        
        # Add test status if available
        test_status = asset_data.get("test_status")
        if test_status == "passed":
            evidence_links["Test Status"] = "Passed - see test reports"
        
        return evidence_links
    
    def _summarize_blockers(self, blockers: List[str]) -> List[str]:
        """Summarize blockers to top 5 most critical."""
        if not blockers:
            return ["No critical blockers identified"]
        
        # Prioritize critical blockers
        critical = [b for b in blockers if "secret" in b.lower() or "private key" in b.lower()]
        major = [b for b in blockers if "ownership" in b.lower() or "license" in b.lower() or "build" in b.lower()]
        other = [b for b in blockers if b not in critical and b not in major]
        
        prioritized = critical + major + other
        return prioritized[:5]
    
    def _determine_packet_readiness(
        self,
        grades: Dict[str, Any],
        committee_results: Dict[str, Any],
        liquidification_plan: Dict[str, Any],
    ) -> str:
        """Determine packet readiness status."""
        financeability = grades.get("financeability_score", 0)
        production_grade = grades.get("production_grade", "F")
        collateral_grade = grades.get("collateral_grade", "F")
        
        # Check for risk blocks
        risk_blocked = committee_results.get("committee_report", {}).get("risk_blocked", False)
        
        if risk_blocked:
            return "Not ready - risk blockers must be resolved"
        
        # Check cleanup requirements
        required_cleanup = liquidification_plan.get("required_cleanup", [])
        has_cleanup = required_cleanup and "No critical cleanup required" not in required_cleanup
        
        if has_cleanup:
            return "Cleanup required before packaging"
        
        # Determine readiness based on grades
        buyer_ready = (
            production_grade in ["A", "B"] and
            commercial_grade in ["A", "B"] and
            financeability >= 60
        )
        
        lender_ready = (
            collateral_grade in ["A", "B"] and
            financeability >= 70
        )
        
        if lender_ready:
            return "Lender-ready after human review"
        elif buyer_ready:
            return "Buyer-ready after packaging. Lender-ready only after review and outcome evidence."
        elif financeability >= 50:
            return "Partially buyer-ready - requires packaging and documentation"
        else:
            return "Not ready - significant development or cleanup required"
    
    def generate_batch_cards(
        self,
        evaluations: List[Dict[str, Any]],
    ) -> List[ProfessionalReviewCard]:
        """
        Generate review cards for a batch of assets.
        
        Args:
            evaluations: List of evaluation dictionaries, each containing:
                - asset_data
                - grades
                - committee_results
                - strategic_classification
                - liquidification_plan
                - capital_translation
        
        Returns:
            List of ProfessionalReviewCard objects
        """
        cards = []
        
        for evaluation in evaluations:
            card = self.generate_card(
                asset_data=evaluation.get("asset_data", {}),
                grades=evaluation.get("grades", {}),
                committee_results=evaluation.get("committee_results", {}),
                strategic_classification=evaluation.get("strategic_classification", {}),
                liquidification_plan=evaluation.get("liquidification_plan", {}),
                capital_translation=evaluation.get("capital_translation", {}),
            )
            cards.append(card)
        
        return cards


class ReviewCardFormatter:
    """
    Formats review cards for different output channels.
    """
    
    @staticmethod
    def format_for_dashboard(card: ProfessionalReviewCard) -> Dict[str, Any]:
        """Format card for dashboard display."""
        return {
            "asset_name": card.asset_name,
            "financeability_score": card.financeability_score,
            "production_grade": card.production_grade,
            "commercial_grade": card.commercial_grade,
            "collateral_grade": card.collateral_grade,
            "strategic_value": card.strategic_value,
            "best_next_action": card.best_next_action,
            "risk_blocked": len(card.main_blockers) > 0 and "secret" in " ".join(card.main_blockers).lower(),
        }
    
    @staticmethod
    def format_for_email(card: ProfessionalReviewCard) -> str:
        """Format card for email notification."""
        subject = f"Asset Review: {card.asset_name} - {card.production_grade} Production Grade"
        
        body = f"""
Asset Review: {card.asset_name}

Classification: {card.classification}

Grades:
- Production: {card.production_grade}
- Commercial: {card.commercial_grade}
- Collateral: {card.collateral_grade}
- Financeability: {card.financeability_score}/100

Proof Level: {card.proof_level.display_name()}

Strategic Assessment:
- Strategic Value: {card.strategic_value}
- Buyer-Today Value: {card.buyer_today_value}
- Collateral Support: {card.collateral_support}

Main Blockers:
{chr(10).join(f'  - {b}' for b in card.main_blockers)}

Best Next Action:
{card.best_next_action}

Likely Route:
{chr(10).join(f'  - {r}' for r in card.likely_route)}

Packet Readiness:
{card.packet_readiness}

---
Generated by Job-Description Intelligence Engine v1
"""
        return subject, body
    
    @staticmethod
    def format_for_pdf(card: ProfessionalReviewCard) -> Dict[str, Any]:
        """Format card for PDF generation."""
        return {
            "title": f"Professional Asset Review: {card.asset_name}",
            "sections": [
                {
                    "heading": "Asset Classification",
                    "content": card.classification,
                },
                {
                    "heading": "Professional Grades",
                    "content": [
                        f"Production Grade: {card.production_grade}",
                        f"Commercial Grade: {card.commercial_grade}",
                        f"Collateral Grade: {card.collateral_grade}",
                        f"Financeability Score: {card.financeability_score}/100",
                    ],
                },
                {
                    "heading": "Proof Level",
                    "content": card.proof_level.display_name(),
                },
                {
                    "heading": "Strategic Assessment",
                    "content": [
                        f"Strategic Value: {card.strategic_value}",
                        f"Buyer-Today Value: {card.buyer_today_value}",
                        f"Collateral Support: {card.collateral_support}",
                    ],
                },
                {
                    "heading": "Main Blockers",
                    "content": card.main_blockers,
                },
                {
                    "heading": "Best Next Action",
                    "content": card.best_next_action,
                },
                {
                    "heading": "Likely Route",
                    "content": card.likely_route,
                },
                {
                    "heading": "Packet Readiness",
                    "content": card.packet_readiness,
                },
            ],
            "metadata": {
                "evaluated_at": card.evaluated_at.isoformat(),
                "evaluator_version": card.evaluator_version,
            },
        }
