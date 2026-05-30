#!/usr/bin/env python3
"""
Professional Scoring System - Multi-dimensional asset evaluation.

The evaluator should produce separate grades. Do not collapse everything into one number.

Structure:
- Production Grade: How real, maintainable, executable, and technically complete the asset is
- Commercial Grade: How useful, understandable, sellable, and productizable it is
- Collateral Grade: How recoverable, transferable, monitorable, and lender-readable it is
- Financeability Score: The final readiness score for capital recognition

Strong 100-point base rubric:
- Engineering substance: 20
- Execution proof: 15
- Originality and ownership: 15
- Security and license cleanliness: 15
- Market usefulness: 15
- Liquidation path: 10
- Documentation and packaging: 5
- Revenue/adoption proof: 5

This is better than a single "value score" - it distinguishes useful from financeable.
"""

from enum import Enum
from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass, field
from datetime import datetime
import json


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


@dataclass
class ProfessionalGrades:
    """
    Professional grades for software assets.
    
    Separate grades for different dimensions - do not collapse into one number.
    """
    production_grade: str  # A+ to F
    commercial_grade: str  # A+ to F
    collateral_grade: str  # A+ to F
    financeability_score: int  # 0-100
    
    # Component scores
    engineering_substance: float  # 0-20
    execution_proof: float  # 0-15
    originality_ownership: float  # 0-15
    security_license_cleanliness: float  # 0-15
    market_usefulness: float  # 0-15
    liquidation_path: float  # 0-10
    documentation_packaging: float  # 0-5
    revenue_adoption_proof: float  # 0-5
    
    # Metadata
    proof_level: ProofLevel = ProofLevel.CLAIMED
    evaluated_at: datetime = field(default_factory=datetime.now)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "production_grade": self.production_grade,
            "commercial_grade": self.commercial_grade,
            "collateral_grade": self.collateral_grade,
            "financeability_score": self.financeability_score,
            "engineering_substance": self.engineering_substance,
            "execution_proof": self.execution_proof,
            "originality_ownership": self.originality_ownership,
            "security_license_cleanliness": self.security_license_cleanliness,
            "market_usefulness": self.market_usefulness,
            "liquidation_path": self.liquidation_path,
            "documentation_packaging": self.documentation_packaging,
            "revenue_adoption_proof": self.revenue_adoption_proof,
            "proof_level": self.proof_level.value,
            "evaluated_at": self.evaluated_at.isoformat(),
        }


