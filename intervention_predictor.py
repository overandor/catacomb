#!/usr/bin/env python3
"""
Intervention Prediction Model - ML model for predicting intervention outcomes.

Trains on verified intervention-outcome pairs from the outcome ledger.
Predicts:
- Expected value creation
- Success probability
- Risk level
- Effort required
"""

import sqlite3
import json
import numpy as np
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum

# Try to import sklearn, fall back to simple heuristics if not available
try:
    from sklearn.ensemble import RandomForestRegressor, GradientBoostingClassifier
    from sklearn.preprocessing import StandardScaler, LabelEncoder
    from sklearn.model_selection import train_test_split, cross_val_score
    from sklearn.metrics import mean_squared_error, accuracy_score, classification_report
    SKLEARN_AVAILABLE = True
except ImportError:
    SKLEARN_AVAILABLE = False


class InterventionType(Enum):
    """Types of interventions."""
    PERFORMANCE_OPTIMIZATION = "performance_optimization"
    SECURITY_HARDENING = "security_hardening"
    DOCUMENTATION = "documentation"
    REFACTORING = "refactoring"
    FEATURE_ADDITION = "feature_addition"
    BUG_FIX = "bug_fix"
    DEPENDENCY_UPDATE = "dependency_update"
    TESTING = "testing"
    CI_CD = "ci_cd"
    MONITORING = "monitoring"


@dataclass
class InterventionFeatures:
    """Features for intervention prediction."""
    # Asset features
    asset_age_days: float
    stars: float
    forks: float
    open_issues: float
    contributors: float
    commit_frequency: float
    
    # Intervention features
    intervention_type: str
    planned_effort_days: float
    
    # Context features
    is_first_intervention: bool
    previous_success_rate: float
    developer_experience: float


@dataclass
class InterventionPrediction:
    """Prediction for an intervention."""
    predicted_value: float  # Expected value created
    success_probability: float  # 0-1
    risk_level: float  # 0-1
    effort_required: float  # Days
    confidence: float  # 0-1
    recommended: bool  # Whether to proceed


