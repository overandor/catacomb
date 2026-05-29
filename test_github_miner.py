#!/usr/bin/env python3
"""
Test script for GitHub Intervention Miner with mock data.
"""

import sys
sys.path.insert(0, '/Users/alep/Downloads/02_AI_Agents/catacomb')

from github_intervention_miner import InterventionClassifier, GitHubInterventionMiner
from outcome_ledger_v2 import OutcomeLedger, VerificationStatus
from innovation_elo import InnovationElo
from transformation_tracking import TransformationTracker

def test_classifier():
    """Test the intervention classifier."""
    print("Testing InterventionClassifier...")
    
    classifier = InterventionClassifier()
    
    # Test various intervention types
    test_cases = [
        ("Add documentation for API", "documentation", ["README.md", "docs/api.md"]),
        ("Update build system with GitHub Actions", "build_system", [".github/workflows/ci.yml"]),
        ("Add new feature for user authentication", "feature_expansion", ["src/auth.py"]),
        ("Optimize database queries for performance", "performance", ["src/db/query.py"]),
        ("Migrate from Python 3.8 to 3.11", "migration", ["setup.py", "requirements.txt"]),
        ("Publish package to npm", "packaging", ["package.json"]),
        ("Add REST API endpoints", "api", ["src/api/routes.py"]),
        ("Enable cloud hosting for SaaS", "saas", ["deploy/cloud.yml"]),
        ("Integrate GPT-4 for AI features", "ai_integration", ["src/ai/gpt.py"]),
        ("Fix security vulnerability in auth", "security", ["src/auth/security.py"]),
        ("Update dependencies and clean up lockfile", "dependency_cleanup", ["package-lock.json"])
    ]
    
    for title, expected_type, files in test_cases:
        result = classifier.classify(title, "", files)
        status = "✓" if result == expected_type else "✗"
        print(f"  {status} '{title}' -> {result} (expected: {expected_type})")
    
    print()


def test_miner_with_mock():
    """Test miner with mock PR data."""
    print("Testing GitHubInterventionMiner with mock data...")
    
    miner = GitHubInterventionMiner(github_token=None)
    
    # Mock PR data
    mock_pr = {
        "number": 123,
        "title": "Add comprehensive documentation",
        "body": "This PR adds documentation for the new API",
        "merged_at": "2024-01-15T10:00:00Z",
        "created_at": "2024-01-10T10:00:00Z",
        "user": {"login": "testuser"},
        "html_url": "https://github.com/test/repo/pull/123",
        "additions": 500,
        "deletions": 50
    }
    
    # This will fail without real GitHub API, but we can test the extraction logic
    # by mocking the internal methods
    print("  Note: Full test requires GitHub token and API access")
    print("  Mock extraction test skipped (requires API)")
    print()


