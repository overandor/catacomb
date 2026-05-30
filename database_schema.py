#!/usr/bin/env python3
"""
Database Schema for Catacomb - Innovation Allocation and Asset Underwriting Engine.

This module defines the SQLAlchemy models for persistent storage of:
- Assets and evaluations
- Professional review cards
- Audit logs
- Job descriptions and competency graph
- Users and authentication
"""

from sqlalchemy import Column, String, Integer, Float, Boolean, DateTime, Text, JSON, ForeignKey, Enum as SQLEnum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime
import enum

Base = declarative_base()


class UserRole(enum.Enum):
    """User roles for three-tier product model."""
    PUBLIC = "public"
    PROFESSIONAL = "professional"
    ADMIN = "admin"


class AssetClassification(enum.Enum):
    """Asset classification types."""
    REAL_PRODUCTION_SYSTEM = "real_production_system"
    WORKING_PROTOTYPE = "working_prototype"
    RESEARCH_PROTOTYPE = "research_prototype"
    INTERNAL_TOOL = "internal_tool"
    API_SERVICE = "api_service"
    FRONTEND_PRODUCT = "frontend_product"
    BACKEND_SERVICE = "backend_service"
    SMART_CONTRACT_PROTOCOL = "smart_contract_protocol"
    TRADING_ENGINE = "trading_engine"
    DATA_PIPELINE = "data_pipeline"
    HUGGING_FACE_SPACE = "hugging_face_space"
    PROMPT_SYSTEM = "prompt_system"
    AGENT_WORKFLOW = "agent_workflow"
    DOCUMENTATION_PACKAGE = "documentation_package"
    VALUATION_LEDGER = "valuation_ledger"
    PROOF_LEDGER = "proof_ledger"
    SALES_OUTREACH_TOOL = "sales_outreach_tool"
    FORK_TEMPLATE = "fork_template"
    SCAFFOLD = "scaffold"
    DUPLICATE = "duplicate"
    JUNK = "junk"
    RISK_BLOCKED = "risk_blocked"


