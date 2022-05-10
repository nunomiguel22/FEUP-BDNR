# pylint: skip-file
from gremlin_python.process.anonymous_traversal import traversal
from gremlin_python.driver.driver_remote_connection import DriverRemoteConnection
import pprint

MOVIE_NAME = "Justice League"

pp = pprint.PrettyPrinter(indent=4)
g = traversal().with_remote(DriverRemoteConnection(
    'ws://127.0.0.1:8182/gremlin', 'g'))

print('\nMOVIE INFO\n\n')
movie = g.V().hasLabel('movies').has('original_title', MOVIE_NAME).next()
movie_info = g.V(movie.id).valueMap().next()
pp.pprint(movie_info)

print('\nACTOR NAMES\n\n')
actors = g.V(movie.id).bothE('acted_in').bothV().hasLabel(
    'person').values('name').toList()
pp.pprint(actors)

print('\nCREW - JOB\n\n')
crew = g.V(movie.id).bothE('crew_in').toList()
for member in crew:
    # Get attribute of edge
    job = g.E(member.id["@value"]["relationId"]).values('job').next()
    # Get attribute of actor vertex
    name = g.E(member.id["@value"]["relationId"]
               ).bothV().hasLabel('person').values('name').next()
    print(f'{name} - {job}')

ACTOR_NAME = "Willem Dafoe"

print('\nACTOR INFO\n\n')
actor = g.V().hasLabel('person').has('name', ACTOR_NAME).next()
actor_info = g.V(actor.id).valueMap().next()
pp.pprint(actor_info)

print('\nWORKED IN\n\n')
movies = g.V(actor.id).bothE('acted_in').bothV().hasLabel(
    'movies').toList()
for film in movies:
    print(g.V(film.id).values('title').next())

print('\nWORKED WITH\n\n')
for film in movies:
    worked_with = g.V(film.id).bothE('acted_in').bothV().hasLabel(
        'person').values('name').toList()
    worked_with = set(worked_with)
    for colleague in worked_with:
        if colleague != ACTOR_NAME: print(colleague)

