import os

from dotenv import load_dotenv
from neo4j import GraphDatabase


load_dotenv()

HOST = os.environ["MEMGRAPH_HOST"]
PORT = os.environ["MEMGRAPH_PORT"]
USERNAME = os.environ["MEMGRAPH_USERNAME"]
PASSWORD = os.environ["MEMGRAPH_PASSWORD"]

URI = f"bolt+ssc://{HOST}:{PORT}"


def main():
    print("Connecting to Memgraph...")
    print(f"Host: {HOST}")
    print(f"Port: {PORT}")

    with GraphDatabase.driver(
        URI,
        auth=(USERNAME, PASSWORD),
    ) as driver:

        driver.verify_connectivity()

        records, _, _ = driver.execute_query(
            "RETURN 1 AS result"
        )

        print("Memgraph: CONNECTION SUCCESSFUL")
        print(f"Memgraph: Response = {records[0]['result']}")


if __name__ == "__main__":
    main()