class ProfessionalScoringSystem:
    """
    Professional scoring system for software assets.
    
    Uses the 100-point base rubric to generate professional grades.
    """
    
    def __init__(self):
        self.rubric_weights = {
            "engineering_substance": 20,
            "execution_proof": 15,
            "originality_ownership": 15,
            "security_license_cleanliness": 15,
            "market_usefulness": 15,
            "liquidation_path": 10,
            "documentation_packaging": 5,
            "revenue_adoption_proof": 5,
        }
    
    def score_asset(self, committee_results: Dict[str, Any], asset_data: Dict[str, Any]) -> ProfessionalGrades:
        """
        Score an asset using the professional rubric.
        
        Args:
            committee_results: Results from the synthetic committee evaluation
            asset_data: Raw asset data
        
        Returns:
            ProfessionalGrades with all dimensions scored
        """
        # Extract component scores from committee results
        engineering_score = self._extract_score(committee_results, "engineering")
        execution_score = self._extract_score(committee_results, "execution")
        security_score = self._extract_score(committee_results, "security")
        license_score = self._extract_score(committee_results, "license_originality")
        market_score = self._extract_score(committee_results, "market")
        collateral_score = self._extract_score(committee_results, "collateral")
        liquidation_score = self._extract_score(committee_results, "liquidation")
        
        # Calculate rubric components
        engineering_substance = self._normalize_score(engineering_score, 20)
        execution_proof = self._normalize_score(execution_score, 15)
        originality_ownership = self._normalize_score(license_score, 15)
        security_license_cleanliness = self._normalize_score(
            (security_score + license_score) / 2, 15
        )
        market_usefulness = self._normalize_score(market_score, 15)
        liquidation_path = self._normalize_score(liquidation_score, 10)
        
        # Documentation and packaging
        documentation_score = asset_data.get("documentation_score", 0)
        documentation_packaging = self._normalize_score(documentation_score, 5)
        
        # Revenue and adoption proof
        revenue_evidence = asset_data.get("revenue_evidence", [])
        adoption_signals = asset_data.get("adoption_signals", {})
        revenue_adoption_proof = self._calculate_revenue_adoption_score(
            revenue_evidence, adoption_signals, 5
        )
        
        # Calculate financeability score
        financeability_score = (
            engineering_substance +
            execution_proof +
            originality_ownership +
            security_license_cleanliness +
            market_usefulness +
            liquidation_path +
            documentation_packaging +
            revenue_adoption_proof
        )
        
        # Determine grades
        production_grade = self._calculate_production_grade(
            engineering_substance, execution_proof, security_license_cleanliness
        )
        commercial_grade = self._calculate_commercial_grade(
            market_usefulness, documentation_packaging, revenue_adoption_proof
        )
        collateral_grade = self._calculate_collateral_grade(
            originality_ownership, liquidation_path, collateral_score
        )
        
        # Determine proof level
        proof_level = self._determine_proof_level(
            execution_score, security_score, financeability_score
        )
        
        return ProfessionalGrades(
            production_grade=production_grade,
            commercial_grade=commercial_grade,
            collateral_grade=collateral_grade,
            financeability_score=int(financeability_score),
            engineering_substance=engineering_substance,
            execution_proof=execution_proof,
            originality_ownership=originality_ownership,
            security_license_cleanliness=security_license_cleanliness,
            market_usefulness=market_usefulness,
            liquidation_path=liquidation_path,
            documentation_packaging=documentation_packaging,
            revenue_adoption_proof=revenue_adoption_proof,
            proof_level=proof_level,
        )
    
    def _extract_score(self, committee_results: Dict[str, Any], evaluator_name: str) -> float:
        """Extract score from committee results."""
        evaluator_results = committee_results.get("evaluator_results", {})
        evaluator_data = evaluator_results.get(evaluator_name, {})
        return evaluator_data.get("score", 0)
    
    def _normalize_score(self, score: float, max_points: float) -> float:
        """Normalize a 0-100 score to the rubric weight."""
        return (score / 100) * max_points
    
    def _calculate_revenue_adoption_score(
        self, revenue_evidence: List[Dict], adoption_signals: Dict, max_points: float
    ) -> float:
        """Calculate revenue/adoption proof score."""
        score = 0
        
        # Revenue evidence
        if revenue_evidence:
            score += min(max_points * 0.6, len(revenue_evidence) * 2)
        
        # Adoption signals
        stars = adoption_signals.get("stars", 0)
        forks = adoption_signals.get("forks", 0)
        downloads = adoption_signals.get("downloads", 0)
        
        if stars > 1000:
            score += max_points * 0.2
        elif stars > 100:
            score += max_points * 0.1
        
        if downloads > 10000:
            score += max_points * 0.2
        elif downloads > 1000:
            score += max_points * 0.1
        
        return min(score, max_points)
    
    def _calculate_production_grade(
        self, engineering: float, execution: float, security: float
    ) -> str:
        """Calculate production grade."""
        total = engineering + execution + security
        max_total = 20 + 15 + 15  # 50
        
        percentage = (total / max_total) * 100
        
        if percentage >= 90:
            return "A+"
        elif percentage >= 85:
            return "A"
        elif percentage >= 80:
            return "A-"
        elif percentage >= 75:
            return "B+"
        elif percentage >= 70:
            return "B"
        elif percentage >= 65:
            return "B-"
        elif percentage >= 60:
            return "C+"
        elif percentage >= 50:
            return "C"
        elif percentage >= 40:
            return "C-"
        else:
            return "D"
    
    def _calculate_commercial_grade(
        self, market: float, documentation: float, revenue: float
    ) -> str:
        """Calculate commercial grade."""
        total = market + documentation + revenue
        max_total = 15 + 5 + 5  # 25
        
        percentage = (total / max_total) * 100
        
        if percentage >= 90:
            return "A+"
        elif percentage >= 85:
            return "A"
        elif percentage >= 80:
            return "A-"
        elif percentage >= 75:
            return "B+"
        elif percentage >= 70:
            return "B"
        elif percentage >= 65:
            return "B-"
        elif percentage >= 60:
            return "C+"
        elif percentage >= 50:
            return "C"
        elif percentage >= 40:
            return "C-"
        else:
            return "D"
    
    def _calculate_collateral_grade(
        self, originality: float, liquidation: float, collateral_score: float
    ) -> str:
        """Calculate collateral grade."""
        total = originality + liquidation + (collateral_score / 100 * 10)
        max_total = 15 + 10 + 10  # 35
        
        percentage = (total / max_total) * 100
        
        if percentage >= 90:
            return "A+"
        elif percentage >= 85:
            return "A"
        elif percentage >= 80:
            return "A-"
        elif percentage >= 75:
            return "B+"
        elif percentage >= 70:
            return "B"
        elif percentage >= 65:
            return "B-"
        elif percentage >= 60:
            return "C+"
        elif percentage >= 50:
            return "C"
        elif percentage >= 40:
            return "C-"
        else:
            return "D"
    
    def _determine_proof_level(
        self, execution_score: float, security_score: float, financeability_score: float
    ) -> ProofLevel:
        """Determine proof level based on scores."""
        if financeability_score >= 80 and execution_score >= 80 and security_score >= 90:
            return ProofLevel.FINANCEABLE
        elif financeability_score >= 70 and execution_score >= 70:
            return ProofLevel.MARKET_VERIFIED
        elif execution_score >= 80:
            return ProofLevel.USE_VERIFIED
        elif execution_score >= 70:
            return ProofLevel.BUILD_VERIFIED
        elif security_score >= 80:
            return ProofLevel.CLEAN
        elif execution_score >= 50:
            return ProofLevel.HASHED
        elif execution_score >= 30:
            return ProofLevel.DISCOVERED
        else:
            return ProofLevel.CLAIMED


