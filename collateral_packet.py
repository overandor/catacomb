#!/usr/bin/env python3
"""
Collateral Packet - Core financial object for Software Collateral Execution.

This module defines the Software Collateral Packet: a bundled evidence object
that makes software work legible to lenders, buyers, brokers, and investors.

Doctrines enforced:
- A file is not money.
- Appraisal is not liquidity.
- Strategic value is not collateral value.
- Software becomes financeable only when proof reduces uncertainty.
- The packet is the product.
"""

from __future__ import annotations

import hashlib
import json
import uuid
from dataclasses import dataclass, field, asdict
from datetime import datetime
from decimal import Decimal, ROUND_HALF_EVEN
from enum import Enum
from typing import Dict, Any, List, Optional, Tuple


class AssetType(Enum):
    """Institutional asset classifications."""
    ORIGINAL_REPOSITORY = "original_repository"
    LOCAL_FOLDER = "local_folder"
    HUGGING_FACE_SPACE = "hugging_face_space"
    DEPLOYED_API = "deployed_api"
    AI_AGENT_OUTPUT = "ai_agent_output"
    RESEARCH_PAPER = "research_paper"
    PROMPT_SYSTEM = "prompt_system"
    DATASET = "dataset"
    TRADING_ENGINE = "trading_engine"
    PROTOCOL_SMART_CONTRACT = "protocol_smart_contract"
    FRONTEND_PRODUCT = "frontend_product"
    BACKEND_SERVICE = "backend_service"
    DOCUMENTATION_PACKAGE = "documentation_package"
    PATENT_IP_RECORD = "patent_ip_record"
    PROOF_LEDGER = "proof_ledger"
    OUTREACH_SALES_SYSTEM = "outreach_sales_system"
    FORK_TEMPLATE = "fork_template"
    SCAFFOLD = "scaffold"
    DUPLICATE = "duplicate"
    JUNK = "junk"
    RISK_BLOCKED = "risk_blocked"


class ProofLevel(Enum):
    """Trust ladder for asset verification."""
    CLAIMED = 0
    DISCOVERED = 1
    HASHED = 2
    CLEAN = 3
    BUILD_VERIFIED = 4
    USE_VERIFIED = 5
    MARKET_VERIFIED = 6
    FINANCEABLE = 7


class CapitalReadinessState(Enum):
    """Pipeline state for asset maturity."""
    DISCOVERED = "discovered"
    CLASSIFIED = "classified"
    PROOF_STARTED = "proof_started"
    PROOF_COMPLETE = "proof_complete"
    RISK_BLOCKED = "risk_blocked"
    BUILD_VERIFIED = "build_verified"
    PACKET_READY = "packet_ready"
    BUYER_READY = "buyer_ready"
    LENDER_READY = "lender_ready"
    MARKET_TESTED = "market_tested"
    FINANCEABLE = "financeable"
    MONITORED_COLLATERAL = "monitored_collateral"
    ARCHIVED = "archived"


class RiskBlockReason(Enum):
    """Reasons an asset may be blocked from monetization."""
    SECRETS_DETECTED = "secrets_detected"
    PRIVATE_KEYS_DETECTED = "private_keys_detected"
    UNCLEAR_OWNERSHIP = "unclear_ownership"
    EMPLOYER_CLIENT_OWNERSHIP_RISK = "employer_client_ownership_risk"
    COPIED_REPO = "copied_repo"
    FORK_CONTAMINATION = "fork_contamination"
    MISSING_LICENSE = "missing_license"
    MALWARE_LIKE_BEHAVIOR = "malware_like_behavior"
    FINANCIAL_CLAIMS_WITHOUT_PROOF = "financial_claims_without_proof"
    ILLEGAL_OR_REGULATED_ACTIVITY = "illegal_or_regulated_activity"
    PRIVACY_PII_EXPOSURE = "privacy_pii_exposure"
    BROKEN_BUILD_WITH_INFLATED_CLAIMS = "broken_build_with_inflated_claims"


@dataclass
class HashManifest:
    """Tamper-evident file hash manifest."""
    folder_hash: str
    file_hashes: Dict[str, str] = field(default_factory=dict)
    merkle_root: Optional[str] = None
    generated_at: datetime = field(default_factory=datetime.now)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "folder_hash": self.folder_hash,
            "file_hashes": self.file_hashes,
            "merkle_root": self.merkle_root,
            "generated_at": self.generated_at.isoformat(),
        }


