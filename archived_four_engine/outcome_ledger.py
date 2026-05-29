"""Outcome Ledger - tracks intervention results and enables learning from reality."""
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
from dataclasses import dataclass, field
from enum import Enum
import json
import hashlib


class InterventionStatus(Enum):
    """Status of an intervention."""
    PLANNED = "planned"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    ABANDONED = "abandoned"


class VerificationStatus(Enum):
    """Verification status of outcome claims."""
    PENDING = "pending"
    VERIFIED = "verified"
    DISPUTED = "disputed"
    REJECTED = "rejected"


@dataclass
class InterventionRecord:
    """A complete record of an intervention and its outcome."""
    record_id: str
    asset_id: str
    asset_type: str
    asset_name: str
    developer_id: str
    developer_username: str
    
    # Before state
    before_state: Dict[str, Any]
    
    # Intervention
    intervention_type: str
    intervention_description: str
    planned_effort_days: int
    actual_effort_days: int = 0
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    
    # Predictions (at time of intervention)
    predicted_value: float
    predicted_probability: float
    predicted_risk: float
    
    # Status
    status: InterventionStatus = InterventionStatus.PLANNED
    
    # After state (when completed)
    after_state: Optional[Dict[str, Any]] = None
    
    # Outcome metrics (when completed)
    outcome_metrics: Optional[Dict[str, Any]] = None
    
    # Actual delta metrics (the most valuable data)
    actual_stars_delta: Optional[int] = None
    actual_downloads_delta: Optional[int] = None
    actual_revenue_delta: Optional[float] = None
    actual_contributors_delta: Optional[int] = None
    
    # Verification
    verification_status: VerificationStatus = VerificationStatus.PENDING
    verified_by: Optional[List[str]] = None
    verification_notes: Optional[str] = None
    
    # Metadata
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    updated_at: str = field(default_factory=lambda: datetime.now().isoformat())
    
    def calculate_prediction_accuracy(self) -> Dict[str, float]:
        """Calculate how accurate predictions were."""
        if not self.outcome_metrics:
            return {}
        
        # Calculate actual value from outcome
        actual_value = self.outcome_metrics.get("actual_value", 0)
        
        # Value accuracy
        value_error = abs(self.predicted_value - actual_value)
        value_accuracy = max(0, 1 - value_error)
        
        # Probability accuracy (did it succeed?)
        actual_success = self.outcome_metrics.get("success", False)
        probability_accuracy = 1 - abs(self.predicted_probability - (1 if actual_success else 0))
        
        # Risk accuracy
        actual_risk = self.outcome_metrics.get("actual_risk", 0)
        risk_accuracy = 1 - abs(self.predicted_risk - actual_risk)
        
        return {
            "value_accuracy": value_accuracy,
            "probability_accuracy": probability_accuracy,
            "risk_accuracy": risk_accuracy,
            "overall_accuracy": (value_accuracy + probability_accuracy + risk_accuracy) / 3
        }
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "record_id": self.record_id,
            "asset_id": self.asset_id,
            "asset_type": self.asset_type,
            "asset_name": self.asset_name,
            "developer_id": self.developer_id,
            "developer_username": self.developer_username,
            "before_state": self.before_state,
            "intervention_type": self.intervention_type,
            "intervention_description": self.intervention_description,
            "planned_effort_days": self.planned_effort_days,
            "actual_effort_days": self.actual_effort_days,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "predicted_value": self.predicted_value,
            "predicted_probability": self.predicted_probability,
            "predicted_risk": self.predicted_risk,
            "status": self.status.value,
            "after_state": self.after_state,
            "outcome_metrics": self.outcome_metrics,
            "actual_stars_delta": self.actual_stars_delta,
            "actual_downloads_delta": self.actual_downloads_delta,
            "actual_revenue_delta": self.actual_revenue_delta,
            "actual_contributors_delta": self.actual_contributors_delta,
            "verification_status": self.verification_status.value,
            "verified_by": self.verified_by,
            "verification_notes": self.verification_notes,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "prediction_accuracy": self.calculate_prediction_accuracy()
        }


