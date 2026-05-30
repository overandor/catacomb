#!/usr/bin/env python3
"""
Asset Desk UI - Professional asset management interface.

The UI should not look like a file explorer. It should look like an asset desk.

Main views:
- Portfolio Balance Sheet
- Asset Register
- Financeability Queue
- Risk-Blocked Assets
- Buyer-Ready Assets
- Lender-Ready Assets
- Collateral Packet Candidates
- Agent Work Accounting
- Outcome Ledger

The dashboard should say:
"You have 121 discovered software objects.

17 are real assets.
31 are scaffolds.
12 are duplicates.
9 are risk-blocked.
6 are buyer-ready.
3 are collateral-packet candidates.
0 are fully financeable today.

Best next action:
Verify build and deployment proof for the top 3 assets."

That is the feel of a professional operation. It is honest, but useful.
"""

from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum


class AssetDeskView(Enum):
    """Main views for the asset desk."""
    PORTFOLIO_BALANCE_SHEET = "portfolio_balance_sheet"
    ASSET_REGISTER = "asset_register"
    FINANCEABILITY_QUEUE = "financeability_queue"
    RISK_BLOCKED_ASSETS = "risk_blocked_assets"
    BUYER_READY_ASSETS = "buyer_ready_assets"
    LENDER_READY_ASSETS = "lender_ready_assets"
    COLLATERAL_PACKET_CANDIDATES = "collateral_packet_candidates"
    AGENT_WORK_ACCOUNTING = "agent_work_accounting"
    OUTCOME_LEDGER = "outcome_ledger"


@dataclass
class PortfolioSummary:
    """Summary statistics for the portfolio."""
    total_discovered: int = 0
    real_assets: int = 0
    scaffolds: int = 0
    duplicates: int = 0
    risk_blocked: int = 0
    buyer_ready: int = 0
    lender_ready: int = 0
    collateral_packet_candidates: int = 0
    fully_financeable: int = 0
    
    # Value aggregates
    total_strategic_value_usd: float = 0
    total_collateral_support_usd: float = 0
    
    # Quality metrics
    average_production_grade: str = "C"
    average_commercial_grade: str = "C"
    average_collateral_grade: str = "C"
    average_financeability_score: float = 0
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "total_discovered": self.total_discovered,
            "real_assets": self.real_assets,
            "scaffolds": self.scaffolds,
            "duplicates": self.duplicates,
            "risk_blocked": self.risk_blocked,
            "buyer_ready": self.buyer_ready,
            "lender_ready": self.lender_ready,
            "collateral_packet_candidates": self.collateral_packet_candidates,
            "fully_financeable": self.fully_financeable,
            "total_strategic_value_usd": self.total_strategic_value_usd,
            "total_collateral_support_usd": self.total_collateral_support_usd,
            "average_production_grade": self.average_production_grade,
            "average_commercial_grade": self.average_commercial_grade,
            "average_collateral_grade": self.average_collateral_grade,
            "average_financeability_score": self.average_financeability_score,
        }


