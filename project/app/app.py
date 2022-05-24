# pylint: skip-file
from flask import Flask, render_template, request
from gremlin_python.process.anonymous_traversal import traversal
from gremlin_python.driver.driver_remote_connection import DriverRemoteConnection

app = Flask(__name__)
g = traversal().with_remote(DriverRemoteConnection(
    'ws://janusgraph:8182/gremlin', 'g'))


@app.route('/movie/<int:id>')
def movie(id):
    movie = g.V(id).valueMap().next()
    return render_template('movie.html', movie=movie)


@app.route('/')
def index():
    sort_by = request.args.get("sort_by")
    sort_by = "original_title" if sort_by is None else sort_by
    print(sort_by)
    movies = g.V().hasLabel('movies').order().by(sort_by).limit(20).toList()
    movies = [(movie.id, g.V(movie.id).valueMap().next()) for movie in movies]
    return render_template('index.html', movies=movies)


def main():
    """ Entry function """
    app.run(debug=True, host='0.0.0.0')


if __name__ == '__main__':
    main()
