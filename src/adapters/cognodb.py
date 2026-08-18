import os

from dotenv import load_dotenv
from neo4j import GraphDatabase

from adapters.base import GraphDatabaseAdapter


load_dotenv()


class CognoDBAdapter(GraphDatabaseAdapter):

    def __init__(self):
        self.uri = os.environ["COGNODB_URI"]
        self.username = os.environ["COGNODB_USERNAME"]
        self.password = os.environ["COGNODB_PASSWORD"]

        self.driver = None

    def connect(self):
        self.driver = GraphDatabase.driver(
            self.uri,
            auth=(self.username, self.password),
        )

        self.driver.verify_connectivity()

    def close(self):
        if self.driver:
            self.driver.close()
            self.driver = None

    def clear(self):
        query = """
        MATCH (n)
        DETACH DELETE n
        """

        with self.driver.session(database="neo4j") as session:
            session.run(query).consume()

    def load_nodes(self, nodes, batch_size=1000):
        query = """
        UNWIND $nodes AS node_id
        CREATE (:User {id: node_id})
        """

        nodes = list(nodes)

        with self.driver.session(database="neo4j") as session:
            for start in range(0, len(nodes), batch_size):
                batch = nodes[start:start + batch_size]

                session.run(
                    query,
                    nodes=batch,
                ).consume()

    def load_edges(self, edges, batch_size=1000):
        query = """
        UNWIND $edges AS edge
        MATCH (source:User {id: edge.source})
        MATCH (target:User {id: edge.target})
        CREATE (source)-[:FOLLOWS]->(target)
        """

        edges = list(edges)

        with self.driver.session(database="neo4j") as session:
            for start in range(0, len(edges), batch_size):
                batch = edges[start:start + batch_size]

                formatted_edges = [
                    {
                        "source": source,
                        "target": target,
                    }
                    for source, target in batch
                ]

                session.run(
                    query,
                    edges=formatted_edges,
                ).consume()

    def point_lookup(self, node_id):
        query = """
        MATCH (u:User {id: $node_id})
        RETURN u.id AS id
        """

        with self.driver.session(database="neo4j") as session:
            return session.run(
                query,
                node_id=node_id,
            ).data()

    def traversal_1hop(self, node_id):
        query = """
        MATCH (u:User {id: $node_id})-[:FOLLOWS]->(v)
        RETURN count(DISTINCT v) AS result
        """

        with self.driver.session(database="neo4j") as session:
            return session.run(
                query,
                node_id=node_id,
            ).data()

    def traversal_2hop(self, node_id):
        query = """
        MATCH (u:User {id: $node_id})
              -[:FOLLOWS]->()
              -[:FOLLOWS]->(v)
        RETURN count(DISTINCT v) AS result
        """

        with self.driver.session(database="neo4j") as session:
            return session.run(
                query,
                node_id=node_id,
            ).data()

    def traversal_3hop(self, node_id):
        query = """
        MATCH (u:User {id: $node_id})
              -[:FOLLOWS]->()
              -[:FOLLOWS]->()
              -[:FOLLOWS]->(v)
        RETURN count(DISTINCT v) AS result
        """

        with self.driver.session(database="neo4j") as session:
            return session.run(
                query,
                node_id=node_id,
            ).data()

    def filtered_lookup(self, node_id):
        query = """
        MATCH (u:User)
        WHERE u.id = $node_id
        RETURN u.id AS id
        """

        with self.driver.session(database="neo4j") as session:
            return session.run(
                query,
                node_id=node_id,
            ).data()

    def aggregation(self):
        query = """
        MATCH (u:User)
        RETURN count(u) AS user_count
        """

        with self.driver.session(database="neo4j") as session:
            return session.run(query).data()

    def write_test(self, source_id, target_id):
        query = """
        MATCH (u:User {id: $source_id})
        MATCH (v:User {id: $target_id})
        MERGE (u)-[:BENCHMARK_WRITE]->(v)
        RETURN count(*) AS result
        """

        with self.driver.session(database="neo4j") as session:
            return session.run(
                query,
                source_id=source_id,
                target_id=target_id,
            ).data()