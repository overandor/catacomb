# Asset Embedding Model Architecture

## Purpose

Transform software repositories into latent innovation vectors that capture architectural depth, innovation patterns, and ecosystem position beyond surface GitHub signals.

## Model Architecture

### Input Features

#### 1. Surface Signals (Baseline)
- Stars, forks, commits, contributors
- Language, license, age
- CI presence, test presence
- README quality

#### 2. Architecture Features (The Moat)
- **Code Structure**: Module complexity, dependency depth, coupling metrics
- **Pattern Recognition**: Design patterns, architectural patterns, anti-patterns
- **Innovation Indicators**: Novel algorithms, unique abstractions, paradigm shifts
- **Domain Semantics**: Problem domain, solution approach, technical novelty
- **Ecosystem Position**: Upstream/downstream relationships, dependency graph centrality
- **Maintainer DNA**: Commit patterns, contribution velocity, expertise distribution

#### 3. Semantic Features
- README embeddings (topic modeling, technical depth)
- Code comment density and quality
- Documentation completeness
- API surface area and complexity
- Extension/plugin architecture presence

### Model Architecture

```
Input Layer (128 features)
    ↓
Feature Embedding Layer (256 dim)
    ↓
Architecture Encoder (512 dim)
    ↓
Semantic Encoder (512 dim)
    ↓
Ecosystem Encoder (256 dim)
    ↓
Fusion Layer (384 dim)
    ↓
Latent Innovation Vector (256 dim)
```

### Training Strategy

#### Phase 1: Self-Supervised Pre-training
- **Contrastive Learning**: Similar repos (same ecosystem, similar patterns) closer in embedding space
- **Masked Feature Prediction**: Predict masked architecture features
- **Temporal Consistency**: Embeddings should be stable over time for stable repos

#### Phase 2: Supervised Fine-tuning
- **Similarity Labels**: Pairs of repos known to be architecturally similar
- **Cluster Labels**: Innovation clusters (e.g., "software asset capital markets")
- **Outcome Labels**: Intervention success as similarity signal

### Embedding Dimensions

The 256-dimensional latent space should capture:

1. **Technical Novelty** (0-31): Algorithmic innovation, unique abstractions
2. **Architecture Maturity** (32-63): Code organization, patterns, best practices
3. **Ecosystem Centrality** (64-95): Dependency graph position, influence
4. **Domain Specificity** (96-127): Problem domain specialization
5. **Maintainer Quality** (128-159): Development practices, velocity
6. **Intervention Potential** (160-191): Susceptibility to value-adding interventions
7. **Ecosystem Fit** (192-223): How well it fits existing ecosystems
8. **Growth Trajectory** (224-255): Predicted adoption trajectory

### Similarity Metrics

#### Cosine Similarity
- General similarity for clustering
- Fast for nearest-neighbor search

#### Weighted Similarity
- Emphasize innovation dimensions for discovery
- Emphasize ecosystem dimensions for strategic analysis

#### Temporal Similarity
- Track embedding drift over time
- Detect architectural evolution

## Use Cases

### 1. Discovery Without Stars
Find projects similar to early-stage successes:

```python
# Find repos similar to early Supabase
supabase_embedding = get_embedding("supabase/supabase", timestamp="2020-01-01")
similar_repos = find_similar(supabase_embedding, k=10, time_window="2019-2021")
```

### 2. Innovation Cluster Detection
Discover ecosystems of related projects:

```python
# Cluster repos by innovation patterns
clusters = detect_innovation_clusters(embeddings, threshold=0.7)
# Returns: {
#   "Software Asset Capital Markets": ["DollarFS", "Collateral Token", "Provenance Engine"],
#   "ZK Proof Systems": ["BitNet", "LLM ZK Training SDK"],
#   ...
# }
```

### 3. Intervention Recommender Input
Asset genome for transformation path prediction:

```python
asset_genome = {
    "embedding": repo_embedding,
    "architecture_features": arch_features,
    "ecosystem_features": eco_features
}
transformation_paths = recommend_interventions(asset_genome)
```

### 4. Ecosystem Gap Analysis
Find missing pieces in innovation clusters:

```python
cluster = get_cluster("Software Asset Capital Markets")
missing_components = analyze_gaps(cluster)
# Returns: ["GitHub Scanner Product", "Developer Capitalization Dashboard"]
```

## Implementation Plan

### Phase 1: Feature Extraction
1. Extend `repo_scanner.py` with architecture features
2. Add code structure analysis (complexity, coupling)
3. Add pattern recognition (design patterns, anti-patterns)
4. Add dependency graph analysis (centrality, position)

### Phase 2: Model Training
1. Collect training dataset (10,000+ repos)
2. Implement contrastive learning pipeline
3. Train architecture encoder
4. Fine-tune with cluster labels

### Phase 3: Deployment
1. Embedding API endpoint
2. Similarity search service
3. Cluster detection pipeline
4. Visualization dashboard

### Phase 4: Integration
1. Replace surface-signal scoring with embedding-based scoring
2. Add cluster-aware recommendations
3. Ecosystem-level analysis

## Data Requirements

### Training Dataset
- **Minimum**: 10,000 repos
- **Ideal**: 100,000+ repos
- **Diversity**: Multiple ecosystems, languages, domains
- **Temporal**: Historical snapshots for temporal consistency

### Cluster Labels
- Manual labeling of known innovation clusters
- Community verification
- Continuous refinement

### Similarity Labels
- Expert-curated similar repo pairs
- Dependency-based similarity
- Topic-based similarity

## Evaluation Metrics

### Intrinsic
- **Clustering Quality**: Silhouette score, Davies-Bouldin index
- **Retrieval Quality**: Precision@k, MRR for similar repo retrieval
- **Temporal Stability**: Embedding drift over time

### Extrinsic
- **Discovery Quality**: Can we find early-stage successes?
- **Cluster Quality**: Do discovered clusters make semantic sense?
- **Intervention Accuracy**: Do embeddings improve intervention prediction?

## Proprietary Value

This model becomes the moat because:

1. **Hard to Replicate**: Requires custom architecture features, not just GitHub API
2. **Data Network Effect**: More interventions → better embeddings → better discovery
3. **Time-Dependent**: Historical embeddings required for temporal consistency
4. **Domain Expertise**: Cluster labeling requires software architecture expertise
5. **Feedback Loop**: Intervention outcomes improve embeddings, embeddings improve interventions

## Next Steps

1. Implement architecture feature extraction
2. Collect initial training dataset
3. Build contrastive learning pipeline
4. Train initial model
5. Deploy embedding API
6. Integrate with cluster detection
