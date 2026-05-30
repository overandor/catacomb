#!/usr/bin/env python3
"""Seed 10,000 intervention records into the outcome ledger."""
import sqlite3
import json
import uuid
import random
from datetime import datetime, timedelta

REPOS = [
    "facebook/react", "vercel/next.js", "microsoft/vscode", "google/go", "rust-lang/rust",
    "nodejs/node", "python/cpython", "kubernetes/kubernetes", "tensorflow/tensorflow",
    "pytorch/pytorch", "apache/spark", "apache/kafka", "apache/flink", "redis/redis",
    "mongodb/mongo", "postgres/postgres", "sqlite/sqlite", "nginx/nginx", "apache/httpd",
    "docker/docker", "moby/moby", "kubernetes/minikube", "helm/helm", "prometheus/prometheus",
    "grafana/grafana", "istio/istio", "envoyproxy/envoy", "coredns/coredns", "etcd-io/etcd",
    "hashicorp/terraform", "hashicorp/vault", "hashicorp/consul", "hashicorp/nomad",
    "ansible/ansible", "chef/chef", "puppetlabs/puppet", "saltstack/salt",
    "elastic/elasticsearch", "elastic/logstash", "elastic/kibana", "apache/lucene",
    "apache/solr", "apache/nutch", "apache/hadoop", "apache/hive", "apache/pig",
    "apache/hbase", "apache/zookeeper", "apache/cassandra", "scylladb/scylla",
    "datastax/java-driver", "rethinkdb/rethinkdb", "couchbase/couchbase", "arangodb/arangodb",
    "neo4j/neo4j", "orientdb/orientdb", "influxdata/influxdb", "timescale/timescaledb",
    "questdb/questdb", "clickhouse/clickhouse", "druid-io/druid", "apache/pinot",
    "prestodb/presto", "trinodb/trino", "apache/drill", "apache/calcite",
    "apache/beam", "apache/samza", "apache/storm", "apache/apex",
    "dask/dask", "ray-project/ray", "modin-project/modin", "rapidsai/cudf",
    "rapidsai/cuml", "rapidsai/cugraph", "blazingdb/blazingsql", "xgboost/xgboost",
    "lightgbm/lightgbm", "catboost/catboost", "microsoft/LightGBM", "scikit-learn/scikit-learn",
    "scipy/scipy", "numpy/numpy", "pandas/pandas", "matplotlib/matplotlib",
    "jupyter/jupyter", "ipython/ipython", "nteract/nteract", "plotly/plotly.py",
    "bokeh/bokeh", "altair-viz/altair", "holoviz/holoviews", "streamlit/streamlit",
    "gradio-app/gradio", "huggingface/transformers", "huggingface/datasets",
    "openai/whisper", "openai/gpt-3", "anthropic/claude", "stability-ai/stablediffusion",
    "AUTOMATIC1111/stable-diffusion-webui", "comfyanonymous/ComfyUI", "lllyasviel/Fooocus",
    "oobabooga/text-generation-webui", "ggerganov/llama.cpp", "microsoft/DeepSpeed",
    "mosaicml/composer", "hpcaitech/ColossalAI", "bigscience/bloom", "meta-llama/llama",
    "meta-llama/llama2", "meta-llama/llama3", "mistralai/mistral", "01-ai/Yi",
    "QwenLM/Qwen", "baichuan-inc/baichuan", "THUDM/ChatGLM", "Cohee1207/SillyTavern",
    "SillyTavern/SillyTavern", "Azure/azure-sdk-for-python", "Azure/azure-sdk-for-js",
    "aws/aws-sdk-js", "aws/aws-sdk-java", "googleapis/google-api-python-client",
    "googleapis/google-cloud-go", "firebase/firebase-js-sdk", "supabase/supabase",
    "appwrite/appwrite", "parse-community/parse-server", "loopbackio/loopback-next",
    "nestjs/nest", "expressjs/express", "fastify/fastify", "hapijs/hapi",
    "koajs/koa", "sails/sails", "adonisjs/core", "feathersjs/feathers",
    "strapi/strapi", "directus/directus", "payloadcms/payload", "keystonejs/keystone",
    "prisma/prisma", "sequelize/sequelize", "typeorm/typeorm", "knex/knex",
    "bookshelf/bookshelf", "waterline/waterline", "mongoose/mongoose",
    "Automattic/mongoose", "mongodb/mongoose", "socketio/socket.io",
    "websockets/ws", "uNetworking/uWebSockets", "crossbario/crossbar",
    "zeromq/libzmq", "rabbitmq/rabbitmq-server", "celery/celery",
    "dramatiq/dramatiq", "huey/huey", "rq/rq", "agronholm/apscheduler",
    "schedule/schedule", "dbader/schedule", "tomerfiliba/plx",
    "pexpect/pexpect", "fabric/fabric", "paramiko/paramiko", "netmiko/netmiko",
    "napalm-automation/napalm", "ansible-community/ara", "Tower/tower-cli",
    "ansible/awx", "ansible/semaphore", "rundeck/rundeck", "jenkins/jenkins",
    "jenkinsci/jenkins", "hudson/hudson", "buildbot/buildbot", "drone/drone",
    "concourse/concourse", "spinnaker/spinnaker", "argoproj/argo-cd",
    "argoproj/argo-workflows", "tektoncd/pipeline", "knative/serving",
    "openfaas/faas", "openfaas/faas-netes", "kubeless/kubeless",
    "fission/fission", "nuclio/nuclio", "dapr/dapr", "open-telemetry/opentelemetry",
    "opentracing/opentracing-go", "jaegertracing/jaeger", "zipkin/zipkin",
    "linkerd/linkerd2", "projectcontour/contour", "kubernetes/ingress-nginx",
    "traefik/traefik", "emissary-ingress/emissary", "kong/kong", "apache/apisix",
    "3scale/apisonator", "zuul/zuul", "spring-cloud/spring-cloud-gateway",
    "netflix/zuul", "netflix/eureka", "netflix/hystrix", "netflix/ribbon",
    "resilience4j/resilience4j", "spring-projects/spring-boot",
    "spring-projects/spring-framework", "spring-projects/spring-security",
    "spring-projects/spring-data", "spring-projects/spring-batch",
    "micronaut-projects/micronaut-core", "quarkusio/quarkus", "eclipse-vertx/vert.x",
    "wildfly/wildfly", "jetty/jetty.project", "tomcat/tomcat", "undertow-io/undertow",
    "oracle/graal", "oracle/graaljs", "oracle/truffleruby", "jruby/jruby",
    "Shopify/bootsnap", "Shopify/liquid", "Shopify/toxiproxy", "stripe/stripe-ruby",
    "stripe/stripe-python", "stripe/stripe-go", "plaid/plaid-python", "dwolla/dwolla-swagger-ruby",
    "square/square-ruby-sdk", "braintree/braintree_python", "recurly/recurly-client-python",
    "chargebee/chargebee-python", "paddlehq/paddle-python-sdk", "pusher/pusher-http-python",
    "twilio/twilio-python", "sendgrid/sendgrid-python", "mailgun/mailgun-python",
    "postalserver/postal", "mailcow/mailcow-dockerized", "mail-in-a-box/mailinabox",
    "roundcube/roundcubemail", "RainLoop/rainloop-webmail", "snappy-mail/snappymail",
    "the-djmaze/snappymail", "freescout/freescout", "uvdesk/uvdesk",
    "osTicket/osTicket", "zammad/zammad", "frappe/frappe", "frappe/erpnext",
    "odoo/odoo", "Tryton/tryton", "apache/ofbiz", "apache/openejb",
    "WildFlySecurity/wildfly-elytron", "keycloak/keycloak", "casdoor/casdoor",
    "authelia/authelia", "oauth2-proxy/oauth2-proxy", "dexidp/dex",
    "ory/hydra", "ory/kratos", "ory/oathkeeper", "ory/keto",
    "casbin/casbin", "casbin/casbin-server", "permify/permify",
    "permify/permify-go", "openpolicyagent/opa", "styra/styra-das",
    "cedar/cedar", "google/zanzibar", "google/cel-spec", "bufbuild/buf",
    "protocolbuffers/protobuf", "google/flatbuffers", "capnproto/capnproto",
    "msgpack/msgpack-python", "pickle/pickle", "jsonpickle/jsonpickle",
    "orjson/orjson", "simdjson/simdjson", "rapidjson/rapidjson",
    "nlohmann/json", "taocpp/json", "boostorg/json", "cfeclipse/json",
    "FasterXML/jackson", "google/gson", "square/moshi", "square/retrofit",
    "reactivex/rxjava", "reactivex/rxjs", "reactivex/rxswift",
    "CombineSwift/Combine", "apple/swift-async-algorithms", "apple/swift-collections",
    "apple/swift-nio", "apple/swift-log", "vapor/vapor", "perfect/perfect",
    "kitura/kitura", "hummingbird-project/hummingbird", "tokio-rs/tokio",
    "async-rs/async-std", "crossbeam-rs/crossbeam", "rayon-rs/rayon",
    "dashmap/dashmap", "parking_lot/parking_lot", "Amanieu/hashbrown",
    "rust-lang/hashbrown", "servo/servo", "servo/webrender", "servo/ipc-channel",
    "gfx-rs/gfx", "gfx-rs/wgpu", "bevyengine/bevy", "amethyst/amethyst",
    "Fyrox/Fyrox", "godotengine/godot", "godot-rust/gdnative", "o3de/o3de",
    "cocos2d/cocos2d-x", "cocos/cocos-engine", "defold/defold", "love2d/love",
    "heapsio/heaps", "haxe/haxe", "openfl/openfl", "pixijs/pixijs",
    "threejs/three.js", "babylonjs/babylon.js", "playcanvas/engine",
    "aframevr/aframe", "mrdoob/three.js", "schteppe/cannon.js",
    "lo-th/Oimo.js", "kripken/ammo.js", "jMonkeyEngine/jmonkeyengine",
    "libgdx/libgdx", "MonoGame/MonoGame", "FNA-XNA/FNA", "love2d/love",
    "raylib/raylib", "libsdl-org/SDL", "glfw/glfw", "sfml/sfml",
    "allegro/allegro5", "liballeg/allegro", "ClanLib/ClanLib",
    "cocos2d/cocos2d-html5", "melonjs/melonJS", "phaser/phaser",
    "Impact/Impact", "crafty/Crafty", "excalibur/Excalibur",
    "pixijs/pixi.js", "GoodBoyDigital/pixi.js", "createjs/createjs",
    "greensock/GreenSock-JS", "Popmotion/popmotion", "framer/motion",
    "airbnb/lottie-web", "bodymovin/bodymovin", "haiku-ai/haiku",
    "rive-app/rive-react", "rive-app/rive-cpp", "rive-app/rive-ios",
    "rive-app/rive-android", "rive-app/rive-flutter", "rive-app/rive-js",
    "rive-app/rive-wasm", "rive-app/rive-rs", "rive-app/rive",
    "rive-app/rive-runtime", "rive-app/rive-renderer", "rive-app/rive-timeline",
    "rive-app/rive-text", "rive-app/rive-layout", "rive-app/rive-animation",
    "rive-app/rive-state-machine", "rive-app/rive-interactive",
    "rive-app/rive-gesture", "rive-app/rive-scroll", "rive-app/rive-responsive",
    "rive-app/rive-accessibility", "rive-app/rive-performance",
    "rive-app/rive-memory", "rive-app/rive-battery", "rive-app/rive-network",
    "rive-app/rive-offline", "rive-app/rive-pwa", "rive-app/rive-ssr",
    "rive-app/rive-csr", "rive-app/rive-isr", "rive-app/rive-edge",
    "rive-app/rive-cdn", "rive-app/rive-api", "rive-app/rive-cli",
    "rive-app/rive-studio", "rive-app/rive-player", "rive-app/rive-preview",
]

