-- Create main movies table with movie metadata; set movie id to primary key and refernce directors table director_id as foreign key
CREATE TABLE Movies (
    Movie_ID SERIAL PRIMARY KEY,
    title VARCHAR(500),
    Genres VARCHAR(500),
    release_date INTEGER,
    budget BIGINT,
    revenue BIGINT,
    Runtime DECIMAL,
    Country VARCHAR(500),
    Language VARCHAR(500),
    spoken_languages_number INTEGER,
    Age VARCHAR(10),
    popularity VARCHAR(100),
    vote_average DECIMAL,
    vote_count BIGINT,
    imdb_id VARCHAR(100),
    IMDb DECIMAL,
    Rotten_Tomatoes VARCHAR(5),
    Director_ID INTEGER,
   	FOREIGN KEY (Director_ID) REFERENCES Directors(Director_ID)
);

-- Create streaming platform tables using movie_id as foreign key 
CREATE TABLE Amazon_Prime (
    Movie_ID INTEGER,
    FOREIGN KEY (Movie_ID) REFERENCES Movies(Movie_ID)
);

CREATE TABLE Netflix (
    Movie_ID INTEGER,
    FOREIGN KEY (Movie_ID) REFERENCES Movies(Movie_ID)
);

CREATE TABLE Disney_Plus (
    Movie_ID INTEGER,
    FOREIGN KEY (Movie_ID) REFERENCES Movies(Movie_ID)
);

CREATE TABLE Hulu (
   Movie_ID INTEGER,
   FOREIGN KEY (Movie_ID) REFERENCES Movies(Movie_ID)
);

-- Create directores table with director name, set director ID to primary key 
CREATE TABLE Directors (
    Director_ID INTEGER PRIMARY KEY,
    Name VARCHAR(50)
);