class OutcomeLedger:
    """Ledger for tracking intervention outcomes and learning from reality."""
    
    def __init__(self, storage_path: str = "outcome_ledger.json"):
        self.storage_path = storage_path
        self.records: Dict[str, InterventionRecord] = {}
        self._load()
    
    def _load(self):
        """Load records from storage."""
        try:
            with open(self.storage_path, 'r') as f:
                data = json.load(f)
                for record_data in data:
                    record = self._dict_to_record(record_data)
                    self.records[record.record_id] = record
        except FileNotFoundError:
            self.records = {}
    
    def _save(self):
        """Save records to storage."""
        data = [record.to_dict() for record in self.records.values()]
        with open(self.storage_path, 'w') as f:
            json.dump(data, f, indent=2)
    
    def _dict_to_record(self, data: Dict[str, Any]) -> InterventionRecord:
        """Convert dictionary to InterventionRecord."""
        return InterventionRecord(
            record_id=data["record_id"],
            asset_id=data["asset_id"],
            asset_type=data["asset_type"],
            asset_name=data["asset_name"],
            developer_id=data["developer_id"],
            developer_username=data["developer_username"],
            before_state=data["before_state"],
            intervention_type=data["intervention_type"],
            intervention_description=data["intervention_description"],
            planned_effort_days=data["planned_effort_days"],
            actual_effort_days=data.get("actual_effort_days", 0),
            start_date=data.get("start_date"),
            end_date=data.get("end_date"),
            predicted_value=data["predicted_value"],
            predicted_probability=data["predicted_probability"],
            predicted_risk=data["predicted_risk"],
            status=InterventionStatus(data.get("status", "planned")),
            after_state=data.get("after_state"),
            outcome_metrics=data.get("outcome_metrics"),
            verification_status=VerificationStatus(data.get("verification_status", "pending")),
            verified_by=data.get("verified_by"),
            verification_notes=data.get("verification_notes"),
            created_at=data.get("created_at"),
            updated_at=data.get("updated_at")
        )
    
    def _generate_record_id(self) -> str:
        """Generate unique record ID."""
        timestamp = datetime.now().isoformat()
        content = f"{timestamp}_{len(self.records)}"
        return hashlib.sha256(content.encode()).hexdigest()[:16]
    
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
        predicted_risk: float
    ) -> InterventionRecord:
        """Create a new intervention record."""
        record_id = self._generate_record_id()
        
        record = InterventionRecord(
            record_id=record_id,
            asset_id=asset_id,
            asset_type=asset_type,
            asset_name=asset_name,
            developer_id=developer_id,
            developer_username=developer_username,
            before_state=before_state,
            intervention_type=intervention_type,
            intervention_description=intervention_description,
            planned_effort_days=planned_effort_days,
            predicted_value=predicted_value,
            predicted_probability=predicted_probability,
            predicted_risk=predicted_risk
        )
        
        self.records[record_id] = record
        self._save()
        
        return record
    
    def start_intervention(self, record_id: str, actual_effort_days: int = None) -> InterventionRecord:
        """Mark intervention as in progress."""
        record = self.records.get(record_id)
        if not record:
            raise ValueError(f"Record {record_id} not found")
        
        record.status = InterventionStatus.IN_PROGRESS
        record.start_date = datetime.now().isoformat()
        if actual_effort_days:
            record.actual_effort_days = actual_effort_days
        record.updated_at = datetime.now().isoformat()
        
        self._save()
        return record
    
    def complete_intervention(
        self,
        record_id: str,
        after_state: Dict[str, Any],
        outcome_metrics: Dict[str, Any],
        actual_effort_days: int = None,
        actual_stars_delta: int = None,
        actual_downloads_delta: int = None,
        actual_revenue_delta: float = None,
        actual_contributors_delta: int = None
    ) -> InterventionRecord:
        """Mark intervention as completed with outcome data."""
        record = self.records.get(record_id)
        if not record:
            raise ValueError(f"Record {record_id} not found")
        
        record.status = InterventionStatus.COMPLETED
        record.end_date = datetime.now().isoformat()
        record.after_state = after_state
        record.outcome_metrics = outcome_metrics
        record.actual_stars_delta = actual_stars_delta
        record.actual_downloads_delta = actual_downloads_delta
        record.actual_revenue_delta = actual_revenue_delta
        record.actual_contributors_delta = actual_contributors_delta
        if actual_effort_days:
            record.actual_effort_days = actual_effort_days
        record.updated_at = datetime.now().isoformat()
        
        self._save()
        return record
    
    def fail_intervention(self, record_id: str, reason: str) -> InterventionRecord:
        """Mark intervention as failed."""
        record = self.records.get(record_id)
        if not record:
            raise ValueError(f"Record {record_id} not found")
        
        record.status = InterventionStatus.FAILED
        record.end_date = datetime.now().isoformat()
        record.outcome_metrics = {"failure_reason": reason}
        record.updated_at = datetime.now().isoformat()
        
        self._save()
        return record
    
    def verify_outcome(
        self,
        record_id: str,
        verifier_id: str,
        status: VerificationStatus,
        notes: str = None
    ) -> InterventionRecord:
        """Verify an intervention outcome."""
        record = self.records.get(record_id)
        if not record:
            raise ValueError(f"Record {record_id} not found")
        
        if not record.verified_by:
            record.verified_by = []
        
        record.verified_by.append(verifier_id)
        record.verification_status = status
        record.verification_notes = notes
        record.updated_at = datetime.now().isoformat()
        
        self._save()
        return record
    
    def get_record(self, record_id: str) -> Optional[InterventionRecord]:
        """Get a specific record."""
        return self.records.get(record_id)
    
    def get_developer_records(self, developer_id: str) -> List[InterventionRecord]:
        """Get all records for a developer."""
        return [
            record for record in self.records.values()
            if record.developer_id == developer_id
        ]
    
    def get_asset_records(self, asset_id: str) -> List[InterventionRecord]:
        """Get all records for an asset."""
        return [
            record for record in self.records.values()
            if record.asset_id == asset_id
        ]
    
    def get_intervention_type_records(self, intervention_type: str) -> List[InterventionRecord]:
        """Get all records of a specific intervention type."""
        return [
            record for record in self.records.values()
            if record.intervention_type == intervention_type
        ]
    
    def get_completed_records(self) -> List[InterventionRecord]:
        """Get all completed records."""
        return [
            record for record in self.records.values()
            if record.status == InterventionStatus.COMPLETED
        ]
    
    def calculate_learning_metrics(self) -> Dict[str, Any]:
        """Calculate learning metrics from completed records."""
        completed = self.get_completed_records()
        
        if not completed:
            return {"message": "No completed records to learn from"}
        
        # Calculate prediction accuracies
        value_accuracies = []
        probability_accuracies = []
        risk_accuracies = []
        
        for record in completed:
            accuracy = record.calculate_prediction_accuracy()
            if accuracy:
                value_accuracies.append(accuracy.get("value_accuracy", 0))
                probability_accuracies.append(accuracy.get("probability_accuracy", 0))
                risk_accuracies.append(accuracy.get("risk_accuracy", 0))
        
        metrics = {
            "total_completed": len(completed),
            "avg_value_accuracy": sum(value_accuracies) / len(value_accuracies) if value_accuracies else 0,
            "avg_probability_accuracy": sum(probability_accuracies) / len(probability_accuracies) if probability_accuracies else 0,
            "avg_risk_accuracy": sum(risk_accuracies) / len(risk_accuracies) if risk_accuracies else 0,
            "overall_accuracy": (sum(value_accuracies) + sum(probability_accuracies) + sum(risk_accuracies)) / (3 * len(completed)) if completed else 0
        }
        
        # Calculate intervention type success rates
        intervention_success = {}
        for record in completed:
            intervention = record.intervention_type
            if intervention not in intervention_success:
                intervention_success[intervention] = {"total": 0, "successful": 0}
            
            intervention_success[intervention]["total"] += 1
            if record.outcome_metrics and record.outcome_metrics.get("success", False):
                intervention_success[intervention]["successful"] += 1
        
        for intervention, data in intervention_success.items():
            intervention_success[intervention]["success_rate"] = data["successful"] / data["total"] if data["total"] > 0 else 0
        
        metrics["intervention_success_rates"] = intervention_success
        
        return metrics
    
    def get_training_dataset(self) -> List[Dict[str, Any]]:
        """Get training dataset for ML models."""
        completed = self.get_completed_records()
        
        training_data = []
        for record in completed:
            if record.outcome_metrics:
                training_data.append({
                    "before_state": record.before_state,
                    "intervention": record.intervention_type,
                    "predicted_value": record.predicted_value,
                    "predicted_probability": record.predicted_probability,
                    "predicted_risk": record.predicted_risk,
                    "actual_value": record.outcome_metrics.get("actual_value", 0),
                    "actual_success": record.outcome_metrics.get("success", False),
                    "actual_risk": record.outcome_metrics.get("actual_risk", 0),
                    "effort_days": record.actual_effort_days,
                    "prediction_accuracy": record.calculate_prediction_accuracy()
                })
        
        return training_data
    
    def export_dataset(self, filepath: str):
        """Export dataset for external analysis."""
        dataset = self.get_training_dataset()
        with open(filepath, 'w') as f:
            json.dump(dataset, f, indent=2)
    
    def get_developer_reputation(self, developer_id: str) -> Dict[str, Any]:
        """Calculate developer reputation based on intervention outcomes."""
        records = self.get_developer_records(developer_id)
        
        if not records:
            return {"message": "No records for developer"}
        
        completed = [r for r in records if r.status == InterventionStatus.COMPLETED]
        
        reputation = {
            "total_interventions": len(records),
            "completed_interventions": len(completed),
            "success_rate": 0,
            "avg_prediction_accuracy": 0,
            "total_value_created": 0,
            "total_effort_days": 0
        }
        
        if completed:
            successful = [r for r in completed if r.outcome_metrics and r.outcome_metrics.get("success", False)]
            reputation["success_rate"] = len(successful) / len(completed)
            
            accuracies = [r.calculate_prediction_accuracy().get("overall_accuracy", 0) for r in completed]
            reputation["avg_prediction_accuracy"] = sum(accuracies) / len(accuracies)
            
            reputation["total_value_created"] = sum(
                r.outcome_metrics.get("value_created", 0) for r in completed if r.outcome_metrics
            )
            
            reputation["total_effort_days"] = sum(r.actual_effort_days for r in completed)
        
        return reputation


