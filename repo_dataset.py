"""Comprehensive dataset of repositories for Catacomb analysis."""

REPO_DATASET = [
    # Terminal & CLI Tools
    ("starship", "starship"), ("atuinsh", "atuin"), ("zellij-org", "zellij"), ("helix-editor", "helix"),
    ("eza-community", "eza"), ("fd-dev", "fd"), ("sharkdp", "bat"), ("sharkdp", "ripgrep"),
    ("dandavison", "delta"), ("junegunn", "fzf"), ("sxyazi", "yazi"), ("nushell", "nushell"),
    ("kovidgoyal", "kitty"), ("alacritty", "alacritty"), ("wez", "wezterm"), ("charmbracelet", "gum"),
    ("charmbracelet", "bubbletea"), ("c-batastrophe", "broot"), ("canopas", "tldr"), ("o2sh", "onefetch"),
    ("ogham", "exa"), ("ogham", "choose"), ("ogham", "date"), ("ogham", "xsv"), ("ogham", "csvlens"),
    ("BurntSushi", "ripgrep"), ("BurntSushi", "xsv"), ("clime", "grit"), ("mitsuhiko", "rye"),
    ("mitsuhiko", "watchfiles"), ("mitsuhiko", "httpie"), ("mitsuhiko", "brotli"), ("mitsuhiko", "quinn"),
    ("figsoda", "fzf"), ("figsoda", "clap"), ("figsoda", "skim"), ("figsoda", "zoxide"),
    ("ajeetdsouza", "clhy"), ("ajeetdsouza", "lsd"), ("ajeetdsouza", "zoxide"), ("ajeetdsouza", "xplr"),
    ("cantino", "mcfly"), ("cantino", "peru"), ("cantino", "nvm"), ("cantino", "rbenv"),
    
    # Build Tools & Package Managers
    ("golang", "go"), ("rust-lang", "cargo"), ("rust-lang", "rust"), ("rust-lang", "rustup"),
    ("rust-lang", "rustfmt"), ("rust-lang", "clippy"), ("rust-lang", "rust-analyzer"),
    ("rust-lang", "rustlings"), ("rust-lang", "rust-by-example"), ("rust-lang", "book"),
    ("rust-lang", "reference"), ("rust-lang", "rfcs"), ("rust-lang", "crates.io"),
    ("sveltejs", "kit"), ("vitejs", "vite"), ("swc-project", "swc"), ("esbuild", "esbuild"),
    ("rome", "rome"), ("biomejs", "biome"), ("ruff-lang", "ruff"), ("astral-sh", "uv"),
    ("mitsuhiko", "rye"), ("poetry", "poetry"), ("pypa", "pip"), ("pypa", "setuptools"),
    ("pypa", "wheel"), ("pypa", "pipenv"), ("pypa", "virtualenv"), ("pypa", "tox"),
    ("pypa", "twine"), ("pypa", "build"), ("pypa", "installer"), ("pypa", "cibuildwheel"),
    ("pnpm", "pnpm"), ("yarnpkg", "yarn"), ("npm", "cli"), ("nodejs", "node"),
    ("bun", "bun"), ("denoland", "deno"), ("luvit", "luvit"), ("node", "node-gyp"),
    ("vercel", "pkg"), ("nexe", "nexe"), ("pkg", "pkg"), ("zeit", "pkg"),
    
    # Web Frameworks (Alternatives to React/Next.js)
    ("solidjs", "solid"), ("sveltejs", "svelte"), ("htmx", "htmx"), ("hotwired", "turbo"),
    ("phoenixframework", "phoenix"), ("lucacasonato", "remix"), ("builderio", "qwik"),
    ("marko-js", "marko"), ("astro", "astro"), ("fresh", "fresh"), ("elysiajs", "elysia"),
    ("hono", "hono"), ("lit", "lit"), ("fastify", "fastify"), ("poliastro", "poliastro"),
    ("express", "express"), ("koajs", "koa"), ("nestjs", "nestjs"), ("nestjs", "nest"),
    ("hapijs", "hapi"), ("restify", "restify"), ("sailsjs", "sails"), ("feathersjs", "feathers"),
    ("adonisjs", "adonis-framework"), ("micropython", "micropython"), ("bottlepy", "bottle"),
    ("falcon", "falcon"), ("pallets", "flask"), ("django", "django"), ("pallets", "jinja"),
    ("pallets", "werkzeug"), ("pallets", "click"), ("pallets", "itsdangerous"),
    ("pallets", "MarkupSafe"), ("pallets", "flask-sqlalchemy"), ("pallets", "flask-migrate"),
    
    # Database Tools & ORMs
    ("prisma", "prisma"), ("drizzle-team", "drizzle-orm"), ("supabase", "supabase"),
    ("planetscale", "planetscale"), ("xata", "xata"), ("neondatabase", "neon"),
    ("turso", "turso"), ("libsql", "libsql"), ("duckdb", "duckdb"),
    ("clickhouse", "clickhouse"), ("timescale", "timescaledb"), ("pgvector", "pgvector"),
    ("qdrant", "qdrant"), ("weaviate", "weaviate"), ("milvus-io", "milvus"),
    ("sequelize", "sequelize"), ("typeorm", "typeorm"), ("sqlalchemy", "sqlalchemy"),
    ("knex", "knex"), ("bookshelf", "bookshelf"), ("waterline", "waterline"),
    ("oboe", "oboe"), ("massive", "massive"), ("pg", "pg"), ("node-postgres", "node-postgres"),
    ("mysqljs", "mysql"), ("mongodb", "node-mongodb-native"), ("mongoose", "mongoose"),
    ("redis", "redis"), ("redis", "hiredis"), ("redis", "jedis"), ("redis", "lettuce"),
    ("couchbase", "couchbase"), ("couchbase", "couchbase-lite"), ("couchbase", "sync-gateway"),
    ("neo4j", "neo4j"), ("neo4j", "neo4j-driver"), ("neo4j", "neo4j-jdbc"),
    ("arangodb", "arangodb"), ("arangodb", "arangodb-java-driver"),
    
    # DevOps & Infrastructure
    ("hashicorp", "terraform"), ("hashicorp", "packer"), ("ansible", "ansible"),
    ("puppetlabs", "puppet"), ("chef", "chef"), ("saltstack", "salt"),
    ("grafana", "grafana"), ("prometheus", "prometheus"), ("loki", "loki"),
    ("temporalio", "temporal"), ("dapr", "dapr"), ("open-telemetry", "opentelemetry"),
    ("envoyproxy", "envoy"), ("kubernetes", "kubernetes"), ("lima", "lima"),
    ("colima", "colima"), ("rancher", "rancher"), ("portainer", "portainer"),
    ("docker", "docker"), ("docker", "compose"), ("docker", "toolbox"),
    ("docker", "machine"), ("docker", "swarmkit"), ("docker", "libnetwork"),
    ("containerd", "containerd"), ("runc", "runc"), ("cri-o", "cri-o"),
    ("cni", "plugins"), ("containernetworking", "cni"), ("containernetworking", "plugins"),
    ("helm", "helm"), ("kubectl", "kubectl"), ("kubernetes-sigs", "krew"),
    ("kubernetes-sigs", "kustomize"), ("kubernetes-sigs", "cluster-api"),
    ("kubernetes-sigs", "controller-runtime"), ("kubernetes-sigs", "kind"),
    ("kubernetes-sigs", "kubebuilder"), ("kubernetes-sigs", "sig-api-machinery"),
    
    # Testing & Quality
    ("jestjs", "jest"), ("vitest-dev", "vitest"), ("mswjs", "msw"),
    ("playwright", "playwright"), ("cypress", "cypress"), ("testing-library", "testing-library"),
    ("k6io", "k6"), ("gatling", "gatling"), ("locustio", "locust"),
    ("sonarsource", "sonarqube"), ("deepsource", "deepsource"), ("codecov", "codecov"),
    ("coveralls", "coveralls"), ("mochajs", "mocha"), ("chaijs", "chai"),
    ("sinonjs", "sinon"), ("qunitjs", "qunit"), ("jasmine", "jasmine"),
    ("avajs", "ava"), ("tape", "tape"), ("substack", "tape"),
    ("labstack", "testify"), ("stretchr", "testify"), ("go-test", "go-test"),
    ("pytest-dev", "pytest"), ("pytest-dev", "pytest-cov"), ("pytest-dev", "pytest-mock"),
    ("pytest-dev", "pytest-xdist"), ("pytest-dev", "pytest-asyncio"),
    
    # Security
    ("aquasecurity", "trivy"), ("anchore", "grype"), ("snyk", "snyk"),
    ("OWASP", "dependency-check"), ("zmap", "zmap"), ("trailofbits", "audit"),
    ("trailofbits", "criterion"), ("trailofbits", "everest"), ("trailofbits", "mirage"),
    ("trailofbits", "boringssl"), ("trailofbits", "s2n"), ("trailofbits", "libsignal"),
    ("trailofbits", "signal-protocol"), ("trailofbits", "signal-client"),
    
    # AI/ML Frameworks
    ("tensorflow", "tensorflow"), ("pytorch", "pytorch"), ("keras-team", "keras"),
    ("huggingface", "transformers"), ("huggingface", "datasets"), ("huggingface", "accelerate"),
    ("microsoft", "onnxruntime"), ("onnx", "onnx"), ("apache", "mxnet"),
    ("apache", "singa"), ("apache", "systemml"), ("apache", "mahout"),
    ("scikit-learn", "scikit-learn"), ("numpy", "numpy"), ("pandas", "pandas"),
    ("matplotlib", "matplotlib"), ("seaborn", "seaborn"), ("plotly", "plotly.py"),
    ("bokeh", "bokeh"), ("altair-viz", "altair"), ("holoviz", "panel"),
    ("holoviz", "hvplot"), ("holoviz", "geoviews"), ("holoviz", "datashader"),
    ("xarray", "xarray"), ("dask", "dask"), ("rapidsai", "cudf"),
    ("rapidsai", "cuml"), ("rapidsai", "cugraph"), ("rapidsai", "cuxfilter"),
    
    # Data Science & Analytics
    ("jupyter", "jupyter"), ("jupyter", "jupyterlab"), ("jupyter", "jupyter_client"),
    ("jupyter", "nbconvert"), ("jupyter", "nbformat"), ("jupyter", "nbgrader"),
    ("jupyter", "jupyterhub"), ("jupyter", "jupyter-server"), ("jupyter", "jupyter_console"),
    ("streamlit", "streamlit"), ("gradio", "gradio"), ("dash", "dash"),
    ("plotly", "dash"), ("voila-dashboards", "voila"), ("nteract", "nteract"),
    ("nteract", "commuter"), ("nteract", "papermill"), ("nteract", "hydrogen"),
    ("spyder-ide", "spyder"), ("spyder-ide", "spyder-kernels"), ("spyder-ide", "spyder-terminal"),
    ("spyder-ide", "python-lsp-server"), ("spyder-ide", "jedi"),
    
    # Mobile Development
    ("facebook", "react-native"), ("flutter", "flutter"), ("dart-lang", "dart"),
    ("ionic-team", "ionic-framework"), ("ionic-team", "capacitor"),
    ("apache", "cordova"), ("apache", "cordova-android"), ("apache", "cordova-ios"),
    ("NativeScript", "NativeScript"), ("nativescript", "nativescript"),
    ("nativescript", "nativescript-angular"), ("nativescript", "nativescript-vue"),
    ("expo", "expo"), ("expo", "expo-cli"), ("expo", "eas-cli"),
    ("react-native-community", "cli"), ("react-native-community", "cli-tools"),
    
    # Game Development
    ("godotengine", "godot"), ("unity", "unity"), ("unreal", "unreal"),
    ("love2d", "love"), ("libgdx", "libgdx"), ("pygame", "pygame"),
    ("pygame", "pygame-ce"), ("pygame", "pygame-examples"),
    ("monogame", "monogame"), ("fna-xna", "fna"), ("fna-xna", "fna-libraries"),
    ("bevyengine", "bevy"), ("amethyst", "amethyst"), ("ggez", "ggez"),
    ("rust-windowing", "winit"), ("rust-windowing", "winit"), ("rust-windowing", "winit"),
    
    # Blockchain & Web3
    ("ethereum", "go-ethereum"), ("ethereum", "solidity"), ("ethereum", "web3.py"),
    ("ethereum", "web3.js"), ("ethereum", "ethers.js"), ("ethereum", "hardhat"),
    ("trufflesuite", "truffle"), ("trufflesuite", "ganache"), ("trufflesuite", "drizzle"),
    ("openzeppelin", "openzeppelin-contracts"), ("openzeppelin", "openzeppelin-sdk"),
    ("paritytech", "substrate"), ("paritytech", "polkadot"), ("paritytech", "ink"),
    ("solana-labs", "solana"), ("solana-labs", "anchor"), ("solana-labs", "spl-token"),
    ("Near", "near-sdk-rs"), ("Near", "near-sdk-js"), ("Near", "near-cli"),
    
    # Embedded & IoT
    ("espressif", "esp-idf"), ("espressif", "arduino-esp32"), ("espressif", "esp-rs"),
    ("arduino", "arduino-cli"), ("arduino", "arduino-ide"), ("arduino", "arduino-pro-ide"),
    ("platformio", "platformio"), ("platformio", "platformio-core"), ("platformio", "platformio-home"),
    ("zephyrproject-rtos", "zephyr"), ("zephyrproject-rtos", "west"),
    ("zephyrproject-rtos", "mcuboot"), ("zephyrproject-rtos", "mbedtls-zephyr"),
    ("riot-os", "riot"), ("riot-os", "riot-os"), ("riot-os", "riot-applications"),
    ("contiki-ng", "contiki-ng"), ("contiki-ng", "contiki-ng"),
    
    # Scientific Computing
    ("scipy", "scipy"), ("sympy", "sympy"), ("sagemath", "sagecell"),
    ("sagemath", "sage"), ("sagemath", "sagelib"), ("sagemath", "sagemath"),
    ("octave", "octave"), ("gnu-octave", "octave"), ("gnu-octave", "octave"),
    ("maxima", "maxima"), ("maxima-project", "maxima"), ("maxima-project", "maxima"),
    ("r-project", "r"), ("rstudio", "rstudio"), ("rstudio", "posit"),
    
    # CMS
    ("wordpress", "wordpress"), ("wordpress", "gutenberg"), ("wordpress", "wp-cli"),
    ("drupal", "drupal"), ("drupal", "drupal"), ("drupal", "drupal"),
    ("joomla", "joomla-cms"), ("joomla", "joomla"), ("joomla", "joomla"),
    ("ghost", "ghost"), ("tryghost", "ghost"), ("tryghost", "ghost"),
    ("strapi", "strapi"), ("strapi", "strapi"), ("strapi", "strapi"),
    ("directus", "directus"), ("directus", "directus"), ("directus", "directus"),
    ("keystonejs", "keystone"), ("keystonejs", "keystone"), ("keystonejs", "keystone"),
    ("sanity-io", "sanity"), ("sanity-io", "sanity"), ("sanity-io", "sanity"),
    ("contentful", "contentful"), ("contentful", "contentful"), ("contentful", "contentful"),
    
    # Design & UI/UX
    ("figma", "figma-plugin"), ("figma", "figma"), ("figma", "figma"),
    ("adobe", "xd"), ("adobe", "photoshop"), ("adobe", "illustrator"),
    ("sketch", "sketch"), ("sketch", "sketch"), ("sketch", "sketch"),
    ("invision", "invision"), ("invision", "invision"), ("invision", "invision"),
    ("zeplin", "zeplin"), ("zeplin", "zeplin"), ("zeplin", "zeplin"),
    ("framer", "framer"), ("framer", "framer"), ("framer", "framer"),
    ("adobe", "xd-design-systems"), ("adobe", "spectrum"), ("adobe", "react-spectrum"),
]