def test_seeding():
    """Test seeding a mock intervention."""
    print("Testing intervention seeding...")
    
    ledger = OutcomeLedger("outcome_ledger.db")
    elo_system = InnovationElo()
    transformation_tracker = TransformationTracker()
    
    # Mock intervention
    mock_intervention = {
        "asset_id": "test/test-repo",
        "asset_type": "github_repo",
        "asset_name": "test-repo",
        "developer_id": "github:testuser",
        "developer_username": "testuser",
        "before_state": {
            "stars": 100,
            "forks": 20,
            "contributors": 10,
            "language": "python",
            "category": "framework"
        },
        "intervention_type": "documentation",
        "intervention_description": "Add comprehensive documentation",
        "planned_effort_days": 7,
        "predicted_value": 30,
        "predicted_probability": 0.5,
        "predicted_risk": 0.3,
        "start_date": "2024-01-10T10:00:00Z",
        "end_date": "2024-01-15T10:00:00Z",
        "after_state": {
            "stars": 110,
            "forks": 22,
            "contributors": 11
        },
        "outcome_metrics": {
            "actual_value": 15,
            "success": True,
            "actual_risk": 0.3
        },
        "verification_link": "https://github.com/test/test-repo/pull/123"
    }
    
    try:
        # Calculate predicted outcome
        star_growth = (mock_intervention['after_state']['stars'] - mock_intervention['before_state']['stars']) / max(mock_intervention['before_state']['stars'], 1)
        contributor_growth = (mock_intervention['after_state']['contributors'] - mock_intervention['before_state']['contributors']) / max(mock_intervention['before_state']['contributors'], 1)
        
        predicted_outcome = {
            "star_growth": star_growth,
            "contributor_growth": contributor_growth
        }
        
        # Create intervention
        record_id = ledger.create_intervention(
            asset_id=mock_intervention["asset_id"],
            asset_type=mock_intervention["asset_type"],
            asset_name=mock_intervention["asset_name"],
            developer_id=mock_intervention["developer_id"],
            developer_username=mock_intervention["developer_username"],
            before_state=mock_intervention["before_state"],
            intervention_type=mock_intervention["intervention_type"],
            intervention_description=mock_intervention["intervention_description"],
            planned_effort_days=mock_intervention["planned_effort_days"],
            predicted_value=mock_intervention["predicted_value"],
            predicted_probability=mock_intervention["predicted_probability"],
            predicted_risk=mock_intervention["predicted_risk"],
            predicted_outcome=predicted_outcome
        )
        
        print(f"  ✓ Created intervention: {record_id}")
        
        # Start intervention
        ledger.start_intervention(record_id=record_id)
        print(f"  ✓ Started intervention")
        
        # Complete intervention
        ledger.complete_intervention(
            record_id=record_id,
            after_state=mock_intervention["after_state"],
            outcome_metrics=mock_intervention["outcome_metrics"]
        )
        print(f"  ✓ Completed intervention")
        
        # Verify outcome
        ledger.verify_outcome(
            record_id=record_id,
            verifier_id="test_miner",
            verifier_username="test_miner",
            status=VerificationStatus.VERIFIED.value,
            notes="Test verification"
        )
        print(f"  ✓ Verified intervention")
        
        # Update Elo
        elo_system.update_from_intervention(
            developer_id=mock_intervention["developer_id"],
            intervention_type=mock_intervention["intervention_type"],
            predicted_value=mock_intervention["predicted_value"],
            actual_value=mock_intervention["outcome_metrics"]["actual_value"]
        )
        print(f"  ✓ Updated Elo ratings")
        
        # Record transformation
        transformation_tracker.record_transformation(
            asset_id=mock_intervention["asset_id"],
            asset_type=mock_intervention["asset_type"],
            intervention_type=mock_intervention["intervention_type"],
            context=mock_intervention["before_state"],
            before_metrics=mock_intervention["before_state"],
            after_metrics=mock_intervention["after_state"]
        )
        print(f"  ✓ Recorded transformation pattern")
        
        # Save
        elo_system.save_to_file("elo_ratings.json")
        transformation_tracker.export_patterns("transformation_patterns.json")
        print(f"  ✓ Saved Elo ratings and patterns")
        
        print(f"\n✓ Test intervention seeded successfully")
        
    except Exception as e:
        print(f"  ✗ Error: {e}")
        import traceback
        traceback.print_exc()
    
    print()


def check_current_count():
    """Check current intervention count in ledger."""
    print("Checking current intervention count...")
    
    ledger = OutcomeLedger("outcome_ledger.db")
    
    # Count total interventions
    import sqlite3
    conn = sqlite3.connect("outcome_ledger.db")
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM interventions")
    total = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM interventions WHERE status = ?", (VerificationStatus.VERIFIED.value,))
    verified = cursor.fetchone()[0]
    
    conn.close()
    
    print(f"  Total interventions: {total}")
    print(f"  Verified interventions: {verified}")
    print()


if __name__ == "__main__":
    print("=" * 60)
    print("GitHub Intervention Miner - Test Suite")
    print("=" * 60)
    print()
    
    test_classifier()
    test_miner_with_mock()
    test_seeding()
    check_current_count()
    
    print("=" * 60)
    print("Test suite complete")
    print("=" * 60)
    print()
    print("To run the actual miner with GitHub API access:")
    print("  GITHUB_TOKEN=your_token python3 github_intervention_miner.py")
