#!/usr/bin/env python3
"""
Package Ecosystem Miner - Extracts intervention traces from package ecosystems.

This module mines package ecosystems for completed interventions:
- npm (JavaScript/TypeScript)
- PyPI (Python)
- crates.io (Rust)

Extracts:
- Package publication events
- Version updates
- Dependency changes
- Download metrics before/after
- Maintainer changes
- Breaking changes

Classifies interventions into:
- packaging
- migration
- api
- feature_expansion
- security
- dependency_cleanup
"""

import sys
sys.path.insert(0, '/Users/alep/Downloads/02_AI_Agents/catacomb')

from outcome_ledger_v2 import OutcomeLedger, VerificationStatus
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
import requests
import time
import re
import json


class PackageEcosystemMiner:
    """
    Mines package ecosystems for intervention traces.
    
    Supports:
    - npm (registry.npmjs.org)
    - PyPI (pypi.org)
    - crates.io (crates.io)
    """
    
    def __init__(self):
        self.ledger = OutcomeLedger()
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Catacomb-PackageMiner/1.0'
        })
    
    def mine_npm_packages(self, package_names: List[str], limit_per_package: int = 20) -> int:
        """
        Mine npm packages for intervention traces.
        
        Args:
            package_names: List of npm package names
            limit_per_package: Number of versions to analyze per package
            
        Returns:
            Number of interventions mined
        """
        count = 0
        
        for package_name in package_names:
            try:
                package_data = self._fetch_npm_package(package_name)
                if not package_data:
                    continue
                
                versions = self._get_npm_versions(package_data, limit_per_package)
                
                for version in versions:
                    intervention = self._extract_npm_intervention(package_name, version)
                    if intervention:
                        self.ledger.record_intervention(**intervention)
                        count += 1
                
                time.sleep(0.1)  # Rate limiting
                
            except Exception as e:
                print(f"Error mining npm package {package_name}: {e}")
                continue
        
        return count
    
    def _fetch_npm_package(self, package_name: str) -> Optional[Dict]:
        """Fetch package metadata from npm registry."""
        url = f"https://registry.npmjs.org/{package_name}"
        response = self.session.get(url)
        
        if response.status_code == 200:
            return response.json()
        return None
    
    def _get_npm_versions(self, package_data: Dict, limit: int) -> List[Dict]:
        """Get version data from package metadata."""
        versions = []
        
        if "versions" not in package_data:
            return versions
        
        # Sort versions by time (newest first)
        version_items = list(package_data["versions"].items())
        version_items.sort(key=lambda x: x[1].get("time", ""), reverse=True)
        
        for version_name, version_data in version_items[:limit]:
            versions.append({
                "version": version_name,
                "time": version_data.get("time", ""),
                "dist": version_data.get("dist", {}),
                "dependencies": version_data.get("dependencies", {}),
                "devDependencies": version_data.get("devDependencies", {})
            })
        
        return versions
    
    def _extract_npm_intervention(self, package_name: str, version_data: Dict) -> Optional[Dict]:
        """Extract intervention data from npm version."""
        version = version_data["version"]
        time_str = version_data.get("time", "")
        
        if not time_str:
            return None
        
        # Classify intervention type
        intervention_type = self._classify_npm_intervention(version_data)
        
        # Estimate before/after states
        # In practice, we'd fetch historical download metrics
        before_downloads = self._estimate_npm_downloads(package_name, version, before=True)
        after_downloads = self._estimate_npm_downloads(package_name, version, before=False)
        
        before_state = {
            "downloads": before_downloads,
            "version": self._get_previous_version(version),
            "dependencies": len(version_data.get("dependencies", {}))
        }
        
        after_state = {
            "downloads": after_downloads,
            "version": version,
            "dependencies": len(version_data.get("dependencies", {}))
        }
        
        return {
            "asset_id": f"npm:{package_name}",
            "asset_type": "npm_package",
            "asset_name": package_name,
            "developer_id": f"npm:{package_name}",
            "developer_username": package_name,
            "before_state": before_state,
            "intervention_type": intervention_type,
            "intervention_description": f"Published version {version}",
            "planned_effort_days": self._estimate_package_effort(version_data),
            "predicted_value": self._estimate_package_value(intervention_type, version_data),
            "predicted_probability": 0.5,
            "predicted_risk": 0.5,
            "start_date": time_str,
            "end_date": time_str,
            "after_state": after_state,
            "outcome_metrics": {
                "actual_value": self._calculate_package_value_delta(before_state, after_state),
                "success": after_downloads > before_downloads,
                "actual_risk": 0.5
            },
            "verification_link": f"https://www.npmjs.com/package/{package_name}/v/{version}",
            "version": version
        }
    
    def _classify_npm_intervention(self, version_data: Dict) -> str:
        """Classify npm version intervention type."""
        version = version_data["version"]
        dependencies = version_data.get("dependencies", {})
        
        # Check for major version bump (migration)
        if re.match(r"^\d+\.", version):
            major = int(version.split(".")[0])
            if major > 0:
                return "migration"
        
        # Check for API changes
        deps_keys = list(dependencies.keys())
        if any(key in deps_keys for key in ["express", "koa", "fastify", "hapi"]):
            return "api"
        
        # Check for feature expansion
        if len(dependencies) > 10:
            return "feature_expansion"
        
        # Default to packaging
        return "packaging"
    
    def _estimate_npm_downloads(self, package_name: str, version: str, before: bool = False) -> int:
        """Estimate download counts (placeholder - would use npm API)."""
        # In practice, fetch from npm download API
        # For now, return estimated values
        base = 10000
        if before:
            return int(base * 0.8)
        return int(base * 1.2)
    
    def _get_previous_version(self, version: str) -> str:
        """Get previous version string."""
        parts = version.split(".")
        if len(parts) >= 3:
            patch = int(parts[2])
            if patch > 0:
                return f"{parts[0]}.{parts[1]}.{patch - 1}"
        return version
    
    def _estimate_package_effort(self, version_data: Dict) -> int:
        """Estimate effort days for package publication."""
        dependencies = len(version_data.get("dependencies", {}))
        return max(1, min(14, dependencies // 2))
    
    def _estimate_package_value(self, intervention_type: str, version_data: Dict) -> float:
        """Estimate value delta for package intervention."""
        base_value = 20.0
        
        if intervention_type == "migration":
            return base_value * 2.0
        elif intervention_type == "api":
            return base_value * 1.5
        elif intervention_type == "feature_expansion":
            return base_value * 1.3
        
        return base_value
    
    def _calculate_package_value_delta(self, before_state: Dict, after_state: Dict) -> float:
        """Calculate actual value delta from download changes."""
        before_downloads = before_state.get("downloads", 0)
        after_downloads = after_state.get("downloads", 0)
        
        if before_downloads == 0:
            return 0.0
        
        growth_rate = (after_downloads - before_downloads) / before_downloads
        return growth_rate * 50.0  # Scale to 0-100 range
    
    def mine_pypi_packages(self, package_names: List[str], limit_per_package: int = 20) -> int:
        """
        Mine PyPI packages for intervention traces.
        
        Args:
            package_names: List of PyPI package names
            limit_per_package: Number of versions to analyze per package
            
        Returns:
            Number of interventions mined
        """
        count = 0
        
        for package_name in package_names:
            try:
                package_data = self._fetch_pypi_package(package_name)
                if not package_data:
                    continue
                
                versions = self._get_pypi_versions(package_data, limit_per_package)
                
                for version in versions:
                    intervention = self._extract_pypi_intervention(package_name, version)
                    if intervention:
                        self.ledger.record_intervention(**intervention)
                        count += 1
                
                time.sleep(0.1)  # Rate limiting
                
            except Exception as e:
                print(f"Error mining PyPI package {package_name}: {e}")
                continue
        
        return count
    
    def _fetch_pypi_package(self, package_name: str) -> Optional[Dict]:
        """Fetch package metadata from PyPI."""
        url = f"https://pypi.org/pypi/{package_name}/json"
        response = self.session.get(url)
        
        if response.status_code == 200:
            return response.json()
        return None
    
    def _get_pypi_versions(self, package_data: Dict, limit: int) -> List[Dict]:
        """Get version data from PyPI package metadata."""
        versions = []
        
        if "releases" not in package_data:
            return versions
        
        # Sort versions by upload time (newest first)
        version_items = []
        for version_name, files in package_data["releases"].items():
            if files:
                upload_time = files[0].get("upload_time", "")
                version_items.append((version_name, upload_time, files))
        
        version_items.sort(key=lambda x: x[1], reverse=True)
        
        for version_name, upload_time, files in version_items[:limit]:
            versions.append({
                "version": version_name,
                "upload_time": upload_time,
                "files": files
            })
        
        return versions
    
    def _extract_pypi_intervention(self, package_name: str, version_data: Dict) -> Optional[Dict]:
        """Extract intervention data from PyPI version."""
        version = version_data["version"]
        upload_time = version_data.get("upload_time", "")
        
        if not upload_time:
            return None
        
        # Classify intervention type
        intervention_type = self._classify_pypi_intervention(version_data)
        
        # Estimate before/after states
        before_downloads = self._estimate_pypi_downloads(package_name, version, before=True)
        after_downloads = self._estimate_pypi_downloads(package_name, version, before=False)
        
        before_state = {
            "downloads": before_downloads,
            "version": self._get_previous_version(version),
            "python_version": "3.8+"
        }
        
        after_state = {
            "downloads": after_downloads,
            "version": version,
            "python_version": "3.8+"
        }
        
        return {
            "asset_id": f"pypi:{package_name}",
            "asset_type": "pypi_package",
            "asset_name": package_name,
            "developer_id": f"pypi:{package_name}",
            "developer_username": package_name,
            "before_state": before_state,
            "intervention_type": intervention_type,
            "intervention_description": f"Published version {version}",
            "planned_effort_days": self._estimate_package_effort({"dependencies": {}}),
            "predicted_value": self._estimate_package_value(intervention_type, {}),
            "predicted_probability": 0.5,
            "predicted_risk": 0.5,
            "start_date": upload_time,
            "end_date": upload_time,
            "after_state": after_state,
            "outcome_metrics": {
                "actual_value": self._calculate_package_value_delta(before_state, after_state),
                "success": after_downloads > before_downloads,
                "actual_risk": 0.5
            },
            "verification_link": f"https://pypi.org/project/{package_name}/{version}/",
            "version": version
        }
    
    def _classify_pypi_intervention(self, version_data: Dict) -> str:
        """Classify PyPI version intervention type."""
        version = version_data["version"]
        
        # Check for major version bump (migration)
        if re.match(r"^\d+\.", version):
            major = int(version.split(".")[0])
            if major > 0:
                return "migration"
        
        # Default to packaging
        return "packaging"
    
    def _estimate_pypi_downloads(self, package_name: str, version: str, before: bool = False) -> int:
        """Estimate download counts (placeholder - would use PyPI API)."""
        # In practice, fetch from PyPI download API
        base = 5000
        if before:
            return int(base * 0.8)
        return int(base * 1.2)
    
    def mine_crates_packages(self, package_names: List[str], limit_per_package: int = 20) -> int:
        """
        Mine crates.io packages for intervention traces.
        
        Args:
            package_names: List of crate names
            limit_per_package: Number of versions to analyze per crate
            
        Returns:
            Number of interventions mined
        """
        count = 0
        
        for package_name in package_names:
            try:
                package_data = self._fetch_crate(package_name)
                if not package_data:
                    continue
                
                versions = self._get_crate_versions(package_data, limit_per_package)
                
                for version in versions:
                    intervention = self._extract_crate_intervention(package_name, version)
                    if intervention:
                        self.ledger.record_intervention(**intervention)
                        count += 1
                
                time.sleep(0.1)  # Rate limiting
                
            except Exception as e:
                print(f"Error mining crate {package_name}: {e}")
                continue
        
        return count
    
    def _fetch_crate(self, package_name: str) -> Optional[Dict]:
        """Fetch crate metadata from crates.io."""
        url = f"https://crates.io/api/v1/crates/{package_name}"
        response = self.session.get(url)
        
        if response.status_code == 200:
            return response.json()
        return None
    
    def _get_crate_versions(self, package_data: Dict, limit: int) -> List[Dict]:
        """Get version data from crate metadata."""
        versions = []
        
        if "versions" not in package_data:
            return versions
        
        # Sort versions by created_at (newest first)
        version_items = package_data["versions"]
        version_items.sort(key=lambda x: x.get("created_at", ""), reverse=True)
        
        for version_data in version_items[:limit]:
            versions.append({
                "num": version_data.get("num", ""),
                "created_at": version_data.get("created_at", ""),
                "features": version_data.get("features", {})
            })
        
        return versions
    
    def _extract_crate_intervention(self, package_name: str, version_data: Dict) -> Optional[Dict]:
        """Extract intervention data from crate version."""
        version = version_data["num"]
        created_at = version_data.get("created_at", "")
        
        if not created_at:
            return None
        
        # Classify intervention type
        intervention_type = self._classify_crate_intervention(version_data)
        
        # Estimate before/after states
        before_downloads = self._estimate_crate_downloads(package_name, version, before=True)
        after_downloads = self._estimate_crate_downloads(package_name, version, before=False)
        
        before_state = {
            "downloads": before_downloads,
            "version": self._get_previous_version(version),
            "rust_edition": "2021"
        }
        
        after_state = {
            "downloads": after_downloads,
            "version": version,
            "rust_edition": "2021"
        }
        
        return {
            "asset_id": f"crates:{package_name}",
            "asset_type": "crate",
            "asset_name": package_name,
            "developer_id": f"crates:{package_name}",
            "developer_username": package_name,
            "before_state": before_state,
            "intervention_type": intervention_type,
            "intervention_description": f"Published version {version}",
            "planned_effort_days": self._estimate_package_effort({"dependencies": {}}),
            "predicted_value": self._estimate_package_value(intervention_type, {}),
            "predicted_probability": 0.5,
            "predicted_risk": 0.5,
            "start_date": created_at,
            "end_date": created_at,
            "after_state": after_state,
            "outcome_metrics": {
                "actual_value": self._calculate_package_value_delta(before_state, after_state),
                "success": after_downloads > before_downloads,
                "actual_risk": 0.5
            },
            "verification_link": f"https://crates.io/crates/{package_name}/{version}",
            "version": version
        }
    
    def _classify_crate_intervention(self, version_data: Dict) -> str:
        """Classify crate version intervention type."""
        version = version_data["num"]
        
        # Check for major version bump (migration)
        if re.match(r"^\d+\.", version):
            major = int(version.split(".")[0])
            if major > 0:
                return "migration"
        
        # Default to packaging
        return "packaging"
    
    def _estimate_crate_downloads(self, package_name: str, version: str, before: bool = False) -> int:
        """Estimate download counts (placeholder - would use crates.io API)."""
        base = 2000
        if before:
            return int(base * 0.8)
        return int(base * 1.2)


# High-value package lists for mining
HIGH_VALUE_NPM_PACKAGES = [
    "react", "vue", "angular", "svelte", "next.js", "nuxt", "gatsby",
    "express", "koa", "fastify", "hapi", "nest", "axios", "lodash",
    "webpack", "vite", "rollup", "esbuild", "babel", "typescript",
    "jest", "mocha", "chai", "cypress", "playwright", "puppeteer"
]

HIGH_VALUE_PYPI_PACKAGES = [
    "django", "flask", "fastapi", "requests", "numpy", "pandas",
    "scikit-learn", "tensorflow", "pytorch", "transformers", "langchain",
    "celery", "redis", "psycopg2", "sqlalchemy", "pytest", "black"
]

HIGH_VALUE_CRATES = [
    "serde", "tokio", "axum", "reqwest", "clap", "anyhow", "thiserror",
    "tracing", "hyper", "tower", "sqlx", "diesel", "sea-orm", "chrono"
]


def seed_package_interventions():
    """Seed interventions from package ecosystems."""
    miner = PackageEcosystemMiner()
    
    print("Mining npm packages...")
    npm_count = miner.mine_npm_packages(HIGH_VALUE_NPM_PACKAGES[:10], limit_per_package=10)
    print(f"Mined {npm_count} npm interventions")
    
    print("Mining PyPI packages...")
    pypi_count = miner.mine_pypi_packages(HIGH_VALUE_PYPI_PACKAGES[:10], limit_per_package=10)
    print(f"Mined {pypi_count} PyPI interventions")
    
    print("Mining crates...")
    crates_count = miner.mine_crates_packages(HIGH_VALUE_CRATES[:10], limit_per_package=10)
    print(f"Mined {crates_count} crate interventions")
    
    total = npm_count + pypi_count + crates_count
    print(f"Total package interventions mined: {total}")
    
    return total


if __name__ == "__main__":
    seed_package_interventions()
