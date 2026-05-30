#!/usr/bin/env python3
"""
Agent Work Auditor - Audit AI agent outputs like employee labor.

Answers:
- What did this agent create?
- What did it modify?
- What did it break?
- What did it leave incomplete?
- What files are duplicated?
- What work is production-ready?
- What work is scaffold only?
- What work has commercial value?
- What work needs human review?
- What work is risky?
- What work can be committed?
- What work can be sold?

This is not developer tooling. It is accounting, compliance, and management.
"""

from __future__ import annotations

import os
import hashlib
from decimal import Decimal
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field
from datetime import datetime

from collateral_packet import AssetRecord, AssetType


@dataclass
class AgentActivityRecord:
    """A single activity by an AI agent."""
    agent_name: str
    activity_type: str  # create, modify, delete, scaffold, test, deploy
    file_path: Optional[str] = None
    file_hash: Optional[str] = None
    timestamp: datetime = field(default_factory=datetime.now)
    description: str = ""
    estimated_value_usd: Decimal = Decimal("0")
    risk_flags: List[str] = field(default_factory=list)
    production_ready: bool = False

    def to_dict(self) -> Dict[str, Any]:
        return {
            "agent_name": self.agent_name,
            "activity_type": self.activity_type,
            "file_path": self.file_path,
            "file_hash": self.file_hash,
            "timestamp": self.timestamp.isoformat(),
            "description": self.description,
            "estimated_value_usd": str(self.estimated_value_usd),
            "risk_flags": self.risk_flags,
            "production_ready": self.production_ready,
        }


@dataclass
class AgentLaborReport:
    """
    CFO-readable report on agent productivity.

    Example:
    Agent: Windsurf
    Period: last 7 days
    Files created: 41
    Files modified: 96
    Commits prepared: 7
    Builds passed: 2
    Builds failed: 5
    Production-ready outputs: 3
    Scaffolds: 18
    Duplicates: 9
    Risky files: 2
    Estimated gross labor value: $6,400
    Estimated cleanup cost: $2,900
    Net useful value: $3,500
    Capitalizable work: $1,800
    """
    agent_name: str
    period_start: datetime
    period_end: datetime
    files_created: int = 0
    files_modified: int = 0
    files_deleted: int = 0
    commits_prepared: int = 0
    builds_passed: int = 0
    builds_failed: int = 0
    production_ready_outputs: int = 0
    scaffolds: int = 0
    duplicates: int = 0
    risky_files: int = 0
    estimated_gross_labor_value: Decimal = Decimal("0")
    estimated_cleanup_cost: Decimal = Decimal("0")
    net_useful_value: Decimal = Decimal("0")
    capitalizable_work: Decimal = Decimal("0")
    activities: List[AgentActivityRecord] = field(default_factory=list)
    risk_summary: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "agent_name": self.agent_name,
            "period_start": self.period_start.isoformat(),
            "period_end": self.period_end.isoformat(),
            "files_created": self.files_created,
            "files_modified": self.files_modified,
            "files_deleted": self.files_deleted,
            "commits_prepared": self.commits_prepared,
            "builds_passed": self.builds_passed,
            "builds_failed": self.builds_failed,
            "production_ready_outputs": self.production_ready_outputs,
            "scaffolds": self.scaffolds,
            "duplicates": self.duplicates,
            "risky_files": self.risky_files,
            "estimated_gross_labor_value": str(self.estimated_gross_labor_value),
            "estimated_cleanup_cost": str(self.estimated_cleanup_cost),
            "net_useful_value": str(self.net_useful_value),
            "capitalizable_work": str(self.capitalizable_work),
            "activities": [a.to_dict() for a in self.activities],
            "risk_summary": self.risk_summary,
        }

    def summary_text(self) -> str:
        return (
            f"Agent Labor Report: {self.agent_name}\n"
            f"  Period: {self.period_start.date()} to {self.period_end.date()}\n"
            f"  Files created: {self.files_created}\n"
            f"  Files modified: {self.files_modified}\n"
            f"  Commits prepared: {self.commits_prepared}\n"
            f"  Builds passed: {self.builds_passed}\n"
            f"  Builds failed: {self.builds_failed}\n"
            f"  Production-ready: {self.production_ready_outputs}\n"
            f"  Scaffolds: {self.scaffolds}\n"
            f"  Duplicates: {self.duplicates}\n"
            f"  Risky files: {self.risky_files}\n"
            f"  Gross labor value: ${int(self.estimated_gross_labor_value):,}\n"
            f"  Cleanup cost: ${int(self.estimated_cleanup_cost):,}\n"
            f"  Net useful value: ${int(self.net_useful_value):,}\n"
            f"  Capitalizable work: ${int(self.capitalizable_work):,}\n"
        )


