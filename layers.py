"""Three-layer architecture for Catacomb: Evidence, Opportunity, Strategy."""
from typing import Dict, Any, List
from repo_scanner import RepoScannerAgent
from buildability_agent import BuildabilityAgent
from code_quality_agent import CodeQualityAgent
from language_layer import LanguageLayer
from novelty_agent import NoveltyAgent
from market_demand_agent import MarketDemandAgent
from revival_agent import RevivalAgent
from strategy_agent import StrategyAgent
from trajectory_agent import TrajectoryAgent
from utility_agent import UtilityAgent
from venture_agent import VentureAgent


class EvidenceLayer:
    """Layer 1: Factual measurements of what exists."""
    
    def __init__(self, github_token: str = None):
        self.scanner = RepoScannerAgent(github_token)
        self.buildability = BuildabilityAgent()
        self.code_quality = CodeQualityAgent()
        self.language = LanguageLayer()
    
    def analyze(self, repo_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate evidence layer outputs."""
        scanner_output = self.scanner.execute(repo_data)
        buildability_output = self.buildability.execute(repo_data)
        code_quality_output = self.code_quality.execute(repo_data)
        language_output = self.language.execute(repo_data)
        
        return {
            "scanner": scanner_output.to_dict(),
            "buildability": buildability_output.to_dict(),
            "code_quality": code_quality_output.to_dict(),
            "language": language_output.to_dict()
        }


class OpportunityLayer:
    """Layer 2: Assessment of latent potential."""
    
    def __init__(self, github_token: str = None, use_ml: bool = True):
        self.novelty = NoveltyAgent(github_token)
        self.market_demand = MarketDemandAgent(github_token)
        self.revival = RevivalAgent()
        self.trajectory = TrajectoryAgent()
        self.utility = UtilityAgent()
        self.venture = VentureAgent()
        if use_ml:
            try:
                from ml_prediction_agent import MLPredictionAgent
                self.ml_prediction = MLPredictionAgent()
            except ImportError:
                self.ml_prediction = None
        else:
            self.ml_prediction = None
        self.use_ml = use_ml
    
    def analyze(self, repo_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate opportunity layer outputs."""
        novelty_output = self.novelty.execute(repo_data)
        market_demand_output = self.market_demand.execute(repo_data)
        revival_output = self.revival.execute(repo_data)
        trajectory_output = self.trajectory.execute(repo_data)
        utility_output = self.utility.execute(repo_data)
        venture_output = self.venture.execute(repo_data)
        
        opportunity = {
            "novelty": novelty_output.to_dict(),
            "market_demand": market_demand_output.to_dict(),
            "revival": revival_output.to_dict(),
            "trajectory": trajectory_output.to_dict(),
            "utility": utility_output.to_dict(),
            "venture": venture_output.to_dict()
        }
        
        # Add ML predictions if enabled
        if self.use_ml and self.ml_prediction:
            ml_output = self.ml_prediction.execute(repo_data)
            opportunity["ml_prediction"] = ml_output.to_dict()
        
        return opportunity


class StrategyLayer:
    """Layer 3: Generation and ranking of intervention paths."""
    
    def __init__(self):
        self.strategy = StrategyAgent()
    
    def analyze(self, repo_data: Dict[str, Any], opportunity_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate strategy layer outputs with multiple intervention paths."""
        # Set revival score for strategy agent
        revival_score = opportunity_data["revival"]["score"]
        self.strategy.target_revival_score = revival_score
        
        strategy_output = self.strategy.execute(repo_data)
        
        # Generate multiple intervention paths with individual scores
        intervention_paths = self._generate_intervention_paths(
            repo_data, 
            opportunity_data, 
            strategy_output
        )
        
        return {
            "strategy": strategy_output.to_dict(),
            "intervention_paths": intervention_paths
        }
    
    def _generate_intervention_paths(
        self, 
        repo_data: Dict[str, Any], 
        opportunity_data: Dict[str, Any],
        strategy_output: Any
    ) -> List[Dict[str, Any]]:
        """Generate multiple transformation paths with individual scores."""
        paths = []
        
        # Extract key metrics
        code_quality = opportunity_data.get("code_quality", {}).get("score", 50)
        language_score = opportunity_data.get("evidence", {}).get("language", {}).get("score", 50)
        market_demand = opportunity_data.get("market_demand", {}).get("score", 50)
        novelty = opportunity_data.get("novelty", {}).get("score", 50)
        trajectory_score = opportunity_data.get("trajectory", {}).get("score", 50)
        trajectory_direction = opportunity_data.get("trajectory", {}).get("evidence", {}).get("trajectory_direction", "stable")
        underexposure = strategy_output.evidence.get("revival", {}).get("underexposure", {}).get("underexposure_signal", 0.5)
        transformation = strategy_output.evidence.get("transformation", {}).get("transformation_potential", 0.5)
        risk = strategy_output.evidence.get("risk", {}).get("risk_penalty", 0.5)
        
        # Language detection
        language = repo_data.get("language", "").lower()
        language_evidence = opportunity_data.get("evidence", {}).get("language", {}).get("evidence", {})
        has_cpp = language_evidence.get("cpp_detection", {}).get("has_cpp", False)
        has_rust = language_evidence.get("rust_detection", {}).get("has_rust", False)
        
        # Path 1: Documentation Improvement
        paths.append({
            "name": "Documentation Overhaul",
            "description": "Comprehensive documentation, examples, and guides",
            "effort_days": 7,
            "probability": 0.9,
            "upside": 0.3,
            "intervention_score": self._calculate_intervention_score(0.3, 0.9, 7, risk),
            "steps": [
                "Create comprehensive README",
                "Add API documentation",
                "Write usage examples",
                "Create contribution guide"
            ]
        })
        
        # Path 2: Package Manager & Build System
        paths.append({
            "name": "Build System Modernization",
            "description": "Add package manager, CI/CD, and automated testing",
            "effort_days": 14,
            "probability": 0.8,
            "upside": 0.5,
            "intervention_score": self._calculate_intervention_score(0.5, 0.8, 14, risk),
            "steps": [
                "Add package manager",
                "Configure CI/CD pipeline",
                "Add automated tests",
                "Set up release automation"
            ]
        })
        
        # Path 3: Feature Expansion
        paths.append({
            "name": "Feature Expansion",
            "description": "Add missing features based on community requests",
            "effort_days": 21,
            "probability": 0.7,
            "upside": 0.6,
            "intervention_score": self._calculate_intervention_score(0.6, 0.7, 21, risk),
            "steps": [
                "Analyze issue backlog",
                "Prioritize high-impact features",
                "Implement top 5 features",
                "Release with announcement"
            ]
        })
        
        # Path 4: SaaS Conversion (if high market demand)
        if market_demand > 60:
            paths.append({
                "name": "SaaS Conversion",
                "description": "Convert to hosted SaaS service",
                "effort_days": 60,
                "probability": 0.5,
                "upside": 0.9,
                "intervention_score": self._calculate_intervention_score(0.9, 0.5, 60, risk),
                "steps": [
                    "Design SaaS architecture",
                    "Implement billing system",
                    "Build admin dashboard",
                    "Deploy to cloud infrastructure"
                ]
            })
        
        # Path 5: AI Integration (if high novelty)
        if novelty > 60:
            paths.append({
                "name": "AI Integration",
                "description": "Add AI/ML capabilities to the project",
                "effort_days": 45,
                "probability": 0.6,
                "upside": 0.85,
                "intervention_score": self._calculate_intervention_score(0.85, 0.6, 45, risk),
                "steps": [
                    "Identify AI use cases",
                    "Integrate with LLM APIs",
                    "Build AI-powered features",
                    "Launch AI capabilities"
                ]
            })
        
        # Path 6: Infrastructure Repositioning (if high code quality)
        if code_quality > 70:
            paths.append({
                "name": "Infrastructure Repositioning",
                "description": "Reposition as infrastructure/library for other developers",
                "effort_days": 30,
                "probability": 0.7,
                "upside": 0.8,
                "intervention_score": self._calculate_intervention_score(0.8, 0.7, 30, risk),
                "steps": [
                    "Refactor for library use",
                    "Create plugin system",
                    "Build developer documentation",
                    "Launch as developer tool"
                ]
            })
        
        # Path 7: Community Building (if high underexposure)
        if underexposure > 0.6:
            paths.append({
                "name": "Community Building",
                "description": "Build community around the project",
                "effort_days": 21,
                "probability": 0.8,
                "upside": 0.7,
                "intervention_score": self._calculate_intervention_score(0.7, 0.8, 21, risk),
                "steps": [
                    "Create Discord/community",
                    "Engage with users",
                    "Host events/workshops",
                    "Build contributor program"
                ]
            })
        
        # Trajectory-aware paths
        if trajectory_direction in ["accelerating", "explosive_growth"]:
            # Momentum Amplification
            paths.append({
                "name": "Momentum Amplification",
                "description": "Accelerate existing growth trajectory with targeted interventions",
                "effort_days": 14,
                "probability": 0.85,
                "upside": 0.9,
                "intervention_score": self._calculate_intervention_score(0.9, 0.85, 14, risk),
                "steps": [
                    "Identify growth drivers",
                    "Amplify successful patterns",
                    "Add growth blockers removal",
                    "Scale community engagement"
                ]
            })
        elif trajectory_direction == "decelerating":
            # Turnaround Strategy
            paths.append({
                "name": "Turnaround Strategy",
                "description": "Reverse declining trajectory with strategic interventions",
                "effort_days": 28,
                "probability": 0.6,
                "upside": 0.8,
                "intervention_score": self._calculate_intervention_score(0.8, 0.6, 28, risk),
                "steps": [
                    "Diagnose decline causes",
                    "Address maintainer burnout",
                    "Re-engage community",
                    "Release major version"
                ]
            })
        elif trajectory_direction == "stagnant" and trajectory_score < 30:
            # Dormant Awakening
            paths.append({
                "name": "Dormant Awakening",
                "description": "Revive stagnant project with strategic intervention",
                "effort_days": 35,
                "probability": 0.5,
                "upside": 0.75,
                "intervention_score": self._calculate_intervention_score(0.75, 0.5, 35, risk),
                "steps": [
                    "Assess codebase health",
                    "Modernize dependencies",
                    "Add missing features",
                    "Re-launch with announcement"
                ]
            })
        
        # C++-specific paths
        if has_cpp or "c++" in language:
            # C++ Modernization
            if language_score < 60:
                paths.append({
                    "name": "C++ Modernization",
                    "description": "Modernize C++ codebase to C++17/20 standards",
                    "effort_days": 30,
                    "probability": 0.7,
                    "upside": 0.75,
                    "intervention_score": self._calculate_intervention_score(0.75, 0.7, 30, risk),
                    "steps": [
                        "Upgrade to C++17/20",
                        "Replace raw pointers with smart pointers",
                        "Modernize STL usage",
                        "Add constexpr and noexcept"
                    ]
                })
            
            # CMake Migration
            if not repo_data.get("has_cmake", False):
                paths.append({
                    "name": "CMake Migration",
                    "description": "Migrate to modern CMake build system",
                    "effort_days": 14,
                    "probability": 0.85,
                    "upside": 0.6,
                    "intervention_score": self._calculate_intervention_score(0.6, 0.85, 14, risk),
                    "steps": [
                        "Create CMakeLists.txt",
                        "Configure targets and dependencies",
                        "Set up Conan/vcpkg integration",
                        "Add CI/CD with CMake"
                    ]
                })
            
            # C++ Library Publication
            if code_quality > 70:
                paths.append({
                    "name": "C++ Library Publication",
                    "description": "Package as C++ library for Conan/vcpkg",
                    "effort_days": 21,
                    "probability": 0.6,
                    "upside": 0.8,
                    "intervention_score": self._calculate_intervention_score(0.8, 0.6, 21, risk),
                    "steps": [
                        "Create Conan package recipe",
                        "Add vcpkg port",
                        "Set up package CI",
                        "Publish to package managers"
                    ]
                })
        
        # Rust-specific paths
        if has_rust or "rust" in language:
            # WASM Compilation
            if language_score > 50:
                paths.append({
                    "name": "WASM Compilation",
                    "description": "Add WebAssembly compilation support",
                    "effort_days": 14,
                    "probability": 0.8,
                    "upside": 0.7,
                    "intervention_score": self._calculate_intervention_score(0.7, 0.8, 14, risk),
                    "steps": [
                        "Add wasm32 target to Cargo",
                        "Configure wasm-bindgen",
                        "Create WASM build script",
                        "Add browser examples"
                    ]
                })
            
            # Crates.io Publication
            if not repo_data.get("is_published", False):
                paths.append({
                    "name": "Crates.io Publication",
                    "description": "Publish Rust crate to crates.io",
                    "effort_days": 7,
                    "probability": 0.9,
                    "upside": 0.65,
                    "intervention_score": self._calculate_intervention_score(0.65, 0.9, 7, risk),
                    "steps": [
                        "Prepare crate metadata",
                        "Add documentation",
                        "Publish to crates.io",
                        "Create release notes"
                    ]
                })
            
            # Rust FFI Layer
            if code_quality > 70:
                paths.append({
                    "name": "Rust FFI Layer",
                    "description": "Add C FFI layer for cross-language integration",
                    "effort_days": 21,
                    "probability": 0.7,
                    "upside": 0.75,
                    "intervention_score": self._calculate_intervention_score(0.75, 0.7, 21, risk),
                    "steps": [
                        "Design C API",
                        "Implement FFI bindings",
                        "Add cbindgen for headers",
                        "Create C examples"
                    ]
                })
            
            # Rust Async Migration
            if language_score < 70:
                paths.append({
                    "name": "Rust Async Migration",
                    "description": "Migrate to async/await with tokio",
                    "effort_days": 28,
                    "probability": 0.65,
                    "upside": 0.8,
                    "intervention_score": self._calculate_intervention_score(0.8, 0.65, 28, risk),
                    "steps": [
                        "Identify blocking operations",
                        "Migrate to async functions",
                        "Integrate tokio runtime",
                        "Add async tests"
                    ]
                })
        
        # Sort by intervention score
        paths.sort(key=lambda x: x["intervention_score"], reverse=True)
        
        return paths
    
    def _calculate_intervention_score(
        self, 
        upside: float, 
        probability: float, 
        effort_days: int, 
        risk: float
    ) -> float:
        """
        Calculate Intervention Score = (Upside × Probability) / Effort × (1 - Risk)
        """
        expected_value = upside * probability
        effort_factor = 1 / (effort_days ** 0.5)  # Square root to penalize extreme effort less
        risk_adjustment = 1 - risk
        
        intervention_score = expected_value * effort_factor * risk_adjustment * 100
        
        return round(intervention_score, 2)


class CatacombEngine:
    """Main engine orchestrating all three layers."""
    
    def __init__(self, github_token: str = None, use_ml: bool = True):
        self.evidence_layer = EvidenceLayer(github_token)
        self.opportunity_layer = OpportunityLayer(github_token, use_ml)
        self.strategy_layer = StrategyLayer()
        self.use_ml = use_ml
    
    def analyze(self, repo_data: Dict[str, Any]) -> Dict[str, Any]:
        """Run full three-layer analysis."""
        # Layer 1: Evidence
        evidence = self.evidence_layer.analyze(repo_data)
        
        # Layer 2: Opportunity
        opportunity = self.opportunity_layer.analyze(repo_data)
        
        # Layer 3: Strategy
        strategy = self.strategy_layer.analyze(repo_data, opportunity)
        
        # Select best intervention
        best_intervention = strategy["intervention_paths"][0] if strategy["intervention_paths"] else None
        
        # Calculate ML-enhanced intervention score if available
        intervention_score = best_intervention["intervention_score"] if best_intervention else 0
        if self.use_ml and "ml_prediction" in opportunity:
            ml_virality = opportunity["ml_prediction"]["evidence"].get("virality_score", 0.5)
            ml_usefulness = opportunity["ml_prediction"]["evidence"].get("usefulness_score", 0.5)
            
            # Boost intervention score based on ML predictions
            ml_boost = (ml_virality + ml_usefulness) / 2
            intervention_score = intervention_score * (0.7 + 0.3 * ml_boost)
            intervention_score = min(intervention_score, 100)
        
        return {
            "evidence": evidence,
            "opportunity": opportunity,
            "strategy": strategy,
            "best_intervention": best_intervention,
            "intervention_score": round(intervention_score, 2)
        }
