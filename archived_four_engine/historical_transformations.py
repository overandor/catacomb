"""Historical transformation dataset for training intervention models."""
from typing import Dict, Any, List
from datetime import datetime
import json


class HistoricalTransformation:
    """Represents a historical repo transformation (before → intervention → after)."""
    
    def __init__(
        self,
        repo_id: str,
        before_state: Dict[str, Any],
        intervention: str,
        intervention_date: str,
        after_state: Dict[str, Any],
        outcome_metrics: Dict[str, float],
        metadata: Dict[str, Any] = None
    ):
        self.repo_id = repo_id
        self.before_state = before_state
        self.intervention = intervention
        self.intervention_date = intervention_date
        self.after_state = after_state
        self.outcome_metrics = outcome_metrics
        self.metadata = metadata or {}
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "repo_id": self.repo_id,
            "before_state": self.before_state,
            "intervention": self.intervention,
            "intervention_date": self.intervention_date,
            "after_state": self.after_state,
            "outcome_metrics": self.outcome_metrics,
            "metadata": self.metadata
        }


class HistoricalTransformationDataset:
    """Dataset of historical transformations for ML training."""
    
    def __init__(self):
        self.transformations: List[HistoricalTransformation] = []
    
    def add_transformation(self, transformation: HistoricalTransformation):
        """Add a transformation to the dataset."""
        self.transformations.append(transformation)
    
    def get_training_examples(self) -> List[Dict[str, Any]]:
        """Get training examples for intervention model."""
        training_data = []
        
        for transformation in self.transformations:
            # Extract features from before state
            features = self._extract_features(
                transformation.before_state,
                transformation.intervention
            )
            
            # Labels from outcome metrics
            labels = transformation.outcome_metrics
            
            training_data.append({
                "repo_id": transformation.repo_id,
                "features": features,
                "labels": labels,
                "intervention": transformation.intervention,
                "metadata": transformation.metadata
            })
        
        return training_data
    
    def _extract_features(self, repo_state: Dict[str, Any], intervention: str) -> List[float]:
        """Extract features from repo state (compatible with InterventionMLAgent)."""
        from intervention_ml_agent import InterventionMLAgent
        agent = InterventionMLAgent()
        return agent._extract_intervention_features(repo_state, intervention).tolist()
    
    def save(self, filepath: str):
        """Save dataset to file."""
        data = [t.to_dict() for t in self.transformations]
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)
    
    def load(self, filepath: str):
        """Load dataset from file."""
        with open(filepath, 'r') as f:
            data = json.load(f)
        
        self.transformations = [
            HistoricalTransformation(
                item["repo_id"],
                item["before_state"],
                item["intervention"],
                item["intervention_date"],
                item["after_state"],
                item["outcome_metrics"],
                item.get("metadata", {})
            )
            for item in data
        ]


