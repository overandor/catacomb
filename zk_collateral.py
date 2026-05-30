#!/usr/bin/env python3
"""
ZK Collateral System - Zero-Knowledge proofs for inference collateralization.

This module provides:
- ZK proof generation for inference claims
- Collateral tracking and management
- Liquidity memory layer for collateral states
- Integration with Ollama inference
- Custom SDK for ZK collateral inference
"""

import hashlib
import json
import sqlite3
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field
from datetime import datetime
import secrets
from decimal import Decimal
from proof_of_inference import ProofOfInference, OllamaInferenceClient


@dataclass
class ZKProof:
    """
    Zero-Knowledge proof for inference.
    
    Structure:
    - Public inputs: model hash, prompt hash, output hash
    - Private inputs: actual model, actual prompt, actual output
    - Proof: ZK-SNARK proof (simplified for demo)
    - Verification key: Public verification key
    """
    proof_id: str
    public_inputs: Dict[str, str]
    proof: str
    verification_key: str
    timestamp: datetime = field(default_factory=datetime.now)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "proof_id": self.proof_id,
            "public_inputs": self.public_inputs,
            "proof": self.proof,
            "verification_key": self.verification_key,
            "timestamp": self.timestamp.isoformat(),
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ZKProof':
        """Create from dictionary."""
        return cls(
            proof_id=data["proof_id"],
            public_inputs=data["public_inputs"],
            proof=data["proof"],
            verification_key=data["verification_key"],
            timestamp=datetime.fromisoformat(data["timestamp"]),
        )


@dataclass
class CollateralPosition:
    """
    Collateral position for ZK proof.
    
    Tracks:
    - Collateral amount and token
    - Proof ID being collateralized
    - Liquidity pool participation
    - Unlock conditions
    """
    position_id: str
    proof_id: str
    collateral_amount: Decimal
    collateral_token: str
    liquidity_pool_id: str
    creator: str
    created_at: datetime = field(default_factory=datetime.now)
    unlocked_at: Optional[datetime] = None
    unlock_conditions: Dict[str, Any] = field(default_factory=dict)
    status: str = "locked"  # locked, unlocked, liquidated
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "position_id": self.position_id,
            "proof_id": self.proof_id,
            "collateral_amount": str(self.collateral_amount),
            "collateral_token": self.collateral_token,
            "liquidity_pool_id": self.liquidity_pool_id,
            "creator": self.creator,
            "created_at": self.created_at.isoformat(),
            "unlocked_at": self.unlocked_at.isoformat() if self.unlocked_at else None,
            "unlock_conditions": self.unlock_conditions,
            "status": self.status,
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'CollateralPosition':
        """Create from dictionary."""
        return cls(
            position_id=data["position_id"],
            proof_id=data["proof_id"],
            collateral_amount=Decimal(data["collateral_amount"]),
            collateral_token=data["collateral_token"],
            liquidity_pool_id=data["liquidity_pool_id"],
            creator=data["creator"],
            created_at=datetime.fromisoformat(data["created_at"]),
            unlocked_at=datetime.fromisoformat(data["unlocked_at"]) if data.get("unlocked_at") else None,
            unlock_conditions=data.get("unlock_conditions", {}),
            status=data.get("status", "locked"),
        )


@dataclass
class LiquidityPool:
    """
    Liquidity pool for collateral.
    
    Manages:
    - Total liquidity
    - Collateral positions
    - Pool utilization
    - Reward distribution
    """
    pool_id: str
    collateral_token: str
    total_liquidity: Decimal
    locked_collateral: Decimal
    available_liquidity: Decimal
    reward_rate: Decimal
    positions: List[str] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)
    
    @property
    def utilization_rate(self) -> Decimal:
        """Calculate pool utilization rate."""
        if self.total_liquidity == 0:
            return Decimal("0")
        return self.locked_collateral / self.total_liquidity
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "pool_id": self.pool_id,
            "collateral_token": self.collateral_token,
            "total_liquidity": str(self.total_liquidity),
            "locked_collateral": str(self.locked_collateral),
            "available_liquidity": str(self.available_liquidity),
            "reward_rate": str(self.reward_rate),
            "utilization_rate": str(self.utilization_rate),
            "positions": self.positions,
            "created_at": self.created_at.isoformat(),
        }


