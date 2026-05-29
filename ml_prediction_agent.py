"""ML-based prediction agent for repo virality and usefulness."""
from typing import Dict, Any, List
import numpy as np
from base_agent import BaseAgent, AgentOutput


class MLPredictionAgent(BaseAgent):
    """ML model for predicting repo virality and usefulness."""
    
    def __init__(self, model_path: str = None):
        super().__init__("MLPrediction")
        self.model_path = model_path
        self.model = None
        self._load_model()
    
    def _load_model(self):
        """Load trained ML model."""
        # Placeholder for model loading
        # In production, this would load a trained model from disk
        # For now, we'll use a heuristic-based approach
        self.model = "heuristic"
    
    def _extract_features(self, repo_data: Dict[str, Any]) -> np.ndarray:
        """Extract features from repo data for ML prediction."""
        features = []
        
        # Basic metrics
        features.append(repo_data.get("stars", 0))
        features.append(repo_data.get("forks", 0))
        features.append(repo_data.get("open_issues", 0))
        features.append(repo_data.get("watchers", 0))
        features.append(repo_data.get("subscribers", 0))
        
        # Activity metrics
        features.append(repo_data.get("commits_last_year", 0))
        features.append(repo_data.get("contributors", 0))
        features.append(repo_data.get("releases", 0))
        
        # Size metrics
        features.append(repo_data.get("size", 0))
        
        # Binary features
        features.append(1 if repo_data.get("has_readme", False) else 0)
        features.append(1 if repo_data.get("has_wiki", False) else 0)
        features.append(1 if repo_data.get("has_pages", False) else 0)
        features.append(1 if repo_data.get("has_ci", False) else 0)
        features.append(1 if repo_data.get("has_dockerfile", False) else 0)
        
        # License (one-hot encoded for common licenses)
        license_key = repo_data.get("license", "")
        common_licenses = ["mit", "apache-2.0", "gpl-3.0", "bsd-3-clause"]
        for lic in common_licenses:
            features.append(1 if license_key == lic else 0)
        
        # Language (one-hot encoded for common languages)
        language = repo_data.get("language", "").lower()
        common_languages = ["python", "javascript", "typescript", "rust", "go", "java", "c++", "ruby"]
        for lang in common_languages:
            features.append(1 if language == lang else 0)
        
        # Topic count
        features.append(len(repo_data.get("topics", [])))
        
        # Age metrics (days since creation)
        from datetime import datetime
        created_at = repo_data.get("created_at")
        if created_at:
            try:
                created_date = datetime.fromisoformat(created_at.replace("Z", "+00:00"))
                days_since_creation = (datetime.now(created_date.tzinfo) - created_date).days
                features.append(days_since_creation)
            except:
                features.append(365)
        else:
            features.append(365)
        
        # Fork status
        features.append(1 if repo_data.get("is_fork", False) else 0)
        
        # Archived status
        features.append(1 if repo_data.get("archived", False) else 0)
        
        return np.array(features, dtype=np.float32)
    
    def _predict_virality_heuristic(self, features: np.ndarray) -> float:
        """Heuristic-based virality prediction (placeholder for ML model)."""
        # Extract key features
        stars = features[0]
        forks = features[1]
        issues = features[2]
        commits = features[5]
        contributors = features[6]
        has_readme = features[9]
        has_ci = features[12]
        age_days = features[22]
        
        # Virality score based on growth potential
        virality = 0.0
        
        # High stars + low age = already viral (high score)
        if stars > 1000 and age_days < 365:
            virality += 0.8
        elif stars > 100 and age_days < 180:
            virality += 0.6
        elif stars > 10 and age_days < 90:
            virality += 0.4
        
        # Fork ratio indicates interest
        if stars > 0:
            fork_ratio = forks / stars
            if fork_ratio > 0.5:
                virality += 0.2
            elif fork_ratio > 0.3:
                virality += 0.1
        
        # Active development
        if commits > 50:
            virality += 0.15
        elif commits > 10:
            virality += 0.1
        
        # Multiple contributors
        if contributors > 5:
            virality += 0.1
        elif contributors > 2:
            virality += 0.05
        
        # Documentation and CI
        if has_readme:
            virality += 0.1
        if has_ci:
            virality += 0.1
        
        # Issue engagement
        if issues > 50:
            virality += 0.1
        elif issues > 10:
            virality += 0.05
        
        return min(virality, 1.0)
    
    def _predict_usefulness_heuristic(self, features: np.ndarray) -> float:
        """Heuristic-based usefulness prediction (placeholder for ML model)."""
        # Extract key features
        stars = features[0]
        forks = features[1]
        issues = features[2]
        has_readme = features[9]
        has_ci = features[12]
        has_dockerfile = features[13]
        license_idx = features[14:18]
        language_idx = features[18:26]
        contributors = features[6]
        releases = features[7]
        
        usefulness = 0.0
        
        # Adoption signals
        if stars > 100:
            usefulness += 0.3
        elif stars > 10:
            usefulness += 0.15
        
        if forks > 20:
            usefulness += 0.2
        elif forks > 5:
            usefulness += 0.1
        
        # Maintenance signals
        if contributors > 3:
            usefulness += 0.15
        elif contributors > 1:
            usefulness += 0.08
        
        if releases > 5:
            usefulness += 0.15
        elif releases > 1:
            usefulness += 0.08
        
        # Quality signals
        if has_readme:
            usefulness += 0.1
        if has_ci:
            usefulness += 0.1
        if has_dockerfile:
            usefulness += 0.05
        
        # License (permissive licenses indicate library/utility focus)
        if license_idx[0] == 1 or license_idx[1] == 1:  # MIT or Apache
            usefulness += 0.1
        
        # Language (infrastructure languages indicate utility)
        if language_idx[3] == 1 or language_idx[4] == 1:  # Rust or Go
            usefulness += 0.1
        elif language_idx[6] == 1:  # C++
            usefulness += 0.08
        
        # Issue engagement (indicates actual use)
        if issues > 20:
            usefulness += 0.1
        elif issues > 5:
            usefulness += 0.05
        
        return min(usefulness, 1.0)
    
    def predict(self, repo_data: Dict[str, Any]) -> Dict[str, float]:
        """
        Predict virality and usefulness scores.
        
        Returns:
            Dict with 'virality' and 'usefulness' scores (0-1)
        """
        features = self._extract_features(repo_data)
        
        if self.model == "heuristic":
            virality = self._predict_virality_heuristic(features)
            usefulness = self._predict_usefulness_heuristic(features)
        else:
            # Use actual ML model prediction
            virality = self._predict_virality_heuristic(features)  # Fallback
            usefulness = self._predict_usefulness_heuristic(features)  # Fallback
        
        return {
            "virality": round(virality, 3),
            "usefulness": round(usefulness, 3)
        }
    
    def analyze(self, repo_data: Dict[str, Any]) -> AgentOutput:
        """
        Analyze repo using ML predictions.
        """
        predictions = self.predict(repo_data)
        
        evidence = {
            "virality_score": predictions["virality"],
            "usefulness_score": predictions["usefulness"],
            "model_type": self.model,
            "feature_count": len(self._extract_features(repo_data))
        }
        
        # Combined ML score
        ml_score = (predictions["virality"] + predictions["usefulness"]) / 2
        
        confidence = 0.7 if self.model == "heuristic" else 0.9
        
        return AgentOutput(
            score=round(ml_score * 100, 2),
            evidence=evidence,
            confidence=confidence,
            hash=""
        )


