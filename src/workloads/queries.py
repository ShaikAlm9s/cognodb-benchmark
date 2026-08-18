POINT_LOOKUP = """
MATCH (u:User {id: $node_id})
RETURN u.id AS id
"""


TRAVERSAL_1HOP = """
MATCH (u:User {id: $node_id})-[:FOLLOWS]->(v)
RETURN v.id AS id
"""


TRAVERSAL_2HOP = """
MATCH (u:User {id: $node_id})
      -[:FOLLOWS]->()
      -[:FOLLOWS]->(v)
RETURN v.id AS id
"""


TRAVERSAL_3HOP = """
MATCH (u:User {id: $node_id})
      -[:FOLLOWS]->()
      -[:FOLLOWS]->()
      -[:FOLLOWS]->(v)
RETURN v.id AS id
"""


FILTERED_LOOKUP = """
MATCH (u:User)
WHERE u.id = $node_id
RETURN u.id AS id
"""


AGGREGATION = """
MATCH (u:User)
RETURN count(u) AS user_count
"""


WRITE_TEST = """
MATCH (u:User {id: $source_id})
MATCH (v:User {id: $target_id})
MERGE (u)-[:BENCHMARK_WRITE]->(v)
RETURN count(*) AS result
"""