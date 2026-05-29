"""Automated Outcome Monitoring - tracks metrics over time for interventions."""
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
from outcome_ledger import OutcomeLedger, InterventionStatus
import time
import threading


class MetricSnapshot:
    """A snapshot of metrics at a point in time."""
    
    def __init__(
        self,
        record_id: str,
        timestamp: str,
        stars: int,
        forks: int,
        contributors: int,
        downloads: int = None,
        revenue: float = None,
        issues: int = None,
        releases: int = None
    ):
        self.record_id = record_id
        self.timestamp = timestamp
        self.stars = stars
        self.forks = forks
        self.contributors = contributors
        self.downloads = downloads
        self.revenue = revenue
        self.issues = issues
        self.releases = releases
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "record_id": self.record_id,
            "timestamp": self.timestamp,
            "stars": self.stars,
            "forks": self.forks,
            "contributors": self.contributors,
            "downloads": self.downloads,
            "revenue": self.revenue,
            "issues": self.issues,
            "releases": self.releases
        }


class OutcomeMonitor:
    """
    Monitors interventions and tracks metrics over time.
    
    Every intervention creates watchers for:
    - GitHub stars
    - Forks
    - Contributors
    - Downloads
    - Revenue
    - Issues
    - Releases
    
    Snapshots at: 30d, 60d, 90d, 180d, 365d
    """
    
    def __init__(self, ledger: OutcomeLedger):
        self.ledger = ledger
        self.snapshots: Dict[str, List[MetricSnapshot]] = {}  # record_id -> list of snapshots
        self.snapshot_intervals = [30, 60, 90, 180, 365]  # days
    
    def start_monitoring(self, record_id: str):
        """Start monitoring an intervention."""
        if record_id not in self.snapshots:
            self.snapshots[record_id] = []
    
    def take_snapshot(
        self,
        record_id: str,
        stars: int,
        forks: int,
        contributors: int,
        downloads: int = None,
        revenue: float = None,
        issues: int = None,
        releases: int = None
    ) -> MetricSnapshot:
        """Take a snapshot of current metrics."""
        snapshot = MetricSnapshot(
            record_id=record_id,
            timestamp=datetime.now().isoformat(),
            stars=stars,
            forks=forks,
            contributors=contributors,
            downloads=downloads,
            revenue=revenue,
            issues=issues,
            releases=releases
        )
        
        if record_id not in self.snapshots:
            self.snapshots[record_id] = []
        
        self.snapshots[record_id].append(snapshot)
        
        return snapshot
    
    def get_snapshots(self, record_id: str) -> List[MetricSnapshot]:
        """Get all snapshots for a record."""
        return self.snapshots.get(record_id, [])
    
    def calculate_deltas(self, record_id: str) -> Dict[str, int]:
        """Calculate deltas from first to latest snapshot."""
        snapshots = self.get_snapshots(record_id)
        
        if len(snapshots) < 2:
            return {}
        
        first = snapshots[0]
        latest = snapshots[-1]
        
        deltas = {
            "stars_delta": latest.stars - first.stars,
            "forks_delta": latest.forks - first.forks,
            "contributors_delta": latest.contributors - first.contributors
        }
        
        if first.downloads is not None and latest.downloads is not None:
            deltas["downloads_delta"] = latest.downloads - first.downloads
        
        if first.revenue is not None and latest.revenue is not None:
            deltas["revenue_delta"] = latest.revenue - first.revenue
        
        if first.issues is not None and latest.issues is not None:
            deltas["issues_delta"] = latest.issues - first.issues
        
        if first.releases is not None and latest.releases is not None:
            deltas["releases_delta"] = latest.releases - first.releases
        
        return deltas
    
    def auto_update_outcome_ledger(self, record_id: str):
        """Auto-update outcome ledger with latest deltas."""
        record = self.ledger.get_record(record_id)
        
        if not record or record.status != InterventionStatus.IN_PROGRESS:
            return
        
        deltas = self.calculate_deltas(record_id)
        
        if deltas:
            # Update record with latest deltas
            record.actual_stars_delta = deltas.get("stars_delta")
            record.actual_downloads_delta = deltas.get("downloads_delta")
            record.actual_revenue_delta = deltas.get("revenue_delta")
            record.actual_contributors_delta = deltas.get("contributors_delta")
            
            self.ledger._save()


