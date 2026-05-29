"""Innovation Elo system - tracks prediction accuracy for interventions."""
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field
from enum import Enum
import math


class EloEntityType(Enum):
    """Types of entities that can have Elo ratings."""
    DEVELOPER = "developer"
    INTERVENTION_TYPE = "intervention_type"
    ASSET_TYPE = "asset_type"
    PREDICTION_MODEL = "prediction_model"


@dataclass
class EloRating:
    """Elo rating for an entity."""
    entity_id: str
    entity_type: EloEntityType
    rating: float = 1000.0  # Starting Elo
    games_played: int = 0
    wins: int = 0
    losses: int = 0
    draws: int = 0
    history: List[Dict[str, Any]] = field(default_factory=list)
    
    def update_rating(self, new_rating: float, result: str, opponent_rating: float):
        """Update rating after a game."""
        self.rating = new_rating
        self.games_played += 1
        
        if result == "win":
            self.wins += 1
        elif result == "loss":
            self.losses += 1
        else:
            self.draws += 1
        
        self.history.append({
            "new_rating": new_rating,
            "result": result,
            "opponent_rating": opponent_rating,
            "timestamp": self.games_played
        })
    
    def win_rate(self) -> float:
        """Calculate win rate."""
        if self.games_played == 0:
            return 0.0
        return self.wins / self.games_played
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "entity_id": self.entity_id,
            "entity_type": self.entity_type.value,
            "rating": round(self.rating, 2),
            "games_played": self.games_played,
            "wins": self.wins,
            "losses": self.losses,
            "draws": self.draws,
            "win_rate": round(self.win_rate(), 3),
            "history": self.history[-10:]  # Last 10 games
        }


