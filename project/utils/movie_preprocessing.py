# pylint: skip-file
import pandas as pd
import ast
from progress.bar import Bar

CUTOFF_YEAR = 2016

df = pd.read_csv('../datasets/movies_metadata.csv', low_memory=False)
# Drop adult films
df = df[df["adult"] == "False"]
df = df.drop(["adult", "homepage"], axis=1)
df = df.dropna(subset=["release_date"])
df["year"] = df["release_date"].map(lambda x: int(x.split("-")[0]))

df = df[df["year"] > CUTOFF_YEAR]

df = df.drop(["year"], axis=1)


genres_dict = {"id": [], "name": []}
movies_genres_dict = {"movie_id": [], "genre_id": []}
collections_dict = {"id": [], "name": [],
                    "poster_path": [], "backdrop_path": []
                    }
movies_collections_dict = {"movie_id": [], "collection_id": []}
bar = Bar('Row', max=df.shape[0])
for i, row in df.iterrows():
    bar.next()

    genres = ast.literal_eval(row["genres"])
    movie_id = row["id"]
    for genre in genres:
        genres_dict["id"].append(genre["id"])
        genres_dict["name"].append(genre["name"])
        movies_genres_dict["movie_id"].append(movie_id)
        movies_genres_dict["genre_id"].append(genre["id"])

    collect = row["belongs_to_collection"]
    if pd.isna(collect):
        continue

    collect = ast.literal_eval(collect)
    for key in collections_dict.keys():
        collections_dict[key].append(collect[key])
    movies_collections_dict["movie_id"].append(movie_id)
    movies_collections_dict["collection_id"].append(collect["id"])
bar.finish()

df = df.drop([
    "belongs_to_collection", "genres", "video",
    "production_companies", "production_countries",
    "spoken_languages", "status", "vote_count"
], axis=1)
genres_df = pd.DataFrame(genres_dict).drop_duplicates()
collections_df = pd.DataFrame(collections_dict).drop_duplicates()
movies_collections_df = pd.DataFrame(movies_collections_dict).drop_duplicates()
movies_genres_df = pd.DataFrame(movies_genres_dict).drop_duplicates()

df.to_csv('../datasets/movies.csv', index=False)
movies_collections_df.to_csv(
    '../datasets/movies_collections.csv', index=False
)
collections_df.to_csv('../datasets/collections.csv', index=False)
genres_df.to_csv('../datasets/genres.csv', index=False)
movies_genres_df.to_csv('../datasets/movies_genres.csv', index=False)
