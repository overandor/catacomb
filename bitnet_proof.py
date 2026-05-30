#!/usr/bin/env python3
"""
BitNet Proof Verification - Security layer for cryptographic proof validation.

This module provides:
- BitNet proof packet structure for intervention evidence
- Cryptographic proof verification using SHA-256 and HMAC
- Evidence packet generation for asset interventions
- Integration with Outcome Ledger for proof storage
- Proof validation for intervention authenticity
"""

import hashlib
import hmac
import json
import sqlite3
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field
from datetime import datetime
import secrets


@dataclass
class BitNetProofPacket:
    """
    BitNet Proof Packet - Cryptographic evidence packet for interventions.
    
    Structure:
    - Header: Version, packet type, timestamp
    - Evidence: Asset ID, intervention type, before/after states
    - Proof: SHA-256 hash, HMAC signature, nonce
    - Metadata: Creator, chain of custody, verification status
    """
    # Header
    version: str = "1.0"
    packet_type: str = "intervention_evidence"
    timestamp: datetime = field(default_factory=datetime.now)
    
    # Evidence
    asset_id: str = ""
    intervention_type: str = ""
    before_state: Dict[str, Any] = field(default_factory=dict)
    after_state: Dict[str, Any] = field(default_factory=dict)
    predicted_outcome: Dict[str, Any] = field(default_factory=dict)
    actual_outcome: Dict[str, Any] = field(default_factory=dict)
    
    # Proof
    evidence_hash: str = ""
    signature: str = ""
    nonce: str = ""
    
    # Metadata
    creator: str = ""
    chain_of_custody: List[Dict[str, Any]] = field(default_factory=list)
    verification_status: str = "pending"  # pending, verified, rejected
    verification_timestamp: Optional[datetime] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "version": self.version,
            "packet_type": self.packet_type,
            "timestamp": self.timestamp.isoformat(),
            "asset_id": self.asset_id,
            "intervention_type": self.intervention_type,
            "before_state": self.before_state,
            "after_state": self.after_state,
            "predicted_outcome": self.predicted_outcome,
            "actual_outcome": self.actual_outcome,
            "evidence_hash": self.evidence_hash,
            "signature": self.signature,
            "nonce": self.nonce,
            "creator": self.creator,
            "chain_of_custody": self.chain_of_custody,
            "verification_status": self.verification_status,
            "verification_timestamp": self.verification_timestamp.isoformat() if self.verification_timestamp else None,
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'BitNetProofPacket':
        """Create from dictionary."""
        return cls(
            version=data.get("version", "1.0"),
            packet_type=data.get("packet_type", "intervention_evidence"),
            timestamp=datetime.fromisoformat(data["timestamp"]),
            asset_id=data["asset_id"],
            intervention_type=data["intervention_type"],
            before_state=data.get("before_state", {}),
            after_state=data.get("after_state", {}),
            predicted_outcome=data.get("predicted_outcome", {}),
            actual_outcome=data.get("actual_outcome", {}),
            evidence_hash=data.get("evidence_hash", ""),
            signature=data.get("signature", ""),
            nonce=data.get("nonce", ""),
            creator=data.get("creator", ""),
            chain_of_custody=data.get("chain_of_custody", []),
            verification_status=data.get("verification_status", "pending"),
            verification_timestamp=datetime.fromisoformat(data["verification_timestamp"]) if data.get("verification_timestamp") else None,
        )


class BitNetProofGenerator:
    """
    Generate BitNet proof packets for interventions.
    
    Uses SHA-256 for evidence hashing and HMAC-SHA256 for signatures.
    """
    
    def __init__(self, secret_key: Optional[str] = None):
        """
        Initialize proof generator.
        
        Args:
            secret_key: Secret key for HMAC signatures. If None, generates one.
        """
        self.secret_key = secret_key or secrets.token_hex(32)
    
    def _hash_evidence(self, evidence: Dict[str, Any]) -> str:
        """
        Generate SHA-256 hash of evidence.
        
        Args:
            evidence: Evidence dictionary
            
        Returns:
            Hex-encoded SHA-256 hash
        """
        # Sort keys for deterministic hashing
        evidence_str = json.dumps(evidence, sort_keys=True)
        return hashlib.sha256(evidence_str.encode()).hexdigest()
    
    def _sign_hash(self, hash_value: str, nonce: str) -> str:
        """
        Generate HMAC-SHA256 signature.
        
        Args:
            hash_value: Hash to sign
            nonce: Nonce for signature
            
        Returns:
            Hex-encoded HMAC signature
        """
        message = f"{hash_value}:{nonce}".encode()
        return hmac.new(
            self.secret_key.encode(),
            message,
            hashlib.sha256
        ).hexdigest()
    
    def generate_proof_packet(
        self,
        asset_id: str,
        intervention_type: str,
        before_state: Dict[str, Any],
        after_state: Dict[str, Any],
        predicted_outcome: Dict[str, Any],
        actual_outcome: Dict[str, Any],
        creator: str = "catacomb_system"
    ) -> BitNetProofPacket:
        """
        Generate a complete BitNet proof packet.
        
        Args:
            asset_id: Asset identifier
            intervention_type: Type of intervention
            before_state: State before intervention
            after_state: State after intervention
            predicted_outcome: Predicted intervention outcome
            actual_outcome: Actual intervention outcome
            creator: Creator of the proof packet
            
        Returns:
            BitNetProofPacket with cryptographic proofs
        """
        # Generate nonce
        nonce = secrets.token_hex(16)
        
        # Create evidence
        evidence = {
            "asset_id": asset_id,
            "intervention_type": intervention_type,
            "before_state": before_state,
            "after_state": after_state,
            "predicted_outcome": predicted_outcome,
            "actual_outcome": actual_outcome,
            "timestamp": datetime.utcnow().isoformat(),
        }
        
        # Hash evidence
        evidence_hash = self._hash_evidence(evidence)
        
        # Sign hash
        signature = self._sign_hash(evidence_hash, nonce)
        
        # Create packet
        packet = BitNetProofPacket(
            asset_id=asset_id,
            intervention_type=intervention_type,
            before_state=before_state,
            after_state=after_state,
            predicted_outcome=predicted_outcome,
            actual_outcome=actual_outcome,
            evidence_hash=evidence_hash,
            signature=signature,
            nonce=nonce,
            creator=creator,
        )
        
        return packet


