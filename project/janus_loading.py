# pylint: skip-file
from gremlin_python.process.anonymous_traversal import traversal
from gremlin_python.driver.driver_remote_connection import DriverRemoteConnection
import pandas as pd
from progress.bar import Bar


def find_vertex(l, id):
    for vertex in l:
        if vertex[0] == id:
            return vertex
    return None


def upload_dataframe(df, g, label):
    bar = Bar(label, max=df.shape[0])
    vertices = []
    for _, row in df.iterrows():
        bar.next()
        vertex = g.addV(label)
        for column in df.columns:
            if pd.isna(row[column]):
                continue
            vertex = vertex.property(column, row[column])
        vertices.append((row["id"], vertex.next()))
    bar.finish()
    return vertices


def upload_edges(df, in_column, out_column, in_list, out_list, label):
    edges = []
    bar = Bar(label, max=df.shape[0])
    for _, row in df.iterrows():
        bar.next()
        in_id = row[in_column]
        out_id = row[out_column]
        in_vertex = find_vertex(in_list, in_id)
        out_vertex = find_vertex(out_id, out_list)
        edge = g.addE(label).from_(in_vertex).to(out_vertex)
        for column in df.columns:
            if column in (in_column, out_column) or pd.isna(row[column]):
                continue
            edge = edge.property(column, row[column])

        edges.append(edge.next())
    return edges


def main():
    cast = pd.read_csv('datasets/cast.csv')
    collections = pd.read_csv('datasets/collections.csv')
    crew = pd.read_csv('datasets/crew.csv')
    genres = pd.read_csv('datasets/genres.csv')
    movie_collections = pd.read_csv('datasets/movies_collections.csv')
    movie_genres = pd.read_csv('datasets/movies_genres.csv')
    movies = pd.read_csv('datasets/movies.csv')
    person = pd.read_csv('datasets/person.csv')

    g = traversal().with_remote(DriverRemoteConnection(
        'ws://127.0.0.1:8182/gremlin', 'g'))

    genres = upload_dataframe(genres, g, "genres")
    movies = upload_dataframe(movies, g, "movies")
    movie_genres = upload_edges(
        movie_genres, "movie_id", "genre_id", movies, genres, "of_genre"
    )

    person = upload_dataframe(person, g, "person")
    movie_collections = upload_edges(
        movie_collections, "movie_id", "collection_id", movies, collections, "of_collection"
    )
    cast = upload_edges(
        cast, "movie_id", "person_id", movies, person, "acted_in"
    )
    crew = upload_edges(
        crew, "movie_id", "person_id", movies, person, "crew_in"
    )


if __name__ == '__main__':
    main()
