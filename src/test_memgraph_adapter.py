from adapters.memgraph import MemgraphAdapter


def main():
    db = MemgraphAdapter()

    try:
        print("Connecting to Memgraph...")
        db.connect()
        print("Connection successful.")

        print("Clearing test data...")
        db.clear()

        print("Creating test nodes...")
        db.load_nodes([1, 2, 3])

        print("Creating test relationships...")
        db.load_edges([
            (1, 2),
            (1, 3),
        ])

        print("Running point lookup...")
        print(db.point_lookup(1))

        print("Running 1-hop traversal...")
        print(db.traversal_1hop(1))

        print("Running aggregation...")
        print(db.aggregation())

        print("Memgraph adapter test completed successfully.")

    finally:
        if db.driver:
            db.clear()

        db.close()
        print("Test data removed.")
        print("Connection closed.")


if __name__ == "__main__":
    main()