INTERVENTION_TYPES = [
    "api_launch", "performance_optimization", "security_hardening", "documentation_overhaul",
    "test_coverage", "ci_cd_pipeline", "dependency_update", "feature_extraction",
    "modularization", "containerization", "observability", "cost_optimization",
    "accessibility_improvement", "localization", "analytics_integration",
    "payment_integration", "auth_integration", "search_improvement",
    "caching_layer", "database_migration", "queue_system", "websocket_support",
    "graphql_migration", "grpc_adoption", "microservice_split", "serverless_migration",
    "edge_deployment", "multi_region", "disaster_recovery", "backup_system",
    "log_aggregation", "metrics_pipeline", "alerting_system", "sla_monitoring",
    "rate_limiting", "circuit_breaker", "bulkhead_pattern", "retry_logic",
    "idempotency", "event_sourcing", "cqrs_pattern", "saga_pattern",
    "outbox_pattern", "inbox_pattern", "change_data_capture", "streaming_pipeline",
    "batch_processing", "real_time_analytics", "ml_ops_pipeline", "feature_store",
    "model_registry", "experiment_tracking", "data_validation", "schema_evolution",
    "data_lineage", "quality_gates", "synthetic_data", "privacy_engineering",
    "federated_learning", "differential_privacy", "homomorphic_encryption",
    "zero_knowledge", "mpc_protocols", "threshold_signatures", "multi_party_computation",
]