class InnovationElo:
    """
    Elo system for intervention predictions.
    
    Not developer reputation. Not GitHub stars. Not followers.
    
    An Elo system for interventions.
    
    Example:
    - Prediction: Expected Value = 84, Actual Value = 86 → +18 Elo
    - Prediction: Expected Value = 90, Actual Value = 12 → -44 Elo
    
    Now Catacomb learns who consistently predicts value creation.
    """
    
    def __init__(self, k_factor: float = 32.0):
        """
        Initialize Elo system.
        
        Args:
            k_factor: K-factor determines how much ratings change (default 32, like chess)
        """
        self.k_factor = k_factor
        self.ratings: Dict[str, EloRating] = {}
    
    def get_rating(self, entity_id: str, entity_type: EloEntityType) -> EloRating:
        """Get or create rating for an entity."""
        key = f"{entity_type.value}:{entity_id}"
        
        if key not in self.ratings:
            self.ratings[key] = EloRating(
                entity_id=entity_id,
                entity_type=entity_type
            )
        
        return self.ratings[key]
    
    def calculate_expected_score(self, rating_a: float, rating_b: float) -> float:
        """
        Calculate expected score for entity A against entity B.
        
        Formula: E_A = 1 / (1 + 10^((R_B - R_A) / 400))
        """
        return 1.0 / (1.0 + math.pow(10, (rating_b - rating_a) / 400))
    
    def update_rating(
        self,
        entity_id: str,
        entity_type: EloEntityType,
        predicted_value: float,
        actual_value: float,
        opponent_rating: float = 1000.0
    ) -> float:
        """
        Update Elo rating based on prediction accuracy.
        
        Args:
            entity_id: ID of the entity (developer, intervention type, etc.)
            entity_type: Type of entity
            predicted_value: Predicted value (0-100)
            actual_value: Actual value (0-100)
            opponent_rating: Rating of the "opponent" (baseline difficulty)
        
        Returns:
            New Elo rating
        """
        rating = self.get_rating(entity_id, entity_type)
        
        # Calculate prediction error
        error = abs(predicted_value - actual_value)
        
        # Determine result based on error
        # Error < 10: win
        # Error < 20: draw
        # Error >= 20: loss
        if error < 10:
            result = "win"
            actual_score = 1.0
        elif error < 20:
            result = "draw"
            actual_score = 0.5
        else:
            result = "loss"
            actual_score = 0.0
        
        # Calculate expected score
        expected_score = self.calculate_expected_score(rating.rating, opponent_rating)
        
        # Calculate new rating
        new_rating = rating.rating + self.k_factor * (actual_score - expected_score)
        
        # Update rating
        rating.update_rating(new_rating, result, opponent_rating)
        
        return new_rating
    
    def update_from_intervention(
        self,
        developer_id: str,
        intervention_type: str,
        predicted_value: float,
        actual_value: float
    ) -> Dict[str, float]:
        """
        Update ratings for developer and intervention type.
        
        Args:
            developer_id: ID of the developer who made the prediction
            intervention_type: Type of intervention
            predicted_value: Predicted value
            actual_value: Actual value
        
        Returns:
            Dict with new ratings
        """
        # Update developer rating
        new_developer_rating = self.update_rating(
            developer_id,
            EloEntityType.DEVELOPER,
            predicted_value,
            actual_value
        )
        
        # Update intervention type rating
        new_intervention_rating = self.update_rating(
            intervention_type,
            EloEntityType.INTERVENTION_TYPE,
            predicted_value,
            actual_value
        )
        
        return {
            "developer_rating": new_developer_rating,
            "intervention_type_rating": new_intervention_rating
        }
    
    def get_leaderboard(self, entity_type: EloEntityType, limit: int = 10) -> List[Dict[str, Any]]:
        """Get leaderboard for an entity type."""
        filtered = [
            rating for rating in self.ratings.values()
            if rating.entity_type == entity_type
        ]
        
        # Sort by rating
        filtered.sort(key=lambda x: x.rating, reverse=True)
        
        # Get top N
        top = filtered[:limit]
        
        return [rating.to_dict() for rating in top]
    
    def get_developer_leaderboard(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get developer leaderboard."""
        return self.get_leaderboard(EloEntityType.DEVELOPER, limit)
    
    def get_intervention_type_leaderboard(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get intervention type leaderboard."""
        return self.get_leaderboard(EloEntityType.INTERVENTION_TYPE, limit)
    
    def get_entity_rating(self, entity_id: str, entity_type: EloEntityType) -> Optional[Dict[str, Any]]:
        """Get rating for a specific entity."""
        key = f"{entity_type.value}:{entity_id}"
        rating = self.ratings.get(key)
        
        if not rating:
            return None
        
        return rating.to_dict()
    
    def get_percentile(self, entity_id: str, entity_type: EloEntityType) -> float:
        """Get percentile rank of an entity."""
        key = f"{entity_type.value}:{entity_id}"
        rating = self.ratings.get(key)
        
        if not rating:
            return 0.0
        
        # Get all ratings of this type
        filtered = [
            r for r in self.ratings.values()
            if r.entity_type == entity_type
        ]
        
        if not filtered:
            return 0.0
        
        # Sort by rating
        filtered.sort(key=lambda x: x.rating, reverse=True)
        
        # Find position
        for i, r in enumerate(filtered):
            if r.entity_id == entity_id:
                return (i + 1) / len(filtered)
        
        return 0.0
    
    def get_rating_distribution(self, entity_type: EloEntityType) -> Dict[str, Any]:
        """Get rating distribution statistics."""
        filtered = [
            rating for rating in self.ratings.values()
            if rating.entity_type == entity_type
        ]
        
        if not filtered:
            return {"message": "No ratings for this entity type"}
        
        ratings = [r.rating for r in filtered]
        
        return {
            "count": len(filtered),
            "min": min(ratings),
            "max": max(ratings),
            "mean": sum(ratings) / len(ratings),
            "median": sorted(ratings)[len(ratings) // 2],
            "std_dev": math.sqrt(sum((r - sum(ratings) / len(ratings)) ** 2 for r in ratings) / len(ratings))
        }
    
    def find_underrated_entities(
        self,
        entity_type: EloEntityType,
        min_games: int = 5,
        threshold: float = 1100.0
    ) -> List[Dict[str, Any]]:
        """Find entities with high ratings but low recognition."""
        filtered = [
            rating for rating in self.ratings.values()
            if rating.entity_type == entity_type
            and rating.games_played >= min_games
            and rating.rating >= threshold
        ]
        
        # Sort by rating
        filtered.sort(key=lambda x: x.rating, reverse=True)
        
        return [rating.to_dict() for rating in filtered]
    
    def find_overrated_entities(
        self,
        entity_type: EloEntityType,
        min_games: int = 5,
        threshold: float = 900.0
    ) -> List[Dict[str, Any]]:
        """Find entities with low ratings but high recognition."""
        filtered = [
            rating for rating in self.ratings.values()
            if rating.entity_type == entity_type
            and rating.games_played >= min_games
            and rating.rating <= threshold
        ]
        
        # Sort by rating (ascending)
        filtered.sort(key=lambda x: x.rating)
        
        return [rating.to_dict() for rating in filtered]
    
    def calculate_matchup_probability(
        self,
        entity_a_id: str,
        entity_b_id: str,
        entity_type: EloEntityType
    ) -> float:
        """
        Calculate probability that entity A beats entity B.
        """
        rating_a = self.get_rating(entity_a_id, entity_type)
        rating_b = self.get_rating(entity_b_id, entity_type)
        
        return self.calculate_expected_score(rating_a.rating, rating_b.rating)
    
    def batch_update_from_outcomes(
        self,
        outcomes: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Batch update ratings from multiple outcomes.
        
        Args:
            outcomes: List of outcome dicts with developer_id, intervention_type, predicted_value, actual_value
        
        Returns:
            Summary of updates
        """
        updates = []
        
        for outcome in outcomes:
            result = self.update_from_intervention(
                developer_id=outcome["developer_id"],
                intervention_type=outcome["intervention_type"],
                predicted_value=outcome["predicted_value"],
                actual_value=outcome["actual_value"]
            )
            updates.append(result)
        
        # Calculate summary
        avg_developer_rating_change = sum(
            u["developer_rating"] - 1000 for u in updates
        ) / len(updates) if updates else 0
        
        avg_intervention_rating_change = sum(
            u["intervention_type_rating"] - 1000 for u in updates
        ) / len(updates) if updates else 0
        
        return {
            "total_updates": len(updates),
            "avg_developer_rating_change": avg_developer_rating_change,
            "avg_intervention_rating_change": avg_intervention_rating_change,
            "updates": updates
        }
    
    def save_to_file(self, filepath: str):
        """Save ratings to file."""
        import json
        data = {
            "k_factor": self.k_factor,
            "ratings": {key: rating.to_dict() for key, rating in self.ratings.items()}
        }
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)
    
    def load_from_file(self, filepath: str):
        """Load ratings from file."""
        import json
        with open(filepath, 'r') as f:
            data = json.load(f)
        
        self.k_factor = data["k_factor"]
        self.ratings = {}
        
        for key, rating_data in data["ratings"].items():
            rating = EloRating(
                entity_id=rating_data["entity_id"],
                entity_type=EloEntityType(rating_data["entity_type"]),
                rating=rating_data["rating"],
                games_played=rating_data["games_played"],
                wins=rating_data["wins"],
                losses=rating_data["losses"],
                draws=rating_data["draws"]
            )
            rating.history = rating_data.get("history", [])
            self.ratings[key] = rating


class PredictionAccuracyTracker:
    """
    Tracks prediction accuracy for different prediction sources.
    
    Can track:
    - Individual developers
    - Prediction models
    - Intervention types
    - Asset types
    """
    
    def __init__(self):
        self.elo = InnovationElo()
    
    def record_prediction(
        self,
        predictor_id: str,
        predictor_type: EloEntityType,
        intervention_type: str,
        predicted_value: float,
        actual_value: float
    ) -> Dict[str, float]:
        """Record a prediction and its outcome."""
        return self.elo.update_from_intervention(
            developer_id=predictor_id,
            intervention_type=intervention_type,
            predicted_value=predicted_value,
            actual_value=actual_value
        )
    
    def get_top_predictors(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get top predictors by Elo rating."""
        return self.elo.get_leaderboard(EloEntityType.DEVELOPER, limit)
    
    def get_best_interventions(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get best intervention types by Elo rating."""
        return self.elo.get_leaderboard(EloEntityType.INTERVENTION_TYPE, limit)
    
    def get_predictor_stats(self, predictor_id: str) -> Dict[str, Any]:
        """Get detailed stats for a predictor."""
        rating = self.elo.get_entity_rating(predictor_id, EloEntityType.DEVELOPER)
        percentile = self.elo.get_percentile(predictor_id, EloEntityType.DEVELOPER)
        
        if not rating:
            return {"error": "Predictor not found"}
        
        return {
            **rating,
            "percentile": percentile
        }