@dataclass
class ValuationSet:
    """
    Six-value institutional appraisal.

    Do not mix these into one number. They answer different questions.
    """
    replacement_cost_usd: Decimal = Decimal("0")
    as_is_sale_value_usd: Decimal = Decimal("0")
    productized_value_usd: Decimal = Decimal("0")
    liquidation_value_usd: Decimal = Decimal("0")
    collateral_support_value_usd: Decimal = Decimal("0")
    financeability_score: int = 0  # 0-100

    # Confidence bands
    replacement_cost_range: Tuple[Decimal, Decimal] = (Decimal("0"), Decimal("0"))
    as_is_sale_range: Tuple[Decimal, Decimal] = (Decimal("0"), Decimal("0"))
    liquidation_range: Tuple[Decimal, Decimal] = (Decimal("0"), Decimal("0"))
    collateral_support_range: Tuple[Decimal, Decimal] = (Decimal("0"), Decimal("0"))

    # Methodology note
    methodology_version: str = "collateral_ops_v1"
    generated_at: datetime = field(default_factory=datetime.now)

    def to_dict(self) -> Dict[str, Any]:
        def _fmt(d: Decimal) -> str:
            return str(d.quantize(Decimal("0.01"), rounding=ROUND_HALF_EVEN))

        def _range(t: Tuple[Decimal, Decimal]) -> List[str]:
            return [_fmt(t[0]), _fmt(t[1])]

        return {
            "replacement_cost_usd": _fmt(self.replacement_cost_usd),
            "as_is_sale_value_usd": _fmt(self.as_is_sale_value_usd),
            "productized_value_usd": _fmt(self.productized_value_usd),
            "liquidation_value_usd": _fmt(self.liquidation_value_usd),
            "collateral_support_value_usd": _fmt(self.collateral_support_value_usd),
            "financeability_score": self.financeability_score,
            "replacement_cost_range": _range(self.replacement_cost_range),
            "as_is_sale_range": _range(self.as_is_sale_range),
            "liquidation_range": _range(self.liquidation_range),
            "collateral_support_range": _range(self.collateral_support_range),
            "methodology_version": self.methodology_version,
            "generated_at": self.generated_at.isoformat(),
        }


@dataclass
class DeductionSchedule:
    """Transparent haircuts applied to value."""
    base_strategic_value: Decimal = Decimal("0")
    deductions: List[Dict[str, Any]] = field(default_factory=list)
    final_collateral_support: Decimal = Decimal("0")

    def to_dict(self) -> Dict[str, Any]:
        def _clean(val):
            if isinstance(val, Decimal):
                return str(val.quantize(Decimal("0.01"), rounding=ROUND_HALF_EVEN))
            if isinstance(val, dict):
                return {k: _clean(v) for k, v in val.items()}
            return val

        return {
            "base_strategic_value": str(self.base_strategic_value),
            "deductions": [_clean(d) for d in self.deductions],
            "final_collateral_support": str(self.final_collateral_support),
        }


@dataclass
class RiskRegister:
    """Structured risk findings with severity."""
    ownership_risk: str = "unknown"  # low, medium, high
    originality_risk: str = "unknown"
    build_risk: str = "unknown"
    license_risk: str = "unknown"
    secret_risk: str = "unknown"
    legal_risk: str = "unknown"
    security_risk: str = "unknown"
    market_risk: str = "unknown"
    liquidation_risk: str = "unknown"
    revenue_risk: str = "unknown"

    risk_flags: List[str] = field(default_factory=list)
    blockers: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "ownership_risk": self.ownership_risk,
            "originality_risk": self.originality_risk,
            "build_risk": self.build_risk,
            "license_risk": self.license_risk,
            "secret_risk": self.secret_risk,
            "legal_risk": self.legal_risk,
            "security_risk": self.security_risk,
            "market_risk": self.market_risk,
            "liquidation_risk": self.liquidation_risk,
            "revenue_risk": self.revenue_risk,
            "risk_flags": self.risk_flags,
            "blockers": self.blockers,
        }


@dataclass
class BuyerUniverseEntry:
    """A potential acquirer or licensee."""
    buyer_name: str
    buyer_category: str
    fit_reason: str
    estimated_budget_band: str
    contact_route: Optional[str] = None
    strategic_relevance: int = 0  # 0-100
    risk_level: str = "medium"
    expected_response_probability: float = 0.0
    expected_sale_difficulty: str = "medium"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "buyer_name": self.buyer_name,
            "buyer_category": self.buyer_category,
            "fit_reason": self.fit_reason,
            "estimated_budget_band": self.estimated_budget_band,
            "contact_route": self.contact_route,
            "strategic_relevance": self.strategic_relevance,
            "risk_level": self.risk_level,
            "expected_response_probability": self.expected_response_probability,
            "expected_sale_difficulty": self.expected_sale_difficulty,
        }


