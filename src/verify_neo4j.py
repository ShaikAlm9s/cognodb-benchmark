from adapters.neo4j import Neo4jAdapter


def main():
    db = Neo4jAdapter()

    try:
        print("Connecting to Neo4j...")
        db.connect()

        with db.driver.session(
            database=db.database
        ) as session:

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