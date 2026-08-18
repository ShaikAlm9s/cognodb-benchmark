import os

from dotenv import load_dotenv
from neo4j import GraphDatabase


load_dotenv()


def test_database(name, uri, username, password, database):
    print(f"\nTesting {name}...")

    try:
        with GraphDatabase.driver(
            uri,
            auth=(username, password),
        ) as driver:

            driver.verify_connectivity()

            records, _, _ = driver.execute_query(
                "RETURN 1 AS result",
                database_=database,
            )

            print(f"{name}: CONNECTION SUCCESSFUL")
            print(f"{name}: Response = {records[0]['result']}")

    except Exception as error:
        print(f"{name}: CONNECTION FAILED")
        print(f"Error: {error}")


def main():
    test_database(
        "CognoDB",
        os.environ["COGNODB_URI"],
        os.environ["COGNODB_USERNAME"],
        os.environ["COGNODB_PASSWORD"],
        "neo4j",
    )

    test_database(
        "Neo4j AuraDB",
        os.environ["NEO4J_URI"],
        os.environ["NEO4J_USERNAME"],
        os.environ["NEO4J_PASSWORD"],
        os.environ["NEO4J_DATABASE"],
    )


if __name__ == "__main__":
    main()