class StrategicValueClassifier:
    """
    Classify strategic value of assets.
    
    Determines:
    - Strategic value (High, Moderate, Low)
    - Buyer-today value (High, Moderate, Low)
    - Collateral support (Conservative, Moderate, Aggressive)
    """
    
    def classify(self, grades: ProfessionalGrades, committee_results: Dict[str, Any]) -> Dict[str, str]:
        """Classify strategic value dimensions."""
        strategic_value = self._classify_strategic_value(grades, committee_results)
        buyer_today_value = self._classify_buyer_today_value(grades, committee_results)
        collateral_support = self._classify_collateral_support(grades, committee_results)
        
        return {
            "strategic_value": strategic_value,
            "buyer_today_value": buyer_today_value,
            "collateral_support": collateral_support,
        }
    
    def _classify_strategic_value(
        self, grades: ProfessionalGrades, committee_results: Dict[str, Any]
    ) -> str:
        """Classify strategic value."""
        # Strategic value combines production + commercial grades
        production_rank = self._grade_to_rank(grades.production_grade)
        commercial_rank = self._grade_to_rank(grades.commercial_grade)
        
        avg_rank = (production_rank + commercial_rank) / 2
        
        if avg_rank >= 4.5:
            return "High"
        elif avg_rank >= 3.5:
            return "Moderate"
        else:
            return "Low"
    
    def _classify_buyer_today_value(
        self, grades: ProfessionalGrades, committee_results: Dict[str, Any]
    ) -> str:
        """Classify buyer-today value."""
        # Buyer-today value focuses on execution + market + liquidation
        execution_score = grades.execution_proof
        market_score = grades.market_usefulness
        liquidation_score = grades.liquidation_path
        
        total = execution_score + market_score + liquidation_score
        max_total = 15 + 15 + 10  # 40
        
        percentage = (total / max_total) * 100
        
        if percentage >= 75:
            return "High"
        elif percentage >= 50:
            return "Moderate"
        else:
            return "Low"
    
    def _classify_collateral_support(
        self, grades: ProfessionalGrades, committee_results: Dict[str, Any]
    ) -> str:
        """Classify collateral support."""
        # Collateral support focuses on originality + liquidation + collateral grade
        originality_score = grades.originality_ownership
        liquidation_score = grades.liquidation_path
        collateral_rank = self._grade_to_rank(grades.collateral_grade)
        
        # Check for risk blocks
        committee_report = committee_results.get("committee_report", {})
        risk_blocked = committee_report.get("risk_blocked", False)
        
        if risk_blocked:
            return "Risk-blocked - not eligible"
        
        avg_score = (originality_score + liquidation_score) / 2
        max_score = (15 + 10) / 2  # 12.5
        
        percentage = (avg_score / max_score) * 100
        
        if percentage >= 75 and collateral_rank >= 4:
            return "Aggressive"
        elif percentage >= 50 and collateral_rank >= 3:
            return "Moderate"
        elif percentage >= 30:
            return "Conservative and conditional"
        else:
            return "Not eligible"
    
    def _grade_to_rank(self, grade: str) -> float:
        """Convert letter grade to numeric rank."""
        grade_map = {
            "A+": 5.0,
            "A": 4.7,
            "A-": 4.3,
            "B+": 4.0,
            "B": 3.7,
            "B-": 3.3,
            "C+": 3.0,
            "C": 2.7,
            "C-": 2.3,
            "D": 2.0,
            "F": 1.0,
        }
        return grade_map.get(grade, 1.0)


class BlockerAnalyzer:
    """
    Analyze blockers and identify main issues preventing financeability.
    """
    
    def analyze_blockers(self, committee_results: Dict[str, Any]) -> List[str]:
        """Analyze and categorize blockers."""
        committee_report = committee_results.get("committee_report", {})
        all_blockers = committee_report.get("all_blockers", [])
        
        # Categorize blockers
        categorized = {
            "critical": [],
            "major": [],
            "moderate": [],
        }
        
        for blocker in all_blockers:
            if "secret" in blocker.lower() or "private key" in blocker.lower():
                categorized["critical"].append(blocker)
            elif "ownership" in blocker.lower() or "license" in blocker.lower():
                categorized["major"].append(blocker)
            elif "build" in blocker.lower() or "scaffold" in blocker.lower():
                categorized["major"].append(blocker)
            else:
                categorized["moderate"].append(blocker)
        
        # Generate main blockers summary
        main_blockers = []
        
        if categorized["critical"]:
            main_blockers.append(f"CRITICAL: {', '.join(categorized['critical'][:2])}")
        
        if categorized["major"]:
            main_blockers.append(f"MAJOR: {', '.join(categorized['major'][:3])}")
        
        if categorized["moderate"]:
            main_blockers.append(f"MODERATE: {len(categorized['moderate'])} issues")
        
        return main_blockers if main_blockers else ["No critical blockers identified"]
