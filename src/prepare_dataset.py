import csv
import gzip
from pathlib import Path


RAW_FILE = Path("data/raw/wiki-Vote.txt.gz")
PROCESSED_DIR = Path("data/processed")

NODES_FILE = PROCESSED_DIR / "nodes.csv"
EDGES_FILE = PROCESSED_DIR / "edges.csv"


def prepare_dataset():
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

    nodes = set()
    edges = []

    with gzip.open(RAW_FILE, "rt", encoding="utf-8") as file:
        for line in file:
            line = line.strip()

            if not line or line.startswith("#"):
                continue

            source, target = line.split()

            source = int(source)
            target = int(target)

            nodes.add(source)
            nodes.add(target)
            edges.append((source, target))

    with NODES_FILE.open("w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["node_id"])

        for node_id in sorted(nodes):
            writer.writerow([node_id])

    with EDGES_FILE.open("w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["source", "target"])

        for source, target in edges:
            writer.writerow([source, target])

    print("Dataset preparation complete.")
    print(f"Nodes: {len(nodes)}")
    print(f"Relationships: {len(edges)}")
    print(f"Nodes file: {NODES_FILE}")
    print(f"Edges file: {EDGES_FILE}")


if __name__ == "__main__":
    prepare_dataset()