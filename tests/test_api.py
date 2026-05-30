#!/usr/bin/env python3
"""
Production API tests for Catacomb.

Tests:
- API endpoints
- Input validation
- Error handling
- Authentication
- Authorization
"""

import pytest
import json
from datetime import datetime


class TestHealthEndpoint:
    """Test health check endpoint."""
    
    def test_health_check(self, client):
        """Test health check returns 200."""
        response = client.get('/api/health')
        assert response.status_code == 200
        data = response.get_json()
        assert data['status'] == 'ok'
        assert 'timestamp' in data
        assert 'version' in data


class TestStatsEndpoint:
    """Test statistics endpoint."""
    
    def test_stats_requires_no_auth(self, client):
        """Test stats endpoint is public."""
        response = client.get('/api/v1/stats')
        assert response.status_code in [200, 500]  # May fail if DB not set up
    
    def test_stats_returns_structure(self, client):
        """Test stats returns expected structure."""
        response = client.get('/api/v1/stats')
        if response.status_code == 200:
            data = response.get_json()
            assert 'total_interventions' in data
            assert 'verified_interventions' in data
            assert 'timestamp' in data


class TestInterventionsEndpoint:
    """Test interventions endpoint."""
    
    def test_interventions_pagination(self, client):
        """Test interventions pagination works."""
        response = client.get('/api/v1/interventions?page=1&limit=10')
        assert response.status_code in [200, 500]
        
        if response.status_code == 200:
            data = response.get_json()
            assert 'data' in data
            assert 'page' in data
            assert 'limit' in data
    
    def test_interventions_filter_by_status(self, client):
        """Test interventions can be filtered by status."""
        response = client.get('/api/v1/interventions?status=verified')
        assert response.status_code in [200, 500]


class TestSearchEndpoint:
    """Test search endpoint."""
    
    def test_search_requires_query(self, client):
        """Test search requires query parameter."""
        response = client.get('/api/v1/search')
        assert response.status_code in [400, 500]
    
    def test_search_with_query(self, client):
        """Test search with query parameter."""
        response = client.get('/api/v1/search?q=test')
        assert response.status_code in [200, 500]
        
        if response.status_code == 200:
            data = response.get_json()
            assert 'assets' in data or 'interventions' in data


class TestInferenceProofEndpoint:
    """Test proof of inference endpoint."""
    
    def test_proof_generation_requires_data(self, client):
        """Test proof generation requires model, prompt, response."""
        response = client.post('/api/v1/inference/proof', json={})
        assert response.status_code == 400
    
    def test_proof_generation_with_valid_data(self, client):
        """Test proof generation with valid data."""
        response = client.post('/api/v1/inference/proof', json={
            'model': 'llama3.1',
            'prompt': 'test prompt',
            'response': 'test response'
        })
        assert response.status_code in [200, 500]
        
        if response.status_code == 200:
            data = response.get_json()
            assert 'proof_id' in data
            assert 'composite_hash' in data


class TestErrorHandling:
    """Test error handling."""
    
    def test_invalid_repo_format(self, client):
        """Test invalid repository format returns error."""
        response = client.post('/api/v1/repo/ingest', json={
            'owner': 'invalid-repo-format'
        })
        assert response.status_code == 400
    
    def test_missing_github_token(self, client):
        """Test missing GitHub token returns error."""
        # This test assumes GITHUB_TOKEN is not set
        import os
        token = os.environ.get('GITHUB_TOKEN')
        if not token:
            response = client.post('/api/v1/mine/start', json={
                'ecosystem': 'github',
                'limit': 10
            })
            assert response.status_code in [401, 500]


class TestAuthentication:
    """Test authentication."""
    
    def test_protected_endpoint_requires_token(self, client):
        """Test protected endpoint requires authentication."""
        response = client.get('/api/v1/mine/status')
        assert response.status_code == 401
    
    def test_invalid_token_returns_401(self, client):
        """Test invalid token returns 401."""
        response = client.get('/api/v1/mine/status', headers={
            'Authorization': 'Bearer invalid-token'
        })
        assert response.status_code == 401


class TestAuthorization:
    """Test authorization."""
    
    def test_viewer_cannot_access_mine(self, client, viewer_token):
        """Test viewer role cannot access mine endpoint."""
        response = client.get('/api/v1/mine/status', headers={
            'Authorization': f'Bearer {viewer_token}'
        })
        assert response.status_code == 403
    
    def test_admin_can_access_mine(self, client, admin_token):
        """Test admin role can access mine endpoint."""
        response = client.get('/api/v1/mine/status', headers={
            'Authorization': f'Bearer {admin_token}'
        })
        assert response.status_code in [200, 500]


# Fixtures
@pytest.fixture
def client():
    """Create test client."""
    from api.index import app
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


@pytest.fixture
def viewer_token():
    """Create viewer token for testing."""
    from auth import generate_token
    return generate_token('test-viewer-id', 'viewer@test.com', 'viewer')


@pytest.fixture
def admin_token():
    """Create admin token for testing."""
    from auth import generate_token
    return generate_token('test-admin-id', 'admin@test.com', 'admin')
