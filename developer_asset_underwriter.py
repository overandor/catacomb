#!/usr/bin/env python3
"""
Developer Asset Underwriter - Main Orchestrator

This is the main orchestrator that integrates all components of the Job-Description
Intelligence Engine into a cohesive system.

The product's strongest claim becomes:
"CollateralOps manufactures the missing professional layer between software builders and capital."

It understands software from the developer side, evaluates risk like an auditor, routes
assets like a broker, and translates proof into collateral language.

That is the professional feel.
"""

from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field
from datetime import datetime
import json

# Import all components
from job_description_intelligence import (
    JobDescriptionCorpus,
    CompetencyGraph,
    create_seed_competency_graph,
    RoleFamily,
)
from synthetic_committee import SyntheticCommittee
from professional_scoring import (
    ProfessionalScoringSystem,
    StrategicValueClassifier,
    BlockerAnalyzer,
)
from capital_translation import CapitalTranslator
from liquidification_layer import LiquidificationEngine
from professional_review_card import (
    ProfessionalReviewCardGenerator,
    ReviewCardFormatter,
)
from asset_desk_ui import AssetDeskUI
from next_action_engine import NextActionEngine
from job_description_miner import JobDescriptionMiner, JobCorpusManager
from evidence_based_scoring import EvidenceBasedScoring
from audit_log import AuditLogger


@dataclass
class AssetEvaluation:
    """
    Complete evaluation result for a single asset.
    
    This is the comprehensive output of the Developer Asset Underwriter system.
    """
    asset_id: str
    asset_name: str
    
    # Raw data
    asset_data: Dict[str, Any]
    
    # Committee evaluation
    committee_results: Dict[str, Any]
    
    # Professional grades
    grades: Dict[str, Any]
    
    # Strategic classification
    strategic_classification: Dict[str, Any]
    
    # Capital translation
    capital_translation: Dict[str, Any]
    
    # Liquidification plan
    liquidification_plan: Dict[str, Any]
    
    # Review card
    review_card: Dict[str, Any]
    
    # Next action
    next_action: Dict[str, Any]
    
    # Metadata
    evaluated_at: datetime = field(default_factory=datetime.now)
    evaluator_version: str = "developer_asset_underwriter_v1"
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "asset_id": self.asset_id,
            "asset_name": self.asset_name,
            "asset_data": self.asset_data,
            "committee_results": self.committee_results,
            "grades": self.grades,
            "strategic_classification": self.strategic_classification,
            "capital_translation": self.capital_translation,
            "liquidification_plan": self.liquidification_plan,
            "review_card": self.review_card,
            "next_action": self.next_action,
            "evaluated_at": self.evaluated_at.isoformat(),
            "evaluator_version": self.evaluator_version,
        }


