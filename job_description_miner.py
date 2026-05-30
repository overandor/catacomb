#!/usr/bin/env python3
"""
Job Description Mining - Collecting professional judgment from labor market.

This module handles the collection and management of job descriptions from permitted
sources to build the competency graph for the Developer Asset Underwriter.

The job corpus becomes a moat:
- First version: job descriptions define professional judgment
- Better version: outcomes from real transactions
- Loop: job descriptions → evaluator → packets → outcomes → scoring improvement
"""

from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
import json
import re


class JobSource(Enum):
    """Permitted sources for job descriptions."""
    LINKEDIN = "linkedin"
    INDEED = "indeed"
    GLASSDOOR = "glassdoor"
    COMPANY_CAREERS = "company_careers"
    ANGEL_LIST = "angel_list"
    WELLFOUND = "wellfound"
    REMOTE_CO = "remote_co"
    WE_WORK_REMOTELY = "we_work_remotely"


@dataclass
class MiningConfig:
    """Configuration for job description mining."""
    sources: List[JobSource] = field(default_factory=lambda: [JobSource.LINKEDIN, JobSource.INDEED])
    role_families: List[str] = field(default_factory=list)
    max_jobs_per_role: int = 100
    max_total_jobs: int = 1000
    require_salary: bool = False
    require_remote: bool = False
    location_filter: Optional[str] = None
    date_range_days: int = 30


