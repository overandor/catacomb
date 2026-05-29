"""Outcome Ledger v2 - Closed-loop prediction system with SQLite storage."""
import sqlite3
import json
import uuid
from datetime import datetime
from typing import Dict, Any, List, Optional
from enum import Enum


class InterventionStatus(Enum):
    PLANNED = "planned"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    VERIFIED = "verified"
    FAILED = "failed"


class VerificationStatus(Enum):
    VERIFIED = "verified"
    DISPUTED = "disputed"
    PENDING = "pending"


class OutcomeLedger:
    """Closed-loop system for tracking predictions, interventions, and outcomes."""
    
    def __init__(self, db_path: str = "outcome_ledger.db"):
        self.db_path = db_path
        self._init_db()
    
    def _init_db(self):
        """Initialize SQLite database with schema."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Interventions table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS interventions (
                record_id TEXT PRIMARY KEY,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL,
                
                -- Asset identification
                asset_id TEXT NOT NULL,
                asset_type TEXT NOT NULL,
                asset_name TEXT NOT NULL,
                
                -- Developer identification
                developer_id TEXT,
                developer_username TEXT,
                
                -- Before state (JSON)
                before_state TEXT NOT NULL,
                before_hash TEXT NOT NULL,
                
                -- Prediction
                intervention_type TEXT NOT NULL,
                intervention_description TEXT,
                planned_effort_days INTEGER,
                predicted_value REAL,
                predicted_probability REAL,
                predicted_risk REAL,
                predicted_outcome TEXT,
                
                -- Execution
                status TEXT NOT NULL,
                started_at TEXT,
                completed_at TEXT,
                actual_effort_days INTEGER,
                
                -- After state (JSON)
                after_state TEXT,
                after_hash TEXT,
                
                -- Observed outcome (JSON)
                outcome_metrics TEXT,
                
                -- Verification
                verification_status TEXT,
                verification_notes TEXT,
                
                -- Learning
                prediction_accuracy TEXT,
                
                -- Reproducibility
                intervention_hash TEXT NOT NULL
            )
        """)
        
        # Verifications table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS verifications (
                verification_id TEXT PRIMARY KEY,
                record_id TEXT NOT NULL,
                verifier_id TEXT NOT NULL,
                verifier_username TEXT NOT NULL,
                status TEXT NOT NULL,
                notes TEXT,
                verified_at TEXT NOT NULL,
                FOREIGN KEY (record_id) REFERENCES interventions(record_id)
            )
        """)
        
        # Developer profiles table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS developer_profiles (
                developer_id TEXT PRIMARY KEY,
                username TEXT NOT NULL,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL,
                
                -- Reputation metrics
                total_interventions INTEGER DEFAULT 0,
                successful_interventions INTEGER DEFAULT 0,
                failed_interventions INTEGER DEFAULT 0,
                disputed_interventions INTEGER DEFAULT 0,
                
                -- Value created
                total_value_created REAL DEFAULT 0.0,
                avg_value_per_intervention REAL DEFAULT 0.0,
                
                -- Accuracy
                prediction_accuracy REAL DEFAULT 0.0,
                effort_accuracy REAL DEFAULT 0.0,
                
                -- Specialization (JSON)
                top_intervention_types TEXT,
                top_languages TEXT,
                top_categories TEXT
            )
        """)
        
        # Asset history table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS asset_history (
                asset_id TEXT NOT NULL,
                snapshot_timestamp TEXT NOT NULL,
                snapshot_data TEXT NOT NULL,
                PRIMARY KEY (asset_id, snapshot_timestamp)
            )
        """)
        
        # Transformation laws table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS transformation_laws (
                law_id TEXT PRIMARY KEY,
                pattern_signature TEXT NOT NULL,
                intervention_type TEXT NOT NULL,
                asset_category TEXT,
                language TEXT,
                
                -- Statistics
                total_applications INTEGER DEFAULT 0,
                successful_applications INTEGER DEFAULT 0,
                avg_adoption_multiplier REAL DEFAULT 0.0,
                avg_value_created REAL DEFAULT 0.0,
                
                -- Confidence
                confidence_score REAL DEFAULT 0.0,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            )
        """)
        
        conn.commit()
        conn.close()
    
    def create_intervention(
        self,
        asset_id: str,
        asset_type: str,
        asset_name: str,
        developer_id: str,
        developer_username: str,
        before_state: Dict[str, Any],
        intervention_type: str,
        intervention_description: str,
        planned_effort_days: int,
        predicted_value: float,
        predicted_probability: float,
        predicted_risk: float,
        predicted_outcome: Dict[str, float] = None
    ) -> str:
        """Create a new intervention record."""
        record_id = str(uuid.uuid4())
        now = datetime.utcnow().isoformat()
        
        before_hash = self._compute_hash(before_state)
        intervention_hash = self._compute_hash({
            "intervention_type": intervention_type,
            "intervention_description": intervention_description,
            "asset_id": asset_id
        })
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO interventions (
                record_id, created_at, updated_at,
                asset_id, asset_type, asset_name,
                developer_id, developer_username,
                before_state, before_hash,
                intervention_type, intervention_description, planned_effort_days,
                predicted_value, predicted_probability, predicted_risk, predicted_outcome,
                status, intervention_hash
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            record_id, now, now,
            asset_id, asset_type, asset_name,
            developer_id, developer_username,
            json.dumps(before_state), before_hash,
            intervention_type, intervention_description, planned_effort_days,
            predicted_value, predicted_probability, predicted_risk,
            json.dumps(predicted_outcome) if predicted_outcome else None,
            InterventionStatus.PLANNED.value, intervention_hash
        ))
        
        conn.commit()
        conn.close()
        
        return record_id
    
    def start_intervention(self, record_id: str, actual_effort_days: int = None) -> Dict[str, Any]:
        """Mark intervention as started."""
        now = datetime.utcnow().isoformat()
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            UPDATE interventions
            SET status = ?, started_at = ?, updated_at = ?, actual_effort_days = COALESCE(?, actual_effort_days)
            WHERE record_id = ?
        """, (InterventionStatus.IN_PROGRESS.value, now, now, actual_effort_days, record_id))
        
        conn.commit()
        conn.close()
        
        return self.get_intervention(record_id)
    
    def complete_intervention(
        self,
        record_id: str,
        after_state: Dict[str, Any],
        outcome_metrics: Dict[str, float],
        actual_effort_days: int = None
    ) -> Dict[str, Any]:
        """Mark intervention as completed with after state and outcomes."""
        now = datetime.utcnow().isoformat()
        after_hash = self._compute_hash(after_state)
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Get before state for comparison
        cursor.execute("SELECT before_state, predicted_outcome FROM interventions WHERE record_id = ?", (record_id,))
        row = cursor.fetchone()
        if not row:
            conn.close()
            raise ValueError(f"Record {record_id} not found")
        
        before_state_json, predicted_outcome_json = row
        before_state = json.loads(before_state_json)
        predicted_outcome = json.loads(predicted_outcome_json) if predicted_outcome_json else {}
        
        # Calculate prediction accuracy
        prediction_accuracy = self._calculate_prediction_accuracy(
            predicted_outcome, outcome_metrics, before_state, after_state
        )
        
        cursor.execute("""
            UPDATE interventions
            SET status = ?, completed_at = ?, updated_at = ?, 
                after_state = ?, after_hash = ?, outcome_metrics = ?,
                actual_effort_days = COALESCE(?, actual_effort_days),
                prediction_accuracy = ?
            WHERE record_id = ?
        """, (
            InterventionStatus.COMPLETED.value, now, now,
            json.dumps(after_state), after_hash, json.dumps(outcome_metrics),
            actual_effort_days,
            json.dumps(prediction_accuracy),
            record_id
        ))
        
        # Update developer profile
        cursor.execute("SELECT developer_id FROM interventions WHERE record_id = ?", (record_id,))
        developer_id = cursor.fetchone()[0]
        if developer_id:
            self._update_developer_profile(cursor, developer_id, prediction_accuracy, outcome_metrics)
        
        conn.commit()
        conn.close()
        
        return self.get_intervention(record_id)
    
    def verify_outcome(
        self,
        record_id: str,
        verifier_id: str,
        verifier_username: str,
        status: str,
        notes: str = None
    ) -> Dict[str, Any]:
        """Verify an intervention outcome."""
        verification_id = str(uuid.uuid4())
        now = datetime.utcnow().isoformat()
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Add verification record
        cursor.execute("""
            INSERT INTO verifications (verification_id, record_id, verifier_id, verifier_username, status, notes, verified_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (verification_id, record_id, verifier_id, verifier_username, status, notes, now))
        
        # Update intervention status if verified
        if status == VerificationStatus.VERIFIED.value:
            cursor.execute("""
                UPDATE interventions
                SET status = ?, verification_status = ?, verification_notes = ?, updated_at = ?
                WHERE record_id = ?
            """, (InterventionStatus.VERIFIED.value, status, notes, now, record_id))
        
        conn.commit()
        conn.close()
        
        return self.get_intervention(record_id)
    
    def get_intervention(self, record_id: str) -> Dict[str, Any]:
        """Get intervention record by ID."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM interventions WHERE record_id = ?", (record_id,))
        row = cursor.fetchone()
        
        if not row:
            conn.close()
            return None
        
        columns = [desc[0] for desc in cursor.description]
        result = dict(zip(columns, row))
        
        # Parse JSON fields
        for json_field in ['before_state', 'predicted_outcome', 'after_state', 'outcome_metrics', 'prediction_accuracy']:
            if result[json_field]:
                result[json_field] = json.loads(result[json_field])
        
        conn.close()
        return result
    
    def get_developer_reputation(self, developer_id: str) -> Dict[str, Any]:
        """Get developer reputation metrics."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM developer_profiles WHERE developer_id = ?", (developer_id,))
        row = cursor.fetchone()
        
        if not row:
            conn.close()
            return None
        
        columns = [desc[0] for desc in cursor.description]
        result = dict(zip(columns, row))
        
        # Parse JSON fields
        for json_field in ['top_intervention_types', 'top_languages', 'top_categories']:
            if result[json_field]:
                result[json_field] = json.loads(result[json_field])
        
        conn.close()
        return result
    
    def get_training_dataset(self) -> List[Dict[str, Any]]:
        """Get all completed interventions for ML training."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT record_id, before_state, intervention_type, predicted_outcome, 
                   after_state, outcome_metrics, prediction_accuracy
            FROM interventions
            WHERE status = ?
            ORDER BY completed_at DESC
        """, (InterventionStatus.COMPLETED.value,))
        
        rows = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]
        
        dataset = []
        for row in rows:
            result = dict(zip(columns, row))
            # Parse JSON fields
            for json_field in ['before_state', 'predicted_outcome', 'after_state', 'outcome_metrics', 'prediction_accuracy']:
                if result[json_field]:
                    result[json_field] = json.loads(result[json_field])
            dataset.append(result)
        
        conn.close()
        return dataset
    
    def snapshot_asset(self, asset_id: str, snapshot_data: Dict[str, Any]):
        """Take a snapshot of asset metrics."""
        now = datetime.utcnow().isoformat()
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT OR REPLACE INTO asset_history (asset_id, snapshot_timestamp, snapshot_data)
            VALUES (?, ?, ?)
        """, (asset_id, now, json.dumps(snapshot_data)))
        
        conn.commit()
        conn.close()
    
    def _compute_hash(self, data: Dict[str, Any]) -> str:
        """Compute SHA256 hash of data for reproducibility."""
        import hashlib
        return hashlib.sha256(json.dumps(data, sort_keys=True).encode()).hexdigest()[:32]
    
    def _calculate_prediction_accuracy(
        self,
        predicted: Dict[str, float],
        observed: Dict[str, float],
        before: Dict[str, Any],
        after: Dict[str, Any]
    ) -> Dict[str, float]:
        """Calculate prediction accuracy metrics."""
        accuracy = {}
        
        # Calculate actual deltas
        star_delta = after.get('stars', 0) - before.get('stars', 0)
        contributor_delta = after.get('contributors', 0) - before.get('contributors', 0)
        fork_delta = after.get('forks', 0) - before.get('forks', 0)
        
        # Normalize deltas
        max_stars = max(before.get('stars', 1), 1)
        star_growth = star_delta / max_stars
        
        # Compare with predictions
        predicted_star_growth = predicted.get('star_growth', 0)
        predicted_contributor_growth = predicted.get('contributor_growth', 0)
        
        accuracy['star_growth_error'] = abs(star_growth - predicted_star_growth)
        accuracy['contributor_growth_error'] = abs(contributor_delta/10 - predicted_contributor_growth)  # Normalize
        accuracy['overall_error'] = (accuracy['star_growth_error'] + accuracy['contributor_growth_error']) / 2
        
        return accuracy
    
    def _update_developer_profile(
        self,
        cursor: sqlite3.Cursor,
        developer_id: str,
        prediction_accuracy: Dict[str, float],
        outcome_metrics: Dict[str, float]
    ):
        """Update developer profile with new intervention results."""
        # Check if profile exists
        cursor.execute("SELECT developer_id FROM developer_profiles WHERE developer_id = ?", (developer_id,))
        exists = cursor.fetchone()
        
        now = datetime.utcnow().isoformat()
        
        if exists:
            # Update existing profile
            cursor.execute("""
                UPDATE developer_profiles
                SET total_interventions = total_interventions + 1,
                    updated_at = ?,
                    prediction_accuracy = prediction_accuracy * 0.9 + ? * 0.1
                WHERE developer_id = ?
            """, (now, 1 - prediction_accuracy.get('overall_error', 0), developer_id))
        else:
            # Create new profile
            cursor.execute("""
                INSERT INTO developer_profiles (developer_id, username, created_at, updated_at, total_interventions, prediction_accuracy)
                VALUES (?, ?, ?, ?, 1, ?)
            """, (developer_id, developer_id, now, now, 1 - prediction_accuracy.get('overall_error', 0)))
