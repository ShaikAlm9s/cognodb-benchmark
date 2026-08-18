from adapters.tigergraph import TigerGraphAdapter
from benchmark.runner import (
    run_read_workload,
    run_aggregation_workload,
    run_mixed_read_write,
    save_results,
)


NODE_IDS = [
    "5298",
    "5127",
    "5020",
    "4966",
    "4947",
]


def main():
    db = TigerGraphAdapter()

    try:
        print("Connecting to TigerGraph...")
        db.connect()

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
                    database_name="TigerGraph",
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
                database_name="TigerGraph",
                warmup_runs=10,
                measured_runs=100,
            )
        )

        results.append(
            run_mixed_read_write(
                database=db,
                database_name="TigerGraph",
                node_ids=NODE_IDS,
                workers=4,
                operations=40,
                seed=42,
            )
        )

        save_results(
            results,
            "tigergraph_results.csv",
        )

    finally:
        db.close()
        print()
        print("TigerGraph benchmark complete.")
        print("Connection closed.")


if __name__ == "__main__":
    main()