import os

import pyTigerGraph
from dotenv import load_dotenv


load_dotenv()


QUERIES = {
    "benchmark_1hop": """
CREATE QUERY benchmark_1hop(UINT node_id) FOR GRAPH Transaction_Fraud {
    Start = {User.*};
    Start = SELECT s
             FROM Start:s
             WHERE s == to_vertex(node_id, "User");

    Result = SELECT v
             FROM Start:s
             -(FOLLOWS)-> User:v;

    PRINT Result;
}
""",

    "benchmark_2hop": """
CREATE QUERY benchmark_2hop(UINT node_id) FOR GRAPH Transaction_Fraud {
    Start = {User.*};
    Start = SELECT s
             FROM Start:s
             WHERE s == to_vertex(node_id, "User");

    Hop1 = SELECT v
            FROM Start:s
            -(FOLLOWS)-> User:v;

    Hop2 = SELECT w
            FROM Hop1:v
            -(FOLLOWS)-> User:w;

    PRINT Hop2;
}
""",

    "benchmark_3hop": """
CREATE QUERY benchmark_3hop(UINT node_id) FOR GRAPH Transaction_Fraud {
    Start = {User.*};
    Start = SELECT s
             FROM Start:s
             WHERE s == to_vertex(node_id, "User");

    Hop1 = SELECT v
            FROM Start:s
            -(FOLLOWS)-> User:v;

    Hop2 = SELECT w
            FROM Hop1:v
            -(FOLLOWS)-> User:w;

    Hop3 = SELECT x
            FROM Hop2:w
            -(FOLLOWS)-> User:x;

    PRINT Hop3;
}
""",

    "benchmark_filtered": """
CREATE QUERY benchmark_filtered(UINT node_id) FOR GRAPH Transaction_Fraud {
    Start = {User.*};
    Result = SELECT u
             FROM Start:u
             WHERE u == to_vertex(node_id, "User");

    PRINT Result;
}
""",

    "benchmark_aggregation": """
CREATE QUERY benchmark_aggregation() FOR GRAPH Transaction_Fraud {
    Users = {User.*};
    Result = SELECT COUNT(*) AS user_count
             FROM Users:u;

    PRINT Result;
}
""",
}


def main():
    conn = pyTigerGraph.TigerGraphConnection(
        host=os.environ["TIGERGRAPH_HOST"],
        graphname=os.environ["TIGERGRAPH_GRAPH"],
        gsqlSecret=os.environ["TIGERGRAPH_SECRET"],
    )

    conn.getToken(os.environ["TIGERGRAPH_SECRET"])

    print("Creating TigerGraph benchmark queries...")

    for name, query in QUERIES.items():
        print()
        print(f"Creating: {name}")

        try:
            result = conn.createQuery(query)
            print(result)
        except Exception as exc:
            print(f"FAILED: {exc}")

    print()
    print("Installed query names:")
    print(conn.listQueryNames())


if __name__ == "__main__":
    main()
