"""Base agent class with deterministic output requirements."""
import hashlib
import json
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Dict


@dataclass
class AgentOutput:
    """Deterministic agent output."""
    score: float  # 0-100
    evidence: Dict[str, Any]  # exact fields used
    confidence: float  # 0-1
    hash: str  # sha256(input + output)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "score": self.score,
            "evidence": self.evidence,
            "confidence": self.confidence,
            "hash": self.hash
        }


class BaseAgent(ABC):
    """Base class for all deterministic agents."""
    
    def __init__(self, name: str):
        self.name = name
    
    @abstractmethod
    def analyze(self, repo_data: Dict[str, Any]) -> AgentOutput:
        """Analyze repo and return deterministic output."""
        pass
    
    def _compute_hash(self, input_data: Dict[str, Any], output_data: Dict[str, Any]) -> str:
        """Compute sha256 hash of input + output."""
        combined = json.dumps({
            "input": input_data,
            "output": output_data
        }, sort_keys=True)
        return hashlib.sha256(combined.encode()).hexdigest()
    
    def execute(self, repo_data: Dict[str, Any]) -> AgentOutput:
        """Execute agent with deterministic hash computation."""
        output = self.analyze(repo_data)
        
        # Recompute hash with actual output
        output.hash = self._compute_hash(repo_data, {
            "score": output.score,
            "evidence": output.evidence,
            "confidence": output.confidence
        })
        
        return output