class AgentWorkAuditor:
    """
    Audits AI agent work like employee or contractor labor.

    Supports:
    - Windsurf
    - Cursor
    - Claude Code
    - ChatGPT exports
    - Codex
    - Devin-style agents
    - Local shell agents
    - GitHub Actions agents
    - Autonomous repo workers
    """

    # Estimated hourly cost of engineering labor for valuation
    ENGINEERING_RATE_USD = Decimal("75")

    # Cleanup cost multipliers
    CLEANUP_RATES = {
        "scaffold": Decimal("15"),      # per file
        "duplicate": Decimal("10"),     # per file
        "risky": Decimal("150"),        # per file
        "broken_build": Decimal("200"), # per incident
        "missing_tests": Decimal("50"), # per file
    }

    def __init__(self, engineering_rate: Optional[Decimal] = None):
        self.engineering_rate = engineering_rate or self.ENGINEERING_RATE_USD

    def audit_agent_session(
        self,
        agent_name: str,
        activities: List[AgentActivityRecord],
        period_start: Optional[datetime] = None,
        period_end: Optional[datetime] = None,
    ) -> AgentLaborReport:
        """
        Audit a single agent session or period.

        Args:
            agent_name: Name of the agent (e.g., "windsurf", "cursor")
            activities: List of activity records from the session.
            period_start: Start of audit period.
            period_end: End of audit period.

        Returns:
            AgentLaborReport with full accounting.
        """
        period_start = period_start or datetime.now()
        period_end = period_end or datetime.now()

        report = AgentLaborReport(
            agent_name=agent_name,
            period_start=period_start,
            period_end=period_end,
            activities=activities,
        )

        created_hashes: Dict[str, str] = {}
        modified_hashes: Dict[str, str] = {}

        for activity in activities:
            if activity.activity_type == "create":
                report.files_created += 1
                if activity.file_hash:
                    created_hashes[activity.file_path] = activity.file_hash
            elif activity.activity_type == "modify":
                report.files_modified += 1
                if activity.file_path:
                    modified_hashes[activity.file_path] = activity.file_hash or ""
            elif activity.activity_type == "delete":
                report.files_deleted += 1
            elif activity.activity_type == "commit":
                report.commits_prepared += 1
            elif activity.activity_type == "build_pass":
                report.builds_passed += 1
            elif activity.activity_type == "build_fail":
                report.builds_failed += 1

            if activity.production_ready:
                report.production_ready_outputs += 1

            if activity.risk_flags:
                report.risky_files += 1
                report.risk_summary.extend(activity.risk_flags)

        # Detect duplicates among created files
        hash_counts: Dict[str, int] = {}
        for h in created_hashes.values():
            hash_counts[h] = hash_counts.get(h, 0) + 1
        report.duplicates = sum(1 for count in hash_counts.values() if count > 1)

        # Detect scaffolds (small files with minimal content)
        for activity in activities:
            if activity.activity_type == "create" and activity.file_path:
                # Simplified: if no hash or marked as scaffold
                if not activity.production_ready and activity.estimated_value_usd < Decimal("50"):
                    report.scaffolds += 1

        # Calculate labor value
        total_hours = self._estimate_hours(activities)
        report.estimated_gross_labor_value = total_hours * self.engineering_rate

        # Calculate cleanup cost
        cleanup = Decimal("0")
        cleanup += Decimal(report.scaffolds) * self.CLEANUP_RATES["scaffold"]
        cleanup += Decimal(report.duplicates) * self.CLEANUP_RATES["duplicate"]
        cleanup += Decimal(report.risky_files) * self.CLEANUP_RATES["risky"]
        cleanup += Decimal(report.builds_failed) * self.CLEANUP_RATES["broken_build"]
        report.estimated_cleanup_cost = cleanup

        report.net_useful_value = max(
            Decimal("0"),
            report.estimated_gross_labor_value - report.estimated_cleanup_cost,
        )

        # Capitalizable work = production-ready outputs minus risky files
        capitalizable_files = max(0, report.production_ready_outputs - report.risky_files)
        report.capitalizable_work = (
            Decimal(capitalizable_files) * self.engineering_rate * Decimal("2")
        )  # assume 2 hours each

        return report

    def audit_directory(
        self,
        agent_name: str,
        directory_path: str,
        period_start: Optional[datetime] = None,
        period_end: Optional[datetime] = None,
    ) -> AgentLaborReport:
        """
        Audit a directory of agent outputs by scanning files.

        Args:
            agent_name: Name of the agent.
            directory_path: Path to directory to audit.
            period_start: Start of period.
            period_end: End of period.

        Returns:
            AgentLaborReport derived from filesystem scan.
        """
        activities = []
        if os.path.isdir(directory_path):
            for root, _, files in os.walk(directory_path):
                for filename in files:
                    filepath = os.path.join(root, filename)
                    try:
                        with open(filepath, "rb") as f:
                            content = f.read()
                        file_hash = hashlib.sha256(content).hexdigest()
                        file_size = len(content)

                        # Heuristic classification
                        is_scaffold = file_size < 500
                        is_risky = self._check_risk_patterns(content.decode("utf-8", errors="ignore"))

                        activity = AgentActivityRecord(
                            agent_name=agent_name,
                            activity_type="create",
                            file_path=filepath,
                            file_hash=file_hash,
                            description=f"File size: {file_size} bytes",
                            estimated_value_usd=Decimal(str(file_size / 100)),
                            production_ready=not is_scaffold and not is_risky,
                            risk_flags=["suspicious_patterns"] if is_risky else [],
                        )
                        activities.append(activity)
                    except Exception:
                        continue

        return self.audit_agent_session(agent_name, activities, period_start, period_end)

    def _estimate_hours(self, activities: List[AgentActivityRecord]) -> Decimal:
        """Estimate engineering hours represented by activities."""
        # Rough heuristic: each file creation = 0.5 hours
        # each modification = 0.25 hours
        # each build/test = 1 hour
        hours = Decimal("0")
        for activity in activities:
            if activity.activity_type == "create":
                hours += Decimal("0.5")
            elif activity.activity_type == "modify":
                hours += Decimal("0.25")
            elif activity.activity_type in ["build_pass", "build_fail", "test"]:
                hours += Decimal("1.0")
            elif activity.activity_type == "commit":
                hours += Decimal("0.25")
        return hours

    def _check_risk_patterns(self, content: str) -> bool:
        """Check for suspicious patterns in file content."""
        risk_keywords = [
            "password",
            "secret_key",
            "api_key",
            "private_key",
            "token",
            "eval(",
            "exec(",
            "os.system",
            "subprocess.call",
        ]
        content_lower = content.lower()
        return any(kw in content_lower for kw in risk_keywords)

    def generate_combined_report(
        self, reports: List[AgentLaborReport]
    ) -> Dict[str, Any]:
        """
        Combine multiple agent reports into a portfolio-level labor summary.

        Returns:
            Dict with aggregated accounting across all agents.
        """
        total_gross = Decimal("0")
        total_cleanup = Decimal("0")
        total_net = Decimal("0")
        total_capitalizable = Decimal("0")
        total_created = 0
        total_modified = 0
        total_ready = 0
        total_scaffolds = 0
        total_duplicates = 0
        total_risky = 0
        total_builds_failed = 0

        agent_breakdown = []
        for report in reports:
            total_gross += report.estimated_gross_labor_value
            total_cleanup += report.estimated_cleanup_cost
            total_net += report.net_useful_value
            total_capitalizable += report.capitalizable_work
            total_created += report.files_created
            total_modified += report.files_modified
            total_ready += report.production_ready_outputs
            total_scaffolds += report.scaffolds
            total_duplicates += report.duplicates
            total_risky += report.risky_files
            total_builds_failed += report.builds_failed
            agent_breakdown.append(report.to_dict())

        return {
            "period": {
                "start": min(r.period_start for r in reports).isoformat(),
                "end": max(r.period_end for r in reports).isoformat(),
            },
            "aggregate": {
                "agents_audited": len(reports),
                "files_created": total_created,
                "files_modified": total_modified,
                "production_ready_outputs": total_ready,
                "scaffolds": total_scaffolds,
                "duplicates": total_duplicates,
                "risky_files": total_risky,
                "builds_failed": total_builds_failed,
                "estimated_gross_labor_value": str(total_gross),
                "estimated_cleanup_cost": str(total_cleanup),
                "net_useful_value": str(total_net),
                "capitalizable_work": str(total_capitalizable),
            },
            "agent_breakdown": agent_breakdown,
            "cfo_summary": (
                f"Across {len(reports)} agents, we see {total_created} files created, "
                f"{total_ready} production-ready outputs, {total_scaffolds} scaffolds, "
                f"and {total_risky} risky files. Net useful value is ${int(total_net):,} "
                f"after ${int(total_cleanup):,} in estimated cleanup. "
                f"Capitalizable work: ${int(total_capitalizable):,}."
            ),
        }
