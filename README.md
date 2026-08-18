# CognoDB Benchmark

A reproducible comparative benchmark evaluating CognoDB against Neo4j, Memgraph, FalkorDB, and TigerGraph using the same Wiki-Vote graph dataset and a common workload and measurement framework.

## 1. Executive Summary

This project benchmarks five graph database systems:

- CognoDB
- Neo4j
- Memgraph
- FalkorDB
- TigerGraph

The benchmark evaluates seven graph-oriented workloads:

1. Point lookup
2. 1-hop traversal
3. 2-hop traversal
4. 3-hop traversal
5. Filtered lookup
6. Aggregation
7. Mixed read/write

The benchmark uses the Wiki-Vote dataset containing 7,115 vertices and 103,689 directed relationships.

Each read workload uses 10 warm-up iterations followed by 100 measured iterations with random seed 42. The mixed workload uses four workers executing 40 operations consisting of 20 reads and 20 writes.

Reported metrics include minimum latency, maximum latency, mean latency, P50 latency, P95 latency, and throughput.

The results are environment-specific measurements and should not be interpreted as universal rankings of the database systems.

## 2. Databases

| Database | Role |
|---|---|
| CognoDB | System under evaluation |
| Neo4j | Comparison system |
| Memgraph | Comparison system |
| FalkorDB | Comparison system |
| TigerGraph | Comparison system |

## 3. Dataset

The benchmark uses the Wiki-Vote graph dataset.

The processed dataset contains:

| Metric | Value |
|---|---:|
| Nodes | 7,115 |
| Directed relationships | 103,689 |
| Relationship type | FOLLOWS |
| Benchmark node type | User |

The dataset is stored in:

```text
data/
├── raw/
│   └── wiki-Vote.txt.gz
└── processed/
    ├── nodes.csv
    └── edges.csv
```

The dataset preparation script is:

```text
src/prepare_dataset.py
```

It converts the raw Wiki-Vote edge list into the processed node and edge CSV files.

### Dataset validation

The processed dataset contains 7,115 unique nodes and 103,689 directed relationships. The benchmark uses the same logical graph structure across the database adapters.

The processed files use the following schemas:

```text
nodes.csv
---------
node_id
```

```text
edges.csv
---------
source,target
```

## 4. Benchmark Workloads

### 4.1 Point Lookup

Retrieves a single vertex using its identifier.

This workload measures basic indexed or primary-key graph access.

### 4.2 1-Hop Traversal

Retrieves vertices directly connected to a selected source vertex through the `FOLLOWS` relationship.

### 4.3 2-Hop Traversal

Traverses two consecutive `FOLLOWS` relationships from the selected source vertex.

### 4.4 3-Hop Traversal

Traverses three consecutive `FOLLOWS` relationships from the selected source vertex.

### 4.5 Filtered Lookup

Performs a server-side filtered lookup for a selected vertex.

### 4.6 Aggregation

Counts graph vertices as an aggregation workload.

### 4.7 Mixed Read/Write

The mixed workload executes:

- 4 concurrent workers
- 40 total operations
- 20 read operations
- 20 write operations
- Random seed 42

This workload evaluates database behavior under concurrent mixed access rather than isolated read-only workloads.

## 5. Measurement Methodology

### Read workloads

Each read workload uses:

- 10 warm-up iterations
- 100 measured iterations
- Random seed 42

Warm-up measurements are excluded from the reported statistics.

The benchmark records:

- Minimum latency
- Maximum latency
- Mean latency
- P50 latency
- P95 latency
- Throughput in operations/second

### Mixed workload

The mixed workload uses:

- 4 workers
- 40 total operations
- 20 reads
- 20 writes
- Random seed 42

The database adapters implement equivalent logical workloads using the APIs and query mechanisms appropriate to each platform.

### Measurement interpretation

Latency values are measured at the benchmark client and therefore may include network and client/API overhead for managed database deployments.

Results should be interpreted as measurements of the complete tested client-to-database path rather than as isolated database-engine execution time.

## 6. Complete Results Matrix

