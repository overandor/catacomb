#!/usr/bin/env python3
"""
Job Description Source Compliance Module.

Ensures that job descriptions used for competency graph mining comply with:
- Terms of service of job boards
- Copyright and licensing requirements
- Rate limiting and API usage policies
- Data retention and privacy requirements
"""

import os
import time
import hashlib
from typing import Dict, List, Optional, Set
from datetime import datetime, timedelta
from enum import Enum


class JobSource(Enum):
    """Supported job description sources with compliance requirements."""
    LINKEDIN = "linkedin"
    INDEED = "indeed"
    GITHUB_JOBS = "github_jobs"
    REMOTE_CO = "remote_co"
    WE_WORK_REMOTELY = "we_work_remotely"
    ANGEL_LIST = "angel_list"
    GREENHOUSE = "greenhouse"
    LEVER = "lever"
    CUSTOM_API = "custom_api"
    MANUAL_ENTRY = "manual_entry"


class ComplianceStatus(Enum):
    """Compliance status for job descriptions."""
    COMPLIANT = "compliant"
    NON_COMPLIANT = "non_compliant"
    REVIEW_REQUIRED = "review_required"
    RATE_LIMITED = "rate_limited"
    EXPIRED = "expired"


class JobSourceCompliance:
    """
    Manages compliance for job description sources.
    
    Tracks:
    - Rate limits per source
    - Terms of service compliance
    - Data retention policies
    - Source-specific requirements
    """
    
    def __init__(self):
        """Initialize compliance manager."""
        self.rate_limits = {
            JobSource.LINKEDIN: {"requests_per_minute": 30, "requests_per_day": 1000},
            JobSource.INDEED: {"requests_per_minute": 10, "requests_per_day": 500},
            JobSource.GITHUB_JOBS: {"requests_per_minute": 60, "requests_per_day": 5000},
            JobSource.REMOTE_CO: {"requests_per_minute": 10, "requests_per_day": 1000},
            JobSource.WE_WORK_REMOTELY: {"requests_per_minute": 10, "requests_per_day": 1000},
            JobSource.ANGEL_LIST: {"requests_per_minute": 30, "requests_per_day": 1000},
            JobSource.GREENHOUSE: {"requests_per_minute": 60, "requests_per_day": 10000},
            JobSource.LEVER: {"requests_per_minute": 60, "requests_per_day": 10000},
            JobSource.CUSTOM_API: {"requests_per_minute": 60, "requests_per_day": 10000},
            JobSource.MANUAL_ENTRY: {"requests_per_minute": 9999, "requests_per_day": 999999},
        }
        
        self.request_history = {}  # source -> list of timestamps
        self.tos_acceptance = {}  # source -> acceptance timestamp
        self.data_retention_days = 90  # Default retention period
        
    def check_rate_limit(self, source: JobSource) -> tuple[bool, int]:
        """
        Check if a request can be made to a source.
        
        Args:
            source: Job source
            
        Returns:
            (allowed, seconds_until_reset)
        """
        now = datetime.utcnow()
        limits = self.rate_limits.get(source, {"requests_per_minute": 60, "requests_per_day": 10000})
        
        # Initialize history if needed
        if source not in self.request_history:
            self.request_history[source] = []
        
        # Filter old requests
        minute_ago = now - timedelta(minutes=1)
        day_ago = now - timedelta(days=1)
        
        self.request_history[source] = [
            ts for ts in self.request_history[source]
            if ts > minute_ago
        ]
        
        # Check minute limit
        if len(self.request_history[source]) >= limits["requests_per_minute"]:
            reset_time = minute_ago + timedelta(minutes=1)
            seconds_until_reset = (reset_time - now).total_seconds()
            return False, int(seconds_until_reset)
        
        # Check day limit (simplified - in production would check full day history)
        # For now, just check minute limit
        return True, 0
    
    def record_request(self, source: JobSource):
        """Record a request to a source."""
        if source not in self.request_history:
            self.request_history[source] = []
        self.request_history[source].append(datetime.utcnow())
    
    def accept_tos(self, source: JobSource, accepted_by: str) -> bool:
        """
        Record terms of service acceptance for a source.
        
        Args:
            source: Job source
            accepted_by: User or system accepting the ToS
            
        Returns:
            True if accepted successfully
        """
        self.tos_acceptance[source] = {
            "accepted_at": datetime.utcnow(),
            "accepted_by": accepted_by,
        }
        return True
    
    def is_tos_accepted(self, source: JobSource) -> bool:
        """Check if ToS has been accepted for a source."""
        return source in self.tos_acceptance
    
    def check_compliance(self, job_data: Dict) -> tuple[ComplianceStatus, List[str]]:
        """
        Check if a job description is compliant.
        
        Args:
            job_data: Job description data
            
        Returns:
            (status, warnings)
        """
        warnings = []
        
        # Check source
        source_str = job_data.get("source", "unknown")
        try:
            source = JobSource(source_str)
        except ValueError:
            warnings.append(f"Unknown source: {source_str}")
            return ComplianceStatus.REVIEW_REQUIRED, warnings
        
        # Check ToS acceptance
        if not self.is_tos_accepted(source):
            warnings.append(f"Terms of service not accepted for {source.value}")
            return ComplianceStatus.NON_COMPLIANT, warnings
        
        # Check data age
        posted_date = job_data.get("posted_date")
        if posted_date:
            if isinstance(posted_date, str):
                try:
                    posted_date = datetime.fromisoformat(posted_date)
                except ValueError:
                    warnings.append("Invalid posted_date format")
            if isinstance(posted_date, datetime):
                age = datetime.utcnow() - posted_date
                if age.days > self.data_retention_days:
                    warnings.append(f"Job description is {age.days} days old (exceeds {self.data_retention_days} day retention)")
                    return ComplianceStatus.EXPIRED, warnings
        
        # Check for required fields
        required_fields = ["role_family", "title", "description"]
        for field in required_fields:
            if not job_data.get(field):
                warnings.append(f"Missing required field: {field}")
        
        # Check for PII (simplified - in production would use regex patterns)
        description = job_data.get("description", "")
        if "@" in description and "email" in description.lower():
            warnings.append("Potential email address found in description")
        
        if warnings:
            return ComplianceStatus.REVIEW_REQUIRED, warnings
        
        return ComplianceStatus.COMPLIANT, []
    
    def generate_compliance_report(self) -> Dict:
        """Generate a compliance report for all sources."""
        report = {
            "generated_at": datetime.utcnow().isoformat(),
            "sources": {},
            "summary": {
                "total_sources": len(JobSource),
                "tos_accepted": len(self.tos_acceptance),
                "rate_limited": 0,
            },
        }
        
        for source in JobSource:
            source_data = {
                "tos_accepted": self.is_tos_accepted(source),
                "rate_limit": self.rate_limits.get(source),
                "recent_requests": len(self.request_history.get(source, [])),
            }
            
            allowed, _ = self.check_rate_limit(source)
            if not allowed:
                source_data["rate_limited"] = True
                report["summary"]["rate_limited"] += 1
            
            report["sources"][source.value] = source_data
        
        return report
    
    def cleanup_old_data(self, days: int = None):
        """
        Clean up old request history data.
        
        Args:
            days: Days to keep (default: data_retention_days)
        """
        if days is None:
            days = self.data_retention_days
        
        cutoff = datetime.utcnow() - timedelta(days=days)
        
        for source in list(self.request_history.keys()):
            self.request_history[source] = [
                ts for ts in self.request_history[source]
                if ts > cutoff
            ]


