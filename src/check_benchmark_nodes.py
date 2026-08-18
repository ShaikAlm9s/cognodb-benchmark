from adapters.cognodb import CognoDBAdapter


NODE_IDS = [
    30,
    35,
    40,
    50,
    60,
]


def main():
    db = CognoDBAdapter()

    try:
        db.connect()

        print("Checking benchmark node IDs...")
        print()

        for node_id in NODE_IDS:
            result = db.point_lookup(node_id)

            if result:
                print(f"Node {node_id}: EXISTS")
            else:
                print(f"Node {node_id}: NOT FOUND")

    finally:
        db.close()


if __name__ == "__main__":
    main()