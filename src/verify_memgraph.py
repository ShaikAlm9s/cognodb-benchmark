from adapters.memgraph import MemgraphAdapter


def main():
    db = MemgraphAdapter()

    try:
        print("Connecting to Memgraph...")
        db.connect()

        with db.driver.session() as session:

            node_result = session.run(
                """
                MATCH (u:User)
                RETURN count(u) AS count
                """
            ).single()

            edge_result = session.run(
                """
                MATCH (:User)-[:FOLLOWS]->(:User)
                RETURN count(*) AS count
                """
            ).single()

        print(f"User nodes: {node_result['count']}")
        print(
            f"FOLLOWS relationships: "
            f"{edge_result['count']}"
        )

    finally:
        db.close()
        print("Connection closed.")


if __name__ == "__main__":
    main()