@dataclass
class AssetDeskDashboard:
    """
    Main dashboard for the asset desk.
    
    Provides a professional overview of the software asset portfolio.
    """
    portfolio_summary: PortfolioSummary
    best_next_action: str
    priority_assets: List[Dict[str, Any]]  # Top assets requiring attention
    recent_evaluations: List[Dict[str, Any]]  # Recently evaluated assets
    upcoming_deadlines: List[Dict[str, Any]]  # Actions with deadlines
    
    # Quick stats
    financeability_distribution: Dict[str, int]  # Distribution of financeability scores
    grade_distribution: Dict[str, int]  # Distribution of grades
    
    generated_at: datetime = field(default_factory=datetime.now)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "portfolio_summary": self.portfolio_summary.to_dict(),
            "best_next_action": self.best_next_action,
            "priority_assets": self.priority_assets,
            "recent_evaluations": self.recent_evaluations,
            "upcoming_deadlines": self.upcoming_deadlines,
            "financeability_distribution": self.financeability_distribution,
            "grade_distribution": self.grade_distribution,
            "generated_at": self.generated_at.isoformat(),
        }
    
    def to_markdown(self) -> str:
        """Generate markdown representation of the dashboard."""
        lines = [
            "# Asset Desk Dashboard",
            "",
            "## Portfolio Summary",
            "",
            f"You have {self.portfolio_summary.total_discovered} discovered software objects.",
            "",
            f"- {self.portfolio_summary.real_assets} are real assets",
            f"- {self.portfolio_summary.scaffolds} are scaffolds",
            f"- {self.portfolio_summary.duplicates} are duplicates",
            f"- {self.portfolio_summary.risk_blocked} are risk-blocked",
            f"- {self.portfolio_summary.buyer_ready} are buyer-ready",
            f"- {self.portfolio_summary.lender_ready} are lender-ready",
            f"- {self.portfolio_summary.collateral_packet_candidates} are collateral-packet candidates",
            f"- {self.portfolio_summary.fully_financeable} are fully financeable today",
            "",
            "## Best Next Action",
            "",
            self.best_next_action,
            "",
            "## Priority Assets",
            "",
        ]
        
        for i, asset in enumerate(self.priority_assets[:5], 1):
            lines.append(f"{i}. {asset.get('asset_name', 'Unknown')} - {asset.get('status', 'Unknown')}")
        
        lines.extend([
            "",
            "## Portfolio Metrics",
            "",
            f"Average Production Grade: {self.portfolio_summary.average_production_grade}",
            f"Average Commercial Grade: {self.portfolio_summary.average_commercial_grade}",
            f"Average Collateral Grade: {self.portfolio_summary.average_collateral_grade}",
            f"Average Financeability Score: {self.portfolio_summary.average_financeability_score:.1f}/100",
            "",
            f"Total Strategic Value: ${self.portfolio_summary.total_strategic_value_usd:,.2f}",
            f"Total Collateral Support: ${self.portfolio_summary.total_collateral_support_usd:,.2f}",
        ])
        
        return "\n".join(lines)


