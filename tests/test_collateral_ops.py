#!/usr/bin/env python3
"""Unit tests for CollateralOps capital translation modules."""

import sys
import os
import unittest
import tempfile
import shutil
from decimal import Decimal

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from collateral_packet import (
    AssetRecord,
    ValuationSet,
    DeductionSchedule,
    RiskRegister,
    SoftwareCollateralPacket,
    ProofLevel,
    AssetType,
)
from underwriting_engine import UnderwritingEngine
from financeability_engine import FinanceabilityEngine
from lender_packet import LenderPacketGenerator
from buyer_packet import BuyerPacketGenerator
from asset_improvement_agent import AssetImprovementAgent
from agent_work_auditor import AgentWorkAuditor, AgentActivityRecord
from collateral_registry import CollateralRegistry


class TestValuationSetSerialization(unittest.TestCase):
    def test_decimal_serialization(self):
        v = ValuationSet(
            replacement_cost_usd=Decimal("12345.67"),
            as_is_sale_value_usd=Decimal("5000.00"),
            productized_value_usd=Decimal("8000.50"),
            liquidation_value_usd=Decimal("2000.00"),
            collateral_support_value_usd=Decimal("1500.25"),
            financeability_score=55,
        )
        d = v.to_dict()
        self.assertEqual(d["replacement_cost_usd"], "12345.67")
        self.assertEqual(d["financeability_score"], 55)


class TestDeductionScheduleSerialization(unittest.TestCase):
    def test_nested_decimal_serialization(self):
        ds = DeductionSchedule(
            base_strategic_value=Decimal("10000"),
            deductions=[
                {"reason": "test", "amount": Decimal("2500.50"), "pct": "25%"}
            ],
            final_collateral_support=Decimal("7500"),
        )
        d = ds.to_dict()
        self.assertEqual(d["deductions"][0]["amount"], "2500.50")
        self.assertEqual(d["final_collateral_support"], "7500")


class TestUnderwritingEngine(unittest.TestCase):
    def setUp(self):
        self.engine = UnderwritingEngine()
        self.asset = AssetRecord(
            asset_name="test_repo",
            asset_type=AssetType.ORIGINAL_REPOSITORY,
            primary_language="python",
            file_count=25,
            total_size_bytes=50000,
            build_status="passed",
            test_status="passed",
            license_status="clean",
            secret_scan_status="passed",
            documentation_score=60,
            risk_register=RiskRegister(
                ownership_risk="low",
                originality_risk="low",
                build_risk="low",
                license_risk="low",
                secret_risk="low",
                market_risk="medium",
                liquidation_risk="low",
            ),
        )

    def test_appraise_returns_valuation(self):
        v = self.engine.appraise(self.asset, {"stars": 50, "forks": 5})
        self.assertIsInstance(v, ValuationSet)
        self.assertGreater(v.replacement_cost_usd, Decimal("0"))
        self.assertGreaterEqual(v.financeability_score, 0)
        self.assertLessEqual(v.financeability_score, 100)

    def test_deduction_schedule(self):
        v = self.engine.appraise(self.asset, {"stars": 50})
        ds = self.engine.generate_deduction_schedule(self.asset, v.replacement_cost_usd)
        self.assertIsInstance(ds, DeductionSchedule)
        self.assertGreater(len(ds.deductions), 0)
        self.assertIsInstance(ds.final_collateral_support, Decimal)

    def test_conservatism_applied(self):
        v = self.engine.appraise(self.asset, {"stars": 1000})
        self.assertLess(v.replacement_cost_usd, Decimal("5000000"))


class TestFinanceabilityEngine(unittest.TestCase):
    def setUp(self):
        self.engine = FinanceabilityEngine()
        self.asset = AssetRecord(
            asset_name="test_repo",
            asset_type=AssetType.ORIGINAL_REPOSITORY,
            primary_language="python",
            build_status="passed",
            test_status="passed",
            license_status="clean",
            secret_scan_status="passed",
            documentation_score=70,
            risk_register=RiskRegister(
                ownership_risk="low",
                originality_risk="low",
                build_risk="low",
                license_risk="low",
                secret_risk="low",
                market_risk="medium",
                liquidation_risk="low",
            ),
        )
        # Give it a valuation
        uw = UnderwritingEngine()
        self.asset.valuation = uw.appraise(self.asset, {"stars": 100})

    def test_analyze_returns_report(self):
        report = self.engine.analyze(self.asset)
        self.assertIsNotNone(report.subscores)
        self.assertIsInstance(report.overall_score, int)
        self.assertGreaterEqual(report.overall_score, 0)
        self.assertLessEqual(report.overall_score, 100)

    def test_improvement_queue_generated(self):
        report = self.engine.analyze(self.asset)
        self.assertIsInstance(report.improvement_queue, list)

    def test_best_next_action(self):
        report = self.engine.analyze(self.asset)
        if report.improvement_queue:
            self.assertIsNotNone(report.one_best_next_action)


