#!/usr/bin/env python3
"""
Liquidification Layer - Finding the practical path to cash.

Liquidification means the product always asks: How does this asset move toward cash?

For each asset, it should generate a route:
- Sell as standalone codebase
- Package as micro-SaaS
- Turn into hosted API
- Turn into Hugging Face Space
- License to strategic buyer
- Sell as data/report package
- Submit to IP broker
- Submit to venture studio
- Submit to accelerator
- Offer to software M&A buyer
- Open-source with paid services
- Bundle with related repos
- Archive as non-financeable

Then it should assign:
- Expected buyer category
- Expected sale difficulty
- Expected sale timeline
- Expected forced-sale range
- Required cleanup before outreach
- Best next action

This is how the system stops being a dashboard and becomes a monetization operator.
"""

from enum import Enum
from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass, field
from datetime import datetime
import json


class LiquidationRoute(Enum):
    """Monetization routes for software assets."""
    STANDALONE_CODEBASE_SALE = "standalone_codebase_sale"
    MICRO_SAAS = "micro_saas"
    HOSTED_API = "hosted_api"
    HUGGING_FACE_SPACE = "hugging_face_space"
    STRATEGIC_LICENSE = "strategic_license"
    DATA_REPORT_PACKAGE = "data_report_package"
    IP_BROKER_SUBMISSION = "ip_broker_submission"
    VENTURE_STUDIO_SUBMISSION = "venture_studio_submission"
    ACCELERATOR_SUBMISSION = "accelerator_submission"
    SOFTWARE_MA_BUYER = "software_ma_buyer"
    OPEN_SOURCE_PAID_SERVICES = "open_source_paid_services"
    BUNDLE_WITH_REPOS = "bundle_with_repos"
    ARCHIVE_NON_FINANCEABLE = "archive_non_financeable"


class BuyerCategory(Enum):
    """Categories of potential buyers."""
    DEVELOPER_TOOLING_BUYERS = "developer_tooling_buyers"
    IP_CONSULTANTS = "ip_consultants"
    VENTURE_STUDIOS = "venture_studios"
    SOFTWARE_MA_ADVISORS = "software_ma_advisors"
    CORPORATE_ACQUIRERS = "corporate_acquirers"
    PRIVATE_EQUITY = "private_equity"
    STRATEGIC_BUYERS = "strategic_buyers"
    MARKETPLACES = "marketplaces"
    BROKERS = "brokers"
    ACCELERATORS = "accelerators"