class AssetDeskUI:
    """
    Asset Desk UI - Professional asset management interface.
    
    Provides views and data structures for a professional asset desk.
    """
    
    def __init__(self):
        self.current_view = AssetDeskView.PORTFOLIO_BALANCE_SHEET
    
    def generate_dashboard(
        self,
        asset_evaluations: List[Dict[str, Any]],
    ) -> AssetDeskDashboard:
        """
        Generate the main dashboard.
        
        Args:
            asset_evaluations: List of evaluated assets with grades and classifications
        
        Returns:
            AssetDeskDashboard with complete portfolio overview
        """
        # Calculate portfolio summary
        portfolio_summary = self._calculate_portfolio_summary(asset_evaluations)
        
        # Determine best next action
        best_next_action = self._determine_best_next_action(portfolio_summary, asset_evaluations)
        
        # Identify priority assets
        priority_assets = self._identify_priority_assets(asset_evaluations)
        
        # Get recent evaluations
        recent_evaluations = self._get_recent_evaluations(asset_evaluations)
        
        # Calculate distributions
        financeability_distribution = self._calculate_financeability_distribution(asset_evaluations)
        grade_distribution = self._calculate_grade_distribution(asset_evaluations)
        
        # Get upcoming deadlines (placeholder for now)
        upcoming_deadlines = []
        
        return AssetDeskDashboard(
            portfolio_summary=portfolio_summary,
            best_next_action=best_next_action,
            priority_assets=priority_assets,
            recent_evaluations=recent_evaluations,
            upcoming_deadlines=upcoming_deadlines,
            financeability_distribution=financeability_distribution,
            grade_distribution=grade_distribution,
        )
    
    def _calculate_portfolio_summary(
        self,
        asset_evaluations: List[Dict[str, Any]],
    ) -> PortfolioSummary:
        """Calculate portfolio summary statistics."""
        summary = PortfolioSummary()
        
        if not asset_evaluations:
            return summary
        
        summary.total_discovered = len(asset_evaluations)
        
        # Count by classification
        for evaluation in asset_evaluations:
            asset_data = evaluation.get("asset_data", {})
            grades = evaluation.get("grades", {})
            committee_results = evaluation.get("committee_results", {})
            
            classification = asset_data.get("classification", "unknown")
            
            if classification == "real_production_system":
                summary.real_assets += 1
            elif classification == "scaffold":
                summary.scaffolds += 1
            elif classification == "duplicate":
                summary.duplicates += 1
            
            # Check risk blocked
            if committee_results.get("committee_report", {}).get("risk_blocked", False):
                summary.risk_blocked += 1
            
            # Check buyer ready
            financeability = grades.get("financeability_score", 0)
            production_grade = grades.get("production_grade", "F")
            commercial_grade = grades.get("commercial_grade", "F")
            
            if financeability >= 60 and production_grade in ["A", "B"] and commercial_grade in ["A", "B"]:
                summary.buyer_ready += 1
            
            # Check lender ready
            collateral_grade = grades.get("collateral_grade", "F")
            if financeability >= 70 and collateral_grade in ["A", "B"]:
                summary.lender_ready += 1
            
            # Check collateral packet candidates
            if financeability >= 50 and collateral_grade in ["B", "C"]:
                summary.collateral_packet_candidates += 1
            
            # Check fully financeable
            if financeability >= 80:
                summary.fully_financeable += 1
            
            # Aggregate values
            liquidification_plan = evaluation.get("liquidification_plan", {})
            price_range = liquidification_plan.get("expected_price_range", [0, 0])
            summary.total_strategic_value_usd += price_range[1]  # Use max as strategic value
            summary.total_collateral_support_usd += price_range[0]  # Use min as collateral support
        
        # Calculate averages
        production_grades = [e.get("grades", {}).get("production_grade", "C") for e in asset_evaluations]
        commercial_grades = [e.get("grades", {}).get("commercial_grade", "C") for e in asset_evaluations]
        collateral_grades = [e.get("grades", {}).get("collateral_grade", "C") for e in asset_evaluations]
        financeability_scores = [e.get("grades", {}).get("financeability_score", 0) for e in asset_evaluations]
        
        summary.average_production_grade = self._average_grade(production_grades)
        summary.average_commercial_grade = self._average_grade(commercial_grades)
        summary.average_collateral_grade = self._average_grade(collateral_grades)
        summary.average_financeability_score = sum(financeability_scores) / len(financeability_scores) if financeability_scores else 0
        
        return summary
    
    def _average_grade(self, grades: List[str]) -> str:
        """Calculate average grade from list of grades."""
        if not grades:
            return "C"
        
        grade_order = ["F", "D", "C-", "C", "C+", "B-", "B", "B+", "A-", "A", "A+"]
        grade_values = {grade: i for i, grade in enumerate(grade_order)}
        
        numeric_values = [grade_values.get(grade, 5) for grade in grades]
        average = sum(numeric_values) / len(numeric_values)
        
        return grade_order[int(round(average))]
    
    def _determine_best_next_action(
        self,
        portfolio_summary: PortfolioSummary,
        asset_evaluations: List[Dict[str, Any]],
    ) -> str:
        """Determine the single best next action for the portfolio."""
        # Priority: risk blockers > buyer-ready packaging > lender-ready packaging > development
        
        if portfolio_summary.risk_blocked > 0:
            return f"Resolve risk blockers for {portfolio_summary.risk_blocked} assets (secrets, ownership, license issues)"
        
        if portfolio_summary.buyer_ready > 0:
            return f"Package {portfolio_summary.buyer_ready} buyer-ready assets and begin outreach"
        
        if portfolio_summary.collateral_packet_candidates > 0:
            return f"Prepare collateral packets for {portfolio_summary.collateral_packet_candidates} assets"
        
        if portfolio_summary.real_assets > 0:
            return f"Verify build and deployment proof for the top {min(3, portfolio_summary.real_assets)} assets"
        
        if portfolio_summary.scaffolds > 0:
            return f"Review {portfolio_summary.scaffolds} scaffolds and extract custom work"
        
        return "Discover and evaluate new software assets"
    
    def _identify_priority_assets(
        self,
        asset_evaluations: List[Dict[str, Any]],
    ) -> List[Dict[str, Any]]:
        """Identify assets requiring priority attention."""
        priority_assets = []
        
        for evaluation in asset_evaluations:
            asset_data = evaluation.get("asset_data", {})
            grades = evaluation.get("grades", {})
            committee_results = evaluation.get("committee_results", {})
            liquidification_plan = evaluation.get("liquidification_plan", {})
            
            asset_name = asset_data.get("asset_name", "Unknown")
            financeability = grades.get("financeability_score", 0)
            
            # Risk blocked - highest priority
            if committee_results.get("committee_report", {}).get("risk_blocked", False):
                priority_assets.append({
                    "asset_name": asset_name,
                    "status": "RISK BLOCKED",
                    "priority": "critical",
                    "action": "Resolve blockers immediately",
                })
            
            # High financeability but not packaged
            elif financeability >= 70:
                required_cleanup = liquidification_plan.get("required_cleanup", [])
                if not required_cleanup or "No critical cleanup required" in required_cleanup:
                    priority_assets.append({
                        "asset_name": asset_name,
                        "status": "READY FOR PACKAGING",
                        "priority": "high",
                        "action": "Package for monetization",
                    })
            
            # Medium financeability with clear path
            elif financeability >= 50:
                priority_assets.append({
                    "asset_name": asset_name,
                    "status": "DEVELOPMENT CANDIDATE",
                    "priority": "medium",
                    "action": "Complete development milestones",
                })
        
        # Sort by priority
        priority_order = {"critical": 0, "high": 1, "medium": 2}
        priority_assets.sort(key=lambda x: priority_order.get(x["priority"], 3))
        
        return priority_assets[:10]
    
    def _get_recent_evaluations(
        self,
        asset_evaluations: List[Dict[str, Any]],
    ) -> List[Dict[str, Any]]:
        """Get recently evaluated assets."""
        # Sort by evaluation time (assuming we have timestamp)
        # For now, just return the last 5
        return asset_evaluations[-5:]
    
    def _calculate_financeability_distribution(
        self,
        asset_evaluations: List[Dict[str, Any]],
    ) -> Dict[str, int]:
        """Calculate distribution of financeability scores."""
        distribution = {
            "0-20": 0,
            "20-40": 0,
            "40-60": 0,
            "60-80": 0,
            "80-100": 0,
        }
        
        for evaluation in asset_evaluations:
            financeability = evaluation.get("grades", {}).get("financeability_score", 0)
            
            if financeability < 20:
                distribution["0-20"] += 1
            elif financeability < 40:
                distribution["20-40"] += 1
            elif financeability < 60:
                distribution["40-60"] += 1
            elif financeability < 80:
                distribution["60-80"] += 1
            else:
                distribution["80-100"] += 1
        
        return distribution
    
    def _calculate_grade_distribution(
        self,
        asset_evaluations: List[Dict[str, Any]],
    ) -> Dict[str, int]:
        """Calculate distribution of grades."""
        distribution = {
            "A": 0,
            "B": 0,
            "C": 0,
            "D": 0,
            "F": 0,
        }
        
        for evaluation in asset_evaluations:
            grades = evaluation.get("grades", {})
            production_grade = grades.get("production_grade", "F")
            
            if production_grade.startswith("A"):
                distribution["A"] += 1
            elif production_grade.startswith("B"):
                distribution["B"] += 1
            elif production_grade.startswith("C"):
                distribution["C"] += 1
            elif production_grade.startswith("D"):
                distribution["D"] += 1
            else:
                distribution["F"] += 1
        
        return distribution
    
    def generate_view(
        self,
        view: AssetDeskView,
        asset_evaluations: List[Dict[str, Any]],
    ) -> Dict[str, Any]:
        """
        Generate a specific view of the asset desk.
        
        Args:
            view: The view to generate
            asset_evaluations: List of evaluated assets
        
        Returns:
            View-specific data
        """
        if view == AssetDeskView.PORTFOLIO_BALANCE_SHEET:
            return self._generate_balance_sheet_view(asset_evaluations)
        elif view == AssetDeskView.ASSET_REGISTER:
            return self._generate_asset_register_view(asset_evaluations)
        elif view == AssetDeskView.FINANCEABILITY_QUEUE:
            return self._generate_financeability_queue_view(asset_evaluations)
        elif view == AssetDeskView.RISK_BLOCKED_ASSETS:
            return self._generate_risk_blocked_view(asset_evaluations)
        elif view == AssetDeskView.BUYER_READY_ASSETS:
            return self._generate_buyer_ready_view(asset_evaluations)
        elif view == AssetDeskView.LENDER_READY_ASSETS:
            return self._generate_lender_ready_view(asset_evaluations)
        elif view == AssetDeskView.COLLATERAL_PACKET_CANDIDATES:
            return self._generate_collateral_packet_candidates_view(asset_evaluations)
        else:
            return {"error": f"View {view.value} not implemented"}
    
    def _generate_balance_sheet_view(
        self,
        asset_evaluations: List[Dict[str, Any]],
    ) -> Dict[str, Any]:
        """Generate portfolio balance sheet view."""
        summary = self._calculate_portfolio_summary(asset_evaluations)
        
        assets_by_classification = {}
        for evaluation in asset_evaluations:
            classification = evaluation.get("asset_data", {}).get("classification", "unknown")
            if classification not in assets_by_classification:
                assets_by_classification[classification] = []
            assets_by_classification[classification].append(evaluation)
        
        return {
            "view": "portfolio_balance_sheet",
            "summary": summary.to_dict(),
            "assets_by_classification": {
                classification: [e.get("asset_data", {}).get("asset_name", "Unknown") for e in assets]
                for classification, assets in assets_by_classification.items()
            },
        }
    
    def _generate_asset_register_view(
        self,
        asset_evaluations: List[Dict[str, Any]],
    ) -> Dict[str, Any]:
        """Generate asset register view."""
        register = []
        
        for evaluation in asset_evaluations:
            asset_data = evaluation.get("asset_data", {})
            grades = evaluation.get("grades", {})
            
            register.append({
                "asset_id": asset_data.get("asset_id", "unknown"),
                "asset_name": asset_data.get("asset_name", "Unknown"),
                "classification": asset_data.get("classification", "unknown"),
                "production_grade": grades.get("production_grade", "C"),
                "commercial_grade": grades.get("commercial_grade", "C"),
                "collateral_grade": grades.get("collateral_grade", "C"),
                "financeability_score": grades.get("financeability_score", 0),
                "evaluated_at": evaluation.get("evaluated_at", datetime.now().isoformat()),
            })
        
        # Sort by financeability score
        register.sort(key=lambda x: x["financeability_score"], reverse=True)
        
        return {
            "view": "asset_register",
            "total_assets": len(register),
            "assets": register,
        }
    
    def _generate_financeability_queue_view(
        self,
        asset_evaluations: List[Dict[str, Any]],
    ) -> Dict[str, Any]:
        """Generate financeability queue view."""
        # Filter assets that are not yet financeable but have potential
        queue = []
        
        for evaluation in asset_evaluations:
            grades = evaluation.get("grades", {})
            financeability = grades.get("financeability_score", 0)
            
            if 40 <= financeability < 80:
                asset_data = evaluation.get("asset_data", {})
                liquidification_plan = evaluation.get("liquidification_plan", {})
                
                queue.append({
                    "asset_name": asset_data.get("asset_name", "Unknown"),
                    "financeability_score": financeability,
                    "best_next_action": liquidification_plan.get("best_next_action", "Review"),
                    "action_priority": liquidification_plan.get("action_priority", "medium"),
                })
        
        # Sort by financeability score
        queue.sort(key=lambda x: x["financeability_score"], reverse=True)
        
        return {
            "view": "financeability_queue",
            "total_in_queue": len(queue),
            "queue": queue,
        }
    
    def _generate_risk_blocked_view(
        self,
        asset_evaluations: List[Dict[str, Any]],
    ) -> Dict[str, Any]:
        """Generate risk-blocked assets view."""
        risk_blocked = []
        
        for evaluation in asset_evaluations:
            committee_results = evaluation.get("committee_results", {})
            if committee_results.get("committee_report", {}).get("risk_blocked", False):
                asset_data = evaluation.get("asset_data", {})
                blockers = committee_results.get("committee_report", {}).get("all_blockers", [])
                
                risk_blocked.append({
                    "asset_name": asset_data.get("asset_name", "Unknown"),
                    "blockers": blockers,
                    "asset_id": asset_data.get("asset_id", "unknown"),
                })
        
        return {
            "view": "risk_blocked_assets",
            "total_risk_blocked": len(risk_blocked),
            "assets": risk_blocked,
        }
    
    def _generate_buyer_ready_view(
        self,
        asset_evaluations: List[Dict[str, Any]],
    ) -> Dict[str, Any]:
        """Generate buyer-ready assets view."""
        buyer_ready = []
        
        for evaluation in asset_evaluations:
            grades = evaluation.get("grades", {})
            financeability = grades.get("financeability_score", 0)
            production_grade = grades.get("production_grade", "F")
            commercial_grade = grades.get("commercial_grade", "F")
            
            if financeability >= 60 and production_grade in ["A", "B"] and commercial_grade in ["A", "B"]:
                asset_data = evaluation.get("asset_data", {})
                liquidification_plan = evaluation.get("liquidification_plan", {})
                
                buyer_ready.append({
                    "asset_name": asset_data.get("asset_name", "Unknown"),
                    "primary_route": liquidification_plan.get("primary_route", "unknown"),
                    "expected_price_range": liquidification_plan.get("expected_price_range", [0, 0]),
                    "buyer_universe": liquidification_plan.get("buyer_universe", []),
                })
        
        return {
            "view": "buyer_ready_assets",
            "total_buyer_ready": len(buyer_ready),
            "assets": buyer_ready,
        }
    
    def _generate_lender_ready_view(
        self,
        asset_evaluations: List[Dict[str, Any]],
    ) -> Dict[str, Any]:
        """Generate lender-ready assets view."""
        lender_ready = []
        
        for evaluation in asset_evaluations:
            grades = evaluation.get("grades", {})
            financeability = grades.get("financeability_score", 0)
            collateral_grade = grades.get("collateral_grade", "F")
            
            if financeability >= 70 and collateral_grade in ["A", "B"]:
                asset_data = evaluation.get("asset_data", {})
                liquidification_plan = evaluation.get("liquidification_plan", {})
                
                lender_ready.append({
                    "asset_name": asset_data.get("asset_name", "Unknown"),
                    "collateral_support_range": liquidification_plan.get("expected_price_range", [0, 0]),
                    "liquidation_route": liquidification_plan.get("primary_route", "unknown"),
                })
        
        return {
            "view": "lender_ready_assets",
            "total_lender_ready": len(lender_ready),
            "assets": lender_ready,
        }
    
    def _generate_collateral_packet_candidates_view(
        self,
        asset_evaluations: List[Dict[str, Any]],
    ) -> Dict[str, Any]:
        """Generate collateral packet candidates view."""
        candidates = []
        
        for evaluation in asset_evaluations:
            grades = evaluation.get("grades", {})
            financeability = grades.get("financeability_score", 0)
            collateral_grade = grades.get("collateral_grade", "F")
            
            if financeability >= 50 and collateral_grade in ["B", "C"]:
                asset_data = evaluation.get("asset_data", {})
                
                candidates.append({
                    "asset_name": asset_data.get("asset_name", "Unknown"),
                    "collateral_grade": collateral_grade,
                    "financeability_score": financeability,
                    "status": "Candidate" if financeability >= 60 else "Development needed",
                })
        
        return {
            "view": "collateral_packet_candidates",
            "total_candidates": len(candidates),
            "assets": candidates,
        }
