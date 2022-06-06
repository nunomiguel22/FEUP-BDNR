# pylint: skip-file
from flask import Flask, render_template, request, redirect
from gremlin_python.process.anonymous_traversal import traversal
from gremlin_python.driver.driver_remote_connection import DriverRemoteConnection
from gremlin_python.process.graph_traversal import __
from gremlin_python.process.strategies import *
from gremlin_python.process.traversal import T
import time


app = Flask(__name__)


def init_g():
    g = None
    for _ in range(60):
        if g:
            break
        try:
            g = traversal().with_remote(DriverRemoteConnection(
                'ws://janusgraph:8182/gremlin', 'g'))
        except Exception as e:
            print("Could not connect to JanusGraph")
            print(e)
        finally:
            time.sleep(1)
    return g


KBID = 0
g = init_g()

if not g:
    exit(-1)

years = g.V().hasLabel('movies').values("year").dedup().to_list()
genres = g.V().hasLabel("movies").outE(
    'of_genre').inV().dedup().valueMap('name').toList()


def init_janus(KBID, g):

    for _ in range(30):
        if KBID:
            return
        try:
            KBID = g.V().hasLabel("person").has("name", "Kevin Bacon").next().id
        except Exception as e:
            print("Could not connect to JanusGraph, perhaps the graph is not loaded")
            print(e)
        finally:
            time.sleep(1)
    exit(-1)


@app.route('/movie/<int:id>')
def movie(id):
    movie = g.V(id).valueMap().next()
    cast_edges = g.V(id).outE('acted_in').elementMap().to_list()
    cast_vertices = g.V(id).outE('acted_in').inV().elementMap().to_list()
    cast = list(zip(cast_edges, cast_vertices))

    crew_edges = g.V(id).outE('crew_in').elementMap().to_list()
    crew_vertices = g.V(id).outE('crew_in').inV().elementMap().to_list()
    crew = list(zip(crew_edges, crew_vertices))

    return render_template('movie.html', movie=movie, cast=cast, crew=crew, T=T)


@app.route('/<int:id>/edit')
def edit(id):
    vertex = g.V(id).valueMap().next()
    return render_template('edit.html', id=id, vertex=vertex)


@app.route('/<int:id>/update', methods=['POST'])
def updatevertex(id):
    vertex = g.V(id)
    for key, value in request.form.items():
        if value:
            vertex = vertex.property(key, value)
        else:
            g.V(id).properties(key).drop().iterate()
    vertex.next()
    return redirect(request.referrer)


@app.route('/<int:id>/delete', methods=['POST'])
def delete_vertex(id):

    g.V(id).drop().iterate()
    return redirect(request.referrer)


@app.route('/actor/<int:id>')
def actor(id):
    actor = g.V(id).valueMap().next()
    movies = g.V(id).outE("acted_in").to_list()

    movie_list = []

    for movie in movies:
        character = g.E(movie.id["@value"]["relationId"]
                        ).values("character").next()

        movie_id = g.E(movie.id["@value"]["relationId"]
                       ).inV().next()
        movie_info = g.V(movie_id).values(
            "original_title", "release_date", "popularity", "poster_path").to_list()
        movie_list.append((movie_id, character, movie_info))

    popular_movies = sorted(
        movie_list, key=lambda tup: tup[2][2])[:4]

    kb6d = g.V(id).repeat(__.out().simplePath()).until(
        __.hasId(KBID).or_().loops().is_(4)).path().next()
    kb6d = [g.V(vertex).valueMap().next() for vertex in kb6d]

    path = []
    for vertex in kb6d:
        name = vertex["name"][0] if "name" in vertex else vertex["original_title"][0]
        img = vertex["poster_path"][0] if "poster_path" in vertex else vertex["profile_path"][0]
        path.append((name, img))
    return render_template('actor.html', actor=actor, movies=movie_list, popular_movies=popular_movies, kb6d=path[:-1])


@app.route('/')
def index():
    sort_by = request.args.get("sort_by")
    search = request.args.get("search")
    filter_by = request.args.get("filter_by")
    year = request.args.get("year")
    sort_by = "original_title" if sort_by is None else sort_by

    query = g.V()

    if filter_by is not None:
        query = query.hasLabel('genres').has('name', filter_by).outE(
            'of_genre').limit(20).inV()
    else:
        query = query.hasLabel('movies')

    if year is not None:
        query = query.has('year', year)

    movies = query.order().by(sort_by).limit(20).toList()

    movies = [(movie.id, g.V(movie.id).valueMap().next()) for movie in movies]
    return render_template('index.html', movies=movies, genres=genres, years=years)


def main():
    init_janus(KBID, g)
    app.run(debug=True, host='0.0.0.0')


if __name__ == '__main__':
    main()
