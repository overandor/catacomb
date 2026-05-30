#!/usr/bin/env python3
"""
One Best Next Action Recommendation Engine.

This is important.

Do not end with twenty vague recommendations.
End with one main action.

Examples:
- Best next action: Add a reproducible build log and deployment URL.
- Best next action: Resolve license ambiguity before generating a buyer packet.
- Best next action: Bundle this with two related repos and package as a single API product.
- Best next action: Send the buyer memo to 20 qualified targets and record responses.
- Best next action: Do not monetize yet. Remove secrets and separate original code from forked code.

This makes the system feel like a specialist, not a chatbot.
"""

from typing import Dict, Any, List, Optional
from dataclasses import dataclass
from enum import Enum
from datetime import datetime


class ActionPriority(Enum):
    """Priority levels for actions."""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class ActionCategory(Enum):
    """Categories of actions."""
    CLEANUP = "cleanup"
    DEVELOPMENT = "development"
    PACKAGING = "packaging"
    OUTREACH = "outreach"
    DOCUMENTATION = "documentation"
    VERIFICATION = "verification"
    STRATEGIC = "strategic"


@dataclass
class NextAction:
    """
    A single recommended next action.
    
    The system should end with ONE main action, not twenty vague recommendations.
    """
    action: str
    priority: ActionPriority
    category: ActionCategory
    rationale: str
    estimated_effort_hours: float
    dependencies: List[str]  # Actions that must be completed first
    success_criteria: List[str]  # How to know if the action succeeded
    alternative_actions: List[str]  # Alternative approaches if the main action fails
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "action": self.action,
            "priority": self.priority.value,
            "category": self.category.value,
            "rationale": self.rationale,
            "estimated_effort_hours": self.estimated_effort_hours,
            "dependencies": self.dependencies,
            "success_criteria": self.success_criteria,
            "alternative_actions": self.alternative_actions,
        }


