# ETL-Project

We downloaded our data sources from the web. One of the csv's was too large so we had to compress the resources folder into a zip file. To prevent issues, we added the Resources folder into the .gitignore.

Starter notebook was created, importing csv's into PD DataFrames. Some initial cleaning was done to perform the first merge to allow our group to play with the data.

Ben has Amazon Prime.

Tyson has Hulu.

Buckley has Netflix.

Ryan has Disney +.

Leo and Calvin are going to clean the main DF.


We are going to do some ETL on some <strong>movies</strong>.


Project Write-Up

The purpose of our ETL project is to prepare data to compare the movie libraries of various streaming-service providers and/or the success of movie directors.  First, download and install IMDbPY using (pip install IMDbPY).  Once this is complete you will need to make a clone of the repository on your computer.  After this clone has been created, navigate into the repository from your terminal and make a new branch. Before doing anything else, double check that you are on your newly created branch of the repository.  Once you have confirmed that you are on your new branch execute the following command: tar -xvzf archive.tar.gz.  This command will unzip the Resources folder containing our CSVs.  Next, open Master_Munger.ipynb and begin to run the code within the notebook.  The Master_Munger.ipynb will first merge your two CSVs into a single “super_merge” dataframe, stripping out unnecessary columns, filling in NaNs with “None”, splitting arrays and adding additional columns.  From here, any of the director/genre information that was not available within the original CSVs is filled in using a loop that references the IMDbPY library.  When this loop finishes, the duplicate genre column is removed, and a new data frame for directors, called “directors_df”, is created with a unique Director_ID for each director.  These new Director_IDs are then merged into the original dataframe and the Director Name is removed, creating the “super_ultra_merge” dataframe.  From here your “super_ultra_merge” is exported as “main_movie_table1.csv” and your “directors_df” is exported as “directors_table1.csv” to the output_data folder.  From here dataframes for each streaming provider are created using a .loc, and exported to our output_data folder. CSVs that were exported to our output_data are then loaded into a PostGRE database in the following order: directors_table1.csv -> main_movie_table1 -> (any order of streaming service tables).

We chose to use SQL as our database as it is designed to handle structured/relational datasets allowing for easy querying of information.  Our original CSVs from Kaggle and subsequent tables are all structured datasets, which made choosing SQL a no-brainer.

Calvin does not have commits as he worked collaboratively with Leo in the same workspace.
Calvin also wrote the readme for the team.