class User(Base):
    """User accounts for authentication and role-based access."""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    role = Column(SQLEnum(UserRole), default=UserRole.PUBLIC, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    
    # Relationships
    assets = relationship("Asset", back_populates="owner")
    evaluations = relationship("Evaluation", back_populates="user")


class Asset(Base):
    """Software assets for evaluation and underwriting."""
    __tablename__ = "assets"
    
    id = Column(Integer, primary_key=True, index=True)
    asset_id = Column(String(255), unique=True, nullable=False, index=True)
    asset_name = Column(String(255), nullable=False)
    classification = Column(SQLEnum(AssetClassification), nullable=False)
    
    # Technical metadata
    primary_language = Column(String(50))
    file_count = Column(Integer, default=0)
    has_tests = Column(Boolean, default=False)
    has_ci_cd = Column(Boolean, default=False)
    has_documentation = Column(Boolean, default=False)
    code_quality_score = Column(Float, default=0.0)
    build_status = Column(String(50))
    test_status = Column(String(50))
    deployment_status = Column(String(50))
    
    # Ownership and license
    has_license = Column(Boolean, default=False)
    license_type = Column(String(100))
    is_fork = Column(Boolean, default=False)
    ownership_clarity = Column(String(50))
    
    # Links
    repo_url = Column(String(500))
    deployment_url = Column(String(500))
    
    # Additional metadata as JSON
    metadata = Column(JSON, default={})
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Foreign keys
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    
    # Relationships
    owner = relationship("User", back_populates="assets")
    evaluations = relationship("Evaluation", back_populates="asset", cascade="all, delete-orphan")
    review_cards = relationship("ReviewCard", back_populates="asset", cascade="all, delete-orphan")


class Evaluation(Base):
    """Professional evaluation results for assets."""
    __tablename__ = "evaluations"
    
    id = Column(Integer, primary_key=True, index=True)
    evaluation_id = Column(String(255), unique=True, nullable=False, index=True)
    
    # Grades
    production_grade = Column(String(5))
    commercial_grade = Column(String(5))
    collateral_grade = Column(String(5))
    financeability_score = Column(Integer, default=0)
    proof_level = Column(Integer, default=0)
    
    # Strategic classification
    strategic_value = Column(String(50))
    buyer_today_value = Column(String(50))
    collateral_support = Column(String(50))
    
    # Committee results
    committee_results = Column(JSON, default={})
    
    # Capital translation
    capital_translation = Column(JSON, default={})
    
    # Liquidification plan
    liquidification_plan = Column(JSON, default={})
    
    # Next action
    next_action = Column(JSON, default={})
    
    # Evidence
    evidence = Column(JSON, default={})
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    # Foreign keys
    asset_id = Column(Integer, ForeignKey("assets.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    
    # Relationships
    asset = relationship("Asset", back_populates="evaluations")
    user = relationship("User", back_populates="evaluations")
    audit_entries = relationship("AuditEntry", back_populates="evaluation", cascade="all, delete-orphan")


class ReviewCard(Base):
    """Professional review cards for assets."""
    __tablename__ = "review_cards"
    
    id = Column(Integer, primary_key=True, index=True)
    card_id = Column(String(255), unique=True, nullable=False, index=True)
    
    # Card content
    classification = Column(String(255))
    production_grade = Column(String(5))
    commercial_grade = Column(String(5))
    collateral_grade = Column(String(5))
    financeability_score = Column(Integer, default=0)
    proof_level = Column(Integer, default=0)
    strategic_value = Column(String(50))
    buyer_today_value = Column(String(50))
    collateral_support = Column(String(50))
    
    # Blockers and action
    main_blockers = Column(JSON, default=[])
    best_next_action = Column(String(500))
    likely_route = Column(JSON, default=[])
    packet_readiness = Column(Text)
    
    # Disclaimers and evidence
    disclaimers = Column(JSON, default=[])
    evidence_links = Column(JSON, default={})
    
    # Card format
    format_type = Column(String(20), default="text")  # text, markdown, json
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    # Foreign keys
    asset_id = Column(Integer, ForeignKey("assets.id"), nullable=False)
    
    # Relationships
    asset = relationship("Asset", back_populates="review_cards")


class AuditEntry(Base):
    """Audit log entries for decision tracking."""
    __tablename__ = "audit_entries"
    
    id = Column(Integer, primary_key=True, index=True)
    entry_id = Column(String(255), unique=True, nullable=False, index=True)
    
    # Decision details
    evaluator_name = Column(String(255), nullable=False)
    decision_type = Column(String(100), nullable=False)
    decision_value = Column(JSON, nullable=False)
    evidence = Column(JSON, default={})
    reasoning = Column(Text, nullable=False)
    confidence = Column(Float, default=1.0)
    
    # Integrity
    entry_hash = Column(String(64), nullable=False)  # SHA-256 hash
    
    # Metadata
    metadata = Column(JSON, default={})
    
    # Timestamps
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    # Foreign keys
    evaluation_id = Column(Integer, ForeignKey("evaluations.id"), nullable=True)
    
    # Relationships
    evaluation = relationship("Evaluation", back_populates="audit_entries")


class JobDescription(Base):
    """Job descriptions for competency graph mining."""
    __tablename__ = "job_descriptions"
    
    id = Column(Integer, primary_key=True, index=True)
    job_id = Column(String(255), unique=True, nullable=False, index=True)
    
    # Job details
    role_family = Column(String(255), nullable=False, index=True)
    title = Column(String(255))
    company = Column(String(255))
    description = Column(Text)
    requirements = Column(JSON, default=[])
    skills = Column(JSON, default=[])
    tools = Column(JSON, default=[])
    deliverables = Column(JSON, default=[])
    
    # Source
    source = Column(String(100), nullable=False)
    url = Column(String(500))
    salary_range = Column(String(100))
    location = Column(String(255))
    posted_date = Column(DateTime)
    
    # Metadata
    extracted_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    # Competency extraction
    extracted_competencies = Column(JSON, default=[])


class Competency(Base):
    """Competencies extracted from job descriptions."""
    __tablename__ = "competencies"
    
    id = Column(Integer, primary_key=True, index=True)
    competency_id = Column(String(255), unique=True, nullable=False, index=True)
    
    # Competency details
    name = Column(String(255), nullable=False)
    description = Column(Text)
    domain = Column(String(100), nullable=False, index=True)
    
    # Signals and evidence
    signals = Column(JSON, default=[])
    evidence_types = Column(JSON, default=[])
    scoring_rules = Column(JSON, default={})
    artifacts = Column(JSON, default=[])
    
    # Role mapping
    role_families = Column(JSON, default=[])
    
    # Metadata
    version = Column(String(20), default="1.0")
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)


class CompetencyGraph(Base):
    """Competency graph versions."""
    __tablename__ = "competency_graphs"
    
    id = Column(Integer, primary_key=True, index=True)
    graph_id = Column(String(255), unique=True, nullable=False, index=True)
    
    # Graph details
    name = Column(String(255), nullable=False)
    description = Column(Text)
    
    # Graph structure
    competencies = Column(JSON, default={})  # competency_id -> competency data
    role_competency_map = Column(JSON, default={})  # role_family -> competency_ids
    domain_competency_map = Column(JSON, default={})  # domain -> competency_ids
    
    # Metadata
    version = Column(String(20), default="1.0")
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    last_updated = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Active flag
    is_active = Column(Boolean, default=True, nullable=False)


class Outcome(Base):
    """Verified intervention outcomes for transformation law extraction."""
    __tablename__ = "outcomes"
    
    id = Column(Integer, primary_key=True, index=True)
    outcome_id = Column(String(255), unique=True, nullable=False, index=True)
    
    # Outcome details
    intervention_type = Column(String(255), nullable=False)
    asset_id = Column(String(255), nullable=False)
    
    # Results
    pre_intervention_value = Column(Float)
    post_intervention_value = Column(Float)
    value_delta = Column(Float)
    value_delta_percent = Column(Float)
    
    # Verification
    is_verified = Column(Boolean, default=False)
    verified_by = Column(String(255))
    verified_at = Column(DateTime)
    
    # Metadata
    outcome_date = Column(DateTime, default=datetime.utcnow, nullable=False)
    notes = Column(Text)
