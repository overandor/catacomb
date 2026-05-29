"""Repo Scanner Agent - Collects repo facts from GitHub API."""
import os
from typing import Dict, Any, List
import requests
from base_agent import BaseAgent, AgentOutput


class RepoScannerAgent(BaseAgent):
    """Scans GitHub repositories and collects deterministic facts."""
    
    def __init__(self, github_token: str = None):
        super().__init__("RepoScanner")
        self.github_token = github_token or os.getenv("GITHUB_TOKEN")
        self.headers = {"Accept": "application/vnd.github.v3+json"}
        if self.github_token:
            self.headers["Authorization"] = f"token {self.github_token}"
    
    def _get_repo_data(self, owner: str, repo: str) -> Dict[str, Any]:
        """Fetch comprehensive repo data from GitHub API."""
        base_url = f"https://api.github.com/repos/{owner}/{repo}"
        
        data = {}
        
        # Basic repo info
        try:
            response = requests.get(base_url, headers=self.headers)
            response.raise_for_status()
            repo_info = response.json()
            
            data["owner"] = owner
            data["repo"] = repo
            data["full_name"] = repo_info.get("full_name")
            data["description"] = repo_info.get("description")
            data["stars"] = repo_info.get("stargazers_count", 0)
            data["forks"] = repo_info.get("forks_count", 0)
            data["open_issues"] = repo_info.get("open_issues_count", 0)
            data["watchers"] = repo_info.get("watchers_count", 0)
            data["subscribers"] = repo_info.get("subscribers_count", 0)
            data["created_at"] = repo_info.get("created_at")
            data["updated_at"] = repo_info.get("updated_at")
            data["pushed_at"] = repo_info.get("pushed_at")
            data["size"] = repo_info.get("size", 0)
            data["is_fork"] = repo_info.get("fork", False)
            data["default_branch"] = repo_info.get("default_branch")
            data["has_issues"] = repo_info.get("has_issues", False)
            data["has_wiki"] = repo_info.get("has_wiki", False)
            data["has_pages"] = repo_info.get("has_pages", False)
            data["has_downloads"] = repo_info.get("has_downloads", False)
            data["archived"] = repo_info.get("archived", False)
            data["disabled"] = repo_info.get("disabled", False)
            data["license"] = repo_info.get("license", {}).get("key") if repo_info.get("license") else None
            data["language"] = repo_info.get("language")
            data["homepage"] = repo_info.get("homepage")
            data["topics"] = repo_info.get("topics", [])
            
            # Get languages
            languages_url = f"{base_url}/languages"
            lang_response = requests.get(languages_url, headers=self.headers)
            if lang_response.status_code == 200:
                data["languages"] = lang_response.json()
            else:
                data["languages"] = {}
            
            # Get commit count (last year)
            commits_url = f"{base_url}/commits?per_page=1&since=2024-01-01"
            commits_response = requests.get(commits_url, headers=self.headers)
            if commits_response.status_code == 200:
                # Get total count from Link header
                link_header = commits_response.headers.get("Link", "")
                if link_header:
                    import re
                    match = re.search(r'page=(\d+)>; rel="last"', link_header)
                    if match:
                        data["commits_last_year"] = int(match.group(1))
                    else:
                        data["commits_last_year"] = 1
                else:
                    data["commits_last_year"] = 1
            else:
                data["commits_last_year"] = 0
            
            # Get contributors count
            contributors_url = f"{base_url}/contributors?per_page=1"
            contrib_response = requests.get(contributors_url, headers=self.headers)
            if contrib_response.status_code == 200:
                link_header = contrib_response.headers.get("Link", "")
                if link_header:
                    import re
                    match = re.search(r'page=(\d+)>; rel="last"', link_header)
                    if match:
                        data["contributors"] = int(match.group(1))
                    else:
                        data["contributors"] = 1
                else:
                    data["contributors"] = 1
            else:
                data["contributors"] = 0
            
            # Get release count
            releases_url = f"{base_url}/releases?per_page=1"
            releases_response = requests.get(releases_url, headers=self.headers)
            if releases_response.status_code == 200:
                link_header = releases_response.headers.get("Link", "")
                if link_header:
                    import re
                    match = re.search(r'page=(\d+)>; rel="last"', link_header)
                    if match:
                        data["releases"] = int(match.group(1))
                    else:
                        data["releases"] = 1
                else:
                    data["releases"] = 1
            else:
                data["releases"] = 0
            
            # Get README
            readme_url = f"{base_url}/readme"
            readme_response = requests.get(readme_url, headers=self.headers)
            if readme_response.status_code == 200:
                readme_data = readme_response.json()
                data["has_readme"] = True
                data["readme_size"] = len(readme_data.get("content", ""))
            else:
                data["has_readme"] = False
                data["readme_size"] = 0
            
            # Check for common package files
            contents_url = f"{base_url}/contents"
            contents_response = requests.get(contents_url, headers=self.headers)
            if contents_response.status_code == 200:
                contents = contents_response.json()
                filenames = [item.get("name", "") for item in contents if isinstance(item, dict)]
                data["has_package_json"] = "package.json" in filenames
                data["has_requirements_txt"] = "requirements.txt" in filenames
                data["has_setup_py"] = "setup.py" in filenames
                data["has_pyproject_toml"] = "pyproject.toml" in filenames
                data["has_cargo_toml"] = "Cargo.toml" in filenames
                data["has_go_mod"] = "go.mod" in filenames
                data["has_gemfile"] = "Gemfile" in filenames
                data["has_composer_json"] = "composer.json" in filenames
                data["has_makefile"] = "Makefile" in filenames
                data["has_dockerfile"] = "Dockerfile" in filenames
                data["has_ci"] = any(
                    ".github" in f or ".gitlab-ci.yml" in f or "travis.yml" in f or "circleci" in f
                    for f in filenames
                )
            else:
                data["has_package_json"] = False
                data["has_requirements_txt"] = False
                data["has_setup_py"] = False
                data["has_pyproject_toml"] = False
                data["has_cargo_toml"] = False
                data["has_go_mod"] = False
                data["has_gemfile"] = False
                data["has_composer_json"] = False
                data["has_makefile"] = False
                data["has_dockerfile"] = False
                data["has_ci"] = False
            
        except Exception as e:
            data["error"] = str(e)
        
        return data
    
    def search_repos_by_topic(self, topic: str, limit: int = 50) -> List[Dict[str, Any]]:
        """Search for repos by topic."""
        url = f"https://api.github.com/search/repositories"
        params = {
            "q": f"topic:{topic}",
            "sort": "updated",
            "order": "desc",
            "per_page": min(limit, 100)
        }
        
        try:
            response = requests.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            results = response.json().get("items", [])
            
            repos = []
            for item in results:
                owner, repo = item["full_name"].split("/")
                repos.append(self._get_repo_data(owner, repo))
            
            return repos
        except Exception as e:
            print(f"Error searching repos: {e}")
            return []
    
    def search_repos_by_user(self, username: str, limit: int = 50) -> List[Dict[str, Any]]:
        """Search for repos by user."""
        url = f"https://api.github.com/users/{username}/repos"
        params = {
            "sort": "updated",
            "order": "desc",
            "per_page": min(limit, 100)
        }
        
        try:
            response = requests.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            results = response.json()
            
            repos = []
            for item in results:
                owner, repo = item["full_name"].split("/")
                repos.append(self._get_repo_data(owner, repo))
            
            return repos
        except Exception as e:
            print(f"Error searching user repos: {e}")
            return []
    
    def analyze(self, repo_data: Dict[str, Any]) -> AgentOutput:
        """
        Analyze repo data and produce scanner score.
        Score based on data completeness and repo health indicators.
        """
        evidence = {}
        
        # Data completeness
        required_fields = [
            "stars", "forks", "open_issues", "created_at", "updated_at",
            "pushed_at", "language", "license", "has_readme"
        ]
        completeness = sum(1 for field in required_fields if field in repo_data and repo_data[field] is not None)
        evidence["data_completeness"] = f"{completeness}/{len(required_fields)}"
        
        # Activity signals
        evidence["stars"] = repo_data.get("stars", 0)
        evidence["forks"] = repo_data.get("forks", 0)
        evidence["open_issues"] = repo_data.get("open_issues", 0)
        evidence["commits_last_year"] = repo_data.get("commits_last_year", 0)
        evidence["contributors"] = repo_data.get("contributors", 0)
        evidence["releases"] = repo_data.get("releases", 0)
        
        # Package management
        package_files = [
            "has_package_json", "has_requirements_txt", "has_setup_py",
            "has_pyproject_toml", "has_cargo_toml", "has_go_mod"
        ]
        has_package = any(repo_data.get(pf, False) for pf in package_files)
        evidence["has_package_manager"] = has_package
        
        # Documentation
        evidence["has_readme"] = repo_data.get("has_readme", False)
        evidence["has_wiki"] = repo_data.get("has_wiki", False)
        evidence["has_pages"] = repo_data.get("has_pages", False)
        
        # CI/CD
        evidence["has_ci"] = repo_data.get("has_ci", False)
        
        # Calculate score (0-100)
        score = 0
        
        # Data completeness (20 points)
        score += (completeness / len(required_fields)) * 20
        
        # Activity (30 points)
        activity_score = min(repo_data.get("commits_last_year", 0) / 52, 1) * 10  # Weekly commits
        activity_score += min(repo_data.get("contributors", 0) / 5, 1) * 10  # Contributors
        activity_score += min(repo_data.get("releases", 0) / 4, 1) * 10  # Releases
        score += activity_score
        
        # Engagement (20 points)
        engagement_score = min(repo_data.get("stars", 0) / 100, 1) * 10
        engagement_score += min(repo_data.get("forks", 0) / 20, 1) * 10
        score += engagement_score
        
        # Setup quality (20 points)
        if has_package:
            score += 10
        if repo_data.get("has_readme", False):
            score += 5
        if repo_data.get("has_ci", False):
            score += 5
        
        # License (10 points)
        if repo_data.get("license"):
            score += 10
        
        score = min(max(score, 0), 100)
        
        confidence = 0.9 if "error" not in repo_data else 0.5
        
        return AgentOutput(
            score=round(score, 2),
            evidence=evidence,
            confidence=confidence,
            hash=""  # Will be computed by execute()
        )
