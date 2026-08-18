import csv
from pathlib import Path


NODES_FILE = Path("data/processed/nodes.csv")
EDGES_FILE = Path("data/processed/edges.csv")


def main():
    nodes = set()

    with NODES_FILE.open("r", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for row in reader:
            nodes.add(int(row["node_id"]))

    edges = []
    unique_edges = set()
    self_loops = 0

    with EDGES_FILE.open("r", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for row in reader:
            source = int(row["source"])
            target = int(row["target"])

            edge = (source, target)

            edges.append(edge)
            unique_edges.add(edge)

            if source == target:
                self_loops += 1

    duplicate_edges = len(edges) - len(unique_edges)

    print("Dataset validation")
    print("------------------")
    print(f"Nodes: {len(nodes)}")
    print(f"Relationships: {len(edges)}")
    print(f"Unique relationships: {len(unique_edges)}")
    print(f"Duplicate relationships: {duplicate_edges}")
    print(f"Self-loops: {self_loops}")

    print()
    print("Validation complete.")


if __name__ == "__main__":
    main()