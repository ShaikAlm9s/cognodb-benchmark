import csv
import time

from adapters.cognodb import CognoDBAdapter


NODES_FILE = "data/processed/nodes.csv"
EDGES_FILE = "data/processed/edges.csv"


def read_nodes():
    with open(NODES_FILE, "r", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for row in reader:
            yield int(row["node_id"])


def read_edges():
    with open(EDGES_FILE, "r", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for row in reader:
            yield (
                int(row["source"]),
                int(row["target"]),
            )


def main():
    db = CognoDBAdapter()

    try:
        print("Connecting to CognoDB...")
        db.connect()

        print("Clearing existing benchmark data...")
        db.clear()

        print("Loading nodes...")
        nodes = list(read_nodes())

        start = time.perf_counter()
        db.load_nodes(nodes)
        node_time = time.perf_counter() - start

        print(f"Loaded {len(nodes)} nodes in {node_time:.3f} seconds")

        print("Loading relationships...")
        edges = list(read_edges())

        start = time.perf_counter()
        db.load_edges(edges)
        edge_time = time.perf_counter() - start

        print(
            f"Loaded {len(edges)} relationships "
            f"in {edge_time:.3f} seconds"
        )

        print()
        print("Loading complete.")
        print(f"Nodes: {len(nodes)}")
        print(f"Relationships: {len(edges)}")

    finally:
        db.close()
        print("Connection closed.")


if __name__ == "__main__":
    main()