#!/usr/bin/env python3
"""
Job-Description Intelligence Engine - Mining professional judgment from labor market.

This module implements the core system for extracting professional patterns from job
descriptions to create a synthetic Developer Asset Underwriter.

Core concept: The missing professional is not one job title. It is a synthetic role
created from many overlapping professions: software due diligence, technical M&A,
IP commercialization, collateral underwriting, and developer-capital translation.

The job-description corpus becomes the raw material for the synthetic professional.
Output is not a resume - it is a competency graph.
"""

from enum import Enum
from typing import Dict, Any, List, Optional, Set
from dataclasses import dataclass, field
from datetime import datetime
import json
import re


class RoleFamily(Enum):
    """Role families that define the Developer Asset Underwriter."""
    SOFTWARE_DUE_DILIGENCE_ENGINEER = "software_due_diligence_engineer"
    TECHNICAL_MA_ANALYST = "technical_ma_analyst"
    STARTUP_CTO_ADVISOR = "startup_cto_advisor"
    VENTURE_STUDIO_TECHNICAL_LEAD = "venture_studio_technical_lead"
    SOFTWARE_ACQUISITION_ANALYST = "software_acquisition_analyst"
    OPEN_SOURCE_COMPLIANCE_SPECIALIST = "open_source_compliance_specialist"
    APPLICATION_SECURITY_AUDITOR = "application_security_auditor"
    DEVOPS_SRE_REVIEWER = "devops_sre_reviewer"
    TECHNICAL_PRODUCT_MANAGER = "technical_product_manager"
    IP_COMMERCIALIZATION_ANALYST = "ip_commercialization_analyst"
    TECHNOLOGY_TRANSFER_OFFICER = "technology_transfer_officer"
    PATENT_LICENSING_ANALYST = "patent_licensing_analyst"
    INNOVATION_SCOUT = "innovation_scout"
    MICRO_SAAS_ACQUISITION_ANALYST = "micro_saas_acquisition_analyst"
    REVENUE_BASED_FINANCE_UNDERWRITER = "revenue_based_finance_underwriter"
    ASSET_BASED_LENDING_ANALYST = "asset_based_lending_analyst"
    COLLATERAL_ANALYST = "collateral_analyst"
    AI_GOVERNANCE_ANALYST = "ai_governance_analyst"
    AI_AGENT_EVALUATOR = "ai_agent_evaluator"
    SOFTWARE_ASSET_MANAGER = "software_asset_manager"
    TECHNICAL_PROGRAM_MANAGER = "technical_program_manager"
    DEVELOPER_RELATIONS_LEAD = "developer_relations_lead"
    PLATFORM_ECOSYSTEM_ANALYST = "platform_ecosystem_analyst"


class CompetencyDomain(Enum):
    """High-level competency domains."""
    TECHNICAL_DILIGENCE = "technical_diligence"
    PRODUCTION_READINESS = "production_readiness"
    SECURITY_COMPLIANCE = "security_compliance"
    IP_OWNERSHIP = "ip_ownership"
    MARKET_FIT = "market_fit"
    COMMERCIALIZATION = "commercialization"
    COLLATERAL_SUPPORT = "collateral_support"
    LIQUIDATION_ROUTE = "liquidation_route"
    RISK_ASSESSMENT = "risk_assessment"
    DOCUMENTATION = "documentation"


@dataclass
class JobDescription:
    """A single job description from the labor market."""
    job_id: str
    role_family: RoleFamily
    title: str
    company: str
    description: str
    requirements: List[str]
    skills: List[str]
    tools: List[str]
    deliverables: List[str]
    source: str  # linkedin, indeed, company_careers, etc.
    url: Optional[str] = None
    salary_range: Optional[str] = None
    location: Optional[str] = None
    posted_date: Optional[datetime] = None
    extracted_at: datetime = field(default_factory=datetime.now)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "job_id": self.job_id,
            "role_family": self.role_family.value,
            "title": self.title,
            "company": self.company,
            "description": self.description,
            "requirements": self.requirements,
            "skills": self.skills,
            "tools": self.tools,
            "deliverables": self.deliverables,
            "source": self.source,
            "url": self.url,
            "salary_range": self.salary_range,
            "location": self.location,
            "posted_date": self.posted_date.isoformat() if self.posted_date else None,
            "extracted_at": self.extracted_at.isoformat(),
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'JobDescription':
        return cls(
            job_id=data["job_id"],
            role_family=RoleFamily(data["role_family"]),
            title=data["title"],
            company=data["company"],
            description=data["description"],
            requirements=data["requirements"],
            skills=data["skills"],
            tools=data["tools"],
            deliverables=data["deliverables"],
            source=data["source"],
            url=data.get("url"),
            salary_range=data.get("salary_range"),
            location=data.get("location"),
            posted_date=datetime.fromisoformat(data["posted_date"]) if data.get("posted_date") else None,
            extracted_at=datetime.fromisoformat(data["extracted_at"]),
        )