class ZKProofGenerator:
    """
    Generate Zero-Knowledge proofs for inference.
    
    Simplified ZK-SNARK implementation for demo.
    In production, use circom, snarkjs, or similar.
    """
    
    def __init__(self):
        self.verification_key = secrets.token_hex(32)
    
    def _hash_input(self, data: str) -> str:
        """Hash input for ZK proof."""
        return hashlib.sha256(data.encode()).hexdigest()
    
    def generate_proof(
        self,
        model: str,
        prompt: str,
        output: str,
        private_inputs: Optional[Dict[str, Any]] = None
    ) -> ZKProof:
        """
        Generate ZK proof for inference.
        
        Args:
            model: Model name/identifier
            prompt: Input prompt
            output: Model output
            private_inputs: Private inputs (not revealed in proof)
            
        Returns:
            ZKProof object
        """
        # Public inputs (revealed)
        public_inputs = {
            "model_hash": self._hash_input(model),
            "prompt_hash": self._hash_input(prompt),
            "output_hash": self._hash_input(output),
        }
        
        # Generate proof (simplified - in production use actual ZK-SNARK)
        proof_data = {
            "public_inputs": public_inputs,
            "private_inputs": private_inputs or {},
            "nonce": secrets.token_hex(16),
        }
        proof = self._hash_input(json.dumps(proof_data, sort_keys=True))
        
        proof_id = hashlib.sha256(
            f"{public_inputs['model_hash']}:{public_inputs['prompt_hash']}:{proof}".encode()
        ).hexdigest()
        
        return ZKProof(
            proof_id=proof_id,
            public_inputs=public_inputs,
            proof=proof,
            verification_key=self.verification_key,
        )
    
    def verify_proof(self, proof: ZKProof) -> bool:
        """
        Verify ZK proof.
        
        Args:
            proof: Proof to verify
            
        Returns:
            True if proof is valid
        """
        # Simplified verification - in production use actual ZK verification
        # Check that proof matches verification key
        expected_proof = self._hash_input(
            json.dumps({
                "public_inputs": proof.public_inputs,
                "nonce": proof.proof[:32],  # Extract nonce from proof
            }, sort_keys=True)
        )
        
        return proof.verification_key == self.verification_key