class ViralityUsefulnessDataset:
    """Dataset collection and management for ML training."""
    
    def __init__(self, github_token: str = None):
        self.github_token = github_token
        self.data = []
    
    def collect_training_data(self, repos: List[str], limit: int = 1000) -> List[Dict[str, Any]]:
        """
        Collect training data from repositories.
        
        Args:
            repos: List of repo identifiers (owner/repo)
            limit: Maximum number of repos to collect
        
        Returns:
            List of training examples with features and labels
        """
        from repo_scanner import RepoScannerAgent
        scanner = RepoScannerAgent(self.github_token)
        
        training_data = []
        
        for repo_id in repos[:limit]:
            try:
                owner, repo = repo_id.split("/")
                repo_data = scanner._get_repo_data(owner, repo)
                
                if "error" not in repo_data:
                    features = self._extract_features(repo_data)
                    labels = self._generate_labels(repo_data)
                    
                    training_data.append({
                        "repo": repo_id,
                        "features": features,
                        "labels": labels,
                        "metadata": repo_data
                    })
            except Exception as e:
                print(f"Error collecting data for {repo_id}: {e}")
                continue
        
        self.data = training_data
        return training_data
    
    def _extract_features(self, repo_data: Dict[str, Any]) -> np.ndarray:
        """Extract features (same as MLPredictionAgent)."""
        agent = MLPredictionAgent()
        return agent._extract_features(repo_data)
    
    def _generate_labels(self, repo_data: Dict[str, Any]) -> Dict[str, float]:
        """
        Generate training labels based on historical performance.
        
        Labels:
        - virality: 0-1 score based on star growth rate
        - usefulness: 0-1 score based on adoption and maintenance
        """
        stars = repo_data.get("stars", 0)
        forks = repo_data.get("forks", 0)
        contributors = repo_data.get("contributors", 0)
        age_days = self._get_age_days(repo_data)
        
        # Virality label: star growth rate
        if age_days > 0:
            star_growth_rate = stars / age_days
            virality = min(star_growth_rate * 10, 1.0)  # Normalize
        else:
            virality = 0.0
        
        # Usefulness label: adoption and maintenance
        usefulness = 0.0
        
        if stars > 100:
            usefulness += 0.4
        elif stars > 10:
            usefulness += 0.2
        
        if forks > 20:
            usefulness += 0.3
        elif forks > 5:
            usefulness += 0.15
        
        if contributors > 3:
            usefulness += 0.3
        elif contributors > 1:
            usefulness += 0.15
        
        usefulness = min(usefulness, 1.0)
        
        return {
            "virality": virality,
            "usefulness": usefulness
        }
    
    def _get_age_days(self, repo_data: Dict[str, Any]) -> int:
        """Calculate repository age in days."""
        from datetime import datetime
        created_at = repo_data.get("created_at")
        if created_at:
            try:
                created_date = datetime.fromisoformat(created_at.replace("Z", "+00:00"))
                return (datetime.now(created_date.tzinfo) - created_date).days
            except:
                return 365
        return 365


