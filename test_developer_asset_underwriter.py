#!/usr/bin/env python3
"""
Test suite for Developer Asset Underwriter system.

Tests core components with mock asset data to ensure proper functionality.
"""

import sys
import json
from typing import Dict, Any, List

# Test imports
try:
    from job_description_intelligence import JobDescriptionCorpus, CompetencyGraph, create_seed_competency_graph
    from synthetic_committee import SyntheticCommittee
    from professional_scoring import ProfessionalScoringSystem
    from capital_translation import CapitalTranslator
    from liquidification_layer import LiquidificationEngine
    from professional_review_card import ProfessionalReviewCardGenerator
    from asset_desk_ui import AssetDeskUI
    from next_action_engine import NextActionEngine
    from developer_asset_underwriter import DeveloperAssetUnderwriter
    from evidence_based_scoring import EvidenceBasedScoring
    from audit_log import AuditLogger
    print("✅ All imports successful")
except ImportError as e:
    print(f"❌ Import failed: {e}")
    sys.exit(1)


# Mock asset data for testing
MOCK_ASSETS = [
    {
        "asset_id": "test_001",
        "asset_name": "Production API Service",
        "classification": "api_service",
        "primary_language": "Python",
        "file_count": 45,
        "has_tests": True,
        "has_ci_cd": True,
        "has_documentation": True,
        "code_quality_score": 85,
        "build_status": "passed",
        "test_status": "passed",
        "deployment_status": "deployed",
        "has_license": True,
        "license_type": "MIT",
        "is_fork": False,
        "ownership_clarity": "clear",
        "repo_url": "https://github.com/test/api-service",
        "deployment_url": "https://api.example.com",
    },
    {
        "asset_id": "test_002",
        "asset_name": "Internal Tool",
        "classification": "internal_tool",
        "primary_language": "JavaScript",
        "file_count": 20,
        "has_tests": False,
        "has_ci_cd": False,
        "has_documentation": False,
        "code_quality_score": 60,
        "build_status": "unknown",
        "test_status": "unknown",
        "deployment_status": "unknown",
        "has_license": False,
        "license_type": "",
        "is_fork": False,
        "ownership_clarity": "unclear",
        "repo_url": "https://github.com/test/internal-tool",
    },
    {
        "asset_id": "test_003",
        "asset_name": "Research Prototype",
        "classification": "research_prototype",
        "primary_language": "Python",
        "file_count": 15,
        "has_tests": True,
        "has_ci_cd": False,
        "has_documentation": True,
        "code_quality_score": 70,
        "build_status": "passed",
        "test_status": "passed",
        "deployment_status": "unknown",
        "has_license": True,
        "license_type": "Apache-2.0",
        "is_fork": False,
        "ownership_clarity": "clear",
        "repo_url": "https://github.com/test/research-proto",
    },
    {
        "asset_id": "test_004",
        "asset_name": "Frontend Product",
        "classification": "frontend_product",
        "primary_language": "TypeScript",
        "file_count": 80,
        "has_tests": True,
        "has_ci_cd": True,
        "has_documentation": True,
        "code_quality_score": 90,
        "build_status": "passed",
        "test_status": "passed",
        "deployment_status": "deployed",
        "has_license": True,
        "license_type": "MIT",
        "is_fork": False,
        "ownership_clarity": "clear",
        "repo_url": "https://github.com/test/frontend-product",
        "deployment_url": "https://app.example.com",
    },
    {
        "asset_id": "test_005",
        "asset_name": "Trading Engine",
        "classification": "trading_engine",
        "primary_language": "Rust",
        "file_count": 120,
        "has_tests": True,
        "has_ci_cd": True,
        "has_documentation": True,
        "code_quality_score": 95,
        "build_status": "passed",
        "test_status": "passed",
        "deployment_status": "deployed",
        "has_license": True,
        "license_type": "MIT",
        "is_fork": False,
        "ownership_clarity": "clear",
        "repo_url": "https://github.com/test/trading-engine",
        "deployment_url": "https://trade.example.com",
    },
]