Latency values are milliseconds. Throughput is operations/second.

### CognoDB

| Workload | Count | Min ms | Max ms | Mean ms | P50 ms | P95 ms | Throughput |
|---|---:|---:|---:|---:|---:|---:|---:|
| point_lookup | 100 | 239.042 | 569.943 | 256.173 | 243.018 | 299.975 | 3.904 |
| traversal_1hop | 100 | 239.876 | 309.179 | 251.071 | 243.398 | 297.515 | 3.983 |
| traversal_2hop | 100 | 240.188 | 340.738 | 251.276 | 246.842 | 267.143 | 3.980 |
| traversal_3hop | 100 | 239.746 | 1561.749 | 358.409 | 266.812 | 900.054 | 2.790 |
| filtered_lookup | 100 | 239.729 | 364.771 | 254.388 | 246.688 | 305.139 | 3.931 |
| aggregation | 100 | 237.899 | 426.914 | 251.439 | 245.847 | 279.470 | 3.977 |
| mixed_read_write | 40 | 240.311 | 1302.472 | 326.783 | 247.764 | 1238.020 | 11.732 |

### Neo4j

| Workload | Count | Min ms | Max ms | Mean ms | P50 ms | P95 ms | Throughput |
|---|---:|---:|---:|---:|---:|---:|---:|
| point_lookup | 100 | 84.294 | 313.390 | 108.492 | 88.789 | 178.018 | 9.217 |
| traversal_1hop | 100 | 84.284 | 832.730 | 105.567 | 88.450 | 162.152 | 9.472 |
| traversal_2hop | 100 | 84.215 | 201.899 | 97.680 | 88.086 | 155.303 | 10.237 |
| traversal_3hop | 100 | 84.592 | 336.049 | 104.387 | 89.728 | 160.615 | 9.579 |
| filtered_lookup | 100 | 84.138 | 203.594 | 100.089 | 88.276 | 158.297 | 9.991 |
| aggregation | 100 | 82.367 | 194.317 | 92.571 | 85.497 | 152.226 | 10.802 |
| mixed_read_write | 40 | 84.193 | 455.955 | 135.608 | 93.360 | 437.942 | 28.244 |

### Memgraph

| Workload | Count | Min ms | Max ms | Mean ms | P50 ms | P95 ms | Throughput |
|---|---:|---:|---:|---:|---:|---:|---:|
| point_lookup | 100 | 182.857 | 421.951 | 208.693 | 187.899 | 258.116 | 4.792 |
| traversal_1hop | 100 | 182.222 | 547.454 | 208.284 | 185.405 | 249.501 | 4.801 |
| traversal_2hop | 100 | 182.777 | 340.087 | 208.757 | 191.060 | 248.773 | 4.790 |
| traversal_3hop | 100 | 182.599 | 602.843 | 218.784 | 199.342 | 265.612 | 4.571 |
| filtered_lookup | 100 | 182.279 | 1377.009 | 301.663 | 203.608 | 857.127 | 3.315 |
| aggregation | 100 | 181.815 | 593.919 | 207.212 | 184.464 | 248.715 | 4.826 |
| mixed_read_write | 40 | 160.703 | 1532.060 | 322.351 | 239.439 | 1111.210 | 12.177 |

### FalkorDB

| Workload | Count | Min ms | Max ms | Mean ms | P50 ms | P95 ms | Throughput |
|---|---:|---:|---:|---:|---:|---:|---:|
| point_lookup | 100 | 22.824 | 390.174 | 56.999 | 33.186 | 133.205 | 17.543 |
| traversal_1hop | 100 | 22.799 | 162.427 | 43.610 | 24.708 | 89.568 | 22.929 |
| traversal_2hop | 100 | 23.127 | 137.197 | 47.313 | 26.586 | 88.213 | 21.134 |
| traversal_3hop | 100 | 22.931 | 137.401 | 47.833 | 28.044 | 88.253 | 20.905 |
| filtered_lookup | 100 | 22.927 | 136.285 | 46.808 | 24.577 | 88.919 | 21.362 |
| aggregation | 100 | 21.747 | 220.799 | 52.319 | 38.049 | 95.011 | 19.112 |
| mixed_read_write | 40 | 22.791 | 935.178 | 109.611 | 73.871 | 510.023 | 36.418 |

