#!/usr/bin/env python3
"""
Structured error handling for Catacomb.

Provides consistent error responses for:
- GitHub rate limits
- Missing tokens
- Invalid repositories
- Backend unavailability
- Database errors
- Mining job failures
"""

import logging
from typing import Dict, Any, Optional
from flask import jsonify
from datetime import datetime

logger = logging.getLogger(__name__)


class CatacombError(Exception):
    """Base exception for Catacomb errors."""
    
    def __init__(self, message: str, error_code: str, status_code: int = 500):
        self.message = message
        self.error_code = error_code
        self.status_code = status_code
        self.timestamp = datetime.utcnow().isoformat()
        super().__init__(message)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert error to dictionary."""
        return {
            'error': self.error_code,
            'message': self.message,
            'timestamp': self.timestamp
        }


class GitHubRateLimitError(CatacombError):
    """GitHub API rate limit exceeded."""
    
    def __init__(self, reset_time: Optional[str] = None):
        message = "GitHub API rate limit exceeded"
        if reset_time:
            message += f". Resets at {reset_time}"
        super().__init__(message, 'GITHUB_RATE_LIMIT', 429)
        self.reset_time = reset_time
    
    def to_dict(self) -> Dict[str, Any]:
        data = super().to_dict()
        if self.reset_time:
            data['reset_time'] = self.reset_time
        return data


class GitHubTokenError(CatacombError):
    """GitHub token missing or invalid."""
    
    def __init__(self, reason: str = "GitHub token is missing or invalid"):
        super().__init__(reason, 'GITHUB_TOKEN_ERROR', 401)


class InvalidRepositoryError(CatacombError):
    """Invalid repository format or repository not found."""
    
    def __init__(self, repo: str, reason: str = "Repository not found or invalid"):
        message = f"Invalid repository: {repo}. {reason}"
        super().__init__(message, 'INVALID_REPOSITORY', 400)
        self.repo = repo
    
    def to_dict(self) -> Dict[str, Any]:
        data = super().to_dict()
        data['repository'] = self.repo
        return data


class DatabaseError(CatacombError):
    """Database operation failed."""
    
    def __init__(self, reason: str = "Database operation failed"):
        super().__init__(reason, 'DATABASE_ERROR', 500)


class BackendUnavailableError(CatacombError):
    """Backend service unavailable."""
    
    def __init__(self, service: str = "Backend service"):
        message = f"{service} is currently unavailable"
        super().__init__(message, 'BACKEND_UNAVAILABLE', 503)
        self.service = service
    
    def to_dict(self) -> Dict[str, Any]:
        data = super().to_dict()
        data['service'] = self.service
        return data


class MiningJobError(CatacombError):
    """Mining job failed."""
    
    def __init__(self, job_id: str, reason: str = "Mining job failed"):
        message = f"Mining job {job_id} failed: {reason}"
        super().__init__(message, 'MINING_JOB_ERROR', 500)
        self.job_id = job_id
    
    def to_dict(self) -> Dict[str, Any]:
        data = super().to_dict()
        data['job_id'] = self.job_id
        return data


class AuthenticationError(CatacombError):
    """Authentication failed."""
    
    def __init__(self, reason: str = "Authentication failed"):
        super().__init__(reason, 'AUTH_ERROR', 401)


class AuthorizationError(CatacombError):
    """Authorization failed."""
    
    def __init__(self, reason: str = "Insufficient permissions"):
        super().__init__(reason, 'AUTH_ERROR', 403)


class ValidationError(CatacombError):
    """Input validation failed."""
    
    def __init__(self, field: str, reason: str = "Validation failed"):
        message = f"Validation failed for {field}: {reason}"
        super().__init__(message, 'VALIDATION_ERROR', 400)
        self.field = field
    
    def to_dict(self) -> Dict[str, Any]:
        data = super().to_dict()
        data['field'] = self.field
        return data


def handle_error(error: Exception) -> tuple:
    """
    Handle error and return Flask response.
    
    Args:
        error: Exception to handle
        
    Returns:
        Tuple of (response_dict, status_code)
    """
    if isinstance(error, CatacombError):
        logger.error(f"{error.error_code}: {error.message}")
        return error.to_dict(), error.status_code
    else:
        logger.error(f"Unexpected error: {str(error)}")
        return {
            'error': 'INTERNAL_ERROR',
            'message': 'An unexpected error occurred',
            'timestamp': datetime.utcnow().isoformat()
        }, 500


def error_response(error_code: str, message: str, status_code: int = 500, **kwargs) -> tuple:
    """
    Create error response.
    
    Args:
        error_code: Error code
        message: Error message
        status_code: HTTP status code
        **kwargs: Additional error data
        
    Returns:
        Tuple of (response_dict, status_code)
    """
    response = {
        'error': error_code,
        'message': message,
        'timestamp': datetime.utcnow().isoformat()
    }
    response.update(kwargs)
    
    logger.error(f"{error_code}: {message}")
    return response, status_code


def check_github_token() -> None:
    """
    Check if GitHub token is available.
    
    Raises:
        GitHubTokenError: If token is missing
    """
    import os
    token = os.environ.get('GITHUB_TOKEN')
    if not token:
        raise GitHubTokenError("GITHUB_TOKEN environment variable not set")


def check_repo_format(repo: str) -> None:
    """
    Check if repository format is valid.
    
    Args:
        repo: Repository string (e.g., "owner/repo")
        
    Raises:
        InvalidRepositoryError: If format is invalid
    """
    if not repo or '/' not in repo:
        raise InvalidRepositoryError(repo, "Repository must be in 'owner/repo' format")
    
    parts = repo.split('/')
    if len(parts) != 2 or not all(parts):
        raise InvalidRepositoryError(repo, "Repository must be in 'owner/repo' format")


def check_github_rate_limit(response_status: int, response_headers: Dict[str, str]) -> None:
    """
    Check if GitHub rate limit was hit.
    
    Args:
        response_status: HTTP response status
        response_headers: Response headers
        
    Raises:
        GitHubRateLimitError: If rate limit exceeded
    """
    if response_status == 403:
        reset_time = response_headers.get('X-RateLimit-Reset')
        raise GitHubRateLimitError(reset_time)
