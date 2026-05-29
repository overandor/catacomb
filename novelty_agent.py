"""Novelty Agent - Deterministic novelty engine: similar repos, architecture uniqueness, category saturation, problem rarity."""
from typing import Dict, Any, List
import requests
from base_agent import BaseAgent, AgentOutput


class NoveltyAgent(BaseAgent):
    """Deterministically assesses novelty without LLMs."""
    
    def __init__(self, github_token: str = None):
        super().__init__("Novelty")
        self.github_token = github_token
        self.headers = {"Accept": "application/vnd.github.v3+json"}
        if self.github_token:
            self.headers["Authorization"] = f"token {self.github_token}"
    
    def _count_similar_repos(self, repo_data: Dict[str, Any]) -> Dict[str, Any]:
        """Count repositories with similar language and topics."""
        evidence = {}
        
        language = repo_data.get("language")
        topics = repo_data.get("topics", [])
        
        evidence["language"] = language
        evidence["topics"] = topics
        
        if not language and not topics:
            evidence["similar_repo_count"] = 0
            evidence["category_saturation"] = 0.5  # Unknown
            return {
                "score": 50,
                "evidence": evidence
            }
        
        # Search for similar repos
        query_parts = []
        if language:
            query_parts.append(f"language:{language}")
        if topics:
            query_parts.append(" ".join([f"topic:{t}" for t in topics[:3]]))  # Top 3 topics
        
        if not query_parts:
            evidence["similar_repo_count"] = 0
            evidence["category_saturation"] = 0.5
            return {
                "score": 50,
                "evidence": evidence
            }
        
        query = " ".join(query_parts)
        
        try:
            url = "https://api.github.com/search/repositories"
            params = {
                "q": query,
                "per_page": 1  # Just get count
            }
            response = requests.get(url, headers=self.headers, params=params)
            if response.status_code == 200:
                total_count = response.json().get("total_count", 0)
                evidence["similar_repo_count"] = total_count
                
                # Saturation: more repos = more saturated
                if total_count > 10000:
                    saturation = 1.0
                elif total_count > 5000:
                    saturation = 0.8
                elif total_count > 1000:
                    saturation = 0.6
                elif total_count > 100:
                    saturation = 0.4
                elif total_count > 10:
                    saturation = 0.2
                else:
                    saturation = 0.0
                
                evidence["category_saturation"] = saturation
            else:
                evidence["similar_repo_count"] = 0
                evidence["category_saturation"] = 0.5
        except:
            evidence["similar_repo_count"] = 0
            evidence["category_saturation"] = 0.5
        
        # Novelty score: inverse of saturation
        novelty_score = (1 - evidence["category_saturation"]) * 100
        
        return {
            "score": novelty_score,
            "evidence": evidence
        }
    
    def _assess_architecture_uniqueness(self, repo_data: Dict[str, Any]) -> Dict[str, Any]:
        """Assess architecture uniqueness based on structure."""
        evidence = {}
        
        size = repo_data.get("size", 0)
        languages = repo_data.get("languages", {})
        has_package = any([
            repo_data.get("has_package_json", False),
            repo_data.get("has_requirements_txt", False),
            repo_data.get("has_setup_py", False),
            repo_data.get("has_pyproject_toml", False),
            repo_data.get("has_cargo_toml", False),
            repo_data.get("has_go_mod", False)
        ])
        has_dockerfile = repo_data.get("has_dockerfile", False)
        has_makefile = repo_data.get("has_makefile", False)
        
        evidence["size_kb"] = size
        evidence["language_count"] = len(languages)
        evidence["has_package_manager"] = has_package
        evidence["has_dockerfile"] = has_dockerfile
        evidence["has_makefile"] = has_makefile
        
        # Architecture uniqueness score
        uniqueness = 50  # Base
        
        # Multi-language projects are often more unique
        if len(languages) > 3:
            uniqueness += 20
        elif len(languages) > 1:
            uniqueness += 10
        
        # Containerization suggests modern architecture
        if has_dockerfile:
            uniqueness += 15
        
        # Makefile suggests custom build system
        if has_makefile:
            uniqueness += 10
        
        # Size extremes suggest unique projects
        if size < 10:  # Very small = focused tool
            uniqueness += 10
        elif size > 50000:  # Very large = complex system
            uniqueness += 5
        
        uniqueness = min(uniqueness, 100)
        evidence["architecture_uniqueness"] = uniqueness
        
        return {
            "score": uniqueness,
            "evidence": evidence
        }
    
    def _assess_problem_rarity(self, repo_data: Dict[str, Any]) -> Dict[str, Any]:
        """Assess if solving a rare problem based on description and topics."""
        evidence = {}
        
        description = (repo_data.get("description") or "").lower()
        topics = repo_data.get("topics", [])
        stars = repo_data.get("stars", 0)
        
        evidence["description"] = description
        evidence["topics"] = topics
        evidence["stars"] = stars
        
        # Common CRUD indicators (lower rarity)
        common_keywords = [
            "crud", "rest api", "api", "backend", "frontend",
            "cms", "blog", "ecommerce", "todo", "chat"
        ]
        
        # Rare problem indicators (higher rarity)
        rare_keywords = [
            "quantum", "neural", "cryptography", "blockchain",
            "distributed", "consensus", "compiler", "interpreter",
            "operating system", "kernel", "database engine",
            "protocol", "format", "specification"
        ]
        
        common_count = sum(1 for kw in common_keywords if kw in description)
        rare_count = sum(1 for kw in rare_keywords if kw in description)
        
        evidence["common_keyword_count"] = common_count
        evidence["rare_keyword_count"] = rare_count
        
        # Problem rarity score
        rarity = 50  # Base
        
        if rare_count > 0:
            rarity += rare_count * 15
        if common_count > 0:
            rarity -= common_count * 10
        
        # Low stars on rare problem = undervalued
        if rare_count > 0 and stars < 100:
            rarity += 20
        
        rarity = max(0, min(rarity, 100))
        evidence["problem_rarity"] = rarity
        
        return {
            "score": rarity,
            "evidence": evidence
        }
    
    def _assess_crud_likelihood(self, repo_data: Dict[str, Any]) -> Dict[str, Any]:
        """Assess likelihood of being just another CRUD app."""
        evidence = {}
        
        description = (repo_data.get("description") or "").lower()
        topics = [t.lower() for t in repo_data.get("topics", []) if t]
        language = (repo_data.get("language") or "").lower()
        
        evidence["description"] = description
        evidence["topics"] = topics
        evidence["language"] = language
        
        # CRUD indicators
        crud_indicators = 0
        
        if any(kw in description for kw in ["crud", "rest", "api", "backend", "cms", "admin"]):
            crud_indicators += 2
        if any(kw in topics for kw in ["crud", "rest", "api", "cms", "admin"]):
            crud_indicators += 2
        if language in ["javascript", "typescript", "php", "ruby"]:
            crud_indicators += 1
        
        evidence["crud_indicators"] = crud_indicators
        
        # CRUD likelihood (higher = more likely to be CRUD)
        crud_likelihood = min(crud_indicators / 5, 1.0)
        evidence["crud_likelihood"] = crud_likelihood
        
        # Non-CRDD score (inverse)
        non_crud_score = (1 - crud_likelihood) * 100
        
        return {
            "score": non_crud_score,
            "evidence": evidence
        }
    
    def analyze(self, repo_data: Dict[str, Any]) -> AgentOutput:
        """
        Analyze novelty across multiple dimensions.
        """
        evidence = {}
        
        # Assess all dimensions
        similar = self._count_similar_repos(repo_data)
        architecture = self._assess_architecture_uniqueness(repo_data)
        problem = self._assess_problem_rarity(repo_data)
        crud = self._assess_crud_likelihood(repo_data)
        
        # Store evidence
        evidence["similar_repos"] = similar["evidence"]
        evidence["architecture"] = architecture["evidence"]
        evidence["problem_rarity"] = problem["evidence"]
        evidence["crud_assessment"] = crud["evidence"]
        
        # Calculate overall novelty score
        # Weighted combination
        novelty_score = (
            0.30 * similar["score"] +  # Category sparsity
            0.25 * architecture["score"] +  # Unique architecture
            0.30 * problem["score"] +  # Rare problem
            0.15 * crud["score"]  # Not just CRUD
        )
        
        evidence["overall_novelty"] = novelty_score
        
        # Confidence based on data availability
        has_description = bool(repo_data.get("description"))
        has_topics = bool(repo_data.get("topics"))
        has_language = bool(repo_data.get("language"))
        
        confidence = 0.5
        if has_description:
            confidence += 0.2
        if has_topics:
            confidence += 0.2
        if has_language:
            confidence += 0.1
        
        return AgentOutput(
            score=round(novelty_score, 2),
            evidence=evidence,
            confidence=confidence,
            hash=""
        )
