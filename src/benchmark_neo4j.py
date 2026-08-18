from adapters.neo4j import Neo4jAdapter
from benchmark.runner import (
    run_read_workload,
    run_aggregation_workload,
    run_mixed_read_write,
    save_results,
)


from benchmark.node_pool import get_benchmark_node_pool


def main():
    db = Neo4jAdapter()

    try:
        print("Connecting to Neo4j...")
        db.connect()
        NODE_IDS = get_benchmark_node_pool()

        results = []


        workloads = [
            (
                "point_lookup",
                db.point_lookup,
            ),
            (
                "traversal_1hop",
                db.traversal_1hop,
            ),
            (
                "traversal_2hop",
                db.traversal_2hop,
            ),
            (
                "traversal_3hop",
                db.traversal_3hop,
            ),
            (
                "filtered_lookup",
                db.filtered_lookup,
            ),
        ]

        for workload_name, operation in workloads:
            results.append(
                run_read_workload(
                    database=db,
                    database_name="Neo4j",
                    workload_name=workload_name,
                    operation=operation,
                    node_ids=NODE_IDS,
                    warmup_runs=10,
                    measured_runs=100,
                    seed=42,
                )
            )

        results.append(
            run_aggregation_workload(
                database=db,
                database_name="Neo4j",
                warmup_runs=10,
                measured_runs=100,
            )
        )

        results.append(
            run_mixed_read_write(
                database=db,
                database_name="Neo4j",
                node_ids=NODE_IDS,
                workers=4,
                operations=40,
            )
        )

        save_results(
            results,
            "neo4j_results.csv",
        )

    finally:
        db.close()
        print()
        print("Neo4j benchmark complete.")
        print("Connection closed.")


if __name__ == "__main__":
    main()