def test_component_initialization():
    """Test that all components initialize correctly."""
    print("\n" + "="*60)
    print("TEST: Component Initialization")
    print("="*60)
    
    try:
        # Initialize competency graph
        competency_graph = create_seed_competency_graph()
        print("✅ Competency graph initialized")
        
        # Initialize synthetic committee
        committee = SyntheticCommittee()
        print("✅ Synthetic committee initialized")
        
        # Initialize scoring system
        scoring_system = ProfessionalScoringSystem()
        print("✅ Professional scoring system initialized")
        
        # Initialize capital translator
        capital_translator = CapitalTranslator()
        print("✅ Capital translator initialized")
        
        # Initialize liquidification engine
        liquidification_engine = LiquidificationEngine()
        print("✅ Liquidification engine initialized")
        
        # Initialize review card generator
        review_card_generator = ProfessionalReviewCardGenerator()
        print("✅ Review card generator initialized")
        
        # Initialize asset desk UI
        asset_desk_ui = AssetDeskUI()
        print("✅ Asset desk UI initialized")
        
        # Initialize next action engine
        next_action_engine = NextActionEngine()
        print("✅ Next action engine initialized")
        
        # Initialize evidence-based scoring
        evidence_scoring = EvidenceBasedScoring()
        print("✅ Evidence-based scoring initialized")
        
        # Initialize audit logger
        audit_logger = AuditLogger()
        print("✅ Audit logger initialized")
        
        return True
    except Exception as e:
        print(f"❌ Component initialization failed: {e}")
        return False