class TestLenderPacketGenerator(unittest.TestCase):
    def setUp(self):
        self.gen = LenderPacketGenerator()
        self.asset = AssetRecord(
            asset_name="lender_test",
            asset_type=AssetType.ORIGINAL_REPOSITORY,
            primary_language="python",
            build_status="passed",
            test_status="passed",
            license_status="clean",
            secret_scan_status="passed",
            risk_register=RiskRegister(
                ownership_risk="low",
                originality_risk="low",
                build_risk="low",
                license_risk="low",
                secret_risk="low",
                market_risk="medium",
                liquidation_risk="low",
            ),
        )
        uw = UnderwritingEngine()
        self.asset.valuation = uw.appraise(self.asset, {"stars": 50})

    def test_generate_packet(self):
        packet = self.gen.generate(self.asset, {"stars": 50})
        self.assertIsInstance(packet, SoftwareCollateralPacket)
        self.assertTrue(packet.packet_hash)
        # With build passed, license clean, docs 60, score is ~55 => LTV 5%-15%
        self.assertTrue(len(packet.recommended_loan_to_value or "") > 0)

    def test_summary_text(self):
        packet = self.gen.generate(self.asset, {"stars": 50})
        summary = self.gen.generate_summary_text(packet)
        self.assertIn("SOFTWARE COLLATERAL PACKET", summary)


class TestBuyerPacketGenerator(unittest.TestCase):
    def setUp(self):
        self.gen = BuyerPacketGenerator()
        self.asset = AssetRecord(
            asset_name="buyer_test",
            asset_type=AssetType.ORIGINAL_REPOSITORY,
            primary_language="python",
            build_status="passed",
            license_status="clean",
            risk_register=RiskRegister(
                ownership_risk="low",
                originality_risk="low",
                build_risk="low",
                license_risk="low",
                secret_risk="low",
                market_risk="medium",
                liquidation_risk="low",
            ),
        )
        uw = UnderwritingEngine()
        self.asset.valuation = uw.appraise(self.asset, {"stars": 50})

    def test_generate_packet(self):
        packet = self.gen.generate(self.asset, {"stars": 50})
        self.assertIsInstance(packet, SoftwareCollateralPacket)
        self.assertTrue(packet.packet_hash)


class TestAssetImprovementAgent(unittest.TestCase):
    def setUp(self):
        self.agent = AssetImprovementAgent()
        self.asset = AssetRecord(
            asset_name="improve_test",
            asset_type=AssetType.ORIGINAL_REPOSITORY,
            primary_language="python",
            build_status="passed",
            test_status="passed",
            license_status="clean",
            secret_scan_status="passed",
            documentation_score=70,
            risk_register=RiskRegister(
                ownership_risk="low",
                originality_risk="low",
                build_risk="low",
                license_risk="low",
                secret_risk="low",
                market_risk="medium",
                liquidation_risk="low",
            ),
        )

    def test_analyze_single_asset(self):
        result = self.agent.analyze_single_asset(self.asset, {"stars": 50})
        self.assertIn("financeability_report", result)
        self.assertIn("valuation", result)

    def test_portfolio_audit(self):
        report = self.agent.run_portfolio_audit([self.asset], {})
        self.assertIsNotNone(report)
        self.assertEqual(report.new_assets_found, 0)


class TestAgentWorkAuditor(unittest.TestCase):
    def setUp(self):
        self.auditor = AgentWorkAuditor()

    def test_audit_session(self):
        activities = [
            AgentActivityRecord(
                agent_name="windsurf",
                activity_type="create",
                file_path="test.py",
                file_hash="abc123",
                description="Created test module",
                production_ready=True,
            ),
            AgentActivityRecord(
                agent_name="windsurf",
                activity_type="build_pass",
                description="Build passed",
            ),
        ]
        report = self.auditor.audit_agent_session("windsurf", activities)
        self.assertEqual(report.agent_name, "windsurf")
        self.assertEqual(report.files_created, 1)
        self.assertEqual(report.builds_passed, 1)
        self.assertGreater(report.estimated_gross_labor_value, Decimal("0"))

    def test_audit_directory(self):
        tmpdir = tempfile.mkdtemp()
        with open(os.path.join(tmpdir, "main.py"), "w") as f:
            f.write("def main(): pass\n")
        try:
            report = self.auditor.audit_directory("windsurf", tmpdir)
            self.assertGreaterEqual(report.files_created, 1)
        finally:
            shutil.rmtree(tmpdir)

    def test_combined_report(self):
        r1 = self.auditor.audit_agent_session("windsurf", [])
        r2 = self.auditor.audit_agent_session("cursor", [])
        combined = self.auditor.generate_combined_report([r1, r2])
        self.assertEqual(combined["aggregate"]["agents_audited"], 2)


class TestCollateralRegistry(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.NamedTemporaryFile(suffix=".db", delete=False)
        self._tmp.close()
        self.tmp_db = self._tmp.name
        self.registry = CollateralRegistry(self.tmp_db)

    def tearDown(self):
        if os.path.exists(self.tmp_db):
            os.remove(self.tmp_db)

    def test_store_and_retrieve(self):
        packet = {"packet_id": "test-123", "section_a_identity": {"asset_record": {"asset_id": "a1", "asset_name": "foo"}}}
        row_id = self.registry.store_packet(packet)
        self.assertGreater(row_id, 0)

        retrieved = self.registry.get_packet("test-123")
        self.assertIsNotNone(retrieved)
        self.assertEqual(retrieved["packet_id"], "test-123")

    def test_list_packets(self):
        self.registry.store_packet({"packet_id": "p1", "section_a_identity": {"asset_record": {"asset_id": "a1", "asset_name": "foo"}}})
        packets = self.registry.list_all_packets()
        self.assertEqual(len(packets), 1)

    def test_log_event(self):
        self.registry.log_event("a1", "build_pass", {"status": "ok"})
        events = self.registry.get_events("a1")
        self.assertEqual(len(events), 1)
        self.assertEqual(events[0]["event_type"], "build_pass")


if __name__ == "__main__":
    unittest.main()
