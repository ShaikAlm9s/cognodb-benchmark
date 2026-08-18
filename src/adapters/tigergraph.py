import os

import pyTigerGraph
from dotenv import load_dotenv


load_dotenv()


class TigerGraphAdapter:

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
    # Point lookup
    # ---------------------------------------------------------

    def point_lookup(self, transaction_id):
        return self.conn.getVerticesById(
            "Payment_Transaction",
            [str(transaction_id)],
        )

    # ---------------------------------------------------------
    # 1-hop traversal
    #
    # Payment_Transaction
    #       -> Merchant
    # ---------------------------------------------------------

    def traversal_1hop(self, transaction_id):
        return self.conn.getEdges(
            "Payment_Transaction",
            str(transaction_id),
            edgeType="Merchant_Receive_Transaction",
        )

    # ---------------------------------------------------------
    # 2-hop traversal
    #
    # Payment_Transaction
    #       -> Card
    #       -> Merchant
    #
    # Executed server-side.
    # ---------------------------------------------------------

    def traversal_2hop(self, transaction_id):
        transaction_id = str(transaction_id).replace(
            '"',
            '\\"',
        )

        query = f"""
        INTERPRET QUERY () FOR GRAPH $graphname {{

            Start = {{Payment_Transaction.*}};

            Cards = SELECT c
                    FROM Start:s
                    -(Card_Send_Transaction)- Card:c
                    WHERE s.id == "{transaction_id}";

            Merchants = SELECT m
                        FROM Cards:c
                        -(Has_Interaction_With_Merchant)- Merchant:m;

            PRINT Merchants;
        }}
        """

        return self.conn.runInterpretedQuery(query)

    # ---------------------------------------------------------
    # 3-hop traversal
    #
    # Payment_Transaction
    #       -> Card
    #       -> Merchant
    #       -> Merchant_Category
    #
    # Executed server-side.
    # ---------------------------------------------------------

    def traversal_3hop(self, transaction_id):
        transaction_id = str(transaction_id).replace(
            '"',
            '\\"',
        )

        query = f"""
        INTERPRET QUERY () FOR GRAPH $graphname {{

            Start = {{Payment_Transaction.*}};

            Cards = SELECT c
                    FROM Start:s
                    -(Card_Send_Transaction)- Card:c
                    WHERE s.id == "{transaction_id}";

            Merchants = SELECT m
                        FROM Cards:c
                        -(Has_Interaction_With_Merchant)- Merchant:m;

            Categories = SELECT mc
                        FROM Merchants:m
                        -(Merchant_Assigned)- Merchant_Category:mc;

            PRINT Categories;
        }}
        """

        return self.conn.runInterpretedQuery(query)

    # ---------------------------------------------------------
    # Filtered lookup
    # ---------------------------------------------------------

    def filtered_lookup(self, transaction_id):
        rows = self.conn.getVerticesById(
            "Payment_Transaction",
            [str(transaction_id)],
        )

        if not rows:
            return None

        transaction = rows[0]

        attributes = transaction.get(
            "attributes",
            {},
        )

        return {
            "id": attributes.get(
                "id",
                transaction.get("v_id"),
            ),
            "amount": attributes.get("amount"),
            "is_fraud": attributes.get("is_fraud"),
            "transaction_time": attributes.get("transaction_time"),
        }

    # ---------------------------------------------------------
    # Aggregation
    # ---------------------------------------------------------

    def aggregation(self):
        transactions = self.conn.getVertices(
            "Payment_Transaction",
            limit=1000,
        )

        total_amount = 0.0
        transaction_count = 0
        fraud_count = 0

        for transaction in transactions:

            attributes = transaction.get(
                "attributes",
                {},
            )

            amount = attributes.get("amount", 0)
            is_fraud = attributes.get("is_fraud", 0)

            if amount is None:
                amount = 0

            if is_fraud is None:
                is_fraud = 0

            try:
                total_amount += float(amount)
            except (TypeError, ValueError):
                pass

            transaction_count += 1

            try:
                fraud_count += int(is_fraud)
            except (TypeError, ValueError):
                pass

        average_amount = (
            total_amount / transaction_count
            if transaction_count > 0
            else 0.0
        )

        return {
            "transaction_count": transaction_count,
            "total_amount": total_amount,
            "average_amount": average_amount,
            "fraud_count": fraud_count,
        }

    # ---------------------------------------------------------
    # Write operation
    #
    # The benchmark runner calls:
    #
    #     write_test(source_id, target_id)
    #
    # We use target_id for the upsert.
    # ---------------------------------------------------------

    def write_test(self, source_id, target_id):
        return self.conn.upsertVertex(
            "Payment_Transaction",
            str(target_id),
            {
                "amount": (0.0, "+"),
            },
        )