@dataclass
class Competency:
    """A professional competency extracted from job descriptions."""
    competency_id: str
    domain: CompetencyDomain
    name: str
    description: str
    signals: List[str]  # What this competency looks for
    evidence_types: List[str]  # What artifacts constitute evidence
    scoring_rules: List[str]  # How to evaluate this competency
    role_families: List[RoleFamily]  # Which roles use this competency
    frequency: int = 0  # How many job descriptions mention this
    confidence: float = 0.0  # Confidence in this competency

    def to_dict(self) -> Dict[str, Any]:
        return {
            "competency_id": self.competency_id,
            "domain": self.domain.value,
            "name": self.name,
            "description": self.description,
            "signals": self.signals,
            "evidence_types": self.evidence_types,
            "scoring_rules": self.scoring_rules,
            "role_families": [rf.value for rf in self.role_families],
            "frequency": self.frequency,
            "confidence": self.confidence,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Competency':
        return cls(
            competency_id=data["competency_id"],
            domain=CompetencyDomain(data["domain"]),
            name=data["name"],
            description=data["description"],
            signals=data["signals"],
            evidence_types=data["evidence_types"],
            scoring_rules=data["scoring_rules"],
            role_families=[RoleFamily(rf) for rf in data["role_families"]],
            frequency=data.get("frequency", 0),
            confidence=data.get("confidence", 0.0),
        )


@dataclass
class CompetencyGraph:
    """
    The competency graph: role → competency → signal → evidence → scoring → artifact.
    
    This graph is how the system gets the "feel" of a professional.
    It no longer says "AI thinks this is valuable."
    It says: "This asset was reviewed against a professional competency graph derived
    from technical diligence, software commercialization, compliance, and collateral
    underwriting roles."
    """
    graph_id: str
    name: str
    description: str
    competencies: Dict[str, Competency] = field(default_factory=dict)
    role_competency_map: Dict[RoleFamily, List[str]] = field(default_factory=dict)
    domain_competency_map: Dict[CompetencyDomain, List[str]] = field(default_factory=dict)
    version: str = "1.0"
    created_at: datetime = field(default_factory=datetime.now)
    last_updated: datetime = field(default_factory=datetime.now)

    def add_competency(self, competency: Competency) -> None:
        """Add a competency to the graph."""
        self.competencies[competency.competency_id] = competency
        
        # Update role map
        for role_family in competency.role_families:
            if role_family not in self.role_competency_map:
                self.role_competency_map[role_family] = []
            if competency.competency_id not in self.role_competency_map[role_family]:
                self.role_competency_map[role_family].append(competency.competency_id)
        
        # Update domain map
        if competency.domain not in self.domain_competency_map:
            self.domain_competency_map[competency.domain] = []
        if competency.competency_id not in self.domain_competency_map[competency.domain]:
            self.domain_competency_map[competency.domain].append(competency.competency_id)
        
        self.last_updated = datetime.now()

    def get_competencies_for_role(self, role_family: RoleFamily) -> List[Competency]:
        """Get all competencies for a specific role family."""
        competency_ids = self.role_competency_map.get(role_family, [])
        return [self.competencies[cid] for cid in competency_ids if cid in self.competencies]

    def get_competencies_for_domain(self, domain: CompetencyDomain) -> List[Competency]:
        """Get all competencies for a specific domain."""
        competency_ids = self.domain_competency_map.get(domain, [])
        return [self.competencies[cid] for cid in competency_ids if cid in self.competencies]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "graph_id": self.graph_id,
            "name": self.name,
            "description": self.description,
            "competencies": {cid: comp.to_dict() for cid, comp in self.competencies.items()},
            "role_competency_map": {rf.value: cids for rf, cids in self.role_competency_map.items()},
            "domain_competency_map": {domain.value: cids for domain, cids in self.domain_competency_map.items()},
            "version": self.version,
            "created_at": self.created_at.isoformat(),
            "last_updated": self.last_updated.isoformat(),
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'CompetencyGraph':
        graph = cls(
            graph_id=data["graph_id"],
            name=data["name"],
            description=data["description"],
            version=data.get("version", "1.0"),
            created_at=datetime.fromisoformat(data["created_at"]),
            last_updated=datetime.fromisoformat(data["last_updated"]),
        )
        
        # Rebuild competencies
        for cid, comp_data in data["competencies"].items():
            competency = Competency.from_dict(comp_data)
            graph.competencies[cid] = competency
        
        # Rebuild maps
        for rf_value, cids in data["role_competency_map"].items():
            graph.role_competency_map[RoleFamily(rf_value)] = cids
        
        for domain_value, cids in data["domain_competency_map"].items():
            graph.domain_competency_map[CompetencyDomain(domain_value)] = cids
        
        return graph


class JobDescriptionCorpus:
    """
    Repository of job descriptions used to build the competency graph.
    
    The first version uses job descriptions to build the evaluator.
    The better version uses outcomes from real transactions.
    
    Loop: job descriptions → professional judgment → evaluator scores → packets →
    outcomes → scoring improvement → better buyer matching → better underwriting.
    """

    def __init__(self):
        self.job_descriptions: Dict[str, JobDescription] = {}
        self.competency_graph: Optional[CompetencyGraph] = None
        self.extraction_stats: Dict[str, Any] = {
            "total_jobs": 0,
            "by_role_family": {},
            "by_source": {},
        }

    def add_job_description(self, job: JobDescription) -> None:
        """Add a job description to the corpus."""
        self.job_descriptions[job.job_id] = job
        self.extraction_stats["total_jobs"] += 1
        
        # Update role family stats
        rf = job.role_family.value
        if rf not in self.extraction_stats["by_role_family"]:
            self.extraction_stats["by_role_family"][rf] = 0
        self.extraction_stats["by_role_family"][rf] += 1
        
        # Update source stats
        source = job.source
        if source not in self.extraction_stats["by_source"]:
            self.extraction_stats["by_source"][source] = 0
        self.extraction_stats["by_source"][source] += 1

    def get_jobs_by_role_family(self, role_family: RoleFamily) -> List[JobDescription]:
        """Get all job descriptions for a specific role family."""
        return [
            job for job in self.job_descriptions.values()
            if job.role_family == role_family
        ]

    def extract_competencies(self) -> CompetencyGraph:
        """
        Extract competencies from the job description corpus.
        
        This is the core move: mining job descriptions into professional judgment.
        """
        if not self.job_descriptions:
            raise ValueError("No job descriptions in corpus")
        
        graph = CompetencyGraph(
            graph_id="developer_asset_underwriter_v1",
            name="Developer Asset Underwriter Competency Graph",
            description="Professional competencies derived from 22 role families at the developer-capital translation layer",
        )
        
        # Extract competencies by role family
        for role_family in RoleFamily:
            jobs = self.get_jobs_by_role_family(role_family)
            if not jobs:
                continue
            
            # Aggregate signals from all jobs in this role family
            all_skills = []
            all_tools = []
            all_deliverables = []
            all_requirements = []
            
            for job in jobs:
                all_skills.extend(job.skills)
                all_tools.extend(job.tools)
                all_deliverables.extend(job.deliverables)
                all_requirements.extend(job.requirements)
            
            # Count frequencies
            skill_freq = self._count_frequencies(all_skills)
            tool_freq = self._count_frequencies(all_tools)
            deliverable_freq = self._count_frequencies(all_deliverables)
            requirement_freq = self._count_frequencies(all_requirements)
            
            # Create competencies based on high-frequency items
            self._create_competencies_from_frequencies(
                graph,
                role_family,
                skill_freq,
                tool_freq,
                deliverable_freq,
                requirement_freq,
            )
        
        self.competency_graph = graph
        return graph

    def _count_frequencies(self, items: List[str]) -> Dict[str, int]:
        """Count frequency of items in a list."""
        freq = {}
        for item in items:
            item_lower = item.lower().strip()
            if item_lower:
                freq[item_lower] = freq.get(item_lower, 0) + 1
        return freq

    def _create_competencies_from_frequencies(
        self,
        graph: CompetencyGraph,
        role_family: RoleFamily,
        skill_freq: Dict[str, int],
        tool_freq: Dict[str, int],
        deliverable_freq: Dict[str, int],
        requirement_freq: Dict[str, int],
    ) -> None:
        """Create competencies from frequency analysis."""
        # This is a simplified version - in production, use NLP/ML
        # to extract more sophisticated competencies
        
        # Map role families to domains
        domain_mapping = {
            RoleFamily.SOFTWARE_DUE_DILIGENCE_ENGINEER: CompetencyDomain.TECHNICAL_DILIGENCE,
            RoleFamily.APPLICATION_SECURITY_AUDITOR: CompetencyDomain.SECURITY_COMPLIANCE,
            RoleFamily.IP_COMMERCIALIZATION_ANALYST: CompetencyDomain.COMMERCIALIZATION,
            RoleFamily.COLLATERAL_ANALYST: CompetencyDomain.COLLATERAL_SUPPORT,
            RoleFamily.DEVOPS_SRE_REVIEWER: CompetencyDomain.PRODUCTION_READINESS,
            RoleFamily.OPEN_SOURCE_COMPLIANCE_SPECIALIST: CompetencyDomain.IP_OWNERSHIP,
            RoleFamily.TECHNICAL_MA_ANALYST: CompetencyDomain.MARKET_FIT,
            RoleFamily.AI_AGENT_EVALUATOR: CompetencyDomain.RISK_ASSESSMENT,
        }
        
        domain = domain_mapping.get(role_family, CompetencyDomain.TECHNICAL_DILIGENCE)
        
        # Create competency from top skills
        top_skills = sorted(skill_freq.items(), key=lambda x: x[1], reverse=True)[:5]
        if top_skills:
            competency_id = f"{role_family.value}_competency"
            competency = Competency(
                competency_id=competency_id,
                domain=domain,
                name=f"{role_family.value.replace('_', ' ').title()} Competency",
                description=f"Core competency for {role_family.value.replace('_', ' ')}",
                signals=[skill for skill, _ in top_skills],
                evidence_types=[tool for tool, _ in sorted(tool_freq.items(), key=lambda x: x[1], reverse=True)[:3]],
                scoring_rules=[
                    f"Evaluate presence of {skill}" for skill, _ in top_skills[:3]
                ],
                role_families=[role_family],
                frequency=sum(count for _, count in top_skills),
                confidence=min(1.0, len(top_skills) / 5),
            )
            graph.add_competency(competency)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "job_descriptions": {jid: job.to_dict() for jid, job in self.job_descriptions.items()},
            "competency_graph": self.competency_graph.to_dict() if self.competency_graph else None,
            "extraction_stats": self.extraction_stats,
        }

    def save_to_file(self, filepath: str) -> None:
        """Save corpus to file."""
        with open(filepath, 'w') as f:
            json.dump(self.to_dict(), f, indent=2)

    @classmethod
    def load_from_file(cls, filepath: str) -> 'JobDescriptionCorpus':
        """Load corpus from file."""
        with open(filepath, 'r') as f:
            data = json.load(f)
        
        corpus = cls()
        
        # Rebuild job descriptions
        for jid, job_data in data["job_descriptions"].items():
            job = JobDescription.from_dict(job_data)
            corpus.job_descriptions[jid] = job
        
        # Rebuild competency graph
        if data.get("competency_graph"):
            corpus.competency_graph = CompetencyGraph.from_dict(data["competency_graph"])
        
        corpus.extraction_stats = data.get("extraction_stats", {})
        
        return corpus


