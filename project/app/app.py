# pylint: skip-file
from lib2to3.pytree import generate_matches
from flask import Flask, render_template, request
from gremlin_python.process.anonymous_traversal import traversal
from gremlin_python.process.graph_traversal import __
from gremlin_python.driver.driver_remote_connection import DriverRemoteConnection

from gremlin_python.process.graph_traversal import __
from gremlin_python.process.strategies import *


app = Flask(__name__)
g = traversal().with_remote(DriverRemoteConnection(
    'ws://janusgraph:8182/gremlin', 'g'))

KBID = g.V().hasLabel("person").has("name", "Kevin Bacon").next().id


@app.route('/movie/<int:id>')
def movie(id):
    movie = g.V(id).valueMap().next()
    cast = g.V(id).outE('acted_in').inV().valueMap(
        "name", "profile_path").to_list()
    return render_template('movie.html', movie=movie, cast=cast)

@app.route('/actor/<int:id>')
def actor(id):
    global KBID
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
    print(sort_by)
    if search != None:
        movies = g.V().hasLabel('movies').has('original_title', search).toList()
    elif filter_by != None:
        movies = g.V().hasLabel('genres').has('name', filter_by).outE('of_genre').limit(20).inV().toList()
    elif year != None:
        movies = g.V().hasLabel('movies').has('year', year).limit(20).toList()
    else:
        movies = g.V().hasLabel('movies').order().by(sort_by).limit(20).toList()
    years = g.V().hasLabel('movies').values("year").dedup().to_list()
    genres = g.V().hasLabel("movies").outE('of_genre').inV().dedup().valueMap('name').toList()
    movies = [(movie.id, g.V(movie.id).valueMap().next()) for movie in movies]
    return render_template('index.html', movies=movies, genres=genres, years=years)


def main():
    """ Entry function """
    app.run(debug=True, host='0.0.0.0')


if __name__ == '__main__':
    main()
