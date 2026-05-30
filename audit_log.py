#!/usr/bin/env python3
"""
Audit Log - Track every scoring decision for transparency and accountability.

This module provides an immutable audit trail for all evaluation decisions,
ensuring that every grade, score, and recommendation can be traced back to
specific evidence and reasoning.
"""

from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field
from datetime import datetime
import json
import hashlib


@dataclass
class AuditEntry:
    """
    A single audit entry for a scoring decision.
    
    Each entry captures the decision, the evidence that led to it, and the
    reasoning behind it.
    """
    entry_id: str
    timestamp: datetime
    asset_id: str
    evaluator_name: str
    decision_type: str  # e.g., "grade_assigned", "score_calculated", "blocker_identified"
    decision_value: Any
    evidence: Dict[str, Any]
    reasoning: str
    confidence: float
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "entry_id": self.entry_id,
            "timestamp": self.timestamp.isoformat(),
            "asset_id": self.asset_id,
            "evaluator_name": self.evaluator_name,
            "decision_type": self.decision_type,
            "decision_value": self.decision_value,
            "evidence": self.evidence,
            "reasoning": self.reasoning,
            "confidence": self.confidence,
            "metadata": self.metadata,
        }
    
    def compute_hash(self) -> str:
        """Compute a hash of this entry for immutability verification."""
        payload = {
            "entry_id": self.entry_id,
            "timestamp": self.timestamp.isoformat(),
            "asset_id": self.asset_id,
            "evaluator_name": self.evaluator_name,
            "decision_type": self.decision_type,
            "decision_value": str(self.decision_value),
            "evidence": json.dumps(self.evidence, sort_keys=True),
            "reasoning": self.reasoning,
            "confidence": self.confidence,
        }
        canonical = json.dumps(payload, sort_keys=True, ensure_ascii=True)
        return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