### TigerGraph

| Workload | Count | Min ms | Max ms | Mean ms | P50 ms | P95 ms | Throughput |
|---|---:|---:|---:|---:|---:|---:|---:|
| point_lookup | 100 | 247.320 | 1084.303 | 292.940 | 250.945 | 533.837 | 3.414 |
| traversal_1hop | 100 | 246.563 | 310.884 | 252.646 | 248.451 | 261.719 | 3.958 |
| traversal_2hop | 100 | 526.292 | 1196.521 | 610.359 | 589.887 | 741.904 | 1.638 |
| traversal_3hop | 100 | 509.265 | 687.908 | 579.413 | 573.992 | 670.212 | 1.726 |
| filtered_lookup | 100 | 246.874 | 335.760 | 264.148 | 255.778 | 316.011 | 3.786 |
| aggregation | 100 | 311.697 | 2227.550 | 433.931 | 343.016 | 749.473 | 2.304 |
| mixed_read_write | 40 | 263.024 | 1252.122 | 380.437 | 284.737 | 1194.672 | 9.947 |

## 7. Results Analysis

### 7.1 Read-heavy workloads

FalkorDB produced the lowest mean latency across all six read-oriented workloads in the submitted measurements.

Its mean latency ranged from approximately 43.6 ms to 57.0 ms across:

- Point lookup
- 1-hop traversal
- 2-hop traversal
- 3-hop traversal
- Filtered lookup
- Aggregation

Neo4j was the second strongest read performer, with mean latency ranging from approximately 92.6 ms to 108.5 ms across the six read workloads.

Memgraph produced mean latencies primarily around 207–219 ms, with filtered lookup increasing to approximately 301.7 ms.

CognoDB produced mean latencies from approximately 251.1 ms to 358.4 ms across the six read workloads.

TigerGraph showed the highest mean latency in several workloads, particularly the deeper traversal workloads.

### 7.2 Point lookup

FalkorDB recorded the lowest mean point-lookup latency:

```text
56.999 ms
```

followed by Neo4j:

```text
108.492 ms
```

Memgraph, CognoDB, and TigerGraph recorded higher mean latencies of approximately:

```text
208.693 ms
256.173 ms
292.940 ms
```

respectively.

### 7.3 Traversal workloads

FalkorDB maintained low mean latency as traversal depth increased:

```text
1-hop: 43.610 ms
2-hop: 47.313 ms
3-hop: 47.833 ms
```

Neo4j also remained relatively stable:

```text
1-hop: 105.567 ms
2-hop: 97.680 ms
3-hop: 104.387 ms
```

CognoDB showed a larger increase at 3-hop traversal:

```text
1-hop: 251.071 ms
2-hop: 251.276 ms
3-hop: 358.409 ms
```

TigerGraph showed the largest traversal latency among the submitted results:

```text
1-hop: 252.646 ms
2-hop: 610.359 ms
3-hop: 579.413 ms
```

### 7.4 Aggregation

FalkorDB recorded the lowest mean aggregation latency at:

```text
52.319 ms
```

Neo4j recorded:

```text
92.571 ms
```

Memgraph:

```text
207.212 ms
```

CognoDB:

```text
251.439 ms
```

TigerGraph:

```text
433.931 ms
```

### 7.5 Mixed read/write workload

The mixed workload produced a different but still consistent overall performance pattern.

FalkorDB recorded:

```text
Mean:       109.611 ms
P50:         73.871 ms
P95:        510.023 ms
Throughput:  36.418 ops/sec
```

Neo4j recorded:

```text
Mean:       135.608 ms
P50:         93.360 ms
P95:        437.942 ms
Throughput:  28.244 ops/sec
```

Memgraph recorded:

```text
Mean:       322.351 ms
P50:        239.439 ms
P95:       1111.210 ms
Throughput:  12.177 ops/sec
```

