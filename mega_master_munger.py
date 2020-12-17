import pandas as pd
import numpy as np
from imdb import IMDb

##Creating the IMDb instance
ia = IMDb()

## Creating CSV filepath variables
movies_csv_path = "Resources/AllMoviesDetailsCleaned.csv"
streaming_csv_path = "Resources/MoviesOnStreamingPlatforms_updated.csv"

movies_df = pd.read_csv(movies_csv_path, encoding="utf-8", delimiter=";", parse_dates=["release_date"])
streaming_df = pd.read_csv(streaming_csv_path, encoding="utf-8", parse_dates=["Year"])

#Uniforming the dates between both CSVs.
movies_df["release_date"] = movies_df["release_date"].dt.year
streaming_df["Year"] = streaming_df["Year"].dt.year
movies_df = movies_df.loc[(movies_df["release_date"].isnull() != True),:]
movies_df["release_date"] = movies_df["release_date"].astype(int)


### Creating a merged dataframe on Title and Year
super_merge = pd.merge(movies_df, streaming_df, left_on=["title", "release_date"], right_on=["Title", "Year"]).reset_index(drop=True)
super_merge['genres'] = super_merge['genres'].str.replace(pat="|", repl=",")
movie_merge = pd.merge(movies_df, streaming_df, left_on=["title", "release_date"], right_on=["Title", "Year"]).reset_index(drop=True)
desiredColumns = ['title', 'genres', 'Genres', 'release_date', 'budget', 'revenue', 'Runtime', 'Country', 'Language', 'spoken_languages_number', 'Age', 'popularity', 'vote_average', 'vote_count', 'imdb_id', 'IMDb', 'Rotten Tomatoes', 'Directors']
super_merge = super_merge.loc[:, desiredColumns]

#cleaned up imdb_id with a left strip. now this id is usable with the imdb module
super_merge['imdb_id'] = super_merge['imdb_id'].str.lstrip('tt')

#filling NaNs for datagrabbing
super_merge.loc[super_merge['imdb_id'].isnull(),'imdb_id'] = "None"
super_merge.loc[super_merge['genres'].isnull(),'genres'] = "None"
super_merge.loc[super_merge['Genres'].isnull(),'Genres'] = "None"
super_merge.loc[super_merge['Directors'].isnull(),'Directors'] = "None"

#Grabbing only the first director from possible arrays.
directors_list = super_merge['Directors'].str.split(pat=",")
first_director_list = []
for i in directors_list:
    first_director_list.append(i[0])
    
#reassigning the directors column with the scrubbed director list    
super_merge['Directors'] = first_director_list

###Counter for how many times we made a call on the imbd module
imdb_counter = 0


### running a for loop to clean up genres and directors. If no data was available in these columns from either CSV, IMDb module was used to grab the data.
 
for index,row in super_merge.iterrows():
    if row['Genres'] == "None":
        super_merge.loc[index, 'Genres'] = row['genres']
    if (row['Genres'] == "None") & (row['genres'] == "None") & (row['imdb_id'] != "None"):
        imdb_counter += 1
        try:
            movie = ia.get_movie(row['imdb_id'])
            imdb_genre = movie['genres'][0]
            super_merge.loc[index, 'Genres'] = imdb_genre
        except (KeyError, ValueError):
            print(f'Genre data was not avilable for {index} {row["title"]} Value error with {imdb_genre}')
            
    if (row['Directors'] == 'None') & (row['imdb_id'] != "None"):
        try:
            movie = ia.get_movie(row['imdb_id'])
            imdb_counter += 1
            director_name = movie['directors'][0]['name']
            super_merge.loc[index, 'Directors'] = director_name
        except KeyError:
            print(f'Director data was not avilable for {index} {row["title"]}')
            
print(f"The IMDb module was used {imdb_counter} times")    


###Creating a variable of columns and removing the column I want to remove.
scrub_columns = super_merge.columns.to_list()
scrub_columns.remove("genres")
super_merge = super_merge.loc[:, scrub_columns]


### Creating a DataFrame to give the Directors an ID.
director_unique = pd.unique(super_merge['Directors'])
unique_list_length = len(director_unique)
unique_dict = {"Name": director_unique}
directors_df = pd.DataFrame(unique_dict)
directors_df.insert(0, "Director_ID", range(420, 420 + unique_list_length))


###Final table that holds director id and drops director column
super_ultra_merge = pd.merge(super_merge, directors_df, left_on = "Directors", right_on="Name", how="left")
super_ultra_merge = super_ultra_merge.drop(columns = ['Directors', 'Name'])

###Exporting final tables to CSV's to upload to postgreSQL
super_ultra_merge.to_csv("output_data/main_movie_table1.csv", index=True)
directors_df.to_csv("output_data/directors_table1.csv", index=False)

###Creating Netflix DF for Netflix reference table
netflix_df = movie_merge[["Netflix"]]
netflix_df = netflix_df.loc[netflix_df['Netflix'] >= 1].reset_index(drop=False).rename(columns={"index": "Movie_ID"}).drop(columns="Netflix")

netflix_df.to_csv("output_data/netflix_table.csv", index=False)

###Prime Video DF to csv.
prime_video = movie_merge.loc[movie_merge["Prime Video"] == 1, "Prime Video"]
prime_video = pd.DataFrame(prime_video).reset_index(drop=False).rename(columns={"index": "Movie_ID"}).drop(columns="Prime Video")
prime_video.to_csv("output_data/Prime_Video_data.csv", index=False)

###HULU DF to CSV
hulu_df = movie_merge.loc[movie_merge["Hulu"]==1,'Hulu']
hulu_df = pd.DataFrame(hulu_df).reset_index(drop=False).rename(columns={"index": "Movie_ID"}).drop(columns="Hulu")
hulu_df.to_csv("output_data/hulu_count.csv", header=True, index=False)
###Disney DF to CSV
disney_df = movie_merge[["Disney+"]]
disney_plus_df = disney_df.loc[disney_df["Disney+"]>= 1].reset_index(drop=False).rename(columns={"index": "Movie_ID"}).drop(columns="Disney+")
disney_plus_df.to_csv("output_data/disneyplus_csv.csv", index=False)
