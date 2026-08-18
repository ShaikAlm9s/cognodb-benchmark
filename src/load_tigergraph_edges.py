import csv
import os
import time

import pyTigerGraph
from dotenv import load_dotenv


EDGES_FILE = "data/processed/edges.csv"
BATCH_SIZE = 500


def main():
    load_dotenv()

    conn = pyTigerGraph.TigerGraphConnection(
        host=os.environ["TIGERGRAPH_HOST"],
        graphname=os.environ["TIGERGRAPH_GRAPH"],
        gsqlSecret=os.environ["TIGERGRAPH_SECRET"],
    )

    conn.getToken(os.environ["TIGERGRAPH_SECRET"])

    rows = []

    with open(
        EDGES_FILE,
        "r",
        newline="",
        encoding="utf-8",
    ) as file:
        reader = csv.DictReader(file)

        for row in reader:
            rows.append(
                (
                    str(row["source"]),
                    str(row["target"]),
                    {},
                )
            )

    print(f"Edges to load: {len(rows)}")
    print(f"Batch size: {BATCH_SIZE}")
    print()

    total = 0
    start_time = time.perf_counter()

    total_batches = (len(rows) + BATCH_SIZE - 1) // BATCH_SIZE

    for start in range(0, len(rows), BATCH_SIZE):
        batch = rows[start:start + BATCH_SIZE]

        written = conn.upsertEdges(
            "User",
            "FOLLOWS",
            "User",
            batch,
        )

        total += written

        processed = min(start + BATCH_SIZE, len(rows))

        print(
            f"Edge batch "
            f"{(start // BATCH_SIZE) + 1}/{total_batches}: "
            f"{processed}/{len(rows)} processed, "
            f"{written} written"
        )

    elapsed = time.perf_counter() - start_time

    print()
    print("TigerGraph edge loading complete.")
    print(f"Edges requested: {len(rows)}")
    print(f"Edges accepted: {total}")
    print(f"Elapsed time: {elapsed:.3f} seconds")

    if elapsed > 0:
        print(
            f"Relationship throughput: "
            f"{total / elapsed:.2f} edges/sec"
        )

    edges = conn.getEdges(
        "User",
        "30",
        edgeType="FOLLOWS",
    )

    print(
        f"User 30 outgoing FOLLOWS edges: "
        f"{len(edges)}"
    )

    conn.close()


if __name__ == "__main__":
    main()