CognoDB recorded:

```text
Mean:       326.783 ms
P50:        247.764 ms
P95:       1238.020 ms
Throughput:  11.732 ops/sec
```

TigerGraph recorded:

```text
Mean:       380.437 ms
P50:        284.737 ms
P95:       1194.672 ms
Throughput:  9.947 ops/sec
```

FalkorDB therefore produced the highest mixed-workload throughput in the submitted measurements.

## 8. Overall Findings

Based on the submitted benchmark results:

1. FalkorDB produced the strongest overall read performance.
2. FalkorDB also produced the highest mixed read/write throughput.
3. Neo4j provided consistently strong performance across both read-heavy and mixed workloads.
4. Memgraph showed intermediate performance for most workloads.
5. CognoDB produced stable results for several simple workloads but had higher latency than FalkorDB and Neo4j.
6. CognoDB showed a larger P95 latency increase for 3-hop traversal and mixed workloads.
7. TigerGraph showed substantially higher latency for 2-hop and 3-hop traversal in the submitted run.

These findings describe the tested configurations and workload rather than universal characteristics of the database products.

## 9. Loading Metrics

The repository contains database-specific loading scripts.

However, the submitted result CSV files do not contain standardized loading measurements captured under the same controlled run for:

- Node loading time
- Relationship loading time
- Nodes/second
- Relationships/second
- Total load wall-clock time

These values are therefore reported as **not available** rather than estimated or reconstructed.

This is an identified limitation of the submitted benchmark.

The repository does contain loading implementations that can be used for future controlled measurement runs.

## 10. Resource and Fairness Considerations

The benchmark was executed using the available database deployments and the same benchmark client environment.

The benchmark attempts to maintain consistency in:

- Dataset
- Logical workloads
- Measurement counts
- Warm-up policy
- Random seed
- Client-side benchmark harness
- Reported metrics

However, exact infrastructure resources were not uniformly observable across all managed database providers.

Therefore, exact CPU, RAM, storage, and internal server configuration values are not asserted where they were not directly recorded.

The results should consequently be interpreted as environment-specific benchmark observations.

A fully controlled hardware comparison would require identical CPU, memory, storage, network, operating system, database version, configuration, and deployment region for all systems.

## 11. Benchmark Limitations and Caveats

The following limitations apply:

1. The benchmark compares database deployments whose underlying infrastructure may differ.
2. Exact CPU, RAM, storage, and server configuration were not uniformly observable.
3. Loading throughput was not captured as a standardized metric in the submitted result CSV files.
4. Network latency can contribute to measured request latency for managed deployments.
5. Database-specific query languages and APIs require adapter implementations that preserve equivalent logical workloads rather than identical query syntax.
6. Only one graph dataset is used.
7. The benchmark does not establish performance across all possible graph topologies.
8. The benchmark does not establish performance across all possible query patterns.
9. Read workloads use 100 measured iterations, while the mixed workload uses 40 operations.
10. Larger datasets and longer benchmark runs may produce different results.
11. Results are environment-specific and should not be treated as universal database rankings.
12. The submitted TigerGraph CSV represents the completed benchmark run and was not replaced by later query-validation experiments.

## 12. TigerGraph Validation

TigerGraph was validated using the benchmark `User` vertex type and `FOLLOWS` edge type.

The graph contains the expected benchmark schema:

```text
User
FOLLOWS
```

A direct edge lookup for User `30` returned five outgoing `FOLLOWS` relationships.

An installed TigerGraph `benchmark_1hop` query returned the same five destination vertices.

This confirmed that:

- The User vertices were loaded.
- The FOLLOWS relationships were loaded.
- The TigerGraph graph schema was accessible.
- Installed TigerGraph benchmark queries could execute successfully.
- A 1-hop traversal could be validated against direct edge retrieval.

The validation was performed after the submitted benchmark result file was generated and was used to verify the database state and query mechanism.

It did not replace the submitted TigerGraph benchmark result file.

## 13. Reproducibility

### Requirements

The project uses Python and a virtual environment.

