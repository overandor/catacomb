#!/usr/bin/env python3
"""
Proof of Inference SDK — Verifiable LLM Inference for Ollama

Generates cryptographically verifiable proofs that a specific inference
was performed at a specific time with specific inputs and outputs.

Usage:
    from proof_of_inference import ProofOfInference
    
    poi = ProofOfInference()
    
    # Generate proof after inference
    proof = poi.generate_proof(
        model="llama3.1",
        prompt="Analyze this code",
        response="The code is...",
        metadata={"temperature": 0.7, "context": "code_review"}
    )
    
    # Verify proof
    is_valid = poi.verify_proof(proof)
    
    # Store in ledger
    poi.store_proof(proof, ledger)

Proof Structure:
{
    "proof_id": "uuid",
    "model": "llama3.1",
    "timestamp": "2024-01-15T10:30:00Z",
    "input_hash": "sha256(prompt)",
    "output_hash": "sha256(response)",
    "model_hash": "sha256(model_name + version)",
    "parameters_hash": "sha256(json(metadata))",
    "composite_hash": "sha256(input + output + model + params + timestamp)",
    "signature": "hmac(composite_hash, secret)",
    "verification_url": "/api/v1/proof/{proof_id}/verify"
}
"""

import hashlib
import hmac
import json
import uuid
import time
from datetime import datetime
from typing import Dict, Any, Optional
import os


