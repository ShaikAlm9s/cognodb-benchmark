import csv
import random


NODES_FILE = "data/processed/nodes.csv"

NODE_POOL_SIZE = 100
RANDOM_SEED = 42


def load_node_ids():
    with open(
        NODES_FILE,
        "r",
        encoding="utf-8",
    ) as file:
        reader = csv.DictReader(file)

        return [
            int(row["node_id"])
            for row in reader
        ]


def get_benchmark_node_pool(
    size=NODE_POOL_SIZE,
    seed=RANDOM_SEED,
):
    node_ids = load_node_ids()

    if len(node_ids) < size:
        raise ValueError(
            f"Dataset contains only "
            f"{len(node_ids)} nodes; "
            f"cannot create a pool of {size}."
        )

    rng = random.Random(seed)

    return rng.sample(
        node_ids,
        size,
    )