class JobDescriptionMiner:
    """
    Job Description Miner - Collects job descriptions from permitted sources.
    
    This is the data collection layer for the Job-Description Intelligence Engine.
    """
    
    def __init__(self, config: Optional[MiningConfig] = None):
        self.config = config or MiningConfig()
        self.mining_stats = {
            "total_attempted": 0,
            "total_collected": 0,
            "by_source": {},
            "by_role_family": {},
            "errors": [],
        }
    
    def mine_job_descriptions(
        self,
        role_families: Optional[List[str]] = None,
    ) -> List[Dict[str, Any]]:
        """
        Mine job descriptions from configured sources.
        
        Args:
            role_families: Specific role families to mine (optional)
        
        Returns:
            List of job description dictionaries
        """
        if role_families:
            target_roles = role_families
        else:
            target_roles = self.config.role_families
        
        if not target_roles:
            # Default to all role families
            from job_description_intelligence import RoleFamily
            target_roles = [rf.value for rf in RoleFamily]
        
        all_jobs = []
        
        for role_family in target_roles:
            jobs = self._mine_for_role_family(role_family)
            all_jobs.extend(jobs)
            
            # Stop if we've reached max total
            if len(all_jobs) >= self.config.max_total_jobs:
                break
        
        self.mining_stats["total_attempted"] = len(target_roles) * self.config.max_jobs_per_role
        self.mining_stats["total_collected"] = len(all_jobs)
        
        return all_jobs
    
    def _mine_for_role_family(self, role_family: str) -> List[Dict[str, Any]]:
        """Mine job descriptions for a specific role family."""
        jobs = []
        
        for source in self.config.sources:
            try:
                source_jobs = self._mine_from_source(source, role_family)
                jobs.extend(source_jobs)
                
                # Update stats
                if source.value not in self.mining_stats["by_source"]:
                    self.mining_stats["by_source"][source.value] = 0
                self.mining_stats["by_source"][source.value] += len(source_jobs)
                
                # Stop if we've reached max for this role
                if len(jobs) >= self.config.max_jobs_per_role:
                    break
                    
            except Exception as e:
                self.mining_stats["errors"].append({
                    "source": source.value,
                    "role_family": role_family,
                    "error": str(e),
                    "timestamp": datetime.now().isoformat(),
                })
        
        # Update role family stats
        if role_family not in self.mining_stats["by_role_family"]:
            self.mining_stats["by_role_family"][role_family] = 0
        self.mining_stats["by_role_family"][role_family] += len(jobs)
        
        return jobs[:self.config.max_jobs_per_role]
    
    def _mine_from_source(self, source: JobSource, role_family: str) -> List[Dict[str, Any]]:
        """
        Mine job descriptions from a specific source.
        
        This is a placeholder implementation. In production, this would integrate
        with actual APIs or web scraping for each source.
        """
        # Placeholder: Return sample job descriptions
        # In production, implement actual API calls or scraping
        
        sample_jobs = self._generate_sample_jobs(source, role_family)
        return sample_jobs
    
    def _generate_sample_jobs(self, source: JobSource, role_family: str) -> List[Dict[str, Any]]:
        """Generate sample job descriptions for testing."""
        # This is a placeholder for demonstration
        # In production, this would be replaced with actual data collection
        
        sample_count = min(5, self.config.max_jobs_per_role)
        sample_jobs = []
        
        for i in range(sample_count):
            job = {
                "job_id": f"{source.value}_{role_family}_{i}",
                "role_family": role_family,
                "title": f"{role_family.replace('_', ' ').title()}",
                "company": f"Company {i+1}",
                "description": self._generate_sample_description(role_family),
                "requirements": self._generate_sample_requirements(role_family),
                "skills": self._generate_sample_skills(role_family),
                "tools": self._generate_sample_tools(role_family),
                "deliverables": self._generate_sample_deliverables(role_family),
                "source": source.value,
                "url": f"https://example.com/jobs/{i}",
                "salary_range": "$100k - $150k",
                "location": "Remote",
                "posted_date": datetime.now().isoformat(),
                "extracted_at": datetime.now().isoformat(),
            }
            sample_jobs.append(job)
        
        return sample_jobs
    
    def _generate_sample_description(self, role_family: str) -> str:
        """Generate sample job description."""
        descriptions = {
            "software_due_diligence_engineer": "We are seeking a Software Due Diligence Engineer to evaluate software architecture, scalability, maintainability, and technical debt for potential acquisitions.",
            "technical_ma_analyst": "Join our team as a Technical M&A Analyst to assess technology assets, evaluate code quality, and provide technical recommendations for acquisitions.",
            "ip_commercialization_analyst": "We need an IP Commercialization Analyst to identify licensing opportunities, evaluate market fit, and develop monetization strategies for intellectual property.",
            "collateral_analyst": "Seeking a Collateral Analyst to evaluate asset recoverability, assess collateral coverage, and develop monitoring plans for software-based lending.",
        }
        return descriptions.get(role_family, "We are seeking a qualified professional to join our team.")
    
    def _generate_sample_requirements(self, role_family: str) -> List[str]:
        """Generate sample job requirements."""
        return [
            "5+ years of relevant experience",
            "Strong technical background",
            "Excellent communication skills",
            "Experience with due diligence processes",
            "Ability to work cross-functionally",
        ]
    
    def _generate_sample_skills(self, role_family: str) -> List[str]:
        """Generate sample job skills."""
        skills_map = {
            "software_due_diligence_engineer": ["Software Architecture", "Code Review", "Technical Assessment", "Risk Analysis"],
            "technical_ma_analyst": ["Due Diligence", "Financial Analysis", "Technical Evaluation", "Market Research"],
            "ip_commercialization_analyst": ["IP Law", "Licensing", "Market Analysis", "Business Development"],
            "collateral_analyst": ["Risk Assessment", "Asset Valuation", "Financial Analysis", "Monitoring"],
        }
        return skills_map.get(role_family, ["Analysis", "Communication", "Technical Skills"])
    
    def _generate_sample_tools(self, role_family: str) -> List[str]:
        """Generate sample job tools."""
        return ["GitHub", "GitLab", "JIRA", "Confluence", "Excel"]
    
    def _generate_sample_deliverables(self, role_family: str) -> List[str]:
        """Generate sample job deliverables."""
        return [
            "Technical assessment reports",
            "Due diligence memos",
            "Risk analysis documents",
            "Strategic recommendations",
        ]
    
    def get_mining_stats(self) -> Dict[str, Any]:
        """Get mining statistics."""
        return self.mining_stats
    
    def export_mining_report(self) -> str:
        """Export a mining report as text."""
        lines = [
            "Job Description Mining Report",
            "=" * 50,
            "",
            f"Total Attempted: {self.mining_stats['total_attempted']}",
            f"Total Collected: {self.mining_stats['total_collected']}",
            f"Success Rate: {self.mining_stats['total_collected'] / self.mining_stats['total_attempted'] * 100 if self.mining_stats['total_attempted'] > 0 else 0:.1f}%",
            "",
            "By Source:",
        ]
        
        for source, count in self.mining_stats["by_source"].items():
            lines.append(f"  {source}: {count}")
        
        lines.extend([
            "",
            "By Role Family:",
        ])
        
        for role, count in self.mining_stats["by_role_family"].items():
            lines.append(f"  {role}: {count}")
        
        if self.mining_stats["errors"]:
            lines.extend([
                "",
                f"Errors: {len(self.mining_stats['errors'])}",
            ])
            for error in self.mining_stats["errors"][:5]:
                lines.append(f"  - {error['source']}/{error['role_family']}: {error['error']}")
        
        return "\n".join(lines)


