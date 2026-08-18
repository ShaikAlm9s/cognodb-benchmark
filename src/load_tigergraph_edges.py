import csv
import os

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
                )
            )

    print(f"Edges to load: {len(rows)}")

    total = 0

    for start in range(0, len(rows), BATCH_SIZE):
        batch = rows[start:start + BATCH_SIZE]

        written = 0

        for source, target in batch:
            written += conn.upsertEdge(
                "User",
                source,
                "FOLLOWS",
                "User",
                target,
                {},
            )

        total += written

        print(
            f"Processed {min(start + BATCH_SIZE, len(rows))}"
            f"/{len(rows)} edges"
        )

    print()
    print(f"Total FOLLOWS upserts: {total}")

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
