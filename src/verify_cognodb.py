from adapters.cognodb import CognoDBAdapter


def main():
    db = CognoDBAdapter()

    try:
        print("Connecting to CognoDB...")
        db.connect()

        with db.driver.session(database="neo4j") as session:

            node_result = session.run(
                "MATCH (u:User) RETURN count(u) AS count"
            ).single()

            edge_result = session.run(
                """
                MATCH (:User)-[:FOLLOWS]->(:User)
                RETURN count(*) AS count
                """
            ).single()

        print(f"User nodes: {node_result['count']}")
        print(f"FOLLOWS relationships: {edge_result['count']}")

    finally:
        db.close()
        print("Connection closed.")


if __name__ == "__main__":
    main()