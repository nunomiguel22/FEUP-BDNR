#pylint: skip-file
import pandas as pd
import ast
from progress.bar import Bar

df = pd.read_csv('datasets/credits.csv', low_memory=False)

person_dict = {"id": [], "name": [], "gender": [], "profile_path": []}
cast_dict = {"movie_id": [], "person_id": [], "character": [], "credit_id": []}
crew_dict = {
    "movie_id": [], "person_id": [],
    "credit_id": [], "department": [], "job": []
}

bar = Bar('Row', max=df.shape[0])
for i, row in df.iterrows():
    bar().next()

    movie_id = row["id"]
    cast = ast.literal_eval(row["cast"])
    crew = ast.literal_eval(row["crew"])

    for actor in cast:
        for key in person_dict.keys():
            person_dict[key].append(actor[key])

        cast_dict["movie_id"].append(movie_id)
        cast_dict["person_id"].append(actor["id"])
        cast_dict["character"].append(actor["character"])
        cast_dict["credit_id"].append(actor["credit_id"])

    for crew_member in crew:
        for key in person_dict.keys():
            person_dict[key].append(crew_member[key])

        crew_dict["movie_id"].append(movie_id)
        crew_dict["person_id"].append(crew_member["id"])
        crew_dict["credit_id"].append(crew_member["credit_id"])
        crew_dict["department"].append(crew_member["department"])
        crew_dict["job"].append(crew_member["job"])
bar.finish()


cast_df = pd.DataFrame(cast_dict).drop_duplicates()
crew_df = pd.DataFrame(crew_dict).drop_duplicates()
person_df = pd.DataFrame(person_dict).drop_duplicates()

cast_df.to_csv(
    'datasets/cast.csv', index=False
)
crew_df.to_csv('datasets/crew.csv', index=False)
person_df.to_csv('datasets/person.csv', index=False)
