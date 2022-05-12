#pylint: skip-file
import pandas as pd
from cassandra.cluster import Cluster
# Connect to the Cassandra server running on the localhost.
cluster = Cluster()

# Connect to the `bdnr_test` keyspace.
session = cluster.connect('bdnr_test')

# Execute a CQL statement and iterate through the results.
bookmarks_porto = session.execute(
    """SELECT *
FROM bookmarks_by_tags
WHERE tag = 'porto'
ORDER BY timestamp;""")

bookmarks_education = session.execute(
    """SELECT *
FROM bookmarks_by_tags
WHERE tag = 'education'
ORDER BY timestamp;""")

inters = []

for b1 in bookmarks_education:
    inters.append((b1.url, b1.timestamp))

for b2 in bookmarks_porto:
    inters.append((b2.url, b2.timestamp))

for bookmark in set(inters):
    print(bookmark[0], bookmark[1])
