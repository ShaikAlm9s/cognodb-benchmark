import csv
import random
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

from benchmark.metrics import measure, calculate_latency_metrics


RESULTS_DIR = Path("results")

# Fixed seed makes the benchmark reproducible.
RANDOM_SEED = 42

# Final benchmark configuration.
DEFAULT_WARMUP_RUNS = 10
DEFAULT_MEASURED_RUNS = 100


def build_node_sequence(
    node_ids,
    count,
    seed=RANDOM_SEED,
):
    """
    Build a reproducible randomized sequence of benchmark
    start nodes.

    The same seed produces the same sequence for every
    database, ensuring that each database receives the same
    logical workload.
    """

    if not node_ids:
        raise ValueError("node_ids cannot be empty")

    rng = random.Random(seed)

    return [
        rng.choice(node_ids)
        for _ in range(count)
    ]


def run_read_workload(
    database,
    database_name,
    workload_name,
    operation,
    node_ids,
    warmup_runs=DEFAULT_WARMUP_RUNS,
    measured_runs=DEFAULT_MEASURED_RUNS,
    seed=RANDOM_SEED,
):
    print()
    print("=" * 60)
    print(f"Database: {database_name}")
    print(f"Workload: {workload_name}")
    print("=" * 60)

    if not node_ids:
        raise ValueError("node_ids cannot be empty")

    node_sequence = build_node_sequence(
        node_ids,
        warmup_runs + measured_runs,
        seed=seed,
    )

    warmup_nodes = node_sequence[:warmup_runs]
    measured_nodes = node_sequence[
        warmup_runs:
    ]

    print(f"Random seed: {seed}")
    print(f"Warm-up runs: {warmup_runs}")

    for node_id in warmup_nodes:
        operation(node_id)

    print(f"Measured runs: {measured_runs}")

    latencies = []

    total_start = time.perf_counter()

    for node_id in measured_nodes:

        _, elapsed_ms = measure(
            lambda node_id=node_id:
            operation(node_id)
        )

        latencies.append(elapsed_ms)

    total_elapsed = (
        time.perf_counter() - total_start
    )

    metrics = calculate_latency_metrics(
        latencies
    )

    throughput = (
        measured_runs / total_elapsed
        if total_elapsed > 0
        else 0
    )

    metrics["throughput_ops_sec"] = throughput

    print(
        f"Min:        "
        f"{metrics['min_ms']:.3f} ms"
    )

    print(
        f"Mean:       "
        f"{metrics['mean_ms']:.3f} ms"
    )

    print(
        f"P50:        "
        f"{metrics['p50_ms']:.3f} ms"
    )

    print(
        f"P95:        "
        f"{metrics['p95_ms']:.3f} ms"
    )

    print(
        f"Max:        "
        f"{metrics['max_ms']:.3f} ms"
    )

    print(
        f"Throughput: "
        f"{throughput:.3f} ops/sec"
    )

    return {
        "database": database_name,
        "workload": workload_name,
        **metrics,
    }


def run_aggregation_workload(
    database,
    database_name,
    warmup_runs=DEFAULT_WARMUP_RUNS,
    measured_runs=DEFAULT_MEASURED_RUNS,
):
    print()
    print("=" * 60)
    print(f"Database: {database_name}")
    print("Workload: aggregation")
    print("=" * 60)

    print(f"Warm-up runs: {warmup_runs}")

    for _ in range(warmup_runs):
        database.aggregation()

    print(f"Measured runs: {measured_runs}")

    latencies = []

    total_start = time.perf_counter()

    for _ in range(measured_runs):

        _, elapsed_ms = measure(
            database.aggregation
        )

        latencies.append(elapsed_ms)

    total_elapsed = (
        time.perf_counter() - total_start
    )

    metrics = calculate_latency_metrics(
        latencies
    )

    throughput = (
        measured_runs / total_elapsed
        if total_elapsed > 0
        else 0
    )

    metrics["throughput_ops_sec"] = throughput

    print(
        f"Min:        "
        f"{metrics['min_ms']:.3f} ms"
    )

    print(
        f"Mean:       "
        f"{metrics['mean_ms']:.3f} ms"
    )

    print(
        f"P50:        "
        f"{metrics['p50_ms']:.3f} ms"
    )

    print(
        f"P95:        "
        f"{metrics['p95_ms']:.3f} ms"
    )

    print(
        f"Max:        "
        f"{metrics['max_ms']:.3f} ms"
    )

    print(
        f"Throughput: "
        f"{throughput:.3f} ops/sec"
    )

    return {
        "database": database_name,
        "workload": "aggregation",
        **metrics,
    }


