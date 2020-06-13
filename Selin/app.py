import os
import numpy as np
import pandas as pd
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

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
engine = create_engine(SQLITE)
Base.metadata.create_all(engine)

# Save reference to the table
from sqlalchemy.orm import Session
session = Session(bind=engine)

class Movies(Base):
    __tablename__ = 'sqldata'
    movie_title = Column(String, primary_key=True)
    director_name = Column(String)
    duration = Column(Integer)
    Genre1 = Column(String)
    Genre2 = Column(String)
    Genre3 = Column(String)
    Genre4 = Column(String)
    actors = Column(String)
    plot_keywords= Column(String)
    language = Column(String)
    country= Column(String)
    title_year = Column(Integer)
    imdb_score = Column(Integer)


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
        f"Available Routes:<br/>"
        f"/movie_data<br/>"
        f"/get_piechart_data<br/>"
        f"/get_barchart_data<br/>"
        f"/dashboard<br/>"
    )

@app.route("/movie_data")
def movie_data():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of movie data """
    # Query all movies
    results = session.query(Movies.movie_title, Movies.director_name, Movies.duration, Movies.Genre1,Movies.Genre2,Movies.Genre3,Movies.Genre4,
    Movies.actors, Movies.plot_keywords, Movies.language, Movies.country, Movies.title_year, Movies.imdb_score).all()
    session.close()

    # Create a dictionary from the row data and append to a list of movies
    all_movies = []
    for movie_title, director_name, duration, Genre1, Genre2,Genre3,Genre4, actors, plot_keywords, language, country, title_year, imdb_score  in results:
        movies_dict = {}
        movies_dict["movie"] = movie_title
        movies_dict["director"] = director_name
        movies_dict["genres"] = {"genre1": Genre1, "genre2": Genre2,"genre3": Genre3, "genre4": Genre4}
        movies_dict["actors"] = actors
        movies_dict["keywords"] = plot_keywords
        movies_dict["language"] = language
        movies_dict["country"] = country
        movies_dict["year"] = title_year
        movies_dict["rating"] = imdb_score
        movies_dict["duration"] = duration
        all_movies.append(movies_dict)
    return jsonify(all_movies)

@app.route('/dashboard')
def dashboard():
    return render_template('index.html')

def calculate_percentage(val, total):
    """Calculates the percentage of a value over a total"""
    percent = np.divide(val, total)
    
    return percent

@app.route('/get_piechart_data')
def get_piechart_data():
    # Create our session (link) from Python to the DB
    session = Session(engine)
    """Return a list of movie data """
    results = session.query(Movies.movie_title, Movies.Genre1).all()
    session.close()
    # Create a dictionary from the row data and append to a list of movies
    pie_chart = []
    for movie_title, Genre1 in results:
        movies_dict = {}
        movies_dict["movie"] = movie_title
        movies_dict["Genre"] = Genre1
        pie_chart.append(movies_dict)
    df=pd.DataFrame(pie_chart)
    count=df.groupby('Genre').count()
    sum=count.sum()
    percent=df.groupby('Genre').count()/sum*100
    percent=percent.reset_index()
    # dictionary=percent.to_dict()
    # return jsonify(dictionary)
    class_labels=percent.Genre
    pclass_percent=calculate_percentage(df.groupby('Genre').size().values, df['movie'].count())*100
    pieChartData = []
    for index, item in enumerate(pclass_percent):
        eachData = {}
        eachData['category'] = class_labels[index]
        eachData['measure'] =  round(item,1)
        pieChartData.append(eachData)

    return jsonify(pieChartData)


@app.route('/get_barchart_data')
def get_barchart_data():

    return jsonify(barChartData)

if __name__ == '__main__':
    app.run(debug=True)

