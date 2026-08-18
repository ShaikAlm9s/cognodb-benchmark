import os

from dotenv import load_dotenv
from neo4j import GraphDatabase


load_dotenv()

URI = os.environ["COGNODB_URI"]
USERNAME = os.environ["COGNODB_USERNAME"]
PASSWORD = os.environ["COGNODB_PASSWORD"]


def main():
    print("Connecting to CognoDB...")

    with GraphDatabase.driver(
        URI,
        auth=(USERNAME, PASSWORD),
    ) as driver:

        driver.verify_connectivity()

        records, summary, keys = driver.execute_query(
            "RETURN 1 AS result"
        )

        print("Connection successful.")
        print(f"Database response: {records[0]['result']}")


if __name__ == "__main__":
    main()