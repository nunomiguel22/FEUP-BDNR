#pylint: skip-file

from cassandra.cluster import Cluster
# Connect to the Cassandra server running on the localhost.
cluster = Cluster()

# Connect to the `bdnr_test` keyspace.
session = cluster.connect('bdnr_test')

# Execute a CQL statement and iterate through the results.
bookmarks = session.execute(
    "SELECT * FROM bookmarks WHERE url_md5='93462762d236aed61c248298584ea5bf'")
for bookmark in bookmarks:
    print(bookmark.url, bookmark.timestamp)