# Seed data: Initial competency definitions based on the 22 role families
# This provides a starting point before mining real job descriptions
SEED_COMPETENCIES = {
    "software_due_diligence": Competency(
        competency_id="software_due_diligence",
        domain=CompetencyDomain.TECHNICAL_DILIGENCE,
        name="Software Due Diligence",
        description="Evaluate software architecture, scalability, maintainability, technical debt, documentation, and security",
        signals=[
            "architecture review",
            "scalability assessment",
            "maintainability analysis",
            "technical debt evaluation",
            "documentation quality",
            "security posture",
        ],
        evidence_types=[
            "package files",
            "test logs",
            "GitHub Actions",
            "Dockerfile",
            "architecture diagrams",
            "README",
        ],
        scoring_rules=[
            "Score production readiness based on CI/CD presence",
            "Evaluate test coverage and quality",
            "Assess documentation completeness",
            "Review dependency management",
        ],
        role_families=[RoleFamily.SOFTWARE_DUE_DILIGENCE_ENGINEER],
        frequency=100,
        confidence=0.9,
    ),
    
    "ip_commercialization": Competency(
        competency_id="ip_commercialization",
        domain=CompetencyDomain.COMMERCIALIZATION,
        name="IP Commercialization",
        description="Evaluate licensing potential, buyer category, market use case, and monetization pathways",
        signals=[
            "licensing potential",
            "buyer category",
            "market use case",
            "monetization pathway",
            "IP clarity",
        ],
        evidence_types=[
            "README",
            "product summary",
            "endpoint documentation",
            "demo",
            "buyer list",
            "license file",
        ],
        scoring_rules=[
            "Score marketability based on buyer relevance",
            "Evaluate licensing clarity",
            "Assess product readiness",
            "Review competitive positioning",
        ],
        role_families=[RoleFamily.IP_COMMERCIALIZATION_ANALYST, RoleFamily.TECHNOLOGY_TRANSFER_OFFICER],
        frequency=85,
        confidence=0.85,
    ),
    
    "collateral_support": Competency(
        competency_id="collateral_support",
        domain=CompetencyDomain.COLLATERAL_SUPPORT,
        name="Collateral Support",
        description="Evaluate recoverability, ownership clarity, monitoring plan, and collateral support range",
        signals=[
            "liquidation route",
            "ownership clarity",
            "monitoring plan",
            "collateral coverage",
            "recoverability",
        ],
        evidence_types=[
            "ownership statement",
            "buyer universe",
            "packet manifest",
            "monitoring plan",
            "liquidation route",
        ],
        scoring_rules=[
            "Score collateral support based on recoverability",
            "Evaluate ownership clarity",
            "Assess monitoring feasibility",
            "Review liquidation timeline",
        ],
        role_families=[RoleFamily.COLLATERAL_ANALYST, RoleFamily.ASSET_BASED_LENDING_ANALYST],
        frequency=90,
        confidence=0.88,
    ),
    
    "production_readiness": Competency(
        competency_id="production_readiness",
        domain=CompetencyDomain.PRODUCTION_READINESS,
        name="Production Readiness",
        description="Evaluate whether software is production-grade, deployable, and maintainable",
        signals=[
            "CI/CD pipeline",
            "testing infrastructure",
            "deployment automation",
            "monitoring setup",
            "error handling",
        ],
        evidence_types=[
            "GitHub Actions",
            "Dockerfile",
            "test suite",
            "deployment logs",
            "monitoring dashboards",
        ],
        scoring_rules=[
            "Score based on CI/CD presence",
            "Evaluate test coverage",
            "Assess deployment automation",
            "Review monitoring setup",
        ],
        role_families=[RoleFamily.DEVOPS_SRE_REVIEWER, RoleFamily.STARTUP_CTO_ADVISOR],
        frequency=95,
        confidence=0.92,
    ),
    
    "security_compliance": Competency(
        competency_id="security_compliance",
        domain=CompetencyDomain.SECURITY_COMPLIANCE,
        name="Security and Compliance",
        description="Evaluate security posture, vulnerability exposure, and compliance status",
        signals=[
            "secret management",
            "vulnerability scanning",
            "dependency security",
            "access controls",
            "compliance standards",
        ],
        evidence_types=[
            "secret scan report",
            "dependency audit",
            "security headers",
            "access logs",
            "compliance documentation",
        ],
        scoring_rules=[
            "Score based on secret scan results",
            "Evaluate dependency vulnerabilities",
            "Assess access controls",
            "Review compliance documentation",
        ],
        role_families=[RoleFamily.APPLICATION_SECURITY_AUDITOR, RoleFamily.OPEN_SOURCE_COMPLIANCE_SPECIALIST],
        frequency=88,
        confidence=0.9,
    ),
}


def create_seed_competency_graph() -> CompetencyGraph:
    """Create a competency graph from seed data."""
    graph = CompetencyGraph(
        graph_id="developer_asset_underwriter_seed_v1",
        name="Developer Asset Underwriter Seed Competency Graph",
        description="Initial competency graph based on professional judgment of 22 role families",
    )
    
    for competency in SEED_COMPETENCIES.values():
        graph.add_competency(competency)
    
    return graph