class InterventionPredictor:
    """ML model for predicting intervention outcomes."""
    
    def __init__(self, db_path: str = "outcome_ledger.db"):
        self.db_path = db_path
        self.value_model = None
        self.success_model = None
        self.risk_model = None
        self.scaler = None
        self.label_encoders = {}
        self.is_trained = False
        
    def _load_training_data(self) -> Tuple[List[InterventionFeatures], List[Dict]]:
        """Load verified interventions for training."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT 
                before_state,
                intervention_type,
                planned_effort_days,
                predicted_value,
                predicted_probability,
                predicted_risk,
                outcome_metrics,
                prediction_accuracy
            FROM interventions
            WHERE status = 'verified'
            AND outcome_metrics IS NOT NULL
        """)
        
        rows = cursor.fetchall()
        conn.close()
        
        features = []
        targets = []
        
        for row in rows:
            before_state = json.loads(row[0])
            outcome_metrics = json.loads(row[6]) if row[6] else {}
            
            # Extract features
            feature = InterventionFeatures(
                asset_age_days=before_state.get('age_days', 0),
                stars=before_state.get('stars', 0),
                forks=before_state.get('forks', 0),
                open_issues=before_state.get('open_issues', 0),
                contributors=before_state.get('contributors', 0),
                commit_frequency=before_state.get('commit_frequency', 0),
                intervention_type=row[1],
                planned_effort_days=row[2] or 0,
                is_first_intervention=before_state.get('is_first_intervention', False),
                previous_success_rate=before_state.get('previous_success_rate', 0.5),
                developer_experience=before_state.get('developer_experience', 0.5)
            )
            
            # Extract targets
            actual_value = outcome_metrics.get('value_created', row[3] or 0)
            actual_success = 1.0 if outcome_metrics.get('success', True) else 0.0
            actual_risk = outcome_metrics.get('risk', row[5] or 0.5)
            
            features.append(feature)
            targets.append({
                'value': actual_value,
                'success': actual_success,
                'risk': actual_risk
            })
        
        return features, targets
    
    def _features_to_array(self, features: List[InterventionFeatures]) -> np.ndarray:
        """Convert features to numpy array for ML."""
        X = []
        for f in features:
            row = [
                f.asset_age_days,
                f.stars,
                f.forks,
                f.open_issues,
                f.contributors,
                f.commit_frequency,
                f.planned_effort_days,
                1.0 if f.is_first_intervention else 0.0,
                f.previous_success_rate,
                f.developer_experience
            ]
            X.append(row)
        
        return np.array(X)
    
    def _encode_intervention_type(self, features: List[InterventionFeatures]) -> List[InterventionFeatures]:
        """Encode intervention type as numeric."""
        types = [f.intervention_type for f in features]
        if 'intervention_type' not in self.label_encoders:
            self.label_encoders['intervention_type'] = LabelEncoder()
            self.label_encoders['intervention_type'].fit(types)
        
        encoded = self.label_encoders['intervention_type'].transform(types)
        
        for i, f in enumerate(features):
            f.intervention_type = str(encoded[i])
        
        return features
    
    def train(self):
        """Train prediction models on verified outcomes."""
        features, targets = self._load_training_data()
        
        if len(features) < 10:
            print(f"Insufficient training data: {len(features)} samples")
            return False
        
        # Encode categorical features
        features = self._encode_intervention_type(features)
        
        # Convert to arrays
        X = self._features_to_array(features)
        y_value = np.array([t['value'] for t in targets])
        y_success = np.array([t['success'] for t in targets])
        y_risk = np.array([t['risk'] for t in targets])
        
        # Scale features
        self.scaler = StandardScaler()
        X_scaled = self.scaler.fit_transform(X)
        
        if SKLEARN_AVAILABLE:
            # Train value prediction model (regression)
            self.value_model = RandomForestRegressor(
                n_estimators=100,
                max_depth=10,
                random_state=42
            )
            self.value_model.fit(X_scaled, y_value)
            
            # Train success prediction model (classification)
            self.success_model = GradientBoostingClassifier(
                n_estimators=100,
                max_depth=5,
                random_state=42
            )
            self.success_model.fit(X_scaled, y_success)
            
            # Train risk prediction model (regression)
            self.risk_model = RandomForestRegressor(
                n_estimators=100,
                max_depth=10,
                random_state=42
            )
            self.risk_model.fit(X_scaled, y_risk)
            
            # Evaluate models
            value_score = self.value_model.score(X_scaled, y_value)
            success_score = self.success_model.score(X_scaled, y_success)
            risk_score = self.risk_model.score(X_scaled, y_risk)
            
            print(f"Model training complete:")
            print(f"  Value model R²: {value_score:.3f}")
            print(f"  Success model accuracy: {success_score:.3f}")
            print(f"  Risk model R²: {risk_score:.3f}")
        else:
            # Simple heuristic models
            self.value_model = np.mean(y_value)
            self.success_model = np.mean(y_success)
            self.risk_model = np.mean(y_risk)
            print("Using heuristic models (sklearn not available)")
        
        self.is_trained = True
        return True
    
    def predict(self, features: InterventionFeatures) -> InterventionPrediction:
        """Predict outcome for an intervention."""
        if not self.is_trained:
            self.train()
        
        if not self.is_trained:
            # Return default prediction if training failed
            return InterventionPrediction(
                predicted_value=0.0,
                success_probability=0.5,
                risk_level=0.5,
                effort_required=features.planned_effort_days,
                confidence=0.0,
                recommended=False
            )
        
        # Encode and scale features
        features = self._encode_intervention_type([features])[0]
        X = self._features_to_array([features])
        X_scaled = self.scaler.transform(X)
        
        if SKLEARN_AVAILABLE:
            # Make predictions
            predicted_value = self.value_model.predict(X_scaled)[0]
            success_prob = self.success_model.predict_proba(X_scaled)[0][1]
            risk_level = self.risk_model.predict(X_scaled)[0]
            
            # Calculate confidence based on model agreement
            confidence = min(success_prob, 1 - risk_level)
            
            # Recommend if high value, high success, low risk
            recommended = (predicted_value > 1000 and 
                          success_prob > 0.7 and 
                          risk_level < 0.3)
        else:
            # Use heuristics
            predicted_value = self.value_model
            success_prob = self.success_model
            risk_level = self.risk_model
            confidence = 0.5
            recommended = success_prob > 0.6
        
        return InterventionPrediction(
            predicted_value=max(0, predicted_value),
            success_probability=success_prob,
            risk_level=max(0, min(1, risk_level)),
            effort_required=features.planned_effort_days,
            confidence=confidence,
            recommended=recommended
        )
    
    def predict_from_asset(self, asset_data: Dict, intervention_type: str, 
                          planned_effort_days: float) -> InterventionPrediction:
        """Predict outcome from asset data."""
        features = InterventionFeatures(
            asset_age_days=asset_data.get('age_days', 0),
            stars=asset_data.get('stars', 0),
            forks=asset_data.get('forks', 0),
            open_issues=asset_data.get('open_issues', 0),
            contributors=asset_data.get('contributors', 0),
            commit_frequency=asset_data.get('commit_frequency', 0),
            intervention_type=intervention_type,
            planned_effort_days=planned_effort_days,
            is_first_intervention=asset_data.get('is_first_intervention', False),
            previous_success_rate=asset_data.get('previous_success_rate', 0.5),
            developer_experience=asset_data.get('developer_experience', 0.5)
        )
        
        return self.predict(features)
    
    def get_feature_importance(self) -> Dict[str, float]:
        """Get feature importance from trained models."""
        if not SKLEARN_AVAILABLE or not self.is_trained:
            return {}
        
        feature_names = [
            'asset_age_days',
            'stars',
            'forks',
            'open_issues',
            'contributors',
            'commit_frequency',
            'planned_effort_days',
            'is_first_intervention',
            'previous_success_rate',
            'developer_experience'
        ]
        
        importance = dict(zip(feature_names, self.value_model.feature_importances_))
        return dict(sorted(importance.items(), key=lambda x: x[1], reverse=True))


