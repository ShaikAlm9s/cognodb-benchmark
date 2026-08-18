from adapters.falkordb import FalkorDBAdapter
from benchmark.runner import (
    run_read_workload,
    run_aggregation_workload,
    run_mixed_read_write,
    save_results,
)
from benchmark.node_pool import get_benchmark_node_pool


def main():
    db = FalkorDBAdapter()

    try:
        print("Connecting to FalkorDB...")
        db.connect()

        node_ids = get_benchmark_node_pool()

        results = []

        workloads = [
            ("point_lookup", db.point_lookup),
            ("traversal_1hop", db.traversal_1hop),
            ("traversal_2hop", db.traversal_2hop),
            ("traversal_3hop", db.traversal_3hop),
            ("filtered_lookup", db.filtered_lookup),
        ]

        for workload_name, operation in workloads:
            results.append(
                run_read_workload(
                    database=db,
                    database_name="FalkorDB",
                    workload_name=workload_name,
                    operation=operation,
                    node_ids=node_ids,
                    warmup_runs=10,
                    measured_runs=100,
                    seed=42,
                )
            )

        results.append(
            run_aggregation_workload(
                database=db,
                database_name="FalkorDB",
                warmup_runs=10,
                measured_runs=100,
            )
        )

        results.append(
            run_mixed_read_write(
                database=db,
                database_name="FalkorDB",
                node_ids=node_ids,
                workers=4,
                operations=40,
                seed=42,
            )
        )

        save_results(
            results,
            "falkordb_results.csv",
        )

    finally:
        db.close()
        print()
        print("FalkorDB benchmark complete.")
        print("Connection closed.")


if __name__ == "__main__":
    main()