class JobDescriptionComplianceChecker:
    """
    High-level compliance checker for job descriptions.
    
    Integrates with the job description mining pipeline to ensure
    all mined job descriptions are compliant with source requirements.
    """
    
    def __init__(self):
        """Initialize compliance checker."""
        self.compliance = JobSourceCompliance()
        self.compliant_jobs = set()
        self.non_compliant_jobs = set()
        self.review_required_jobs = set()
    
    def check_job_description(self, job_data: Dict) -> tuple[ComplianceStatus, List[str]]:
        """
        Check a single job description for compliance.
        
        Args:
            job_data: Job description data
            
        Returns:
            (status, warnings)
        """
        status, warnings = self.compliance.check_compliance(job_data)
        
        job_id = job_data.get("job_id", "unknown")
        
        if status == ComplianceStatus.COMPLIANT:
            self.compliant_jobs.add(job_id)
        elif status == ComplianceStatus.NON_COMPLIANT:
            self.non_compliant_jobs.add(job_id)
        else:
            self.review_required_jobs.add(job_id)
        
        return status, warnings
    
    def can_fetch_from_source(self, source: JobSource) -> tuple[bool, int]:
        """
        Check if we can fetch from a source (rate limit check).
        
        Args:
            source: Job source
            
        Returns:
            (allowed, seconds_until_reset)
        """
        return self.compliance.check_rate_limit(source)
    
    def record_fetch(self, source: JobSource):
        """Record a fetch from a source."""
        self.compliance.record_request(source)
    
    def accept_source_tos(self, source: JobSource, accepted_by: str) -> bool:
        """Accept terms of service for a source."""
        return self.compliance.accept_tos(source, accepted_by)
    
    def get_compliance_summary(self) -> Dict:
        """Get a summary of compliance status."""
        return {
            "compliant_jobs": len(self.compliant_jobs),
            "non_compliant_jobs": len(self.non_compliant_jobs),
            "review_required_jobs": len(self.review_required_jobs),
            "total_jobs": len(self.compliant_jobs) + len(self.non_compliant_jobs) + len(self.review_required_jobs),
            "compliance_rate": len(self.compliant_jobs) / max(1, len(self.compliant_jobs) + len(self.non_compliant_jobs) + len(self.review_required_jobs)),
        }


# Singleton instance
_compliance_checker: Optional[JobDescriptionComplianceChecker] = None


def get_compliance_checker() -> JobDescriptionComplianceChecker:
    """Get the singleton compliance checker instance."""
    global _compliance_checker
    if _compliance_checker is None:
        _compliance_checker = JobDescriptionComplianceChecker()
    return _compliance_checker
