#!/usr/bin/env python3
"""
CollateralRegistry - SQLite persistence layer for Software Collateral Packets.

Stores packet metadata, valuations, and financeability reports.
"""

import os
import sqlite3
import json
from datetime import datetime
from typing import Dict, Any, List, Optional

from collateral_config import COLLATERAL_DB_PATH


class CollateralRegistry:
    """SQLite-backed registry for collateral packets and asset history."""

    def __init__(self, db_path: str = COLLATERAL_DB_PATH):
        self.db_path = db_path
        self._init_db()

    def _init_db(self) -> None:
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS collateral_packets (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                packet_id TEXT NOT NULL UNIQUE,
                asset_id TEXT NOT NULL,
                asset_name TEXT,
                packet_json TEXT NOT NULL,
                packet_hash TEXT,
                financeability_score INTEGER,
                collateral_support_usd TEXT,
                valuation_json TEXT,
                generated_at TEXT,
                updated_at TEXT
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS asset_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                asset_id TEXT NOT NULL,
                packet_id TEXT,
                event_type TEXT NOT NULL,
                event_data TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        """)

        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_packets_asset_id 
            ON collateral_packets(asset_id)
        """)

        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_history_asset_id 
            ON asset_history(asset_id)
        """)

        conn.commit()
        conn.close()

    def store_packet(self, packet_dict: Dict[str, Any]) -> int:
        """Store a collateral packet and return its DB id."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        packet_id = packet_dict.get("packet_id", "unknown")
        asset_record = packet_dict.get("section_a_identity", {}).get("asset_record") or {}
        asset_id = asset_record.get("asset_id", "unknown")
        asset_name = asset_record.get("asset_name")

        appraisal = packet_dict.get("section_c_economic_appraisal") or {}
        valuation = appraisal.get("valuation") or {}
        fin_score = valuation.get("financeability_score")
        cs_val = str(valuation.get("collateral_support_value_usd", "0"))

        now = datetime.now().isoformat()

        cursor.execute("""
            INSERT OR REPLACE INTO collateral_packets
            (packet_id, asset_id, asset_name, packet_json, packet_hash,
             financeability_score, collateral_support_usd, valuation_json, generated_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            packet_id,
            asset_id,
            asset_name,
            json.dumps(packet_dict),
            packet_dict.get("packet_hash"),
            fin_score,
            cs_val,
            json.dumps(valuation),
            now,
            now,
        ))

        row_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return row_id

    def get_packet(self, packet_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve a packet by its packet_id."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute(
            "SELECT packet_json FROM collateral_packets WHERE packet_id = ?",
            (packet_id,)
        )
        row = cursor.fetchone()
        conn.close()
        if row:
            return json.loads(row["packet_json"])
        return None

    def get_packets_by_asset(self, asset_id: str) -> List[Dict[str, Any]]:
        """Retrieve all packets for an asset."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute(
            "SELECT packet_json FROM collateral_packets WHERE asset_id = ? ORDER BY generated_at DESC",
            (asset_id,)
        )
        rows = cursor.fetchall()
        conn.close()
        return [json.loads(r["packet_json"]) for r in rows]

    def log_event(self, asset_id: str, event_type: str, event_data: Dict[str, Any]) -> None:
        """Log an asset event (e.g., improvement, audit, sale interest)."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO asset_history (asset_id, event_type, event_data)
            VALUES (?, ?, ?)
        """, (asset_id, event_type, json.dumps(event_data)))
        conn.commit()
        conn.close()

    def get_events(self, asset_id: str) -> List[Dict[str, Any]]:
        """Get all events for an asset."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM asset_history WHERE asset_id = ? ORDER BY created_at DESC",
            (asset_id,)
        )
        rows = cursor.fetchall()
        conn.close()
        return [dict(r) for r in rows]

    def list_all_packets(self, limit: int = 100) -> List[Dict[str, Any]]:
        """List all stored packets with summary fields."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("""
            SELECT packet_id, asset_id, asset_name, financeability_score,
                   collateral_support_usd, generated_at
            FROM collateral_packets
            ORDER BY generated_at DESC
            LIMIT ?
        """, (limit,))
        rows = cursor.fetchall()
        conn.close()
        return [dict(r) for r in rows]