@dataclass
class LiquidationRoute:
    """Pre-planned recovery path for lenders."""
    default_trigger: str = "payment_default_or_breach"
    access_rights: str = "owner_transfer_with_legal_review"
    asset_transfer_method: str = "repo_transfer_plus_documentation"
    buyer_list: List[BuyerUniverseEntry] = field(default_factory=list)
    broker_route: Optional[str] = None
    auction_route: Optional[str] = None
    expected_timeline_days: Tuple[int, int] = (45, 120)
    expected_recovery_band: Tuple[Decimal, Decimal] = (Decimal("0"), Decimal("0"))
    legal_review_required: bool = True

    def to_dict(self) -> Dict[str, Any]:
        return {
            "default_trigger": self.default_trigger,
            "access_rights": self.access_rights,
            "asset_transfer_method": self.asset_transfer_method,
            "buyer_list": [b.to_dict() for b in self.buyer_list],
            "broker_route": self.broker_route,
            "auction_route": self.auction_route,
            "expected_timeline_days": list(self.expected_timeline_days),
            "expected_recovery_band": [str(self.expected_recovery_band[0]), str(self.expected_recovery_band[1])],
            "legal_review_required": self.legal_review_required,
        }


@dataclass
class MonitoringPlan:
    """Ongoing collateral monitoring requirements."""
    monthly_hash_snapshot: bool = True
    monthly_build_check: bool = True
    monthly_secret_scan: bool = True
    monthly_license_check: bool = True
    deployment_status_check: bool = True
    revenue_adoption_update: bool = False
    owner_attestation_required: bool = True
    change_log_required: bool = True
    risk_flag_update: bool = True

    def to_dict(self) -> Dict[str, Any]:
        return {k: v for k, v in asdict(self).items()}


