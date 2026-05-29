"""Revival Agent - Determines if repo is underdeveloped, abandoned, underexposed, forkable, and worth reviving."""
from datetime import datetime, timedelta
from typing import Dict, Any
from base_agent import BaseAgent, AgentOutput


class RevivalAgent(BaseAgent):
    """Determines revival potential of a repository."""
    
    def __init__(self):
        super().__init__("Revival")
    
    def _calculate_abandonment_score(self, repo_data: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate abandonment signal based on activity."""
        evidence = {}
        
        # Time since last commit
        pushed_at = repo_data.get("pushed_at")
        if pushed_at:
            try:
                last_commit = datetime.fromisoformat(pushed_at.replace("Z", "+00:00"))
                days_since_commit = (datetime.now(last_commit.tzinfo) - last_commit).days
                evidence["days_since_last_commit"] = days_since_commit
                
                # Abandonment increases with time
                if days_since_commit > 365:
                    abandonment = 1.0
                elif days_since_commit > 180:
                    abandonment = 0.8
                elif days_since_commit > 90:
                    abandonment = 0.6
                elif days_since_commit > 30:
                    abandonment = 0.4
                else:
                    abandonment = 0.1
            except:
                days_since_commit = 999
                abandonment = 1.0
        else:
            days_since_commit = 999
            abandonment = 1.0
        
        evidence["abandonment_signal"] = abandonment
        
        # Check if archived
        is_archived = repo_data.get("archived", False)
        evidence["is_archived"] = is_archived
        if is_archived:
            abandonment = max(abandonment, 0.9)
        
        # Check commit frequency
        commits_last_year = repo_data.get("commits_last_year", 0)
        evidence["commits_last_year"] = commits_last_year
        if commits_last_year == 0:
            abandonment = max(abandonment, 0.9)
        elif commits_last_year < 5:
            abandonment = max(abandonment, 0.7)
        
        return {
            "score": abandonment,
            "evidence": evidence
        }
    
    def _calculate_underexposure_score(self, repo_data: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate underexposure based on stars vs quality."""
        evidence = {}
        
        stars = repo_data.get("stars", 0)
        forks = repo_data.get("forks", 0)
        open_issues = repo_data.get("open_issues", 0)
        has_readme = repo_data.get("has_readme", False)
        has_package = any([
            repo_data.get("has_package_json", False),
            repo_data.get("has_requirements_txt", False),
            repo_data.get("has_setup_py", False),
            repo_data.get("has_pyproject_toml", False),
            repo_data.get("has_cargo_toml", False),
            repo_data.get("has_go_mod", False)
        ])
        
        evidence["stars"] = stars
        evidence["forks"] = forks
        evidence["open_issues"] = open_issues
        evidence["has_readme"] = has_readme
        evidence["has_package_manager"] = has_package
        
        # Underexposed: good quality but low stars
        quality_score = 0
        if has_readme:
            quality_score += 20
        if has_package:
            quality_score += 30
        if open_issues > 0:  # Community engagement
            quality_score += 20
        if forks > 0:
            quality_score += 30
        
        # Normalize quality
        quality_score = min(quality_score, 100)
        
        # Underexposure is high when quality is good but stars are low
        if stars < 10 and quality_score > 50:
            underexposure = 0.9
        elif stars < 50 and quality_score > 60:
            underexposure = 0.7
        elif stars < 100 and quality_score > 70:
            underexposure = 0.5
        elif stars < 500 and quality_score > 80:
            underexposure = 0.3
        else:
            underexposure = 0.1
        
        evidence["quality_score"] = quality_score
        evidence["underexposure_signal"] = underexposure
        
        return {
            "score": underexposure,
            "evidence": evidence
        }
    
    def _calculate_forkability_score(self, repo_data: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate forkability based on license and structure."""
        evidence = {}
        
        license_key = repo_data.get("license")
        is_fork = repo_data.get("is_fork", False)
        size = repo_data.get("size", 0)
        contributors = repo_data.get("contributors", 0)
        
        evidence["license"] = license_key
        evidence["is_fork"] = is_fork
        evidence["size_kb"] = size
        evidence["contributors"] = contributors
        
        # Permissive licenses are most forkable
        permissive_licenses = ["mit", "apache-2.0", "bsd-3-clause", "bsd-2-clause", "isc"]
        if license_key in permissive_licenses:
            forkability = 1.0
        elif license_key:
            forkability = 0.7  # Other licenses
        else:
            forkability = 0.3  # No license - risky
        
        # Don't fork forks
        if is_fork:
            forkability *= 0.5
        
        # Smaller repos are easier to fork
        if size < 1000:  # < 1MB
            forkability *= 1.0
        elif size < 10000:  # < 10MB
            forkability *= 0.9
        elif size < 100000:  # < 100MB
            forkability *= 0.7
        else:
            forkability *= 0.5
        
        # More contributors = harder to take over
        if contributors > 10:
            forkability *= 0.5
        elif contributors > 5:
            forkability *= 0.7
        elif contributors > 1:
            forkability *= 0.9
        
        forkability = min(forkability, 1.0)
        
        evidence["forkability_signal"] = forkability
        
        return {
            "score": forkability,
            "evidence": evidence
        }
    
    def _calculate_underdeveloped_score(self, repo_data: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate if repo is underdeveloped (MVP or incomplete)."""
        evidence = {}
        
        has_readme = repo_data.get("has_readme", False)
        has_package = any([
            repo_data.get("has_package_json", False),
            repo_data.get("has_requirements_txt", False),
            repo_data.get("has_setup_py", False),
            repo_data.get("has_pyproject_toml", False),
            repo_data.get("has_cargo_toml", False),
            repo_data.get("has_go_mod", False)
        ])
        has_ci = repo_data.get("has_ci", False)
        has_tests = repo_data.get("has_ci", False)  # Proxy for tests
        releases = repo_data.get("releases", 0)
        stars = repo_data.get("stars", 0)
        
        evidence["has_readme"] = has_readme
        evidence["has_package_manager"] = has_package
        evidence["has_ci"] = has_ci
        evidence["releases"] = releases
        evidence["stars"] = stars
        
        # Underdeveloped indicators
        missing_features = 0
        if not has_readme:
            missing_features += 1
        if not has_package:
            missing_features += 1
        if not has_ci:
            missing_features += 1
        if releases == 0:
            missing_features += 1
        
        evidence["missing_features_count"] = missing_features
        
        # High underdevelopment if missing features but has some interest
        if missing_features >= 2 and stars < 100:
            underdeveloped = 0.9
        elif missing_features >= 3:
            underdeveloped = 0.8
        elif missing_features >= 2:
            underdeveloped = 0.6
        elif missing_features >= 1:
            underdeveloped = 0.4
        else:
            underdeveloped = 0.1
        
        evidence["underdeveloped_signal"] = underdeveloped
        
        return {
            "score": underdeveloped,
            "evidence": evidence
        }
    
    def analyze(self, repo_data: Dict[str, Any]) -> AgentOutput:
        """
        Analyze revival potential across multiple dimensions.
        """
        evidence = {}
        
        # Calculate individual scores
        abandonment = self._calculate_abandonment_score(repo_data)
        underexposure = self._calculate_underexposure_score(repo_data)
        forkability = self._calculate_forkability_score(repo_data)
        underdeveloped = self._calculate_underdeveloped_score(repo_data)
        
        # Store evidence
        evidence["abandonment"] = abandonment["evidence"]
        evidence["underexposure"] = underexposure["evidence"]
        evidence["forkability"] = forkability["evidence"]
        evidence["underdeveloped"] = underdeveloped["evidence"]
        
        # Calculate overall revival score
        # Weighted combination
        revival_score = (
            0.30 * abandonment["score"] +  # Abandoned = good for revival
            0.30 * underexposure["score"] +  # Underexposed = opportunity
            0.20 * forkability["score"] +  # Forkable = actionable
            0.20 * underdeveloped["score"]  # Underdeveloped = room to grow
        )
        
        evidence["overall_revival_score"] = revival_score
        
        # Confidence based on data availability
        has_activity_data = "pushed_at" in repo_data or "commits_last_year" in repo_data
        has_metadata = "stars" in repo_data and "license" in repo_data
        
        if has_activity_data and has_metadata:
            confidence = 0.9
        elif has_activity_data or has_metadata:
            confidence = 0.7
        else:
            confidence = 0.5
        
        return AgentOutput(
            score=round(revival_score * 100, 2),
            evidence=evidence,
            confidence=confidence,
            hash=""
        )
