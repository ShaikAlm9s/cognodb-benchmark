from adapters.falkordb import FalkorDBAdapter


def main():
    db = FalkorDBAdapter()

    try:
        print("Connecting to FalkorDB...")
        db.connect()

        node_result = db.graph.query(
            """
            MATCH (u:User)
            RETURN count(u) AS user_count
            """
        )

        edge_result = db.graph.query(
            """
            MATCH ()-[r:FOLLOWS]->()
            RETURN count(r) AS relationship_count
            """
        )

        user_count = node_result.result_set[0][0]
        relationship_count = edge_result.result_set[0][0]

        print(f"User nodes: {user_count}")
        print(
            f"FOLLOWS relationships: "
            f"{relationship_count}"
        )

    finally:
        db.close()
        print("Connection closed.")


if __name__ == "__main__":
    main()