class GitHubMonitor:
    """Monitors GitHub repositories for metric changes."""
    
    def __init__(self, github_token: str = None):
        self.github_token = github_token
    
    def fetch_repo_metrics(self, repo_id: str) -> Dict[str, int]:
        """
        Fetch current metrics for a GitHub repo.
        
        Args:
            repo_id: owner/repo format
        
        Returns:
            Dict with stars, forks, contributors, issues, releases
        """
        # Placeholder - would use GitHub API
        # For now, return mock data
        return {
            "stars": 0,
            "forks": 0,
            "contributors": 0,
            "issues": 0,
            "releases": 0
        }
    
    def fetch_repo_metrics_real(self, repo_id: str) -> Dict[str, int]:
        """
        Fetch real metrics from GitHub API.
        
        Args:
            repo_id: owner/repo format
        
        Returns:
            Dict with stars, forks, contributors, issues, releases
        """
        import requests
        import time
        
        if not self.github_token:
            print("Warning: No GitHub token provided, using mock data")
            return self.fetch_repo_metrics(repo_id)
        
        owner, repo = repo_id.split("/")
        
        # Fetch repo data
        headers = {"Authorization": f"token {self.github_token}"}
        repo_url = f"https://api.github.com/repos/{owner}/{repo}"
        
        try:
            response = requests.get(repo_url, headers=headers)
            response.raise_for_status()
            repo_data = response.json()
            
            # Rate limiting - sleep if needed
            remaining = int(response.headers.get('X-RateLimit-Remaining', 1))
            if remaining < 10:
                reset_time = int(response.headers.get('X-RateLimit-Reset', time.time() + 60))
                sleep_time = max(reset_time - time.time(), 1)
                print(f"Rate limit approaching, sleeping {sleep_time:.0f}s")
                time.sleep(sleep_time)
            
            # Fetch contributors count
            contributors_url = f"https://api.github.com/repos/{owner}/{repo}/contributors"
            contributors_response = requests.get(contributors_url, headers=headers)
            contributors_response.raise_for_status()
            contributors_count = len(contributors_response.json())
            
            # Fetch open issues count
            issues_count = repo_data.get("open_issues_count", 0)
            
            # Fetch releases count
            releases_url = f"https://api.github.com/repos/{owner}/{repo}/releases"
            releases_response = requests.get(releases_url, headers=headers)
            releases_response.raise_for_status()
            releases_count = len(releases_response.json())
            
            return {
                "stars": repo_data.get("stargazers_count", 0),
                "forks": repo_data.get("forks_count", 0),
                "contributors": contributors_count,
                "issues": issues_count,
                "releases": releases_count
            }
        except requests.exceptions.RequestException as e:
            print(f"GitHub API error: {e}")
            return self.fetch_repo_metrics(repo_id)


