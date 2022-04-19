#pylint: skip-file
from gremlin_python.process.anonymous_traversal import traversal
from gremlin_python.driver.driver_remote_connection import DriverRemoteConnection


g = traversal().with_remote(DriverRemoteConnection(
    'ws://127.0.0.1:8182/gremlin', 'g'))


all_vertices = g.V().elementMap().toList()
john_id = g.V().hasLabel('john').next().id
g.V(john_id).property('age', 55).next()
john_age = g.V(john_id).values('age').next()


pass

""" # add jack vertex
g.addV('jack').property('age', 40).next()
jack_id = g.V().hasLabel('jack')[0].next().id
jack_properties = g.V(jack_id).valueMap().next()
jack_age = g.V(jack_id).values('age').next()

# update jack's age
g.V(jack_id).property('age', 45).next()
jack_age = g.V(jack_id).values('age').next()
get_all_aged_45 = g.V().has('age', 45).next()

print(jack_age)
 """
