import os

import pyTigerGraph
from dotenv import load_dotenv

from adapters.base import GraphDatabaseAdapter


load_dotenv()


class TigerGraphAdapter(GraphDatabaseAdapter):

    def __init__(self):
        self.host = os.environ["TIGERGRAPH_HOST"]
        self.graph = os.environ["TIGERGRAPH_GRAPH"]
        self.secret = os.environ["TIGERGRAPH_SECRET"]
        self.conn = None

    # ---------------------------------------------------------
    # Connection
    # ---------------------------------------------------------

    def connect(self):
        self.conn = pyTigerGraph.TigerGraphConnection(
            host=self.host,
            graphname=self.graph,
            gsqlSecret=self.secret,
        )

        self.conn.getToken(self.secret)

    def close(self):
        if self.conn is not None:
            try:
                self.conn.close()
            except Exception:
                pass

        self.conn = None

    # ---------------------------------------------------------
    # Data loading
    # ---------------------------------------------------------

    def clear(self):
        query = f"""
        INTERPRET QUERY () FOR GRAPH {self.graph} {{
            Users = {{User.*}};
            DELETE Users;
        }}
        """

        return self.conn.runInterpretedQuery(query)

    def load_nodes(self, nodes, batch_size=1000):
        count = 0

        for node_id in nodes:
            self.conn.upsertVertex(
                "User",
                str(node_id),
                {
                    "id": int(node_id),
                },
            )

            count += 1

        return count

    def load_edges(self, edges, batch_size=1000):
        count = 0

        for source_id, target_id in edges:
            self.conn.upsertEdge(
                "User",
                str(source_id),
                "FOLLOWS",
                "User",
                str(target_id),
                {},
            )

            count += 1

        return count

    # ---------------------------------------------------------
    # Helpers
    # ---------------------------------------------------------

    def _vertex_query(self, node_id, body):
        node_id = int(node_id)

        query = f"""
        INTERPRET QUERY () FOR GRAPH {self.graph} {{
            Start = {{to_vertex("{node_id}", "User")}};

            {body}
        }}
        """

        return self.conn.runInterpretedQuery(query)

    # ---------------------------------------------------------
    # Point lookup
    # ---------------------------------------------------------

    def point_lookup(self, node_id):
        return self.conn.getVerticesById(
            "User",
            [str(int(node_id))],
        )

    # ---------------------------------------------------------
    # 1-hop traversal
    # ---------------------------------------------------------

    def traversal_1hop(self, node_id):

        return self._vertex_query(
            node_id,
            """
            Result = SELECT v
                     FROM Start:u
                     -(FOLLOWS)-> User:v;

            PRINT Result;
            """,
        )

    # ---------------------------------------------------------
    # 2-hop traversal
    # ---------------------------------------------------------

    def traversal_2hop(self, node_id):

        return self._vertex_query(
            node_id,
            """
            Hop1 = SELECT v
                   FROM Start:u
                   -(FOLLOWS)-> User:v;

            Hop2 = SELECT w
                   FROM Hop1:v
                   -(FOLLOWS)-> User:w;

            PRINT Hop2;
            """,
        )

    # ---------------------------------------------------------
    # 3-hop traversal
    # ---------------------------------------------------------

    def traversal_3hop(self, node_id):

        return self._vertex_query(
            node_id,
            """
            Hop1 = SELECT v
                   FROM Start:u
                   -(FOLLOWS)-> User:v;

            Hop2 = SELECT w
                   FROM Hop1:v
                   -(FOLLOWS)-> User:w;

            Hop3 = SELECT x
                   FROM Hop2:w
                   -(FOLLOWS)-> User:x;

            PRINT Hop3;
            """,
        )

    # ---------------------------------------------------------
    # Filtered lookup
    # ---------------------------------------------------------

    def filtered_lookup(self, node_id):

        return self._vertex_query(
            node_id,
            """
            Result = SELECT u
                     FROM Start:u;

            PRINT Result;
            """,
        )

    # ---------------------------------------------------------
    # Aggregation
    # ---------------------------------------------------------

    def aggregation(self):

        query = f"""
        INTERPRET QUERY () FOR GRAPH {self.graph} {{
            Users = {{User.*}};

            UserCount = Users.size();

            PRINT UserCount;
        }}
        """

        return self.conn.runInterpretedQuery(query)

    # ---------------------------------------------------------
    # Write operation
    # ---------------------------------------------------------

    def write_test(self, source_id, target_id):

        return self.conn.upsertEdge(
            "User",
            str(int(source_id)),
            "BENCHMARK_WRITE",
            "User",
            str(int(target_id)),
            {},
        )
