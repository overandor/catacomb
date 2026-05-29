"""Trajectory Agent - Measures direction, velocity, acceleration, not current state."""
from typing import Dict, Any, List
from datetime import datetime, timedelta
from base_agent import BaseAgent, AgentOutput


class TrajectoryAgent(BaseAgent):
    """Analyzes repo trajectory: velocity, acceleration, growth direction."""
    
    def __init__(self):
        super().__init__("Trajectory")
    
    def _calculate_star_velocity(self, repo_data: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate star growth velocity (stars per day)."""
        evidence = {}
        
        stars = repo_data.get("stars", 0)
        created_at = repo_data.get("created_at")
        
        evidence["current_stars"] = stars
        evidence["created_at"] = created_at
        
        if created_at:
            try:
                created_date = datetime.fromisoformat(created_at.replace("Z", "+00:00"))
                days_since_creation = (datetime.now(created_date.tzinfo) - created_date).days
                evidence["days_since_creation"] = days_since_creation
                
                if days_since_creation > 0:
                    velocity = stars / days_since_creation  # stars per day
                    evidence["star_velocity_per_day"] = round(velocity, 4)
                    
                    # Velocity tier
                    if velocity > 10:
                        velocity_tier = "explosive"
                    elif velocity > 1:
                        velocity_tier = "high"
                    elif velocity > 0.1:
                        velocity_tier = "moderate"
                    elif velocity > 0.01:
                        velocity_tier = "low"
                    else:
                        velocity_tier = "stagnant"
                    
                    evidence["velocity_tier"] = velocity_tier
                else:
                    evidence["star_velocity_per_day"] = 0
                    evidence["velocity_tier"] = "unknown"
            except:
                evidence["star_velocity_per_day"] = 0
                evidence["velocity_tier"] = "error"
        else:
            evidence["star_velocity_per_day"] = 0
            evidence["velocity_tier"] = "unknown"
        
        return {
            "score": self._normalize_velocity(evidence.get("star_velocity_per_day", 0)),
            "evidence": evidence
        }
    
    def _calculate_star_acceleration(self, repo_data: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate star acceleration (change in velocity)."""
        evidence = {}
        
        commits_last_year = repo_data.get("commits_last_year", 0)
        stars = repo_data.get("stars", 0)
        
        evidence["commits_last_year"] = commits_last_year
        evidence["stars"] = stars
        
        # Proxy for acceleration: recent activity vs total stars
        # High recent activity relative to total stars suggests accelerating growth
        if stars > 0:
            activity_ratio = commits_last_year / stars
            evidence["activity_to_star_ratio"] = round(activity_ratio, 4)
            
            # Acceleration tier
            if activity_ratio > 0.5:
                acceleration_tier = "accelerating"
            elif activity_ratio > 0.1:
                acceleration_tier = "steady"
            elif activity_ratio > 0.01:
                acceleration_tier = "decelerating"
            else:
                acceleration_tier = "stagnant"
            
            evidence["acceleration_tier"] = acceleration_tier
        else:
            evidence["activity_to_star_ratio"] = 0
            evidence["acceleration_tier"] = "unknown"
        
        return {
            "score": self._normalize_acceleration(evidence.get("activity_to_star_ratio", 0)),
            "evidence": evidence
        }
    
    def _calculate_contributor_growth(self, repo_data: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate contributor growth trajectory."""
        evidence = {}
        
        contributors = repo_data.get("contributors", 0)
        commits_last_year = repo_data.get("commits_last_year", 0)
        
        evidence["contributors"] = contributors
        evidence["commits_last_year"] = commits_last_year
        
        # Contributor efficiency: commits per contributor
        if contributors > 0:
            commits_per_contributor = commits_last_year / contributors
            evidence["commits_per_contributor"] = round(commits_per_contributor, 2)
            
            # Growth tier
            if commits_per_contributor > 20:
                growth_tier = "high_activity"
            elif commits_per_contributor > 5:
                growth_tier = "healthy"
            elif commits_per_contributor > 1:
                growth_tier = "moderate"
            else:
                growth_tier = "low_activity"
            
            evidence["contributor_growth_tier"] = growth_tier
        else:
            evidence["commits_per_contributor"] = 0
            evidence["contributor_growth_tier"] = "no_contributors"
        
        return {
            "score": self._normalize_contributor_growth(contributors, commits_last_year),
            "evidence": evidence
        }
    
    def _calculate_issue_velocity(self, repo_data: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate issue engagement velocity."""
        evidence = {}
        
        open_issues = repo_data.get("open_issues", 0)
        stars = repo_data.get("stars", 0)
        
        evidence["open_issues"] = open_issues
        evidence["stars"] = stars
        
        # Issue engagement: issues per star
        if stars > 0:
            issue_ratio = open_issues / stars
            evidence["issue_to_star_ratio"] = round(issue_ratio, 4)
            
            # Engagement tier
            if issue_ratio > 1.0:
                engagement_tier = "high_engagement"
            elif issue_ratio > 0.5:
                engagement_tier = "moderate_engagement"
            elif issue_ratio > 0.1:
                engagement_tier = "low_engagement"
            else:
                engagement_tier = "minimal_engagement"
            
            evidence["engagement_tier"] = engagement_tier
        else:
            evidence["issue_to_star_ratio"] = 0
            evidence["engagement_tier"] = "unknown"
        
        return {
            "score": self._normalize_issue_engagement(evidence.get("issue_to_star_ratio", 0)),
            "evidence": evidence
        }
    
    def _calculate_release_frequency(self, repo_data: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate release frequency trajectory."""
        evidence = {}
        
        releases = repo_data.get("releases", 0)
        commits_last_year = repo_data.get("commits_last_year", 0)
        
        evidence["releases"] = releases
        evidence["commits_last_year"] = commits_last_year
        
        # Release cadence: releases per year (proxy)
        if commits_last_year > 0:
            release_cadence = releases / (commits_last_year / 52)  # releases per week of activity
            evidence["releases_per_activity_week"] = round(release_cadence, 4)
            
            # Cadence tier
            if release_cadence > 0.5:
                cadence_tier = "frequent"
            elif release_cadence > 0.1:
                cadence_tier = "regular"
            elif release_cadence > 0.01:
                cadence_tier = "occasional"
            else:
                cadence_tier = "rare"
            
            evidence["release_cadence_tier"] = cadence_tier
        else:
            evidence["releases_per_activity_week"] = 0
            evidence["release_cadence_tier"] = "no_activity"
        
        return {
            "score": self._normalize_release_cadence(evidence.get("releases_per_activity_week", 0)),
            "evidence": evidence
        }
    
    def _calculate_dependency_adoption(self, repo_data: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate dependency adoption trajectory (proxy via forks)."""
        evidence = {}
        
        forks = repo_data.get("forks", 0)
        stars = repo_data.get("stars", 0)
        
        evidence["forks"] = forks
        evidence["stars"] = stars
        
        # Fork ratio indicates integration/adoption
        if stars > 0:
            fork_ratio = forks / stars
            evidence["fork_ratio"] = round(fork_ratio, 4)
            
            # Adoption tier
            if fork_ratio > 1.0:
                adoption_tier = "high_adoption"
            elif fork_ratio > 0.5:
                adoption_tier = "moderate_adoption"
            elif fork_ratio > 0.2:
                adoption_tier = "low_adoption"
            else:
                adoption_tier = "minimal_adoption"
            
            evidence["adoption_tier"] = adoption_tier
        else:
            evidence["fork_ratio"] = 0
            evidence["adoption_tier"] = "unknown"
        
        return {
            "score": self._normalize_adoption(evidence.get("fork_ratio", 0)),
            "evidence": evidence
        }
    
    def _normalize_velocity(self, velocity: float) -> float:
        """Normalize velocity to 0-100."""
        # Logarithmic scale for velocity
        if velocity <= 0:
            return 0
        elif velocity < 0.01:
            return 10
        elif velocity < 0.1:
            return 30
        elif velocity < 1:
            return 50
        elif velocity < 10:
            return 70
        else:
            return 90
    
    def _normalize_acceleration(self, ratio: float) -> float:
        """Normalize acceleration to 0-100."""
        if ratio <= 0:
            return 0
        elif ratio < 0.01:
            return 20
        elif ratio < 0.1:
            return 40
        elif ratio < 0.5:
            return 60
        else:
            return 80
    
    def _normalize_contributor_growth(self, contributors: int, commits: int) -> float:
        """Normalize contributor growth to 0-100."""
        if contributors == 0:
            return 0
        elif contributors == 1:
            return 30
        elif contributors < 5:
            return 50
        elif contributors < 10:
            return 70
        else:
            return 90
    
    def _normalize_issue_engagement(self, ratio: float) -> float:
        """Normalize issue engagement to 0-100."""
        if ratio <= 0:
            return 0
        elif ratio < 0.1:
            return 20
        elif ratio < 0.5:
            return 50
        elif ratio < 1.0:
            return 70
        else:
            return 85
    
    def _normalize_release_cadence(self, cadence: float) -> float:
        """Normalize release cadence to 0-100."""
        if cadence <= 0:
            return 0
        elif cadence < 0.01:
            return 20
        elif cadence < 0.1:
            return 50
        elif cadence < 0.5:
            return 70
        else:
            return 90
    
    def _normalize_adoption(self, ratio: float) -> float:
        """Normalize adoption to 0-100."""
        if ratio <= 0:
            return 0
        elif ratio < 0.2:
            return 30
        elif ratio < 0.5:
            return 50
        elif ratio < 1.0:
            return 70
        else:
            return 90
    
    def analyze(self, repo_data: Dict[str, Any]) -> AgentOutput:
        """
        Analyze repo trajectory across multiple dimensions.
        """
        evidence = {}
        
        # Calculate all trajectory metrics
        star_velocity = self._calculate_star_velocity(repo_data)
        star_acceleration = self._calculate_star_acceleration(repo_data)
        contributor_growth = self._calculate_contributor_growth(repo_data)
        issue_velocity = self._calculate_issue_velocity(repo_data)
        release_frequency = self._calculate_release_frequency(repo_data)
        dependency_adoption = self._calculate_dependency_adoption(repo_data)
        
        # Store evidence
        evidence["star_velocity"] = star_velocity["evidence"]
        evidence["star_acceleration"] = star_acceleration["evidence"]
        evidence["contributor_growth"] = contributor_growth["evidence"]
        evidence["issue_velocity"] = issue_velocity["evidence"]
        evidence["release_frequency"] = release_frequency["evidence"]
        evidence["dependency_adoption"] = dependency_adoption["evidence"]
        
        # Calculate overall trajectory score
        # Weighted combination favoring acceleration over current state
        trajectory_score = (
            0.15 * star_velocity["score"] +
            0.25 * star_acceleration["score"] +  # Acceleration weighted higher
            0.20 * contributor_growth["score"] +
            0.15 * issue_velocity["score"] +
            0.10 * release_frequency["score"] +
            0.15 * dependency_adoption["score"]
        )
        
        evidence["overall_trajectory_score"] = trajectory_score
        
        # Determine trajectory direction
        velocity_tier = star_velocity["evidence"].get("velocity_tier", "unknown")
        acceleration_tier = star_acceleration["evidence"].get("acceleration_tier", "unknown")
        
        if acceleration_tier == "accelerating" and velocity_tier in ["high", "explosive"]:
            direction = "explosive_growth"
        elif acceleration_tier == "accelerating":
            direction = "accelerating"
        elif acceleration_tier == "steady" and velocity_tier in ["moderate", "high"]:
            direction = "steady_growth"
        elif acceleration_tier == "steady":
            direction = "stable"
        elif acceleration_tier == "decelerating":
            direction = "decelerating"
        else:
            direction = "stagnant"
        
        evidence["trajectory_direction"] = direction
        
        # Confidence based on data availability
        has_activity_data = repo_data.get("commits_last_year", 0) > 0
        has_stars = repo_data.get("stars", 0) > 0
        has_created_date = bool(repo_data.get("created_at"))
        
        confidence = 0.5
        if has_activity_data:
            confidence += 0.2
        if has_stars:
            confidence += 0.2
        if has_created_date:
            confidence += 0.1
        
        return AgentOutput(
            score=round(trajectory_score, 2),
            evidence=evidence,
            confidence=confidence,
            hash=""
        )
