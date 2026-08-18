import os

from dotenv import load_dotenv
from falkordb import FalkorDB

from adapters.base import GraphDatabaseAdapter


load_dotenv()


class FalkorDBAdapter(GraphDatabaseAdapter):

    def __init__(self):
        self.host = os.environ["FALKORDB_HOST"]
        self.port = int(os.environ["FALKORDB_PORT"])
        self.username = os.environ["FALKORDB_USERNAME"]
        self.password = os.environ["FALKORDB_PASSWORD"]

        self.client = None
        self.graph = None

    def connect(self):
        self.client = FalkorDB(
            host=self.host,
            port=self.port,
            username=self.username,
            password=self.password,
            ssl=False,
	socket_connect_timeout=10,
    	socket_timeout=30
        )

        self.graph = self.client.select_graph(
            "cognodb_benchmark"
        )

        self.graph.query(
            "RETURN 1"
        )

    def close(self):
        self.client = None
        self.graph = None

    def clear(self):
        self.graph.query(
            """
            MATCH (n)
            DETACH DELETE n
            """
        )

    def load_nodes(
        self,
        nodes,
        batch_size=1000,
    ):
        nodes = list(nodes)

        for start in range(
            0,
            len(nodes),
            batch_size,
        ):
            batch = nodes[
                start:start + batch_size
            ]

            query = """
            UNWIND $nodes AS node_id
            CREATE (:User {id: node_id})
            """

            self.graph.query(
                query,
                params={
                    "nodes": batch
                },
            )

    def load_edges(
        self,
        edges,
        batch_size=1000,
    ):
        edges = list(edges)

        for start in range(
            0,
            len(edges),
            batch_size,
        ):
            batch = edges[
                start:start + batch_size
            ]

            formatted_edges = [
                {
                    "source": source,
                    "target": target,
                }
                for source, target in batch
            ]

            query = """
            UNWIND $edges AS edge
            MATCH (source:User {id: edge.source})
            MATCH (target:User {id: edge.target})
            CREATE (source)-[:FOLLOWS]->(target)
            """

            self.graph.query(
                query,
                params={
                    "edges": formatted_edges
                },
            )

    def point_lookup(self, node_id):
        result = self.graph.query(
            """
            MATCH (u:User {id: $node_id})
            RETURN u.id AS id
            """,
            params={
                "node_id": node_id
            },
        )

        return result.result_set

    def traversal_1hop(self, node_id):
        result = self.graph.query(
            """
            MATCH (u:User {id: $node_id})
                  -[:FOLLOWS]->(v)
            RETURN count(DISTINCT v) AS result
            """,
            params={
                "node_id": node_id
            },
        )

        return result.result_set

    def traversal_2hop(self, node_id):
        result = self.graph.query(
            """
            MATCH (u:User {id: $node_id})
                  -[:FOLLOWS]->()
                  -[:FOLLOWS]->(v)
            RETURN count(DISTINCT v) AS result
            """,
            params={
                "node_id": node_id
            },
        )

        return result.result_set

    def traversal_3hop(self, node_id):
        result = self.graph.query(
            """
            MATCH (u:User {id: $node_id})
                  -[:FOLLOWS]->()
                  -[:FOLLOWS]->()
                  -[:FOLLOWS]->(v)
            RETURN count(DISTINCT v) AS result
            """,
            params={
                "node_id": node_id
            },
        )

        return result.result_set

    def filtered_lookup(self, node_id):
        result = self.graph.query(
            """
            MATCH (u:User)
            WHERE u.id = $node_id
            RETURN u.id AS id
            """,
            params={
                "node_id": node_id
            },
        )

        return result.result_set

    def aggregation(self):
        result = self.graph.query(
            """
            MATCH (u:User)
            RETURN count(u) AS user_count
            """
        )

        return result.result_set

    def write_test(
        self,
        source_id,
        target_id,
    ):
        result = self.graph.query(
            """
            MATCH (u:User {id: $source_id})
            MATCH (v:User {id: $target_id})
            MERGE (u)-[:BENCHMARK_WRITE]->(v)
            RETURN count(*) AS result
            """,
            params={
                "source_id": source_id,
                "target_id": target_id,
            },
        )

        return result.result_set