class BitNetProofVerifier:
    """
    Verify BitNet proof packets.
    
    Validates cryptographic proofs and evidence integrity.
    """
    
    def __init__(self, secret_key: str):
        """
        Initialize proof verifier.
        
        Args:
            secret_key: Secret key for signature verification
        """
        self.secret_key = secret_key
    
    def _hash_evidence(self, evidence: Dict[str, Any]) -> str:
        """Generate SHA-256 hash of evidence."""
        evidence_str = json.dumps(evidence, sort_keys=True)
        return hashlib.sha256(evidence_str.encode()).hexdigest()
    
    def _verify_signature(self, hash_value: str, nonce: str, signature: str) -> bool:
        """
        Verify HMAC-SHA256 signature.
        
        Args:
            hash_value: Hash that was signed
            nonce: Nonce used in signature
            signature: Signature to verify
            
        Returns:
            True if signature is valid
        """
        message = f"{hash_value}:{nonce}".encode()
        expected_signature = hmac.new(
            self.secret_key.encode(),
            message,
            hashlib.sha256
        ).hexdigest()
        
        return secrets.compare_digest(expected_signature, signature)
    
    def verify_packet(self, packet: BitNetProofPacket) -> Tuple[bool, str]:
        """
        Verify a BitNet proof packet.
        
        Args:
            packet: Packet to verify
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        # Reconstruct evidence
        evidence = {
            "asset_id": packet.asset_id,
            "intervention_type": packet.intervention_type,
            "before_state": packet.before_state,
            "after_state": packet.after_state,
            "predicted_outcome": packet.predicted_outcome,
            "actual_outcome": packet.actual_outcome,
            "timestamp": packet.timestamp.isoformat(),
        }
        
        # Verify evidence hash
        computed_hash = self._hash_evidence(evidence)
        if computed_hash != packet.evidence_hash:
            return False, "Evidence hash mismatch"
        
        # Verify signature
        if not self._verify_signature(packet.evidence_hash, packet.nonce, packet.signature):
            return False, "Signature verification failed"
        
        return True, "Proof verified"
    
    def verify_and_update_packet(self, packet: BitNetProofPacket) -> BitNetProofPacket:
        """
        Verify packet and update verification status.
        
        Args:
            packet: Packet to verify
            
        Returns:
            Updated packet with verification status
        """
        is_valid, message = self.verify_packet(packet)
        
        packet.verification_status = "verified" if is_valid else "rejected"
        packet.verification_timestamp = datetime.utcnow()
        
        # Add to chain of custody
        packet.chain_of_custody.append({
            "timestamp": datetime.utcnow().isoformat(),
            "action": "verification",
            "result": packet.verification_status,
            "message": message,
        })
        
        return packet


class BitNetProofLedger:
    """
    Ledger for storing and retrieving BitNet proof packets.
    
    Integrates with Outcome Ledger for proof storage.
    """
    
    def __init__(self, db_path: str = "bitnet_proofs.db"):
        """
        Initialize proof ledger.
        
        Args:
            db_path: Path to SQLite database
        """
        self.db_path = db_path
        self._init_db()
    
    def _init_db(self):
        """Initialize database schema."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS proof_packets (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                packet_id TEXT UNIQUE NOT NULL,
                packet_data TEXT NOT NULL,
                asset_id TEXT NOT NULL,
                intervention_type TEXT NOT NULL,
                verification_status TEXT NOT NULL,
                created_at TEXT NOT NULL,
                verified_at TEXT
            )
        """)
        
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_asset_id ON proof_packets(asset_id)
        """)
        
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_verification_status ON proof_packets(verification_status)
        """)
        
        conn.commit()
        conn.close()
    
    def store_packet(self, packet: BitNetProofPacket) -> str:
        """
        Store a proof packet in the ledger.
        
        Args:
            packet: Packet to store
            
        Returns:
            Packet ID
        """
        # Generate packet ID
        packet_id = hashlib.sha256(
            f"{packet.asset_id}:{packet.intervention_type}:{packet.timestamp.isoformat()}".encode()
        ).hexdigest()
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT OR REPLACE INTO proof_packets
            (packet_id, packet_data, asset_id, intervention_type, verification_status, created_at, verified_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            packet_id,
            json.dumps(packet.to_dict()),
            packet.asset_id,
            packet.intervention_type,
            packet.verification_status,
            packet.timestamp.isoformat(),
            packet.verification_timestamp.isoformat() if packet.verification_timestamp else None,
        ))
        
        conn.commit()
        conn.close()
        
        return packet_id
    
    def get_packet(self, packet_id: str) -> Optional[BitNetProofPacket]:
        """
        Retrieve a proof packet by ID.
        
        Args:
            packet_id: Packet ID
            
        Returns:
            BitNetProofPacket or None
        """
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT packet_data FROM proof_packets WHERE packet_id = ?
        """, (packet_id,))
        
        row = cursor.fetchone()
        conn.close()
        
        if not row:
            return None
        
        return BitNetProofPacket.from_dict(json.loads(row["packet_data"]))
    
    def get_packets_by_asset(self, asset_id: str) -> List[BitNetProofPacket]:
        """
        Retrieve all proof packets for an asset.
        
        Args:
            asset_id: Asset ID
            
        Returns:
            List of BitNetProofPacket
        """
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT packet_data FROM proof_packets WHERE asset_id = ? ORDER BY created_at DESC
        """, (asset_id,))
        
        rows = cursor.fetchall()
        conn.close()
        
        return [BitNetProofPacket.from_dict(json.loads(row["packet_data"])) for row in rows]
    
    def get_verified_packets(self, limit: int = 100) -> List[BitNetProofPacket]:
        """
        Retrieve verified proof packets.
        
        Args:
            limit: Maximum number of packets to retrieve
            
        Returns:
            List of verified BitNetProofPacket
        """
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT packet_data FROM proof_packets 
            WHERE verification_status = 'verified'
            ORDER BY created_at DESC
            LIMIT ?
        """, (limit,))
        
        rows = cursor.fetchall()
        conn.close()
        
        return [BitNetProofPacket.from_dict(json.loads(row["packet_data"])) for row in rows]