class ModelTrainer:
    """Train ML models for virality and usefulness prediction."""
    
    def __init__(self):
        self.model = None
    
    def train(self, training_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Train ML model on collected data.
        
        Args:
            training_data: List of training examples with features and labels
        
        Returns:
            Training metrics and model info
        """
        import sklearn
        from sklearn.ensemble import RandomForestRegressor
        from sklearn.model_selection import train_test_split
        from sklearn.metrics import mean_squared_error, r2_score
        
        # Prepare data
        X = np.array([item["features"] for item in training_data])
        y_virality = np.array([item["labels"]["virality"] for item in training_data])
        y_usefulness = np.array([item["labels"]["usefulness"] for item in training_data])
        
        # Split data
        X_train, X_test, y_v_train, y_v_test, y_u_train, y_u_test = train_test_split(
            X, y_virality, y_usefulness, test_size=0.2, random_state=42
        )
        
        # Train models
        virality_model = RandomForestRegressor(n_estimators=100, random_state=42)
        usefulness_model = RandomForestRegressor(n_estimators=100, random_state=42)
        
        virality_model.fit(X_train, y_v_train)
        usefulness_model.fit(X_train, y_u_train)
        
        # Evaluate
        v_pred = virality_model.predict(X_test)
        u_pred = usefulness_model.predict(X_test)
        
        metrics = {
            "virality": {
                "mse": mean_squared_error(y_v_test, v_pred),
                "r2": r2_score(y_v_test, v_pred)
            },
            "usefulness": {
                "mse": mean_squared_error(y_u_test, u_pred),
                "r2": r2_score(y_u_test, u_pred)
            }
        }
        
        self.model = {
            "virality": virality_model,
            "usefulness": usefulness_model
        }
        
        return metrics
    
    def save_model(self, path: str):
        """Save trained model to disk."""
        import joblib
        joblib.dump(self.model, path)
    
    def load_model(self, path: str):
        """Load trained model from disk."""
        import joblib
        self.model = joblib.load(path)
