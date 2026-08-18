from adapters.cognodb import CognoDBAdapter
from benchmark.runner import (
    run_read_workload,
    run_aggregation_workload,
    run_mixed_read_write,
    save_results,
)


from benchmark.node_pool import get_benchmark_node_pool


def main():
    db = CognoDBAdapter()

    try:
        print("Connecting to CognoDB...")
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
            result = run_read_workload(
                database=db,
                database_name="CognoDB",
                workload_name=workload_name,
                operation=operation,
                node_ids=NODE_IDS,
                warmup_runs=10,
                measured_runs=100,
                seed=42,
            )

            results.append(result)

        results.append(
            run_aggregation_workload(
                database=db,
                database_name="CognoDB",
                warmup_runs=10,
                measured_runs=100,
            )
        )

        results.append(
            run_mixed_read_write(
                database=db,
                database_name="CognoDB",
                node_ids=NODE_IDS,
                workers=4,
                operations=40,
            )
        )

        save_results(
            results,
            "cognodb_results.csv",
        )

    finally:
        db.close()
        print()
        print("CognoDB benchmark complete.")
        print("Connection closed.")


if __name__ == "__main__":
    main()