class DeveloperAssetUnderwriter:
    """
    Developer Asset Underwriter - Main orchestrator.
    
    This system manufactures the missing professional layer between software builders
    and capital. It understands software from the developer side, evaluates risk like
    an auditor, routes assets like a broker, and translates proof into collateral language.
    """
    
    def __init__(
        self,
        use_seed_competencies: bool = True,
        competency_graph_path: Optional[str] = None,
    ):
        """
        Initialize the Developer Asset Underwriter.
        
        Args:
            use_seed_competencies: Whether to use seed competencies or load from file
            competency_graph_path: Path to load competency graph from file
        """
        # Initialize competency graph
        if competency_graph_path:
            # Load from file (implementation would go here)
            self.competency_graph = None  # Placeholder
        elif use_seed_competencies:
            self.competency_graph = create_seed_competency_graph()
        else:
            self.competency_graph = None
        
        # Initialize job corpus
        self.job_corpus = JobDescriptionCorpus()
        
        # Initialize components
        self.synthetic_committee = SyntheticCommittee()
        self.scoring_system = ProfessionalScoringSystem()
        self.strategic_classifier = StrategicValueClassifier()
        self.blocker_analyzer = BlockerAnalyzer()
        self.capital_translator = CapitalTranslator()
        self.liquidification_engine = LiquidificationEngine()
        self.review_card_generator = ProfessionalReviewCardGenerator()
        self.asset_desk_ui = AssetDeskUI()
        self.next_action_engine = NextActionEngine()
        self.evidence_based_scoring = EvidenceBasedScoring()
        self.audit_logger = AuditLogger()
        
        # Initialize job mining (optional)
        self.job_miner = JobDescriptionMiner()
        self.corpus_manager = JobCorpusManager()
        
        self.version = "developer_asset_underwriter_v1"
    
    def evaluate_asset(
        self,
        asset_data: Dict[str, Any],
        developer_description: Optional[str] = None,
    ) -> AssetEvaluation:
        """
        Evaluate a single software asset.
        
        This is the main entry point for asset evaluation. It runs the complete
        pipeline from discovery to professional review card.
        
        Args:
            asset_data: Asset metadata and technical data
            developer_description: Optional developer-provided description
        
        Returns:
            AssetEvaluation with complete professional assessment
        """
        asset_id = asset_data.get("asset_id", "unknown")
        asset_name = asset_data.get("asset_name", "Unknown Asset")
        
        # Step 1: Run synthetic committee evaluation
        committee_results = self.synthetic_committee.evaluate(asset_data)
        
        # Step 2: Calculate professional grades
        grades = self.scoring_system.score_asset(committee_results, asset_data)
        grades_dict = grades.to_dict()
        
        # Step 3: Classify strategic value
        strategic_classification = self.strategic_classifier.classify(grades, committee_results)
        
        # Step 4: Translate to capital language
        if developer_description:
            capital_translation = self.capital_translator.translate(
                developer_description,
                asset_data,
                grades_dict,
                committee_results,
            )
            capital_translation_dict = capital_translation.to_dict()
        else:
            # Generate default translation from asset data
            capital_translation = self.capital_translator.translate(
                asset_data.get("description", "Software asset"),
                asset_data,
                grades_dict,
                committee_results,
            )
            capital_translation_dict = capital_translation.to_dict()
        
        # Step 5: Generate liquidification plan
        liquidification_plan = self.liquidification_engine.generate_liquidification_plan(
            asset_data,
            grades_dict,
            committee_results,
        )
        liquidification_plan_dict = liquidification_plan.to_dict()
        
        # Step 6: Generate professional review card
        review_card = self.review_card_generator.generate_card(
            asset_data,
            grades_dict,
            committee_results,
            strategic_classification,
            liquidification_plan_dict,
            capital_translation_dict,
        )
        review_card_dict = review_card.to_dict()
        
        # Step 7: Generate next action
        next_action = self.next_action_engine.recommend_next_action(
            asset_data,
            grades_dict,
            committee_results,
            liquidification_plan_dict,
        )
        next_action_dict = next_action.to_dict()
        
        return AssetEvaluation(
            asset_id=asset_id,
            asset_name=asset_name,
            asset_data=asset_data,
            committee_results=committee_results,
            grades=grades_dict,
            strategic_classification=strategic_classification,
            capital_translation=capital_translation_dict,
            liquidification_plan=liquidification_plan_dict,
            review_card=review_card_dict,
            next_action=next_action_dict,
        )
    
    def evaluate_portfolio(
        self,
        asset_data_list: List[Dict[str, Any]],
    ) -> Dict[str, Any]:
        """
        Evaluate a portfolio of software assets.
        
        Args:
            asset_data_list: List of asset data dictionaries
        
        Returns:
            Portfolio evaluation with dashboard and individual asset results
        """
        # Evaluate each asset
        evaluations = []
        for asset_data in asset_data_list:
            evaluation = self.evaluate_asset(asset_data)
            evaluations.append(evaluation.to_dict())
        
        # Generate asset desk dashboard
        dashboard = self.asset_desk_ui.generate_dashboard(evaluations)
        dashboard_dict = dashboard.to_dict()
        
        # Generate portfolio-level next actions
        portfolio_actions = self.next_action_engine.recommend_portfolio_actions(evaluations)
        
        return {
            "portfolio_summary": dashboard_dict["portfolio_summary"],
            "best_next_action": dashboard_dict["best_next_action"],
            "priority_assets": dashboard_dict["priority_assets"],
            "portfolio_actions": portfolio_actions,
            "individual_evaluations": evaluations,
            "total_assets": len(evaluations),
            "evaluated_at": datetime.now().isoformat(),
            "evaluator_version": self.version,
        }
    
    def build_competency_graph_from_corpus(self) -> CompetencyGraph:
        """
        Build competency graph from job description corpus.
        
        This is the core move: mining job descriptions into professional judgment.
        """
        # Extract competencies from corpus
        competency_graph = self.job_corpus.extract_competencies()
        
        self.competency_graph = competency_graph
        return competency_graph
    
    def mine_job_descriptions(
        self,
        role_families: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        """
        Mine job descriptions to build the competency graph.
        
        Args:
            role_families: Specific role families to mine (optional)
        
        Returns:
            Mining results and statistics
        """
        # Mine job descriptions
        jobs = self.job_miner.mine_job_descriptions(role_families)
        
        # Add to corpus
        added_count = self.corpus_manager.add_jobs(jobs)
        
        # Get mining stats
        mining_stats = self.job_miner.get_mining_stats()
        
        # Get corpus stats
        corpus_stats = self.corpus_manager.get_corpus_stats()
        
        return {
            "jobs_mined": len(jobs),
            "jobs_added_to_corpus": added_count,
            "mining_stats": mining_stats,
            "corpus_stats": corpus_stats,
            "mining_report": self.job_miner.export_mining_report(),
        }
    
    def generate_asset_desk_view(
        self,
        view_name: str,
        asset_evaluations: List[Dict[str, Any]],
    ) -> Dict[str, Any]:
        """
        Generate a specific asset desk view.
        
        Args:
            view_name: Name of the view to generate
            asset_evaluations: List of asset evaluations
        
        Returns:
            View-specific data
        """
        from asset_desk_ui import AssetDeskView
        
        try:
            view = AssetDeskView(view_name)
            return self.asset_desk_ui.generate_view(view, asset_evaluations)
        except ValueError:
            return {"error": f"Unknown view: {view_name}"}
    
    def export_evaluation_report(
        self,
        evaluation: AssetEvaluation,
        format: str = "markdown",
    ) -> str:
        """
        Export an evaluation report in the specified format.
        
        Args:
            evaluation: Asset evaluation to export
            format: Export format (markdown, text, json)
        
        Returns:
            Formatted report
        """
        from professional_review_card import ProfessionalReviewCard, ProofLevel
        
        # Convert proof_level int to enum
        proof_level_int = evaluation.grades.get("proof_level", 0)
        proof_level = ProofLevel(proof_level_int)
        
        if format == "markdown":
            card = ProfessionalReviewCard(
                asset_id=evaluation.asset_id,
                asset_name=evaluation.asset_name,
                classification=evaluation.asset_data.get("classification", "unknown"),
                production_grade=evaluation.grades.get("production_grade", "C"),
                commercial_grade=evaluation.grades.get("commercial_grade", "C"),
                collateral_grade=evaluation.grades.get("collateral_grade", "C"),
                financeability_score=evaluation.grades.get("financeability_score", 0),
                proof_level=proof_level,
                strategic_value=evaluation.strategic_classification.get("strategic_value", "unknown"),
                buyer_today_value=evaluation.strategic_classification.get("buyer_today_value", "unknown"),
                collateral_support=evaluation.strategic_classification.get("collateral_support", "unknown"),
                main_blockers=evaluation.committee_results.get("committee_report", {}).get("all_blockers", [])[:5],
                best_next_action=evaluation.next_action.get("action", "Review asset"),
                likely_route=evaluation.liquidification_plan.get("buyer_universe", [])[:5],
                packet_readiness="Generated by Developer Asset Underwriter",
            )
            return card.to_markdown()
        
        elif format == "text":
            card = ProfessionalReviewCard(
                asset_id=evaluation.asset_id,
                asset_name=evaluation.asset_name,
                classification=evaluation.asset_data.get("classification", "unknown"),
                production_grade=evaluation.grades.get("production_grade", "C"),
                commercial_grade=evaluation.grades.get("commercial_grade", "C"),
                collateral_grade=evaluation.grades.get("collateral_grade", "C"),
                financeability_score=evaluation.grades.get("financeability_score", 0),
                proof_level=proof_level,
                strategic_value=evaluation.strategic_classification.get("strategic_value", "unknown"),
                buyer_today_value=evaluation.strategic_classification.get("buyer_today_value", "unknown"),
                collateral_support=evaluation.strategic_classification.get("collateral_support", "unknown"),
                main_blockers=evaluation.committee_results.get("committee_report", {}).get("all_blockers", [])[:5],
                best_next_action=evaluation.next_action.get("action", "Review asset"),
                likely_route=evaluation.liquidification_plan.get("buyer_universe", [])[:5],
                packet_readiness="Generated by Developer Asset Underwriter",
            )
            return card.to_text()
        
        elif format == "json":
            return json.dumps(evaluation.to_dict(), indent=2)
        
        else:
            raise ValueError(f"Unknown format: {format}")
    
    def get_system_info(self) -> Dict[str, Any]:
        """Get system information and status."""
        return {
            "version": self.version,
            "competency_graph_loaded": self.competency_graph is not None,
            "competency_graph_id": self.competency_graph.graph_id if self.competency_graph else None,
            "job_corpus_size": len(self.job_corpus.job_descriptions),
            "components": {
                "synthetic_committee": "operational",
                "scoring_system": "operational",
                "capital_translator": "operational",
                "liquidification_engine": "operational",
                "review_card_generator": "operational",
                "asset_desk_ui": "operational",
                "next_action_engine": "operational",
                "job_miner": "operational",
                "corpus_manager": "operational",
            },
        }


# Example usage and testing
if __name__ == "__main__":
    # Initialize the system
    underwriter = DeveloperAssetUnderwriter()
    
    # Example asset data
    example_asset = {
        "asset_id": "example_repo_1",
        "asset_name": "Repo Appraiser Pro",
        "classification": "real_production_system",
        "description": "A local Python app that scans repos and estimates value",
        "primary_language": "python",
        "file_count": 45,
        "has_tests": True,
        "has_ci_cd": True,
        "has_documentation": True,
        "code_quality_score": 75,
        "architecture_complexity": "moderate",
        "build_status": "passed",
        "test_status": "passed",
        "deployment_status": "deployable",
        "has_endpoints": True,
        "has_demo": False,
        "has_license": True,
        "license_type": "MIT",
        "is_fork": False,
        "copied_code_ratio": 0.05,
        "template_dependence": False,
        "ownership_clarity": "clear",
        "has_ownership_clarity": True,
        "has_liquidation_route": False,
        "has_monitoring_plan": False,
        "has_api_potential": True,
        "has_data_value": False,
        "has_strategic_value": True,
        "category": "developer_tools",
        "buyer_categories": ["developer_tooling_buyers", "ip_consultants"],
        "market_size": "medium",
        "competitive_landscape": [],
        "unique_value_proposition": "Automated repo appraisal with professional grading",
        "adoption_signals": {
            "stars": 150,
            "forks": 30,
            "downloads": 5000,
        },
        "revenue_evidence": [],
        "documentation_score": 70,
        "secrets_detected": [],
        "private_keys_detected": [],
        "vulnerable_dependencies": [],
        "unsafe_patterns": [],
        "pii_detected": [],
        "runtime_errors": [],
        "related_assets": [],
        "is_agent_generated": False,
        "signal_to_noise_ratio": 1.0,
        "duplicate_ratio": 0.0,
        "scaffold_ratio": 0.1,
        "original_contribution_ratio": 0.9,
    }
    
    # Evaluate the asset
    evaluation = underwriter.evaluate_asset(
        example_asset,
        developer_description="This is a local Python app that scans repos and estimates value",
    )
    
    # Print the review card
    print("=" * 60)
    print("PROFESSIONAL REVIEW CARD")
    print("=" * 60)
    print(underwriter.export_evaluation_report(evaluation, format="text"))
    print("=" * 60)
    
    # Print system info
    print("\nSYSTEM INFO:")
    print(json.dumps(underwriter.get_system_info(), indent=2))