STATUSES = ["planned", "in_progress", "completed", "verified", "failed"]
VERIFICATION_STATUSES = ["pending", "verified", "disputed"]


def random_date(start, end):
    delta = end - start
    return start + timedelta(seconds=random.randint(0, int(delta.total_seconds())))


def seed_db(target_count=10000):
    conn = sqlite3.connect("outcome_ledger.db")
    cursor = conn.cursor()

    # Count existing
    cursor.execute("SELECT COUNT(*) FROM interventions")
    existing = cursor.fetchone()[0]
    to_create = target_count - existing
    if to_create <= 0:
        print(f"Already have {existing} records. Target was {target_count}.")
        conn.close()
        return

    print(f"Creating {to_create} new intervention records...")

    now = datetime.now(datetime.now().astimezone().tzinfo).replace(tzinfo=None)
    start_date = now - timedelta(days=730)

    for i in range(to_create):
        record_id = str(uuid.uuid4())
        created = random_date(start_date, now)
        updated = random_date(created, now)
        repo = random.choice(REPOS)
        asset_id = repo
        asset_name = repo.split("/")[1]
        dev_id = f"dev_{random.randint(1,5000)}"
        dev_username = f"engineer{random.randint(1,5000)}"

        intervention_type = random.choice(INTERVENTION_TYPES)
        status = random.choice(STATUSES)
        verification_status = random.choice(VERIFICATION_STATUSES)
        if status in ("planned", "in_progress"):
            verification_status = "pending"

        planned_effort = random.randint(1, 90)
        actual_effort = planned_effort + random.randint(-10, 20) if status in ("completed", "verified", "failed") else None
        if actual_effort and actual_effort < 1:
            actual_effort = 1

        predicted_value = round(random.uniform(1000, 500000), 2)
        predicted_prob = round(random.uniform(0.3, 0.95), 2)
        predicted_risk = round(random.uniform(0.05, 0.8), 2)

        before_state = json.dumps({
            "stars": random.randint(100, 50000),
            "forks": random.randint(50, 10000),
            "issues": random.randint(10, 2000),
            "language": random.choice(["Python", "JavaScript", "Go", "Rust", "Java", "TypeScript", "C++", "Ruby"]),
            "last_commit_days": random.randint(1, 365),
            "bus_factor": random.randint(1, 10),
            "test_coverage": round(random.uniform(10, 95), 1),
            "documentation_score": round(random.uniform(20, 90), 1),
        })

        after_state = None
        outcome_metrics = None
        if status in ("completed", "verified", "failed"):
            after_state = json.dumps({
                "stars": random.randint(500, 100000),
                "forks": random.randint(100, 20000),
                "issues": random.randint(5, 1500),
                "language": random.choice(["Python", "JavaScript", "Go", "Rust", "Java", "TypeScript"]),
                "last_commit_days": random.randint(0, 30),
                "bus_factor": random.randint(2, 12),
                "test_coverage": round(random.uniform(40, 98), 1),
                "documentation_score": round(random.uniform(40, 95), 1),
            })
            actual_value = round(predicted_value * random.uniform(0.5, 1.8), 2)
            outcome_metrics = json.dumps({
                "actual_value": actual_value,
                "value_delta_percent": round(((actual_value - predicted_value) / predicted_value) * 100, 2),
                "effort_accuracy": round((planned_effort / actual_effort) * 100, 2) if actual_effort else 100,
                "adoption_rate": round(random.uniform(10, 95), 2),
                "user_satisfaction": round(random.uniform(3.0, 5.0), 2),
            })

        cursor.execute("""
            INSERT INTO interventions (
                record_id, created_at, updated_at, asset_id, asset_type, asset_name,
                developer_id, developer_username, before_state, before_hash,
                intervention_type, intervention_description, planned_effort_days,
                predicted_value, predicted_probability, predicted_risk, predicted_outcome,
                status, started_at, completed_at, actual_effort_days,
                after_state, after_hash, outcome_metrics,
                verification_status, verification_notes, prediction_accuracy, intervention_hash
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            record_id,
            created.isoformat(),
            updated.isoformat(),
            asset_id,
            "github_repo",
            asset_name,
            dev_id,
            dev_username,
            before_state,
            uuid.uuid4().hex[:32],
            intervention_type,
            f"{intervention_type.replace('_', ' ').title()} for {asset_name}",
            planned_effort,
            predicted_value,
            predicted_prob,
            predicted_risk,
            json.dumps({"expected_value": predicted_value, "confidence": predicted_prob}),
            status,
            random_date(created, updated).isoformat() if status != "planned" else None,
            random_date(created, updated).isoformat() if status in ("completed", "verified", "failed") else None,
            actual_effort,
            after_state,
            uuid.uuid4().hex[:32] if after_state else None,
            outcome_metrics,
            verification_status,
            f"Verified by {dev_username}" if verification_status == "verified" else None,
            json.dumps({"accuracy": round(random.uniform(0.6, 0.95), 2)}) if status == "verified" else None,
            uuid.uuid4().hex[:32],
        ))

        if (i + 1) % 1000 == 0:
            conn.commit()
            print(f"  ... {i + 1} records created")

    conn.commit()
    cursor.execute("SELECT COUNT(*) FROM interventions")
    total = cursor.fetchone()[0]
    print(f"Done. Total records in ledger: {total}")
    conn.close()


if __name__ == "__main__":
    seed_db(10000)
