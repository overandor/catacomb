"""Seed script for historical transformations."""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from outcome_ledger_v2 import OutcomeLedger, InterventionStatus, VerificationStatus
from innovation_elo import InnovationElo, EloEntityType
from transformation_tracking import TransformationTracker
from datetime import datetime, timedelta


def seed_historical_transformations():
    """Seed the Outcome Ledger with known historical transformations."""
    
    ledger = OutcomeLedger("outcome_ledger.db")
    elo_system = InnovationElo()
    transformation_tracker = TransformationTracker()
    
    # Historical transformations
    transformations = [
        {
            "asset_id": "vercel/next.js",
            "asset_type": "github_repo",
            "asset_name": "next.js",
            "developer_id": "github:vercel",
            "developer_username": "vercel",
            "before_state": {
                "stars": 500,
                "forks": 50,
                "contributors": 5,
                "language": "javascript",
                "category": "framework"
            },
            "intervention_type": "Feature Expansion",
            "intervention_description": "Added SSR, API routes, and image optimization",
            "planned_effort_days": 90,
            "predicted_value": 85,
            "predicted_probability": 0.7,
            "predicted_risk": 0.4,
            "start_date": "2016-10-25",
            "end_date": "2017-10-25",
            "after_state": {
                "stars": 50000,
                "forks": 5000,
                "contributors": 500
            },
            "outcome_metrics": {
                "actual_value": 90,
                "success": True,
                "actual_risk": 0.3
            },
            "actual_stars_delta": 49500,
            "actual_downloads_delta": 1000000,
            "actual_revenue_delta": 5000000,
            "actual_contributors_delta": 495
        },
        {
            "asset_id": "supabase/supabase",
            "asset_type": "github_repo",
            "asset_name": "supabase",
            "developer_id": "github:supabase",
            "developer_username": "supabase",
            "before_state": {
                "stars": 1000,
                "forks": 100,
                "contributors": 10,
                "language": "typescript",
                "category": "database"
            },
            "intervention_type": "SaaS Conversion",
            "intervention_description": "Converted open source Firebase alternative to SaaS platform",
            "planned_effort_days": 180,
            "predicted_value": 80,
            "predicted_probability": 0.6,
            "predicted_risk": 0.5,
            "start_date": "2020-01-01",
            "end_date": "2021-01-01",
            "after_state": {
                "stars": 50000,
                "forks": 3000,
                "contributors": 300
            },
            "outcome_metrics": {
                "actual_value": 85,
                "success": True,
                "actual_risk": 0.4
            },
            "actual_stars_delta": 49000,
            "actual_downloads_delta": 500000,
            "actual_revenue_delta": 10000000,
            "actual_contributors_delta": 290
        },
        {
            "asset_id": "langchain-ai/langchain",
            "asset_type": "github_repo",
            "asset_name": "langchain",
            "developer_id": "github:langchain-ai",
            "developer_username": "langchain-ai",
            "before_state": {
                "stars": 100,
                "forks": 20,
                "contributors": 3,
                "language": "python",
                "category": "ai"
            },
            "intervention_type": "AI Integration",
            "intervention_description": "Created LLM framework for AI application development",
            "planned_effort_days": 60,
            "predicted_value": 75,
            "predicted_probability": 0.65,
            "predicted_risk": 0.45,
            "start_date": "2022-10-01",
            "end_date": "2023-04-01",
            "after_state": {
                "stars": 75000,
                "forks": 10000,
                "contributors": 1000
            },
            "outcome_metrics": {
                "actual_value": 90,
                "success": True,
                "actual_risk": 0.3
            },
            "actual_stars_delta": 74900,
            "actual_downloads_delta": 2000000,
            "actual_revenue_delta": 15000000,
            "actual_contributors_delta": 997
        },
        {
            "asset_id": "tiangolo/fastapi",
            "asset_type": "github_repo",
            "asset_name": "fastapi",
            "developer_id": "github:tiangolo",
            "developer_username": "tiangolo",
            "before_state": {
                "stars": 500,
                "forks": 50,
                "contributors": 8,
                "language": "python",
                "category": "framework"
            },
            "intervention_type": "Modernization",
            "intervention_description": "Modern Python web framework with async support",
            "planned_effort_days": 45,
            "predicted_value": 70,
            "predicted_probability": 0.75,
            "predicted_risk": 0.3,
            "start_date": "2018-12-01",
            "end_date": "2019-06-01",
            "after_state": {
                "stars": 65000,
                "forks": 5000,
                "contributors": 400
            },
            "outcome_metrics": {
                "actual_value": 85,
                "success": True,
                "actual_risk": 0.25
            },
            "actual_stars_delta": 64500,
            "actual_downloads_delta": 5000000,
            "actual_revenue_delta": 2000000,
            "actual_contributors_delta": 392
        },
        {
            "asset_id": "oven-sh/bun",
            "asset_type": "github_repo",
            "asset_name": "bun",
            "developer_id": "github:oven-sh",
            "developer_username": "oven-sh",
            "before_state": {
                "stars": 1000,
                "forks": 100,
                "contributors": 15,
                "language": "zig",
                "category": "runtime"
            },
            "intervention_type": "Runtime Rewrite",
            "intervention_description": "Rewrote JavaScript runtime in Zig for performance",
            "planned_effort_days": 365,
            "predicted_value": 80,
            "predicted_probability": 0.5,
            "predicted_risk": 0.6,
            "start_date": "2022-07-01",
            "end_date": "2023-07-01",
            "after_state": {
                "stars": 45000,
                "forks": 2000,
                "contributors": 200
            },
            "outcome_metrics": {
                "actual_value": 75,
                "success": True,
                "actual_risk": 0.5
            },
            "actual_stars_delta": 44000,
            "actual_downloads_delta": 10000000,
            "actual_revenue_delta": 5000000,
            "actual_contributors_delta": 185
        },
        {
            "asset_id": "tailwindlabs/tailwindcss",
            "asset_type": "github_repo",
            "asset_name": "tailwindcss",
            "developer_id": "github:tailwindlabs",
            "developer_username": "tailwindlabs",
            "before_state": {
                "stars": 2000,
                "forks": 150,
                "contributors": 20,
                "language": "javascript",
                "category": "css"
            },
            "intervention_type": "Documentation Overhaul",
            "intervention_description": "Comprehensive documentation rewrite with examples",
            "planned_effort_days": 60,
            "predicted_value": 75,
            "predicted_probability": 0.8,
            "predicted_risk": 0.2,
            "start_date": "2019-05-01",
            "end_date": "2020-05-01",
            "after_state": {
                "stars": 70000,
                "forks": 4000,
                "contributors": 500
            },
            "outcome_metrics": {
                "actual_value": 80,
                "success": True,
                "actual_risk": 0.15
            },
            "actual_stars_delta": 68000,
            "actual_downloads_delta": 8000000,
            "actual_revenue_delta": 3000000,
            "actual_contributors_delta": 480
        },
        {
            "asset_id": "prisma/prisma",
            "asset_type": "github_repo",
            "asset_name": "prisma",
            "developer_id": "github:prisma",
            "developer_username": "prisma",
            "before_state": {
                "stars": 3000,
                "forks": 200,
                "contributors": 25,
                "language": "typescript",
                "category": "database"
            },
            "intervention_type": "Build System Modernization",
            "intervention_description": "Rewrote ORM with TypeScript and modern tooling",
            "planned_effort_days": 120,
            "predicted_value": 70,
            "predicted_probability": 0.7,
            "predicted_risk": 0.4,
            "start_date": "2019-01-01",
            "end_date": "2020-01-01",
            "after_state": {
                "stars": 35000,
                "forks": 2500,
                "contributors": 350
            },
            "outcome_metrics": {
                "actual_value": 75,
                "success": True,
                "actual_risk": 0.35
            },
            "actual_stars_delta": 32000,
            "actual_downloads_delta": 3000000,
            "actual_revenue_delta": 8000000,
            "actual_contributors_delta": 325
        },
        {
            "asset_id": "vitejs/vite",
            "asset_type": "github_repo",
            "asset_name": "vite",
            "developer_id": "github:vitejs",
            "developer_username": "vitejs",
            "before_state": {
                "stars": 1000,
                "forks": 80,
                "contributors": 10,
                "language": "typescript",
                "category": "build"
            },
            "intervention_type": "Build System Modernization",
            "intervention_description": "Modern build tool with HMR and native ESM",
            "planned_effort_days": 90,
            "predicted_value": 80,
            "predicted_probability": 0.75,
            "predicted_risk": 0.3,
            "start_date": "2020-04-01",
            "end_date": "2021-04-01",
            "after_state": {
                "stars": 60000,
                "forks": 5000,
                "contributors": 600
            },
            "outcome_metrics": {
                "actual_value": 85,
                "success": True,
                "actual_risk": 0.25
            },
            "actual_stars_delta": 59000,
            "actual_downloads_delta": 15000000,
            "actual_revenue_delta": 4000000,
            "actual_contributors_delta": 590
        },
        {
            "asset_id": "facebook/react",
            "asset_type": "github_repo",
            "asset_name": "react",
            "developer_id": "github:facebook",
            "developer_username": "facebook",
            "before_state": {
                "stars": 10000,
                "forks": 1000,
                "contributors": 100,
                "language": "javascript",
                "category": "framework"
            },
            "intervention_type": "Feature Expansion",
            "intervention_description": "Added Hooks API for state management",
            "planned_effort_days": 180,
            "predicted_value": 85,
            "predicted_probability": 0.8,
            "predicted_risk": 0.3,
            "start_date": "2018-02-01",
            "end_date": "2019-02-01",
            "after_state": {
                "stars": 200000,
                "forks": 40000,
                "contributors": 1500
            },
            "outcome_metrics": {
                "actual_value": 90,
                "success": True,
                "actual_risk": 0.2
            },
            "actual_stars_delta": 190000,
            "actual_downloads_delta": 50000000,
            "actual_revenue_delta": 0,
            "actual_contributors_delta": 1400
        },
        {
            "asset_id": "microsoft/typescript",
            "asset_type": "github_repo",
            "asset_name": "typescript",
            "developer_id": "github:microsoft",
            "developer_username": "microsoft",
            "before_state": {
                "stars": 5000,
                "forks": 500,
                "contributors": 50,
                "language": "typescript",
                "category": "language"
            },
            "intervention_type": "Feature Expansion",
            "intervention_description": "Added type inference and better tooling",
            "planned_effort_days": 365,
            "predicted_value": 75,
            "predicted_probability": 0.7,
            "predicted_risk": 0.4,
            "start_date": "2015-01-01",
            "end_date": "2017-01-01",
            "after_state": {
                "stars": 90000,
                "forks": 12000,
                "contributors": 1000
            },
            "outcome_metrics": {
                "actual_value": 80,
                "success": True,
                "actual_risk": 0.35
            },
            "actual_stars_delta": 85000,
            "actual_downloads_delta": 100000000,
            "actual_revenue_delta": 0,
            "actual_contributors_delta": 950
        },
        {
            "asset_id": "golang/go",
            "asset_type": "github_repo",
            "asset_name": "go",
            "developer_id": "github:golang",
            "developer_username": "golang",
            "before_state": {
                "stars": 10000,
                "forks": 1000,
                "contributors": 200,
                "language": "go",
                "category": "language"
            },
            "intervention_type": "Infrastructure Repositioning",
            "intervention_description": "Added modules and improved dependency management",
            "planned_effort_days": 365,
            "predicted_value": 70,
            "predicted_probability": 0.75,
            "predicted_risk": 0.35,
            "start_date": "2018-01-01",
            "end_date": "2020-01-01",
            "after_state": {
                "stars": 110000,
                "forks": 16000,
                "contributors": 2000
            },
            "outcome_metrics": {
                "actual_value": 75,
                "success": True,
                "actual_risk": 0.3
            },
            "actual_stars_delta": 100000,
            "actual_downloads_delta": 0,
            "actual_revenue_delta": 0,
            "actual_contributors_delta": 1800
        },
        {
            "asset_id": "rust-lang/rust",
            "asset_type": "github_repo",
            "asset_name": "rust",
            "developer_id": "github:rust-lang",
            "developer_username": "rust-lang",
            "before_state": {
                "stars": 5000,
                "forks": 500,
                "contributors": 100,
                "language": "rust",
                "category": "language"
            },
            "intervention_type": "Documentation Overhaul",
            "intervention_description": "Complete documentation rewrite with The Rust Book",
            "planned_effort_days": 180,
            "predicted_value": 80,
            "predicted_probability": 0.7,
            "predicted_risk": 0.4,
            "start_date": "2016-01-01",
            "end_date": "2017-01-01",
            "after_state": {
                "stars": 85000,
                "forks": 11000,
                "contributors": 3000
            },
            "outcome_metrics": {
                "actual_value": 85,
                "success": True,
                "actual_risk": 0.35
            },
            "actual_stars_delta": 80000,
            "actual_downloads_delta": 0,
            "actual_revenue_delta": 0,
            "actual_contributors_delta": 2900
        },
        {
            "asset_id": "docker/docker",
            "asset_type": "github_repo",
            "asset_name": "docker",
            "developer_id": "github:docker",
            "developer_username": "docker",
            "before_state": {
                "stars": 2000,
                "forks": 300,
                "contributors": 50,
                "language": "go",
                "category": "infrastructure"
            },
            "intervention_type": "Infrastructure Repositioning",
            "intervention_description": "Added Docker Compose and improved tooling",
            "planned_effort_days": 120,
            "predicted_value": 85,
            "predicted_probability": 0.8,
            "predicted_risk": 0.3,
            "start_date": "2014-01-01",
            "end_date": "2015-01-01",
            "after_state": {
                "stars": 66000,
                "forks": 19000,
                "contributors": 2000
            },
            "outcome_metrics": {
                "actual_value": 90,
                "success": True,
                "actual_risk": 0.25
            },
            "actual_stars_delta": 64000,
            "actual_downloads_delta": 0,
            "actual_revenue_delta": 50000000,
            "actual_contributors_delta": 1950
        },
        {
            "asset_id": "kubernetes/kubernetes",
            "asset_type": "github_repo",
            "asset_name": "kubernetes",
            "developer_id": "github:kubernetes",
            "developer_username": "kubernetes",
            "before_state": {
                "stars": 5000,
                "forks": 1000,
                "contributors": 200,
                "language": "go",
                "category": "infrastructure"
            },
            "intervention_type": "Community Building",
            "intervention_description": "Built CNCF and community governance",
            "planned_effort_days": 365,
            "predicted_value": 90,
            "predicted_probability": 0.7,
            "predicted_risk": 0.4,
            "start_date": "2015-01-01",
            "end_date": "2017-01-01",
            "after_state": {
                "stars": 100000,
                "forks": 38000,
                "contributors": 3000
            },
            "outcome_metrics": {
                "actual_value": 95,
                "success": True,
                "actual_risk": 0.3
            },
            "actual_stars_delta": 95000,
            "actual_downloads_delta": 0,
            "actual_revenue_delta": 0,
            "actual_contributors_delta": 2800
        },
        {
            "asset_id": "home-assistant/core",
            "asset_type": "github_repo",
            "asset_name": "home-assistant",
            "developer_id": "github:home-assistant",
            "developer_username": "home-assistant",
            "before_state": {
                "stars": 1000,
                "forks": 200,
                "contributors": 30,
                "language": "python",
                "category": "iot"
            },
            "intervention_type": "Feature Expansion",
            "intervention_description": "Added integrations and improved UI",
            "planned_effort_days": 180,
            "predicted_value": 70,
            "predicted_probability": 0.65,
            "predicted_risk": 0.45,
            "start_date": "2016-01-01",
            "end_date": "2018-01-01",
            "after_state": {
                "stars": 65000,
                "forks": 20000,
                "contributors": 2000
            },
            "outcome_metrics": {
                "actual_value": 75,
                "success": True,
                "actual_risk": 0.4
            },
            "actual_stars_delta": 64000,
            "actual_downloads_delta": 0,
            "actual_revenue_delta": 5000000,
            "actual_contributors_delta": 1970
        },
        {
            "asset_id": "facebook/relay",
            "asset_type": "github_repo",
            "asset_name": "relay",
            "developer_id": "github:facebook",
            "developer_username": "facebook",
            "before_state": {
                "stars": 8000,
                "forks": 600,
                "contributors": 80,
                "language": "javascript",
                "category": "framework"
            },
            "intervention_type": "Feature Expansion",
            "intervention_description": "Added concurrent mode and improved performance",
            "planned_effort_days": 180,
            "predicted_value": 75,
            "predicted_probability": 0.7,
            "predicted_risk": 0.4,
            "start_date": "2018-01-01",
            "end_date": "2019-01-01",
            "after_state": {
                "stars": 17000,
                "forks": 1800,
                "contributors": 150
            },
            "outcome_metrics": {
                "actual_value": 45,
                "success": False,
                "actual_risk": 0.6
            },
            "actual_stars_delta": 9000,
            "actual_downloads_delta": 500000,
            "actual_revenue_delta": 0,
            "actual_contributors_delta": 70
        },
        {
            "asset_id": "angular/angular",
            "asset_type": "github_repo",
            "asset_name": "angular",
            "developer_id": "github:angular",
            "developer_username": "angular",
            "before_state": {
                "stars": 20000,
                "forks": 5000,
                "contributors": 500,
                "language": "typescript",
                "category": "framework"
            },
            "intervention_type": "Build System Modernization",
            "intervention_description": "Migrated to Ivy compiler and improved build times",
            "planned_effort_days": 365,
            "predicted_value": 70,
            "predicted_probability": 0.6,
            "predicted_risk": 0.5,
            "start_date": "2018-11-01",
            "end_date": "2020-05-01",
            "after_state": {
                "stars": 88000,
                "forks": 24000,
                "contributors": 1500
            },
            "outcome_metrics": {
                "actual_value": 75,
                "success": True,
                "actual_risk": 0.45
            },
            "actual_stars_delta": 68000,
            "actual_downloads_delta": 20000000,
            "actual_revenue_delta": 0,
            "actual_contributors_delta": 1000
        },
        {
            "asset_id": "vuejs/vue",
            "asset_type": "github_repo",
            "asset_name": "vue",
            "developer_id": "github:vuejs",
            "developer_username": "vuejs",
            "before_state": {
                "stars": 3000,
                "forks": 400,
                "contributors": 50,
                "language": "javascript",
                "category": "framework"
            },
            "intervention_type": "Documentation Overhaul",
            "intervention_description": "Rewrote documentation and added examples",
            "planned_effort_days": 90,
            "predicted_value": 80,
            "predicted_probability": 0.8,
            "predicted_risk": 0.25,
            "start_date": "2016-01-01",
            "end_date": "2017-01-01",
            "after_state": {
                "stars": 200000,
                "forks": 33000,
                "contributors": 400
            },
            "outcome_metrics": {
                "actual_value": 90,
                "success": True,
                "actual_risk": 0.2
            },
            "actual_stars_delta": 197000,
            "actual_downloads_delta": 30000000,
            "actual_revenue_delta": 2000000,
            "actual_contributors_delta": 350
        },
        {
            "asset_id": "sveltejs/svelte",
            "asset_type": "github_repo",
            "asset_name": "svelte",
            "developer_id": "github:sveltejs",
            "developer_username": "sveltejs",
            "before_state": {
                "stars": 500,
                "forks": 50,
                "contributors": 20,
                "language": "javascript",
                "category": "framework"
            },
            "intervention_type": "Feature Expansion",
            "intervention_description": "Added SvelteKit for full-stack framework",
            "planned_effort_days": 180,
            "predicted_value": 75,
            "predicted_probability": 0.7,
            "predicted_risk": 0.4,
            "start_date": "2020-01-01",
            "end_date": "2021-01-01",
            "after_state": {
                "stars": 70000,
                "forks": 4000,
                "contributors": 800
            },
            "outcome_metrics": {
                "actual_value": 85,
                "success": True,
                "actual_risk": 0.3
            },
            "actual_stars_delta": 69500,
            "actual_downloads_delta": 5000000,
            "actual_revenue_delta": 1000000,
            "actual_contributors_delta": 780
        },
        {
            "asset_id": "nuxt/nuxt",
            "asset_type": "github_repo",
            "asset_name": "nuxt",
            "developer_id": "github:nuxt",
            "developer_username": "nuxt",
            "before_state": {
                "stars": 2000,
                "forks": 300,
                "contributors": 40,
                "language": "javascript",
                "category": "framework"
            },
            "intervention_type": "Build System Modernization",
            "intervention_description": "Rewrote with Nuxt 3 and Nitro engine",
            "planned_effort_days": 365,
            "predicted_value": 70,
            "predicted_probability": 0.65,
            "predicted_risk": 0.45,
            "start_date": "2020-01-01",
            "end_date": "2022-01-01",
            "after_state": {
                "stars": 48000,
                "forks": 4000,
                "contributors": 800
            },
            "outcome_metrics": {
                "actual_value": 75,
                "success": True,
                "actual_risk": 0.4
            },
            "actual_stars_delta": 46000,
            "actual_downloads_delta": 3000000,
            "actual_revenue_delta": 2000000,
            "actual_contributors_delta": 760
        },
        {
            "asset_id": "remix-run/remix",
            "asset_type": "github_repo",
            "asset_name": "remix",
            "developer_id": "github:remix-run",
            "developer_username": "remix-run",
            "before_state": {
                "stars": 1000,
                "forks": 100,
                "contributors": 15,
                "language": "typescript",
                "category": "framework"
            },
            "intervention_type": "Feature Expansion",
            "intervention_description": "Added nested routes and improved data loading",
            "planned_effort_days": 120,
            "predicted_value": 75,
            "predicted_probability": 0.7,
            "predicted_risk": 0.4,
            "start_date": "2021-01-01",
            "end_date": "2022-01-01",
            "after_state": {
                "stars": 25000,
                "forks": 2000,
                "contributors": 400
            },
            "outcome_metrics": {
                "actual_value": 80,
                "success": True,
                "actual_risk": 0.35
            },
            "actual_stars_delta": 24000,
            "actual_downloads_delta": 1000000,
            "actual_revenue_delta": 5000000,
            "actual_contributors_delta": 385
        },
        {
            "asset_id": "solidjs/solid",
            "asset_type": "github_repo",
            "asset_name": "solid",
            "developer_id": "github:solidjs",
            "developer_username": "solidjs",
            "before_state": {
                "stars": 200,
                "forks": 20,
                "contributors": 10,
                "language": "typescript",
                "category": "framework"
            },
            "intervention_type": "Feature Expansion",
            "intervention_description": "Added SolidStart for full-stack framework",
            "planned_effort_days": 90,
            "predicted_value": 65,
            "predicted_probability": 0.6,
            "predicted_risk": 0.5,
            "start_date": "2021-01-01",
            "end_date": "2022-01-01",
            "after_state": {
                "stars": 28000,
                "forks": 1500,
                "contributors": 300
            },
            "outcome_metrics": {
                "actual_value": 70,
                "success": True,
                "actual_risk": 0.45
            },
            "actual_stars_delta": 27800,
            "actual_downloads_delta": 500000,
            "actual_revenue_delta": 500000,
            "actual_contributors_delta": 290
        },
        {
            "asset_id": "denoland/deno",
            "asset_type": "github_repo",
            "asset_name": "deno",
            "developer_id": "github:denoland",
            "developer_username": "denoland",
            "before_state": {
                "stars": 5000,
                "forks": 300,
                "contributors": 50,
                "language": "rust",
                "category": "runtime"
            },
            "intervention_type": "Runtime Rewrite",
            "intervention_description": "Built secure TypeScript runtime with V8",
            "planned_effort_days": 365,
            "predicted_value": 70,
            "predicted_probability": 0.5,
            "predicted_risk": 0.6,
            "start_date": "2018-05-01",
            "end_date": "2020-05-01",
            "after_state": {
                "stars": 91000,
                "forks": 5000,
                "contributors": 1000
            },
            "outcome_metrics": {
                "actual_value": 75,
                "success": True,
                "actual_risk": 0.5
            },
            "actual_stars_delta": 86000,
            "actual_downloads_delta": 5000000,
            "actual_revenue_delta": 2000000,
            "actual_contributors_delta": 950
        },
        {
            "asset_id": "nodejs/node",
            "asset_type": "github_repo",
            "asset_name": "node",
            "developer_id": "github:nodejs",
            "developer_username": "nodejs",
            "before_state": {
                "stars": 10000,
                "forks": 2000,
                "contributors": 500,
                "language": "javascript",
                "category": "runtime"
            },
            "intervention_type": "Infrastructure Repositioning",
            "intervention_description": "Added ES modules and improved async/await",
            "planned_effort_days": 365,
            "predicted_value": 75,
            "predicted_probability": 0.8,
            "predicted_risk": 0.3,
            "start_date": "2015-01-01",
            "end_date": "2017-01-01",
            "after_state": {
                "stars": 98000,
                "forks": 26000,
                "contributors": 3000
            },
            "outcome_metrics": {
                "actual_value": 80,
                "success": True,
                "actual_risk": 0.25
            },
            "actual_stars_delta": 88000,
            "actual_downloads_delta": 0,
            "actual_revenue_delta": 0,
            "actual_contributors_delta": 2500
        },
        {
            "asset_id": "python/cpython",
            "asset_type": "github_repo",
            "asset_name": "python",
            "developer_id": "github:python",
            "developer_username": "python",
            "before_state": {
                "stars": 5000,
                "forks": 1000,
                "contributors": 200,
                "language": "python",
                "category": "language"
            },
            "intervention_type": "Feature Expansion",
            "intervention_description": "Added async/await and type hints",
            "planned_effort_days": 365,
            "predicted_value": 70,
            "predicted_probability": 0.75,
            "predicted_risk": 0.35,
            "start_date": "2015-01-01",
            "end_date": "2017-01-01",
            "after_state": {
                "stars": 56000,
                "forks": 15000,
                "contributors": 3000
            },
            "outcome_metrics": {
                "actual_value": 75,
                "success": True,
                "actual_risk": 0.3
            },
            "actual_stars_delta": 51000,
            "actual_downloads_delta": 0,
            "actual_revenue_delta": 0,
            "actual_contributors_delta": 2800
        },
        {
            "asset_id": "pallets/flask",
            "asset_type": "github_repo",
            "asset_name": "flask",
            "developer_id": "github:pallets",
            "developer_username": "pallets",
            "before_state": {
                "stars": 3000,
                "forks": 800,
                "contributors": 100,
                "language": "python",
                "category": "framework"
            },
            "intervention_type": "Documentation Overhaul",
            "intervention_description": "Rewrote documentation with modern examples",
            "planned_effort_days": 60,
            "predicted_value": 65,
            "predicted_probability": 0.7,
            "predicted_risk": 0.35,
            "start_date": "2015-01-01",
            "end_date": "2016-01-01",
            "after_state": {
                "stars": 63000,
                "forks": 16000,
                "contributors": 1000
            },
            "outcome_metrics": {
                "actual_value": 70,
                "success": True,
                "actual_risk": 0.3
            },
            "actual_stars_delta": 60000,
            "actual_downloads_delta": 100000000,
            "actual_revenue_delta": 0,
            "actual_contributors_delta": 900
        },
        {
            "asset_id": "django/django",
            "asset_type": "github_repo",
            "asset_name": "django",
            "developer_id": "github:django",
            "developer_username": "django",
            "before_state": {
                "stars": 5000,
                "forks": 1500,
                "contributors": 200,
                "language": "python",
                "category": "framework"
            },
            "intervention_type": "Feature Expansion",
            "intervention_description": "Added async views and improved ORM",
            "planned_effort_days": 180,
            "predicted_value": 70,
            "predicted_probability": 0.7,
            "predicted_risk": 0.4,
            "start_date": "2019-01-01",
            "end_date": "2020-01-01",
            "after_state": {
                "stars": 73000,
                "forks": 30000,
                "contributors": 2000
            },
            "outcome_metrics": {
                "actual_value": 75,
                "success": True,
                "actual_risk": 0.35
            },
            "actual_stars_delta": 68000,
            "actual_downloads_delta": 50000000,
            "actual_revenue_delta": 0,
            "actual_contributors_delta": 1800
        },
        {
            "asset_id": "tensorflow/tensorflow",
            "asset_type": "github_repo",
            "asset_name": "tensorflow",
            "developer_id": "github:tensorflow",
            "developer_username": "tensorflow",
            "before_state": {
                "stars": 10000,
                "forks": 5000,
                "contributors": 500,
                "language": "python",
                "category": "ai"
            },
            "intervention_type": "Feature Expansion",
            "intervention_description": "Added Keras integration and improved API",
            "planned_effort_days": 365,
            "predicted_value": 80,
            "predicted_probability": 0.75,
            "predicted_risk": 0.35,
            "start_date": "2017-01-01",
            "end_date": "2019-01-01",
            "after_state": {
                "stars": 175000,
                "forks": 88000,
                "contributors": 4000
            },
            "outcome_metrics": {
                "actual_value": 85,
                "success": True,
                "actual_risk": 0.3
            },
            "actual_stars_delta": 165000,
            "actual_downloads_delta": 500000000,
            "actual_revenue_delta": 0,
            "actual_contributors_delta": 3500
        },
        {
            "asset_id": "pytorch/pytorch",
            "asset_type": "github_repo",
            "asset_name": "pytorch",
            "developer_id": "github:pytorch",
            "developer_username": "pytorch",
            "before_state": {
                "stars": 5000,
                "forks": 1000,
                "contributors": 200,
                "language": "python",
                "category": "ai"
            },
            "intervention_type": "Feature Expansion",
            "intervention_description": "Added distributed training and improved performance",
            "planned_effort_days": 365,
            "predicted_value": 85,
            "predicted_probability": 0.8,
            "predicted_risk": 0.3,
            "start_date": "2017-01-01",
            "end_date": "2019-01-01",
            "after_state": {
                "stars": 72000,
                "forks": 20000,
                "contributors": 2500
            },
            "outcome_metrics": {
                "actual_value": 90,
                "success": True,
                "actual_risk": 0.25
            },
            "actual_stars_delta": 67000,
            "actual_downloads_delta": 200000000,
            "actual_revenue_delta": 0,
            "actual_contributors_delta": 2300
        },
        {
            "asset_id": "huggingface/transformers",
            "asset_type": "github_repo",
            "asset_name": "transformers",
            "developer_id": "github:huggingface",
            "developer_username": "huggingface",
            "before_state": {
                "stars": 1000,
                "forks": 200,
                "contributors": 30,
                "language": "python",
                "category": "ai"
            },
            "intervention_type": "AI Integration",
            "intervention_description": "Created unified API for transformer models",
            "planned_effort_days": 180,
            "predicted_value": 85,
            "predicted_probability": 0.75,
            "predicted_risk": 0.35,
            "start_date": "2019-01-01",
            "end_date": "2020-01-01",
            "after_state": {
                "stars": 120000,
                "forks": 24000,
                "contributors": 1000
            },
            "outcome_metrics": {
                "actual_value": 90,
                "success": True,
                "actual_risk": 0.3
            },
            "actual_stars_delta": 119000,
            "actual_downloads_delta": 50000000,
            "actual_revenue_delta": 10000000,
            "actual_contributors_delta": 970
        },
        {
            "asset_id": "openai/gym",
            "asset_type": "github_repo",
            "asset_name": "gym",
            "developer_id": "github:openai",
            "developer_username": "openai",
            "before_state": {
                "stars": 500,
                "forks": 100,
                "contributors": 20,
                "language": "python",
                "category": "ai"
            },
            "intervention_type": "Feature Expansion",
            "intervention_description": "Added new environments and improved API",
            "planned_effort_days": 90,
            "predicted_value": 70,
            "predicted_probability": 0.7,
            "predicted_risk": 0.4,
            "start_date": "2017-01-01",
            "end_date": "2018-01-01",
            "after_state": {
                "stars": 30000,
                "forks": 8000,
                "contributors": 500
            },
            "outcome_metrics": {
                "actual_value": 75,
                "success": True,
                "actual_risk": 0.35
            },
            "actual_stars_delta": 29500,
            "actual_downloads_delta": 10000000,
            "actual_revenue_delta": 0,
            "actual_contributors_delta": 480
        },
        {
            "asset_id": "postgres/postgres",
            "asset_type": "github_repo",
            "asset_name": "postgres",
            "developer_id": "github:postgres",
            "developer_username": "postgres",
            "before_state": {
                "stars": 2000,
                "forks": 500,
                "contributors": 100,
                "language": "c",
                "category": "database"
            },
            "intervention_type": "Feature Expansion",
            "intervention_description": "Added JSON support and improved performance",
            "planned_effort_days": 365,
            "predicted_value": 75,
            "predicted_probability": 0.8,
            "predicted_risk": 0.3,
            "start_date": "2014-01-01",
            "end_date": "2016-01-01",
            "after_state": {
                "stars": 14000,
                "forks": 4000,
                "contributors": 1000
            },
            "outcome_metrics": {
                "actual_value": 80,
                "success": True,
                "actual_risk": 0.25
            },
            "actual_stars_delta": 12000,
            "actual_downloads_delta": 0,
            "actual_revenue_delta": 0,
            "actual_contributors_delta": 900
        },
        {
            "asset_id": "mongodb/mongo",
            "asset_type": "github_repo",
            "asset_name": "mongodb",
            "developer_id": "github:mongodb",
            "developer_username": "mongodb",
            "before_state": {
                "stars": 3000,
                "forks": 800,
                "contributors": 150,
                "language": "c++",
                "category": "database"
            },
            "intervention_type": "Feature Expansion",
            "intervention_description": "Added transactions and improved aggregation",
            "planned_effort_days": 365,
            "predicted_value": 70,
            "predicted_probability": 0.7,
            "predicted_risk": 0.4,
            "start_date": "2016-01-01",
            "end_date": "2018-01-01",
            "after_state": {
                "stars": 25000,
                "forks": 6000,
                "contributors": 1000
            },
            "outcome_metrics": {
                "actual_value": 75,
                "success": True,
                "actual_risk": 0.35
            },
            "actual_stars_delta": 22000,
            "actual_downloads_delta": 0,
            "actual_revenue_delta": 50000000,
            "actual_contributors_delta": 850
        },
        {
            "asset_id": "redis/redis",
            "asset_type": "github_repo",
            "asset_name": "redis",
            "developer_id": "github:redis",
            "developer_username": "redis",
            "before_state": {
                "stars": 5000,
                "forks": 1000,
                "contributors": 200,
                "language": "c",
                "category": "database"
            },
            "intervention_type": "Feature Expansion",
            "intervention_description": "Added modules and improved clustering",
            "planned_effort_days": 180,
            "predicted_value": 70,
            "predicted_probability": 0.75,
            "predicted_risk": 0.35,
            "start_date": "2015-01-01",
            "end_date": "2016-01-01",
            "after_state": {
                "stars": 62000,
                "forks": 23000,
                "contributors": 1500
            },
            "outcome_metrics": {
                "actual_value": 75,
                "success": True,
                "actual_risk": 0.3
            },
            "actual_stars_delta": 57000,
            "actual_downloads_delta": 0,
            "actual_revenue_delta": 0,
            "actual_contributors_delta": 1300
        },
        {
            "asset_id": "elastic/elasticsearch",
            "asset_type": "github_repo",
            "asset_name": "elasticsearch",
            "developer_id": "github:elastic",
            "developer_username": "elastic",
            "before_state": {
                "stars": 3000,
                "forks": 600,
                "contributors": 100,
                "language": "java",
                "category": "database"
            },
            "intervention_type": "Feature Expansion",
            "intervention_description": "Added machine learning features and improved scalability",
            "planned_effort_days": 365,
            "predicted_value": 75,
            "predicted_probability": 0.7,
            "predicted_risk": 0.4,
            "start_date": "2015-01-01",
            "end_date": "2017-01-01",
            "after_state": {
                "stars": 65000,
                "forks": 24000,
                "contributors": 2000
            },
            "outcome_metrics": {
                "actual_value": 80,
                "success": True,
                "actual_risk": 0.35
            },
            "actual_stars_delta": 62000,
            "actual_downloads_delta": 0,
            "actual_revenue_delta": 200000000,
            "actual_contributors_delta": 1900
        },
        {
            "asset_id": "apache/spark",
            "asset_type": "github_repo",
            "asset_name": "spark",
            "developer_id": "github:apache",
            "developer_username": "apache",
            "before_state": {
                "stars": 2000,
                "forks": 1000,
                "contributors": 300,
                "language": "scala",
                "category": "data"
            },
            "intervention_type": "Feature Expansion",
            "intervention_description": "Added structured streaming and improved performance",
            "planned_effort_days": 365,
            "predicted_value": 70,
            "predicted_probability": 0.7,
            "predicted_risk": 0.4,
            "start_date": "2016-01-01",
            "end_date": "2018-01-01",
            "after_state": {
                "stars": 36000,
                "forks": 28000,
                "contributors": 2000
            },
            "outcome_metrics": {
                "actual_value": 75,
                "success": True,
                "actual_risk": 0.35
            },
            "actual_stars_delta": 34000,
            "actual_downloads_delta": 0,
            "actual_revenue_delta": 0,
            "actual_contributors_delta": 1700
        },
        {
            "asset_id": "databricks/delta",
            "asset_type": "github_repo",
            "asset_name": "delta",
            "developer_id": "github:databricks",
            "developer_username": "databricks",
            "before_state": {
                "stars": 500,
                "forks": 100,
                "contributors": 30,
                "language": "scala",
                "category": "data"
            },
            "intervention_type": "Feature Expansion",
            "intervention_description": "Added ACID transactions and time travel",
            "planned_effort_days": 180,
            "predicted_value": 75,
            "predicted_probability": 0.7,
            "predicted_risk": 0.4,
            "start_date": "2019-01-01",
            "end_date": "2020-01-01",
            "after_state": {
                "stars": 6000,
                "forks": 1300,
                "contributors": 400
            },
            "outcome_metrics": {
                "actual_value": 80,
                "success": True,
                "actual_risk": 0.35
            },
            "actual_stars_delta": 5500,
            "actual_downloads_delta": 0,
            "actual_revenue_delta": 50000000,
            "actual_contributors_delta": 370
        },
        {
            "asset_id": "grafana/grafana",
            "asset_type": "github_repo",
            "asset_name": "grafana",
            "developer_id": "github:grafana",
            "developer_username": "grafana",
            "before_state": {
                "stars": 5000,
                "forks": 800,
                "contributors": 200,
                "language": "go",
                "category": "monitoring"
            },
            "intervention_type": "Feature Expansion",
            "intervention_description": "Added panels, plugins, and improved UI",
            "planned_effort_days": 180,
            "predicted_value": 75,
            "predicted_probability": 0.75,
            "predicted_risk": 0.35,
            "start_date": "2015-01-01",
            "end_date": "2017-01-01",
            "after_state": {
                "stars": 57000,
                "forks": 11000,
                "contributors": 2000
            },
            "outcome_metrics": {
                "actual_value": 80,
                "success": True,
                "actual_risk": 0.3
            },
            "actual_stars_delta": 52000,
            "actual_downloads_delta": 0,
            "actual_revenue_delta": 50000000,
            "actual_contributors_delta": 1800
        },
        {
            "asset_id": "prometheus/prometheus",
            "asset_type": "github_repo",
            "asset_name": "prometheus",
            "developer_id": "github:prometheus",
            "developer_username": "prometheus",
            "before_state": {
                "stars": 2000,
                "forks": 400,
                "contributors": 100,
                "language": "go",
                "category": "monitoring"
            },
            "intervention_type": "Community Building",
            "intervention_description": "Built CNCF and community governance",
            "planned_effort_days": 365,
            "predicted_value": 85,
            "predicted_probability": 0.7,
            "predicted_risk": 0.4,
            "start_date": "2016-01-01",
            "end_date": "2018-01-01",
            "after_state": {
                "stars": 50000,
                "forks": 8500,
                "contributors": 1000
            },
            "outcome_metrics": {
                "actual_value": 90,
                "success": True,
                "actual_risk": 0.3
            },
            "actual_stars_delta": 48000,
            "actual_downloads_delta": 0,
            "actual_revenue_delta": 0,
            "actual_contributors_delta": 900
        },
        {
            "asset_id": "hashicorp/terraform",
            "asset_type": "github_repo",
            "asset_name": "terraform",
            "developer_id": "github:hashicorp",
            "developer_username": "hashicorp",
            "before_state": {
                "stars": 3000,
                "forks": 800,
                "contributors": 150,
                "language": "go",
                "category": "infrastructure"
            },
            "intervention_type": "Feature Expansion",
            "intervention_description": "Added modules and state management",
            "planned_effort_days": 180,
            "predicted_value": 80,
            "predicted_probability": 0.75,
            "predicted_risk": 0.35,
            "start_date": "2015-01-01",
            "end_date": "2017-01-01",
            "after_state": {
                "stars": 39000,
                "forks": 9000,
                "contributors": 2000
            },
            "outcome_metrics": {
                "actual_value": 85,
                "success": True,
                "actual_risk": 0.3
            },
            "actual_stars_delta": 36000,
            "actual_downloads_delta": 0,
            "actual_revenue_delta": 100000000,
            "actual_contributors_delta": 1850
        },
        {
            "asset_id": "hashicorp/vault",
            "asset_type": "github_repo",
            "asset_name": "vault",
            "developer_id": "github:hashicorp",
            "developer_username": "hashicorp",
            "before_state": {
                "stars": 1000,
                "forks": 200,
                "contributors": 50,
                "language": "go",
                "category": "security"
            },
            "intervention_type": "Feature Expansion",
            "intervention_description": "Added secrets engines and improved UI",
            "planned_effort_days": 180,
            "predicted_value": 75,
            "predicted_probability": 0.7,
            "predicted_risk": 0.4,
            "start_date": "2015-01-01",
            "end_date": "2017-01-01",
            "after_state": {
                "stars": 28000,
                "forks": 4000,
                "contributors": 1000
            },
            "outcome_metrics": {
                "actual_value": 80,
                "success": True,
                "actual_risk": 0.35
            },
            "actual_stars_delta": 27000,
            "actual_downloads_delta": 0,
            "actual_revenue_delta": 50000000,
            "actual_contributors_delta": 950
        },
        {
            "asset_id": "envoyproxy/envoy",
            "asset_type": "github_repo",
            "asset_name": "envoy",
            "developer_id": "github:envoyproxy",
            "developer_username": "envoyproxy",
            "before_state": {
                "stars": 500,
                "forks": 100,
                "contributors": 30,
                "language": "c++",
                "category": "infrastructure"
            },
            "intervention_type": "Community Building",
            "intervention_description": "Built CNCF and community governance",
            "planned_effort_days": 365,
            "predicted_value": 85,
            "predicted_probability": 0.7,
            "predicted_risk": 0.4,
            "start_date": "2016-01-01",
            "end_date": "2018-01-01",
            "after_state": {
                "stars": 22000,
                "forks": 4000,
                "contributors": 1000
            },
            "outcome_metrics": {
                "actual_value": 90,
                "success": True,
                "actual_risk": 0.3
            },
            "actual_stars_delta": 21500,
            "actual_downloads_delta": 0,
            "actual_revenue_delta": 0,
            "actual_contributors_delta": 970
        },
        {
            "asset_id": "istio/istio",
            "asset_type": "github_repo",
            "asset_name": "istio",
            "developer_id": "github:istio",
            "developer_username": "istio",
            "before_state": {
                "stars": 1000,
                "forks": 200,
                "contributors": 50,
                "language": "go",
                "category": "infrastructure"
            },
            "intervention_type": "Community Building",
            "intervention_description": "Built CNCF and community governance",
            "planned_effort_days": 365,
            "predicted_value": 80,
            "predicted_probability": 0.65,
            "predicted_risk": 0.5,
            "start_date": "2017-01-01",
            "end_date": "2019-01-01",
            "after_state": {
                "stars": 34000,
                "forks": 7000,
                "contributors": 1500
            },
            "outcome_metrics": {
                "actual_value": 85,
                "success": True,
                "actual_risk": 0.4
            },
            "actual_stars_delta": 33000,
            "actual_downloads_delta": 0,
            "actual_revenue_delta": 0,
            "actual_contributors_delta": 1450
        },
        {
            "asset_id": "argoproj/argo-cd",
            "asset_type": "github_repo",
            "asset_name": "argo-cd",
            "developer_id": "github:argoproj",
            "developer_username": "argoproj",
            "before_state": {
                "stars": 500,
                "forks": 100,
                "contributors": 30,
                "language": "go",
                "category": "infrastructure"
            },
            "intervention_type": "Feature Expansion",
            "intervention_description": "Added sync waves and improved UI",
            "planned_effort_days": 120,
            "predicted_value": 75,
            "predicted_probability": 0.7,
            "predicted_risk": 0.4,
            "start_date": "2018-01-01",
            "end_date": "2019-01-01",
            "after_state": {
                "stars": 15000,
                "forks": 4000,
                "contributors": 500
            },
            "outcome_metrics": {
                "actual_value": 80,
                "success": True,
                "actual_risk": 0.35
            },
            "actual_stars_delta": 14500,
            "actual_downloads_delta": 0,
            "actual_revenue_delta": 10000000,
            "actual_contributors_delta": 470
        },
        {
            "asset_id": "crossplane/crossplane",
            "asset_type": "github_repo",
            "asset_name": "crossplane",
            "developer_id": "github:crossplane",
            "developer_username": "crossplane",
            "before_state": {
                "stars": 200,
                "forks": 50,
                "contributors": 20,
                "language": "go",
                "category": "infrastructure"
            },
            "intervention_type": "Community Building",
            "intervention_description": "Built CNCF and community governance",
            "planned_effort_days": 180,
            "predicted_value": 65,
            "predicted_probability": 0.6,
            "predicted_risk": 0.5,
            "start_date": "2018-01-01",
            "end_date": "2019-01-01",
            "after_state": {
                "stars": 8000,
                "forks": 800,
                "contributors": 200
            },
            "outcome_metrics": {
                "actual_value": 70,
                "success": True,
                "actual_risk": 0.45
            },
            "actual_stars_delta": 7800,
            "actual_downloads_delta": 0,
            "actual_revenue_delta": 5000000,
            "actual_contributors_delta": 180
        },
        {
            "asset_id": "open-telemetry/opentelemetry",
            "asset_type": "github_repo",
            "asset_name": "opentelemetry",
            "developer_id": "github:open-telemetry",
            "developer_username": "open-telemetry",
            "before_state": {
                "stars": 500,
                "forks": 100,
                "contributors": 50,
                "language": "go",
                "category": "monitoring"
            },
            "intervention_type": "Community Building",
            "intervention_description": "Built CNCF and community governance",
            "planned_effort_days": 365,
            "predicted_value": 80,
            "predicted_probability": 0.7,
            "predicted_risk": 0.4,
            "start_date": "2019-01-01",
            "end_date": "2021-01-01",
            "after_state": {
                "stars": 3500,
                "forks": 800,
                "contributors": 500
            },
            "outcome_metrics": {
                "actual_value": 70,
                "success": True,
                "actual_risk": 0.45
            },
            "actual_stars_delta": 3000,
            "actual_downloads_delta": 0,
            "actual_revenue_delta": 0,
            "actual_contributors_delta": 450
        },
        {
            "asset_id": "jaegertracing/jaeger",
            "asset_type": "github_repo",
            "asset_name": "jaeger",
            "developer_id": "github:jaegertracing",
            "developer_username": "jaegertracing",
            "before_state": {
                "stars": 1000,
                "forks": 200,
                "contributors": 50,
                "language": "go",
                "category": "monitoring"
            },
            "intervention_type": "Community Building",
            "intervention_description": "Built CNCF and community governance",
            "planned_effort_days": 180,
            "predicted_value": 75,
            "predicted_probability": 0.7,
            "predicted_risk": 0.4,
            "start_date": "2017-01-01",
            "end_date": "2018-01-01",
            "after_state": {
                "stars": 18000,
                "forks": 2100,
                "contributors": 500
            },
            "outcome_metrics": {
                "actual_value": 80,
                "success": True,
                "actual_risk": 0.35
            },
            "actual_stars_delta": 17000,
            "actual_downloads_delta": 0,
            "actual_revenue_delta": 0,
            "actual_contributors_delta": 450
        },
        {
            "asset_id": "linkerd/linkerd2",
            "asset_type": "github_repo",
            "asset_name": "linkerd",
            "developer_id": "github:linkerd",
            "developer_username": "linkerd",
            "before_state": {
                "stars": 1000,
                "forks": 200,
                "contributors": 50,
                "language": "rust",
                "category": "infrastructure"
            },
            "intervention_type": "Community Building",
            "intervention_description": "Built CNCF and community governance",
            "planned_effort_days": 180,
            "predicted_value": 70,
            "predicted_probability": 0.65,
            "predicted_risk": 0.5,
            "start_date": "2017-01-01",
            "end_date": "2018-01-01",
            "after_state": {
                "stars": 10000,
                "forks": 1300,
                "contributors": 300
            },
            "outcome_metrics": {
                "actual_value": 75,
                "success": True,
                "actual_risk": 0.45
            },
            "actual_stars_delta": 9000,
            "actual_downloads_delta": 0,
            "actual_revenue_delta": 0,
            "actual_contributors_delta": 250
        },
        {
            "asset_id": "cilium/cilium",
            "asset_type": "github_repo",
            "asset_name": "cilium",
            "developer_id": "github:cilium",
            "developer_username": "cilium",
            "before_state": {
                "stars": 500,
                "forks": 100,
                "contributors": 30,
                "language": "go",
                "category": "infrastructure"
            },
            "intervention_type": "Community Building",
            "intervention_description": "Built CNCF and community governance",
            "planned_effort_days": 180,
            "predicted_value": 70,
            "predicted_probability": 0.65,
            "predicted_risk": 0.5,
            "start_date": "2017-01-01",
            "end_date": "2018-01-01",
            "after_state": {
                "stars": 17000,
                "forks": 2500,
                "contributors": 500
            },
            "outcome_metrics": {
                "actual_value": 75,
                "success": True,
                "actual_risk": 0.45
            },
            "actual_stars_delta": 16500,
            "actual_downloads_delta": 0,
            "actual_revenue_delta": 20000000,
            "actual_contributors_delta": 470
        },
        {
            "asset_id": "strapi/strapi",
            "asset_type": "github_repo",
            "asset_name": "strapi",
            "developer_id": "github:strapi",
            "developer_username": "strapi",
            "before_state": {
                "stars": 1000,
                "forks": 200,
                "contributors": 30,
                "language": "javascript",
                "category": "cms"
            },
            "intervention_type": "SaaS Conversion",
            "intervention_description": "Converted to SaaS with cloud hosting",
            "planned_effort_days": 180,
            "predicted_value": 70,
            "predicted_probability": 0.6,
            "predicted_risk": 0.5,
            "start_date": "2019-01-01",
            "end_date": "2020-01-01",
            "after_state": {
                "stars": 56000,
                "forks": 7000,
                "contributors": 1000
            },
            "outcome_metrics": {
                "actual_value": 75,
                "success": True,
                "actual_risk": 0.45
            },
            "actual_stars_delta": 55000,
            "actual_downloads_delta": 5000000,
            "actual_revenue_delta": 10000000,
            "actual_contributors_delta": 970
        },
        {
            "asset_id": "directus/directus",
            "asset_type": "github_repo",
            "asset_name": "directus",
            "developer_id": "github:directus",
            "developer_username": "directus",
            "before_state": {
                "stars": 500,
                "forks": 100,
                "contributors": 20,
                "language": "javascript",
                "category": "cms"
            },
            "intervention_type": "SaaS Conversion",
            "intervention_description": "Converted to SaaS with cloud hosting",
            "planned_effort_days": 120,
            "predicted_value": 65,
            "predicted_probability": 0.6,
            "predicted_risk": 0.5,
            "start_date": "2019-01-01",
            "end_date": "2020-01-01",
            "after_state": {
                "stars": 23000,
                "forks": 1500,
                "contributors": 400
            },
            "outcome_metrics": {
                "actual_value": 70,
                "success": True,
                "actual_risk": 0.45
            },
            "actual_stars_delta": 22500,
            "actual_downloads_delta": 1000000,
            "actual_revenue_delta": 5000000,
            "actual_contributors_delta": 380
        },
        {
            "asset_id": "kestra-io/kestra",
            "asset_type": "github_repo",
            "asset_name": "kestra",
            "developer_id": "github:kestra-io",
            "developer_username": "kestra-io",
            "before_state": {
                "stars": 100,
                "forks": 20,
                "contributors": 10,
                "language": "java",
                "category": "workflow"
            },
            "intervention_type": "Feature Expansion",
            "intervention_description": "Added UI and improved workflow editor",
            "planned_effort_days": 90,
            "predicted_value": 65,
            "predicted_probability": 0.65,
            "predicted_risk": 0.45,
            "start_date": "2021-01-01",
            "end_date": "2022-01-01",
            "after_state": {
                "stars": 5000,
                "forks": 300,
                "contributors": 100
            },
            "outcome_metrics": {
                "actual_value": 70,
                "success": True,
                "actual_risk": 0.4
            },
            "actual_stars_delta": 4900,
            "actual_downloads_delta": 100000,
            "actual_revenue_delta": 2000000,
            "actual_contributors_delta": 90
        },
        {
            "asset_id": "apache/airflow",
            "asset_type": "github_repo",
            "asset_name": "airflow",
            "developer_id": "github:apache",
            "developer_username": "apache",
            "before_state": {
                "stars": 2000,
                "forks": 800,
                "contributors": 200,
                "language": "python",
                "category": "workflow"
            },
            "intervention_type": "Feature Expansion",
            "intervention_description": "Added DAG builder and improved UI",
            "planned_effort_days": 180,
            "predicted_value": 75,
            "predicted_probability": 0.7,
            "predicted_risk": 0.4,
            "start_date": "2018-01-01",
            "end_date": "2019-01-01",
            "after_state": {
                "stars": 30000,
                "forks": 12000,
                "contributors": 2000
            },
            "outcome_metrics": {
                "actual_value": 80,
                "success": True,
                "actual_risk": 0.35
            },
            "actual_stars_delta": 28000,
            "actual_downloads_delta": 50000000,
            "actual_revenue_delta": 0,
            "actual_contributors_delta": 1800
        },
        {
            "asset_id": "prefecthq/prefect",
            "asset_type": "github_repo",
            "asset_name": "prefect",
            "developer_id": "github:prefecthq",
            "developer_username": "prefecthq",
            "before_state": {
                "stars": 500,
                "forks": 100,
                "contributors": 30,
                "language": "python",
                "category": "workflow"
            },
            "intervention_type": "SaaS Conversion",
            "intervention_description": "Converted to SaaS with cloud hosting",
            "planned_effort_days": 120,
            "predicted_value": 70,
            "predicted_probability": 0.6,
            "predicted_risk": 0.5,
            "start_date": "2020-01-01",
            "end_date": "2021-01-01",
            "after_state": {
                "stars": 14000,
                "forks": 1500,
                "contributors": 500
            },
            "outcome_metrics": {
                "actual_value": 75,
                "success": True,
                "actual_risk": 0.45
            },
            "actual_stars_delta": 13500,
            "actual_downloads_delta": 5000000,
            "actual_revenue_delta": 20000000,
            "actual_contributors_delta": 470
        },
        {
            "asset_id": "dagster-io/dagster",
            "asset_type": "github_repo",
            "asset_name": "dagster",
            "developer_id": "github:dagster-io",
            "developer_username": "dagster-io",
            "before_state": {
                "stars": 200,
                "forks": 50,
                "contributors": 20,
                "language": "python",
                "category": "workflow"
            },
            "intervention_type": "Feature Expansion",
            "intervention_description": "Added asset-oriented programming and improved UI",
            "planned_effort_days": 180,
            "predicted_value": 65,
            "predicted_probability": 0.6,
            "predicted_risk": 0.5,
            "start_date": "2019-01-01",
            "end_date": "2020-01-01",
            "after_state": {
                "stars": 9000,
                "forks": 1000,
                "contributors": 300
            },
            "outcome_metrics": {
                "actual_value": 70,
                "success": True,
                "actual_risk": 0.45
            },
            "actual_stars_delta": 8800,
            "actual_downloads_delta": 1000000,
            "actual_revenue_delta": 10000000,
            "actual_contributors_delta": 280
        },
        {
            "asset_id": "n8n-io/n8n",
            "asset_type": "github_repo",
            "asset_name": "n8n",
            "developer_id": "github:n8n-io",
            "developer_username": "n8n-io",
            "before_state": {
                "stars": 500,
                "forks": 100,
                "contributors": 30,
                "language": "typescript",
                "category": "workflow"
            },
            "intervention_type": "SaaS Conversion",
            "intervention_description": "Converted to SaaS with cloud hosting",
            "planned_effort_days": 120,
            "predicted_value": 70,
            "predicted_probability": 0.6,
            "predicted_risk": 0.5,
            "start_date": "2020-01-01",
            "end_date": "2021-01-01",
            "after_state": {
                "stars": 38000,
                "forks": 4000,
                "contributors": 700
            },
            "outcome_metrics": {
                "actual_value": 75,
                "success": True,
                "actual_risk": 0.45
            },
            "actual_stars_delta": 37500,
            "actual_downloads_delta": 2000000,
            "actual_revenue_delta": 10000000,
            "actual_contributors_delta": 670
        },
        {
            "asset_id": "microsoft/playwright",
            "asset_type": "github_repo",
            "asset_name": "playwright",
            "developer_id": "github:microsoft",
            "developer_username": "microsoft",
            "before_state": {
                "stars": 1000,
                "forks": 200,
                "contributors": 50,
                "language": "typescript",
                "category": "testing"
            },
            "intervention_type": "Feature Expansion",
            "intervention_description": "Added cross-browser support and improved API",
            "planned_effort_days": 180,
            "predicted_value": 80,
            "predicted_probability": 0.75,
            "predicted_risk": 0.35,
            "start_date": "2020-01-01",
            "end_date": "2021-01-01",
            "after_state": {
                "stars": 58000,
                "forks": 3200,
                "contributors": 600
            },
            "outcome_metrics": {
                "actual_value": 85,
                "success": True,
                "actual_risk": 0.3
            },
            "actual_stars_delta": 57000,
            "actual_downloads_delta": 50000000,
            "actual_revenue_delta": 0,
            "actual_contributors_delta": 550
        },
        {
            "asset_id": "cypress-io/cypress",
            "asset_type": "github_repo",
            "asset_name": "cypress",
            "developer_id": "github:cypress-io",
            "developer_username": "cypress-io",
            "before_state": {
                "stars": 2000,
                "forks": 300,
                "contributors": 80,
                "language": "javascript",
                "category": "testing"
            },
            "intervention_type": "Feature Expansion",
            "intervention_description": "Added component testing and improved performance",
            "planned_effort_days": 180,
            "predicted_value": 75,
            "predicted_probability": 0.7,
            "predicted_risk": 0.4,
            "start_date": "2018-01-01",
            "end_date": "2019-01-01",
            "after_state": {
                "stars": 44000,
                "forks": 3000,
                "contributors": 800
            },
            "outcome_metrics": {
                "actual_value": 80,
                "success": True,
                "actual_risk": 0.35
            },
            "actual_stars_delta": 42000,
            "actual_downloads_delta": 50000000,
            "actual_revenue_delta": 20000000,
            "actual_contributors_delta": 720
        },
        {
            "asset_id": "testing-library/react-testing-library",
            "asset_type": "github_repo",
            "asset_name": "react-testing-library",
            "developer_id": "github:testing-library",
            "developer_username": "testing-library",
            "before_state": {
                "stars": 500,
                "forks": 100,
                "contributors": 30,
                "language": "javascript",
                "category": "testing"
            },
            "intervention_type": "Documentation Overhaul",
            "intervention_description": "Rewrote documentation with best practices",
            "planned_effort_days": 60,
            "predicted_value": 75,
            "predicted_probability": 0.8,
            "predicted_risk": 0.25,
            "start_date": "2018-01-01",
            "end_date": "2019-01-01",
            "after_state": {
                "stars": 18000,
                "forks": 1500,
                "contributors": 400
            },
            "outcome_metrics": {
                "actual_value": 80,
                "success": True,
                "actual_risk": 0.2
            },
            "actual_stars_delta": 17500,
            "actual_downloads_delta": 50000000,
            "actual_revenue_delta": 0,
            "actual_contributors_delta": 370
        },
        {
            "asset_id": "vitest-dev/vitest",
            "asset_type": "github_repo",
            "asset_name": "vitest",
            "developer_id": "github:vitest-dev",
            "developer_username": "vitest-dev",
            "before_state": {
                "stars": 500,
                "forks": 50,
                "contributors": 20,
                "language": "typescript",
                "category": "testing"
            },
            "intervention_type": "Feature Expansion",
            "intervention_description": "Added UI mode and improved performance",
            "planned_effort_days": 90,
            "predicted_value": 75,
            "predicted_probability": 0.7,
            "predicted_risk": 0.4,
            "start_date": "2021-01-01",
            "end_date": "2022-01-01",
            "after_state": {
                "stars": 11000,
                "forks": 800,
                "contributors": 400
            },
            "outcome_metrics": {
                "actual_value": 80,
                "success": True,
                "actual_risk": 0.35
            },
            "actual_stars_delta": 10500,
            "actual_downloads_delta": 20000000,
            "actual_revenue_delta": 0,
            "actual_contributors_delta": 380
        },
        {
            "asset_id": "jestjs/jest",
            "asset_type": "github_repo",
            "asset_name": "jest",
            "developer_id": "github:jestjs",
            "developer_username": "jestjs",
            "before_state": {
                "stars": 5000,
                "forks": 500,
                "contributors": 100,
                "language": "javascript",
                "category": "testing"
            },
            "intervention_type": "Feature Expansion",
            "intervention_description": "Added watch mode and improved performance",
            "planned_effort_days": 120,
            "predicted_value": 80,
            "predicted_probability": 0.75,
            "predicted_risk": 0.35,
            "start_date": "2016-01-01",
            "end_date": "2017-01-01",
            "after_state": {
                "stars": 42000,
                "forks": 6300,
                "contributors": 1000
            },
            "outcome_metrics": {
                "actual_value": 85,
                "success": True,
                "actual_risk": 0.3
            },
            "actual_stars_delta": 37000,
            "actual_downloads_delta": 300000000,
            "actual_revenue_delta": 0,
            "actual_contributors_delta": 900
        },
        {
            "asset_id": "storybookjs/storybook",
            "asset_type": "github_repo",
            "asset_name": "storybook",
            "developer_id": "github:storybookjs",
            "developer_username": "storybookjs",
            "before_state": {
                "stars": 1000,
                "forks": 200,
                "contributors": 50,
                "language": "typescript",
                "category": "testing"
            },
            "intervention_type": "Feature Expansion",
            "intervention_description": "Added docs and improved addon ecosystem",
            "planned_effort_days": 180,
            "predicted_value": 75,
            "predicted_probability": 0.7,
            "predicted_risk": 0.4,
            "start_date": "2017-01-01",
            "end_date": "2018-01-01",
            "after_state": {
                "stars": 81000,
                "forks": 8800,
                "contributors": 2000
            },
            "outcome_metrics": {
                "actual_value": 80,
                "success": True,
                "actual_risk": 0.35
            },
            "actual_stars_delta": 80000,
            "actual_downloads_delta": 10000000,
            "actual_revenue_delta": 10000000,
            "actual_contributors_delta": 1950
        },
        {
            "asset_id": "electron/electron",
            "asset_type": "github_repo",
            "asset_name": "electron",
            "developer_id": "github:electron",
            "developer_username": "electron",
            "before_state": {
                "stars": 5000,
                "forks": 1000,
                "contributors": 200,
                "language": "javascript",
                "category": "desktop"
            },
            "intervention_type": "Feature Expansion",
            "intervention_description": "Added security updates and improved performance",
            "planned_effort_days": 180,
            "predicted_value": 70,
            "predicted_probability": 0.7,
            "predicted_risk": 0.4,
            "start_date": "2016-01-01",
            "end_date": "2017-01-01",
            "after_state": {
                "stars": 106000,
                "forks": 14000,
                "contributors": 1500
            },
            "outcome_metrics": {
                "actual_value": 75,
                "success": True,
                "actual_risk": 0.35
            },
            "actual_stars_delta": 101000,
            "actual_downloads_delta": 0,
            "actual_revenue_delta": 0,
            "actual_contributors_delta": 1300
        },
        {
            "asset_id": "tauri-apps/tauri",
            "asset_type": "github_repo",
            "asset_name": "tauri",
            "developer_id": "github:tauri-apps",
            "developer_username": "tauri-apps",
            "before_state": {
                "stars": 500,
                "forks": 50,
                "contributors": 20,
                "language": "rust",
                "category": "desktop"
            },
            "intervention_type": "Feature Expansion",
            "intervention_description": "Added mobile support and improved performance",
            "planned_effort_days": 180,
            "predicted_value": 70,
            "predicted_probability": 0.65,
            "predicted_risk": 0.45,
            "start_date": "2020-01-01",
            "end_date": "2021-01-01",
            "after_state": {
                "stars": 72000,
                "forks": 4000,
                "contributors": 1000
            },
            "outcome_metrics": {
                "actual_value": 75,
                "success": True,
                "actual_risk": 0.4
            },
            "actual_stars_delta": 71500,
            "actual_downloads_delta": 1000000,
            "actual_revenue_delta": 2000000,
            "actual_contributors_delta": 980
        },
        {
            "asset_id": "neovim/neovim",
            "asset_type": "github_repo",
            "asset_name": "neovim",
            "developer_id": "github:neovim",
            "developer_username": "neovim",
            "before_state": {
                "stars": 2000,
                "forks": 300,
                "contributors": 100,
                "language": "lua",
                "category": "editor"
            },
            "intervention_type": "Feature Expansion",
            "intervention_description": "Added LSP support and improved Lua API",
            "planned_effort_days": 365,
            "predicted_value": 75,
            "predicted_probability": 0.7,
            "predicted_risk": 0.4,
            "start_date": "2016-01-01",
            "end_date": "2018-01-01",
            "after_state": {
                "stars": 73000,
                "forks": 5000,
                "contributors": 1000
            },
            "outcome_metrics": {
                "actual_value": 80,
                "success": True,
                "actual_risk": 0.35
            },
            "actual_stars_delta": 71000,
            "actual_downloads_delta": 0,
            "actual_revenue_delta": 0,
            "actual_contributors_delta": 900
        },
        {
            "asset_id": "helix-editor/helix",
            "asset_type": "github_repo",
            "asset_name": "helix",
            "developer_id": "github:helix-editor",
            "developer_username": "helix-editor",
            "before_state": {
                "stars": 100,
                "forks": 20,
                "contributors": 10,
                "language": "rust",
                "category": "editor"
            },
            "intervention_type": "Feature Expansion",
            "intervention_description": "Added tree-sitter support and improved modal editing",
            "planned_effort_days": 180,
            "predicted_value": 65,
            "predicted_probability": 0.6,
            "predicted_risk": 0.5,
            "start_date": "2020-01-01",
            "end_date": "2021-01-01",
            "after_state": {
                "stars": 28000,
                "forks": 2000,
                "contributors": 500
            },
            "outcome_metrics": {
                "actual_value": 70,
                "success": True,
                "actual_risk": 0.45
            },
            "actual_stars_delta": 27900,
            "actual_downloads_delta": 0,
            "actual_revenue_delta": 0,
            "actual_contributors_delta": 490
        },
        {
            "asset_id": "zed-industries/zed",
            "asset_type": "github_repo",
            "asset_name": "zed",
            "developer_id": "github:zed-industries",
            "developer_username": "zed-industries",
            "before_state": {
                "stars": 500,
                "forks": 50,
                "contributors": 20,
                "language": "rust",
                "category": "editor"
            },
            "intervention_type": "Feature Expansion",
            "intervention_description": "Added collaboration features and improved performance",
            "planned_effort_days": 180,
            "predicted_value": 65,
            "predicted_probability": 0.6,
            "predicted_risk": 0.5,
            "start_date": "2022-01-01",
            "end_date": "2023-01-01",
            "after_state": {
                "stars": 40000,
                "forks": 2500,
                "contributors": 400
            },
            "outcome_metrics": {
                "actual_value": 70,
                "success": True,
                "actual_risk": 0.45
            },
            "actual_stars_delta": 39500,
            "actual_downloads_delta": 0,
            "actual_revenue_delta": 5000000,
            "actual_contributors_delta": 380
        },
        {
            "asset_id": "languagetool-org/languagetool",
            "asset_type": "github_repo",
            "asset_name": "languagetool",
            "developer_id": "github:languagetool-org",
            "developer_username": "languagetool-org",
            "before_state": {
                "stars": 1000,
                "forks": 200,
                "contributors": 50,
                "language": "java",
                "category": "ai"
            },
            "intervention_type": "SaaS Conversion",
            "intervention_description": "Converted to SaaS with API access",
            "planned_effort_days": 180,
            "predicted_value": 70,
            "predicted_probability": 0.6,
            "predicted_risk": 0.5,
            "start_date": "2015-01-01",
            "end_date": "2016-01-01",
            "after_state": {
                "stars": 10000,
                "forks": 1200,
                "contributors": 300
            },
            "outcome_metrics": {
                "actual_value": 75,
                "success": True,
                "actual_risk": 0.45
            },
            "actual_stars_delta": 9000,
            "actual_downloads_delta": 0,
            "actual_revenue_delta": 5000000,
            "actual_contributors_delta": 250
        }
    ]
    
    # Seed each transformation
    for i, t in enumerate(transformations):
        print(f"Seeding {i+1}/{len(transformations)}: {t['asset_name']}")
        
        # Create intervention record
        record_id = ledger.create_intervention(
            asset_id=t["asset_id"],
            asset_type=t["asset_type"],
            asset_name=t["asset_name"],
            developer_id=t["developer_id"],
            developer_username=t["developer_username"],
            before_state=t["before_state"],
            intervention_type=t["intervention_type"],
            intervention_description=t["intervention_description"],
            planned_effort_days=t["planned_effort_days"],
            predicted_value=t["predicted_value"],
            predicted_probability=t["predicted_probability"],
            predicted_risk=t["predicted_risk"],
            predicted_outcome={
                "star_growth": (t["after_state"]["stars"] - t["before_state"]["stars"]) / max(t["before_state"]["stars"], 1),
                "contributor_growth": (t["after_state"]["contributors"] - t["before_state"]["contributors"]) / 10
            }
        )
        
        # Start intervention
        ledger.start_intervention(record_id, t["planned_effort_days"])
        
        # Complete intervention
        ledger.complete_intervention(
            record_id,
            t["after_state"],
            t["outcome_metrics"],
            t["planned_effort_days"]
        )
        
        # Verify
        ledger.verify_outcome(
            record_id,
            "system:seed",
            "system",
            VerificationStatus.VERIFIED.value,
            "Seeded historical transformation"
        )
        
        # Update Elo
        elo_system.update_from_intervention(
            t["developer_id"],
            t["intervention_type"],
            t["predicted_value"],
            t["outcome_metrics"]["actual_value"]
        )
        
        # Record transformation
        transformation_tracker.record_transformation(
            asset_id=t["asset_id"],
            asset_type=t["asset_type"],
            intervention_type=t["intervention_type"],
            context={"language": t["before_state"]["language"], "category": t["before_state"]["category"]},
            before_metrics={
                "stars": t["before_state"]["stars"],
                "revenue": 0,
                "contributors": t["before_state"]["contributors"]
            },
            after_metrics={
                "stars": t["after_state"]["stars"],
                "revenue": t["actual_revenue_delta"] if t["actual_revenue_delta"] else 0,
                "contributors": t["after_state"]["contributors"]
            }
        )
        
        print(f"  ✓ Record ID: {record_id}")
    
    # Save Elo ratings
    elo_system.save_to_file("elo_ratings.json")
    
    # Save transformation patterns
    transformation_tracker.export_patterns("transformation_patterns.json")
    
    print(f"\n✓ Seeded {len(transformations)} historical transformations")
    print(f"✓ Elo ratings saved to elo_ratings.json")
    print(f"✓ Transformation patterns saved to transformation_patterns.json")
    
    # Generate reusable laws
    laws = transformation_tracker.get_reusable_laws(min_confidence=0.7, min_samples=2)
    print(f"\n✓ Generated {len(laws)} reusable laws:")
    for law in laws:
        print(f"  - {law['law']}")


if __name__ == "__main__":
    seed_historical_transformations()
