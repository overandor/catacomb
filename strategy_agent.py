"""Strategy Agent - Generates deterministic takeover path: fork, contact maintainer, rebuild, reposition, monetize, launch."""
from typing import Dict, Any, List
from base_agent import BaseAgent, AgentOutput


class StrategyAgent(BaseAgent):
    """Generates deterministic strategy for repo revival."""
    
    def __init__(self):
        super().__init__("Strategy")
        self.target_revival_score = 50.0
    
    def _determine_takeover_path(self, repo_data: Dict[str, Any], revival_score: float) -> List[str]:
        """Determine the optimal takeover path based on repo state."""
        path = []
        
        stars = repo_data.get("stars", 0)
        forks = repo_data.get("forks", 0)
        is_archived = repo_data.get("archived", False)
        is_fork = repo_data.get("is_fork", False)
        license_key = repo_data.get("license")
        contributors = repo_data.get("contributors", 0)
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
        
        # Step 1: Assessment
        if is_archived:
            path.append("ARCHIVED: Fork and reactivate")
        elif is_fork:
            path.append("FORK: Consider original source instead")
        else:
            path.append("ASSESS: Evaluate original repo viability")
        
        # Step 2: Contact decision
        if contributors <= 1 and not is_archived:
            path.append("CONTACT: Reach out to sole maintainer")
        elif contributors <= 3 and not is_archived:
            path.append("CONTACT: Reach out to maintainers")
        elif is_archived:
            path.append("CONTACT: Not needed - repo is archived")
        else:
            path.append("CONTACT: Community outreach via issues")
        
        # Step 3: Fork decision
        if is_archived or (license_key and license_key.lower() in ["mit", "apache-2.0", "bsd"]):
            path.append("FORK: Create fork under your organization")
        elif not license_key:
            path.append("FORK: Risky - no license, proceed with caution")
        else:
            path.append("FORK: Check license compatibility first")
        
        # Step 4: Rebuild strategy
        if not has_package:
            path.append("REBUILD: Add package manager and build system")
        if not has_readme:
            path.append("REBUILD: Create comprehensive documentation")
        if open_issues > 10:
            path.append("REBUILD: Address backlog of open issues")
        path.append("REBUILD: Modernize dependencies and tooling")
        
        # Step 5: Repositioning
        if stars < 50:
            path.append("REPOSITION: Improve SEO and discoverability")
        if not repo_data.get("topics", []):
            path.append("REPOSITION: Add relevant GitHub topics")
        path.append("REPOSITION: Clarify value proposition in README")
        
        # Step 6: Monetization potential
        if stars > 100 and forks > 20:
            path.append("MONETIZE: Consider enterprise features")
        elif stars > 50:
            path.append("MONETIZE: Add sponsorship options")
        else:
            path.append("MONETIZE: Build user base first")
        
        # Step 7: Launch strategy
        if revival_score > 70:
            path.append("LAUNCH: Aggressive marketing campaign")
        elif revival_score > 50:
            path.append("LAUNCH: Targeted community outreach")
        else:
            path.append("LAUNCH: Gradual organic growth")
        
        return path
    
    def _calculate_transformation_potential(self, repo_data: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate potential for transformation/improvement."""
        evidence = {}
        
        stars = repo_data.get("stars", 0)
        forks = repo_data.get("forks", 0)
        open_issues = repo_data.get("open_issues", 0)
        has_readme = repo_data.get("has_readme", False)
        has_ci = repo_data.get("has_ci", False)
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
        evidence["has_ci"] = has_ci
        evidence["has_package_manager"] = has_package
        
        # Transformation potential based on gaps
        gaps = 0
        if not has_readme:
            gaps += 1
        if not has_ci:
            gaps += 1
        if not has_package:
            gaps += 1
        if open_issues > 5:
            gaps += 1
        
        evidence["improvement_gaps"] = gaps
        
        # High transformation potential if there are gaps but some interest
        if gaps >= 2 and (stars > 0 or forks > 0):
            potential = 0.9
        elif gaps >= 3:
            potential = 0.8
        elif gaps >= 2:
            potential = 0.6
        elif gaps >= 1:
            potential = 0.4
        else:
            potential = 0.2
        
        evidence["transformation_potential"] = potential
        
        return {
            "score": potential,
            "evidence": evidence
        }
    
    def _calculate_risk_penalty(self, repo_data: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate risk factors that reduce revival viability."""
        evidence = {}
        
        license_key = repo_data.get("license")
        is_fork = repo_data.get("is_fork", False)
        size = repo_data.get("size", 0)
        contributors = repo_data.get("contributors", 0)
        open_issues = repo_data.get("open_issues", 0)
        
        evidence["license"] = license_key
        evidence["is_fork"] = is_fork
        evidence["size_kb"] = size
        evidence["contributors"] = contributors
        evidence["open_issues"] = open_issues
        
        risk = 0.0
        
        # License risk
        if not license_key:
            risk += 0.3
        elif license_key and license_key.lower() in ["gpl-3.0", "agpl-3.0"]:
            risk += 0.2  # Copyleft licenses
        
        # Fork risk
        if is_fork:
            risk += 0.2
        
        # Size risk (too large = hard to maintain)
        if size > 100000:  # > 100MB
            risk += 0.2
        elif size > 10000:  # > 10MB
            risk += 0.1
        
        # Contributor risk (too many = hard to coordinate)
        if contributors > 20:
            risk += 0.2
        elif contributors > 10:
            risk += 0.1
        
        # Issue debt risk
        if open_issues > 100:
            risk += 0.2
        elif open_issues > 50:
            risk += 0.1
        
        risk = min(risk, 1.0)
        evidence["risk_penalty"] = risk
        
        return {
            "score": risk,
            "evidence": evidence
        }
    
    def analyze(self, repo_data: Dict[str, Any]) -> AgentOutput:
        """
        Generate deterministic strategy for repo revival.
        """
        evidence = {}
        
        # Calculate transformation potential
        transformation = self._calculate_transformation_potential(repo_data)
        evidence["transformation"] = transformation["evidence"]
        
        # Calculate risk penalty
        risk = self._calculate_risk_penalty(repo_data)
        evidence["risk"] = risk["evidence"]
        
        # Generate takeover path using target_revival_score
        revival_score = self.target_revival_score
        takeover_path = self._determine_takeover_path(repo_data, revival_score)
        evidence["takeover_path"] = takeover_path
        
        # Calculate strategy score (0-100)
        # Higher score = better strategy fit
        strategy_score = (
            transformation["score"] * 0.6  # High transformation potential = good
            - risk["score"] * 0.4  # High risk = bad
        )
        strategy_score = max(0, strategy_score) * 100
        
        evidence["strategy_score"] = strategy_score
        
        # Confidence based on data completeness
        required_fields = ["stars", "forks", "license", "contributors"]
        completeness = sum(1 for field in required_fields if field in repo_data)
        confidence = completeness / len(required_fields)
        
        return AgentOutput(
            score=round(strategy_score, 2),
            evidence=evidence,
            confidence=confidence,
            hash=""
        )