class LiquidityMemoryLayer:
    """
    Memory layer for collateral tracking.
    
    Tracks:
    - Collateral positions
    - Liquidity pools
    - Historical states
    - Unlock conditions
    """
    
    def __init__(self, db_path: str = "liquidity_memory.db"):
        """
        Initialize liquidity memory layer.
        
        Args:
            db_path: Path to SQLite database
        """
        self.db_path = db_path
        self._init_db()
    
    def _init_db(self):
        """Initialize database schema."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Collateral positions table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS collateral_positions (
                position_id TEXT PRIMARY KEY,
                proof_id TEXT NOT NULL,
                collateral_amount TEXT NOT NULL,
                collateral_token TEXT NOT NULL,
                liquidity_pool_id TEXT NOT NULL,
                creator TEXT NOT NULL,
                created_at TEXT NOT NULL,
                unlocked_at TEXT,
                unlock_conditions TEXT,
                status TEXT NOT NULL
            )
        """)
        
        # Liquidity pools table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS liquidity_pools (
                pool_id TEXT PRIMARY KEY,
                collateral_token TEXT NOT NULL,
                total_liquidity TEXT NOT NULL,
                locked_collateral TEXT NOT NULL,
                available_liquidity TEXT NOT NULL,
                reward_rate TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
        """)
        
        # Historical states table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS historical_states (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                pool_id TEXT NOT NULL,
                state_data TEXT NOT NULL,
                timestamp TEXT NOT NULL
            )
        """)
        
        # Indexes
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_proof_id ON collateral_positions(proof_id)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_pool_id ON collateral_positions(liquidity_pool_id)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_status ON collateral_positions(status)")
        
        conn.commit()
        conn.close()
    
    def create_pool(
        self,
        pool_id: str,
        collateral_token: str,
        initial_liquidity: Decimal,
        reward_rate: Decimal = Decimal("0.05")
    ) -> LiquidityPool:
        """
        Create a new liquidity pool.
        
        Args:
            pool_id: Pool identifier
            collateral_token: Token used for collateral
            initial_liquidity: Initial liquidity amount
            reward_rate: Annual reward rate (e.g., 0.05 for 5%)
            
        Returns:
            LiquidityPool object
        """
        pool = LiquidityPool(
            pool_id=pool_id,
            collateral_token=collateral_token,
            total_liquidity=initial_liquidity,
            locked_collateral=Decimal("0"),
            available_liquidity=initial_liquidity,
            reward_rate=reward_rate,
        )
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO liquidity_pools
            (pool_id, collateral_token, total_liquidity, locked_collateral, available_liquidity, reward_rate, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            pool.pool_id,
            pool.collateral_token,
            str(pool.total_liquidity),
            str(pool.locked_collateral),
            str(pool.available_liquidity),
            str(pool.reward_rate),
            pool.created_at.isoformat(),
        ))
        
        conn.commit()
        conn.close()
        
        return pool
    
    def get_pool(self, pool_id: str) -> Optional[LiquidityPool]:
        """Get a liquidity pool by ID."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT * FROM liquidity_pools WHERE pool_id = ?
        """, (pool_id,))
        
        row = cursor.fetchone()
        conn.close()
        
        if not row:
            return None
        
        # Get positions
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT position_id FROM collateral_positions WHERE liquidity_pool_id = ? AND status = 'locked'
        """, (pool_id,))
        positions = [r[0] for r in cursor.fetchall()]
        conn.close()
        
        return LiquidityPool(
            pool_id=row["pool_id"],
            collateral_token=row["collateral_token"],
            total_liquidity=Decimal(row["total_liquidity"]),
            locked_collateral=Decimal(row["locked_collateral"]),
            available_liquidity=Decimal(row["available_liquidity"]),
            reward_rate=Decimal(row["reward_rate"]),
            positions=positions,
            created_at=datetime.fromisoformat(row["created_at"]),
        )
    
    def lock_collateral(
        self,
        proof_id: str,
        collateral_amount: Decimal,
        collateral_token: str,
        pool_id: str,
        creator: str,
        unlock_conditions: Optional[Dict[str, Any]] = None
    ) -> CollateralPosition:
        """
        Lock collateral for a proof.
        
        Args:
            proof_id: Proof ID to collateralize
            collateral_amount: Amount to lock
            collateral_token: Token to use
            pool_id: Liquidity pool ID
            creator: Creator of the position
            unlock_conditions: Conditions for unlocking
            
        Returns:
            CollateralPosition object
        """
        # Generate position ID
        position_id = hashlib.sha256(
            f"{proof_id}:{creator}:{datetime.utcnow().isoformat()}".encode()
        ).hexdigest()
        
        # Create position
        position = CollateralPosition(
            position_id=position_id,
            proof_id=proof_id,
            collateral_amount=collateral_amount,
            collateral_token=collateral_token,
            liquidity_pool_id=pool_id,
            creator=creator,
            unlock_conditions=unlock_conditions or {},
        )
        
        # Update pool
        pool = self.get_pool(pool_id)
        if not pool:
            raise ValueError(f"Pool {pool_id} not found")
        
        if pool.available_liquidity < collateral_amount:
            raise ValueError("Insufficient liquidity in pool")
        
        pool.locked_collateral += collateral_amount
        pool.available_liquidity -= collateral_amount
        pool.positions.append(position_id)
        
        # Store position
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO collateral_positions
            (position_id, proof_id, collateral_amount, collateral_token, liquidity_pool_id, creator, created_at, unlock_conditions, status)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            position.position_id,
            position.proof_id,
            str(position.collateral_amount),
            position.collateral_token,
            position.liquidity_pool_id,
            position.creator,
            position.created_at.isoformat(),
            json.dumps(position.unlock_conditions),
            position.status,
        ))
        
        # Update pool
        cursor.execute("""
            UPDATE liquidity_pools
            SET locked_collateral = ?, available_liquidity = ?
            WHERE pool_id = ?
        """, (str(pool.locked_collateral), str(pool.available_liquidity), pool_id))
        
        # Save historical state
        cursor.execute("""
            INSERT INTO historical_states (pool_id, state_data, timestamp)
            VALUES (?, ?, ?)
        """, (pool_id, json.dumps(pool.to_dict()), datetime.utcnow().isoformat()))
        
        conn.commit()
        conn.close()
        
        return position
    
    def unlock_collateral(self, position_id: str) -> CollateralPosition:
        """
        Unlock collateral.
        
        Args:
            position_id: Position ID to unlock
            
        Returns:
            Updated CollateralPosition
        """
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT * FROM collateral_positions WHERE position_id = ?
        """, (position_id,))
        
        row = cursor.fetchone()
        if not row:
            conn.close()
            raise ValueError(f"Position {position_id} not found")
        
        position = CollateralPosition.from_dict(dict(row))
        
        if position.status != "locked":
            conn.close()
            raise ValueError(f"Position {position_id} is not locked")
        
        # Update position
        position.status = "unlocked"
        position.unlocked_at = datetime.utcnow()
        
        # Update pool
        pool = self.get_pool(position.liquidity_pool_id)
        pool.locked_collateral -= position.collateral_amount
        pool.available_liquidity += position.collateral_amount
        pool.positions.remove(position_id)
        
        # Update database
        cursor.execute("""
            UPDATE collateral_positions
            SET status = ?, unlocked_at = ?
            WHERE position_id = ?
        """, (position.status, position.unlocked_at.isoformat(), position_id))
        
        cursor.execute("""
            UPDATE liquidity_pools
            SET locked_collateral = ?, available_liquidity = ?
            WHERE pool_id = ?
        """, (str(pool.locked_collateral), str(pool.available_liquidity), position.liquidity_pool_id))
        
        # Save historical state
        cursor.execute("""
            INSERT INTO historical_states (pool_id, state_data, timestamp)
            VALUES (?, ?, ?)
        """, (position.liquidity_pool_id, json.dumps(pool.to_dict()), datetime.utcnow().isoformat()))
        
        conn.commit()
        conn.close()
        
        return position
    
    def get_position(self, position_id: str) -> Optional[CollateralPosition]:
        """Get a collateral position by ID."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT * FROM collateral_positions WHERE position_id = ?
        """, (position_id,))
        
        row = cursor.fetchone()
        conn.close()
        
        if not row:
            return None
        
        return CollateralPosition.from_dict(dict(row))
    
    def get_positions_by_proof(self, proof_id: str) -> List[CollateralPosition]:
        """Get all positions for a proof."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT * FROM collateral_positions WHERE proof_id = ?
        """, (proof_id,))
        
        rows = cursor.fetchall()
        conn.close()
        
        return [CollateralPosition.from_dict(dict(row)) for row in rows]


