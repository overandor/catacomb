"""Smoke tests for all public Catacomb API routes and pages."""
import pytest
from app import app


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


class TestPublicPages:
    def test_health(self, client):
        resp = client.get('/api/health')
        assert resp.status_code == 200
        data = resp.get_json()
        assert data['status'] == 'healthy'

    def test_metrics(self, client):
        resp = client.get('/api/metrics')
        assert resp.status_code == 200

    def test_radar(self, client):
        resp = client.get('/api/radar')
        assert resp.status_code == 200

    def test_interventions(self, client):
        resp = client.get('/api/interventions')
        assert resp.status_code == 200

    def test_ledger(self, client):
        resp = client.get('/api/ledger')
        assert resp.status_code == 200

    def test_discover_promising(self, client):
        resp = client.get('/api/discover/promising')
        assert resp.status_code == 200

    def test_api_v1_search(self, client):
        resp = client.get('/api/v1/search?q=dep')
        assert resp.status_code == 200
        data = resp.get_json()
        assert 'results' in data

    def test_api_v1_dashboard_summary(self, client):
        resp = client.get('/api/v1/dashboard/summary')
        assert resp.status_code == 200
        data = resp.get_json()
        assert 'total_interventions' in data

    def test_api_v1_repo_ingest(self, client):
        resp = client.post('/api/v1/repo/ingest', json={'owner': 'facebook', 'repo': 'react'})
        assert resp.status_code == 200
        data = resp.get_json()
        assert data['status'] == 'ingested'

    def test_api_v1_inference_proof(self, client):
        resp = client.post('/api/v1/inference/proof', json={
            'model': 'test', 'prompt': 'hi', 'response': 'hello'
        })
        assert resp.status_code == 200
        data = resp.get_json()
        assert 'proof_id' in data

    def test_api_v1_inference_proof_store(self, client):
        resp = client.post('/api/v1/inference/proof', json={
            'model': 'test', 'prompt': 'hi', 'response': 'hello', 'store_in_ledger': True
        })
        assert resp.status_code == 200
        data = resp.get_json()
        assert 'stored_record_id' in data

    def test_api_v1_verify_proof_not_found(self, client):
        resp = client.get('/api/v1/proof/does-not-exist/verify')
        assert resp.status_code == 404
        data = resp.get_json()
        assert 'error' in data

    def test_api_404_returns_json(self, client):
        resp = client.get('/api/nonexistent')
        assert resp.status_code == 404
        data = resp.get_json()
        assert data['status'] == 'error'
