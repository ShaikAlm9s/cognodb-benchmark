from adapters.tigergraph import TigerGraphAdapter


def main():
    db = TigerGraphAdapter()

    try:
        print("Connecting to TigerGraph...")
        db.connect()

        print("Connection successful.")

        print("Testing point lookup...")
        result = db.point_lookup("5298")
        print(result)

        print("Testing 1-hop traversal...")
        result = db.traversal_1hop("5298")
        print(result)

        print("Testing 2-hop traversal...")
        result = db.traversal_2hop("5298")
        print(f"Returned {len(result)} results")

        print("Testing 3-hop traversal...")
        result = db.traversal_3hop("5298")
        print(f"Returned {len(result)} results")

        print("Testing filtered lookup...")
        result = db.filtered_lookup("5298")
        print(result)

        print("Testing aggregation...")
        result = db.aggregation()
        print(result)

        print()
        print("TigerGraph adapter test completed successfully.")

    finally:
        db.close()
        print("Connection closed.")


if __name__ == "__main__":
    main()