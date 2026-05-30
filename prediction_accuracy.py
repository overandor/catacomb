"""Prediction Accuracy Reporting for Catacomb.

Tracks and reports prediction accuracy metrics:
- MAE (Mean Absolute Error)
- Calibration Error
- Brier Score
- Intervention-type accuracy
- Prediction drift
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple
from datetime import datetime, timedelta
import json
import math
from collections import defaultdict


@dataclass
class PredictionRecord:
    """A single prediction record."""
    record_id: str
    intervention_type: str
    predicted_value: float
    predicted_probability: float
    actual_value: float
    actual_success: bool
    timestamp: datetime
    developer_id: str
    
    # Optional metadata
    asset_category: str = ""
    effort_days: int = 0


@dataclass
class AccuracyMetrics:
    """Accuracy metrics for a subset of predictions."""
    mae: float  # Mean Absolute Error
    rmse: float  # Root Mean Square Error
    calibration_error: float  # Calibration error
    brier_score: float  # Brier score
    accuracy: float  # Binary accuracy
    precision: float
    recall: float
    f1_score: float
    sample_size: int
    
    # Per-type metrics
    per_type_metrics: Dict[str, Dict] = field(default_factory=dict)
    
    # Drift metrics
    prediction_drift: float = 0.0
    value_drift: float = 0.0


class PredictionAccuracyTracker:
    """Tracks and reports prediction accuracy metrics."""
    
    def __init__(self):
        self.records: List[PredictionRecord] = []
        self.baseline_metrics: Optional[AccuracyMetrics] = None
        self.baseline_timestamp: Optional[datetime] = None
    
    def add_record(self, record: PredictionRecord):
        """Add a prediction record."""
        self.records.append(record)
    
    def add_records_batch(self, records: List[PredictionRecord]):
        """Add multiple prediction records."""
        self.records.extend(records)
    
    def calculate_metrics(self, records: List[PredictionRecord] = None) -> AccuracyMetrics:
        """Calculate accuracy metrics for given records (or all if None)."""
        if records is None:
            records = self.records
        
        if not records:
            return AccuracyMetrics(
                mae=0.0, rmse=0.0, calibration_error=0.0, brier_score=0.0,
                accuracy=0.0, precision=0.0, recall=0.0, f1_score=0.0,
                sample_size=0
            )
        
        # Calculate MAE
        errors = [abs(r.predicted_value - r.actual_value) for r in records]
        mae = sum(errors) / len(errors)
        
        # Calculate RMSE
        squared_errors = [(r.predicted_value - r.actual_value) ** 2 for r in records]
        rmse = math.sqrt(sum(squared_errors) / len(squared_errors))
        
        # Calculate Brier Score (for binary predictions)
        brier_scores = [(r.predicted_probability - (1 if r.actual_success else 0)) ** 2 for r in records]
        brier_score = sum(brier_scores) / len(brier_scores)
        
        # Calculate binary accuracy
        predictions = [1 if r.predicted_probability > 0.5 else 0 for r in records]
        actuals = [1 if r.actual_success else 0 for r in records]
        accuracy = sum(1 for p, a in zip(predictions, actuals) if p == a) / len(predictions)
        
        # Calculate precision, recall, F1
        true_positives = sum(1 for p, a in zip(predictions, actuals) if p == 1 and a == 1)
        false_positives = sum(1 for p, a in zip(predictions, actuals) if p == 1 and a == 0)
        false_negatives = sum(1 for p, a in zip(predictions, actuals) if p == 0 and a == 1)
        
        precision = true_positives / (true_positives + false_positives) if (true_positives + false_positives) > 0 else 0
        recall = true_positives / (true_positives + false_negatives) if (true_positives + false_negatives) > 0 else 0
        f1_score = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0
        
        # Calculate calibration error
        calibration_error = self._calculate_calibration_error(records)
        
        # Calculate per-type metrics
        per_type_metrics = self._calculate_per_type_metrics(records)
        
        # Calculate drift if baseline exists
        prediction_drift = 0.0
        value_drift = 0.0
        if self.baseline_metrics and self.baseline_timestamp:
            prediction_drift = self._calculate_prediction_drift(records)
            value_drift = self._calculate_value_drift(records)
        
        return AccuracyMetrics(
            mae=mae,
            rmse=rmse,
            calibration_error=calibration_error,
            brier_score=brier_score,
            accuracy=accuracy,
            precision=precision,
            recall=recall,
            f1_score=f1_score,
            sample_size=len(records),
            per_type_metrics=per_type_metrics,
            prediction_drift=prediction_drift,
            value_drift=value_drift
        )
    
    def _calculate_calibration_error(self, records: List[PredictionRecord]) -> float:
        """Calculate calibration error (reliability diagram approach)."""
        # Group predictions by probability bins
        bins = defaultdict(list)
        for record in records:
            bin_key = int(record.predicted_probability * 10) / 10  # 0.0, 0.1, ..., 1.0
            bins[bin_key].append(record)
        
        # Calculate calibration error
        calibration_error = 0.0
        bin_count = 0
        
        for bin_prob, bin_records in bins.items():
            if not bin_records:
                continue
            
            actual_rate = sum(1 for r in bin_records if r.actual_success) / len(bin_records)
            calibration_error += abs(bin_prob - actual_rate)
            bin_count += 1
        
        return calibration_error / bin_count if bin_count > 0 else 0.0
    
    def _calculate_per_type_metrics(self, records: List[PredictionRecord]) -> Dict[str, Dict]:
        """Calculate metrics per intervention type."""
        type_records = defaultdict(list)
        for record in records:
            type_records[record.intervention_type].append(record)
        
        per_type_metrics = {}
        for intv_type, type_recs in type_records.items():
            if not type_recs:
                continue
            
            errors = [abs(r.predicted_value - r.actual_value) for r in type_recs]
            mae = sum(errors) / len(errors)
            
            predictions = [1 if r.predicted_probability > 0.5 else 0 for r in type_recs]
            actuals = [1 if r.actual_success else 0 for r in type_recs]
            accuracy = sum(1 for p, a in zip(predictions, actuals) if p == a) / len(predictions)
            
            per_type_metrics[intv_type] = {
                "mae": mae,
                "accuracy": accuracy,
                "sample_size": len(type_recs)
            }
        
        return per_type_metrics
    
    def _calculate_prediction_drift(self, records: List[PredictionRecord]) -> float:
        """Calculate prediction drift from baseline."""
        if not self.baseline_timestamp:
            return 0.0
        
        # Split records into old and new based on baseline timestamp
        old_records = [r for r in records if r.timestamp < self.baseline_timestamp]
        new_records = [r for r in records if r.timestamp >= self.baseline_timestamp]
        
        if not old_records or not new_records:
            return 0.0
        
        # Calculate average predicted probability
        old_avg_prob = sum(r.predicted_probability for r in old_records) / len(old_records)
        new_avg_prob = sum(r.predicted_probability for r in new_records) / len(new_records)
        
        return abs(new_avg_prob - old_avg_prob)
    
    def _calculate_value_drift(self, records: List[PredictionRecord]) -> float:
        """Calculate value drift from baseline."""
        if not self.baseline_timestamp:
            return 0.0
        
        old_records = [r for r in records if r.timestamp < self.baseline_timestamp]
        new_records = [r for r in records if r.timestamp >= self.baseline_timestamp]
        
        if not old_records or not new_records:
            return 0.0
        
        old_avg_value = sum(r.actual_value for r in old_records) / len(old_records)
        new_avg_value = sum(r.actual_value for r in new_records) / len(new_records)
        
        return abs(new_avg_value - old_avg_value)
    
    def set_baseline(self):
        """Set current metrics as baseline for drift calculation."""
        self.baseline_metrics = self.calculate_metrics()
        self.baseline_timestamp = datetime.utcnow()
    
    def get_accuracy_report(self) -> Dict:
        """Generate comprehensive accuracy report."""
        current_metrics = self.calculate_metrics()
        
        report = {
            "timestamp": datetime.utcnow().isoformat(),
            "total_records": len(self.records),
            "current_metrics": {
                "mae": current_metrics.mae,
                "rmse": current_metrics.rmse,
                "calibration_error": current_metrics.calibration_error,
                "brier_score": current_metrics.brier_score,
                "accuracy": current_metrics.accuracy,
                "precision": current_metrics.precision,
                "recall": current_metrics.recall,
                "f1_score": current_metrics.f1_score,
                "sample_size": current_metrics.sample_size
            },
            "per_type_metrics": current_metrics.per_type_metrics,
            "drift_metrics": {
                "prediction_drift": current_metrics.prediction_drift,
                "value_drift": current_metrics.value_drift,
                "baseline_timestamp": self.baseline_timestamp.isoformat() if self.baseline_timestamp else None
            }
        }
        
        if self.baseline_metrics:
            report["baseline_metrics"] = {
                "mae": self.baseline_metrics.mae,
                "accuracy": self.baseline_metrics.accuracy,
                "sample_size": self.baseline_metrics.sample_size
            }
            
            # Calculate improvement
            report["improvement"] = {
                "mae_improvement": self.baseline_metrics.mae - current_metrics.mae,
                "accuracy_improvement": current_metrics.accuracy - self.baseline_metrics.accuracy
            }
        
        return report
    
    def export_records(self, filepath: str):
        """Export prediction records to JSON file."""
        records_data = []
        for record in self.records:
            records_data.append({
                "record_id": record.record_id,
                "intervention_type": record.intervention_type,
                "predicted_value": record.predicted_value,
                "predicted_probability": record.predicted_probability,
                "actual_value": record.actual_value,
                "actual_success": record.actual_success,
                "timestamp": record.timestamp.isoformat(),
                "developer_id": record.developer_id,
                "asset_category": record.asset_category,
                "effort_days": record.effort_days
            })
        
        with open(filepath, 'w') as f:
            json.dump(records_data, f, indent=2)
    
    def load_records_from_ledger(self, ledger) -> int:
        """Load prediction records from Outcome Ledger."""
        import sqlite3
        
        conn = sqlite3.connect(ledger.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT record_id, intervention_type, predicted_value, 
                   outcome_metrics, verification_status
            FROM interventions
            WHERE verification_status = 'verified'
        """)
        
        rows = cursor.fetchall()
        loaded_count = 0
        
        for row in rows:
            record_id, intv_type, predicted_value, outcome_metrics_json, verification_status = row
            
            if not outcome_metrics_json:
                continue
            
            try:
                outcome_metrics = json.loads(outcome_metrics_json)
                actual_value = outcome_metrics.get("actual_value", 0.0)
                actual_success = outcome_metrics.get("success", False)
                
                # Estimate predicted probability from predicted_value
                predicted_probability = min(1.0, max(0.0, predicted_value / 100.0))
                
                record = PredictionRecord(
                    record_id=record_id,
                    intervention_type=intv_type,
                    predicted_value=predicted_value,
                    predicted_probability=predicted_probability,
                    actual_value=actual_value,
                    actual_success=actual_success,
                    timestamp=datetime.utcnow(),
                    developer_id="unknown"
                )
                
                self.add_record(record)
                loaded_count += 1
            except (json.JSONDecodeError, KeyError):
                continue
        
        conn.close()
        return loaded_count