def run_mixed_read_write(
    database,
    database_name,
    node_ids,
    workers=4,
    operations=40,
    seed=RANDOM_SEED,
):
    print()
    print("=" * 60)
    print(f"Database: {database_name}")
    print("Workload: mixed_read_write")
    print("=" * 60)

    if not node_ids:
        raise ValueError("node_ids cannot be empty")

    rng = random.Random(seed)

    # Warm-up reads.
    for _ in range(10):
        node_id = rng.choice(node_ids)
        database.point_lookup(node_id)

    def execute_operation(index):

        source_id = rng.choice(node_ids)
        target_id = rng.choice(node_ids)

        start = time.perf_counter()

        if index % 2 == 0:

            database.point_lookup(
                source_id
            )

            operation_type = "read"

        else:

            database.write_test(
                source_id,
                target_id,
            )

            operation_type = "write"

        elapsed_ms = (
            time.perf_counter() - start
        ) * 1000

        return operation_type, elapsed_ms

    print(f"Random seed: {seed}")
    print(f"Workers: {workers}")
    print(f"Operations: {operations}")

    results = []

    total_start = time.perf_counter()

    with ThreadPoolExecutor(
        max_workers=workers
    ) as executor:

        futures = [
            executor.submit(
                execute_operation,
                i,
            )
            for i in range(operations)
        ]

        for future in as_completed(futures):
            results.append(
                future.result()
            )

    total_elapsed = (
        time.perf_counter() - total_start
    )

    all_latencies = [
        elapsed
        for _, elapsed in results
    ]

    metrics = calculate_latency_metrics(
        all_latencies
    )

    throughput = (
        operations / total_elapsed
        if total_elapsed > 0
        else 0
    )

    reads = [
        elapsed
        for operation_type, elapsed
        in results
        if operation_type == "read"
    ]

    writes = [
        elapsed
        for operation_type, elapsed
        in results
        if operation_type == "write"
    ]

    print(f"Reads:       {len(reads)}")
    print(f"Writes:      {len(writes)}")

    print(
        f"Mean:        "
        f"{metrics['mean_ms']:.3f} ms"
    )

    print(
        f"P50:         "
        f"{metrics['p50_ms']:.3f} ms"
    )

    print(
        f"P95:         "
        f"{metrics['p95_ms']:.3f} ms"
    )

    print(
        f"Throughput:  "
        f"{throughput:.3f} ops/sec"
    )

    return {
        "database": database_name,
        "workload": "mixed_read_write",
        **metrics,
        "throughput_ops_sec": throughput,
        "read_operations": len(reads),
        "write_operations": len(writes),
        "workers": workers,
    }


def save_results(results, filename):

    RESULTS_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    output_file = (
        RESULTS_DIR / filename
    )

    fieldnames = [
        "database",
        "workload",
        "count",
        "min_ms",
        "max_ms",
        "mean_ms",
        "p50_ms",
        "p95_ms",
        "throughput_ops_sec",
        "read_operations",
        "write_operations",
        "workers",
    ]

    with output_file.open(
        "w",
        newline="",
        encoding="utf-8",
    ) as file:

        writer = csv.DictWriter(
            file,
            fieldnames=fieldnames,
            extrasaction="ignore",
        )

        writer.writeheader()
        writer.writerows(results)

    print()
    print(
        f"Results saved to: "
        f"{output_file}"
    )