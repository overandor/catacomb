#!/usr/bin/env python3
"""
Ledger tests for Catacomb.

Tests:
- Ledger write operations
- Ledger read operations
- Intervention verification
- Outcome tracking
"""

import pytest
from datetime import datetime


class TestLedgerWrite:
    """Test ledger write operations."""
    
    def test_write_intervention(self, db):
        """Test writing intervention to ledger."""
        intervention_data = {
            'asset_id': 'test/repo',
            'intervention_type': 'documentation',
            'predicted_value': 50.0,
            'planned_effort_days': 10,
            'outcome_metrics': None,
            'before_state': {'stars': 100},
            'after_state': None,
            'verification_status': 'pending'
        }
        
        result = db.insert('interventions', intervention_data)
        assert result == 1
    
    def test_write_intervention_with_outcome(self, db):
        """Test writing intervention with outcome metrics."""
        intervention_data = {
            'asset_id': 'test/repo',
            'intervention_type': 'documentation',
            'predicted_value': 50.0,
            'planned_effort_days': 10,
            'outcome_metrics': {'actual_value': 45.0, 'stars_delta': 20},
            'before_state': {'stars': 100},
            'after_state': {'stars': 120},
            'verification_status': 'verified'
        }
        
        result = db.insert('interventions', intervention_data)
        assert result == 1
    
    def test_write_proof_packet(self, db):
        """Test writing proof packet to ledger."""
        proof_data = {
            'packet_id': 'test-proof-id',
            'packet_data': {'test': 'data'},
            'asset_id': 'test/repo',
            'intervention_type': 'documentation',
            'verification_status': 'pending',
            'created_at': datetime.utcnow().isoformat(),
            'verified_at': None
        }
        
        result = db.insert('proof_packets', proof_data)
        assert result == 1


class TestLedgerRead:
    """Test ledger read operations."""
    
    def test_read_intervention_by_asset(self, db):
        """Test reading interventions by asset ID."""
        # First write an intervention
        db.insert('interventions', {
            'asset_id': 'test/repo',
            'intervention_type': 'documentation',
            'predicted_value': 50.0,
            'planned_effort_days': 10,
            'outcome_metrics': None,
            'before_state': {'stars': 100},
            'after_state': None,
            'verification_status': 'pending'
        })
        
        # Then read it
        interventions = db.select('interventions', where={'asset_id': 'test/repo'})
        assert len(interventions) > 0
        assert interventions[0]['asset_id'] == 'test/repo'
    
    def test_read_verified_interventions(self, db):
        """Test reading only verified interventions."""
        # Write verified intervention
        db.insert('interventions', {
            'asset_id': 'test/repo',
            'intervention_type': 'documentation',
            'predicted_value': 50.0,
            'planned_effort_days': 10,
            'outcome_metrics': {'actual_value': 45.0},
            'before_state': {'stars': 100},
            'after_state': {'stars': 120},
            'verification_status': 'verified'
        })
        
        # Write pending intervention
        db.insert('interventions', {
            'asset_id': 'test/repo2',
            'intervention_type': 'api',
            'predicted_value': 30.0,
            'planned_effort_days': 5,
            'outcome_metrics': None,
            'before_state': {'stars': 50},
            'after_state': None,
            'verification_status': 'pending'
        })
        
        # Read only verified
        verified = db.select('interventions', where={'verification_status': 'verified'})
        assert len(verified) == 1
        assert verified[0]['verification_status'] == 'verified'
    
    def test_read_intervention_with_pagination(self, db):
        """Test reading interventions with pagination."""
        # Write multiple interventions
        for i in range(5):
            db.insert('interventions', {
                'asset_id': f'test/repo{i}',
                'intervention_type': 'documentation',
                'predicted_value': 50.0,
                'planned_effort_days': 10,
                'outcome_metrics': None,
                'before_state': {'stars': 100},
                'after_state': None,
                'verification_status': 'pending'
            })
        
        # Read with limit
        interventions = db.select('interventions', limit=3)
        assert len(interventions) == 3


class TestInterventionVerification:
    """Test intervention verification."""
    
    def test_verify_intervention(self, db):
        """Test verifying an intervention."""
        # Write pending intervention
        db.insert('interventions', {
            'asset_id': 'test/repo',
            'intervention_type': 'documentation',
            'predicted_value': 50.0,
            'planned_effort_days': 10,
            'outcome_metrics': None,
            'before_state': {'stars': 100},
            'after_state': None,
            'verification_status': 'pending'
        })
        
        # Verify it
        result = db.update('interventions',
                         data={
                             'verification_status': 'verified',
                             'outcome_metrics': {'actual_value': 45.0},
                             'after_state': {'stars': 120}
                         },
                         where={'asset_id': 'test/repo', 'verification_status': 'pending'})
        
        assert result == 1
        
        # Verify the update
        verified = db.select('interventions', where={'asset_id': 'test/repo'})
        assert verified[0]['verification_status'] == 'verified'
        assert verified[0]['outcome_metrics'] is not None


class TestOutcomeTracking:
    """Test outcome tracking."""
    
    def test_track_outcome_metrics(self, db):
        """Test tracking outcome metrics."""
        # Write intervention with outcome
        db.insert('interventions', {
            'asset_id': 'test/repo',
            'intervention_type': 'documentation',
            'predicted_value': 50.0,
            'planned_effort_days': 10,
            'outcome_metrics': {
                'actual_value': 45.0,
                'stars_delta': 20,
                'forks_delta': 5,
                'contributors_delta': 2
            },
            'before_state': {'stars': 100, 'forks': 10, 'contributors': 5},
            'after_state': {'stars': 120, 'forks': 15, 'contributors': 7},
            'verification_status': 'verified'
        })
        
        # Read and verify
        intervention = db.select('interventions', where={'asset_id': 'test/repo'})[0]
        assert intervention['outcome_metrics']['actual_value'] == 45.0
        assert intervention['outcome_metrics']['stars_delta'] == 20
    
    def test_calculate_prediction_accuracy(self, db):
        """Test calculating prediction accuracy."""
        # Write intervention with known outcome
        db.insert('interventions', {
            'asset_id': 'test/repo',
            'intervention_type': 'documentation',
            'predicted_value': 50.0,
            'planned_effort_days': 10,
            'outcome_metrics': {'actual_value': 45.0},
            'before_state': {'stars': 100},
            'after_state': {'stars': 120},
            'verification_status': 'verified'
        })
        
        # Calculate accuracy
        intervention = db.select('interventions', where={'asset_id': 'test/repo'})[0]
        predicted = intervention['predicted_value']
        actual = intervention['outcome_metrics']['actual_value']
        
        accuracy = 1 - abs(predicted - actual) / predicted
        assert 0 <= accuracy <= 1


# Fixtures
@pytest.fixture
def db():
    """Create test database."""
    from database import Database
    db = Database('test_ledger.db')
    
    # Create tables
    from migrations import create_interventions_table, create_proof_packets_table
    create_interventions_table()
    create_proof_packets_table()
    
    yield db
    
    # Cleanup
    db.close()
    import os
    if os.path.exists('test_ledger.db'):
        os.remove('test_ledger.db')