# Singleton instance
_predictor_instance = None

def get_predictor(db_path: str = "outcome_ledger.db") -> InterventionPredictor:
    """Get singleton predictor instance."""
    global _predictor_instance
    if _predictor_instance is None:
        _predictor_instance = InterventionPredictor(db_path)
    return _predictor_instance


if __name__ == "__main__":
    # Test the predictor
    predictor = get_predictor()
    predictor.train()
    
    # Test prediction
    test_asset = {
        'age_days': 365,
        'stars': 1000,
        'forks': 200,
        'open_issues': 50,
        'contributors': 20,
        'commit_frequency': 5.0,
        'is_first_intervention': False,
        'previous_success_rate': 0.8,
        'developer_experience': 0.7
    }
    
    prediction = predictor.predict_from_asset(
        test_asset,
        InterventionType.PERFORMANCE_OPTIMIZATION.value,
        planned_effort_days=5
    )
    
    print(f"\nPrediction:")
    print(f"  Expected value: ${prediction.predicted_value:.2f}")
    print(f"  Success probability: {prediction.success_probability:.1%}")
    print(f"  Risk level: {prediction.risk_level:.1%}")
    print(f"  Confidence: {prediction.confidence:.1%}")
    print(f"  Recommended: {prediction.recommended}")
    
    print(f"\nFeature importance:")
    for feat, imp in predictor.get_feature_importance().items():
        print(f"  {feat}: {imp:.3f}")