# Example historical transformations (for documentation and testing)
EXAMPLE_TRANSFORMATIONS = [
    {
        "repo_id": "vercel/next.js",
        "before_state": {
            "stars": 500,
            "forks": 50,
            "open_issues": 20,
            "contributors": 5,
            "commits_last_year": 100,
            "has_readme": True,
            "has_ci": False,
            "has_tests": False,
            "has_dockerfile": False,
            "days_since_last_commit": 30,
            "archived": False,
            "language": "JavaScript",
            "has_package_manager": True,
            "has_api": False,
            "is_library": True,
            "has_examples": False
        },
        "intervention": "feature_expansion",
        "intervention_date": "2016-10-25",
        "after_state": {
            "stars": 120000,
            "forks": 25000,
            "open_issues": 1500,
            "contributors": 2000,
            "commits_last_year": 5000
        },
        "outcome_metrics": {
            "star_growth": 23900.0,  # 500 → 120,000 over years
            "contributor_growth": 400.0,
            "adoption": 0.95,
            "ecosystem_impact": 0.98
        },
        "metadata": {
            "category": "framework",
            "became_startup": True,
            "funding": "Series D",
            "notes": "Added SSR, API routes, image optimization"
        }
    },
    {
        "repo_id": "supabase/supabase",
        "before_state": {
            "stars": 1000,
            "forks": 100,
            "open_issues": 50,
            "contributors": 20,
            "commits_last_year": 200,
            "has_readme": True,
            "has_ci": True,
            "has_tests": True,
            "has_dockerfile": True,
            "days_since_last_commit": 7,
            "archived": False,
            "language": "TypeScript",
            "has_package_manager": True,
            "has_api": True,
            "is_library": True,
            "has_examples": True
        },
        "intervention": "saas_conversion",
        "intervention_date": "2020-01-01",
        "after_state": {
            "stars": 65000,
            "forks": 5000,
            "open_issues": 800,
            "contributors": 800,
            "commits_last_year": 3000
        },
        "outcome_metrics": {
            "star_growth": 65.0,
            "contributor_growth": 40.0,
            "adoption": 0.92,
            "ecosystem_impact": 0.95
        },
        "metadata": {
            "category": "database",
            "became_startup": True,
            "funding": "Series B",
            "notes": "Open source Firebase alternative with managed service"
        }
    },
    {
        "repo_id": "langchain-ai/langchain",
        "before_state": {
            "stars": 100,
            "forks": 10,
            "open_issues": 5,
            "contributors": 3,
            "commits_last_year": 50,
            "has_readme": True,
            "has_ci": False,
            "has_tests": False,
            "has_dockerfile": False,
            "days_since_last_commit": 14,
            "archived": False,
            "language": "Python",
            "has_package_manager": True,
            "has_api": True,
            "is_library": True,
            "has_examples": True
        },
        "intervention": "ai_integration",
        "intervention_date": "2022-10-01",
        "after_state": {
            "stars": 85000,
            "forks": 12000,
            "open_issues": 2000,
            "contributors": 1500,
            "commits_last_year": 4000
        },
        "outcome_metrics": {
            "star_growth": 850.0,
            "contributor_growth": 500.0,
            "adoption": 0.97,
            "ecosystem_impact": 0.99
        },
        "metadata": {
            "category": "ai",
            "became_startup": True,
            "funding": "Series A",
            "notes": "LLM framework for building AI applications"
        }
    },
    {
        "repo_id": "tiangolo/fastapi",
        "before_state": {
            "stars": 50,
            "forks": 5,
            "open_issues": 3,
            "contributors": 2,
            "commits_last_year": 30,
            "has_readme": True,
            "has_ci": True,
            "has_tests": True,
            "has_dockerfile": False,
            "days_since_last_commit": 10,
            "archived": False,
            "language": "Python",
            "has_package_manager": True,
            "has_api": True,
            "is_library": True,
            "has_examples": True
        },
        "intervention": "documentation",
        "intervention_date": "2018-12-01",
        "after_state": {
            "stars": 75000,
            "forks": 6000,
            "open_issues": 500,
            "contributors": 400,
            "commits_last_year": 800
        },
        "outcome_metrics": {
            "star_growth": 1500.0,
            "contributor_growth": 200.0,
            "adoption": 0.94,
            "ecosystem_impact": 0.96
        },
        "metadata": {
            "category": "web",
            "became_startup": False,
            "funding": None,
            "notes": "Modern Python web framework with async support"
        }
    },
    {
        "repo_id": "oven-sh/bun",
        "before_state": {
            "stars": 200,
            "forks": 20,
            "open_issues": 10,
            "contributors": 5,
            "commits_last_year": 100,
            "has_readme": True,
            "has_ci": True,
            "has_tests": True,
            "has_dockerfile": False,
            "days_since_last_commit": 5,
            "archived": False,
            "language": "Zig",
            "has_package_manager": True,
            "has_api": True,
            "is_library": True,
            "has_examples": True
        },
        "intervention": "momentum_amplification",
        "intervention_date": "2022-07-01",
        "after_state": {
            "stars": 70000,
            "forks": 2000,
            "open_issues": 600,
            "contributors": 300,
            "commits_last_year": 2000
        },
        "outcome_metrics": {
            "star_growth": 350.0,
            "contributor_growth": 60.0,
            "adoption": 0.91,
            "ecosystem_impact": 0.93
        },
        "metadata": {
            "category": "runtime",
            "became_startup": True,
            "funding": "Series A",
            "notes": "JavaScript runtime written in Zig"
        }
    }
]


def load_example_dataset() -> HistoricalTransformationDataset:
    """Load example historical transformations."""
    dataset = HistoricalTransformationDataset()
    
    for example in EXAMPLE_TRANSFORMATIONS:
        transformation = HistoricalTransformation(
            example["repo_id"],
            example["before_state"],
            example["intervention"],
            example["intervention_date"],
            example["after_state"],
            example["outcome_metrics"],
            example.get("metadata", {})
        )
        dataset.add_transformation(transformation)
    
    return dataset


def create_transformation_from_github_history(
    repo_id: str,
    before_date: str,
    after_date: str,
    intervention: str
) -> HistoricalTransformation:
    """
    Create a transformation from GitHub history (placeholder for actual implementation).
    
    This would:
    1. Fetch repo state at before_date via GitHub API
    2. Fetch repo state at after_date via GitHub API
    3. Calculate outcome metrics from the difference
    4. Return a HistoricalTransformation object
    
    Requires GitHub API with historical data access.
    """
    # Placeholder - would implement actual GitHub API calls
    pass