class NextActionEngine:
    """
    One Best Next Action Recommendation Engine.
    
    Generates a single, clear, actionable recommendation for each asset.
    This makes the system feel like a specialist, not a chatbot.
    """
    
    def __init__(self):
        self.action_templates = {
            # Cleanup actions
            "remove_secrets": {
                "action": "Remove all secrets and private keys from code",
                "category": ActionCategory.CLEANUP,
                "priority": ActionPriority.CRITICAL,
                "rationale": "Security risk blocks all monetization - must be resolved first",
                "estimated_effort_hours": 2.0,
                "success_criteria": ["Secret scan returns zero results", "No hardcoded credentials in code"],
                "alternative_actions": ["Use environment variables for all secrets", "Implement secret management system"],
            },
            "resolve_ownership": {
                "action": "Clarify ownership through documentation and attribution",
                "category": ActionCategory.CLEANUP,
                "priority": ActionPriority.CRITICAL,
                "rationale": "Ownership ambiguity blocks collateral treatment",
                "estimated_effort_hours": 4.0,
                "success_criteria": ["Ownership statement documented", "All contributors attributed", "License file present"],
                "alternative_actions": ["Obtain IP assignment from employer", "Separate personal work from employer work"],
            },
            "fix_build": {
                "action": "Fix build issues and ensure project builds successfully",
                "category": ActionCategory.DEVELOPMENT,
                "priority": ActionPriority.HIGH,
                "rationale": "Build failure prevents execution proof and deployment",
                "estimated_effort_hours": 8.0,
                "success_criteria": ["Build passes on all platforms", "CI/CD pipeline green", "No build errors"],
                "alternative_actions": ["Simplify build configuration", "Remove broken dependencies"],
            },
            
            # Development actions
            "add_tests": {
                "action": "Add comprehensive test suite with >70% coverage",
                "category": ActionCategory.DEVELOPMENT,
                "priority": ActionPriority.HIGH,
                "rationale": "Tests are required for production grade and buyer confidence",
                "estimated_effort_hours": 16.0,
                "success_criteria": ["Test coverage >70%", "All tests pass", "CI runs tests automatically"],
                "alternative_actions": ["Add integration tests only", "Focus on critical path testing"],
            },
            "add_ci_cd": {
                "action": "Configure CI/CD pipeline with automated testing and deployment",
                "category": ActionCategory.DEVELOPMENT,
                "priority": ActionPriority.HIGH,
                "rationale": "CI/CD is required for production grade and operational credibility",
                "estimated_effort_hours": 8.0,
                "success_criteria": ["CI/CD pipeline configured", "Automated tests run on commit", "Deployment automated"],
                "alternative_actions": ["Use GitHub Actions", "Use GitLab CI", "Use Travis CI"],
            },
            
            # Packaging actions
            "package_api": {
                "action": "Package as hosted API service with documentation",
                "category": ActionCategory.PACKAGING,
                "priority": ActionPriority.MEDIUM,
                "rationale": "API packaging enables micro-SaaS monetization route",
                "estimated_effort_hours": 24.0,
                "success_criteria": ["API endpoints documented", "API deployed and accessible", "Usage examples provided"],
                "alternative_actions": ["Package as library", "Package as CLI tool"],
            },
            "create_demo": {
                "action": "Create interactive demo showcasing core functionality",
                "category": ActionCategory.PACKAGING,
                "priority": ActionPriority.MEDIUM,
                "rationale": "Demo is critical for buyer engagement and proof of execution",
                "estimated_effort_hours": 12.0,
                "success_criteria": ["Demo deployed and accessible", "Demo covers core features", "Demo has clear instructions"],
                "alternative_actions": ["Create video demo", "Create screenshot walkthrough"],
            },
            
            # Documentation actions
            "add_documentation": {
                "action": "Add comprehensive documentation (README, API docs, examples)",
                "category": ActionCategory.DOCUMENTATION,
                "priority": ActionPriority.HIGH,
                "rationale": "Documentation is required for commercial grade and buyer understanding",
                "estimated_effort_hours": 16.0,
                "success_criteria": ["README complete", "API documentation present", "Usage examples provided"],
                "alternative_actions": ["Focus on README only", "Add inline code comments"],
            },
            
            # Verification actions
            "verify_deployment": {
                "action": "Verify build and deployment proof with live URL",
                "category": ActionCategory.VERIFICATION,
                "priority": ActionPriority.HIGH,
                "rationale": "Deployment proof is required for execution proof and buyer confidence",
                "estimated_effort_hours": 4.0,
                "success_criteria": ["Deployment URL accessible", "Build log reproducible", "Deployment documented"],
                "alternative_actions": ["Deploy to staging environment", "Create deployment screenshots"],
            },
            
            # Outreach actions
            "outreach_buyers": {
                "action": "Send buyer memo to 20 qualified targets and record responses",
                "category": ActionCategory.OUTREACH,
                "priority": ActionPriority.MEDIUM,
                "rationale": "Buyer outreach is required to validate market and generate offers",
                "estimated_effort_hours": 8.0,
                "success_criteria": ["20 buyers contacted", "Response rate tracked", "Outcomes recorded"],
                "alternative_actions": ["Use broker for outreach", "List on marketplace"],
            },
            
            # Strategic actions
            "bundle_repos": {
                "action": "Bundle with related repos and package as single product",
                "category": ActionCategory.STRATEGIC,
                "priority": ActionPriority.MEDIUM,
                "rationale": "Bundling increases value and reduces buyer acquisition cost",
                "estimated_effort_hours": 16.0,
                "success_criteria": ["Related repos identified", "Bundle package created", "Bundle documentation complete"],
                "alternative_actions": ["Package as separate products", "Create tiered offering"],
            },
            "archive_asset": {
                "action": "Archive asset as non-financeable and focus on higher-priority projects",
                "category": ActionCategory.STRATEGIC,
                "priority": ActionPriority.LOW,
                "rationale": "Asset has limited monetization potential - opportunity cost too high",
                "estimated_effort_hours": 2.0,
                "success_criteria": ["Archival decision documented", "Asset marked as archived", "Resources reallocated"],
                "alternative_actions": ["Open-source asset", "Donate to community"],
            },
        }
    
    def recommend_next_action(
        self,
        asset_data: Dict[str, Any],
        grades: Dict[str, Any],
        committee_results: Dict[str, Any],
        liquidification_plan: Dict[str, Any],
    ) -> NextAction:
        """
        Recommend the single best next action for an asset.
        
        Args:
            asset_data: Asset metadata and classification
            grades: Professional grades
            committee_results: Committee evaluation results
            liquidification_plan: Liquidification plan
        
        Returns:
            NextAction with the single best recommendation
        """
        # Check for critical blockers first
        critical_action = self._check_critical_blockers(
            asset_data,
            committee_results,
        )
        if critical_action:
            return critical_action
        
        # Check for high-priority development needs
        development_action = self._check_development_needs(
            asset_data,
            grades,
            committee_results,
        )
        if development_action:
            return development_action
        
        # Check for packaging needs
        packaging_action = self._check_packaging_needs(
            asset_data,
            grades,
            liquidification_plan,
        )
        if packaging_action:
            return packaging_action
        
        # Check for outreach readiness
        outreach_action = self._check_outreach_readiness(
            asset_data,
            grades,
            liquidification_plan,
        )
        if outreach_action:
            return outreach_action
        
        # Default to strategic assessment
        return self._strategic_fallback(
            asset_data,
            grades,
            liquidification_plan,
        )
    
    def _check_critical_blockers(
        self,
        asset_data: Dict[str, Any],
        committee_results: Dict[str, Any],
    ) -> Optional[NextAction]:
        """Check for critical blockers that must be resolved first."""
        committee_report = committee_results.get("committee_report", {})
        blockers = committee_report.get("all_blockers", [])
        
        # Check for secrets
        secret_blockers = [b for b in blockers if "secret" in b.lower() or "private key" in b.lower()]
        if secret_blockers:
            template = self.action_templates["remove_secrets"]
            return NextAction(
                action=template["action"],
                priority=template["priority"],
                category=template["category"],
                rationale=template["rationale"],
                estimated_effort_hours=template["estimated_effort_hours"],
                dependencies=[],
                success_criteria=template["success_criteria"],
                alternative_actions=template["alternative_actions"],
            )
        
        # Check for ownership issues
        ownership_blockers = [b for b in blockers if "ownership" in b.lower()]
        if ownership_blockers:
            template = self.action_templates["resolve_ownership"]
            return NextAction(
                action=template["action"],
                priority=template["priority"],
                category=template["category"],
                rationale=template["rationale"],
                estimated_effort_hours=template["estimated_effort_hours"],
                dependencies=[],
                success_criteria=template["success_criteria"],
                alternative_actions=template["alternative_actions"],
            )
        
        # Check for build failures
        build_status = asset_data.get("build_status", "unknown")
        if build_status == "failed":
            template = self.action_templates["fix_build"]
            return NextAction(
                action=template["action"],
                priority=template["priority"],
                category=template["category"],
                rationale=template["rationale"],
                estimated_effort_hours=template["estimated_effort_hours"],
                dependencies=[],
                success_criteria=template["success_criteria"],
                alternative_actions=template["alternative_actions"],
            )
        
        return None
    
    def _check_development_needs(
        self,
        asset_data: Dict[str, Any],
        grades: Dict[str, Any],
        committee_results: Dict[str, Any],
    ) -> Optional[NextAction]:
        """Check for high-priority development needs."""
        # Check for missing tests
        has_tests = asset_data.get("has_tests", False)
        production_grade = grades.get("production_grade", "F")
        
        if not has_tests and production_grade in ["C", "D"]:
            template = self.action_templates["add_tests"]
            return NextAction(
                action=template["action"],
                priority=template["priority"],
                category=template["category"],
                rationale=template["rationale"],
                estimated_effort_hours=template["estimated_effort_hours"],
                dependencies=[],
                success_criteria=template["success_criteria"],
                alternative_actions=template["alternative_actions"],
            )
        
        # Check for missing CI/CD
        has_ci_cd = asset_data.get("has_ci_cd", False)
        if not has_ci_cd and production_grade in ["C", "B"]:
            template = self.action_templates["add_ci_cd"]
            return NextAction(
                action=template["action"],
                priority=template["priority"],
                category=template["category"],
                rationale=template["rationale"],
                estimated_effort_hours=template["estimated_effort_hours"],
                dependencies=[],
                success_criteria=template["success_criteria"],
                alternative_actions=template["alternative_actions"],
            )
        
        # Check for missing documentation
        has_documentation = asset_data.get("has_documentation", False)
        commercial_grade = grades.get("commercial_grade", "F")
        
        if not has_documentation and commercial_grade in ["C", "D"]:
            template = self.action_templates["add_documentation"]
            return NextAction(
                action=template["action"],
                priority=template["priority"],
                category=template["category"],
                rationale=template["rationale"],
                estimated_effort_hours=template["estimated_effort_hours"],
                dependencies=[],
                success_criteria=template["success_criteria"],
                alternative_actions=template["alternative_actions"],
            )
        
        return None
    
    def _check_packaging_needs(
        self,
        asset_data: Dict[str, Any],
        grades: Dict[str, Any],
        liquidification_plan: Dict[str, Any],
    ) -> Optional[NextAction]:
        """Check for packaging needs."""
        financeability = grades.get("financeability_score", 0)
        primary_route = liquidification_plan.get("primary_route", "unknown")
        
        # If financeability is good but not packaged
        if financeability >= 60:
            has_demo = asset_data.get("has_demo", False)
            has_api_potential = asset_data.get("has_api_potential", False)
            
            if not has_demo:
                template = self.action_templates["create_demo"]
                return NextAction(
                    action=template["action"],
                    priority=template["priority"],
                    category=template["category"],
                    rationale=template["rationale"],
                    estimated_effort_hours=template["estimated_effort_hours"],
                    dependencies=[],
                    success_criteria=template["success_criteria"],
                    alternative_actions=template["alternative_actions"],
                )
            
            if has_api_potential and primary_route in ["hosted_api", "micro_saas"]:
                template = self.action_templates["package_api"]
                return NextAction(
                    action=template["action"],
                    priority=template["priority"],
                    category=template["category"],
                    rationale=template["rationale"],
                    estimated_effort_hours=template["estimated_effort_hours"],
                    dependencies=["create_demo"],
                    success_criteria=template["success_criteria"],
                    alternative_actions=template["alternative_actions"],
                )
        
        return None
    
    def _check_outreach_readiness(
        self,
        asset_data: Dict[str, Any],
        grades: Dict[str, Any],
        liquidification_plan: Dict[str, Any],
    ) -> Optional[NextAction]:
        """Check if asset is ready for buyer outreach."""
        financeability = grades.get("financeability_score", 0)
        required_cleanup = liquidification_plan.get("required_cleanup", [])
        
        # If financeability is high and cleanup is done
        if financeability >= 70 and (not required_cleanup or "No critical cleanup required" in required_cleanup):
            template = self.action_templates["outreach_buyers"]
            return NextAction(
                action=template["action"],
                priority=template["priority"],
                category=template["category"],
                rationale=template["rationale"],
                estimated_effort_hours=template["estimated_effort_hours"],
                dependencies=[],
                success_criteria=template["success_criteria"],
                alternative_actions=template["alternative_actions"],
            )
        
        return None
    
    def _strategic_fallback(
        self,
        asset_data: Dict[str, Any],
        grades: Dict[str, Any],
        liquidification_plan: Dict[str, Any],
    ) -> NextAction:
        """Strategic fallback when no specific action is identified."""
        financeability = grades.get("financeability_score", 0)
        classification = asset_data.get("classification", "unknown")
        
        # If financeability is very low, consider archiving
        if financeability < 30 and classification in ["scaffold", "duplicate", "junk"]:
            template = self.action_templates["archive_asset"]
            return NextAction(
                action=template["action"],
                priority=template["priority"],
                category=template["category"],
                rationale=template["rationale"],
                estimated_effort_hours=template["estimated_effort_hours"],
                dependencies=[],
                success_criteria=template["success_criteria"],
                alternative_actions=template["alternative_actions"],
            )
        
        # If asset has related assets, consider bundling
        related_assets = asset_data.get("related_assets", [])
        if related_assets and financeability >= 40:
            template = self.action_templates["bundle_repos"]
            return NextAction(
                action=template["action"],
                priority=template["priority"],
                category=template["category"],
                rationale=template["rationale"],
                estimated_effort_hours=template["estimated_effort_hours"],
                dependencies=[],
                success_criteria=template["success_criteria"],
                alternative_actions=template["alternative_actions"],
            )
        
        # Default: verify deployment
        template = self.action_templates["verify_deployment"]
        return NextAction(
            action=template["action"],
            priority=template["priority"],
            category=template["category"],
            rationale=template["rationale"],
            estimated_effort_hours=template["estimated_effort_hours"],
            dependencies=[],
            success_criteria=template["success_criteria"],
            alternative_actions=template["alternative_actions"],
        )
    
    def recommend_portfolio_actions(
        self,
        asset_evaluations: List[Dict[str, Any]],
    ) -> Dict[str, Any]:
        """
        Recommend actions for the entire portfolio.
        
        Args:
            asset_evaluations: List of evaluated assets
        
        Returns:
            Portfolio-level action recommendations
        """
        # Count actions by priority
        critical_count = 0
        high_count = 0
        medium_count = 0
        low_count = 0
        
        # Collect all next actions
        all_actions = []
        
        for evaluation in asset_evaluations:
            next_action = self.recommend_next_action(
                asset_data=evaluation.get("asset_data", {}),
                grades=evaluation.get("grades", {}),
                committee_results=evaluation.get("committee_results", {}),
                liquidification_plan=evaluation.get("liquidification_plan", {}),
            )
            
            all_actions.append({
                "asset_name": evaluation.get("asset_data", {}).get("asset_name", "Unknown"),
                "action": next_action.action,
                "priority": next_action.priority.value,
                "category": next_action.category.value,
            })
            
            if next_action.priority == ActionPriority.CRITICAL:
                critical_count += 1
            elif next_action.priority == ActionPriority.HIGH:
                high_count += 1
            elif next_action.priority == ActionPriority.MEDIUM:
                medium_count += 1
            else:
                low_count += 1
        
        # Determine portfolio-level best next action
        if critical_count > 0:
            portfolio_action = f"Resolve {critical_count} critical blockers (secrets, ownership, build failures)"
        elif high_count > 0:
            portfolio_action = f"Complete {high_count} high-priority development tasks (tests, CI/CD, documentation)"
        elif medium_count > 0:
            portfolio_action = f"Package {medium_count} assets for monetization (demo, API, documentation)"
        else:
            portfolio_action = "Begin buyer outreach for financeable assets"
        
        return {
            "portfolio_best_next_action": portfolio_action,
            "action_summary": {
                "critical": critical_count,
                "high": high_count,
                "medium": medium_count,
                "low": low_count,
            },
            "all_actions": all_actions,
        }
