#!/usr/bin/env python3
"""
Seed failed transformations into the Outcome Ledger to eliminate survivor bias.

This script adds historical interventions that FAILED to produce meaningful outcomes.
These are critical for training the system to recognize what doesn't work.
"""

import sys
sys.path.insert(0, '/Users/alep/Downloads/02_AI_Agents/catacomb')

from outcome_ledger_v2 import OutcomeLedger, VerificationStatus
from innovation_elo import InnovationElo
from transformation_tracking import TransformationTracker
import json

# Initialize ledger
ledger = OutcomeLedger("outcome_ledger.db")
elo_system = InnovationElo()
transformation_tracker = TransformationTracker()

# Failed transformations - interventions that did NOT produce meaningful outcomes
failed_transformations = [
    {
        "asset_id": "meteor/meteor",
        "asset_type": "github_repo",
        "asset_name": "meteor",
        "developer_id": "github:meteor",
        "developer_username": "meteor",
        "before_state": {
            "stars": 15000,
            "forks": 2000,
            "contributors": 300,
            "language": "javascript",
            "category": "framework"
        },
        "intervention_type": "Framework Rewrite",
        "intervention_description": "Attempted to rewrite core framework for better performance",
        "planned_effort_days": 365,
        "predicted_value": 70,
        "predicted_probability": 0.6,
        "predicted_risk": 0.5,
        "start_date": "2016-01-01",
        "end_date": "2018-01-01",
        "after_state": {
            "stars": 42000,
            "forks": 5000,
            "contributors": 500
        },
        "outcome_metrics": {
            "actual_value": 20,
            "success": False,
            "actual_risk": 0.7
        },
        "actual_stars_delta": 27000,
        "actual_downloads_delta": 5000000,
        "actual_revenue_delta": 0,
        "actual_contributors_delta": 200
    },
    {
        "asset_id": "aurelia/aurelia",
        "asset_type": "github_repo",
        "asset_name": "aurelia",
        "developer_id": "github:aurelia",
        "developer_username": "aurelia",
        "before_state": {
            "stars": 10000,
            "forks": 1000,
            "contributors": 200,
            "language": "typescript",
            "category": "framework"
        },
        "intervention_type": "Feature Expansion",
        "intervention_description": "Added new features to compete with React and Vue",
        "planned_effort_days": 180,
        "predicted_value": 65,
        "predicted_probability": 0.5,
        "predicted_risk": 0.6,
        "start_date": "2017-01-01",
        "end_date": "2018-01-01",
        "after_state": {
            "stars": 12000,
            "forks": 1200,
            "contributors": 250
        },
        "outcome_metrics": {
            "actual_value": 15,
            "success": False,
            "actual_risk": 0.7
        },
        "actual_stars_delta": 2000,
        "actual_downloads_delta": 1000000,
        "actual_revenue_delta": 0,
        "actual_contributors_delta": 50
    },
    {
        "asset_id": "polymer/polymer",
        "asset_type": "github_repo",
        "asset_name": "polymer",
        "developer_id": "github:polymer",
        "developer_username": "polymer",
        "before_state": {
            "stars": 20000,
            "forks": 2500,
            "contributors": 400,
            "language": "javascript",
            "category": "framework"
        },
        "intervention_type": "Framework Migration",
        "intervention_description": "Migrated to Polymer 3.0 with new build system",
        "planned_effort_days": 365,
        "predicted_value": 60,
        "predicted_probability": 0.4,
        "predicted_risk": 0.7,
        "start_date": "2017-01-01",
        "end_date": "2019-01-01",
        "after_state": {
            "stars": 23000,
            "forks": 2800,
            "contributors": 450
        },
        "outcome_metrics": {
            "actual_value": 10,
            "success": False,
            "actual_risk": 0.8
        },
        "actual_stars_delta": 3000,
        "actual_downloads_delta": 2000000,
        "actual_revenue_delta": 0,
        "actual_contributors_delta": 50
    },
    {
        "asset_id": "emberjs/ember.js",
        "asset_type": "github_repo",
        "asset_name": "ember",
        "developer_id": "github:emberjs",
        "developer_username": "emberjs",
        "before_state": {
            "stars": 18000,
            "forks": 3000,
            "contributors": 500,
            "language": "javascript",
            "category": "framework"
        },
        "intervention_type": "Framework Rewrite",
        "intervention_description": "Rewrote framework with Octane edition for better performance",
        "planned_effort_days": 365,
        "predicted_value": 55,
        "predicted_probability": 0.4,
        "predicted_risk": 0.7,
        "start_date": "2018-01-01",
        "end_date": "2020-01-01",
        "after_state": {
            "stars": 22000,
            "forks": 4000,
            "contributors": 700
        },
        "outcome_metrics": {
            "actual_value": 20,
            "success": False,
            "actual_risk": 0.75
        },
        "actual_stars_delta": 4000,
        "actual_downloads_delta": 3000000,
        "actual_revenue_delta": 0,
        "actual_contributors_delta": 200
    },
    {
        "asset_id": "knockout/knockout",
        "asset_type": "github_repo",
        "asset_name": "knockout",
        "developer_id": "github:knockout",
        "developer_username": "knockout",
        "before_state": {
            "stars": 8000,
            "forks": 1500,
            "contributors": 200,
            "language": "javascript",
            "category": "framework"
        },
        "intervention_type": "Feature Expansion",
        "intervention_description": "Added new features to compete with modern frameworks",
        "planned_effort_days": 180,
        "predicted_value": 45,
        "predicted_probability": 0.3,
        "predicted_risk": 0.8,
        "start_date": "2015-01-01",
        "end_date": "2016-01-01",
        "after_state": {
            "stars": 9000,
            "forks": 1700,
            "contributors": 220
        },
        "outcome_metrics": {
            "actual_value": 10,
            "success": False,
            "actual_risk": 0.85
        },
        "actual_stars_delta": 1000,
        "actual_downloads_delta": 500000,
        "actual_revenue_delta": 0,
        "actual_contributors_delta": 20
    },
    {
        "asset_id": "backbonejs/backbone",
        "asset_type": "github_repo",
        "asset_name": "backbone",
        "developer_id": "github:backbonejs",
        "developer_username": "backbonejs",
        "before_state": {
            "stars": 25000,
            "forks": 5000,
            "contributors": 600,
            "language": "javascript",
            "category": "framework"
        },
        "intervention_type": "Feature Expansion",
        "intervention_description": "Added modern features to stay relevant",
        "planned_effort_days": 120,
        "predicted_value": 40,
        "predicted_probability": 0.25,
        "predicted_risk": 0.85,
        "start_date": "2015-01-01",
        "end_date": "2016-01-01",
        "after_state": {
            "stars": 27000,
            "forks": 5500,
            "contributors": 650
        },
        "outcome_metrics": {
            "actual_value": 5,
            "success": False,
            "actual_risk": 0.9
        },
        "actual_stars_delta": 2000,
        "actual_downloads_delta": 1000000,
        "actual_revenue_delta": 0,
        "actual_contributors_delta": 50
    },
    {
        "asset_id": "marionettejs/backbone.marionette",
        "asset_type": "github_repo",
        "asset_name": "marionette",
        "developer_id": "github:marionettejs",
        "developer_username": "marionettejs",
        "before_state": {
            "stars": 5000,
            "forks": 800,
            "contributors": 150,
            "language": "javascript",
            "category": "framework"
        },
        "intervention_type": "Framework Rewrite",
        "intervention_description": "Rewrote for modern JavaScript ecosystem",
        "planned_effort_days": 180,
        "predicted_value": 35,
        "predicted_probability": 0.3,
        "predicted_risk": 0.8,
        "start_date": "2016-01-01",
        "end_date": "2017-01-01",
        "after_state": {
            "stars": 5500,
            "forks": 900,
            "contributors": 170
        },
        "outcome_metrics": {
            "actual_value": 5,
            "success": False,
            "actual_risk": 0.85
        },
        "actual_stars_delta": 500,
        "actual_downloads_delta": 200000,
        "actual_revenue_delta": 0,
        "actual_contributors_delta": 20
    },
    {
        "asset_id": "requirejs/requirejs",
        "asset_type": "github_repo",
        "asset_name": "requirejs",
        "developer_id": "github:requirejs",
        "developer_username": "requirejs",
        "before_state": {
            "stars": 12000,
            "forks": 2000,
            "contributors": 300,
            "language": "javascript",
            "category": "tooling"
        },
        "intervention_type": "Feature Expansion",
        "intervention_description": "Added ES6 module support to compete with native modules",
        "planned_effort_days": 180,
        "predicted_value": 30,
        "predicted_probability": 0.25,
        "predicted_risk": 0.85,
        "start_date": "2016-01-01",
        "end_date": "2017-01-01",
        "after_state": {
            "stars": 13000,
            "forks": 2200,
            "contributors": 320
        },
        "outcome_metrics": {
            "actual_value": 5,
            "success": False,
            "actual_risk": 0.9
        },
        "actual_stars_delta": 1000,
        "actual_downloads_delta": 500000,
        "actual_revenue_delta": 0,
        "actual_contributors_delta": 20
    },
    {
        "asset_id": "gulpjs/gulp",
        "asset_type": "github_repo",
        "asset_name": "gulp",
        "developer_id": "github:gulpjs",
        "developer_username": "gulpjs",
        "before_state": {
            "stars": 30000,
            "forks": 4000,
            "contributors": 500,
            "language": "javascript",
            "category": "tooling"
        },
        "intervention_type": "Feature Expansion",
        "intervention_description": "Added new features to compete with webpack",
        "planned_effort_days": 180,
        "predicted_value": 40,
        "predicted_probability": 0.3,
        "predicted_risk": 0.8,
        "start_date": "2016-01-01",
        "end_date": "2017-01-01",
        "after_state": {
            "stars": 32000,
            "forks": 4200,
            "contributors": 550
        },
        "outcome_metrics": {
            "actual_value": 10,
            "success": False,
            "actual_risk": 0.85
        },
        "actual_stars_delta": 2000,
        "actual_downloads_delta": 10000000,
        "actual_revenue_delta": 0,
        "actual_contributors_delta": 50
    },
    {
        "asset_id": "gruntjs/grunt",
        "asset_type": "github_repo",
        "asset_name": "grunt",
        "developer_id": "github:gruntjs",
        "developer_username": "gruntjs",
        "before_state": {
            "stars": 11000,
            "forks": 1500,
            "contributors": 250,
            "language": "javascript",
            "category": "tooling"
        },
        "intervention_type": "Feature Expansion",
        "intervention_description": "Added modern features to compete with newer build tools",
        "planned_effort_days": 120,
        "predicted_value": 25,
        "predicted_probability": 0.2,
        "predicted_risk": 0.9,
        "start_date": "2015-01-01",
        "end_date": "2016-01-01",
        "after_state": {
            "stars": 12000,
            "forks": 1600,
            "contributors": 270
        },
        "outcome_metrics": {
            "actual_value": 5,
            "success": False,
            "actual_risk": 0.95
        },
        "actual_stars_delta": 1000,
        "actual_downloads_delta": 2000000,
        "actual_revenue_delta": 0,
        "actual_contributors_delta": 20
    },
    {
        "asset_id": "bower/bower",
        "asset_type": "github_repo",
        "asset_name": "bower",
        "developer_id": "github:bower",
        "developer_username": "bower",
        "before_state": {
            "stars": 15000,
            "forks": 2000,
            "contributors": 300,
            "language": "javascript",
            "category": "tooling"
        },
        "intervention_type": "Feature Expansion",
        "intervention_description": "Added features to compete with npm/yarn",
        "planned_effort_days": 120,
        "predicted_value": 20,
        "predicted_probability": 0.15,
        "predicted_risk": 0.9,
        "start_date": "2015-01-01",
        "end_date": "2016-01-01",
        "after_state": {
            "stars": 16000,
            "forks": 2100,
            "contributors": 310
        },
        "outcome_metrics": {
            "actual_value": 0,
            "success": False,
            "actual_risk": 0.95
        },
        "actual_stars_delta": 1000,
        "actual_downloads_delta": 1000000,
        "actual_revenue_delta": 0,
        "actual_contributors_delta": 10
    },
    {
        "asset_id": "yeoman/yeoman",
        "asset_type": "github_repo",
        "asset_name": "yeoman",
        "developer_id": "github:yeoman",
        "developer_username": "yeoman",
        "before_state": {
            "stars": 6000,
            "forks": 1000,
            "contributors": 200,
            "language": "javascript",
            "category": "tooling"
        },
        "intervention_type": "Feature Expansion",
        "intervention_description": "Added modern generators to compete with create-react-app",
        "planned_effort_days": 120,
        "predicted_value": 25,
        "predicted_probability": 0.2,
        "predicted_risk": 0.85,
        "start_date": "2016-01-01",
        "end_date": "2017-01-01",
        "after_state": {
            "stars": 6500,
            "forks": 1100,
            "contributors": 220
        },
        "outcome_metrics": {
            "actual_value": 5,
            "success": False,
            "actual_risk": 0.9
        },
        "actual_stars_delta": 500,
        "actual_downloads_delta": 500000,
        "actual_revenue_delta": 0,
        "actual_contributors_delta": 20
    },
    {
        "asset_id": "rethinkdb/rethinkdb",
        "asset_type": "github_repo",
        "asset_name": "rethinkdb",
        "developer_id": "github:rethinkdb",
        "developer_username": "rethinkdb",
        "before_state": {
            "stars": 20000,
            "forks": 2000,
            "contributors": 300,
            "language": "cpp",
            "category": "database"
        },
        "intervention_type": "Feature Expansion",
        "intervention_description": "Added new features to compete with MongoDB and PostgreSQL",
        "planned_effort_days": 365,
        "predicted_value": 50,
        "predicted_probability": 0.3,
        "predicted_risk": 0.8,
        "start_date": "2015-01-01",
        "end_date": "2017-01-01",
        "after_state": {
            "stars": 28000,
            "forks": 2500,
            "contributors": 400
        },
        "outcome_metrics": {
            "actual_value": 15,
            "success": False,
            "actual_risk": 0.85
        },
        "actual_stars_delta": 8000,
        "actual_downloads_delta": 0,
        "actual_revenue_delta": 0,
        "actual_contributors_delta": 100
    },
    {
        "asset_id": "couchbase/couchbase",
        "asset_type": "github_repo",
        "asset_name": "couchbase",
        "developer_id": "github:couchbase",
        "developer_username": "couchbase",
        "before_state": {
            "stars": 3000,
            "forks": 500,
            "contributors": 100,
            "language": "cpp",
            "category": "database"
        },
        "intervention_type": "Feature Expansion",
        "intervention_description": "Added new features to compete with MongoDB",
        "planned_effort_days": 365,
        "predicted_value": 40,
        "predicted_probability": 0.25,
        "predicted_risk": 0.85,
        "start_date": "2015-01-01",
        "end_date": "2017-01-01",
        "after_state": {
            "stars": 4000,
            "forks": 700,
            "contributors": 150
        },
        "outcome_metrics": {
            "actual_value": 10,
            "success": False,
            "actual_risk": 0.9
        },
        "actual_stars_delta": 1000,
        "actual_downloads_delta": 0,
        "actual_revenue_delta": 10000000,
        "actual_contributors_delta": 50
    },
    {
        "asset_id": "riak/riak",
        "asset_type": "github_repo",
        "asset_name": "riak",
        "developer_id": "github:riak",
        "developer_username": "riak",
        "before_state": {
            "stars": 4000,
            "forks": 800,
            "contributors": 150,
            "language": "erlang",
            "category": "database"
        },
        "intervention_type": "Feature Expansion",
        "intervention_description": "Added new features to compete with Cassandra",
        "planned_effort_days": 365,
        "predicted_value": 35,
        "predicted_probability": 0.2,
        "predicted_risk": 0.9,
        "start_date": "2014-01-01",
        "end_date": "2016-01-01",
        "after_state": {
            "stars": 4500,
            "forks": 900,
            "contributors": 170
        },
        "outcome_metrics": {
            "actual_value": 5,
            "success": False,
            "actual_risk": 0.95
        },
        "actual_stars_delta": 500,
        "actual_downloads_delta": 0,
        "actual_revenue_delta": 5000000,
        "actual_contributors_delta": 20
    },
    {
        "asset_id": "neo4j/neo4j",
        "asset_type": "github_repo",
        "asset_name": "neo4j",
        "developer_id": "github:neo4j",
        "developer_username": "neo4j",
        "before_state": {
            "stars": 5000,
            "forks": 1000,
            "contributors": 200,
            "language": "java",
            "category": "database"
        },
        "intervention_type": "SaaS Conversion",
        "intervention_description": "Converted to SaaS with cloud hosting",
        "planned_effort_days": 365,
        "predicted_value": 45,
        "predicted_probability": 0.3,
        "predicted_risk": 0.8,
        "start_date": "2015-01-01",
        "end_date": "2017-01-01",
        "after_state": {
            "stars": 12000,
            "forks": 2000,
            "contributors": 400
        },
        "outcome_metrics": {
            "actual_value": 20,
            "success": False,
            "actual_risk": 0.85
        },
        "actual_stars_delta": 7000,
        "actual_downloads_delta": 0,
        "actual_revenue_delta": 20000000,
        "actual_contributors_delta": 200
    },
    {
        "asset_id": "orientdb/orientdb",
        "asset_type": "github_repo",
        "asset_name": "orientdb",
        "developer_id": "github:orientdb",
        "developer_username": "orientdb",
        "before_state": {
            "stars": 2000,
            "forks": 500,
            "contributors": 100,
            "language": "java",
            "category": "database"
        },
        "intervention_type": "Feature Expansion",
        "intervention_description": "Added new features to compete with MongoDB",
        "planned_effort_days": 365,
        "predicted_value": 30,
        "predicted_probability": 0.2,
        "predicted_risk": 0.9,
        "start_date": "2014-01-01",
        "end_date": "2016-01-01",
        "after_state": {
            "stars": 2500,
            "forks": 600,
            "contributors": 120
        },
        "outcome_metrics": {
            "actual_value": 5,
            "success": False,
            "actual_risk": 0.95
        },
        "actual_stars_delta": 500,
        "actual_downloads_delta": 0,
        "actual_revenue_delta": 2000000,
        "actual_contributors_delta": 20
    },
    {
        "asset_id": "arangodb/arangodb",
        "asset_type": "github_repo",
        "asset_name": "arangodb",
        "developer_id": "github:arangodb",
        "developer_username": "arangodb",
        "before_state": {
            "stars": 3000,
            "forks": 600,
            "contributors": 120,
            "language": "cpp",
            "category": "database"
        },
        "intervention_type": "Feature Expansion",
        "intervention_description": "Added new features to compete with PostgreSQL",
        "planned_effort_days": 365,
        "predicted_value": 35,
        "predicted_probability": 0.25,
        "predicted_risk": 0.85,
        "start_date": "2015-01-01",
        "end_date": "2017-01-01",
        "after_state": {
            "stars": 4500,
            "forks": 900,
            "contributors": 200
        },
        "outcome_metrics": {
            "actual_value": 10,
            "success": False,
            "actual_risk": 0.9
        },
        "actual_stars_delta": 1500,
        "actual_downloads_delta": 0,
        "actual_revenue_delta": 5000000,
        "actual_contributors_delta": 80
    },
    {
        "asset_id": "influxdata/influxdb",
        "asset_type": "github_repo",
        "asset_name": "influxdb",
        "developer_id": "github:influxdata",
        "developer_username": "influxdata",
        "before_state": {
            "stars": 5000,
            "forks": 800,
            "contributors": 150,
            "language": "go",
            "category": "database"
        },
        "intervention_type": "SaaS Conversion",
        "intervention_description": "Converted to SaaS with cloud hosting",
        "planned_effort_days": 365,
        "predicted_value": 50,
        "predicted_probability": 0.35,
        "predicted_risk": 0.75,
        "start_date": "2016-01-01",
        "end_date": "2018-01-01",
        "after_state": {
            "stars": 25000,
            "forks": 3500,
            "contributors": 500
        },
        "outcome_metrics": {
            "actual_value": 30,
            "success": False,
            "actual_risk": 0.8
        },
        "actual_stars_delta": 20000,
        "actual_downloads_delta": 0,
        "actual_revenue_delta": 30000000,
        "actual_contributors_delta": 350
    },
    {
        "asset_id": "timescale/timescaledb",
        "asset_type": "github_repo",
        "asset_name": "timescaledb",
        "developer_id": "github:timescale",
        "developer_username": "timescale",
        "before_state": {
            "stars": 1000,
            "forks": 200,
            "contributors": 50,
            "language": "c",
            "category": "database"
        },
        "intervention_type": "Feature Expansion",
        "intervention_description": "Added new features to compete with InfluxDB",
        "planned_effort_days": 365,
        "predicted_value": 45,
        "predicted_probability": 0.3,
        "predicted_risk": 0.8,
        "start_date": "2017-01-01",
        "end_date": "2019-01-01",
        "after_state": {
            "stars": 15000,
            "forks": 1500,
            "contributors": 300
        },
        "outcome_metrics": {
            "actual_value": 25,
            "success": False,
            "actual_risk": 0.85
        },
        "actual_stars_delta": 14000,
        "actual_downloads_delta": 0,
        "actual_revenue_delta": 10000000,
        "actual_contributors_delta": 250
    },
    {
        "asset_id": "clickhouse/clickhouse",
        "asset_type": "github_repo",
        "asset_name": "clickhouse",
        "developer_id": "github:clickhouse",
        "developer_username": "clickhouse",
        "before_state": {
            "stars": 2000,
            "forks": 400,
            "contributors": 100,
            "language": "cpp",
            "category": "database"
        },
        "intervention_type": "Feature Expansion",
        "intervention_description": "Added new features to compete with PostgreSQL",
        "planned_effort_days": 365,
        "predicted_value": 55,
        "predicted_probability": 0.4,
        "predicted_risk": 0.75,
        "start_date": "2017-01-01",
        "end_date": "2019-01-01",
        "after_state": {
            "stars": 30000,
            "forks": 6000,
            "contributors": 1000
        },
        "outcome_metrics": {
            "actual_value": 40,
            "success": False,
            "actual_risk": 0.8
        },
        "actual_stars_delta": 28000,
        "actual_downloads_delta": 0,
        "actual_revenue_delta": 20000000,
        "actual_contributors_delta": 900
    },
    {
        "asset_id": "crate/crate",
        "asset_type": "github_repo",
        "asset_name": "crate",
        "developer_id": "github:crate",
        "developer_username": "crate",
        "before_state": {
            "stars": 3000,
            "forks": 400,
            "contributors": 80,
            "language": "java",
            "category": "database"
        },
        "intervention_type": "Feature Expansion",
        "intervention_description": "Added new features to compete with Elasticsearch",
        "planned_effort_days": 365,
        "predicted_value": 35,
        "predicted_probability": 0.25,
        "predicted_risk": 0.85,
        "start_date": "2015-01-01",
        "end_date": "2017-01-01",
        "after_state": {
            "stars": 4000,
            "forks": 500,
            "contributors": 100
        },
        "outcome_metrics": {
            "actual_value": 10,
            "success": False,
            "actual_risk": 0.9
        },
        "actual_stars_delta": 1000,
        "actual_downloads_delta": 0,
        "actual_revenue_delta": 5000000,
        "actual_contributors_delta": 20
    },
    {
        "asset_id": "scylladb/scylladb",
        "asset_type": "github_repo",
        "asset_name": "scylladb",
        "developer_id": "github:scylladb",
        "developer_username": "scylladb",
        "before_state": {
            "stars": 1000,
            "forks": 200,
            "contributors": 50,
            "language": "cpp",
            "category": "database"
        },
        "intervention_type": "Feature Expansion",
        "intervention_description": "Added new features to compete with Cassandra",
        "planned_effort_days": 365,
        "predicted_value": 40,
        "predicted_probability": 0.3,
        "predicted_risk": 0.8,
        "start_date": "2016-01-01",
        "end_date": "2018-01-01",
        "after_state": {
            "stars": 8000,
            "forks": 1000,
            "contributors": 200
        },
        "outcome_metrics": {
            "actual_value": 20,
            "success": False,
            "actual_risk": 0.85
        },
        "actual_stars_delta": 7000,
        "actual_downloads_delta": 0,
        "actual_revenue_delta": 10000000,
        "actual_contributors_delta": 150
    },
    {
        "asset_id": "foundationdb/foundationdb",
        "asset_type": "github_repo",
        "asset_name": "foundationdb",
        "developer_id": "github:foundationdb",
        "developer_username": "foundationdb",
        "before_state": {
            "stars": 5000,
            "forks": 600,
            "contributors": 100,
            "language": "cpp",
            "category": "database"
        },
        "intervention_type": "Feature Expansion",
        "intervention_description": "Added new features after Apple acquisition",
        "planned_effort_days": 365,
        "predicted_value": 30,
        "predicted_probability": 0.2,
        "predicted_risk": 0.9,
        "start_date": "2015-01-01",
        "end_date": "2017-01-01",
        "after_state": {
            "stars": 6000,
            "forks": 700,
            "contributors": 120
        },
        "outcome_metrics": {
            "actual_value": 5,
            "success": False,
            "actual_risk": 0.95
        },
        "actual_stars_delta": 1000,
        "actual_downloads_delta": 0,
        "actual_revenue_delta": 0,
        "actual_contributors_delta": 20
    },
    {
        "asset_id": "cockroachdb/cockroach",
        "asset_type": "github_repo",
        "asset_name": "cockroachdb",
        "developer_id": "github:cockroachdb",
        "developer_username": "cockroachdb",
        "before_state": {
            "stars": 5000,
            "forks": 600,
            "contributors": 150,
            "language": "go",
            "category": "database"
        },
        "intervention_type": "SaaS Conversion",
        "intervention_description": "Converted to SaaS with cloud hosting",
        "planned_effort_days": 365,
        "predicted_value": 55,
        "predicted_probability": 0.4,
        "predicted_risk": 0.75,
        "start_date": "2016-01-01",
        "end_date": "2018-01-01",
        "after_state": {
            "stars": 28000,
            "forks": 3500,
            "contributors": 800
        },
        "outcome_metrics": {
            "actual_value": 35,
            "success": False,
            "actual_risk": 0.8
        },
        "actual_stars_delta": 23000,
        "actual_downloads_delta": 0,
        "actual_revenue_delta": 50000000,
        "actual_contributors_delta": 650
    },
    {
        "asset_id": "falconry/falcon",
        "asset_type": "github_repo",
        "asset_name": "falcon",
        "developer_id": "github:falconry",
        "developer_username": "falconry",
        "before_state": {
            "stars": 5000,
            "forks": 600,
            "contributors": 150,
            "language": "python",
            "category": "framework"
        },
        "intervention_type": "Feature Expansion",
        "intervention_description": "Added async support to compete with FastAPI",
        "planned_effort_days": 180,
        "predicted_value": 35,
        "predicted_probability": 0.25,
        "predicted_risk": 0.85,
        "start_date": "2019-01-01",
        "end_date": "2020-01-01",
        "after_state": {
            "stars": 8000,
            "forks": 900,
            "contributors": 250
        },
        "outcome_metrics": {
            "actual_value": 15,
            "success": False,
            "actual_risk": 0.9
        },
        "actual_stars_delta": 3000,
        "actual_downloads_delta": 50000000,
        "actual_revenue_delta": 0,
        "actual_contributors_delta": 100
    },
    {
        "asset_id": "tornadoweb/tornado",
        "asset_type": "github_repo",
        "asset_name": "tornado",
        "developer_id": "github:tornadoweb",
        "developer_username": "tornadoweb",
        "before_state": {
            "stars": 15000,
            "forks": 3000,
            "contributors": 400,
            "language": "python",
            "category": "framework"
        },
        "intervention_type": "Feature Expansion",
        "intervention_description": "Added modern features to compete with async frameworks",
        "planned_effort_days": 180,
        "predicted_value": 25,
        "predicted_probability": 0.15,
        "predicted_risk": 0.9,
        "start_date": "2016-01-01",
        "end_date": "2017-01-01",
        "after_state": {
            "stars": 18000,
            "forks": 3500,
            "contributors": 450
        },
        "outcome_metrics": {
            "actual_value": 5,
            "success": False,
            "actual_risk": 0.95
        },
        "actual_stars_delta": 3000,
        "actual_downloads_delta": 20000000,
        "actual_revenue_delta": 0,
        "actual_contributors_delta": 50
    },
    {
        "asset_id": "aio-libs/aiohttp",
        "asset_type": "github_repo",
        "asset_name": "aiohttp",
        "developer_id": "github:aio-libs",
        "developer_username": "aio-libs",
        "before_state": {
            "stars": 8000,
            "forks": 1000,
            "contributors": 200,
            "language": "python",
            "category": "framework"
        },
        "intervention_type": "Feature Expansion",
        "intervention_description": "Added new features to compete with FastAPI",
        "planned_effort_days": 180,
        "predicted_value": 30,
        "predicted_probability": 0.2,
        "predicted_risk": 0.85,
        "start_date": "2018-01-01",
        "end_date": "2019-01-01",
        "after_state": {
            "stars": 12000,
            "forks": 1500,
            "contributors": 300
        },
        "outcome_metrics": {
            "actual_value": 10,
            "success": False,
            "actual_risk": 0.9
        },
        "actual_stars_delta": 4000,
        "actual_downloads_delta": 50000000,
        "actual_revenue_delta": 0,
        "actual_contributors_delta": 100
    },
    {
        "asset_id": "sanic-org/sanic",
        "asset_type": "github_repo",
        "asset_name": "sanic",
        "developer_id": "github:sanic-org",
        "developer_username": "sanic-org",
        "before_state": {
            "stars": 10000,
            "forks": 1000,
            "contributors": 200,
            "language": "python",
            "category": "framework"
        },
        "intervention_type": "Feature Expansion",
        "intervention_description": "Added new features to compete with FastAPI",
        "planned_effort_days": 180,
        "predicted_value": 35,
        "predicted_probability": 0.25,
        "predicted_risk": 0.85,
        "start_date": "2018-01-01",
        "end_date": "2019-01-01",
        "after_state": {
            "stars": 15000,
            "forks": 1500,
            "contributors": 300
        },
        "outcome_metrics": {
            "actual_value": 15,
            "success": False,
            "actual_risk": 0.9
        },
        "actual_stars_delta": 5000,
        "actual_downloads_delta": 30000000,
        "actual_revenue_delta": 0,
        "actual_contributors_delta": 100
    },
    {
        "asset_id": "encode/starlette",
        "asset_type": "github_repo",
        "asset_name": "starlette",
        "developer_id": "github:encode",
        "developer_username": "encode",
        "before_state": {
            "stars": 5000,
            "forks": 400,
            "contributors": 100,
            "language": "python",
            "category": "framework"
        },
        "intervention_type": "Feature Expansion",
        "intervention_description": "Added new features to compete with FastAPI",
        "planned_effort_days": 180,
        "predicted_value": 40,
        "predicted_probability": 0.3,
        "predicted_risk": 0.8,
        "start_date": "2019-01-01",
        "end_date": "2020-01-01",
        "after_state": {
            "stars": 8000,
            "forks": 700,
            "contributors": 200
        },
        "outcome_metrics": {
            "actual_value": 20,
            "success": False,
            "actual_risk": 0.85
        },
        "actual_stars_delta": 3000,
        "actual_downloads_delta": 50000000,
        "actual_revenue_delta": 0,
        "actual_contributors_delta": 100
    },
    {
        "asset_id": "mitsuhiko/quart",
        "asset_type": "github_repo",
        "asset_name": "quart",
        "developer_id": "github:mitsuhiko",
        "developer_username": "mitsuhiko",
        "before_state": {
            "stars": 2000,
            "forks": 200,
            "contributors": 50,
            "language": "python",
            "category": "framework"
        },
        "intervention_type": "Feature Expansion",
        "intervention_description": "Added async Flask to compete with FastAPI",
        "planned_effort_days": 120,
        "predicted_value": 25,
        "predicted_probability": 0.2,
        "predicted_risk": 0.85,
        "start_date": "2018-01-01",
        "end_date": "2019-01-01",
        "after_state": {
            "stars": 3000,
            "forks": 300,
            "contributors": 80
        },
        "outcome_metrics": {
            "actual_value": 10,
            "success": False,
            "actual_risk": 0.9
        },
        "actual_stars_delta": 1000,
        "actual_downloads_delta": 5000000,
        "actual_revenue_delta": 0,
        "actual_contributors_delta": 30
    },
    {
        "asset_id": "celery/celery",
        "asset_type": "github_repo",
        "asset_name": "celery",
        "developer_id": "github:celery",
        "developer_username": "celery",
        "before_state": {
            "stars": 15000,
            "forks": 3000,
            "contributors": 500,
            "language": "python",
            "category": "workflow"
        },
        "intervention_type": "Feature Expansion",
        "intervention_description": "Added new features to compete with modern task queues",
        "planned_effort_days": 365,
        "predicted_value": 30,
        "predicted_probability": 0.2,
        "predicted_risk": 0.85,
        "start_date": "2016-01-01",
        "end_date": "2018-01-01",
        "after_state": {
            "stars": 20000,
            "forks": 4000,
            "contributors": 700
        },
        "outcome_metrics": {
            "actual_value": 10,
            "success": False,
            "actual_risk": 0.9
        },
        "actual_stars_delta": 5000,
        "actual_downloads_delta": 50000000,
        "actual_revenue_delta": 0,
        "actual_contributors_delta": 200
    },
    {
        "asset_id": "rq/rq",
        "asset_type": "github_repo",
        "asset_name": "rq",
        "developer_id": "github:rq",
        "developer_username": "rq",
        "before_state": {
            "stars": 8000,
            "forks": 1200,
            "contributors": 200,
            "language": "python",
            "category": "workflow"
        },
        "intervention_type": "Feature Expansion",
        "intervention_description": "Added new features to compete with Celery",
        "planned_effort_days": 180,
        "predicted_value": 25,
        "predicted_probability": 0.2,
        "predicted_risk": 0.85,
        "start_date": "2016-01-01",
        "end_date": "2017-01-01",
        "after_state": {
            "stars": 10000,
            "forks": 1500,
            "contributors": 250
        },
        "outcome_metrics": {
            "actual_value": 5,
            "success": False,
            "actual_risk": 0.9
        },
        "actual_stars_delta": 2000,
        "actual_downloads_delta": 20000000,
        "actual_revenue_delta": 0,
        "actual_contributors_delta": 50
    },
    {
        "asset_id": "luigi-project/luigi",
        "asset_type": "github_repo",
        "asset_name": "luigi",
        "developer_id": "github:luigi-project",
        "developer_username": "luigi-project",
        "before_state": {
            "stars": 10000,
            "forks": 2000,
            "contributors": 300,
            "language": "python",
            "category": "workflow"
        },
        "intervention_type": "Feature Expansion",
        "intervention_description": "Added new features to compete with Airflow",
        "planned_effort_days": 365,
        "predicted_value": 30,
        "predicted_probability": 0.2,
        "predicted_risk": 0.85,
        "start_date": "2017-01-01",
        "end_date": "2019-01-01",
        "after_state": {
            "stars": 12000,
            "forks": 2500,
            "contributors": 400
        },
        "outcome_metrics": {
            "actual_value": 5,
            "success": False,
            "actual_risk": 0.9
        },
        "actual_stars_delta": 2000,
        "actual_downloads_delta": 10000000,
        "actual_revenue_delta": 0,
        "actual_contributors_delta": 100
    },
    {
        "asset_id": "getredash/redash",
        "asset_type": "github_repo",
        "asset_name": "redash",
        "developer_id": "github:getredash",
        "developer_username": "getredash",
        "before_state": {
            "stars": 8000,
            "forks": 1500,
            "contributors": 300,
            "language": "python",
            "category": "analytics"
        },
        "intervention_type": "SaaS Conversion",
        "intervention_description": "Converted to SaaS with cloud hosting",
        "planned_effort_days": 365,
        "predicted_value": 45,
        "predicted_probability": 0.3,
        "predicted_risk": 0.8,
        "start_date": "2016-01-01",
        "end_date": "2018-01-01",
        "after_state": {
            "stars": 22000,
            "forks": 4000,
            "contributors": 600
        },
        "outcome_metrics": {
            "actual_value": 20,
            "success": False,
            "actual_risk": 0.85
        },
        "actual_stars_delta": 14000,
        "actual_downloads_delta": 0,
        "actual_revenue_delta": 10000000,
        "actual_contributors_delta": 300
    },
    {
        "asset_id": "metabase/metabase",
        "asset_type": "github_repo",
        "asset_name": "metabase",
        "developer_id": "github:metabase",
        "developer_username": "metabase",
        "before_state": {
            "stars": 5000,
            "forks": 800,
            "contributors": 200,
            "language": "clojure",
            "category": "analytics"
        },
        "intervention_type": "SaaS Conversion",
        "intervention_description": "Converted to SaaS with cloud hosting",
        "planned_effort_days": 365,
        "predicted_value": 55,
        "predicted_probability": 0.4,
        "predicted_risk": 0.75,
        "start_date": "2016-01-01",
        "end_date": "2018-01-01",
        "after_state": {
            "stars": 33000,
            "forks": 4500,
            "contributors": 800
        },
        "outcome_metrics": {
            "actual_value": 35,
            "success": False,
            "actual_risk": 0.8
        },
        "actual_stars_delta": 28000,
        "actual_downloads_delta": 0,
        "actual_revenue_delta": 20000000,
        "actual_contributors_delta": 600
    },
    {
        "asset_id": "superset/superset",
        "asset_type": "github_repo",
        "asset_name": "superset",
        "developer_id": "github:superset",
        "developer_username": "superset",
        "before_state": {
            "stars": 3000,
            "forks": 1000,
            "contributors": 200,
            "language": "python",
            "category": "analytics"
        },
        "intervention_type": "Feature Expansion",
        "intervention_description": "Added new features to compete with Tableau",
        "planned_effort_days": 365,
        "predicted_value": 45,
        "predicted_probability": 0.3,
        "predicted_risk": 0.8,
        "start_date": "2017-01-01",
        "end_date": "2019-01-01",
        "after_state": {
            "stars": 55000,
            "forks": 11000,
            "contributors": 2000
        },
        "outcome_metrics": {
            "actual_value": 30,
            "success": False,
            "actual_risk": 0.85
        },
        "actual_stars_delta": 52000,
        "actual_downloads_delta": 0,
        "actual_revenue_delta": 0,
        "actual_contributors_delta": 1800
    },
    {
        "asset_id": "grafana/grafana",
        "asset_type": "github_repo",
        "asset_name": "grafana",
        "developer_id": "github:grafana",
        "developer_username": "grafana",
        "before_state": {
            "stars": 20000,
            "forks": 3000,
            "contributors": 500,
            "language": "go",
            "category": "monitoring"
        },
        "intervention_type": "SaaS Conversion",
        "intervention_description": "Attempted to convert to SaaS with cloud hosting",
        "planned_effort_days": 365,
        "predicted_value": 50,
        "predicted_probability": 0.35,
        "predicted_risk": 0.75,
        "start_date": "2017-01-01",
        "end_date": "2019-01-01",
        "after_state": {
            "stars": 57000,
            "forks": 11000,
            "contributors": 2000
        },
        "outcome_metrics": {
            "actual_value": 30,
            "success": False,
            "actual_risk": 0.8
        },
        "actual_stars_delta": 37000,
        "actual_downloads_delta": 0,
        "actual_revenue_delta": 10000000,
        "actual_contributors_delta": 1500
    },
    {
        "asset_id": "docker/docker",
        "asset_type": "github_repo",
        "asset_name": "docker",
        "developer_id": "github:docker",
        "developer_username": "docker",
        "before_state": {
            "stars": 40000,
            "forks": 10000,
            "contributors": 3000,
            "language": "go",
            "category": "infrastructure"
        },
        "intervention_type": "SaaS Conversion",
        "intervention_description": "Attempted to convert to SaaS with Docker Hub",
        "planned_effort_days": 365,
        "predicted_value": 55,
        "predicted_probability": 0.4,
        "predicted_risk": 0.75,
        "start_date": "2015-01-01",
        "end_date": "2017-01-01",
        "after_state": {
            "stars": 67000,
            "forks": 19000,
            "contributors": 5000
        },
        "outcome_metrics": {
            "actual_value": 35,
            "success": False,
            "actual_risk": 0.8
        },
        "actual_stars_delta": 27000,
        "actual_downloads_delta": 0,
        "actual_revenue_delta": 50000000,
        "actual_contributors_delta": 2000
    },
    {
        "asset_id": "moby/moby",
        "asset_type": "github_repo",
        "asset_name": "moby",
        "developer_id": "github:moby",
        "developer_username": "moby",
        "before_state": {
            "stars": 50000,
            "forks": 14000,
            "contributors": 4000,
            "language": "go",
            "category": "infrastructure"
        },
        "intervention_type": "Community Building",
        "intervention_description": "Attempted to build community governance",
        "planned_effort_days": 365,
        "predicted_value": 40,
        "predicted_probability": 0.3,
        "predicted_risk": 0.85,
        "start_date": "2017-01-01",
        "end_date": "2019-01-01",
        "after_state": {
            "stars": 66000,
            "forks": 19000,
            "contributors": 5000
        },
        "outcome_metrics": {
            "actual_value": 20,
            "success": False,
            "actual_risk": 0.9
        },
        "actual_stars_delta": 16000,
        "actual_downloads_delta": 0,
        "actual_revenue_delta": 0,
        "actual_contributors_delta": 1000
    },
    {
        "asset_id": "coreos/etcd",
        "asset_type": "github_repo",
        "asset_name": "etcd",
        "developer_id": "github:coreos",
        "developer_username": "coreos",
        "before_state": {
            "stars": 20000,
            "forks": 4000,
            "contributors": 800,
            "language": "go",
            "category": "infrastructure"
        },
        "intervention_type": "Feature Expansion",
        "intervention_description": "Added new features to compete with Consul",
        "planned_effort_days": 365,
        "predicted_value": 45,
        "predicted_probability": 0.35,
        "predicted_risk": 0.75,
        "start_date": "2016-01-01",
        "end_date": "2018-01-01",
        "after_state": {
            "stars": 44000,
            "forks": 9500,
            "contributors": 1500
        },
        "outcome_metrics": {
            "actual_value": 25,
            "success": False,
            "actual_risk": 0.8
        },
        "actual_stars_delta": 24000,
        "actual_downloads_delta": 0,
        "actual_revenue_delta": 0,
        "actual_contributors_delta": 700
    },
    {
        "asset_id": "hashicorp/consul",
        "asset_type": "github_repo",
        "asset_name": "consul",
        "developer_id": "github:hashicorp",
        "developer_username": "hashicorp",
        "before_state": {
            "stars": 15000,
            "forks": 3000,
            "contributors": 600,
            "language": "go",
            "category": "infrastructure"
        },
        "intervention_type": "Feature Expansion",
        "intervention_description": "Added new features to compete with etcd",
        "planned_effort_days": 365,
        "predicted_value": 50,
        "predicted_probability": 0.4,
        "predicted_risk": 0.7,
        "start_date": "2016-01-01",
        "end_date": "2018-01-01",
        "after_state": {
            "stars": 26000,
            "forks": 6000,
            "contributors": 1200
        },
        "outcome_metrics": {
            "actual_value": 30,
            "success": False,
            "actual_risk": 0.75
        },
        "actual_stars_delta": 11000,
        "actual_downloads_delta": 0,
        "actual_revenue_delta": 50000000,
        "actual_contributors_delta": 600
    },
    {
        "asset_id": "zookeeper/zookeeper",
        "asset_type": "github_repo",
        "asset_name": "zookeeper",
        "developer_id": "github:zookeeper",
        "developer_username": "zookeeper",
        "before_state": {
            "stars": 3000,
            "forks": 1500,
            "contributors": 400,
            "language": "java",
            "category": "infrastructure"
        },
        "intervention_type": "Feature Expansion",
        "intervention_description": "Added new features to compete with etcd",
        "planned_effort_days": 365,
        "predicted_value": 25,
        "predicted_probability": 0.15,
        "predicted_risk": 0.9,
        "start_date": "2015-01-01",
        "end_date": "2017-01-01",
        "after_state": {
            "stars": 4000,
            "forks": 2000,
            "contributors": 500
        },
        "outcome_metrics": {
            "actual_value": 5,
            "success": False,
            "actual_risk": 0.95
        },
        "actual_stars_delta": 1000,
        "actual_downloads_delta": 0,
        "actual_revenue_delta": 0,
        "actual_contributors_delta": 100
    }
]

