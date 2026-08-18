from abc import ABC, abstractmethod


class GraphDatabaseAdapter(ABC):

    @abstractmethod
    def connect(self):
        """Establish a database connection."""
        raise NotImplementedError

    @abstractmethod
    def close(self):
        """Close the database connection."""
        raise NotImplementedError

    @abstractmethod
    def clear(self):
        """Remove benchmark data."""
        raise NotImplementedError

    @abstractmethod
    def load_nodes(self, nodes):
        """Load nodes into the database."""
        raise NotImplementedError

    @abstractmethod
    def load_edges(self, edges):
        """Load relationships into the database."""
        raise NotImplementedError

    @abstractmethod
    def point_lookup(self, node_id):
        """Execute a point lookup."""
        raise NotImplementedError

    @abstractmethod
    def traversal_1hop(self, node_id):
        """Execute a 1-hop traversal."""
        raise NotImplementedError

    @abstractmethod
    def traversal_2hop(self, node_id):
        """Execute a 2-hop traversal."""
        raise NotImplementedError

    @abstractmethod
    def traversal_3hop(self, node_id):
        """Execute a 3-hop traversal."""
        raise NotImplementedError

    @abstractmethod
    def filtered_lookup(self, node_id):
        """Execute an indexed/filtered lookup."""
        raise NotImplementedError

    @abstractmethod
    def aggregation(self):
        """Execute an aggregation."""
        raise NotImplementedError

    @abstractmethod
    def write_test(self, source_id, target_id):
        """Execute a controlled write."""
        raise NotImplementedError