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
        raise NotImplementedError(
            "TigerGraph benchmark data is managed by the "
            "dedicated loading scripts."
        )

    def load_nodes(self, nodes, batch_size=500):
        total = 0

        for node_id in nodes:
            total += self.conn.upsertVertex(
                "User",
                str(node_id),
                {"id": int(node_id)},
            )

        return total

    def load_edges(self, edges, batch_size=500):
        total = 0

        for start in range(0, len(edges), batch_size):
            batch = edges[start:start + batch_size]

            total += self.conn.upsertEdges(
                "User",
                "FOLLOWS",
                "User",
                [
                    (
                        str(source),
                        str(target),
                        {},
                    )
                    for source, target in batch
                ],
            )

        return total

    # ---------------------------------------------------------
    # Point lookup
    # ---------------------------------------------------------

    def point_lookup(self, node_id):
        return self.conn.getVerticesById(
            "User",
            [str(node_id)],
        )

    # ---------------------------------------------------------
    # 1-hop traversal
    # ---------------------------------------------------------

    def traversal_1hop(self, node_id):
        return self.conn.runInstalledQuery(
            "benchmark_1hop",
            {
                "p": {
                    "id": str(node_id),
                    "type": "User",
                }
            },
        )

    # ---------------------------------------------------------
    # 2-hop traversal
    # ---------------------------------------------------------

    def traversal_2hop(self, node_id):
        return self.conn.runInstalledQuery(
            "benchmark_2hop",
            {
                "p": {
                    "id": str(node_id),
                    "type": "User",
                }
            },
        )

    # ---------------------------------------------------------
    # 3-hop traversal
    # ---------------------------------------------------------

    def traversal_3hop(self, node_id):
        return self.conn.runInstalledQuery(
            "benchmark_3hop",
            {
                "p": {
                    "id": str(node_id),
                    "type": "User",
                }
            },
        )

    # ---------------------------------------------------------
    # Filtered lookup
    # ---------------------------------------------------------

    def filtered_lookup(self, node_id):
        vertices = self.conn.getVerticesById(
            "User",
            [str(node_id)],
        )

        return [
            vertex
            for vertex in vertices
            if vertex.get("v_type") == "User"
        ]

    # ---------------------------------------------------------
    # Aggregation
    # ---------------------------------------------------------

    def aggregation(self):
        vertices = self.conn.getVertices(
            "User",
            limit=100000,
        )

        return len(vertices)

    # ---------------------------------------------------------
    # Write operation
    # ---------------------------------------------------------

    def write_test(self, source_id, target_id):
        return self.conn.upsertEdge(
            "User",
            str(source_id),
            "FOLLOWS",
            "User",
            str(target_id),
            {},
        )