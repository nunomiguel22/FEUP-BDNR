#pylint: skip-file

from cassandra.cluster import Cluster
# Connect to the Cassandra server running on the localhost.
cluster = Cluster()

# Connect to the `bdnr_test` keyspace.
session = cluster.connect('bdnr_test')

# Execute a CQL statement and iterate through the results.
catalog = session.execute('SELECT * FROM catalog')
for product in catalog:
    print(product.product_id, product.product_description)
