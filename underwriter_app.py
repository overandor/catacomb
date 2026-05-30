#!/usr/bin/env python3
"""
Catacomb Underwriter - Standalone Professional Service

This is the standalone Underwriter tier service for Catacomb.
It provides professional evaluation, review cards, asset desk, and portfolio management.

Features:
- Asset evaluation with professional grading
- Professional review card generation
- Asset desk dashboard
- Portfolio management
- Evidence-based scoring
- Audit logging
"""

import os
from flask import Flask, render_template, request, jsonify, send_from_directory
from flask_cors import CORS
from datetime import datetime
import json

# Import underwriter components
from developer_asset_underwriter import DeveloperAssetUnderwriter
from evidence_based_scoring import EvidenceBasedScoring
from audit_log import AuditLogger
from auth import generate_token, verify_token, require_auth, UserRole

app = Flask(__name__)
CORS(app)

# Initialize underwriter
underwriter = DeveloperAssetUnderwriter()
evidence_scoring = EvidenceBasedScoring()
audit_logger = AuditLogger()

# Configuration
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')


@app.route('/')
def index():
    """Serve the Underwriter UI."""
    return send_from_directory('static', 'underwriter.html')


@app.route('/api/health')
def health():
    """Health check endpoint."""
    return jsonify({
        'status': 'healthy',
        'service': 'catacomb-underwriter',
        'version': '1.0.0',
        'timestamp': datetime.utcnow().isoformat(),
    })


@app.route('/api/underwriter/evaluate', methods=['POST'])
def evaluate_asset():
    """
    Evaluate a software asset.
    
    Request body:
    {
        "asset_id": "string",
        "asset_name": "string",
        "classification": "string",
        "primary_language": "string",
        "file_count": int,
        "has_tests": bool,
        "has_ci_cd": bool,
        "has_documentation": bool,
        "code_quality_score": float,
        "build_status": "string",
        "test_status": "string",
        "deployment_status": "string",
        "has_license": bool,
        "license_type": "string",
        "is_fork": bool,
        "ownership_clarity": "string",
        "repo_url": "string",
        "deployment_url": "string"
    }
    """
    try:
        asset_data = request.json
        
        # Evaluate asset
        evaluation = underwriter.evaluate_asset(asset_data)
        
        # Convert to dict for JSON response
        response = {
            'asset_id': evaluation.asset_id,
            'asset_name': evaluation.asset_name,
            'grades': evaluation.grades,
            'committee_results': evaluation.committee_results,
            'strategic_classification': evaluation.strategic_classification,
            'liquidification_plan': evaluation.liquidification_plan,
            'capital_translation': evaluation.capital_translation,
            'next_action': evaluation.next_action,
            'evaluated_at': evaluation.evaluated_at.isoformat(),
        }
        
        return jsonify(response), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/underwriter/review-card', methods=['POST'])
def generate_review_card():
    """
    Generate a professional review card.
    
    Request body: Same as evaluate_asset
    """
    try:
        asset_data = request.json
        
        # Evaluate asset first
        evaluation = underwriter.evaluate_asset(asset_data)
        
        # Generate review card
        card = underwriter.review_card_generator.generate_card(
            asset_data=asset_data,
            grades=evaluation.grades,
            committee_results=evaluation.committee_results,
            strategic_classification=evaluation.strategic_classification,
            liquidification_plan=evaluation.liquidification_plan,
            capital_translation=evaluation.capital_translation,
        )
        
        # Convert to dict
        response = card.to_dict()
        
        return jsonify(response), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/underwriter/dashboard')
def get_dashboard():
    """Get asset desk dashboard summary."""
    try:
        # For now, return a mock dashboard
        # In production, this would query the database
        dashboard = {
            'portfolio_summary': {
                'total_discovered': 0,
                'real_assets': 0,
                'scaffolds': 0,
                'duplicates': 0,
                'risk_blocked': 0,
                'buyer_ready': 0,
                'lender_ready': 0,
                'collateral_packet_candidates': 0,
                'fully_financeable': 0,
                'total_strategic_value_usd': 0,
                'total_collateral_support_usd': 0,
                'average_production_grade': 'N/A',
                'average_commercial_grade': 'N/A',
                'average_collateral_grade': 'N/A',
                'average_financeability_score': 0,
            },
            'recent_evaluations': [],
        }
        
        return jsonify(dashboard), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/underwriter/portfolio', methods=['GET', 'POST'])
def portfolio():
    """Get or evaluate portfolio."""
    if request.method == 'GET':
        try:
            # Return portfolio summary
            portfolio = {
                'total_assets': 0,
                'evaluations': [],
                'portfolio_summary': {},
            }
            return jsonify(portfolio), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    elif request.method == 'POST':
        try:
            assets = request.json.get('assets', [])
            
            # Evaluate portfolio
            portfolio = underwriter.evaluate_portfolio(assets)
            
            return jsonify(portfolio), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500


@app.route('/api/underwriter/audit/<asset_id>')
def get_audit_trail(asset_id):
    """Get audit trail for an asset."""
    try:
        audit_trail = audit_logger.get_audit_trail(asset_id)
        return jsonify({'audit_trail': audit_trail}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/auth/login', methods=['POST'])
def login():
    """
    Authenticate user and return JWT token.
    
    Request body:
    {
        "email": "string",
        "password": "string"
    }
    """
    try:
        data = request.json
        email = data.get('email')
        password = data.get('password')
        
        # In production, verify password hash
        # For now, just generate a token
        token = generate_token(
            user_id=email,
            email=email,
            role=UserRole.PROFESSIONAL.value,
        )
        
        return jsonify({
            'token': token,
            'user': {
                'email': email,
                'role': UserRole.PROFESSIONAL.value,
            }
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5002))
    debug = os.environ.get('DEBUG', 'False').lower() == 'true'
    
    print(f"Starting Catacomb Underwriter service on port {port}")
    print(f"Debug mode: {debug}")
    
    app.run(host='0.0.0.0', port=port, debug=debug)