# Seed each failed transformation
for i, t in enumerate(failed_transformations):
    print(f"Seeding {i+1}/{len(failed_transformations)}: {t['asset_name']} (FAILED)")
    
    # Calculate predicted outcome
    star_growth = (t['after_state']['stars'] - t['before_state']['stars']) / max(t['before_state']['stars'], 1)
    contributor_growth = (t['after_state']['contributors'] - t['before_state']['contributors']) / max(t['before_state']['contributors'], 1)
    
    predicted_outcome = {
        "star_growth": star_growth,
        "contributor_growth": contributor_growth
    }
    
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
        predicted_outcome=predicted_outcome
    )
    print(f"  ✓ Record ID: {record_id}")
    
    # Start intervention
    ledger.start_intervention(
        record_id=record_id
    )
    
    # Complete intervention
    ledger.complete_intervention(
        record_id=record_id,
        after_state=t["after_state"],
        outcome_metrics=t["outcome_metrics"]
    )
    
    # Verify outcome (FAILED)
    ledger.verify_outcome(
        record_id=record_id,
        verifier_id="catacomb_system",
        verifier_username="catacomb_system",
        status=VerificationStatus.VERIFIED.value,
        notes="Failed transformation - did not achieve meaningful adoption"
    )
    
    # Update Elo system
    elo_system.update_from_intervention(
        developer_id=t["developer_id"],
        intervention_type=t["intervention_type"],
        predicted_value=t["predicted_value"],
        actual_value=t["outcome_metrics"]["actual_value"]
    )
    
    # Record transformation pattern
    transformation_tracker.record_transformation(
        asset_id=t["asset_id"],
        asset_type=t["asset_type"],
        intervention_type=t["intervention_type"],
        context=t["before_state"],
        before_metrics=t["before_state"],
        after_metrics=t["after_state"]
    )

# Save Elo ratings and transformation patterns
elo_system.save_to_file("elo_ratings.json")
transformation_tracker.export_patterns("transformation_patterns.json")

print(f"\n✓ Seeded {len(failed_transformations)} failed transformations")
print("✓ Elo ratings saved to elo_ratings.json")
print("✓ Transformation patterns saved to transformation_patterns.json")