@dataclass
class AssetRecord:
    """
    Core institutional record for a discovered software asset.

    This is the bridge between local app, dashboard, PDF, lender packet,
    buyer packet, marketplace listing, agent improvement queue, and protocol.
    """
    # Identity
    asset_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    asset_name: str = ""
    asset_type: AssetType = AssetType.ORIGINAL_REPOSITORY
    owner_claim: str = ""
    source_type: str = "github"
    source_path: Optional[str] = None
    repo_url: Optional[str] = None
    deployment_url: Optional[str] = None
    created_at: Optional[datetime] = None
    last_modified: Optional[datetime] = None

    # Technical inventory
    primary_language: str = ""
    framework_stack: List[str] = field(default_factory=list)
    file_count: int = 0
    total_size_bytes: int = 0
    git_commit_snapshot: Optional[str] = None

    # Contributors
    contributor_list: List[str] = field(default_factory=list)
    marketability_score: int = 0  # 0-100, external signal

    # Proof statuses
    hash_manifest: Optional[HashManifest] = None
    build_status: str = "unknown"  # passed, failed, not_tested, unknown
    test_status: str = "unknown"
    deployment_status: str = "unknown"
    license_status: str = "unknown"
    secret_scan_status: str = "unknown"
    fork_status: str = "unknown"
    documentation_score: int = 0  # 0-100
    originality_score: int = 0  # 0-100

    # Economic appraisal
    valuation: Optional[ValuationSet] = None
    deduction_schedule: Optional[DeductionSchedule] = None

    # Risk
    risk_register: RiskRegister = field(default_factory=RiskRegister)
    risk_block_reasons: List[RiskBlockReason] = field(default_factory=list)

    # Market
    buyer_universe: List[BuyerUniverseEntry] = field(default_factory=list)
    liquidation_route: Optional[LiquidationRoute] = None
    revenue_evidence: List[Dict[str, Any]] = field(default_factory=list)

    # Financeability
    proof_level: ProofLevel = ProofLevel.CLAIMED
    capital_readiness_state: CapitalReadinessState = CapitalReadinessState.DISCOVERED
    financeability_score: int = 0

    # Improvement queue
    next_actions: List[Dict[str, Any]] = field(default_factory=list)

    # Packet status
    packet_status: str = "draft"  # draft, review_ready, human_reviewed, signed
    reviewer_signatures: List[Dict[str, Any]] = field(default_factory=list)
    generated_at: datetime = field(default_factory=datetime.now)
    packet_hash: Optional[str] = None

    def compute_packet_hash(self) -> str:
        """Deterministic packet hash for tamper evidence."""
        payload = {
            "asset_id": self.asset_id,
            "asset_name": self.asset_name,
            "owner_claim": self.owner_claim,
            "source_path": self.source_path,
            "valuation": self.valuation.to_dict() if self.valuation else None,
            "risk_register": self.risk_register.to_dict(),
            "generated_at": self.generated_at.isoformat(),
        }
        canonical = json.dumps(payload, sort_keys=True, ensure_ascii=True)
        return hashlib.sha256(canonical.encode("utf-8")).hexdigest()

    def seal_packet(self):
        """Finalize packet and compute hash."""
        self.packet_hash = self.compute_packet_hash()
        self.packet_status = "review_ready"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "asset_id": self.asset_id,
            "asset_name": self.asset_name,
            "asset_type": self.asset_type.value,
            "owner_claim": self.owner_claim,
            "source_type": self.source_type,
            "source_path": self.source_path,
            "repo_url": self.repo_url,
            "deployment_url": self.deployment_url,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "last_modified": self.last_modified.isoformat() if self.last_modified else None,
            "primary_language": self.primary_language,
            "framework_stack": self.framework_stack,
            "file_count": self.file_count,
            "total_size_bytes": self.total_size_bytes,
            "git_commit_snapshot": self.git_commit_snapshot,
            "hash_manifest": self.hash_manifest.to_dict() if self.hash_manifest else None,
            "build_status": self.build_status,
            "test_status": self.test_status,
            "deployment_status": self.deployment_status,
            "license_status": self.license_status,
            "secret_scan_status": self.secret_scan_status,
            "fork_status": self.fork_status,
            "documentation_score": self.documentation_score,
            "originality_score": self.originality_score,
            "valuation": self.valuation.to_dict() if self.valuation else None,
            "deduction_schedule": self.deduction_schedule.to_dict() if self.deduction_schedule else None,
            "risk_register": self.risk_register.to_dict(),
            "risk_block_reasons": [r.value for r in self.risk_block_reasons],
            "buyer_universe": [b.to_dict() for b in self.buyer_universe],
            "liquidation_route": self.liquidation_route.to_dict() if self.liquidation_route else None,
            "revenue_evidence": self.revenue_evidence,
            "proof_level": self.proof_level.value,
            "capital_readiness_state": self.capital_readiness_state.value,
            "financeability_score": self.financeability_score,
            "next_actions": self.next_actions,
            "packet_status": self.packet_status,
            "reviewer_signatures": self.reviewer_signatures,
            "generated_at": self.generated_at.isoformat(),
            "packet_hash": self.packet_hash,
        }