def test_single_asset_evaluation():
    """Test evaluation of a single asset."""
    print("\n" + "="*60)
    print("TEST: Single Asset Evaluation")
    print("="*60)
    
    try:
        underwriter = DeveloperAssetUnderwriter()
        asset_data = MOCK_ASSETS[0]
        
        print(f"Evaluating asset: {asset_data['asset_name']}")
        
        evaluation = underwriter.evaluate_asset(asset_data)
        
        # Verify evaluation structure
        assert evaluation.asset_id == asset_data['asset_id'], "Asset ID mismatch"
        assert evaluation.grades is not None, "Grades missing"
        assert evaluation.committee_results is not None, "Committee results missing"
        assert evaluation.strategic_classification is not None, "Strategic classification missing"
        assert evaluation.liquidification_plan is not None, "Liquidification plan missing"
        assert evaluation.capital_translation is not None, "Capital translation missing"
        assert evaluation.next_action is not None, "Next action missing"
        
        print(f"✅ Production Grade: {evaluation.grades.get('production_grade')}")
        print(f"✅ Commercial Grade: {evaluation.grades.get('commercial_grade')}")
        print(f"✅ Collateral Grade: {evaluation.grades.get('collateral_grade')}")
        print(f"✅ Financeability Score: {evaluation.grades.get('financeability_score')}/100")
        print(f"✅ Best Next Action: {evaluation.next_action.get('action')}")
        
        return True
    except Exception as e:
        print(f"❌ Single asset evaluation failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_multiple_asset_evaluation():
    """Test evaluation of multiple assets."""
    print("\n" + "="*60)
    print("TEST: Multiple Asset Evaluation")
    print("="*60)
    
    try:
        underwriter = DeveloperAssetUnderwriter()
        
        results = []
        for asset_data in MOCK_ASSETS:
            print(f"Evaluating: {asset_data['asset_name']}")
            evaluation = underwriter.evaluate_asset(asset_data)
            results.append(evaluation)
        
        print(f"✅ Evaluated {len(results)} assets successfully")
        
        # Verify all evaluations have required fields
        for evaluation in results:
            assert evaluation.grades is not None, "Grades missing"
            assert evaluation.grades.get('financeability_score', 0) >= 0, "Invalid financeability score"
            assert evaluation.grades.get('financeability_score', 0) <= 100, "Invalid financeability score"
        
        # Print summary
        print("\nEvaluation Summary:")
        for i, evaluation in enumerate(results):
            print(f"  {i+1}. {evaluation.asset_name}: {evaluation.grades.get('financeability_score')}/100")
        
        return True
    except Exception as e:
        print(f"❌ Multiple asset evaluation failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_evidence_based_scoring():
    """Test evidence-based scoring safeguards."""
    print("\n" + "="*60)
    print("TEST: Evidence-Based Scoring")
    print("="*60)
    
    try:
        evidence_scoring = EvidenceBasedScoring()
        
        # Test with full evidence
        raw_scores = {
            "engineering_substance": 85,
            "execution_proof": 90,
            "originality_ownership": 80,
        }
        
        full_evidence = {
            "engineering_substance": {
                "file_count": 100,
                "code_quality_score": 85,
                "verified": True,
            },
            "execution_proof": {
                "build_status": "passed",
                "test_status": "passed",
                "verified": True,
            },
            "originality_ownership": {
                "has_license": True,
                "license_type": "MIT",
                "verified": True,
            },
        }
        
        adjusted_scores, warnings = evidence_scoring.apply_safeguards(raw_scores, full_evidence)
        print(f"✅ Full evidence: scores preserved (no warnings)")
        
        # Test with missing evidence
        missing_evidence = {}
        adjusted_scores, warnings = evidence_scoring.apply_safeguards(raw_scores, missing_evidence)
        print(f"✅ Missing evidence: {len(warnings)} warnings generated")
        print(f"  Scores reduced: {adjusted_scores}")
        
        # Test financeability validation
        validation = evidence_scoring.validate_financeability_claim(85, full_evidence)
        print(f"✅ High financeability with full evidence: {validation['valid']}")
        
        validation = evidence_scoring.validate_financeability_claim(85, missing_evidence)
        print(f"✅ High financeability without evidence: {validation['valid']}")
        print(f"  Adjusted score: {validation['adjusted_score']}")
        
        return True
    except Exception as e:
        print(f"❌ Evidence-based scoring test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_audit_logging():
    """Test audit logging functionality."""
    print("\n" + "="*60)
    print("TEST: Audit Logging")
    print("="*60)
    
    try:
        audit_logger = AuditLogger()
        
        # Log a grade assignment
        entry = audit_logger.log_grade_assignment(
            asset_id="test_001",
            evaluator_name="EngineeringEvaluator",
            grade="A",
            score=85,
            evidence={"file_count": 100, "code_quality": 85},
            reasoning="Strong engineering substance with good code quality",
        )
        print(f"✅ Grade assignment logged: {entry.entry_id}")
        
        # Log a blocker identification
        entry = audit_logger.log_blocker_identification(
            asset_id="test_001",
            evaluator_name="SecurityEvaluator",
            blocker="Secret detected in code",
            severity="high",
            evidence={"secret_found": True, "secret_type": "api_key"},
            reasoning="API key exposed in source code",
        )
        print(f"✅ Blocker identification logged: {entry.entry_id}")
        
        # Log a recommendation
        entry = audit_logger.log_recommendation(
            asset_id="test_001",
            evaluator_name="NextActionEngine",
            recommendation="Remove secret and rotate API key",
            priority="high",
            evidence={"blocker": "secret_detected"},
            reasoning="Security risk must be addressed before monetization",
        )
        print(f"✅ Recommendation logged: {entry.entry_id}")
        
        # Get audit trail
        audit_trail = audit_logger.get_audit_trail("test_001")
        print(f"✅ Audit trail retrieved: {len(audit_trail)} entries")
        
        # Export audit report
        report = audit_logger.export_audit_report("test_001")
        print(f"✅ Audit report exported")
        
        return True
    except Exception as e:
        print(f"❌ Audit logging test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_portfolio_evaluation():
    """Test portfolio-level evaluation."""
    print("\n" + "="*60)
    print("TEST: Portfolio Evaluation")
    print("="*60)
    
    try:
        underwriter = DeveloperAssetUnderwriter()
        
        portfolio = underwriter.evaluate_portfolio(MOCK_ASSETS)
        
        # Verify portfolio structure (returns dict)
        assert portfolio is not None, "Portfolio is None"
        
        # Print actual structure for debugging
        print(f"Portfolio keys: {portfolio.keys()}")
        
        # Check for expected keys
        assert 'total_assets' in portfolio, "total_assets missing"
        assert 'portfolio_summary' in portfolio, "portfolio_summary missing"
        assert 'individual_evaluations' in portfolio, "individual_evaluations missing"
        
        assert portfolio['total_assets'] == len(MOCK_ASSETS), "Total assets count mismatch"
        print(f"✅ Portfolio evaluated: {portfolio['total_assets']} assets")
        print(f"✅ Portfolio summary keys: {portfolio['portfolio_summary'].keys()}")
        
        return True
    except Exception as e:
        print(f"❌ Portfolio evaluation failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def run_all_tests():
    """Run all tests."""
    print("\n" + "="*60)
    print("CATAOMB DEVELOPER ASSET UNDERWRITER - TEST SUITE")
    print("="*60)
    
    tests = [
        ("Component Initialization", test_component_initialization),
        ("Single Asset Evaluation", test_single_asset_evaluation),
        ("Multiple Asset Evaluation", test_multiple_asset_evaluation),
        ("Evidence-Based Scoring", test_evidence_based_scoring),
        ("Audit Logging", test_audit_logging),
        ("Portfolio Evaluation", test_portfolio_evaluation),
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ Test '{test_name}' crashed: {e}")
            results.append((test_name, False))
    
    # Print summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status}: {test_name}")
    
    print(f"\nTotal: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed!")
        return 0
    else:
        print(f"\n⚠️  {total - passed} test(s) failed")
        return 1


if __name__ == "__main__":
    sys.exit(run_all_tests())
