\# CognoDB Benchmark



A reproducible benchmark comparing CognoDB with Neo4j, Memgraph, FalkorDB, and TigerGraph across common graph-database workloads.



\## 1. Overview



This project evaluates the performance of five graph database systems using the same benchmark dataset, workload definitions, measurement procedure, and reporting metrics.



The benchmark focuses on latency and throughput for graph-oriented operations including point lookups, multi-hop traversals, filtered lookups, aggregation, and mixed read/write workloads.



\### Databases



\- CognoDB

\- Neo4j

\- Memgraph

\- FalkorDB

\- TigerGraph



\## 2. Dataset



The benchmark uses the Wiki-Vote graph dataset.



The project contains the raw and processed dataset files:



```text

data/

├── raw/

│   └── wiki-Vote.txt.gz

└── processed/

&#x20;   ├── nodes.csv

&#x20;   └── edges.csv

