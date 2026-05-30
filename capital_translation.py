#!/usr/bin/env python3
"""
Capital Translation Layer - Converting developer language into finance language.

This layer is the product. It translates developer-speak into capital-speak.

Developer language:
"This is a local Python app that scans repos and estimates value."

Capital language:
"This is a software asset appraisal tool with potential use in developer portfolio audits, 
IP diligence, and buyer packet generation. Current strategic value exceeds collateral support 
because recoverability is limited by lack of revenue proof, reviewer validation, and buyer 
outcome history."

Developer language:
"This bot trades micro-notional futures."

Capital language:
"This is financial automation software with engineering value, but collateral treatment 
should be conservative due to regulatory risk, no audited PnL, venue dependency, and high 
operational risk."

Developer language:
"This folder has lots of generated files."

Capital language:
"This appears to be an AI-agent output cluster. It requires deduplication, scaffold removal, 
originality review, and production-readiness classification before any asset value can be 
assigned."

That translation is the product - it preserves the developer's position. The developer is not 
begging a lender to understand code. The developer is presenting standardized evidence.
"""

from typing import Dict, Any, List, Optional
from dataclasses import dataclass
from enum import Enum


class TranslationTone(Enum):
    """Tone for capital translation."""
    PROFESSIONAL = "professional"
    CONSERVATIVE = "conservative"
    OPTIMISTIC = "optimistic"
    CAUTIOUS = "cautious"


@dataclass
class CapitalTranslation:
    """
    A translation from developer language to capital language.
    """
    original_developer_description: str
    translated_capital_description: str
    asset_classification: str
    strategic_value: str
    collateral_treatment: str
    risk_factors: List[str]
    value_drivers: List[str]
    blockers: List[str]
    tone: TranslationTone = TranslationTone.PROFESSIONAL
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "original_developer_description": self.original_developer_description,
            "translated_capital_description": self.translated_capital_description,
            "asset_classification": self.asset_classification,
            "strategic_value": self.strategic_value,
            "collateral_treatment": self.collateral_treatment,
            "risk_factors": self.risk_factors,
            "value_drivers": self.value_drivers,
            "blockers": self.blockers,
            "tone": self.tone.value,
        }