class JobCorpusManager:
    """
    Job Corpus Manager - Manages the job description corpus.
    
    Handles storage, retrieval, and updates to the job description corpus.
    """
    
    def __init__(self, corpus_path: Optional[str] = None):
        self.corpus_path = corpus_path or "job_corpus.json"
        self.corpus = self._load_corpus()
    
    def _load_corpus(self) -> Dict[str, Any]:
        """Load corpus from file."""
        try:
            with open(self.corpus_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {
                "jobs": [],
                "metadata": {
                    "version": "1.0",
                    "created_at": datetime.now().isoformat(),
                    "last_updated": datetime.now().isoformat(),
                },
            }
    
    def add_jobs(self, jobs: List[Dict[str, Any]]) -> int:
        """Add jobs to the corpus."""
        existing_job_ids = {job["job_id"] for job in self.corpus["jobs"]}
        
        added_count = 0
        for job in jobs:
            if job["job_id"] not in existing_job_ids:
                self.corpus["jobs"].append(job)
                added_count += 1
        
        self.corpus["metadata"]["last_updated"] = datetime.now().isoformat()
        self._save_corpus()
        
        return added_count
    
    def get_jobs_by_role_family(self, role_family: str) -> List[Dict[str, Any]]:
        """Get all jobs for a specific role family."""
        return [job for job in self.corpus["jobs"] if job["role_family"] == role_family]
    
    def get_jobs_by_source(self, source: str) -> List[Dict[str, Any]]:
        """Get all jobs from a specific source."""
        return [job for job in self.corpus["jobs"] if job["source"] == source]
    
    def get_corpus_stats(self) -> Dict[str, Any]:
        """Get corpus statistics."""
        jobs = self.corpus["jobs"]
        
        by_role = {}
        by_source = {}
        
        for job in jobs:
            role = job["role_family"]
            source = job["source"]
            
            if role not in by_role:
                by_role[role] = 0
            by_role[role] += 1
            
            if source not in by_source:
                by_source[source] = 0
            by_source[source] += 1
        
        return {
            "total_jobs": len(jobs),
            "by_role_family": by_role,
            "by_source": by_source,
            "metadata": self.corpus["metadata"],
        }
    
    def _save_corpus(self) -> None:
        """Save corpus to file."""
        with open(self.corpus_path, 'w') as f:
            json.dump(self.corpus, f, indent=2)
    
    def export_for_competency_extraction(self) -> List[Dict[str, Any]]:
        """Export corpus in format suitable for competency extraction."""
        return self.corpus["jobs"]
