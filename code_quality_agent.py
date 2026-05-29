"""Code Quality Agent - Scores structure, complexity, dependency health, docs, tests, CI, maintainability."""
from typing import Dict, Any
from base_agent import BaseAgent, AgentOutput


class CodeQualityAgent(BaseAgent):
    """Deterministically scores code quality without LLMs."""
    
    def __init__(self):
        super().__init__("CodeQuality")
    
    def _assess_structure(self, repo_data: Dict[str, Any]) -> Dict[str, Any]:
        """Assess repository structure quality."""
        evidence = {}
        
        size = repo_data.get("size", 0)
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
        has_makefile = repo_data.get("has_makefile", False)
        has_dockerfile = repo_data.get("has_dockerfile", False)
        
        evidence["size_kb"] = size
        evidence["has_readme"] = has_readme
        evidence["has_package_manager"] = has_package
        evidence["has_ci"] = has_ci
        evidence["has_makefile"] = has_makefile
        evidence["has_dockerfile"] = has_dockerfile
        
        # Structure score
        structure_score = 0
        if has_readme:
            structure_score += 20
        if has_package:
            structure_score += 20
        if has_ci:
            structure_score += 20
        if has_makefile:
            structure_score += 15
        if has_dockerfile:
            structure_score += 15
        
        # Size penalty (too large = complexity risk)
        if size > 100000:  # > 100MB
            structure_score *= 0.7
        elif size > 10000:  # > 10MB
            structure_score *= 0.85
        
        evidence["structure_score"] = structure_score
        
        return {
            "score": structure_score,
            "evidence": evidence
        }
    
    def _assess_complexity(self, repo_data: Dict[str, Any]) -> Dict[str, Any]:
        """Assess code complexity based on indirect signals."""
        evidence = {}
        
        size = repo_data.get("size", 0)
        contributors = repo_data.get("contributors", 0)
        open_issues = repo_data.get("open_issues", 0)
        commits_last_year = repo_data.get("commits_last_year", 0)
        
        evidence["size_kb"] = size
        evidence["contributors"] = contributors
        evidence["open_issues"] = open_issues
        evidence["commits_last_year"] = commits_last_year
        
        # Complexity score (lower is better for maintainability)
        complexity_score = 100  # Start with best
        
        # Size indicates complexity
        if size > 100000:
            complexity_score -= 40
        elif size > 10000:
            complexity_score -= 25
        elif size > 1000:
            complexity_score -= 10
        
        # Many contributors suggests complex codebase
        if contributors > 20:
            complexity_score -= 20
        elif contributors > 10:
            complexity_score -= 10
        
        # High issue count suggests complexity or debt
        if open_issues > 100:
            complexity_score -= 20
        elif open_issues > 50:
            complexity_score -= 10
        
        # High commit frequency suggests active maintenance
        if commits_last_year > 100:
            complexity_score += 10
        elif commits_last_year > 50:
            complexity_score += 5
        
        complexity_score = max(0, min(complexity_score, 100))
        evidence["complexity_score"] = complexity_score
        
        return {
            "score": complexity_score,
            "evidence": evidence
        }
    
    def _assess_dependency_health(self, repo_data: Dict[str, Any]) -> Dict[str, Any]:
        """Assess dependency health based on package manager presence."""
        evidence = {}
        
        has_package = any([
            repo_data.get("has_package_json", False),
            repo_data.get("has_requirements_txt", False),
            repo_data.get("has_setup_py", False),
            repo_data.get("has_pyproject_toml", False),
            repo_data.get("has_cargo_toml", False),
            repo_data.get("has_go_mod", False)
        ])
        
        has_ci = repo_data.get("has_ci", False)
        commits_last_year = repo_data.get("commits_last_year", 0)
        
        evidence["has_package_manager"] = has_package
        evidence["has_ci"] = has_ci
        evidence["commits_last_year"] = commits_last_year
        
        # Dependency health score
        dep_health = 0
        if has_package:
            dep_health += 40
        if has_ci:
            dep_health += 30  # CI likely tests dependencies
        if commits_last_year > 0:
            dep_health += 30  # Active maintenance = updated deps
        
        evidence["dependency_health_score"] = dep_health
        
        return {
            "score": dep_health,
            "evidence": evidence
        }
    
    def _assess_documentation(self, repo_data: Dict[str, Any]) -> Dict[str, Any]:
        """Assess documentation quality."""
        evidence = {}
        
        has_readme = repo_data.get("has_readme", False)
        readme_size = repo_data.get("readme_size", 0)
        has_wiki = repo_data.get("has_wiki", False)
        has_pages = repo_data.get("has_pages", False)
        
        evidence["has_readme"] = has_readme
        evidence["readme_size"] = readme_size
        evidence["has_wiki"] = has_wiki
        evidence["has_pages"] = has_pages
        
        # Documentation score
        doc_score = 0
        if has_readme:
            doc_score += 40
            if readme_size > 1000:  # Substantial README
                doc_score += 20
        if has_wiki:
            doc_score += 20
        if has_pages:
            doc_score += 20
        
        evidence["documentation_score"] = doc_score
        
        return {
            "score": doc_score,
            "evidence": evidence
        }
    
    def _assess_tests(self, repo_data: Dict[str, Any]) -> Dict[str, Any]:
        """Assess test coverage based on indirect signals."""
        evidence = {}
        
        has_ci = repo_data.get("has_ci", False)
        has_package = any([
            repo_data.get("has_package_json", False),
            repo_data.get("has_requirements_txt", False),
            repo_data.get("has_setup_py", False),
            repo_data.get("has_pyproject_toml", False),
            repo_data.get("has_cargo_toml", False),
            repo_data.get("has_go_mod", False)
        ])
        
        evidence["has_ci"] = has_ci
        evidence["has_package_manager"] = has_package
        
        # Test score (proxy-based)
        test_score = 0
        if has_ci:
            test_score += 50  # CI likely runs tests
        if has_package:
            test_score += 30  # Package manager enables testing
        test_score += 20  # Base score for potential
        
        evidence["test_score"] = test_score
        
        return {
            "score": test_score,
            "evidence": evidence
        }
    
    def _assess_maintainability(self, repo_data: Dict[str, Any]) -> Dict[str, Any]:
        """Assess maintainability."""
        evidence = {}
        
        contributors = repo_data.get("contributors", 0)
        commits_last_year = repo_data.get("commits_last_year", 0)
        open_issues = repo_data.get("open_issues", 0)
        is_archived = repo_data.get("archived", False)
        license_key = repo_data.get("license")
        
        evidence["contributors"] = contributors
        evidence["commits_last_year"] = commits_last_year
        evidence["open_issues"] = open_issues
        evidence["is_archived"] = is_archived
        evidence["license"] = license_key
        
        # Maintainability score
        maintainability = 0
        
        # Active contributors
        if contributors >= 1:
            maintainability += 20
        if contributors >= 3:
            maintainability += 10
        
        # Recent activity
        if commits_last_year > 0:
            maintainability += 20
        if commits_last_year > 12:
            maintainability += 10
        
        # Issue backlog
        if open_issues < 10:
            maintainability += 20
        elif open_issues < 50:
            maintainability += 10
        
        # Not archived
        if not is_archived:
            maintainability += 10
        
        # Has license
        if license_key:
            maintainability += 10
        
        evidence["maintainability_score"] = maintainability
        
        return {
            "score": maintainability,
            "evidence": evidence
        }
    
    def analyze(self, repo_data: Dict[str, Any]) -> AgentOutput:
        """
        Analyze code quality across multiple dimensions.
        """
        evidence = {}
        
        # Assess all dimensions
        structure = self._assess_structure(repo_data)
        complexity = self._assess_complexity(repo_data)
        dep_health = self._assess_dependency_health(repo_data)
        documentation = self._assess_documentation(repo_data)
        tests = self._assess_tests(repo_data)
        maintainability = self._assess_maintainability(repo_data)
        
        # Store evidence
        evidence["structure"] = structure["evidence"]
        evidence["complexity"] = complexity["evidence"]
        evidence["dependency_health"] = dep_health["evidence"]
        evidence["documentation"] = documentation["evidence"]
        evidence["tests"] = tests["evidence"]
        evidence["maintainability"] = maintainability["evidence"]
        
        # Calculate overall code quality score
        # Weighted combination
        quality_score = (
            0.20 * structure["score"] +
            0.15 * complexity["score"] +
            0.15 * dep_health["score"] +
            0.20 * documentation["score"] +
            0.15 * tests["score"] +
            0.15 * maintainability["score"]
        )
        
        evidence["overall_code_quality"] = quality_score
        
        # Confidence based on data availability
        required_fields = ["size", "has_readme", "has_ci", "contributors"]
        completeness = sum(1 for field in required_fields if field in repo_data)
        confidence = completeness / len(required_fields)
        
        return AgentOutput(
            score=round(quality_score, 2),
            evidence=evidence,
            confidence=confidence,
            hash=""
        )