class ScheduledMonitor:
    """Scheduled monitoring system for automatic snapshots."""
    
    def __init__(self, outcome_monitor: OutcomeMonitor, github_monitor: GitHubMonitor):
        self.outcome_monitor = outcome_monitor
        self.github_monitor = github_monitor
        self.running = False
        self.thread = None
    
    def start(self, interval_hours: int = 24):
        """Start scheduled monitoring."""
        if self.running:
            return
        
        self.running = True
        self.thread = threading.Thread(target=self._monitor_loop, args=(interval_hours,))
        self.thread.daemon = True
        self.thread.start()
    
    def stop(self):
        """Stop scheduled monitoring."""
        self.running = False
        if self.thread:
            self.thread.join()
    
    def _monitor_loop(self, interval_hours: int):
        """Main monitoring loop."""
        while self.running:
            try:
                self._check_all_interventions()
            except Exception as e:
                print(f"Monitoring error: {e}")
            
            # Sleep for interval
            time.sleep(interval_hours * 3600)
    
    def _check_all_interventions(self):
        """Check all active interventions and take snapshots if needed."""
        for record_id, record in self.outcome_monitor.ledger.records.items():
            if record.status != InterventionStatus.IN_PROGRESS:
                continue
            
            # Check if snapshot is due
            if self._is_snapshot_due(record_id):
                self._take_scheduled_snapshot(record_id)
    
    def _is_snapshot_due(self, record_id: str) -> bool:
        """Check if a snapshot is due for this record."""
        record = self.outcome_monitor.ledger.get_record(record_id)
        
        if not record or not record.start_date:
            return False
        
        start_date = datetime.fromisoformat(record.start_date)
        current_date = datetime.now()
        days_elapsed = (current_date - start_date).days
        
        # Get existing snapshots
        snapshots = self.outcome_monitor.get_snapshots(record_id)
        existing_days = [self._days_since_start(s.timestamp, start_date) for s in snapshots]
        
        # Check if any snapshot interval is due
        for interval in self.outcome_monitor.snapshot_intervals:
            if days_elapsed >= interval and interval not in existing_days:
                return True
        
        return False
    
    def _days_since_start(self, timestamp: str, start_date: datetime) -> int:
        """Calculate days since start date."""
        snapshot_date = datetime.fromisoformat(timestamp)
        return (snapshot_date - start_date).days
    
    def _take_scheduled_snapshot(self, record_id: str):
        """Take a scheduled snapshot for a record."""
        record = self.outcome_monitor.ledger.get_record(record_id)
        
        if not record:
            return
        
        # Fetch metrics based on asset type
        if record.asset_type == "github_repo":
            metrics = self.github_monitor.fetch_repo_metrics(record.asset_id)
            
            self.outcome_monitor.take_snapshot(
                record_id=record_id,
                stars=metrics["stars"],
                forks=metrics["forks"],
                contributors=metrics["contributors"],
                issues=metrics["issues"],
                releases=metrics["releases"]
            )
            
            # Auto-update outcome ledger
            self.outcome_monitor.auto_update_outcome_ledger(record_id)
            
            print(f"Snapshot taken for {record_id}")


class SnapshotManager:
    """Manages snapshot lifecycle and cleanup."""
    
    def __init__(self, outcome_monitor: OutcomeMonitor):
        self.outcome_monitor = outcome_monitor
    
    def get_snapshot_at_interval(self, record_id: str, interval_days: int) -> Optional[MetricSnapshot]:
        """Get snapshot at a specific interval from start."""
        record = self.outcome_monitor.ledger.get_record(record_id)
        
        if not record or not record.start_date:
            return None
        
        start_date = datetime.fromisoformat(record.start_date)
        snapshots = self.outcome_monitor.get_snapshots(record_id)
        
        for snapshot in snapshots:
            snapshot_date = datetime.fromisoformat(snapshot.timestamp)
            days_elapsed = (snapshot_date - start_date).days
            
            # Allow +/- 2 days tolerance
            if abs(days_elapsed - interval_days) <= 2:
                return snapshot
        
        return None
    
    def get_all_snapshots_summary(self, record_id: str) -> Dict[str, Any]:
        """Get summary of all snapshots for a record."""
        snapshots = self.outcome_monitor.get_snapshots(record_id)
        
        if not snapshots:
            return {"message": "No snapshots available"}
        
        summary = {
            "total_snapshots": len(snapshots),
            "first_snapshot": snapshots[0].timestamp,
            "latest_snapshot": snapshots[-1].timestamp,
            "intervals_covered": []
        }
        
        record = self.outcome_monitor.ledger.get_record(record_id)
        if record and record.start_date:
            start_date = datetime.fromisoformat(record.start_date)
            
            for interval in self.outcome_monitor.snapshot_intervals:
                snapshot = self.get_snapshot_at_interval(record_id, interval)
                if snapshot:
                    summary["intervals_covered"].append({
                        "interval_days": interval,
                        "timestamp": snapshot.timestamp,
                        "stars": snapshot.stars,
                        "forks": snapshot.forks,
                        "contributors": snapshot.contributors
                    })
        
        return summary
    
    def export_snapshots(self, record_id: str) -> List[Dict[str, Any]]:
        """Export all snapshots for a record."""
        snapshots = self.outcome_monitor.get_snapshots(record_id)
        return [s.to_dict() for s in snapshots]
    
    def cleanup_old_snapshots(self, record_id: str, keep_last_n: int = 10):
        """Clean up old snapshots, keeping only the most recent N."""
        snapshots = self.outcome_monitor.get_snapshots(record_id)
        
        if len(snapshots) <= keep_last_n:
            return
        
        # Keep only the last N
        self.outcome_monitor.snapshots[record_id] = snapshots[-keep_last_n:]
