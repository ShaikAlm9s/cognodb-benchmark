import csv
import os

import pyTigerGraph
from dotenv import load_dotenv


NODES_FILE = "data/processed/nodes.csv"
EDGES_FILE = "data/processed/edges.csv"
BATCH_SIZE = 500


def connect():
    load_dotenv()

    conn = pyTigerGraph.TigerGraphConnection(
        host=os.environ["TIGERGRAPH_HOST"],
        graphname=os.environ["TIGERGRAPH_GRAPH"],
        gsqlSecret=os.environ["TIGERGRAPH_SECRET"],
    )

    conn.getToken(os.environ["TIGERGRAPH_SECRET"])

    return conn


def load_vertices(conn):
    print()
    print("Loading User vertices...")

    rows = []

    with open(
        NODES_FILE,
        "r",
        newline="",
        encoding="utf-8",
    ) as file:
        reader = csv.DictReader(file)

        for row in reader:
            rows.append(
                (
                    str(row["node_id"]),
                    {},
                )
            )

    print(f"Vertices to load: {len(rows)}")

    total = 0

    for start in range(0, len(rows), BATCH_SIZE):
        batch = rows[start:start + BATCH_SIZE]

        written = 0

        for vertex_id, attributes in batch:
            written += conn.upsertVertex(
                "User",
                vertex_id,
                attributes,
            )

        total += written

        print(
            f"Vertex batch {start // BATCH_SIZE + 1}: "
            f"{written} written"
        )

    print(f"Total vertex upserts: {total}")


def load_edges(conn):
    print()
    print("Loading FOLLOWS edges...")

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
            f"Edge batch {start // BATCH_SIZE + 1}: "
            f"{written} written"
        )

    print(f"Total edge upserts: {total}")


def verify(conn):
    print()
    print("Verifying TigerGraph...")

    users = conn.getVertices(
        "User",
        limit=100000,
    )

    print(f"User vertices returned: {len(users)}")

    edges = conn.getEdges(
        "User",
        "30",
        edgeType="FOLLOWS",
    )

    print(
        f"Outgoing FOLLOWS edges from User 30: "
        f"{len(edges)}"
    )


def main():
    print("Connecting to TigerGraph...")

    conn = connect()

    try:
        load_vertices(conn)
        load_edges(conn)
        verify(conn)

        print()
        print("TigerGraph loading complete.")

    finally:
        try:
            conn.close()
        except Exception:
            pass


if __name__ == "__main__":
    main()
