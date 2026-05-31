#!/usr/bin/env python3
"""
Authentication and authorization system for Catacomb.

Three-tier product model:
- PUBLIC: Radar (asset discovery, innovation alpha)
- PROFESSIONAL: Underwriter (professional evaluation, review cards, asset desk)
- ADMIN: Mine (job mining, competency graph, system configuration)
"""

import os
import jwt
import logging
from datetime import datetime, timedelta
from typing import Dict, Optional, List, Any
from functools import wraps
from flask import request, jsonify, g
from enum import Enum

logger = logging.getLogger(__name__)

SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')


class UserRole(Enum):
    """User roles for three-tier product model."""
    PUBLIC = "public"
    PROFESSIONAL = "professional"
    ADMIN = "admin"
    
    @classmethod
    def all(cls) -> List[str]:
        return [role.value for role in cls]
    
    @classmethod
    def can_access_page(cls, role: str, page: str) -> bool:
        """
        Check if a role can access a page.
        
        Args:
            role: User role
            page: Page name
            
        Returns:
            True if role can access page
        """
        # Radar tier (public)
        radar_pages = ['radar', 'alpha', 'search']
        
        # Underwriter tier (professional)
        underwriter_pages = ['underwriter', 'asset-desk', 'review-cards', 'portfolio']
        
        # Mine tier (admin)
        mine_pages = ['mine', 'interventions', 'ledger', 'competency']
        
        # Live (all tiers)
        all_pages = ['live']
        
        if page in radar_pages:
            return role in cls.all()
        elif page in underwriter_pages:
            return role in [cls.PROFESSIONAL.value, cls.ADMIN.value]
        elif page in mine_pages:
            return role == cls.ADMIN.value
        elif page in all_pages:
            return role in cls.all()
        return False
    
    @classmethod
    def can_perform_action(cls, role: str, action: str) -> bool:
        """
        Check if a role can perform an action.
        
        Args:
            role: User role
            action: Action name
            
        Returns:
            True if role can perform action
        """
        permissions = {
            cls.PUBLIC.value: ['view_radar', 'view_alpha', 'search'],
            cls.PROFESSIONAL.value: [
                'view_radar', 'view_alpha', 'search',
                'evaluate_asset', 'generate_review_card', 'view_asset_desk', 'manage_portfolio'
            ],
            cls.ADMIN.value: [
                'view_radar', 'view_alpha', 'search',
                'evaluate_asset', 'generate_review_card', 'view_asset_desk', 'manage_portfolio',
                'mine_jobs', 'edit_competency_graph', 'view_all_audit_logs', 'configure_system'
            ]
        }
        
        return action in permissions.get(role, [])


def generate_token(user_id: str, email: str, role: str, expires_hours: int = 24) -> str:
    """
    Generate JWT token for user.
    
    Args:
        user_id: User ID
        email: User email
        role: User role
        expires_hours: Token expiration in hours
        
    Returns:
        JWT token string
    """
    payload = {
        'user_id': user_id,
        'email': email,
        'role': role,
        'exp': datetime.utcnow() + timedelta(hours=expires_hours),
        'iat': datetime.utcnow()
    }
    
    token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
    logger.info(f"Generated token for user {email} with role {role}")
    return token


def verify_token(token: str) -> Optional[Dict[str, Any]]:
    """
    Verify JWT token.
    
    Args:
        token: JWT token string
        
    Returns:
        Decoded payload if valid, None otherwise
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        logger.info(f"Verified token for user {payload.get('email')}")
        return payload
    except jwt.ExpiredSignatureError:
        logger.warning("Token expired")
        return None
    except jwt.InvalidTokenError as e:
        logger.warning(f"Invalid token: {e}")
        return None


def create_user(email: str, password_hash: str, role: str = UserRole.PUBLIC.value) -> Dict[str, Any]:
    """
    Create a new user.
    
    Args:
        email: User email
        password_hash: Hashed password
        role: User role
        
    Returns:
        User data
    """
    from database_manager import get_database_manager
    from database_schema import UserRole as DBUserRole
    
    db = get_database_manager()
    
    # Map string role to enum
    role_mapping = {
        UserRole.PUBLIC.value: DBUserRole.PUBLIC,
        UserRole.PROFESSIONAL.value: DBUserRole.PROFESSIONAL,
        UserRole.ADMIN.value: DBUserRole.ADMIN,
    }
    
    db_role = role_mapping.get(role, DBUserRole.PUBLIC)
    
    # Check if user exists
    existing = db.get_user_by_email(email)
    if existing:
        logger.warning(f"User {email} already exists")
        return {
            'id': existing.id,
            'email': existing.email,
            'role': existing.role.value,
        }
    
    # Create user
    user = db.create_user(
        email=email,
        password_hash=password_hash,
        role=db_role,
    )
    
    logger.info(f"Created user {email} with role {role}")
    return {
        'id': user.id,
        'email': user.email,
        'role': user.role.value,
    }


def get_user_by_email(email: str) -> Optional[Dict[str, Any]]:
    """
    Get user by email.
    
    Args:
        email: User email
        
    Returns:
        User data or None
    """
    from database_manager import get_database_manager
    
    db = get_database_manager()
    user = db.get_user_by_email(email)
    
    if user:
        return {
            'id': user.id,
            'email': user.email,
            'role': user.role.value,
        }
    return None


def require_role(required_role: str):
    """
    Decorator to require specific role for endpoint.
    
    Args:
        required_role: Required role (or higher)
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            token = request.headers.get('Authorization', '').replace('Bearer ', '')
            
            if not token:
                return jsonify({'error': 'No token provided'}), 401
            
            payload = verify_token(token)
            if not payload:
                return jsonify({'error': 'Invalid or expired token'}), 401
            
            user_role = payload.get('role')
            
            # Check role hierarchy
            role_hierarchy = {
                UserRole.PUBLIC.value: 0,
                UserRole.PROFESSIONAL.value: 1,
                UserRole.ADMIN.value: 2
            }
            
            if role_hierarchy.get(user_role, 0) < role_hierarchy.get(required_role, 0):
                return jsonify({'error': 'Insufficient permissions'}), 403
            
            g.user = payload
            return f(*args, **kwargs)
        
        return decorated_function
    return decorator


def require_auth(f):
    """
    Decorator to require authentication for endpoint.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.headers.get('Authorization', '').replace('Bearer ', '')
        
        if not token:
            return jsonify({'error': 'No token provided'}), 401
        
        payload = verify_token(token)
        if not payload:
            return jsonify({'error': 'Invalid or expired token'}), 401
        
        g.user = payload
        return f(*args, **kwargs)
    
    return decorated_function


def get_current_user() -> Optional[Dict[str, Any]]:
    """
    Get current authenticated user from Flask g object.
    
    Returns:
        User data or None
    """
    return getattr(g, 'user', None)


def is_admin() -> bool:
    """Check if current user is admin."""
    user = get_current_user()
    return user and user.get('role') == UserRole.ADMIN.value


def is_professional() -> bool:
    """Check if current user is professional or admin."""
    user = get_current_user()
    return user and user.get('role') in [UserRole.PROFESSIONAL.value, UserRole.ADMIN.value]


def is_public() -> bool:
    """Check if current user is authenticated (any tier)."""
    user = get_current_user()
    return user is not None
