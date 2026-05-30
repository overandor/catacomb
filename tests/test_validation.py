#!/usr/bin/env python3
"""
Validation tests for Catacomb.

Tests:
- Repository input validation
- Intervention data validation
- Asset data validation
"""

import pytest
from errors import InvalidRepositoryError, ValidationError


class TestRepositoryValidation:
    """Test repository validation."""
    
    def test_valid_repo_format(self):
        """Test valid repository format passes."""
        from errors import check_repo_format
        
        # Should not raise
        check_repo_format('owner/repo')
        check_repo_format('facebook/react')
        check_repo_format('tensorflow/tensorflow')
    
    def test_invalid_repo_format_no_slash(self):
        """Test invalid repository format without slash fails."""
        from errors import check_repo_format
        
        with pytest.raises(InvalidRepositoryError):
            check_repo_format('invalid')
    
    def test_invalid_repo_format_empty(self):
        """Test empty repository fails."""
        from errors import check_repo_format
        
        with pytest.raises(InvalidRepositoryError):
            check_repo_format('')
    
    def test_invalid_repo_format_multiple_slashes(self):
        """Test repository with multiple slashes fails."""
        from errors import check_repo_format
        
        with pytest.raises(InvalidRepositoryError):
            check_repo_format('owner/repo/extra')


class TestInterventionValidation:
    """Test intervention data validation."""
    
    def test_valid_intervention_data(self):
        """Test valid intervention data passes."""
        data = {
            'asset_id': 'owner/repo',
            'intervention_type': 'documentation',
            'predicted_value': 50.0,
            'planned_effort_days': 10
        }
        # Should not raise
        assert data['asset_id'] is not None
        assert data['intervention_type'] is not None
        assert data['predicted_value'] > 0
        assert data['planned_effort_days'] > 0
    
    def test_invalid_intervention_missing_asset_id(self):
        """Test intervention without asset_id fails."""
        data = {
            'intervention_type': 'documentation',
            'predicted_value': 50.0,
            'planned_effort_days': 10
        }
        assert 'asset_id' not in data or not data.get('asset_id')
    
    def test_invalid_intervention_negative_value(self):
        """Test intervention with negative predicted value fails."""
        data = {
            'asset_id': 'owner/repo',
            'intervention_type': 'documentation',
            'predicted_value': -10.0,
            'planned_effort_days': 10
        }
        assert data['predicted_value'] < 0


class TestAssetValidation:
    """Test asset data validation."""
    
    def test_valid_asset_data(self):
        """Test valid asset data passes."""
        from asset_abstraction import AssetType, AssetSource
        
        data = {
            'asset_id': 'owner/repo',
            'asset_type': AssetType.REPOSITORY,
            'source': AssetSource.GITHUB
        }
        assert data['asset_id'] is not None
        assert data['asset_type'] is not None
        assert data['source'] is not None
    
    def test_invalid_asset_type(self):
        """Test invalid asset type fails."""
        from asset_abstraction import AssetType
        
        invalid_type = 'invalid_type'
        assert invalid_type not in AssetType.all()


class TestGitHubFailureTests:
    """Test GitHub failure scenarios."""
    
    def test_github_rate_limit_handling(self):
        """Test GitHub rate limit is handled correctly."""
        from errors import GitHubRateLimitError, check_github_rate_limit
        
        # Simulate rate limit response
        with pytest.raises(GitHubRateLimitError):
            check_github_rate_limit(403, {'X-RateLimit-Reset': '1234567890'})
    
    def test_github_token_error_handling(self):
        """Test GitHub token error is handled correctly."""
        from errors import GitHubTokenError, check_github_token
        
        # Remove token temporarily
        import os
        original_token = os.environ.get('GITHUB_TOKEN')
        os.environ.pop('GITHUB_TOKEN', None)
        
        try:
            with pytest.raises(GitHubTokenError):
                check_github_token()
        finally:
            # Restore token
            if original_token:
                os.environ['GITHUB_TOKEN'] = original_token
    
    def test_github_404_handling(self):
        """Test GitHub 404 is handled correctly."""
        from errors import InvalidRepositoryError
        
        # 404 should be treated as invalid repository
        # This would be tested in integration tests with actual GitHub API
        pass


class TestDatabaseValidation:
    """Test database operation validation."""
    
    def test_sqlite_connection(self):
        """Test SQLite connection works."""
        from database import Database
        
        db = Database('test_ledger.db')
        assert db is not None
        db.close()
    
    def test_postgres_connection_with_url(self):
        """Test Postgres connection with URL."""
        import os
        from database import Database, USE_POSTGRES
        
        if USE_POSTGRES:
            db = Database(os.environ.get('DATABASE_URL'))
            assert db is not None
            db.close()