@dataclass
class SoftwareCollateralPacket:
    """
    The exportable financial wrapper around software work.

    Structured in four standard sections:
    A. Identity and Ownership
    B. Technical Proof
    C. Economic Appraisal
    D. Monetization and Recovery Route
    """
    packet_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    packet_version: str = "collateral_ops_v1.0"
    generated_at: datetime = field(default_factory=datetime.now)
    packet_hash: Optional[str] = None

    # Section A: Identity and Ownership
    asset_record: Optional[AssetRecord] = None
    owner_identity: Dict[str, Any] = field(default_factory=dict)
    ownership_declaration: str = ""
    employer_client_risk_disclosure: str = ""
    contributor_list: List[str] = field(default_factory=list)

    # Section B: Technical Proof
    file_hash_manifest: Optional[HashManifest] = None
    commit_snapshot: Optional[str] = None
    build_log: Optional[str] = None
    test_log: Optional[str] = None
    dependency_manifest: List[str] = field(default_factory=list)
    secret_scan_report: Dict[str, Any] = field(default_factory=dict)
    license_scan_report: Dict[str, Any] = field(default_factory=dict)
    fork_scan_report: Dict[str, Any] = field(default_factory=dict)
    readme_docs_review: Dict[str, Any] = field(default_factory=dict)
    endpoint_verification: Dict[str, Any] = field(default_factory=dict)
    deployment_screenshots: List[str] = field(default_factory=list)
    demo_link: Optional[str] = None
    agent_activity_logs: List[Dict[str, Any]] = field(default_factory=list)

    # Section C: Economic Appraisal
    valuation: Optional[ValuationSet] = None
    deduction_schedule: Optional[DeductionSchedule] = None
    comparable_assets: List[Dict[str, Any]] = field(default_factory=list)
    confidence_score: int = 0

    # Section D: Monetization and Recovery
    buyer_universe: List[BuyerUniverseEntry] = field(default_factory=list)
    broker_list: List[str] = field(default_factory=list)
    licensee_list: List[str] = field(default_factory=list)
    lender_list: List[str] = field(default_factory=list)
    outreach_plan: str = ""
    auction_listing_strategy: Optional[str] = None
    sale_memo: Optional[str] = None
    productization_plan: Optional[str] = None
    nda_checklist: List[str] = field(default_factory=list)
    forced_sale_timeline_days: Tuple[int, int] = (45, 120)
    expected_recovery_range: Tuple[Decimal, Decimal] = (Decimal("0"), Decimal("0"))
    recommended_loan_to_value: str = ""
    liquidation_route: Optional[LiquidationRoute] = None
    monitoring_plan: Optional[MonitoringPlan] = None

    # Disclaimers
    legal_disclaimers: str = (
        "This packet is a draft appraisal and diligence support document. "
        "It is not legal advice, not tax advice, not a guaranteed sale value, "
        "and not a loan approval. Human review is recommended. "
        "Appraisal is not liquidity."
    )

    def compute_packet_hash(self) -> str:
        """Deterministic hash of the entire packet."""
        payload = {
            "packet_id": self.packet_id,
            "packet_version": self.packet_version,
            "asset_id": self.asset_record.asset_id if self.asset_record else None,
            "valuation": self.valuation.to_dict() if self.valuation else None,
            "generated_at": self.generated_at.isoformat(),
        }
        canonical = json.dumps(payload, sort_keys=True, ensure_ascii=True)
        return hashlib.sha256(canonical.encode("utf-8")).hexdigest()

    def seal(self):
        """Seal packet for export."""
        self.packet_hash = self.compute_packet_hash()

    def to_dict(self) -> Dict[str, Any]:
        def _fmt_dec(d: Decimal) -> str:
            return str(d.quantize(Decimal("0.01"), rounding=ROUND_HALF_EVEN))

        return {
            "packet_id": self.packet_id,
            "packet_version": self.packet_version,
            "generated_at": self.generated_at.isoformat(),
            "packet_hash": self.packet_hash,
            "section_a_identity": {
                "asset_record": self.asset_record.to_dict() if self.asset_record else None,
                "owner_identity": self.owner_identity,
                "ownership_declaration": self.ownership_declaration,
                "employer_client_risk_disclosure": self.employer_client_risk_disclosure,
                "contributor_list": self.contributor_list,
            },
            "section_b_technical_proof": {
                "file_hash_manifest": self.file_hash_manifest.to_dict() if self.file_hash_manifest else None,
                "commit_snapshot": self.commit_snapshot,
                "build_log": self.build_log,
                "test_log": self.test_log,
                "dependency_manifest": self.dependency_manifest,
                "secret_scan_report": self.secret_scan_report,
                "license_scan_report": self.license_scan_report,
                "fork_scan_report": self.fork_scan_report,
                "readme_docs_review": self.readme_docs_review,
                "endpoint_verification": self.endpoint_verification,
                "deployment_screenshots": self.deployment_screenshots,
                "demo_link": self.demo_link,
                "agent_activity_logs": self.agent_activity_logs,
            },
            "section_c_economic_appraisal": {
                "valuation": self.valuation.to_dict() if self.valuation else None,
                "deduction_schedule": self.deduction_schedule.to_dict() if self.deduction_schedule else None,
                "comparable_assets": self.comparable_assets,
                "confidence_score": self.confidence_score,
            },
            "section_d_monetization_recovery": {
                "buyer_universe": [b.to_dict() for b in self.buyer_universe],
                "broker_list": self.broker_list,
                "licensee_list": self.licensee_list,
                "lender_list": self.lender_list,
                "outreach_plan": self.outreach_plan,
                "auction_listing_strategy": self.auction_listing_strategy,
                "sale_memo": self.sale_memo,
                "nda_checklist": self.nda_checklist,
                "forced_sale_timeline_days": list(self.forced_sale_timeline_days),
                "expected_recovery_range": [_fmt_dec(self.expected_recovery_range[0]), _fmt_dec(self.expected_recovery_range[1])],
                "recommended_loan_to_value": self.recommended_loan_to_value,
                "liquidation_route": self.liquidation_route.to_dict() if self.liquidation_route else None,
                "monitoring_plan": self.monitoring_plan.to_dict() if self.monitoring_plan else None,
            },
            "legal_disclaimers": self.legal_disclaimers,
        }

    def to_json(self, indent: int = 2) -> str:
        return json.dumps(self.to_dict(), indent=indent, ensure_ascii=True)