class BitNetSecurityLayer:
    """
    High-level security layer for BitNet proof operations.
    
    Combines proof generation, verification, and ledger storage.
    """
    
    def __init__(self, secret_key: Optional[str] = None, ledger_db: str = "bitnet_proofs.db"):
        """
        Initialize security layer.
        
        Args:
            secret_key: Secret key for cryptographic operations
            ledger_db: Path to proof ledger database
        """
        self.secret_key = secret_key or secrets.token_hex(32)
        self.generator = BitNetProofGenerator(self.secret_key)
        self.verifier = BitNetProofVerifier(self.secret_key)
        self.ledger = BitNetProofLedger(ledger_db)
    
    def create_and_store_proof(
        self,
        asset_id: str,
        intervention_type: str,
        before_state: Dict[str, Any],
        after_state: Dict[str, Any],
        predicted_outcome: Dict[str, Any],
        actual_outcome: Dict[str, Any],
        creator: str = "catacomb_system"
    ) -> Tuple[str, BitNetProofPacket]:
        """
        Generate, verify, and store a proof packet.
        
        Args:
            asset_id: Asset identifier
            intervention_type: Type of intervention
            before_state: State before intervention
            after_state: State after intervention
            predicted_outcome: Predicted intervention outcome
            actual_outcome: Actual intervention outcome
            creator: Creator of the proof packet
            
        Returns:
            Tuple of (packet_id, verified_packet)
        """
        # Generate proof packet
        packet = self.generator.generate_proof_packet(
            asset_id=asset_id,
            intervention_type=intervention_type,
            before_state=before_state,
            after_state=after_state,
            predicted_outcome=predicted_outcome,
            actual_outcome=actual_outcome,
            creator=creator,
        )
        
        # Verify packet
        verified_packet = self.verifier.verify_and_update_packet(packet)
        
        # Store in ledger
        packet_id = self.ledger.store_packet(verified_packet)
        
        return packet_id, verified_packet
    
    def verify_stored_proof(self, packet_id: str) -> Tuple[bool, str, Optional[BitNetProofPacket]]:
        """
        Verify a stored proof packet.
        
        Args:
            packet_id: Packet ID to verify
            
        Returns:
            Tuple of (is_valid, message, packet)
        """
        packet = self.ledger.get_packet(packet_id)
        if not packet:
            return False, "Packet not found", None
        
        is_valid, message = self.verifier.verify_packet(packet)
        
        # Update verification status
        packet = self.verifier.verify_and_update_packet(packet)
        self.ledger.store_packet(packet)
        
        return is_valid, message, packet
