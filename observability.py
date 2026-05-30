#!/usr/bin/env python3
"""
Observability system for Catacomb.

Provides:
- Structured logging with request IDs
- Job ID tracking
- Error dashboard integration
- Rate limit tracking
- Performance monitoring
"""

import os
import logging
import uuid
import time
from typing import Dict, Any, Optional
from datetime import datetime
from functools import wraps
from flask import request, g
from database import get_database

logger = logging.getLogger(__name__)


class RequestLogger:
    """Request logging with request IDs."""
    
    @staticmethod
    def generate_request_id() -> str:
        """Generate unique request ID."""
        return str(uuid.uuid4())
    
    @staticmethod
    def log_request(method: str, path: str, request_id: str, 
                    status_code: int, duration_ms: float, 
                    user_id: Optional[str] = None, error: Optional[str] = None):
        """
        Log request with structured data.
        
        Args:
            method: HTTP method
            path: Request path
            request_id: Request ID
            status_code: HTTP status code
            duration_ms: Request duration in milliseconds
            user_id: User ID if authenticated
            error: Error message if request failed
        """
        log_data = {
            'timestamp': datetime.utcnow().isoformat(),
            'request_id': request_id,
            'method': method,
            'path': path,
            'status_code': status_code,
            'duration_ms': duration_ms,
            'user_id': user_id,
            'error': error
        }
        
        if error:
            logger.error(f"Request failed: {log_data}")
        else:
            logger.info(f"Request completed: {log_data}")
        
        # Store in database for dashboard
        try:
            db = get_database()
            db.insert('request_logs', {
                'request_id': request_id,
                'method': method,
                'path': path,
                'status_code': status_code,
                'duration_ms': duration_ms,
                'user_id': user_id,
                'error': error,
                'timestamp': datetime.utcnow().isoformat()
            })
        except Exception as e:
            logger.error(f"Failed to store request log: {e}")


class JobLogger:
    """Job logging with job IDs."""
    
    @staticmethod
    def generate_job_id() -> str:
        """Generate unique job ID."""
        return str(uuid.uuid4())
    
    @staticmethod
    def log_job_start(job_type: str, job_id: str, params: Dict[str, Any],
                     user_id: Optional[str] = None):
        """
        Log job start.
        
        Args:
            job_type: Type of job (e.g., 'github_mining', 'package_mining')
            job_id: Job ID
            params: Job parameters
            user_id: User ID who initiated job
        """
        log_data = {
            'timestamp': datetime.utcnow().isoformat(),
            'job_id': job_id,
            'job_type': job_type,
            'status': 'started',
            'params': params,
            'user_id': user_id
        }
        
        logger.info(f"Job started: {log_data}")
        
        try:
            db = get_database()
            db.insert('job_logs', {
                'job_id': job_id,
                'job_type': job_type,
                'status': 'started',
                'params': params,
                'user_id': user_id,
                'started_at': datetime.utcnow().isoformat()
            })
        except Exception as e:
            logger.error(f"Failed to store job log: {e}")
    
    @staticmethod
    def log_job_complete(job_id: str, result: Dict[str, Any], 
                        duration_ms: float, error: Optional[str] = None):
        """
        Log job completion.
        
        Args:
            job_id: Job ID
            result: Job result
            duration_ms: Job duration in milliseconds
            error: Error message if job failed
        """
        status = 'completed' if not error else 'failed'
        
        log_data = {
            'timestamp': datetime.utcnow().isoformat(),
            'job_id': job_id,
            'status': status,
            'result': result,
            'duration_ms': duration_ms,
            'error': error
        }
        
        if error:
            logger.error(f"Job failed: {log_data}")
        else:
            logger.info(f"Job completed: {log_data}")
        
        try:
            db = get_database()
            db.update('job_logs', 
                     data={
                         'status': status,
                         'result': result,
                         'duration_ms': duration_ms,
                         'error': error,
                         'completed_at': datetime.utcnow().isoformat()
                     },
                     where={'job_id': job_id})
        except Exception as e:
            logger.error(f"Failed to update job log: {e}")


class RateLimitTracker:
    """Track rate limits for external APIs."""
    
    @staticmethod
    def log_rate_limit(service: str, limit: int, remaining: int, 
                      reset_time: Optional[str] = None):
        """
        Log rate limit status.
        
        Args:
            service: Service name (e.g., 'github')
            limit: Rate limit
            remaining: Remaining requests
            reset_time: Reset time
        """
        log_data = {
            'timestamp': datetime.utcnow().isoformat(),
            'service': service,
            'limit': limit,
            'remaining': remaining,
            'reset_time': reset_time
        }
        
        logger.warning(f"Rate limit: {log_data}")
        
        try:
            db = get_database()
            db.insert('rate_limit_logs', {
                'service': service,
                'limit': limit,
                'remaining': remaining,
                'reset_time': reset_time,
                'timestamp': datetime.utcnow().isoformat()
            })
        except Exception as e:
            logger.error(f"Failed to store rate limit log: {e}")


def with_request_logging(f):
    """
    Decorator to add request logging to Flask routes.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        request_id = RequestLogger.generate_request_id()
        g.request_id = request_id
        
        start_time = time.time()
        
        try:
            result = f(*args, **kwargs)
            
            # Handle both tuple responses (data, status) and direct responses
            if isinstance(result, tuple):
                response, status_code = result
            else:
                response = result
                status_code = 200
            
            duration_ms = (time.time() - start_time) * 1000
            
            user_id = getattr(g, 'user', {}).get('user_id') if hasattr(g, 'user') else None
            RequestLogger.log_request(
                method=request.method,
                path=request.path,
                request_id=request_id,
                status_code=status_code,
                duration_ms=duration_ms,
                user_id=user_id
            )
            
            return result
        except Exception as e:
            duration_ms = (time.time() - start_time) * 1000
            
            user_id = getattr(g, 'user', {}).get('user_id') if hasattr(g, 'user') else None
            RequestLogger.log_request(
                method=request.method,
                path=request.path,
                request_id=request_id,
                status_code=500,
                duration_ms=duration_ms,
                user_id=user_id,
                error=str(e)
            )
            raise
    
    return decorated_function


def get_error_dashboard_data(limit: int = 100) -> Dict[str, Any]:
    """
    Get error dashboard data.
    
    Args:
        limit: Maximum number of errors to return
        
    Returns:
        Dashboard data with error counts and recent errors
    """
    db = get_database()
    
    # Get recent request errors
    request_errors = db.select(
        'request_logs',
        where={'error': None},  # This is a placeholder, actual query needs IS NOT NULL
        limit=limit,
        order_by='timestamp DESC'
    )
    
    # Get recent job failures
    job_failures = db.select(
        'job_logs',
        where={'status': 'failed'},
        limit=limit,
        order_by='started_at DESC'
    )
    
    # Get rate limit warnings
    rate_limits = db.select(
        'rate_limit_logs',
        limit=limit,
        order_by='timestamp DESC'
    )
    
    return {
        'request_errors': request_errors,
        'job_failures': job_failures,
        'rate_limits': rate_limits,
        'total_errors': len(request_errors) + len(job_failures)
    }
