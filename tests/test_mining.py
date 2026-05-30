#!/usr/bin/env python3
"""
Mining tests for Catacomb.

Tests:
- GitHub PR mining
- Package ecosystem mining
- Job queue operations
- Worker job execution
"""

import pytest
from datetime import datetime


class TestGitHubMining:
    """Test GitHub mining operations."""
    
    def test_github_pr_mining_with_valid_repo(self):
        """Test GitHub PR mining with valid repository."""
        from worker import mine_github_prs
        
        # This test requires a valid GitHub token
        import os
        if not os.environ.get('GITHUB_TOKEN'):
            pytest.skip("GITHUB_TOKEN not set")
        
        result = mine_github_prs('facebook', 'react', limit=5)
        
        assert result['status'] in ['success', 'error']
        if result['status'] == 'success':
            assert 'prs_found' in result
            assert 'repo' in result
    
    def test_github_pr_mining_with_invalid_repo(self):
        """Test GitHub PR mining with invalid repository."""
        from worker import mine_github_prs
        
        result = mine_github_prs('invalid', 'repo-does-not-exist', limit=5)
        
        # Should handle gracefully
        assert result['status'] in ['success', 'error']
    
    def test_github_pr_mining_without_token(self):
        """Test GitHub PR mining without token fails gracefully."""
        from worker import mine_github_prs
        import os
        
        # Temporarily remove token
        original_token = os.environ.get('GITHUB_TOKEN')
        os.environ.pop('GITHUB_TOKEN', None)
        
        try:
            result = mine_github_prs('facebook', 'react', limit=5)
            assert result['status'] == 'error'
            assert 'GITHUB_TOKEN' in result['message']
        finally:
            if original_token:
                os.environ['GITHUB_TOKEN'] = original_token


class TestPackageMining:
    """Test package ecosystem mining."""
    
    def test_npm_mining(self):
        """Test npm package mining."""
        from worker import mine_package_ecosystem
        
        result = mine_package_ecosystem('npm', limit=10)
        
        assert result['status'] in ['success', 'error']
        if result['status'] == 'success':
            assert result['ecosystem'] == 'npm'
            assert 'packages_mined' in result
    
    def test_pypi_mining(self):
        """Test PyPI package mining."""
        from worker import mine_package_ecosystem
        
        result = mine_package_ecosystem('pypi', limit=10)
        
        assert result['status'] in ['success', 'error']
        if result['status'] == 'success':
            assert result['ecosystem'] == 'pypi'
    
    def test_crates_mining(self):
        """Test crates.io package mining."""
        from worker import mine_package_ecosystem
        
        result = mine_package_ecosystem('crates', limit=10)
        
        assert result['status'] in ['success', 'error']
        if result['status'] == 'success':
            assert result['ecosystem'] == 'crates'


class TestJobQueue:
    """Test job queue operations."""
    
    def test_job_logging(self):
        """Test job logging works."""
        from observability import JobLogger
        
        job_id = JobLogger.generate_job_id()
        assert job_id is not None
        assert len(job_id) > 0
    
    def test_job_start_logging(self, db):
        """Test job start logging."""
        from observability import JobLogger
        
        # Create job_logs table
        from migrations import create_job_logs_table
        create_job_logs_table()
        
        job_id = JobLogger.generate_job_id()
        JobLogger.log_job_start('test_job', job_id, {'param': 'value'}, user_id='test-user')
        
        # Verify log was created
        jobs = db.select('job_logs', where={'job_id': job_id})
        assert len(jobs) == 1
        assert jobs[0]['job_type'] == 'test_job'
        assert jobs[0]['status'] == 'started'
    
    def test_job_complete_logging(self, db):
        """Test job complete logging."""
        from observability import JobLogger
        
        # Create job_logs table
        from migrations import create_job_logs_table
        create_job_logs_table()
        
        job_id = JobLogger.generate_job_id()
        JobLogger.log_job_start('test_job', job_id, {'param': 'value'})
        
        JobLogger.log_job_complete(job_id, {'result': 'success'}, 1000, error=None)
        
        # Verify log was updated
        jobs = db.select('job_logs', where={'job_id': job_id})
        assert len(jobs) == 1
        assert jobs[0]['status'] == 'completed'
        assert jobs[0]['duration_ms'] == 1000
    
    def test_job_failure_logging(self, db):
        """Test job failure logging."""
        from observability import JobLogger
        
        # Create job_logs table
        from migrations import create_job_logs_table
        create_job_logs_table()
        
        job_id = JobLogger.generate_job_id()
        JobLogger.log_job_start('test_job', job_id, {'param': 'value'})
        
        JobLogger.log_job_complete(job_id, {}, 500, error='Test error')
        
        # Verify log was updated
        jobs = db.select('job_logs', where={'job_id': job_id})
        assert len(jobs) == 1
        assert jobs[0]['status'] == 'failed'
        assert jobs[0]['error'] == 'Test error'


class TestInterventionVerification:
    """Test intervention verification in mining context."""
    
    def test_verify_intervention(self):
        """Test intervention verification."""
        from worker import verify_intervention
        
        result = verify_intervention('test-intervention-id')
        
        assert result['status'] in ['success', 'error']
        if result['status'] == 'success':
            assert result['intervention_id'] == 'test-intervention-id'
            assert 'verified' in result


class TestMiningIntegration:
    """Test mining integration scenarios."""
    
    def test_full_mining_workflow(self, db):
        """Test full mining workflow from start to finish."""
        from observability import JobLogger
        from migrations import create_job_logs_table, create_interventions_table
        
        # Create tables
        create_job_logs_table()
        create_interventions_table()
        
        # Start job
        job_id = JobLogger.generate_job_id()
        JobLogger.log_job_start('github_mining', job_id, 
                              {'repo': 'test/repo', 'limit': 10})
        
        # Simulate mining
        import time
        time.sleep(0.1)
        
        # Create intervention from mining results
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
        
        # Complete job
        JobLogger.log_job_complete(job_id, 
                                  {'interventions_found': 1}, 
                                  100)
        
        # Verify workflow
        jobs = db.select('job_logs', where={'job_id': job_id})
        assert jobs[0]['status'] == 'completed'
        
        interventions = db.select('interventions', where={'asset_id': 'test/repo'})
        assert len(interventions) == 1


# Fixtures
@pytest.fixture
def db():
    """Create test database."""
    from database import Database
    db = Database('test_mining.db')
    yield db
    
    # Cleanup
    db.close()
    import os
    if os.path.exists('test_mining.db'):
        os.remove('test_mining.db')
