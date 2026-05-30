#!/usr/bin/env python3
"""
Authentication and authorization system for Catacomb.

Roles:
- viewer: Public read-only access to Radar, Alpha, Interventions, Ledger, Search
- analyst: Can create and verify interventions
- verifier: Can verify intervention outcomes
- admin: Full access including Mine, Jobs, Logs, Config
"""

import os
import jwt
import logging
from datetime import datetime, timedelta
from typing import Dict, Optional, List
from functools import wraps
from flask import request, jsonify, g
from database import get_database

logger = logging.getLogger(__name__)

SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')


class UserRole:
    """User roles with permissions."""
    VIEWER = 'viewer'
    ANALYST = 'analyst'
    VERIFIER = 'verifier'
    ADMIN = 'admin'
    
    @classmethod
    def all(cls) -> List[str]:
        return [cls.VIEWER, cls.ANALYST, cls.VERIFIER, cls.ADMIN]
    
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
        public_pages = ['radar', 'alpha', 'interventions', 'ledger', 'search', 'live']
        admin_pages = ['mine', 'jobs', 'logs', 'config']
        
        if page in public_pages:
            return role in cls.all()
        elif page in admin_pages:
            return role == cls.ADMIN
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
            cls.VIEWER: ['view'],
            cls.ANALYST: ['view', 'create_intervention'],
            cls.VERIFIER: ['view', 'create_intervention', 'verify'],
            cls.ADMIN: ['view', 'create_intervention', 'verify', 'mine', 'admin']
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


def create_user(email: str, name: str, role: str = UserRole.VIEWER) -> Dict[str, Any]:
    """
    Create a new user.
    
    Args:
        email: User email
        name: User name
        role: User role
        
    Returns:
        User data
    """
    db = get_database()
    
    # Check if user exists
    existing = db.select('users', where={'email': email})
    if existing:
        logger.warning(f"User {email} already exists")
        return existing[0]
    
    # Create user
    user_data = {
        'email': email,
        'name': name,
        'role': role,
        'created_at': datetime.utcnow().isoformat(),
        'updated_at': datetime.utcnow().isoformat()
    }
    
    db.insert('users', user_data)
    
    # Fetch created user
    user = db.select('users', where={'email': email})[0]
    logger.info(f"Created user {email} with role {role}")
    return user


def get_user_by_email(email: str) -> Optional[Dict[str, Any]]:
    """
    Get user by email.
    
    Args:
        email: User email
        
    Returns:
        User data or None
    """
    db = get_database()
    users = db.select('users', where={'email': email})
    return users[0] if users else None


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
                UserRole.VIEWER: 0,
                UserRole.ANALYST: 1,
                UserRole.VERIFIER: 2,
                UserRole.ADMIN: 3
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
    return user and user.get('role') == UserRole.ADMIN


def is_verifier() -> bool:
    """Check if current user is verifier or admin."""
    user = get_current_user()
    return user and user.get('role') in [UserRole.VERIFIER, UserRole.ADMIN]


def is_analyst() -> bool:
    """Check if current user is analyst, verifier, or admin."""
    user = get_current_user()
    return user and user.get('role') in [UserRole.ANALYST, UserRole.VERIFIER, UserRole.ADMIN]
