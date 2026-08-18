import os

import pyTigerGraph
from dotenv import load_dotenv


load_dotenv()


def main():
    host = os.environ["TIGERGRAPH_HOST"]
    graph = os.environ["TIGERGRAPH_GRAPH"]
    secret = os.environ["TIGERGRAPH_SECRET"]

    print("Connecting to TigerGraph...")
    print(f"Host: {host}")
    print(f"Graph: {graph}")

    conn = pyTigerGraph.TigerGraphConnection(
        host=host,
        graphname=graph,
        gsqlSecret=secret,
    )

    print("Generating authentication token...")
    conn.getToken(secret)

    print("Testing connection...")
    response = conn.echo()

    print("TigerGraph: CONNECTION SUCCESSFUL")
    print(f"TigerGraph response: {response}")


if __name__ == "__main__":
    main()