class CapitalTranslator:
    """
    Capital Translator - Converts developer language to finance language.
    
    This is the ideological center: Builder-side capital translation.
    
    The product is not built to help banks discount developers.
    It is built to help developers become legible to capital without losing control.
    """
    
    def __init__(self):
        self.translation_patterns = {
            # Pattern: local app → software asset with potential use
            "local_app": {
                "keywords": ["local", "app", "script", "tool", "utility"],
                "translation_template": "This is a {asset_type} with potential use in {use_cases}. {strategic_value_statement}.",
                "asset_type_mapping": {
                    "python": "Python-based software tool",
                    "javascript": "JavaScript-based utility",
                    "rust": "Rust-based system",
                    "go": "Go-based service",
                },
            },
            
            # Pattern: trading bot → financial automation with regulatory risk
            "trading_bot": {
                "keywords": ["trading", "bot", "futures", "crypto", "finance"],
                "translation_template": "This is financial automation software with engineering value, but collateral treatment should be conservative due to {risk_factors}.",
                "risk_factors": [
                    "regulatory risk",
                    "no audited PnL",
                    "venue dependency",
                    "high operational risk",
                ],
            },
            
            # Pattern: generated files → AI-agent output cluster
            "generated_files": {
                "keywords": ["generated", "ai", "agent", "llm", "output"],
                "translation_template": "This appears to be an AI-agent output cluster. It requires {required_actions} before any asset value can be assigned.",
                "required_actions": [
                    "deduplication",
                    "scaffold removal",
                    "originality review",
                    "production-readiness classification",
                ],
            },
            
            # Pattern: repo → software asset
            "repository": {
                "keywords": ["repo", "repository", "github", "codebase"],
                "translation_template": "This is a {asset_classification} with {value_drivers}. {collateral_statement}.",
            },
            
            # Pattern: prototype → early-stage software
            "prototype": {
                "keywords": ["prototype", "poc", "proof of concept", "mvp"],
                "translation_template": "This is an early-stage software asset with {value_drivers}. Collateral treatment should be {treatment} due to {blockers}.",
            },
        }
    
    def translate(
        self,
        developer_description: str,
        asset_data: Dict[str, Any],
        grades: Dict[str, Any],
        committee_results: Dict[str, Any],
    ) -> CapitalTranslation:
        """
        Translate developer description to capital language.
        
        Args:
            developer_description: Original developer description
            asset_data: Asset metadata and classification
            grades: Professional grades
            committee_results: Committee evaluation results
        
        Returns:
            CapitalTranslation with translated description and context
        """
        # Detect pattern
        pattern = self._detect_pattern(developer_description, asset_data)
        
        # Generate translation
        translated = self._generate_translation(
            pattern,
            developer_description,
            asset_data,
            grades,
            committee_results,
        )
        
        return translated
    
    def _detect_pattern(self, description: str, asset_data: Dict[str, Any]) -> str:
        """Detect the translation pattern based on description and asset data."""
        description_lower = description.lower()
        
        # Check for trading bot pattern
        if any(keyword in description_lower for keyword in self.translation_patterns["trading_bot"]["keywords"]):
            return "trading_bot"
        
        # Check for generated files pattern
        if any(keyword in description_lower for keyword in self.translation_patterns["generated_files"]["keywords"]):
            return "generated_files"
        
        # Check for prototype pattern
        if any(keyword in description_lower for keyword in self.translation_patterns["prototype"]["keywords"]):
            return "prototype"
        
        # Check for local app pattern
        if any(keyword in description_lower for keyword in self.translation_patterns["local_app"]["keywords"]):
            return "local_app"
        
        # Default to repository pattern
        return "repository"
    
    def _generate_translation(
        self,
        pattern: str,
        developer_description: str,
        asset_data: Dict[str, Any],
        grades: Dict[str, Any],
        committee_results: Dict[str, Any],
    ) -> CapitalTranslation:
        """Generate the capital translation."""
        pattern_config = self.translation_patterns.get(pattern, self.translation_patterns["repository"])
        
        # Extract key information
        asset_type = asset_data.get("asset_type", "software asset")
        classification = asset_data.get("classification", "unknown")
        language = asset_data.get("primary_language", "unknown")
        
        production_grade = grades.get("production_grade", "C")
        commercial_grade = grades.get("commercial_grade", "C")
        collateral_grade = grades.get("collateral_grade", "C")
        financeability_score = grades.get("financeability_score", 0)
        
        committee_report = committee_results.get("committee_report", {})
        blockers = committee_report.get("all_blockers", [])
        risk_blocked = committee_report.get("risk_blocked", False)
        
        # Generate translation based on pattern
        if pattern == "trading_bot":
            translated = self._translate_trading_bot(
                developer_description, asset_data, grades, committee_results
            )
        elif pattern == "generated_files":
            translated = self._translate_generated_files(
                developer_description, asset_data, grades, committee_results
            )
        elif pattern == "local_app":
            translated = self._translate_local_app(
                developer_description, asset_data, grades, committee_results
            )
        elif pattern == "prototype":
            translated = self._translate_prototype(
                developer_description, asset_data, grades, committee_results
            )
        else:
            translated = self._translate_repository(
                developer_description, asset_data, grades, committee_results
            )
        
        return translated
    
    def _translate_trading_bot(
        self,
        developer_description: str,
        asset_data: Dict[str, Any],
        grades: Dict[str, Any],
        committee_results: Dict[str, Any],
    ) -> CapitalTranslation:
        """Translate trading bot description."""
        risk_factors = [
            "regulatory risk",
            "no audited PnL",
            "venue dependency",
            "high operational risk",
        ]
        
        if grades.get("security_license_cleanliness", 0) < 10:
            risk_factors.append("security concerns")
        
        value_drivers = [
            "automation capability",
            "engineering complexity",
            "potential revenue generation",
        ]
        
        translated = (
            f"This is financial automation software with engineering value, "
            f"but collateral treatment should be conservative due to {', '.join(risk_factors[:3])}. "
            f"Production grade is {grades.get('production_grade', 'C')}, indicating "
            f"{'strong' if grades.get('production_grade') in ['A', 'B'] else 'limited'} "
            f"technical execution. Commercial grade is {grades.get('commercial_grade', 'C')}, "
            f"suggesting {'moderate' if grades.get('commercial_grade') in ['B', 'C'] else 'limited'} "
            f"market potential."
        )
        
        return CapitalTranslation(
            original_developer_description=developer_description,
            translated_capital_description=translated,
            asset_classification="Financial Automation Software",
            strategic_value="Moderate - engineering value present but regulatory and operational risks limit collateral treatment",
            collateral_treatment="Conservative - not suitable as primary collateral due to regulatory and operational risks",
            risk_factors=risk_factors,
            value_drivers=value_drivers,
            blockers=committee_results.get("committee_report", {}).get("all_blockers", []),
            tone=TranslationTone.CAUTIOUS,
        )
    
    def _translate_generated_files(
        self,
        developer_description: str,
        asset_data: Dict[str, Any],
        grades: Dict[str, Any],
        committee_results: Dict[str, Any],
    ) -> CapitalTranslation:
        """Translate generated files description."""
        required_actions = [
            "deduplication",
            "scaffold removal",
            "originality review",
            "production-readiness classification",
        ]
        
        translated = (
            f"This appears to be an AI-agent output cluster. "
            f"It requires {', '.join(required_actions)} before any asset value can be assigned. "
            f"Current financeability score is {grades.get('financeability_score', 0)}/100, "
            f"indicating {'significant' if grades.get('financeability_score', 0) < 30 else 'moderate'} "
            f"cleanup burden. Signal-to-noise ratio assessment suggests "
            f"{'high' if asset_data.get('signal_to_noise_ratio', 0) > 0.7 else 'low'} "
            f"value density after filtering."
        )
        
        return CapitalTranslation(
            original_developer_description=developer_description,
            translated_capital_description=translated,
            asset_classification="AI-Agent Output Cluster",
            strategic_value="Low - requires significant curation and filtering before capitalization",
            collateral_treatment="Not eligible - not a distinct asset until curation and originality review",
            risk_factors=["low signal-to-noise ratio", "scaffold contamination", "originality ambiguity"],
            value_drivers=["potential original contributions", "automation patterns"],
            blockers=committee_results.get("committee_report", {}).get("all_blockers", []),
            tone=TranslationTone.CONSERVATIVE,
        )
    
    def _translate_local_app(
        self,
        developer_description: str,
        asset_data: Dict[str, Any],
        grades: Dict[str, Any],
        committee_results: Dict[str, Any],
    ) -> CapitalTranslation:
        """Translate local app description."""
        language = asset_data.get("primary_language", "unknown")
        use_cases = self._infer_use_cases(asset_data)
        
        strategic_value_statement = (
            f"Current strategic value is {'high' if grades.get('financeability_score', 0) > 70 else 'moderate' if grades.get('financeability_score', 0) > 50 else 'low'}, "
            f"but collateral support is {'limited' if grades.get('collateral_grade') in ['C', 'D'] else 'conditional'} "
            f"due to {'lack of revenue proof' if grades.get('revenue_adoption_proof', 0) < 3 else 'limited market validation'}"
        )
        
        translated = (
            f"This is a {language}-based software tool with potential use in {', '.join(use_cases)}. "
            f"{strategic_value_statement}. "
            f"Production grade is {grades.get('production_grade', 'C')}, "
            f"indicating {'production-ready' if grades.get('production_grade') in ['A', 'B'] else 'prototype-level'} "
            f"execution. Commercial grade is {grades.get('commercial_grade', 'C')}, "
            f"suggesting {'clear' if grades.get('commercial_grade') in ['A', 'B'] else 'developing'} "
            f"market positioning."
        )
        
        return CapitalTranslation(
            original_developer_description=developer_description,
            translated_capital_description=translated,
            asset_classification=f"{language.title()} Software Tool",
            strategic_value=f"{'High' if grades.get('financeability_score', 0) > 70 else 'Moderate' if grades.get('financeability_score', 0) > 50 else 'Low'}",
            collateral_treatment=f"{'Conditional' if grades.get('collateral_grade') in ['B', 'C'] else 'Conservative'}",
            risk_factors=self._extract_risk_factors(committee_results),
            value_drivers=self._extract_value_drivers(asset_data, grades),
            blockers=committee_results.get("committee_report", {}).get("all_blockers", []),
            tone=TranslationTone.PROFESSIONAL,
        )
    
    def _translate_prototype(
        self,
        developer_description: str,
        asset_data: Dict[str, Any],
        grades: Dict[str, Any],
        committee_results: Dict[str, Any],
    ) -> CapitalTranslation:
        """Translate prototype description."""
        blockers = committee_results.get("committee_report", {}).get("all_blockers", [])
        
        treatment = "conservative" if len(blockers) > 2 else "conditional"
        
        translated = (
            f"This is an early-stage software asset with "
            f"{'clear technical direction' if grades.get('production_grade') in ['B', 'C'] else 'developing technical approach'}. "
            f"Collateral treatment should be {treatment} due to "
            f"{', '.join(blockers[:3]) if blockers else 'early-stage development status'}. "
            f"Financeability score is {grades.get('financeability_score', 0)}/100, "
            f"indicating {'significant' if grades.get('financeability_score', 0) < 40 else 'moderate' if grades.get('financeability_score', 0) < 60 else 'limited'} "
            f"development required before capitalization."
        )
        
        return CapitalTranslation(
            original_developer_description=developer_description,
            translated_capital_description=translated,
            asset_classification="Early-Stage Software Asset",
            strategic_value="Moderate - clear potential but requires development",
            collateral_treatment=f"{treatment.title()} - not financeable until development milestones met",
            risk_factors=blockers,
            value_drivers=self._extract_value_drivers(asset_data, grades),
            blockers=blockers,
            tone=TranslationTone.CAUTIOUS,
        )
    
    def _translate_repository(
        self,
        developer_description: str,
        asset_data: Dict[str, Any],
        grades: Dict[str, Any],
        committee_results: Dict[str, Any],
    ) -> CapitalTranslation:
        """Translate repository description."""
        classification = asset_data.get("classification", "software asset")
        value_drivers = self._extract_value_drivers(asset_data, grades)
        
        collateral_statement = (
            f"Collateral grade is {grades.get('collateral_grade', 'C')}, "
            f"indicating {'strong' if grades.get('collateral_grade') in ['A', 'B'] else 'limited' if grades.get('collateral_grade') == 'C' else 'no'} "
            f"collateral support capability."
        )
        
        translated = (
            f"This is a {classification} with {', '.join(value_drivers[:3])}. "
            f"{collateral_statement} "
            f"Production grade is {grades.get('production_grade', 'C')} and "
            f"commercial grade is {grades.get('commercial_grade', 'C')}, "
            f"resulting in a financeability score of {grades.get('financeability_score', 0)}/100."
        )
        
        return CapitalTranslation(
            original_developer_description=developer_description,
            translated_capital_description=translated,
            asset_classification=classification.title(),
            strategic_value=self._classify_strategic_value(grades),
            collateral_treatment=self._classify_collateral_treatment(grades),
            risk_factors=self._extract_risk_factors(committee_results),
            value_drivers=value_drivers,
            blockers=committee_results.get("committee_report", {}).get("all_blockers", []),
            tone=TranslationTone.PROFESSIONAL,
        )
    
    def _infer_use_cases(self, asset_data: Dict[str, Any]) -> List[str]:
        """Infer potential use cases from asset data."""
        use_cases = []
        
        category = asset_data.get("category", "unknown")
        description = asset_data.get("description", "").lower()
        
        if "audit" in description or "review" in description:
            use_cases.append("developer portfolio audits")
        if "diligence" in description or "review" in description:
            use_cases.append("IP diligence")
        if "packet" in description or "report" in description:
            use_cases.append("buyer packet generation")
        if "scan" in description or "analyze" in description:
            use_cases.append("automated analysis")
        if "api" in description or "service" in description:
            use_cases.append("API service")
        
        if not use_cases:
            use_cases.append("developer tooling")
        
        return use_cases
    
    def _extract_value_drivers(self, asset_data: Dict[str, Any], grades: Dict[str, Any]) -> List[str]:
        """Extract value drivers from asset data and grades."""
        drivers = []
        
        if grades.get("engineering_substance", 0) > 15:
            drivers.append("strong engineering foundation")
        if grades.get("execution_proof", 0) > 10:
            drivers.append("proven execution capability")
        if grades.get("market_usefulness", 0) > 10:
            drivers.append("clear market utility")
        if grades.get("originality_ownership", 0) > 10:
            drivers.append("clear ownership and originality")
        if asset_data.get("has_api_potential", False):
            drivers.append("API monetization potential")
        if asset_data.get("has_strategic_value", False):
            drivers.append("strategic buyer interest")
        
        if not drivers:
            drivers.append("development potential")
        
        return drivers
    
    def _extract_risk_factors(self, committee_results: Dict[str, Any]) -> List[str]:
        """Extract risk factors from committee results."""
        committee_report = committee_results.get("committee_report", {})
        blockers = committee_report.get("all_blockers", [])
        
        risk_factors = []
        for blocker in blockers:
            if "secret" in blocker.lower():
                risk_factors.append("security risk")
            elif "ownership" in blocker.lower():
                risk_factors.append("ownership risk")
            elif "build" in blocker.lower():
                risk_factors.append("execution risk")
            elif "license" in blocker.lower():
                risk_factors.append("license risk")
        
        return risk_factors if risk_factors else ["early-stage development"]
    
    def _classify_strategic_value(self, grades: Dict[str, Any]) -> str:
        """Classify strategic value from grades."""
        financeability = grades.get("financeability_score", 0)
        
        if financeability >= 70:
            return "High - strong engineering and commercial positioning"
        elif financeability >= 50:
            return "Moderate - clear potential with development needs"
        else:
            return "Low - significant development or cleanup required"
    
    def _classify_collateral_treatment(self, grades: Dict[str, Any]) -> str:
        """Classify collateral treatment from grades."""
        collateral_grade = grades.get("collateral_grade", "C")
        
        if collateral_grade in ["A+", "A", "A-"]:
            return "Aggressive - strong collateral support"
        elif collateral_grade in ["B+", "B", "B-"]:
            return "Moderate - conditional collateral support"
        elif collateral_grade in ["C+", "C", "C-"]:
            return "Conservative - limited collateral support"
        else:
            return "Not eligible - insufficient collateral support"