class ZKCollateralInferenceSDK:
    """
    Custom SDK for ZK collateral inference with Ollama.
    
    Combines:
    - Ollama inference
    - ZK proof generation
    - Collateral locking
    - Liquidity management
    """
    
    def __init__(
        self,
        ollama_base_url: str = "http://localhost:11434",
        liquidity_db: str = "liquidity_memory.db"
    ):
        """
        Initialize SDK.
        
        Args:
            ollama_base_url: Ollama API base URL
            liquidity_db: Path to liquidity memory database
        """
        self.ollama_client = OllamaInferenceClient(ollama_base_url)
        self.proof_generator = ZKProofGenerator()
        self.liquidity_memory = LiquidityMemoryLayer(liquidity_db)
        self.proof_sdk = ProofOfInference()
    
    def generate_inference_with_zk_proof(
        self,
        model: str,
        prompt: str,
        store_in_ledger: bool = True
    ) -> Tuple[str, ZKProof]:
        """
        Generate inference with ZK proof.
        
        Args:
            model: Ollama model name
            prompt: Input prompt
            store_in_ledger: Whether to store in outcome ledger
            
        Returns:
            Tuple of (response, zk_proof)
        """
        # Generate inference
        response = self.ollama_client.generate(model, prompt)
        
        # Generate ZK proof
        zk_proof = self.proof_generator.generate_proof(
            model=model,
            prompt=prompt,
            output=response,
        )
        
        # Generate BitNet proof
        bitnet_proof = self.proof_sdk.generate_proof(
            model=model,
            prompt=prompt,
            response=response,
            store_in_ledger=store_in_ledger
        )
        
        return response, zk_proof
    
    def collateralize_inference(
        self,
        model: str,
        prompt: str,
        collateral_amount: Decimal,
        collateral_token: str,
        pool_id: str,
        creator: str,
        unlock_conditions: Optional[Dict[str, Any]] = None
    ) -> Tuple[str, ZKProof, CollateralPosition]:
        """
        Generate inference and collateralize with ZK proof.
        
        Args:
            model: Ollama model name
            prompt: Input prompt
            collateral_amount: Amount to collateralize
            collateral_token: Token to use
            pool_id: Liquidity pool ID
            creator: Creator of the position
            unlock_conditions: Conditions for unlocking
            
        Returns:
            Tuple of (response, zk_proof, collateral_position)
        """
        # Generate inference with ZK proof
        response, zk_proof = self.generate_inference_with_zk_proof(model, prompt)
        
        # Lock collateral
        position = self.liquidity_memory.lock_collateral(
            proof_id=zk_proof.proof_id,
            collateral_amount=collateral_amount,
            collateral_token=collateral_token,
            pool_id=pool_id,
            creator=creator,
            unlock_conditions=unlock_conditions,
        )
        
        return response, zk_proof, position
    
    def verify_and_unlock(
        self,
        position_id: str,
        model: str,
        prompt: str,
        expected_output: str
    ) -> Tuple[bool, str, CollateralPosition]:
        """
        Verify proof and unlock collateral.
        
        Args:
            position_id: Position ID to unlock
            model: Model used
            prompt: Prompt used
            expected_output: Expected output
            
        Returns:
            Tuple of (is_valid, message, position)
        """
        # Get position
        position = self.liquidity_memory.get_position(position_id)
        if not position:
            return False, "Position not found", None
        
        # Get proof
        zk_proof = self.proof_generator.generate_proof(
            model=model,
            prompt=prompt,
            output=expected_output,
        )
        
        # Verify proof matches
        if zk_proof.proof_id != position.proof_id:
            return False, "Proof ID mismatch", position
        
        # Verify proof
        is_valid = self.proof_generator.verify_proof(zk_proof)
        
        if is_valid:
            # Unlock collateral
            position = self.liquidity_memory.unlock_collateral(position_id)
            return True, "Collateral unlocked", position
        else:
            return False, "Proof verification failed", position
    
    def get_pool_status(self, pool_id: str) -> Optional[LiquidityPool]:
        """Get liquidity pool status."""
        return self.liquidity_memory.get_pool(pool_id)
    
    def get_position_status(self, position_id: str) -> Optional[CollateralPosition]:
        """Get collateral position status."""
        return self.liquidity_memory.get_position(position_id)
