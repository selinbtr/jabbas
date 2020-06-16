import os
import numpy as np
import pandas as pd
from sqlalchemy.ext.declarative import declarative_base


from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from sqlalchemy import Column, Integer, String, Float
from flask import Flask, jsonify, request, render_template
from flask_cors import CORS


#################################################
# Database Setup
#################################################
SQLITE = "sqlite:///" + os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data', 'movie_db.sqlite')
print(SQLITE)
SQLITE_ZIPCODE = "sqlite:///" + os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data', 'zipcode_db.sqlite')

Base = declarative_base()

engine = create_engine(SQLITE)
Base.metadata.create_all(engine)

# Save reference to the table
session_zipcode = Session(bind=engine)
 
 #zipcode engine 
Base_zipcode = declarative_base()

engine_zipcode = create_engine(SQLITE_ZIPCODE)
Base_zipcode.metadata.create_all(engine_zipcode)


class Movies(Base):
    __tablename__ = 'sqldata'
    movie_title = Column(String, primary_key=True)
    director_name = Column(String)
    duration = Column(Integer)
    Genre1 = Column(String)
    actors = Column(String)
    language = Column(String)
    country= Column(String)
    title_year = Column(Integer)
    imdb_score = Column(Integer)
    content_rating = Column(String)

class Zipcode(Base_zipcode):
    __tablename__ = 'zipcode'
    zip = Column(Integer, primary_key = True)
    latitude = Column(Float)
    longitude = Column(Float)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)
CORS(app)

#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"<h2>Welcome to the Directory</h2>"
        f"Available Routes:<br/>"
        f"<a href = '/zipcodes' target='_blank'>/zipcodes</a><br/>"
        f"<a href = '/movie_data' target='_blank'>/movie_data</a><br/>"
       
    )

@app.route("/movie_data")
def movie_data():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of movie data """
    # Query all movies
    results = session.query(Movies.movie_title, Movies.director_name, Movies.duration, Movies.Genre1,
    Movies.actors, Movies.language, Movies.country, Movies.title_year, Movies.imdb_score, Movies.content_rating).all()
    session.close()

    # Create a dictionary from the row data and append to a list of movies
    all_movies = []
    for movie_title, director_name, duration, Genre1, actors, language, country, title_year, imdb_score, content_rating  in results:
        movies_dict = {}
        movies_dict["movie"] = movie_title
        movies_dict["director"] = director_name
        movies_dict["genres"] = Genre1
        movies_dict["actors"] = actors
        movies_dict["language"] = language
        movies_dict["country"] = country
        movies_dict["year"] = title_year
        movies_dict["rating"] = imdb_score
        movies_dict["duration"] = duration
        movies_dict["content_rating"] = content_rating
        all_movies.append(movies_dict)
    return jsonify(all_movies)


@app.route('/zipcodes')
def zipcode():
    session_zipcode = Session(engine_zipcode)

    results = session_zipcode.query(Zipcode.zip, Zipcode.latitude, Zipcode.longitude).all()

    session_zipcode.close()

    all_zipcodes = []
    for zip, latitude, longitude  in results:
        zipcode_dict = {}
        zipcode_dict['zip'] = zip
        zipcode_dict['lat'] = latitude
        zipcode_dict['lon'] = longitude
        all_zipcodes.append(zipcode_dict)
        
    return jsonify(all_zipcodes)


if __name__ =='__main__':
    app.run(threaded=True, host='0.0.0.0', port=os.environ['PORT'])

