"""Intervention ML Agent - Predicts intervention value, not repo popularity."""
from typing import Dict, Any, List
import numpy as np
from base_agent import BaseAgent, AgentOutput


class InterventionMLAgent(BaseAgent):
    """ML model for predicting intervention value creation."""
    
    def __init__(self, model_path: str = None):
        super().__init__("InterventionML")
        self.model_path = model_path
        self.model = None
        self._load_model()
    
    def _load_model(self):
        """Load trained intervention model."""
        # Placeholder for model loading
        self.model = "heuristic"
    
    def _extract_intervention_features(self, repo_data: Dict[str, Any], intervention_type: str) -> np.ndarray:
        """Extract features for intervention prediction."""
        features = []
        
        # Repo state features
        features.append(repo_data.get("stars", 0))
        features.append(repo_data.get("forks", 0))
        features.append(repo_data.get("open_issues", 0))
        features.append(repo_data.get("contributors", 0))
        features.append(repo_data.get("commits_last_year", 0))
        
        # Quality signals
        features.append(1 if repo_data.get("has_readme", False) else 0)
        features.append(1 if repo_data.get("has_ci", False) else 0)
        features.append(1 if repo_data.get("has_tests", False) else 0)
        features.append(1 if repo_data.get("has_dockerfile", False) else 0)
        
        # Abandonment signals
        features.append(repo_data.get("days_since_last_commit", 365))
        features.append(1 if repo_data.get("archived", False) else 0)
        
        # Language ecosystem
        language = repo_data.get("language", "").lower()
        language_ecosystem_score = self._get_language_ecosystem_score(language)
        features.append(language_ecosystem_score)
        
        # Intervention type one-hot
        intervention_types = [
            "documentation", "build_system", "feature_expansion", 
            "saas_conversion", "ai_integration", "infrastructure_repositioning",
            "community_building", "modernization", "packaging", "momentum_amplification"
        ]
        for it in intervention_types:
            features.append(1 if intervention_type == it else 0)
        
        # Intervention-repo fit
        fit_score = self._calculate_intervention_fit(repo_data, intervention_type)
        features.append(fit_score)
        
        return np.array(features, dtype=np.float32)
    
    def _get_language_ecosystem_score(self, language: str) -> float:
        """Get ecosystem score for language (proxy for intervention potential)."""
        ecosystem_scores = {
            "rust": 0.9,
            "go": 0.85,
            "typescript": 0.8,
            "python": 0.75,
            "javascript": 0.7,
            "java": 0.65,
            "c++": 0.6,
            "ruby": 0.55
        }
        return ecosystem_scores.get(language, 0.5)
    
    def _calculate_intervention_fit(self, repo_data: Dict[str, Any], intervention_type: str) -> float:
        """Calculate how well intervention fits repo state."""
        fit = 0.5  # Default
        
        stars = repo_data.get("stars", 0)
        has_readme = repo_data.get("has_readme", False)
        has_ci = repo_data.get("has_ci", False)
        has_tests = repo_data.get("has_tests", False)
        contributors = repo_data.get("contributors", 0)
        
        if intervention_type == "documentation":
            if not has_readme:
                fit = 0.9
            elif stars < 100:
                fit = 0.7
            else:
                fit = 0.3
        
        elif intervention_type == "build_system":
            if not has_ci:
                fit = 0.85
            elif not has_tests:
                fit = 0.7
            else:
                fit = 0.4
        
        elif intervention_type == "feature_expansion":
            if contributors > 0:
                fit = 0.8
            elif stars > 10:
                fit = 0.6
            else:
                fit = 0.4
        
        elif intervention_type == "saas_conversion":
            if stars > 100 and contributors > 2:
                fit = 0.7
            else:
                fit = 0.3
        
        elif intervention_type == "ai_integration":
            language = repo_data.get("language", "").lower()
            if language in ["python", "typescript", "rust"]:
                fit = 0.8
            else:
                fit = 0.4
        
        elif intervention_type == "packaging":
            language = repo_data.get("language", "").lower()
            if language in ["rust", "python", "javascript"]:
                fit = 0.8
            else:
                fit = 0.5
        
        elif intervention_type == "momentum_amplification":
            commits_last_year = repo_data.get("commits_last_year", 0)
            if commits_last_year > 50:
                fit = 0.9
            else:
                fit = 0.3
        
        return fit
    
    def _predict_intervention_value_heuristic(self, features: np.ndarray, intervention_type: str) -> float:
        """Heuristic-based intervention value prediction."""
        # Extract key features
        stars = features[0]
        forks = features[1]
        issues = features[2]
        contributors = features[3]
        has_readme = features[5]
        has_ci = features[6]
        has_tests = features[7]
        days_since_commit = features[9]
        language_ecosystem = features[11]
        intervention_fit = features[22]
        
        value = 0.0
        
        # Base value from intervention fit
        value += intervention_fit * 0.4
        
        # Language ecosystem multiplier
        value += language_ecosystem * 0.2
        
        # Underserved repos (low stars, high potential)
        if stars < 100 and contributors > 0:
            value += 0.15
        elif stars < 10 and has_readme:
            value += 0.1
        
        # Missing critical infrastructure
        if not has_ci and contributors > 0:
            value += 0.1
        if not has_tests and stars > 10:
            value += 0.1
        
        # Issue engagement (actual users)
        if issues > 10 and stars < 100:
            value += 0.1
        elif issues > 50:
            value += 0.15
        
        # Abandoned but valuable
        if days_since_commit > 180 and stars > 10:
            value += 0.15
        
        # Intervention-specific boosts
        if intervention_type == "documentation" and not has_readme:
            value += 0.1
        if intervention_type == "build_system" and not has_ci:
            value += 0.15
        if intervention_type == "packaging" and language_ecosystem > 0.7:
            value += 0.1
        
        return min(value, 1.0)
    
    def predict_intervention_value(self, repo_data: Dict[str, Any], intervention_type: str) -> float:
        """
        Predict value creation for specific intervention.
        
        Returns:
            Expected value creation (0-1)
        """
        features = self._extract_intervention_features(repo_data, intervention_type)
        
        if self.model == "heuristic":
            value = self._predict_intervention_value_heuristic(features, intervention_type)
        else:
            value = self._predict_intervention_value_heuristic(features, intervention_type)  # Fallback
        
        return round(value, 3)
    
    def rank_interventions(self, repo_data: Dict[str, Any], interventions: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Rank interventions by predicted value creation.
        
        Args:
            repo_data: Repository data
            interventions: List of intervention dicts with 'name' field
        
        Returns:
            Ranked interventions with added 'predicted_value' field
        """
        for intervention in interventions:
            intervention_name = intervention.get("name", "").lower().replace(" ", "_")
            predicted_value = self.predict_intervention_value(repo_data, intervention_name)
            intervention["predicted_value"] = predicted_value
        
        # Sort by predicted value
        ranked = sorted(interventions, key=lambda x: x["predicted_value"], reverse=True)
        
        return ranked
    
    def analyze(self, repo_data: Dict[str, Any], opportunity_data: Dict[str, Any] = None) -> AgentOutput:
        """
        Analyze repo for intervention potential.
        
        Args:
            repo_data: Repository data from GitHub API
            opportunity_data: Real opportunity data from OpportunityLayer (required)
        """
        if opportunity_data is None:
            raise ValueError("opportunity_data is required - no mock data allowed")
        
        # Get standard interventions
        from layers import StrategyLayer
        strategy_layer = StrategyLayer()
        
        # Generate interventions using real opportunity data
        strategy_output = strategy_layer._generate_intervention_paths(
            repo_data, 
            opportunity_data, 
            type('obj', (object,), {'evidence': {
                'revival': {'underexposure': {'underexposure_signal': 0.5}},
                'transformation': {'transformation_potential': 0.5},
                'risk': {'risk_penalty': 0.5}
            }})()
        )
        
        # Rank interventions
        ranked_interventions = self.rank_interventions(repo_data, strategy_output)
        
        evidence = {
            "ranked_interventions": ranked_interventions[:5],  # Top 5
            "intervention_count": len(ranked_interventions),
            "model_type": self.model
        }
        
        # Overall intervention potential
        if ranked_interventions:
            avg_value = sum(i["predicted_value"] for i in ranked_interventions[:5]) / min(5, len(ranked_interventions))
            intervention_score = avg_value * 100
        else:
            intervention_score = 0
        
        confidence = 0.7 if self.model == "heuristic" else 0.9
        
        return AgentOutput(
            score=round(intervention_score, 2),
            evidence=evidence,
            confidence=confidence,
            hash=""
        )


class InterventionOutcomeDataset:
    """Dataset for intervention-outcome pairs."""
    
    def __init__(self):
        self.data = []
    
    def add_intervention_outcome(
        self,
        repo_before: Dict[str, Any],
        intervention: str,
        repo_after: Dict[str, Any],
        outcome_metrics: Dict[str, float]
    ):
        """
        Add intervention-outcome pair to dataset.
        
        Args:
            repo_before: Repo state before intervention
            intervention: Type of intervention applied
            repo_after: Repo state after intervention
            outcome_metrics: Measured outcomes (star_growth, contributor_growth, etc.)
        """
        self.data.append({
            "repo_before": repo_before,
            "intervention": intervention,
            "repo_after": repo_after,
            "outcome_metrics": outcome_metrics
        })
    
    def get_training_examples(self) -> List[Dict[str, Any]]:
        """Get training examples for intervention model."""
        training_data = []
        
        for example in self.data:
            features = self._extract_features(example["repo_before"], example["intervention"])
            labels = example["outcome_metrics"]
            
            training_data.append({
                "features": features,
                "labels": labels,
                "intervention": example["intervention"]
            })
        
        return training_data
    
    def _extract_features(self, repo_data: Dict[str, Any], intervention: str) -> np.ndarray:
        """Extract features (same as InterventionMLAgent)."""
        agent = InterventionMLAgent()
        return agent._extract_intervention_features(repo_data, intervention)


class InterventionModelTrainer:
    """Train model on intervention-outcome data."""
    
    def __init__(self):
        self.model = None
    
    def train(self, training_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Train intervention value prediction model.
        
        Args:
            training_data: List of intervention-outcome examples
        
        Returns:
            Training metrics
        """
        import sklearn
        from sklearn.ensemble import RandomForestRegressor
        from sklearn.model_selection import train_test_split
        from sklearn.metrics import mean_squared_error, r2_score
        
        # Prepare data
        X = np.array([item["features"] for item in training_data])
        
        # Multiple outcome metrics
        y_star_growth = np.array([item["labels"].get("star_growth", 0) for item in training_data])
        y_contributor_growth = np.array([item["labels"].get("contributor_growth", 0) for item in training_data])
        y_adoption = np.array([item["labels"].get("adoption", 0) for item in training_data])
        
        # Combined value score
        y_value = (y_star_growth + y_contributor_growth + y_adoption) / 3
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y_value, test_size=0.2, random_state=42
        )
        
        # Train model
        model = RandomForestRegressor(n_estimators=100, random_state=42)
        model.fit(X_train, y_train)
        
        # Evaluate
        y_pred = model.predict(X_test)
        
        metrics = {
            "mse": mean_squared_error(y_test, y_pred),
            "r2": r2_score(y_test, y_pred)
        }
        
        self.model = model
        
        return metrics
    
    def save_model(self, path: str):
        """Save trained model."""
        import joblib
        joblib.dump(self.model, path)
    
    def load_model(self, path: str):
        """Load trained model."""
        import joblib
        self.model = joblib.load(path)