class ProofOfInference:
    """
    Generates and verifies cryptographic proofs of LLM inferences.
    
    Each proof is a self-contained evidence packet that can be:
    - Verified independently (given the proof and secret)
    - Stored in the OutcomeLedger
    - Submitted to blockchain for permanent attestation
    - Used in legal/audit contexts to prove inference happened
    """
    
    def __init__(self, secret_key: str = None):
        """
        Initialize the Proof of Inference system.
        
        Args:
            secret_key: HMAC secret for signing proofs. If None, uses env var.
        """
        self.secret_key = (secret_key or os.environ.get('POI_SECRET', 'catacomb-proof-default-key')
                          ).encode('utf-8')
        self.version = "1.0.0"
    
    def _hash(self, data: str) -> str:
        """Generate SHA-256 hash of data."""
        return hashlib.sha256(data.encode('utf-8')).hexdigest()
    
    def _sign(self, data: str) -> str:
        """Generate HMAC-SHA256 signature."""
        return hmac.new(
            self.secret_key,
            data.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()
    
    def generate_proof(
        self,
        model: str,
        prompt: str,
        response: str,
        metadata: Dict[str, Any] = None,
        latency_ms: int = None
    ) -> Dict[str, Any]:
        """
        Generate a verifiable proof of inference.
        
        Args:
            model: Model name (e.g., "llama3.1", "mistral", "codellama")
            prompt: The input prompt
            response: The model's response
            metadata: Inference parameters (temperature, top_p, etc.)
            latency_ms: Inference latency in milliseconds
            
        Returns:
            Proof dictionary with all hashes and signature
        """
        timestamp = datetime.utcnow().isoformat()
        proof_id = str(uuid.uuid4())
        
        # Hash individual components
        input_hash = self._hash(prompt)
        output_hash = self._hash(response)
        model_hash = self._hash(f"{model}:{self.version}")
        params_hash = self._hash(json.dumps(metadata or {}, sort_keys=True))
        
        # Composite hash binds everything together
        composite = f"{input_hash}:{output_hash}:{model_hash}:{params_hash}:{timestamp}:{proof_id}"
        composite_hash = self._hash(composite)
        
        # Sign the composite hash
        signature = self._sign(composite_hash)
        
        return {
            "proof_id": proof_id,
            "version": self.version,
            "model": model,
            "timestamp": timestamp,
            "unix_timestamp": int(time.time()),
            "input_hash": input_hash,
            "output_hash": output_hash,
            "model_hash": model_hash,
            "parameters_hash": params_hash,
            "composite_hash": composite_hash,
            "signature": signature,
            "latency_ms": latency_ms,
            "metadata": metadata or {},
            "verification": {
                "algorithm": "sha256+hmac-sha256",
                "verified": False,
                "verification_timestamp": None
            }
        }
    
    def verify_proof(self, proof: Dict[str, Any]) -> Dict[str, Any]:
        """
        Verify a proof of inference.
        
        Args:
            proof: Proof dictionary from generate_proof()
            
        Returns:
            Verification result with boolean and details
        """
        try:
            # Reconstruct composite hash
            composite = (
                f"{proof['input_hash']}:{proof['output_hash']}:{proof['model_hash']}:"
                f"{proof['parameters_hash']}:{proof['timestamp']}:{proof['proof_id']}"
            )
            expected_composite = self._hash(composite)
            
            # Verify composite hash
            if expected_composite != proof['composite_hash']:
                return {
                    "valid": False,
                    "error": "composite_hash_mismatch",
                    "message": "The composite hash does not match recomputed value"
                }
            
            # Verify signature
            expected_signature = self._sign(proof['composite_hash'])
            if not hmac.compare_digest(expected_signature, proof['signature']):
                return {
                    "valid": False,
                    "error": "signature_mismatch",
                    "message": "The HMAC signature is invalid"
                }
            
            # All checks passed
            result = {
                "valid": True,
                "error": None,
                "message": "Proof is cryptographically valid",
                "proof_id": proof['proof_id'],
                "model": proof['model'],
                "timestamp": proof['timestamp'],
                "age_seconds": int(time.time()) - proof.get('unix_timestamp', 0),
                "verification_timestamp": datetime.utcnow().isoformat()
            }
            
            # Update proof with verification
            proof['verification']['verified'] = True
            proof['verification']['verification_timestamp'] = result['verification_timestamp']
            
            return result
            
        except Exception as e:
            return {
                "valid": False,
                "error": "verification_exception",
                "message": str(e)
            }
    
    def store_proof(self, proof: Dict[str, Any], ledger) -> str:
        """
        Store proof in the OutcomeLedger.
        
        Args:
            proof: Proof dictionary
            ledger: OutcomeLedger instance
            
        Returns:
            Record ID in ledger
        """
        record = {
            "asset_id": f"inference:{proof['proof_id']}",
            "asset_type": "llm_inference",
            "asset_name": f"{proof['model']} inference",
            "developer_id": "system:ollama",
            "intervention_type": "inference",
            "intervention_description": f"LLM inference via {proof['model']}",
            "before_state": {"prompt_hash": proof['input_hash']},
            "after_state": {"response_hash": proof['output_hash']},
            "outcome_metrics": {
                "latency_ms": proof.get('latency_ms'),
                "proof_id": proof['proof_id'],
                "model": proof['model']
            },
            "verification_link": f"/api/v1/proof/{proof['proof_id']}/verify",
            "predicted_outcome": json.dumps(proof)
        }
        
        record_id = ledger.record_intervention(**record)
        return record_id
    
    def batch_generate_proofs(
        self,
        inferences: list
    ) -> list:
        """
        Generate proofs for multiple inferences.
        
        Args:
            inferences: List of dicts with model, prompt, response, metadata
            
        Returns:
            List of proof dictionaries
        """
        proofs = []
        for inf in inferences:
            proof = self.generate_proof(
                model=inf['model'],
                prompt=inf['prompt'],
                response=inf['response'],
                metadata=inf.get('metadata'),
                latency_ms=inf.get('latency_ms')
            )
            proofs.append(proof)
        return proofs
    
    def get_proof_by_id(self, proof_id: str, ledger) -> Optional[Dict]:
        """
        Retrieve a proof from the ledger by ID.
        
        Args:
            proof_id: UUID of the proof
            ledger: OutcomeLedger instance
            
        Returns:
            Proof dict or None
        """
        import sqlite3
        conn = sqlite3.connect(ledger.db_path)
        cursor = conn.cursor()
        
        cursor.execute(
            "SELECT predicted_outcome FROM interventions WHERE asset_id = ?",
            (f"inference:{proof_id}",)
        )
        row = cursor.fetchone()
        conn.close()
        
        if row and row[0]:
            try:
                return json.loads(row[0])
            except:
                pass
        return None


class OllamaInferenceClient:
    """
    Client for making verifiable inferences through Ollama.
    
    Wraps Ollama API calls with automatic proof generation.
    """
    
    def __init__(self, base_url: str = "http://localhost:11434", proof_sdk: ProofOfInference = None):
        self.base_url = base_url
        self.poi = proof_sdk or ProofOfInference()
    
    def generate(
        self,
        model: str,
        prompt: str,
        options: Dict[str, Any] = None,
        generate_proof: bool = True
    ) -> Dict[str, Any]:
        """
        Generate response through Ollama with optional proof.
        
        Args:
            model: Ollama model name
            prompt: Input prompt
            options: Generation options (temperature, etc.)
            generate_proof: Whether to generate a proof
            
        Returns:
            Response dict with proof if requested
        """
        import requests
        
        start_time = time.time()
        
        # Call Ollama API
        response = requests.post(
            f"{self.base_url}/api/generate",
            json={
                "model": model,
                "prompt": prompt,
                "stream": False,
                "options": options or {}
            }
        )
        response.raise_for_status()
        result = response.json()
        
        latency_ms = int((time.time() - start_time) * 1000)
        
        if generate_proof:
            proof = self.poi.generate_proof(
                model=model,
                prompt=prompt,
                response=result.get('response', ''),
                metadata={
                    "temperature": options.get('temperature', 0.7) if options else 0.7,
                    "top_p": options.get('top_p', 0.9) if options else 0.9,
                    "context": result.get('context', [])
                },
                latency_ms=latency_ms
            )
            result['proof'] = proof
        
        result['latency_ms'] = latency_ms
        return result
    
    def generate_verified(
        self,
        model: str,
        prompt: str,
        options: Dict[str, Any] = None,
        ledger = None
    ) -> Dict[str, Any]:
        """
        Generate response with proof and optionally store in ledger.
        
        Args:
            model: Ollama model name
            prompt: Input prompt
            options: Generation options
            ledger: Optional ledger to store proof
            
        Returns:
            Response with proof and storage confirmation
        """
        result = self.generate(model, prompt, options, generate_proof=True)
        
        if ledger and 'proof' in result:
            record_id = self.poi.store_proof(result['proof'], ledger)
            result['stored_record_id'] = record_id
        
        return result


# Singleton instance
_default_poi = None

def get_proof_sdk() -> ProofOfInference:
    """Get or create default ProofOfInference instance."""
    global _default_poi
    if _default_poi is None:
        _default_poi = ProofOfInference()
    return _default_poi
