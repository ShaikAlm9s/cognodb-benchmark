import statistics
import time


def measure(operation):
    start = time.perf_counter()

    result = operation()

    elapsed = time.perf_counter() - start

    return result, elapsed * 1000


def percentile(values, percentage):
    if not values:
        return None

    sorted_values = sorted(values)

    index = (len(sorted_values) - 1) * (percentage / 100)

    lower = int(index)
    upper = min(lower + 1, len(sorted_values) - 1)

    weight = index - lower

    return (
        sorted_values[lower]
        + weight * (sorted_values[upper] - sorted_values[lower])
    )


def calculate_latency_metrics(latencies):
    if not latencies:
        return {
            "count": 0,
            "min_ms": None,
            "max_ms": None,
            "mean_ms": None,
            "p50_ms": None,
            "p95_ms": None,
        }

    return {
        "count": len(latencies),
        "min_ms": min(latencies),
        "max_ms": max(latencies),
        "mean_ms": statistics.mean(latencies),
        "p50_ms": percentile(latencies, 50),
        "p95_ms": percentile(latencies, 95),
    }