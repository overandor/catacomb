"""Language-specific analysis layer for C++ and Rust."""
from typing import Dict, Any
from base_agent import BaseAgent, AgentOutput


class LanguageLayer(BaseAgent):
    """Language-specific build system and ecosystem analysis."""
    
    def __init__(self):
        super().__init__("LanguageLayer")
    
    def _analyze_cpp(self, repo_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze C++-specific build systems and patterns."""
        evidence = {}
        
        # C++ build systems
        has_cmake = repo_data.get("has_cmake", False)
        has_makefile = repo_data.get("has_makefile", False)
        has_conan = repo_data.get("has_conan", False)
        has_vcpkg = repo_data.get("has_vcpkg", False)
        has_meson = repo_data.get("has_meson", False)
        has_bazel = repo_data.get("has_bazel", False)
        
        evidence["has_cmake"] = has_cmake
        evidence["has_makefile"] = has_makefile
        evidence["has_conan"] = has_conan
        evidence["has_vcpkg"] = has_vcpkg
        evidence["has_meson"] = has_meson
        evidence["has_bazel"] = has_bazel
        
        # C++ ecosystem score
        cpp_score = 0
        
        if has_cmake:
            cpp_score += 30  # Modern CMake is standard
        if has_conan:
            cpp_score += 25  # Modern package manager
        if has_vcpkg:
            cpp_score += 20  # Microsoft's package manager
        if has_meson:
            cpp_score += 15  # Modern build system
        if has_bazel:
            cpp_score += 20  # Google's build system
        if has_makefile:
            cpp_score += 10  # Traditional but works
        
        # C++-specific quality indicators
        has_tests = repo_data.get("has_cpp_tests", False)
        has_doxygen = repo_data.get("has_doxygen", False)
        has_clang_format = repo_data.get("has_clang_format", False)
        
        evidence["has_tests"] = has_tests
        evidence["has_doxygen"] = has_doxygen
        evidence["has_clang_format"] = has_clang_format
        
        if has_tests:
            cpp_score += 15
        if has_doxygen:
            cpp_score += 10
        if has_clang_format:
            cpp_score += 10
        
        # C++ modernity indicators
        cxx_standard = repo_data.get("cxx_standard", "98")
        evidence["cxx_standard"] = cxx_standard
        
        if cxx_standard in ["20", "23"]:
            cpp_score += 20
        elif cxx_standard in ["17", "14"]:
            cpp_score += 15
        elif cxx_standard == "11":
            cpp_score += 10
        
        cpp_score = min(cpp_score, 100)
        evidence["cpp_ecosystem_score"] = cpp_score
        
        return {
            "score": cpp_score,
            "evidence": evidence
        }
    
    def _analyze_rust(self, repo_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze Rust-specific build systems and patterns."""
        evidence = {}
        
        # Rust build systems
        has_cargo = repo_data.get("has_cargo_toml", False)
        has_cargo_lock = repo_data.get("has_cargo_lock", False)
        has_rustfmt = repo_data.get("has_rustfmt", False)
        has_clippy = repo_data.get("has_clippy", False)
        
        evidence["has_cargo"] = has_cargo
        evidence["has_cargo_lock"] = has_cargo_lock
        evidence["has_rustfmt"] = has_rustfmt
        evidence["has_clippy"] = has_clippy
        
        # Rust ecosystem score
        rust_score = 0
        
        if has_cargo:
            rust_score += 30  # Cargo is standard
        if has_cargo_lock:
            rust_score += 20  # Reproducible builds
        if has_rustfmt:
            rust_score += 15  # Code formatting
        if has_clippy:
            rust_score += 15  # Linting
        
        # Rust-specific quality indicators
        has_tests = repo_data.get("has_rust_tests", False)
        has_docs = repo_data.get("has_rust_docs", False)
        has_workspace = repo_data.get("has_workspace", False)
        
        evidence["has_tests"] = has_tests
        evidence["has_docs"] = has_docs
        evidence["has_workspace"] = has_workspace
        
        if has_tests:
            rust_score += 15
        if has_docs:
            rust_score += 10
        if has_workspace:
            rust_score += 5
        
        # Rust edition
        rust_edition = repo_data.get("rust_edition", "2015")
        evidence["rust_edition"] = rust_edition
        
        if rust_edition in ["2021", "2024"]:
            rust_score += 10
        elif rust_edition == "2018":
            rust_score += 5
        
        # Cargo features
        has_features = repo_data.get("has_features", False)
        has_default_features = repo_data.get("has_default_features", False)
        
        evidence["has_features"] = has_features
        evidence["has_default_features"] = has_default_features
        
        if has_features:
            rust_score += 5
        
        rust_score = min(rust_score, 100)
        evidence["rust_ecosystem_score"] = rust_score
        
        return {
            "score": rust_score,
            "evidence": evidence
        }
    
    def _detect_cpp_files(self, repo_data: Dict[str, Any]) -> Dict[str, Any]:
        """Detect C++ project files from repo data."""
        evidence = {}
        
        # This would be enhanced with actual file scanning in a full implementation
        # For now, we use proxies from the scanner
        
        languages = repo_data.get("languages", {})
        has_cpp = "C++" in languages or "C" in languages
        
        evidence["has_cpp"] = has_cpp
        evidence["cpp_percentage"] = languages.get("C++", 0) if has_cpp else 0
        
        # Proxy detection based on file patterns
        # In a full implementation, this would scan actual files
        has_cmake = repo_data.get("has_cmake", False)
        has_makefile = repo_data.get("has_makefile", False)
        
        evidence["has_cmake"] = has_cmake
        evidence["has_makefile"] = has_makefile
        
        return {
            "score": 50 if has_cpp else 0,
            "evidence": evidence
        }
    
    def _detect_rust_files(self, repo_data: Dict[str, Any]) -> Dict[str, Any]:
        """Detect Rust project files from repo data."""
        evidence = {}
        
        languages = repo_data.get("languages", {})
        has_rust = "Rust" in languages
        
        evidence["has_rust"] = has_rust
        evidence["rust_percentage"] = languages.get("Rust", 0) if has_rust else 0
        
        # Cargo detection
        has_cargo = repo_data.get("has_cargo_toml", False)
        
        evidence["has_cargo"] = has_cargo
        
        return {
            "score": 50 if has_rust else 0,
            "evidence": evidence
        }
    
    def analyze(self, repo_data: Dict[str, Any]) -> AgentOutput:
        """
        Analyze language-specific build systems and ecosystem.
        """
        evidence = {}
        
        language = (repo_data.get("language") or "").lower()
        
        # Detect language
        cpp_detection = self._detect_cpp_files(repo_data)
        rust_detection = self._detect_rust_files(repo_data)
        
        evidence["cpp_detection"] = cpp_detection["evidence"]
        evidence["rust_detection"] = rust_detection["evidence"]
        
        # Language-specific analysis
        language_score = 50  # Default
        
        if "c++" in language or cpp_detection["score"] > 0:
            cpp_analysis = self._analyze_cpp(repo_data)
            evidence["cpp_analysis"] = cpp_analysis["evidence"]
            language_score = cpp_analysis["score"]
        
        elif "rust" in language or rust_detection["score"] > 0:
            rust_analysis = self._analyze_rust(repo_data)
            evidence["rust_analysis"] = rust_analysis["evidence"]
            language_score = rust_analysis["score"]
        
        else:
            evidence["language_analysis"] = "No specific language analysis available"
        
        evidence["overall_language_score"] = language_score
        
        # Confidence based on language detection
        has_language = bool(repo_data.get("language"))
        confidence = 0.8 if has_language else 0.5
        
        return AgentOutput(
            score=round(language_score, 2),
            evidence=evidence,
            confidence=confidence,
            hash=""
        )
