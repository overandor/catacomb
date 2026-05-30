#!/usr/bin/env python3
"""
Database Manager for Catacomb - PostgreSQL connection and operations.

This module provides database connection management and CRUD operations
for all Catacomb data models.
"""

import os
from typing import Optional, List, Dict, Any
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import QueuePool
from contextlib import contextmanager
import logging

from database_schema import (
    Base,
    User,
    Asset,
    Evaluation,
    ReviewCard,
    AuditEntry,
    JobDescription,
    Competency,
    CompetencyGraph,
    Outcome,
    UserRole,
    AssetClassification,
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DatabaseManager:
    """
    Database manager for Catacomb.
    
    Handles PostgreSQL connections, session management, and CRUD operations.
    """
    
    def __init__(self, database_url: Optional[str] = None):
        """
        Initialize the database manager.
        
        Args:
            database_url: PostgreSQL connection URL. If not provided, uses DATABASE_URL env var.
        """
        self.database_url = database_url or os.getenv("DATABASE_URL")
        
        if not self.database_url:
            raise ValueError(
                "DATABASE_URL environment variable not set. "
                "Please set DATABASE_URL to your PostgreSQL connection string."
            )
        
        # Create engine with connection pooling
        self.engine = create_engine(
            self.database_url,
            poolclass=QueuePool,
            pool_size=10,
            max_overflow=20,
            pool_pre_ping=True,  # Verify connections before using
            echo=False,  # Set to True for SQL query logging
        )
        
        # Create session factory
        self.SessionLocal = sessionmaker(
            autocommit=False,
            autoflush=False,
            bind=self.engine,
        )
        
        logger.info("Database manager initialized")
    
    def create_tables(self) -> None:
        """Create all tables in the database."""
        Base.metadata.create_all(bind=self.engine)
        logger.info("All tables created successfully")
    
    def drop_tables(self) -> None:
        """Drop all tables from the database. Use with caution!"""
        Base.metadata.drop_all(bind=self.engine)
        logger.warning("All tables dropped")
    
    @contextmanager
    def get_session(self) -> Session:
        """
        Context manager for database sessions.
        
        Yields:
            Session: SQLAlchemy session
        """
        session = self.SessionLocal()
        try:
            yield session
            session.commit()
        except Exception as e:
            session.rollback()
            logger.error(f"Database error: {e}")
            raise
        finally:
            session.close()
    
    # User operations
    def create_user(
        self,
        email: str,
        password_hash: str,
        role: UserRole = UserRole.PUBLIC,
    ) -> User:
        """Create a new user."""
        with self.get_session() as session:
            user = User(
                email=email,
                password_hash=password_hash,
                role=role,
            )
            session.add(user)
            session.flush()
            session.refresh(user)
            return user
    
    def get_user_by_email(self, email: str) -> Optional[User]:
        """Get a user by email."""
        with self.get_session() as session:
            return session.query(User).filter(User.email == email).first()
    
    def get_user_by_id(self, user_id: int) -> Optional[User]:
        """Get a user by ID."""
        with self.get_session() as session:
            return session.query(User).filter(User.id == user_id).first()
    
    # Asset operations
    def create_asset(
        self,
        asset_id: str,
        asset_name: str,
        classification: AssetClassification,
        owner_id: Optional[int] = None,
        **kwargs,
    ) -> Asset:
        """Create a new asset."""
        with self.get_session() as session:
            asset = Asset(
                asset_id=asset_id,
                asset_name=asset_name,
                classification=classification,
                owner_id=owner_id,
                **kwargs,
            )
            session.add(asset)
            session.flush()
            session.refresh(asset)
            return asset
    
    def get_asset_by_id(self, asset_id: str) -> Optional[Asset]:
        """Get an asset by asset_id."""
        with self.get_session() as session:
            return session.query(Asset).filter(Asset.asset_id == asset_id).first()
    
    def get_assets_by_owner(self, owner_id: int) -> List[Asset]:
        """Get all assets for a specific owner."""
        with self.get_session() as session:
            return session.query(Asset).filter(Asset.owner_id == owner_id).all()
    
    def update_asset(self, asset_id: str, **kwargs) -> Optional[Asset]:
        """Update an asset."""
        with self.get_session() as session:
            asset = session.query(Asset).filter(Asset.asset_id == asset_id).first()
            if asset:
                for key, value in kwargs.items():
                    setattr(asset, key, value)
                session.flush()
                session.refresh(asset)
            return asset
    
    # Evaluation operations
    def create_evaluation(
        self,
        evaluation_id: str,
        asset_id: int,
        user_id: Optional[int] = None,
        **kwargs,
    ) -> Evaluation:
        """Create a new evaluation."""
        with self.get_session() as session:
            evaluation = Evaluation(
                evaluation_id=evaluation_id,
                asset_id=asset_id,
                user_id=user_id,
                **kwargs,
            )
            session.add(evaluation)
            session.flush()
            session.refresh(evaluation)
            return evaluation
    
    def get_evaluation_by_id(self, evaluation_id: str) -> Optional[Evaluation]:
        """Get an evaluation by ID."""
        with self.get_session() as session:
            return session.query(Evaluation).filter(Evaluation.evaluation_id == evaluation_id).first()
    
    def get_evaluations_by_asset(self, asset_id: int) -> List[Evaluation]:
        """Get all evaluations for an asset."""
        with self.get_session() as session:
            return session.query(Evaluation).filter(Evaluation.asset_id == asset_id).all()
    
    def get_evaluations_by_user(self, user_id: int) -> List[Evaluation]:
        """Get all evaluations by a user."""
        with self.get_session() as session:
            return session.query(Evaluation).filter(Evaluation.user_id == user_id).all()
    
    # Review card operations
    def create_review_card(
        self,
        card_id: str,
        asset_id: int,
        **kwargs,
    ) -> ReviewCard:
        """Create a new review card."""
        with self.get_session() as session:
            review_card = ReviewCard(
                card_id=card_id,
                asset_id=asset_id,
                **kwargs,
            )
            session.add(review_card)
            session.flush()
            session.refresh(review_card)
            return review_card
    
    def get_review_card_by_id(self, card_id: str) -> Optional[ReviewCard]:
        """Get a review card by ID."""
        with self.get_session() as session:
            return session.query(ReviewCard).filter(ReviewCard.card_id == card_id).first()
    
    def get_review_cards_by_asset(self, asset_id: int) -> List[ReviewCard]:
        """Get all review cards for an asset."""
        with self.get_session() as session:
            return session.query(ReviewCard).filter(ReviewCard.asset_id == asset_id).all()
    
    # Audit entry operations
    def create_audit_entry(
        self,
        entry_id: str,
        evaluator_name: str,
        decision_type: str,
        decision_value: Any,
        reasoning: str,
        evaluation_id: Optional[int] = None,
        **kwargs,
    ) -> AuditEntry:
        """Create a new audit entry."""
        with self.get_session() as session:
            audit_entry = AuditEntry(
                entry_id=entry_id,
                evaluator_name=evaluator_name,
                decision_type=decision_type,
                decision_value=decision_value,
                reasoning=reasoning,
                evaluation_id=evaluation_id,
                **kwargs,
            )
            session.add(audit_entry)
            session.flush()
            session.refresh(audit_entry)
            return audit_entry
    
    def get_audit_entries_by_evaluation(self, evaluation_id: int) -> List[AuditEntry]:
        """Get all audit entries for an evaluation."""
        with self.get_session() as session:
            return session.query(AuditEntry).filter(AuditEntry.evaluation_id == evaluation_id).all()
    
    def get_audit_entries_by_evaluator(self, evaluator_name: str) -> List[AuditEntry]:
        """Get all audit entries from a specific evaluator."""
        with self.get_session() as session:
            return session.query(AuditEntry).filter(AuditEntry.evaluator_name == evaluator_name).all()
    
    # Job description operations
    def create_job_description(
        self,
        job_id: str,
        role_family: str,
        source: str,
        **kwargs,
    ) -> JobDescription:
        """Create a new job description."""
        with self.get_session() as session:
            job_description = JobDescription(
                job_id=job_id,
                role_family=role_family,
                source=source,
                **kwargs,
            )
            session.add(job_description)
            session.flush()
            session.refresh(job_description)
            return job_description
    
    def get_job_descriptions_by_role_family(self, role_family: str) -> List[JobDescription]:
        """Get all job descriptions for a role family."""
        with self.get_session() as session:
            return session.query(JobDescription).filter(JobDescription.role_family == role_family).all()
    
    def get_job_descriptions_by_source(self, source: str) -> List[JobDescription]:
        """Get all job descriptions from a source."""
        with self.get_session() as session:
            return session.query(JobDescription).filter(JobDescription.source == source).all()
    
    # Competency operations
    def create_competency(
        self,
        competency_id: str,
        name: str,
        domain: str,
        **kwargs,
    ) -> Competency:
        """Create a new competency."""
        with self.get_session() as session:
            competency = Competency(
                competency_id=competency_id,
                name=name,
                domain=domain,
                **kwargs,
            )
            session.add(competency)
            session.flush()
            session.refresh(competency)
            return competency
    
    def get_competency_by_id(self, competency_id: str) -> Optional[Competency]:
        """Get a competency by ID."""
        with self.get_session() as session:
            return session.query(Competency).filter(Competency.competency_id == competency_id).first()
    
    def get_competencies_by_domain(self, domain: str) -> List[Competency]:
        """Get all competencies in a domain."""
        with self.get_session() as session:
            return session.query(Competency).filter(Competency.domain == domain).all()
    
    # Competency graph operations
    def create_competency_graph(
        self,
        graph_id: str,
        name: str,
        **kwargs,
    ) -> CompetencyGraph:
        """Create a new competency graph."""
        with self.get_session() as session:
            competency_graph = CompetencyGraph(
                graph_id=graph_id,
                name=name,
                **kwargs,
            )
            session.add(competency_graph)
            session.flush()
            session.refresh(competency_graph)
            return competency_graph
    
    def get_active_competency_graph(self) -> Optional[CompetencyGraph]:
        """Get the active competency graph."""
        with self.get_session() as session:
            return session.query(CompetencyGraph).filter(CompetencyGraph.is_active == True).first()
    
    def set_active_competency_graph(self, graph_id: str) -> Optional[CompetencyGraph]:
        """Set a competency graph as active."""
        with self.get_session() as session:
            # Deactivate all graphs
            session.query(CompetencyGraph).update({"is_active": False})
            
            # Activate the specified graph
            graph = session.query(CompetencyGraph).filter(CompetencyGraph.graph_id == graph_id).first()
            if graph:
                graph.is_active = True
                session.flush()
                session.refresh(graph)
            return graph
    
    # Outcome operations
    def create_outcome(
        self,
        outcome_id: str,
        intervention_type: str,
        asset_id: str,
        **kwargs,
    ) -> Outcome:
        """Create a new outcome."""
        with self.get_session() as session:
            outcome = Outcome(
                outcome_id=outcome_id,
                intervention_type=intervention_type,
                asset_id=asset_id,
                **kwargs,
            )
            session.add(outcome)
            session.flush()
            session.refresh(outcome)
            return outcome
    
    def get_verified_outcomes(self) -> List[Outcome]:
        """Get all verified outcomes."""
        with self.get_session() as session:
            return session.query(Outcome).filter(Outcome.is_verified == True).all()
    
    def get_outcomes_by_asset(self, asset_id: str) -> List[Outcome]:
        """Get all outcomes for an asset."""
        with self.get_session() as session:
            return session.query(Outcome).filter(Outcome.asset_id == asset_id).all()
    
    # Health check
    def health_check(self) -> bool:
        """Check if database connection is healthy."""
        try:
            with self.get_session() as session:
                session.execute("SELECT 1")
            return True
        except Exception as e:
            logger.error(f"Database health check failed: {e}")
            return False


# Singleton instance
_db_manager: Optional[DatabaseManager] = None


def get_database_manager() -> DatabaseManager:
    """Get the singleton database manager instance."""
    global _db_manager
    if _db_manager is None:
        _db_manager = DatabaseManager()
    return _db_manager


def init_database(database_url: Optional[str] = None) -> DatabaseManager:
    """
    Initialize the database manager and create tables.
    
    Args:
        database_url: Optional database URL. If not provided, uses DATABASE_URL env var.
    
    Returns:
        DatabaseManager instance
    """
    db_manager = DatabaseManager(database_url)
    db_manager.create_tables()
    return db_manager
