"""Orchestrator - Runs 3-layer engine for intervention analysis."""
from typing import Dict, Any, List
from repo_scanner import RepoScannerAgent
from layers import CatacombEngine


class CatacombOrchestrator:
    """Orchestrates 3-layer engine for intervention analysis."""
    
    def __init__(self, github_token: str = None, use_ml: bool = True):
        self.scanner = RepoScannerAgent(github_token)
        self.engine = CatacombEngine(github_token, use_ml)
    
    def analyze_repo(self, owner: str, repo: str, full_build_check: bool = False) -> Dict[str, Any]:
        """
        Analyze a single repository with 3-layer engine.
        """
        # Step 1: Scan repo
        repo_data = self.scanner._get_repo_data(owner, repo)
        
        if "error" in repo_data:
            return {
                "error": repo_data["error"],
                "repo": f"{owner}/{repo}"
            }
        
        # Step 2: Run 3-layer engine
        analysis = self.engine.analyze(repo_data)
        
        return {
            "repo": f"{owner}/{repo}",
            "repo_data": repo_data,
            "analysis": analysis
        }
    
    def analyze_topic(self, topic: str, limit: int = 50) -> List[Dict[str, Any]]:
        """
        Analyze multiple repos by topic.
        """
        repos = self.scanner.search_repos_by_topic(topic, limit)
        
        results = []
        for repo_data in repos:
            owner = repo_data.get("owner")
            repo = repo_data.get("repo")
            
            if owner and repo:
                result = self.analyze_repo(owner, repo)
                results.append(result)
        
        # Sort by intervention score
        results.sort(key=lambda x: x.get("analysis", {}).get("intervention_score", 0), reverse=True)
        
        return results
    
    def analyze_user(self, username: str, limit: int = 50) -> List[Dict[str, Any]]:
        """
        Analyze multiple repos by user.
        """
        repos = self.scanner.search_repos_by_user(username, limit)
        
        results = []
        for repo_data in repos:
            owner = repo_data.get("owner")
            repo = repo_data.get("repo")
            
            if owner and repo:
                result = self.analyze_repo(owner, repo)
                results.append(result)
        
        # Sort by intervention score
        results.sort(key=lambda x: x.get("analysis", {}).get("intervention_score", 0), reverse=True)
        
        return results
    
    def format_output(self, results: List[Dict[str, Any]], verbose: bool = False) -> str:
        """
        Format results for display - showing interventions.
        """
        output = []
        
        for i, result in enumerate(results, 1):
            if "error" in result:
                output.append(f"{i}. {result['repo']}: ERROR - {result['error']}")
                continue
            
            repo = result["repo"]
            analysis = result.get("analysis", {})
            intervention_score = analysis.get("intervention_score", 0)
            best_intervention = analysis.get("best_intervention", {})
            
            output.append(f"\n{'='*60}")
            output.append(f"{i}. {repo}")
            output.append(f"   Intervention Score: {intervention_score}/100")
            
            if best_intervention:
                output.append(f"   Best Intervention: {best_intervention.get('name', 'N/A')}")
                output.append(f"   Effort: {best_intervention.get('effort_days', 0)} days")
                output.append(f"   Probability: {best_intervention.get('probability', 0):.0%}")
                output.append(f"   Upside: {best_intervention.get('upside', 0):.0%}")
            
            output.append(f"   Stars: {result['repo_data'].get('stars', 0)} | Forks: {result['repo_data'].get('forks', 0)}")
            output.append(f"   Language: {result['repo_data'].get('language', 'N/A')}")
            
            if verbose:
                output.append(f"\n   Intervention Steps:")
                for step in best_intervention.get("steps", []):
                    output.append(f"   - {step}")
                
                output.append(f"\n   All Intervention Paths:")
                for path in analysis.get("strategy", {}).get("intervention_paths", []):
                    output.append(f"   - {path.get('name', 'N/A')}: {path.get('intervention_score', 0)} ({path.get('effort_days', 0)} days)")
            
            output.append(f"   Hash: {analysis.get('evidence', {}).get('scanner', {}).get('hash', '')[:16]}...")
        
        return "\n".join(output)