Create the environment:

```powershell
python -m venv .venv
```

Activate it in PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

Install dependencies:

```powershell
pip install -r requirements.txt
```

Prepare the dataset:

```powershell
python src\prepare_dataset.py
```

### Database credentials

Database credentials are stored locally in `.env`.

The `.env` file is intentionally excluded from version control.

Do not commit database passwords, API keys, authentication tokens, or other credentials.

### Database connectivity

The repository contains database-specific connection and validation scripts.

Examples include:

```powershell
python src\test_connection.py
python src\test_databases.py
python src\test_tigergraph.py
```

Individual database adapters are located in:

```text
src/adapters/
```

### Running benchmark scripts

The database-specific benchmark entry points are:

```powershell
python src\benchmark_cognodb.py
python src\benchmark_neo4j.py
python src\benchmark_memgraph.py
python src\benchmark_falkordb.py
python src\benchmark_tigergraph.py
```

The resulting CSV files are stored in:

```text
results/
```

## 14. Benchmark Configuration

The benchmark configuration is stored in:

```text
config/benchmark.yaml
```

The benchmark code is organized into:

```text
src/
├── adapters/
├── benchmark/
└── workloads/
```

The adapters provide database-specific implementations while the benchmark runner provides common measurement logic.

## 15. Project Structure

```text
cognodb-benchmark/
├── analysis/
│   ├── cognodb_benchmark_analysis.xlsx
│   └── cognodb_benchmark_final_report.pdf
├── config/
│   └── benchmark.yaml
├── data/
│   ├── raw/
│   │   └── wiki-Vote.txt.gz
│   └── processed/
│       ├── nodes.csv
│       └── edges.csv
├── results/
│   ├── cognodb_results.csv
│   ├── falkordb_results.csv
│   ├── memgraph_results.csv
│   ├── neo4j_results.csv
│   └── tigergraph_results.csv
├── src/
│   ├── adapters/
│   ├── benchmark/
│   ├── workloads/
│   ├── benchmark_cognodb.py
│   ├── benchmark_falkordb.py
│   ├── benchmark_memgraph.py
│   ├── benchmark_neo4j.py
│   ├── benchmark_tigergraph.py
│   └── prepare_dataset.py
├── requirements.txt
├── README.md
└── .gitignore
```

## 16. Analysis Artifacts

### Excel analysis

```text
analysis/cognodb_benchmark_analysis.xlsx
```

The workbook contains the benchmark comparison and analysis data.

### Final report

```text
analysis/cognodb_benchmark_final_report.pdf
```

The PDF contains the consolidated benchmark report.

## 17. Security

Credentials and secrets are intentionally excluded from the repository.

The following should never be committed:

```text
.env
database credentials
API keys
authentication tokens
private keys
virtual environments
Python cache files
```

The repository uses `.gitignore` to prevent accidental tracking of sensitive and generated local files.

## 18. Reproducibility Notes

The benchmark uses a fixed random seed of:

```text
42
```

Read workloads use:

```text
10 warm-up iterations
100 measured iterations
```

Mixed workloads use:

```text
4 workers
40 total operations
20 reads
20 writes
```

The benchmark source code, dataset, result CSV files, analysis workbook, and final report are included in this repository.

## 19. Conclusion

Under the submitted benchmark conditions, FalkorDB produced the strongest overall performance for the read-heavy workloads and the highest mixed-workload throughput.

Neo4j also demonstrated consistently strong performance across the tested workloads.

Memgraph produced intermediate results, while CognoDB and TigerGraph showed higher latency across several workloads in the submitted measurements.

The benchmark demonstrates why graph database evaluation should use multiple workload categories instead of relying on a single query or latency measurement.

The results should be interpreted as reproducible measurements under the documented experimental conditions rather than universal rankings of graph database technologies.

Future work should capture standardized node-loading time, relationship-loading time, loading throughput, storage footprint, CPU usage, memory usage, and more tightly controlled hardware configurations for every database.

## 20. Repository

GitHub repository:

https://github.com/ShaikAlm9s/cognodb-benchmark