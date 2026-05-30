#!/usr/bin/env python3
"""
Database migrations for Catacomb.

Migrates from SQLite to Postgres and creates production schema.
"""

import os
import psycopg2
from psycopg2 import sql
from datetime import datetime

DATABASE_URL = os.environ.get('DATABASE_URL')


def get_connection():
    """Get database connection."""
    if DATABASE_URL:
        return psycopg2.connect(DATABASE_URL)
    else:
        raise ValueError("DATABASE_URL not set")


def create_interventions_table():
    """Create interventions table."""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS interventions (
            id SERIAL PRIMARY KEY,
            asset_id TEXT NOT NULL,
            intervention_type TEXT NOT NULL,
            predicted_value REAL NOT NULL,
            planned_effort_days INTEGER NOT NULL,
            outcome_metrics JSONB,
            before_state JSONB,
            after_state JSONB,
            verification_status TEXT DEFAULT 'pending',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_interventions_asset_id ON interventions(asset_id)
    """)
    
    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_interventions_verification_status ON interventions(verification_status)
    """)
    
    conn.commit()
    conn.close()
    print("Created interventions table")


def create_proof_packets_table():
    """Create proof packets table."""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS proof_packets (
            id SERIAL PRIMARY KEY,
            packet_id TEXT UNIQUE NOT NULL,
            packet_data JSONB NOT NULL,
            asset_id TEXT NOT NULL,
            intervention_type TEXT NOT NULL,
            verification_status TEXT NOT NULL,
            created_at TIMESTAMP NOT NULL,
            verified_at TIMESTAMP
        )
    """)
    
    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_proof_packets_asset_id ON proof_packets(asset_id)
    """)
    
    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_proof_packets_verification_status ON proof_packets(verification_status)
    """)
    
    conn.commit()
    conn.close()
    print("Created proof_packets table")


def create_asset_embeddings_table():
    """Create asset embeddings table."""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS asset_embeddings (
            asset_id TEXT PRIMARY KEY,
            asset_type TEXT NOT NULL,
            genome_embedding BYTEA NOT NULL,
            state_embedding BYTEA NOT NULL,
            intervention_embedding BYTEA NOT NULL,
            combined_embedding BYTEA NOT NULL,
            genome_weight REAL DEFAULT 0.3,
            state_weight REAL DEFAULT 0.3,
            intervention_weight REAL DEFAULT 0.4,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_asset_embeddings_type ON asset_embeddings(asset_type)
    """)
    
    conn.commit()
    conn.close()
    print("Created asset_embeddings table")


def create_collateral_positions_table():
    """Create collateral positions table."""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS collateral_positions (
            position_id TEXT PRIMARY KEY,
            proof_id TEXT NOT NULL,
            collateral_amount DECIMAL(20, 8) NOT NULL,
            collateral_token TEXT NOT NULL,
            liquidity_pool_id TEXT NOT NULL,
            creator TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            unlocked_at TIMESTAMP,
            unlock_conditions JSONB,
            status TEXT NOT NULL
        )
    """)
    
    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_collateral_positions_proof_id ON collateral_positions(proof_id)
    """)
    
    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_collateral_positions_pool_id ON collateral_positions(liquidity_pool_id)
    """)
    
    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_collateral_positions_status ON collateral_positions(status)
    """)
    
    conn.commit()
    conn.close()
    print("Created collateral_positions table")


def create_liquidity_pools_table():
    """Create liquidity pools table."""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS liquidity_pools (
            pool_id TEXT PRIMARY KEY,
            collateral_token TEXT NOT NULL,
            total_liquidity DECIMAL(20, 8) NOT NULL,
            locked_collateral DECIMAL(20, 8) NOT NULL,
            available_liquidity DECIMAL(20, 8) NOT NULL,
            reward_rate DECIMAL(10, 8) NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    conn.commit()
    conn.close()
    print("Created liquidity_pools table")


def create_historical_states_table():
    """Create historical states table."""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS historical_states (
            id SERIAL PRIMARY KEY,
            pool_id TEXT NOT NULL,
            state_data JSONB NOT NULL,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_historical_states_pool_id ON historical_states(pool_id)
    """)
    
    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_historical_states_timestamp ON historical_states(timestamp)
    """)
    
    conn.commit()
    conn.close()
    print("Created historical_states table")


def create_users_table():
    """Create users table for auth."""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            email TEXT UNIQUE NOT NULL,
            name TEXT,
            role TEXT DEFAULT 'viewer',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_users_email ON users(email)
    """)
    
    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_users_role ON users(role)
    """)
    
    conn.commit()
    conn.close()
    print("Created users table")


def migrate_all():
    """Run all migrations."""
    print("Starting database migrations...")
    print(f"DATABASE_URL: {DATABASE_URL[:20]}..." if DATABASE_URL else "DATABASE_URL not set")
    
    try:
        create_interventions_table()
        create_proof_packets_table()
        create_asset_embeddings_table()
        create_collateral_positions_table()
        create_liquidity_pools_table()
        create_historical_states_table()
        create_users_table()
        
        print("All migrations completed successfully")
    except Exception as e:
        print(f"Migration failed: {e}")
        raise


if __name__ == '__main__':
    migrate_all()