class SaleDifficulty(Enum):
    """Expected difficulty of sale."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    VERY_HIGH = "very_high"


@dataclass
class LiquidificationPlan:
    """
    A complete liquidification plan for an asset.
    
    Answers: How does this asset move toward cash?
    """
    asset_id: str
    primary_route: LiquidationRoute
    alternative_routes: List[LiquidationRoute]
    
    # Buyer information
    expected_buyer_category: BuyerCategory
    buyer_universe: List[str]  # Specific buyer names or types
    
    # Sale expectations
    sale_difficulty: SaleDifficulty
    expected_timeline_days: Tuple[int, int]  # (min, max)
    expected_price_range: Tuple[float, float]  # (min, max) in USD
    
    # Requirements
    required_cleanup: List[str]
    required_packaging: List[str]
    
    # Action
    best_next_action: str
    action_priority: str  # immediate, short_term, long_term
    
    # Metadata
    confidence: float  # 0-1
    generated_at: datetime = field(default_factory=datetime.now)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "asset_id": self.asset_id,
            "primary_route": self.primary_route.value,
            "alternative_routes": [route.value for route in self.alternative_routes],
            "expected_buyer_category": self.expected_buyer_category.value,
            "buyer_universe": self.buyer_universe,
            "sale_difficulty": self.sale_difficulty.value,
            "expected_timeline_days": list(self.expected_timeline_days),
            "expected_price_range": list(self.expected_price_range),
            "required_cleanup": self.required_cleanup,
            "required_packaging": self.required_packaging,
            "best_next_action": self.best_next_action,
            "action_priority": self.action_priority,
            "confidence": self.confidence,
            "generated_at": self.generated_at.isoformat(),
        }


class LiquidificationEngine:
    """
    Liquidification Engine - Generates monetization routes.
    
    This is how the system becomes a monetization operator, not just a dashboard.
    """
    
    def __init__(self):
        self.route_criteria = {
            LiquidationRoute.STANDALONE_CODEBASE_SALE: {
                "min_production_grade": "B",
                "min_collateral_grade": "C",
                "requires": ["clear_ownership", "no_secrets", "buildable"],
            },
            LiquidationRoute.MICRO_SAAS: {
                "min_production_grade": "A-",
                "min_commercial_grade": "B",
                "requires": ["api_potential", "scalable", "market_fit"],
            },
            LiquidationRoute.HOSTED_API: {
                "min_production_grade": "B+",
                "min_execution_score": 70,
                "requires": ["api_endpoints", "deployable", "documentation"],
            },
            LiquidationRoute.HUGGING_FACE_SPACE: {
                "min_production_grade": "C",
                "requires": ["ml_model", "demo_ready", "documentation"],
            },
            LiquidationRoute.STRATEGIC_LICENSE: {
                "min_production_grade": "B",
                "min_commercial_grade": "B",
                "requires": ["clear_license", "strategic_value", "ip_clarity"],
            },
            LiquidationRoute.DATA_REPORT_PACKAGE: {
                "min_production_grade": "C",
                "requires": ["data_value", "analysis_capability", "report_generation"],
            },
            LiquidationRoute.IP_BROKER_SUBMISSION: {
                "min_production_grade": "B",
                "min_collateral_grade": "B",
                "requires": ["clear_ownership", "market_value", "documentation"],
            },
            LiquidationRoute.VENTURE_STUDIO_SUBMISSION: {
                "min_production_grade": "B-",
                "min_commercial_grade": "B-",
                "requires": ["growth_potential", "scalable", "market_fit"],
            },
            LiquidationRoute.ACCELERATOR_SUBMISSION: {
                "min_production_grade": "C+",
                "requires": ["prototype", "team", "vision"],
            },
            LiquidationRoute.SOFTWARE_MA_BUYER: {
                "min_production_grade": "A-",
                "min_collateral_grade": "B+",
                "requires": ["production_ready", "revenue", "clear_ownership"],
            },
            LiquidationRoute.OPEN_SOURCE_PAID_SERVICES: {
                "min_production_grade": "B",
                "requires": ["community", "support_model", "documentation"],
            },
            LiquidationRoute.BUNDLE_WITH_REPOS: {
                "min_production_grade": "C",
                "requires": ["related_assets", "synergy", "packaging"],
            },
        }
    
    def generate_liquidification_plan(
        self,
        asset_data: Dict[str, Any],
        grades: Dict[str, Any],
        committee_results: Dict[str, Any],
    ) -> LiquidificationPlan:
        """
        Generate a complete liquidification plan.
        
        Args:
            asset_data: Asset metadata and classification
            grades: Professional grades
            committee_results: Committee evaluation results
        
        Returns:
            LiquidificationPlan with monetization strategy
        """
        # Determine eligible routes
        eligible_routes = self._determine_eligible_routes(asset_data, grades, committee_results)
        
        # Select primary route
        primary_route = self._select_primary_route(eligible_routes, asset_data, grades)
        
        # Determine buyer category
        buyer_category = self._determine_buyer_category(primary_route, asset_data, grades)
        
        # Generate buyer universe
        buyer_universe = self._generate_buyer_universe(buyer_category, asset_data)
        
        # Estimate sale difficulty
        sale_difficulty = self._estimate_sale_difficulty(primary_route, grades, committee_results)
        
        # Estimate timeline
        timeline = self._estimate_timeline(primary_route, sale_difficulty, grades)
        
        # Estimate price range
        price_range = self._estimate_price_range(grades, committee_results, asset_data)
        
        # Determine required cleanup
        required_cleanup = self._determine_required_cleanup(committee_results, asset_data)
        
        # Determine required packaging
        required_packaging = self._determine_required_packaging(primary_route, asset_data)
        
        # Generate best next action
        best_next_action = self._generate_best_next_action(
            primary_route,
            required_cleanup,
            required_packaging,
            grades,
        )
        
        # Determine action priority
        action_priority = self._determine_action_priority(
            primary_route,
            required_cleanup,
            grades,
        )
        
        # Calculate confidence
        confidence = self._calculate_confidence(grades, committee_results)
        
        return LiquidificationPlan(
            asset_id=asset_data.get("asset_id", "unknown"),
            primary_route=primary_route,
            alternative_routes=[r for r in eligible_routes if r != primary_route],
            expected_buyer_category=buyer_category,
            buyer_universe=buyer_universe,
            sale_difficulty=sale_difficulty,
            expected_timeline_days=timeline,
            expected_price_range=price_range,
            required_cleanup=required_cleanup,
            required_packaging=required_packaging,
            best_next_action=best_next_action,
            action_priority=action_priority,
            confidence=confidence,
        )
    
    def _determine_eligible_routes(
        self,
        asset_data: Dict[str, Any],
        grades: Dict[str, Any],
        committee_results: Dict[str, Any],
    ) -> List[LiquidationRoute]:
        """Determine which liquidation routes are eligible."""
        eligible = []
        
        production_grade = grades.get("production_grade", "F")
        commercial_grade = grades.get("commercial_grade", "F")
        collateral_grade = grades.get("collateral_grade", "F")
        execution_score = grades.get("execution_proof", 0)
        
        # Check for risk blocks
        risk_blocked = committee_results.get("committee_report", {}).get("risk_blocked", False)
        
        for route, criteria in self.route_criteria.items():
            # Skip if risk blocked (except archive)
            if risk_blocked and route != LiquidationRoute.ARCHIVE_NON_FINANCEABLE:
                continue
            
            # Check production grade
            min_prod = criteria.get("min_production_grade", "F")
            if not self._grade_meets_minimum(production_grade, min_prod):
                continue
            
            # Check commercial grade if required
            min_comm = criteria.get("min_commercial_grade")
            if min_comm and not self._grade_meets_minimum(commercial_grade, min_comm):
                continue
            
            # Check collateral grade if required
            min_coll = criteria.get("min_collateral_grade")
            if min_coll and not self._grade_meets_minimum(collateral_grade, min_coll):
                continue
            
            # Check execution score if required
            min_exec = criteria.get("min_execution_score")
            if min_exec and execution_score < min_exec:
                continue
            
            # Check asset-specific requirements
            if not self._check_route_requirements(route, asset_data):
                continue
            
            eligible.append(route)
        
        # Always add archive as fallback
        if LiquidationRoute.ARCHIVE_NON_FINANCEABLE not in eligible:
            eligible.append(LiquidationRoute.ARCHIVE_NON_FINANCEABLE)
        
        return eligible
    
    def _grade_meets_minimum(self, grade: str, minimum: str) -> bool:
        """Check if grade meets minimum requirement."""
        grade_order = ["F", "D", "C-", "C", "C+", "B-", "B", "B+", "A-", "A", "A+"]
        
        try:
            grade_idx = grade_order.index(grade)
            min_idx = grade_order.index(minimum)
            return grade_idx >= min_idx
        except ValueError:
            return False
    
    def _check_route_requirements(self, route: LiquidationRoute, asset_data: Dict[str, Any]) -> bool:
        """Check route-specific requirements."""
        criteria = self.route_criteria[route]
        required = criteria.get("requires", [])
        
        for requirement in required:
            if requirement == "clear_ownership":
                if not asset_data.get("has_ownership_clarity", False):
                    return False
            elif requirement == "no_secrets":
                if asset_data.get("secrets_detected", []):
                    return False
            elif requirement == "buildable":
                if asset_data.get("build_status") != "passed":
                    return False
            elif requirement == "api_potential":
                if not asset_data.get("has_api_potential", False):
                    return False
            elif requirement == "scalable":
                if not asset_data.get("is_scalable", False):
                    return False
            elif requirement == "market_fit":
                if not asset_data.get("has_market_fit", False):
                    return False
            elif requirement == "api_endpoints":
                if not asset_data.get("has_endpoints", False):
                    return False
            elif requirement == "deployable":
                if asset_data.get("deployment_status") not in ["deployed", "deployable"]:
                    return False
            elif requirement == "documentation":
                if not asset_data.get("has_documentation", False):
                    return False
            elif requirement == "ml_model":
                if asset_data.get("asset_type") != "model":
                    return False
            elif requirement == "demo_ready":
                if not asset_data.get("has_demo", False):
                    return False
            elif requirement == "clear_license":
                if not asset_data.get("has_license", False):
                    return False
            elif requirement == "strategic_value":
                if not asset_data.get("has_strategic_value", False):
                    return False
            elif requirement == "ip_clarity":
                if not asset_data.get("has_ownership_clarity", False):
                    return False
            elif requirement == "data_value":
                if not asset_data.get("has_data_value", False):
                    return False
            elif requirement == "analysis_capability":
                if not asset_data.get("has_analysis_capability", False):
                    return False
            elif requirement == "report_generation":
                if not asset_data.get("has_report_generation", False):
                    return False
            elif requirement == "market_value":
                if grades := asset_data.get("grades"):
                    if grades.get("commercial_grade") in ["D", "F"]:
                        return False
            elif requirement == "growth_potential":
                if not asset_data.get("has_growth_potential", False):
                    return False
            elif requirement == "revenue":
                if not asset_data.get("revenue_evidence", []):
                    return False
            elif requirement == "community":
                if not asset_data.get("has_community", False):
                    return False
            elif requirement == "support_model":
                if not asset_data.get("has_support_model", False):
                    return False
            elif requirement == "related_assets":
                if not asset_data.get("related_assets", []):
                    return False
            elif requirement == "synergy":
                if not asset_data.get("has_synergy", False):
                    return False
            elif requirement == "packaging":
                if not asset_data.get("is_packagable", False):
                    return False
            elif requirement == "prototype":
                classification = asset_data.get("classification", "")
                if "prototype" not in classification.lower():
                    return False
            elif requirement == "team":
                if not asset_data.get("has_team", False):
                    return False
            elif requirement == "vision":
                if not asset_data.get("has_vision", False):
                    return False
            elif requirement == "production_ready":
                if grades := asset_data.get("grades"):
                    if grades.get("production_grade") not in ["A", "B"]:
                        return False
        
        return True
    
    def _select_primary_route(
        self,
        eligible_routes: List[LiquidationRoute],
        asset_data: Dict[str, Any],
        grades: Dict[str, Any],
    ) -> LiquidationRoute:
        """Select the primary liquidification route."""
        if not eligible_routes:
            return LiquidationRoute.ARCHIVE_NON_FINANCEABLE
        
        # Priority order for route selection
        priority_order = [
            LiquidationRoute.SOFTWARE_MA_BUYER,
            LiquidationRoute.MICRO_SAAS,
            LiquidationRoute.HOSTED_API,
            LiquidationRoute.STRATEGIC_LICENSE,
            LiquidationRoute.STANDALONE_CODEBASE_SALE,
            LiquidationRoute.IP_BROKER_SUBMISSION,
            LiquidationRoute.VENTURE_STUDIO_SUBMISSION,
            LiquidationRoute.HUGGING_FACE_SPACE,
            LiquidationRoute.DATA_REPORT_PACKAGE,
            LiquidationRoute.OPEN_SOURCE_PAID_SERVICES,
            LiquidationRoute.BUNDLE_WITH_REPOS,
            LiquidationRoute.ACCELERATOR_SUBMISSION,
            LiquidationRoute.ARCHIVE_NON_FINANCEABLE,
        ]
        
        # Select highest priority eligible route
        for route in priority_order:
            if route in eligible_routes:
                return route
        
        return eligible_routes[0]
    
    def _determine_buyer_category(
        self,
        route: LiquidationRoute,
        asset_data: Dict[str, Any],
        grades: Dict[str, Any],
    ) -> BuyerCategory:
        """Determine the expected buyer category."""
        route_to_category = {
            LiquidationRoute.STANDALONE_CODEBASE_SALE: BuyerCategory.DEVELOPER_TOOLING_BUYERS,
            LiquidationRoute.MICRO_SAAS: BuyerCategory.STRATEGIC_BUYERS,
            LiquidationRoute.HOSTED_API: BuyerCategory.DEVELOPER_TOOLING_BUYERS,
            LiquidationRoute.HUGGING_FACE_SPACE: BuyerCategory.MARKETPLACES,
            LiquidationRoute.STRATEGIC_LICENSE: BuyerCategory.STRATEGIC_BUYERS,
            LiquidationRoute.DATA_REPORT_PACKAGE: BuyerCategory.IP_CONSULTANTS,
            LiquidationRoute.IP_BROKER_SUBMISSION: BuyerCategory.BROKERS,
            LiquidationRoute.VENTURE_STUDIO_SUBMISSION: BuyerCategory.VENTURE_STUDIOS,
            LiquidationRoute.ACCELERATOR_SUBMISSION: BuyerCategory.ACCELERATORS,
            LiquidationRoute.SOFTWARE_MA_BUYER: BuyerCategory.SOFTWARE_MA_ADVISORS,
            LiquidationRoute.OPEN_SOURCE_PAID_SERVICES: BuyerCategory.DEVELOPER_TOOLING_BUYERS,
            LiquidationRoute.BUNDLE_WITH_REPOS: BuyerCategory.DEVELOPER_TOOLING_BUYERS,
            LiquidationRoute.ARCHIVE_NON_FINANCEABLE: BuyerCategory.DEVELOPER_TOOLING_BUYERS,
        }
        
        return route_to_category.get(route, BuyerCategory.DEVELOPER_TOOLING_BUYERS)
    
    def _generate_buyer_universe(
        self,
        buyer_category: BuyerCategory,
        asset_data: Dict[str, Any],
    ) -> List[str]:
        """Generate a list of potential buyers."""
        category = asset_data.get("category", "unknown")
        
        buyer_universes = {
            BuyerCategory.DEVELOPER_TOOLING_BUYERS: [
                "Developer tooling companies",
                "IDE vendors",
                "Code platform providers",
                "DevOps tool companies",
            ],
            BuyerCategory.IP_CONSULTANTS: [
                "IP consulting firms",
                "Technology transfer offices",
                "Patent licensing firms",
                "IP brokers",
            ],
            BuyerCategory.VENTURE_STUDIOS: [
                "Venture studios",
                "Startup accelerators",
                "Corporate innovation labs",
                "Technology incubators",
            ],
            BuyerCategory.SOFTWARE_MA_ADVISORS: [
                "Software M&A advisors",
                "Technology investment banks",
                "Private equity tech funds",
                "Strategic acquirers",
            ],
            BuyerCategory.CORPORATE_ACQUIRERS: [
                "Fortune 500 tech acquirers",
                "Corporate development teams",
                "Strategic buyers",
            ],
            BuyerCategory.PRIVATE_EQUITY: [
                "Tech-focused PE firms",
                "Growth equity funds",
                "Buyout funds",
            ],
            BuyerCategory.STRATEGIC_BUYERS: [
                "Competitors in adjacent markets",
                "Platform companies",
                "Strategic acquirers",
            ],
            BuyerCategory.MARKETPLACES: [
                "Hugging Face",
                "GitHub Marketplace",
                "NPM/PyPI ecosystem",
                "API marketplaces",
            ],
            BuyerCategory.BROKERS: [
                "IP brokers",
                "Technology brokers",
                "Software asset brokers",
            ],
            BuyerCategory.ACCELERATORS: [
                "Y Combinator",
                "Techstars",
                "Industry-specific accelerators",
                "Corporate accelerators",
            ],
        }
        
        universe = buyer_universes.get(buyer_category, ["General software buyers"])
        
        # Add category-specific buyers
        if category == "machine_learning":
            universe.extend(["ML platform companies", "AI infrastructure firms"])
        elif category == "developer_tools":
            universe.extend(["IDE vendors", "DevOps companies"])
        elif category == "fintech":
            universe.extend(["Fintech acquirers", "Banks"])
        
        return universe
    
    def _estimate_sale_difficulty(
        self,
        route: LiquidationRoute,
        grades: Dict[str, Any],
        committee_results: Dict[str, Any],
    ) -> SaleDifficulty:
        """Estimate the difficulty of sale."""
        financeability = grades.get("financeability_score", 0)
        commercial_grade = grades.get("commercial_grade", "F")
        
        # Check for blockers
        blockers = committee_results.get("committee_report", {}).get("all_blockers", [])
        
        if blockers:
            return SaleDifficulty.VERY_HIGH
        
        if financeability >= 80 and commercial_grade in ["A", "B"]:
            return SaleDifficulty.LOW
        elif financeability >= 60 and commercial_grade in ["B", "C"]:
            return SaleDifficulty.MEDIUM
        elif financeability >= 40:
            return SaleDifficulty.HIGH
        else:
            return SaleDifficulty.VERY_HIGH
    
    def _estimate_timeline(
        self,
        route: LiquidationRoute,
        difficulty: SaleDifficulty,
        grades: Dict[str, Any],
    ) -> Tuple[int, int]:
        """Estimate sale timeline in days."""
        base_timelines = {
            LiquidationRoute.STANDALONE_CODEBASE_SALE: (30, 90),
            LiquidationRoute.MICRO_SAAS: (60, 180),
            LiquidationRoute.HOSTED_API: (30, 60),
            LiquidationRoute.HUGGING_FACE_SPACE: (7, 30),
            LiquidationRoute.STRATEGIC_LICENSE: (60, 180),
            LiquidationRoute.DATA_REPORT_PACKAGE: (14, 45),
            LiquidationRoute.IP_BROKER_SUBMISSION: (30, 90),
            LiquidationRoute.VENTURE_STUDIO_SUBMISSION: (30, 90),
            LiquidationRoute.ACCELERATOR_SUBMISSION: (30, 60),
            LiquidationRoute.SOFTWARE_MA_BUYER: (90, 180),
            LiquidationRoute.OPEN_SOURCE_PAID_SERVICES: (90, 365),
            LiquidationRoute.BUNDLE_WITH_REPOS: (30, 90),
            LiquidationRoute.ARCHIVE_NON_FINANCEABLE: (0, 0),
        }
        
        base_min, base_max = base_timelines.get(route, (30, 90))
        
        # Adjust based on difficulty
        difficulty_multiplier = {
            SaleDifficulty.LOW: 1.0,
            SaleDifficulty.MEDIUM: 1.5,
            SaleDifficulty.HIGH: 2.0,
            SaleDifficulty.VERY_HIGH: 3.0,
        }
        
        multiplier = difficulty_multiplier.get(difficulty, 1.5)
        
        return (int(base_min * multiplier), int(base_max * multiplier))
    
    def _estimate_price_range(
        self,
        grades: Dict[str, Any],
        committee_results: Dict[str, Any],
        asset_data: Dict[str, Any],
    ) -> Tuple[float, float]:
        """Estimate price range in USD."""
        financeability = grades.get("financeability_score", 0)
        
        # Base price ranges based on financeability
        if financeability >= 80:
            base_min, base_max = 50000, 500000
        elif financeability >= 60:
            base_min, base_max = 25000, 250000
        elif financeability >= 40:
            base_min, base_max = 10000, 100000
        elif financeability >= 20:
            base_min, base_max = 5000, 50000
        else:
            base_min, base_max = 0, 10000
        
        # Adjust based on revenue evidence
        revenue_evidence = asset_data.get("revenue_evidence", [])
        if revenue_evidence:
            base_max *= 2
        
        # Adjust based on strategic value
        if asset_data.get("has_strategic_value", False):
            base_max *= 1.5
        
        return (base_min, base_max)
    
    def _determine_required_cleanup(
        self,
        committee_results: Dict[str, Any],
        asset_data: Dict[str, Any],
    ) -> List[str]:
        """Determine required cleanup before monetization."""
        cleanup = []
        
        blockers = committee_results.get("committee_report", {}).get("all_blockers", [])
        
        for blocker in blockers:
            if "secret" in blocker.lower():
                cleanup.append("Remove all secrets and use environment variables")
            elif "private key" in blocker.lower():
                cleanup.append("Remove all private keys")
            elif "ownership" in blocker.lower():
                cleanup.append("Clarify ownership through documentation")
            elif "license" in blocker.lower():
                cleanup.append("Add appropriate license file")
            elif "build" in blocker.lower():
                cleanup.append("Fix build issues")
            elif "scaffold" in blocker.lower():
                cleanup.append("Remove scaffolding and retain custom work")
        
        # Add standard cleanup if needed
        if not asset_data.get("has_documentation", False):
            cleanup.append("Add comprehensive documentation")
        
        if asset_data.get("build_status") != "passed":
            cleanup.append("Ensure build passes")
        
        return cleanup if cleanup else ["No critical cleanup required"]
    
    def _determine_required_packaging(
        self,
        route: LiquidationRoute,
        asset_data: Dict[str, Any],
    ) -> List[str]:
        """Determine required packaging for the route."""
        packaging = []
        
        route_packaging = {
            LiquidationRoute.STANDALONE_CODEBASE_SALE: [
                "Create sale packet with technical documentation",
                "Prepare code transfer documentation",
                "Generate usage examples",
            ],
            LiquidationRoute.MICRO_SAAS: [
                "Package as deployable SaaS",
                "Create pricing model",
                "Prepare hosting infrastructure",
            ],
            LiquidationRoute.HOSTED_API: [
                "Package as API service",
                "Create API documentation",
                "Set up hosting",
            ],
            LiquidationRoute.HUGGING_FACE_SPACE: [
                "Prepare model for Hugging Face",
                "Create demo notebook",
                "Write model card",
            ],
            LiquidationRoute.STRATEGIC_LICENSE: [
                "Prepare licensing terms",
                "Document IP rights",
                "Create license agreement template",
            ],
            LiquidationRoute.DATA_REPORT_PACKAGE: [
                "Package data with documentation",
                "Create report template",
                "Document data sources",
            ],
            LiquidationRoute.IP_BROKER_SUBMISSION: [
                "Create IP summary",
                "Prepare valuation report",
                "Document ownership chain",
            ],
            LiquidationRoute.VENTURE_STUDIO_SUBMISSION: [
                "Create pitch deck",
                "Document growth metrics",
                "Prepare team information",
            ],
            LiquidationRoute.ACCELERATOR_SUBMISSION: [
                "Create application materials",
                "Document prototype status",
                "Prepare team information",
            ],
            LiquidationRoute.SOFTWARE_MA_BUYER: [
                "Create comprehensive diligence packet",
                "Prepare financial documentation",
                "Document technical architecture",
            ],
            LiquidationRoute.OPEN_SOURCE_PAID_SERVICES: [
                "Prepare open-source release",
                "Define support model",
                "Create pricing for services",
            ],
            LiquidationRoute.BUNDLE_WITH_REPOS: [
                "Identify related assets",
                "Create bundle documentation",
                "Define bundle pricing",
            ],
            LiquidationRoute.ARCHIVE_NON_FINANCEABLE: [
                "Document archival decision",
                "Create summary record",
            ],
        }
        
        return route_packaging.get(route, ["Prepare standard packaging"])
    
    def _generate_best_next_action(
        self,
        route: LiquidationRoute,
        required_cleanup: List[str],
        required_packaging: List[str],
        grades: Dict[str, Any],
    ) -> str:
        """Generate the single best next action."""
        # If critical cleanup needed, that's the action
        critical_cleanup = [c for c in required_cleanup if "secret" in c.lower() or "private key" in c.lower()]
        if critical_cleanup:
            return f"CRITICAL: {critical_cleanup[0]}"
        
        # If cleanup needed, do that first
        if required_cleanup and "No critical cleanup required" not in required_cleanup:
            return f"Complete cleanup: {required_cleanup[0]}"
        
        # If packaging needed, do that
        if required_packaging:
            return f"Complete packaging: {required_packaging[0]}"
        
        # Route-specific actions
        route_actions = {
            LiquidationRoute.STANDALONE_CODEBASE_SALE: "Prepare sale packet and begin outreach to developer tooling buyers",
            LiquidationRoute.MICRO_SAAS: "Deploy as SaaS and begin customer acquisition",
            LiquidationRoute.HOSTED_API: "Deploy API and create integration documentation",
            LiquidationRoute.HUGGING_FACE_SPACE: "Upload to Hugging Face and promote in community",
            LiquidationRoute.STRATEGIC_LICENSE: "Identify strategic buyers and prepare licensing terms",
            LiquidationRoute.DATA_REPORT_PACKAGE: "Package data and reach out to IP consultants",
            LiquidationRoute.IP_BROKER_SUBMISSION: "Submit to IP broker with valuation report",
            LiquidationRoute.VENTURE_STUDIO_SUBMISSION: "Apply to venture studios with pitch deck",
            LiquidationRoute.ACCELERATOR_SUBMISSION: "Apply to relevant accelerators",
            LiquidationRoute.SOFTWARE_MA_BUYER: "Engage software M&A advisor and prepare diligence packet",
            LiquidationRoute.OPEN_SOURCE_PAID_SERVICES: "Release as open-source and define support services",
            LiquidationRoute.BUNDLE_WITH_REPOS: "Identify related repos and create bundle package",
            LiquidationRoute.ARCHIVE_NON_FINANCEABLE: "Archive asset and focus on higher-priority projects",
        }
        
        return route_actions.get(route, "Review and refine asset for monetization")
    
    def _determine_action_priority(
        self,
        route: LiquidationRoute,
        required_cleanup: List[str],
        grades: Dict[str, Any],
    ) -> str:
        """Determine action priority."""
        critical_cleanup = [c for c in required_cleanup if "secret" in c.lower() or "private key" in c.lower()]
        if critical_cleanup:
            return "immediate"
        
        if required_cleanup and "No critical cleanup required" not in required_cleanup:
            return "immediate"
        
        financeability = grades.get("financeability_score", 0)
        if financeability >= 70:
            return "immediate"
        elif financeability >= 50:
            return "short_term"
        else:
            return "long_term"
    
    def _calculate_confidence(
        self,
        grades: Dict[str, Any],
        committee_results: Dict[str, Any],
    ) -> float:
        """Calculate confidence in the liquidification plan."""
        financeability = grades.get("financeability_score", 0)
        
        # Higher financeability = higher confidence
        base_confidence = financeability / 100
        
        # Reduce confidence if risk blocked
        if committee_results.get("committee_report", {}).get("risk_blocked", False):
            base_confidence *= 0.5
        
        return min(1.0, max(0.3, base_confidence))