class InterventionDataset:
    """Proprietary dataset of intervention-outcome pairs."""
    
    def __init__(self, ledger: OutcomeLedger):
        self.ledger = ledger
    
    def get_intervention_effectiveness(self, intervention_type: str) -> Dict[str, float]:
        """Get effectiveness metrics for a specific intervention type."""
        records = self.ledger.get_intervention_type_records(intervention_type)
        completed = [r for r in records if r.status == InterventionStatus.COMPLETED]
        
        if not completed:
            return {"message": "No completed records for this intervention type"}
        
        # Calculate effectiveness metrics
        avg_value = sum(r.outcome_metrics.get("actual_value", 0) for r in completed if r.outcome_metrics) / len(completed)
        success_rate = sum(1 for r in completed if r.outcome_metrics and r.outcome_metrics.get("success", False)) / len(completed)
        avg_effort = sum(r.actual_effort_days for r in completed) / len(completed)
        
        return {
            "intervention_type": intervention_type,
            "total_completed": len(completed),
            "avg_value_created": avg_value,
            "success_rate": success_rate,
            "avg_effort_days": avg_effort,
            "value_per_day": avg_value / avg_effort if avg_effort > 0 else 0
        }
    
    def get_all_intervention_effectiveness(self) -> Dict[str, Dict[str, float]]:
        """Get effectiveness metrics for all intervention types."""
        intervention_types = set()
        for record in self.ledger.records.values():
            intervention_types.add(record.intervention_type)
        
        effectiveness = {}
        for intervention_type in intervention_types:
            effectiveness[intervention_type] = self.get_intervention_effectiveness(intervention_type)
        
        return effectiveness
    
    def find_best_interventions(self, asset_type: str = None) -> List[Dict[str, Any]]:
        """Find the most effective interventions by value per day."""
        effectiveness = self.get_all_intervention_effectiveness()
        
        # Filter by asset type if specified
        if asset_type:
            effectiveness = {
                k: v for k, v in effectiveness.items()
                if self._is_applicable_to_asset_type(k, asset_type)
            }
        
        # Sort by value per day
        sorted_interventions = sorted(
            effectiveness.items(),
            key=lambda x: x[1].get("value_per_day", 0),
            reverse=True
        )
        
        return [
            {
                "intervention_type": intervention,
                **metrics
            }
            for intervention, metrics in sorted_interventions
        ]
    
    def _is_applicable_to_asset_type(self, intervention: str, asset_type: str) -> bool:
        """Check if intervention is applicable to asset type."""
        # Placeholder - would have mapping of interventions to asset types
        return True
