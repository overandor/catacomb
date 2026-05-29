"""Buildability Agent - Checks if repo can be installed, built, tested, run, and reproduced."""
import os
import subprocess
import tempfile
import shutil
from typing import Dict, Any
from base_agent import BaseAgent, AgentOutput


class BuildabilityAgent(BaseAgent):
    """Determines if a repository is buildable and testable."""
    
    def __init__(self, clone_dir: str = None):
        super().__init__("Buildability")
        self.clone_dir = clone_dir or tempfile.mkdtemp(prefix="catacomb_")
    
    def _clone_repo(self, repo_url: str) -> str:
        """Clone repository to temporary directory."""
        try:
            repo_name = repo_url.split("/")[-1].replace(".git", "")
            target_dir = os.path.join(self.clone_dir, repo_name)
            
            if os.path.exists(target_dir):
                shutil.rmtree(target_dir)
            
            subprocess.run(
                ["git", "clone", repo_url, target_dir],
                capture_output=True,
                timeout=300
            )
            
            return target_dir
        except Exception as e:
            return None
    
    def _detect_build_system(self, repo_path: str) -> Dict[str, bool]:
        """Detect build system from repository files."""
        build_systems = {
            "npm": False,
            "yarn": False,
            "pip": False,
            "poetry": False,
            "cargo": False,
            "go": False,
            "make": False,
            "docker": False
        }
        
        if not os.path.exists(repo_path):
            return build_systems
        
        files = os.listdir(repo_path)
        
        if "package.json" in files:
            if "yarn.lock" in files:
                build_systems["yarn"] = True
            else:
                build_systems["npm"] = True
        
        if "requirements.txt" in files:
            build_systems["pip"] = True
        if "pyproject.toml" in files:
            build_systems["poetry"] = True
        if "setup.py" in files:
            build_systems["pip"] = True
        
        if "Cargo.toml" in files:
            build_systems["cargo"] = True
        
        if "go.mod" in files:
            build_systems["go"] = True
        
        if "Makefile" in files:
            build_systems["make"] = True
        
        if "Dockerfile" in files:
            build_systems["docker"] = True
        
        return build_systems
    
    def _check_install(self, repo_path: str, build_systems: Dict[str, bool]) -> Dict[str, Any]:
        """Check if dependencies can be installed."""
        result = {
            "attempted": False,
            "success": False,
            "command": None,
            "error": None
        }
        
        if not os.path.exists(repo_path):
            return result
        
        try:
            if build_systems["npm"]:
                result["attempted"] = True
                result["command"] = "npm install"
                proc = subprocess.run(
                    ["npm", "install"],
                    cwd=repo_path,
                    capture_output=True,
                    timeout=300
                )
                result["success"] = proc.returncode == 0
                if not result["success"]:
                    result["error"] = proc.stderr.decode()[:500]
            
            elif build_systems["yarn"]:
                result["attempted"] = True
                result["command"] = "yarn install"
                proc = subprocess.run(
                    ["yarn", "install"],
                    cwd=repo_path,
                    capture_output=True,
                    timeout=300
                )
                result["success"] = proc.returncode == 0
                if not result["success"]:
                    result["error"] = proc.stderr.decode()[:500]
            
            elif build_systems["pip"]:
                result["attempted"] = True
                result["command"] = "pip install -r requirements.txt"
                proc = subprocess.run(
                    ["pip", "install", "-r", "requirements.txt"],
                    cwd=repo_path,
                    capture_output=True,
                    timeout=300
                )
                result["success"] = proc.returncode == 0
                if not result["success"]:
                    result["error"] = proc.stderr.decode()[:500]
            
            elif build_systems["cargo"]:
                result["attempted"] = True
                result["command"] = "cargo build"
                proc = subprocess.run(
                    ["cargo", "build"],
                    cwd=repo_path,
                    capture_output=True,
                    timeout=300
                )
                result["success"] = proc.returncode == 0
                if not result["success"]:
                    result["error"] = proc.stderr.decode()[:500]
            
        except subprocess.TimeoutExpired:
            result["error"] = "Timeout"
        except Exception as e:
            result["error"] = str(e)[:500]
        
        return result
    
    def _check_build(self, repo_path: str, build_systems: Dict[str, bool]) -> Dict[str, Any]:
        """Check if project can be built."""
        result = {
            "attempted": False,
            "success": False,
            "command": None,
            "error": None
        }
        
        if not os.path.exists(repo_path):
            return result
        
        try:
            if build_systems["npm"] or build_systems["yarn"]:
                result["attempted"] = True
                result["command"] = "npm run build"
                proc = subprocess.run(
                    ["npm", "run", "build"],
                    cwd=repo_path,
                    capture_output=True,
                    timeout=300
                )
                result["success"] = proc.returncode == 0
                if not result["success"]:
                    result["error"] = proc.stderr.decode()[:500]
            
            elif build_systems["cargo"]:
                result["attempted"] = True
                result["command"] = "cargo build --release"
                proc = subprocess.run(
                    ["cargo", "build", "--release"],
                    cwd=repo_path,
                    capture_output=True,
                    timeout=300
                )
                result["success"] = proc.returncode == 0
                if not result["success"]:
                    result["error"] = proc.stderr.decode()[:500]
            
            elif build_systems["make"]:
                result["attempted"] = True
                result["command"] = "make"
                proc = subprocess.run(
                    ["make"],
                    cwd=repo_path,
                    capture_output=True,
                    timeout=300
                )
                result["success"] = proc.returncode == 0
                if not result["success"]:
                    result["error"] = proc.stderr.decode()[:500]
            
        except subprocess.TimeoutExpired:
            result["error"] = "Timeout"
        except Exception as e:
            result["error"] = str(e)[:500]
        
        return result
    
    def _check_tests(self, repo_path: str, build_systems: Dict[str, bool]) -> Dict[str, Any]:
        """Check if tests exist and can run."""
        result = {
            "has_tests": False,
            "attempted": False,
            "success": False,
            "command": None,
            "error": None
        }
        
        if not os.path.exists(repo_path):
            return result
        
        # Check for test files
        test_indicators = []
        for root, dirs, files in os.walk(repo_path):
            # Skip node_modules and similar
            dirs[:] = [d for d in dirs if d not in ["node_modules", "target", "__pycache__", ".git"]]
            
            for file in files:
                if file.endswith(("_test.py", ".test.js", ".test.ts", ".spec.js", ".spec.ts")):
                    test_indicators.append(file)
                elif file == "test_" in file and file.endswith(".py"):
                    test_indicators.append(file)
        
        result["has_tests"] = len(test_indicators) > 0
        result["test_files_count"] = len(test_indicators)
        
        if not result["has_tests"]:
            return result
        
        try:
            if build_systems["npm"] or build_systems["yarn"]:
                result["attempted"] = True
                result["command"] = "npm test"
                proc = subprocess.run(
                    ["npm", "test"],
                    cwd=repo_path,
                    capture_output=True,
                    timeout=300
                )
                result["success"] = proc.returncode == 0
                if not result["success"]:
                    result["error"] = proc.stderr.decode()[:500]
            
            elif build_systems["pip"]:
                result["attempted"] = True
                result["command"] = "python -m pytest"
                proc = subprocess.run(
                    ["python", "-m", "pytest", "-v"],
                    cwd=repo_path,
                    capture_output=True,
                    timeout=300
                )
                result["success"] = proc.returncode == 0
                if not result["success"]:
                    result["error"] = proc.stderr.decode()[:500]
            
            elif build_systems["cargo"]:
                result["attempted"] = True
                result["command"] = "cargo test"
                proc = subprocess.run(
                    ["cargo", "test"],
                    cwd=repo_path,
                    capture_output=True,
                    timeout=300
                )
                result["success"] = proc.returncode == 0
                if not result["success"]:
                    result["error"] = proc.stderr.decode()[:500]
            
        except subprocess.TimeoutExpired:
            result["error"] = "Timeout"
        except Exception as e:
            result["error"] = str(e)[:500]
        
        return result
    
    def analyze(self, repo_data: Dict[str, Any]) -> AgentOutput:
        """
        Analyze buildability without cloning (lightweight check).
        For full buildability, use execute_buildability() separately.
        """
        evidence = {}
        
        # Check for package manager
        package_files = [
            "has_package_json", "has_requirements_txt", "has_setup_py",
            "has_pyproject_toml", "has_cargo_toml", "has_go_mod"
        ]
        has_package = any(repo_data.get(pf, False) for pf in package_files)
        evidence["has_package_manager"] = has_package
        
        # Check for build tools
        evidence["has_makefile"] = repo_data.get("has_makefile", False)
        evidence["has_dockerfile"] = repo_data.get("has_dockerfile", False)
        evidence["has_ci"] = repo_data.get("has_ci", False)
        
        # Check for documentation
        evidence["has_readme"] = repo_data.get("has_readme", False)
        
        # Check activity (indicates maintenance)
        evidence["commits_last_year"] = repo_data.get("commits_last_year", 0)
        evidence["updated_at"] = repo_data.get("updated_at")
        
        # Calculate score (0-100)
        score = 0
        
        # Package manager (30 points)
        if has_package:
            score += 30
        
        # Build tools (20 points)
        if repo_data.get("has_makefile", False):
            score += 10
        if repo_data.get("has_dockerfile", False):
            score += 10
        
        # CI/CD (15 points)
        if repo_data.get("has_ci", False):
            score += 15
        
        # Documentation (15 points)
        if repo_data.get("has_readme", False):
            score += 15
        
        # Recent activity (20 points)
        if repo_data.get("commits_last_year", 0) > 0:
            score += 20
        
        score = min(max(score, 0), 100)
        
        confidence = 0.7  # Lower confidence without actual build attempt
        
        return AgentOutput(
            score=round(score, 2),
            evidence=evidence,
            confidence=confidence,
            hash=""
        )
    
    def execute_buildability(self, repo_url: str) -> AgentOutput:
        """
        Full buildability check with actual clone and build attempt.
        """
        evidence = {}
        
        # Clone repo
        repo_path = self._clone_repo(repo_url)
        evidence["cloned"] = repo_path is not None
        
        if not repo_path:
            return AgentOutput(
                score=0,
                evidence={"error": "Failed to clone repository"},
                confidence=0.0,
                hash=""
            )
        
        # Detect build system
        build_systems = self._detect_build_system(repo_path)
        evidence["build_systems"] = build_systems
        
        # Check install
        install_result = self._check_install(repo_path, build_systems)
        evidence["install"] = install_result
        
        # Check build
        build_result = self._check_build(repo_path, build_systems)
        evidence["build"] = build_result
        
        # Check tests
        test_result = self._check_tests(repo_path, build_systems)
        evidence["tests"] = test_result
        
        # Calculate score
        score = 0
        
        # Clone success (10 points)
        if evidence["cloned"]:
            score += 10
        
        # Has build system (10 points)
        if any(build_systems.values()):
            score += 10
        
        # Install success (30 points)
        if install_result.get("success", False):
            score += 30
        elif install_result.get("attempted", False):
            score += 10  # Partial credit for attempt
        
        # Build success (25 points)
        if build_result.get("success", False):
            score += 25
        elif build_result.get("attempted", False):
            score += 5
        
        # Tests (25 points)
        if test_result.get("success", False):
            score += 25
        elif test_result.get("has_tests", False):
            score += 10
        elif test_result.get("attempted", False):
            score += 5
        
        score = min(max(score, 0), 100)
        
        confidence = 0.95  # High confidence with actual build attempt
        
        # Cleanup
        try:
            shutil.rmtree(repo_path)
        except:
            pass
        
        return AgentOutput(
            score=round(score, 2),
            evidence=evidence,
            confidence=confidence,
            hash=""
        )
