"""Utility Agent - Predicts actual developer usage, dependency potential, integration potential."""
from typing import Dict, Any, List
from base_agent import BaseAgent, AgentOutput


class UtilityAgent(BaseAgent):
    """Analyzes repo utility: dependency potential, integration potential, replacement cost."""
    
    def __init__(self):
        super().__init__("Utility")
    
    def _calculate_dependency_potential(self, repo_data: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate potential to become a dependency for other projects."""
        evidence = {}
        
        language = (repo_data.get("language") or "").lower()
        has_package_manager = repo_data.get("has_package_manager", False)
        has_api = repo_data.get("has_api", False)
        is_library = repo_data.get("is_library", False)
        has_examples = repo_data.get("has_examples", False)
        
        evidence["language"] = language
        evidence["has_package_manager"] = has_package_manager
        evidence["has_api"] = has_api
        evidence["is_library"] = is_library
        evidence["has_examples"] = has_examples
        
        # Language dependency ecosystem score
        language_dependency_scores = {
            "javascript": 0.9,
            "typescript": 0.9,
            "python": 0.85,
            "rust": 0.8,
            "go": 0.75,
            "java": 0.7,
            "c++": 0.5,
            "ruby": 0.7
        }
        
        dependency_score = language_dependency_scores.get(language, 0.5)
        
        # Package manager availability
        if has_package_manager:
            dependency_score += 0.2
        
        # API surface
        if has_api:
            dependency_score += 0.15
        
        # Library structure
        if is_library:
            dependency_score += 0.15
        
        # Examples for integration
        if has_examples:
            dependency_score += 0.1
        
        evidence["dependency_potential_score"] = min(dependency_score, 1.0)
        
        return {
            "score": round(evidence["dependency_potential_score"] * 100, 2),
            "evidence": evidence
        }
    
    def _calculate_integration_potential(self, repo_data: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate ease of integration into other projects."""
        evidence = {}
        
        has_api = repo_data.get("has_api", False)
        has_sdk = repo_data.get("has_sdk", False)
        has_bindings = repo_data.get("has_bindings", False)
        has_webhooks = repo_data.get("has_webhooks", False)
        has_plugins = repo_data.get("has_plugins", False)
        has_rest_api = repo_data.get("has_rest_api", False)
        
        evidence["has_api"] = has_api
        evidence["has_sdk"] = has_sdk
        evidence["has_bindings"] = has_bindings
        evidence["has_webhooks"] = has_webhooks
        evidence["has_plugins"] = has_plugins
        evidence["has_rest_api"] = has_rest_api
        
        integration_score = 0.0
        
        # API availability
        if has_rest_api:
            integration_score += 0.3
        elif has_api:
            integration_score += 0.2
        
        # SDK availability
        if has_sdk:
            integration_score += 0.25
        
        # Multi-language bindings
        if has_bindings:
            integration_score += 0.2
        
        # Extension points
        if has_plugins:
            integration_score += 0.15
        
        # Webhooks for automation
        if has_webhooks:
            integration_score += 0.1
        
        evidence["integration_potential_score"] = min(integration_score, 1.0)
        
        return {
            "score": round(evidence["integration_potential_score"] * 100, 2),
            "evidence": evidence
        }
    
    def _calculate_replacement_cost(self, repo_data: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate cost to replace this repo with alternative."""
        evidence = {}
        
        stars = repo_data.get("stars", 0)
        forks = repo_data.get("forks", 0)
        contributors = repo_data.get("contributors", 0)
        complexity = repo_data.get("complexity", "medium")
        unique_features = repo_data.get("unique_features", 0)
        
        evidence["stars"] = stars
        evidence["forks"] = forks
        evidence["contributors"] = contributors
        evidence["complexity"] = complexity
        evidence["unique_features"] = unique_features
        
        # High adoption = high replacement cost
        replacement_cost = 0.0
        
        if stars > 1000:
            replacement_cost += 0.4
        elif stars > 100:
            replacement_cost += 0.25
        elif stars > 10:
            replacement_cost += 0.1
        
        if forks > 100:
            replacement_cost += 0.2
        elif forks > 10:
            replacement_cost += 0.1
        
        if contributors > 10:
            replacement_cost += 0.2
        elif contributors > 3:
            replacement_cost += 0.1
        
        # Complexity multiplier
        if complexity == "high":
            replacement_cost *= 1.3
        elif complexity == "medium":
            replacement_cost *= 1.0
        else:
            replacement_cost *= 0.7
        
        # Unique features increase replacement cost
        if unique_features > 5:
            replacement_cost += 0.15
        elif unique_features > 2:
            replacement_cost += 0.08
        
        evidence["replacement_cost_score"] = min(replacement_cost, 1.0)
        
        return {
            "score": round(evidence["replacement_cost_score"] * 100, 2),
            "evidence": evidence
        }
    
    def _calculate_maintenance_burden(self, repo_data: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate ongoing maintenance burden."""
        evidence = {}
        
        size = repo_data.get("size", 0)
        complexity = repo_data.get("complexity", "medium")
        has_tests = repo_data.get("has_tests", False)
        has_ci = repo_data.get("has_ci", False)
        has_documentation = repo_data.get("has_documentation", False)
        technical_debt = repo_data.get("technical_debt", "medium")
        
        evidence["size"] = size
        evidence["complexity"] = complexity
        evidence["has_tests"] = has_tests
        evidence["has_ci"] = has_ci
        evidence["has_documentation"] = has_documentation
        evidence["technical_debt"] = technical_debt
        
        maintenance_burden = 0.0
        
        # Size impact
        if size > 100000:  # > 100MB
            maintenance_burden += 0.3
        elif size > 10000:  # > 10MB
            maintenance_burden += 0.2
        elif size > 1000:  # > 1MB
            maintenance_burden += 0.1
        
        # Complexity impact
        if complexity == "high":
            maintenance_burden += 0.3
        elif complexity == "medium":
            maintenance_burden += 0.15
        
        # Technical debt
        if technical_debt == "high":
            maintenance_burden += 0.25
        elif technical_debt == "medium":
            maintenance_burden += 0.15
        
        # Mitigating factors
        if has_tests:
            maintenance_burden -= 0.1
        if has_ci:
            maintenance_burden -= 0.08
        if has_documentation:
            maintenance_burden -= 0.07
        
        evidence["maintenance_burden_score"] = max(0, min(maintenance_burden, 1.0))
        
        return {
            "score": round(evidence["maintenance_burden_score"] * 100, 2),
            "evidence": evidence
        }
    
    def _calculate_actual_usage_signals(self, repo_data: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate signals of actual developer usage beyond stars."""
        evidence = {}
        
        forks = repo_data.get("forks", 0)
        open_issues = repo_data.get("open_issues", 0)
        closed_issues = repo_data.get("closed_issues", 0)
        contributors = repo_data.get("contributors", 0)
        commits_last_year = repo_data.get("commits_last_year", 0)
        releases = repo_data.get("releases", 0)
        
        evidence["forks"] = forks
        evidence["open_issues"] = open_issues
        evidence["closed_issues"] = closed_issues
        evidence["contributors"] = contributors
        evidence["commits_last_year"] = commits_last_year
        evidence["releases"] = releases
        
        usage_score = 0.0
        
        # Forks indicate actual usage
        if forks > 100:
            usage_score += 0.25
        elif forks > 10:
            usage_score += 0.15
        elif forks > 1:
            usage_score += 0.05
        
        # Issue engagement
        total_issues = open_issues + closed_issues
        if total_issues > 100:
            usage_score += 0.2
        elif total_issues > 20:
            usage_score += 0.1
        elif total_issues > 5:
            usage_score += 0.05
        
        # Multiple contributors
        if contributors > 10:
            usage_score += 0.2
        elif contributors > 3:
            usage_score += 0.1
        elif contributors > 1:
            usage_score += 0.05
        
        # Active development
        if commits_last_year > 100:
            usage_score += 0.15
        elif commits_last_year > 20:
            usage_score += 0.08
        
        # Release cadence
        if releases > 10:
            usage_score += 0.1
        elif releases > 3:
            usage_score += 0.05
        
        evidence["actual_usage_score"] = min(usage_score, 1.0)
        
        return {
            "score": round(evidence["actual_usage_score"] * 100, 2),
            "evidence": evidence
        }
    
    def _calculate_ecosystem_importance(self, repo_data: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate importance in its ecosystem."""
        evidence = {}
        
        language = (repo_data.get("language") or "").lower()
        stars = repo_data.get("stars", 0)
        forks = repo_data.get("forks", 0)
        is_infrastructure = repo_data.get("is_infrastructure", False)
        is_framework = repo_data.get("is_framework", False)
        category = repo_data.get("category", "unknown")
        
        evidence["language"] = language
        evidence["stars"] = stars
        evidence["forks"] = forks
        evidence["is_infrastructure"] = is_infrastructure
        evidence["is_framework"] = is_framework
        evidence["category"] = category
        
        ecosystem_score = 0.0
        
        # Infrastructure/framework status
        if is_infrastructure:
            ecosystem_score += 0.3
        if is_framework:
            ecosystem_score += 0.25
        
        # Category importance
        important_categories = ["database", "http", "async", "testing", "cli", "web"]
        if any(cat in category.lower() for cat in important_categories):
            ecosystem_score += 0.2
        
        # Adoption in ecosystem
        if stars > 1000:
            ecosystem_score += 0.2
        elif stars > 100:
            ecosystem_score += 0.1
        
        if forks > 50:
            ecosystem_score += 0.15
        elif forks > 10:
            ecosystem_score += 0.08
        
        evidence["ecosystem_importance_score"] = min(ecosystem_score, 1.0)
        
        return {
            "score": round(evidence["ecosystem_importance_score"] * 100, 2),
            "evidence": evidence
        }
    
    def analyze(self, repo_data: Dict[str, Any]) -> AgentOutput:
        """
        Analyze repo utility across multiple dimensions.
        """
        evidence = {}
        
        # Calculate all utility metrics
        dependency_potential = self._calculate_dependency_potential(repo_data)
        integration_potential = self._calculate_integration_potential(repo_data)
        replacement_cost = self._calculate_replacement_cost(repo_data)
        maintenance_burden = self._calculate_maintenance_burden(repo_data)
        actual_usage = self._calculate_actual_usage_signals(repo_data)
        ecosystem_importance = self._calculate_ecosystem_importance(repo_data)
        
        # Store evidence
        evidence["dependency_potential"] = dependency_potential["evidence"]
        evidence["integration_potential"] = integration_potential["evidence"]
        evidence["replacement_cost"] = replacement_cost["evidence"]
        evidence["maintenance_burden"] = maintenance_burden["evidence"]
        evidence["actual_usage"] = actual_usage["evidence"]
        evidence["ecosystem_importance"] = ecosystem_importance["evidence"]
        
        # Calculate overall utility score
        # Weight actual usage and dependency potential highest
        utility_score = (
            0.25 * actual_usage["score"] +
            0.25 * dependency_potential["score"] +
            0.15 * integration_potential["score"] +
            0.15 * ecosystem_importance["score"] +
            0.10 * replacement_cost["score"] -
            0.10 * maintenance_burden["score"]  # Subtract burden
        )
        
        utility_score = max(0, min(utility_score, 100))
        
        evidence["overall_utility_score"] = utility_score
        
        # Determine utility category
        if utility_score > 75:
            utility_category = "critical_infrastructure"
        elif utility_score > 50:
            utility_category = "highly_useful"
        elif utility_score > 25:
            utility_category = "moderately_useful"
        else:
            utility_category = "limited_utility"
        
        evidence["utility_category"] = utility_category
        
        # Confidence based on data availability
        has_usage_data = repo_data.get("forks", 0) > 0 or repo_data.get("contributors", 0) > 0
        has_structure_data = repo_data.get("has_package_manager", False) or repo_data.get("has_api", False)
        
        confidence = 0.5
        if has_usage_data:
            confidence += 0.3
        if has_structure_data:
            confidence += 0.2
        
        return AgentOutput(
            score=round(utility_score, 2),
            evidence=evidence,
            confidence=confidence,
            hash=""
        )