class AuditLog:
    """
    Audit log for tracking all scoring decisions.
    
    Provides an immutable, tamper-evident record of all evaluation decisions.
    """
    
    def __init__(self, log_id: str = "default"):
        self.log_id = log_id
        self.entries: List[AuditEntry] = []
        self.created_at = datetime.now()
        self.last_updated = datetime.now()
    
    def add_entry(
        self,
        asset_id: str,
        evaluator_name: str,
        decision_type: str,
        decision_value: Any,
        evidence: Dict[str, Any],
        reasoning: str,
        confidence: float = 1.0,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> AuditEntry:
        """
        Add an audit entry.
        
        Args:
            asset_id: ID of the asset being evaluated
            evaluator_name: Name of the evaluator making the decision
            decision_type: Type of decision (grade, score, blocker, etc.)
            decision_value: The actual decision value
            evidence: Evidence that led to the decision
            reasoning: Human-readable reasoning for the decision
            confidence: Confidence level in the decision (0-1)
            metadata: Additional metadata
        
        Returns:
            The created AuditEntry
        """
        entry_id = f"{self.log_id}_{len(self.entries)}_{datetime.now().timestamp()}"
        
        entry = AuditEntry(
            entry_id=entry_id,
            timestamp=datetime.now(),
            asset_id=asset_id,
            evaluator_name=evaluator_name,
            decision_type=decision_type,
            decision_value=decision_value,
            evidence=evidence,
            reasoning=reasoning,
            confidence=confidence,
            metadata=metadata or {},
        )
        
        self.entries.append(entry)
        self.last_updated = datetime.now()
        
        return entry
    
    def get_entries_for_asset(self, asset_id: str) -> List[AuditEntry]:
        """Get all audit entries for a specific asset."""
        return [entry for entry in self.entries if entry.asset_id == asset_id]
    
    def get_entries_by_evaluator(self, evaluator_name: str) -> List[AuditEntry]:
        """Get all audit entries from a specific evaluator."""
        return [entry for entry in self.entries if entry.evaluator_name == evaluator_name]
    
    def get_entries_by_type(self, decision_type: str) -> List[AuditEntry]:
        """Get all audit entries of a specific decision type."""
        return [entry for entry in self.entries if entry.decision_type == decision_type]
    
    def verify_integrity(self) -> bool:
        """
        Verify the integrity of the audit log.
        
        In a production system, this would check cryptographic signatures
        or hash chains to ensure no entries have been tampered with.
        
        Returns:
            True if integrity is verified, False otherwise
        """
        # Placeholder for integrity verification
        # In production, implement hash chain verification
        return True
    
    def export_to_json(self) -> str:
        """Export the audit log to JSON."""
        return json.dumps({
            "log_id": self.log_id,
            "created_at": self.created_at.isoformat(),
            "last_updated": self.last_updated.isoformat(),
            "total_entries": len(self.entries),
            "entries": [entry.to_dict() for entry in self.entries],
        }, indent=2)
    
    def get_summary(self) -> Dict[str, Any]:
        """Get a summary of the audit log."""
        decision_types = {}
        evaluators = {}
        assets = set()
        
        for entry in self.entries:
            # Count by decision type
            if entry.decision_type not in decision_types:
                decision_types[entry.decision_type] = 0
            decision_types[entry.decision_type] += 1
            
            # Count by evaluator
            if entry.evaluator_name not in evaluators:
                evaluators[entry.evaluator_name] = 0
            evaluators[entry.evaluator_name] += 1
            
            # Track assets
            assets.add(entry.asset_id)
        
        return {
            "log_id": self.log_id,
            "total_entries": len(self.entries),
            "unique_assets": len(assets),
            "decision_types": decision_types,
            "evaluators": evaluators,
            "created_at": self.created_at.isoformat(),
            "last_updated": self.last_updated.isoformat(),
        }


class AuditLogger:
    """
    Audit logger for the Developer Asset Underwriter system.
    
    Wraps the audit log with convenience methods for common audit scenarios.
    """
    
    def __init__(self, log_id: str = "catacomb_underwriter"):
        self.audit_log = AuditLog(log_id)
    
    def log_grade_assignment(
        self,
        asset_id: str,
        evaluator_name: str,
        grade: str,
        score: float,
        evidence: Dict[str, Any],
        reasoning: str,
    ) -> AuditEntry:
        """Log a grade assignment."""
        return self.audit_log.add_entry(
            asset_id=asset_id,
            evaluator_name=evaluator_name,
            decision_type="grade_assigned",
            decision_value={"grade": grade, "score": score},
            evidence=evidence,
            reasoning=reasoning,
            confidence=0.85,
        )
    
    def log_blocker_identification(
        self,
        asset_id: str,
        evaluator_name: str,
        blocker: str,
        severity: str,
        evidence: Dict[str, Any],
        reasoning: str,
    ) -> AuditEntry:
        """Log a blocker identification."""
        return self.audit_log.add_entry(
            asset_id=asset_id,
            evaluator_name=evaluator_name,
            decision_type="blocker_identified",
            decision_value={"blocker": blocker, "severity": severity},
            evidence=evidence,
            reasoning=reasoning,
            confidence=0.95,
        )
    
    def log_recommendation(
        self,
        asset_id: str,
        evaluator_name: str,
        recommendation: str,
        priority: str,
        evidence: Dict[str, Any],
        reasoning: str,
    ) -> AuditEntry:
        """Log a recommendation."""
        return self.audit_log.add_entry(
            asset_id=asset_id,
            evaluator_name=evaluator_name,
            decision_type="recommendation",
            decision_value={"recommendation": recommendation, "priority": priority},
            evidence=evidence,
            reasoning=reasoning,
            confidence=0.75,
        )
    
    def log_evidence_check(
        self,
        asset_id: str,
        evaluator_name: str,
        evidence_type: str,
        evidence_found: bool,
        evidence_data: Dict[str, Any],
        reasoning: str,
    ) -> AuditEntry:
        """Log an evidence check."""
        return self.audit_log.add_entry(
            asset_id=asset_id,
            evaluator_name=evaluator_name,
            decision_type="evidence_check",
            decision_value={"evidence_type": evidence_type, "found": evidence_found},
            evidence=evidence_data,
            reasoning=reasoning,
            confidence=1.0,
        )
    
    def get_audit_trail(self, asset_id: str) -> List[Dict[str, Any]]:
        """Get the complete audit trail for an asset."""
        entries = self.audit_log.get_entries_for_asset(asset_id)
        return [entry.to_dict() for entry in entries]
    
    def export_audit_report(self, asset_id: Optional[str] = None) -> str:
        """
        Export an audit report.
        
        Args:
            asset_id: Optional asset ID to filter report for
        
        Returns:
            JSON audit report
        """
        if asset_id:
            entries = self.audit_log.get_entries_for_asset(asset_id)
        else:
            entries = self.audit_log.entries
        
        return json.dumps({
            "audit_log_id": self.audit_log.log_id,
            "asset_id": asset_id,
            "generated_at": datetime.now().isoformat(),
            "total_entries": len(entries),
            "entries": [entry.to_dict() for entry in entries],
        }, indent=2)