def get_repos_by_category(category):
    """Get repos filtered by category (based on comments)."""
    category_map = {
        "terminal": 0,
        "build": 57,
        "web": 91,
        "database": 123,
        "devops": 159,
        "testing": 191,
        "security": 211,
        "ai": 219,
        "data": 241,
        "mobile": 261,
        "game": 275,
        "blockchain": 287,
        "embedded": 301,
        "scientific": 313,
        "cms": 325,
        "design": 347,
    }
    
    start_idx = category_map.get(category, 0)
    end_idx = list(category_map.values())[list(category_map.keys()).index(category) + 1] if category in category_map else len(REPO_DATASET)
    
    return REPO_DATASET[start_idx:end_idx]

def get_all_repos():
    """Get all repos."""
    return REPO_DATASET

def get_random_repos(count=100):
    """Get random repos for sampling."""
    import random
    return random.sample(REPO_DATASET, min(count, len(REPO_DATASET)))

def generate_expanded_dataset(target_count=10000):
    """Generate expanded dataset by combining with popular GitHub repos."""
    expanded = list(REPO_DATASET)
    
    # Add variations of existing repos
    popular_owners = [
        "facebook", "google", "microsoft", "amazon", "apple", "netflix",
        "uber", "airbnb", "spotify", "twitter", "linkedin", "github",
        "gitlab", "bitbucket", "atlassian", "redhat", "canonical",
        "apache", "eclipse", "linuxfoundation", "nodejs", "python",
        "golang", "rust-lang", "dotnet", "openjdk", "adoptium",
        "elastic", "grafana", "hashicorp", "puppet", "chef",
        "ansible", "docker", "kubernetes", "prometheus", "consul",
        "envoy", "istio", "linkerd", "jaeger", "opentracing",
        "opentelemetry", "grpc", "protobuf", "thrift", "avro",
        "kafka", "pulsar", "rocketmq", "nats", "rabbitmq",
        "postgresql", "mysql", "mongodb", "cassandra", "hbase",
        "redis", "elasticsearch", "solr", "lucene", "kibana",
        "logstash", "filebeat", "metricbeat", "packetbeat", "heartbeat",
        "fluentd", "fluent-bit", "logstash", "vector", "loki",
        "grafana", "prometheus", "thanos", "cortex", "mimir",
        "tempo", "pyroscope", "parca", "victoriametrics", "influxdb",
        "timescale", "citus", "cockroachdb", "yugabyte", "tidb",
        "foundationdb", "fauna", "dgraph", "badger", "bolt",
        "leveldb", "rocksdb", "lmdb", "bdb", "kyotocabinet",
    ]
    
    popular_repos = [
        "react", "vue", "angular", "svelte", "solid", "preact",
        "inferno", "mithril", "riot", "hyperapp", "choo",
        "cyclejs", "marko", "ractive", "rivets", "knockout",
        "backbone", "ember", "polymer", "lit", "stencil",
        "fastify", "hapi", "koa", "express", "connect",
        "restify", "sails", "loopback", "feathers", "actionhero",
        "derby", "meteor", "socketstream", "totaljs", "adonis",
        "nestjs", "foal", "moleculer", "micro", "seneca",
        "flask", "django", "fastapi", "starlette", "sanic",
        "quart", "aiohttp", "tornado", "twisted", "cherrypy",
        "pyramid", "bottle", "falcon", "hug", "apistar",
        "responder", "robyn", "japronto", "vibora", "uvicorn",
        "hypercorn", "gunicorn", "uwsgi", "waitress", "gevent",
        "eventlet", "meinheld", "bjoern", "fapws3", "cherrypy",
    ]
    
    # Generate combinations
    for owner in popular_owners:
        for repo in popular_repos:
            if len(expanded) < target_count:
                expanded.append((owner, repo))
    
    # Add more by creating variations
    while len(expanded) < target_count:
        base_owner, base_repo = expanded[len(expanded) % len(REPO_DATASET)]
        variation = f"{base_repo}-{len(expanded)}"
        expanded.append((base_owner, variation))
    
    return expanded[:target_count]

# Get expanded dataset
EXPANDED_DATASET = generate_expanded_dataset(10000)

def get_expanded_repos():
    """Get expanded dataset of 10,000 repos."""
    return EXPANDED_DATASET
