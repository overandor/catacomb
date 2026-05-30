#!/usr/bin/env python3
"""
OAuth authentication for Catacomb.

Supports:
- Google OAuth 2.0
- GitHub OAuth 2.0
"""

import os
import logging
import requests
from typing import Dict, Any, Optional
from flask import session, redirect, url_for, request
from authlib.integrations.flask_client import OAuth
from auth import create_user, generate_token, verify_token
from database import get_database

logger = logging.getLogger(__name__)

# OAuth configuration
GOOGLE_CLIENT_ID = os.environ.get('GOOGLE_CLIENT_ID')
GOOGLE_CLIENT_SECRET = os.environ.get('GOOGLE_CLIENT_SECRET')
GITHUB_CLIENT_ID = os.environ.get('GITHUB_CLIENT_ID')
GITHUB_CLIENT_SECRET = os.environ.get('GITHUB_CLIENT_SECRET')

# Redirect URI
REDIRECT_URI = os.environ.get('OAUTH_REDIRECT_URI', 'http://localhost:5000/auth/callback')


class OAuthProvider:
    """OAuth provider types."""
    GOOGLE = 'google'
    GITHUB = 'github'


class OAuthManager:
    """Manages OAuth authentication flows."""
    
    def __init__(self, app=None):
        self.oauth = None
        self.app = app
        if app:
            self.init_app(app)
    
    def init_app(self, app):
        """Initialize OAuth with Flask app."""
        self.oauth = OAuth(app)
        self._register_providers()
    
    def _register_providers(self):
        """Register OAuth providers."""
        # Google OAuth
        if GOOGLE_CLIENT_ID and GOOGLE_CLIENT_SECRET:
            self.oauth.register(
                name=OAuthProvider.GOOGLE,
                client_id=GOOGLE_CLIENT_ID,
                client_secret=GOOGLE_CLIENT_SECRET,
                server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
                client_kwargs={
                    'scope': 'openid email profile'
                }
            )
            logger.info("Google OAuth registered")
        
        # GitHub OAuth
        if GITHUB_CLIENT_ID and GITHUB_CLIENT_SECRET:
            self.oauth.register(
                name=OAuthProvider.GITHUB,
                client_id=GITHUB_CLIENT_ID,
                client_secret=GITHUB_CLIENT_SECRET,
                access_token_url='https://github.com/login/oauth/access_token',
                authorize_url='https://github.com/login/oauth/authorize',
                api_base_url='https://api.github.com/',
                client_kwargs={'scope': 'user:email'},
                fetch_token=self._fetch_github_token
            )
            logger.info("GitHub OAuth registered")
    
    def _fetch_github_token(self, name, request):
        """Fetch GitHub OAuth token."""
        token = self.oauth.github.fetch_access_token(
            authorization_response=request.url
        )
        return token
    
    def get_google_login_url(self):
        """Get Google OAuth login URL."""
        if not GOOGLE_CLIENT_ID or not GOOGLE_CLIENT_SECRET:
            raise ValueError("Google OAuth not configured")
        
        return self.oauth.google.authorize_redirect(
            redirect_uri=REDIRECT_URI,
            prompt='consent'
        )
    
    def get_github_login_url(self):
        """Get GitHub OAuth login URL."""
        if not GITHUB_CLIENT_ID or not GITHUB_CLIENT_SECRET:
            raise ValueError("GitHub OAuth not configured")
        
        return self.oauth.github.authorize_redirect(
            redirect_uri=REDIRECT_URI
        )
    
    def handle_google_callback(self):
        """Handle Google OAuth callback."""
        if not GOOGLE_CLIENT_ID or not GOOGLE_CLIENT_SECRET:
            raise ValueError("Google OAuth not configured")
        
        token = self.oauth.google.authorize_access_token()
        user_info = self.oauth.google.parse_id_token(token)
        
        return self._process_oauth_user(
            provider=OAuthProvider.GOOGLE,
            user_id=user_info['sub'],
            email=user_info['email'],
            name=user_info.get('name', user_info['email'].split('@')[0]),
            picture=user_info.get('picture')
        )
    
    def handle_github_callback(self):
        """Handle GitHub OAuth callback."""
        if not GITHUB_CLIENT_ID or not GITHUB_CLIENT_SECRET:
            raise ValueError("GitHub OAuth not configured")
        
        token = self.oauth.github.authorize_access_token()
        resp = self.oauth.github.get('user', token=token)
        user_info = resp.json()
        
        # Get primary email
        email_resp = self.oauth.github.get('user/emails', token=token)
        emails = email_resp.json()
        primary_email = next((e['email'] for e in emails if e['primary'] and e['verified']), user_info.get('email'))
        
        return self._process_oauth_user(
            provider=OAuthProvider.GITHUB,
            user_id=str(user_info['id']),
            email=primary_email,
            name=user_info.get('name') or user_info.get('login'),
            picture=user_info.get('avatar_url')
        )
    
    def _process_oauth_user(self, provider: str, user_id: str, email: str, 
                           name: str, picture: Optional[str] = None) -> Dict[str, Any]:
        """
        Process OAuth user and create/update user account.
        
        Args:
            provider: OAuth provider (google or github)
            user_id: Provider-specific user ID
            email: User email
            name: User name
            picture: Profile picture URL
            
        Returns:
            User data with JWT token
        """
        db = get_database()
        
        # Check if user exists by email
        existing_users = db.select('users', where={'email': email})
        
        if existing_users:
            user = existing_users[0]
            logger.info(f"Existing user logged in via {provider}: {email}")
        else:
            # Create new user
            user = create_user(email=email, name=name, role='viewer')
            logger.info(f"New user created via {provider}: {email}")
        
        # Generate JWT token
        token = generate_token(
            user_id=str(user['id']),
            email=user['email'],
            role=user['role']
        )
        
        return {
            'user': user,
            'token': token,
            'provider': provider
        }


# Global OAuth manager instance
_oauth_manager = None


def get_oauth_manager() -> OAuthManager:
    """Get global OAuth manager instance."""
    global _oauth_manager
    return _oauth_manager


def init_oauth(app):
    """Initialize OAuth with Flask app."""
    global _oauth_manager
    _oauth_manager = OAuthManager(app)
    return _oauth_manager
