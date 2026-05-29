"""Venture Agent - Predicts startup, funding, acquisition potential."""
from typing import Dict, Any, List
from base_agent import BaseAgent, AgentOutput


class VentureAgent(BaseAgent):
    """Analyzes venture potential: startup formation, funding, acquisition probability."""
    
    def __init__(self):
        super().__init__("Venture")
    
    def _calculate_startup_probability(self, repo_data: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate probability of repo becoming a startup."""
        evidence = {}
        
        stars = repo_data.get("stars", 0)
        forks = repo_data.get("forks", 0)
        contributors = repo_data.get("contributors", 0)
        commits_last_year = repo_data.get("commits_last_year", 0)
        language = (repo_data.get("language") or "").lower()
        category = (repo_data.get("category") or "").lower()
        has_business_model = repo_data.get("has_business_model", False)
        has_pricing = repo_data.get("has_pricing", False)
        has_enterprise_features = repo_data.get("has_enterprise_features", False)
        
        evidence["stars"] = stars
        evidence["forks"] = forks
        evidence["contributors"] = contributors
        evidence["commits_last_year"] = commits_last_year
        evidence["language"] = language
        evidence["category"] = category
        evidence["has_business_model"] = has_business_model
        evidence["has_pricing"] = has_pricing
        evidence["has_enterprise_features"] = has_enterprise_features
        
        startup_prob = 0.0
        
        # Growth trajectory
        if commits_last_year > 500:
            startup_prob += 0.2
        elif commits_last_year > 100:
            startup_prob += 0.1
        
        # Adoption signals
        if stars > 1000:
            startup_prob += 0.15
        elif stars > 100:
            startup_prob += 0.08
        
        if forks > 100:
            startup_prob += 0.1
        elif forks > 20:
            startup_prob += 0.05
        
        # Team size
        if contributors > 10:
            startup_prob += 0.15
        elif contributors > 3:
            startup_prob += 0.08
        
        # Category startup-friendliness
        startup_friendly_categories = [
            "database", "api", "infrastructure", "ai", "ml", 
            "security", "devops", "platform", "framework"
        ]
        if any(cat in category for cat in startup_friendly_categories):
            startup_prob += 0.15
        
        # Business signals
        if has_business_model:
            startup_prob += 0.2
        if has_pricing:
            startup_prob += 0.15
        if has_enterprise_features:
            startup_prob += 0.1
        
        # Language startup ecosystem
        startup_languages = ["typescript", "rust", "go", "python"]
        if language in startup_languages:
            startup_prob += 0.08
        
        evidence["startup_probability"] = min(startup_prob, 1.0)
        
        return {
            "score": round(evidence["startup_probability"] * 100, 2),
            "evidence": evidence
        }
    
    def _calculate_funding_probability(self, repo_data: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate probability of receiving funding."""
        evidence = {}
        
        stars = repo_data.get("stars", 0)
        contributors = repo_data.get("contributors", 0)
        commits_last_year = repo_data.get("commits_last_year", 0)
        category = (repo_data.get("category") or "").lower()
        has_business_model = repo_data.get("has_business_model", False)
        has_pricing = repo_data.get("has_pricing", False)
        has_enterprise_features = repo_data.get("has_enterprise_features", False)
        has_revenue = repo_data.get("has_revenue", False)
        has_customers = repo_data.get("has_customers", False)
        
        evidence["stars"] = stars
        evidence["contributors"] = contributors
        evidence["commits_last_year"] = commits_last_year
        evidence["category"] = category
        evidence["has_business_model"] = has_business_model
        evidence["has_pricing"] = has_pricing
        evidence["has_enterprise_features"] = has_enterprise_features
        evidence["has_revenue"] = has_revenue
        evidence["has_customers"] = has_customers
        
        funding_prob = 0.0
        
        # Traction requirements
        if stars > 5000:
            funding_prob += 0.2
        elif stars > 1000:
            funding_prob += 0.1
        
        if contributors > 20:
            funding_prob += 0.15
        elif contributors > 5:
            funding_prob += 0.08
        
        if commits_last_year > 1000:
            funding_prob += 0.1
        
        # Business readiness
        if has_business_model:
            funding_prob += 0.2
        if has_pricing:
            funding_prob += 0.15
        if has_enterprise_features:
            funding_prob += 0.1
        if has_revenue:
            funding_prob += 0.25
        if has_customers:
            funding_prob += 0.2
        
        # Category investability
        investable_categories = [
            "database", "ai", "ml", "security", "infrastructure",
            "devops", "platform", "analytics", "observability"
        ]
        if any(cat in category for cat in investable_categories):
            funding_prob += 0.15
        
        evidence["funding_probability"] = min(funding_prob, 1.0)
        
        return {
            "score": round(evidence["funding_probability"] * 100, 2),
            "evidence": evidence
        }
    
    def _calculate_acquisition_probability(self, repo_data: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate probability of acquisition."""
        evidence = {}
        
        stars = repo_data.get("stars", 0)
        forks = repo_data.get("forks", 0)
        contributors = repo_data.get("contributors", 0)
        category = (repo_data.get("category") or "").lower()
        language = (repo_data.get("language") or "").lower()
        has_enterprise_features = repo_data.get("has_enterprise_features", False)
        has_integrations = repo_data.get("has_integrations", False)
        is_infrastructure = repo_data.get("is_infrastructure", False)
        
        evidence["stars"] = stars
        evidence["forks"] = forks
        evidence["contributors"] = contributors
        evidence["category"] = category
        evidence["language"] = language
        evidence["has_enterprise_features"] = has_enterprise_features
        evidence["has_integrations"] = has_integrations
        evidence["is_infrastructure"] = is_infrastructure
        
        acquisition_prob = 0.0
        
        # Adoption threshold
        if stars > 10000:
            acquisition_prob += 0.2
        elif stars > 1000:
            acquisition_prob += 0.1
        
        if forks > 500:
            acquisition_prob += 0.15
        elif forks > 100:
            acquisition_prob += 0.08
        
        # Team size (smaller teams more acquirable)
        if 2 <= contributors <= 10:
            acquisition_prob += 0.15
        elif contributors < 20:
            acquisition_prob += 0.08
        
        # Infrastructure value
        if is_infrastructure:
            acquisition_prob += 0.2
        
        # Integration ecosystem
        if has_integrations:
            acquisition_prob += 0.15
        
        # Enterprise readiness
        if has_enterprise_features:
            acquisition_prob += 0.1
        
        # Category acquisition targets
        acquisition_target_categories = [
            "database", "security", "api", "infrastructure",
            "devops", "monitoring", "logging", "analytics"
        ]
        if any(cat in category for cat in acquisition_target_categories):
            acquisition_prob += 0.15
        
        # Language ecosystem value
        valuable_languages = ["rust", "go", "c++", "zig"]
        if language in valuable_languages:
            acquisition_prob += 0.1
        
        evidence["acquisition_probability"] = min(acquisition_prob, 1.0)
        
        return {
            "score": round(evidence["acquisition_probability"] * 100, 2),
            "evidence": evidence
        }
    
    def _calculate_ecosystem_dominance_probability(self, repo_data: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate probability of becoming ecosystem-dominant."""
        evidence = {}
        
        stars = repo_data.get("stars", 0)
        forks = repo_data.get("forks", 0)
        contributors = repo_data.get("contributors", 0)
        category = (repo_data.get("category") or "").lower()
        is_framework = repo_data.get("is_framework", False)
        is_infrastructure = repo_data.get("is_infrastructure", False)
        has_plugin_system = repo_data.get("has_plugin_system", False)
        has_ecosystem = repo_data.get("has_ecosystem", False)
        
        evidence["stars"] = stars
        evidence["forks"] = forks
        evidence["contributors"] = contributors
        evidence["category"] = category
        evidence["is_framework"] = is_framework
        evidence["is_infrastructure"] = is_infrastructure
        evidence["has_plugin_system"] = has_plugin_system
        evidence["has_ecosystem"] = has_ecosystem
        
        dominance_prob = 0.0
        
        # Mass adoption
        if stars > 50000:
            dominance_prob += 0.25
        elif stars > 10000:
            dominance_prob += 0.15
        
        if forks > 5000:
            dominance_prob += 0.2
        elif forks > 1000:
            dominance_prob += 0.1
        
        # Community scale
        if contributors > 100:
            dominance_prob += 0.2
        elif contributors > 20:
            dominance_prob += 0.1
        
        # Foundation status
        if is_framework:
            dominance_prob += 0.2
        if is_infrastructure:
            dominance_prob += 0.15
        
        # Extensibility
        if has_plugin_system:
            dominance_prob += 0.15
        if has_ecosystem:
            dominance_prob += 0.2
        
        # Category dominance potential
        dominance_categories = [
            "framework", "database", "runtime", "language",
            "platform", "infrastructure"
        ]
        if any(cat in category for cat in dominance_categories):
            dominance_prob += 0.15
        
        evidence["ecosystem_dominance_probability"] = min(dominance_prob, 1.0)
        
        return {
            "score": round(evidence["ecosystem_dominance_probability"] * 100, 2),
            "evidence": evidence
        }
    
    def _calculate_market_size_estimate(self, repo_data: Dict[str, Any]) -> Dict[str, Any]:
        """Estimate addressable market size."""
        evidence = {}
        
        category = (repo_data.get("category") or "").lower()
        is_enterprise = repo_data.get("has_enterprise_features", False)
        is_consumer = repo_data.get("is_consumer", False)
        has_saa_s_model = repo_data.get("has_business_model", False)
        
        evidence["category"] = category
        evidence["is_enterprise"] = is_enterprise
        evidence["is_consumer"] = is_consumer
        evidence["has_saa_s_model"] = has_saa_s_model
        
        # Market size estimates (TAM in billions USD)
        market_sizes = {
            "database": 80,
            "ai": 200,
            "ml": 150,
            "security": 150,
            "infrastructure": 100,
            "devops": 80,
            "api": 60,
            "analytics": 70,
            "observability": 50,
            "framework": 40,
            "platform": 90
        }
        
        base_market = market_sizes.get(category, 20)
        
        # Adjust for target market
        if is_enterprise:
            base_market *= 1.2
        if is_consumer:
            base_market *= 1.5
        if has_saa_s_model:
            base_market *= 1.3
        
        evidence["estimated_market_size_billions"] = round(base_market, 1)
        
        # Market tier
        if base_market > 100:
            market_tier = "massive"
        elif base_market > 50:
            market_tier = "large"
        elif base_market > 20:
            market_tier = "medium"
        else:
            market_tier = "niche"
        
        evidence["market_tier"] = market_tier
        
        return {
            "score": min(base_market * 2, 100),  # Normalize to 0-100
            "evidence": evidence
        }
    
    def analyze(self, repo_data: Dict[str, Any]) -> AgentOutput:
        """
        Analyze venture potential across multiple dimensions.
        """
        evidence = {}
        
        # Calculate all venture metrics
        startup_prob = self._calculate_startup_probability(repo_data)
        funding_prob = self._calculate_funding_probability(repo_data)
        acquisition_prob = self._calculate_acquisition_probability(repo_data)
        dominance_prob = self._calculate_ecosystem_dominance_probability(repo_data)
        market_size = self._calculate_market_size_estimate(repo_data)
        
        # Store evidence
        evidence["startup_probability"] = startup_prob["evidence"]
        evidence["funding_probability"] = funding_prob["evidence"]
        evidence["acquisition_probability"] = acquisition_prob["evidence"]
        evidence["ecosystem_dominance_probability"] = dominance_prob["evidence"]
        evidence["market_size_estimate"] = market_size["evidence"]
        
        # Calculate overall venture score
        # Weight funding and ecosystem dominance highest
        venture_score = (
            0.20 * startup_prob["score"] +
            0.30 * funding_prob["score"] +
            0.25 * acquisition_prob["score"] +
            0.25 * dominance_prob["score"]
        )
        
        evidence["overall_venture_score"] = venture_score
        
        # Determine venture category
        if venture_score > 75:
            venture_category = "unicorn_candidate"
        elif venture_score > 50:
            venture_category = "high_potential"
        elif venture_score > 25:
            venture_category = "moderate_potential"
        else:
            venture_category = "low_potential"
        
        evidence["venture_category"] = venture_category
        
        # Confidence based on business signals
        has_business_signals = (
            repo_data.get("has_business_model", False) or
            repo_data.get("has_pricing", False) or
            repo_data.get("has_enterprise_features", False)
        )
        
        confidence = 0.5
        if has_business_signals:
            confidence += 0.3
        if repo_data.get("stars", 0) > 100:
            confidence += 0.2
        
        return AgentOutput(
            score=round(venture_score, 2),
            evidence=evidence,
            confidence=confidence,
            hash=""
        )
