import os

from dotenv import load_dotenv
from falkordb import FalkorDB


load_dotenv()


def main():
    host = os.environ["FALKORDB_HOST"]
    port = int(os.environ["FALKORDB_PORT"])
    username = os.environ["FALKORDB_USERNAME"]
    password = os.environ["FALKORDB_PASSWORD"]

    print("Connecting to FalkorDB...")
    print(f"Host: {host}")
    print(f"Port: {port}")

    db = FalkorDB(
        host=host,
        port=port,
        username=username,
        password=password,
    )

    graph = db.select_graph("benchmark_test")

    result = graph.query(
        "RETURN 1 AS result"
    )

    print("FalkorDB: CONNECTION SUCCESSFUL")
    print(f"FalkorDB: Response = {result.result_set[0][0]}")


if __name__ == "__main__":
    main()