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
    genres = Column(String)
    content_rating = Column(String)
    plot_keywords= Column(String)
    language = Column(String)
    country= Column(String)
    title_year = Column(Integer)
    imdb_score = Column(Integer)


# results = session.query(Movies)
# for 


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
        f"/piechart_data<br/>"
        f"/get_barchart_data<br/>"
        f"/dashboard<br/>"
    )

@app.route("/movie_data")
def movie_data():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of movie data """
    # Query all movies
    results = session.query(Movies.movie_title, Movies.director_name, Movies.duration, Movies.genres,
    Movies.content_rating, Movies.plot_keywords, Movies.language, Movies.country, Movies.title_year, Movies.imdb_score).all()
    session.close()
    # print(results)

    # Create a dictionary from the row data and append to a list of movies
    all_movies = []
    for movie_title, director_name, duration, genres, content_rating, plot_keywords, language, country, title_year, imdb_score  in results:
        movies_dict = {}
        movies_dict["movie"] = movie_title
        movies_dict["director"] = director_name
        movies_dict["genres"] = genres
        movies_dict["content_rating"] = content_rating
        movies_dict["keywords"] = plot_keywords
        movies_dict["language"] = language
        movies_dict["country"] = country
        movies_dict["year"] = title_year
        movies_dict["rating"] = imdb_score
        movies_dict["duration"] = duration
        all_movies.append(movies_dict)
    return jsonify(all_movies)

# @app.route('/dashboard')
# def dashboard():
#     return render_template('index.html')

# def calculate_percentage(val, total):
#     """Calculates the percentage of a value over a total"""
#     percent = np.divide(val, total)
    
#     return percent

# @app.route('/piechart_data')
# def get_piechart_data():
#     session = Session(engine)
#     """Return a list of content_rating counts """
#     results = session.query(Movies.content_rating,func.count(Movies.content_rating)).\
#                             group_by(Movies.content_rating)
#     session.close()
#     print(results)
# #     # Create a dictionary from the row data and append to a list of movies
#     pie_chart = []
#     for content_rating, count in results:
#         ratings_dict = {}
#         ratings_dict['content_rating'] = content_rating
#         ratings_dict['count'] = count
#         pie_chart.append(ratings_dict)

#     return jsonify(pie_chart)

@app.route('/piechart_data')
def get_piechart_data():
    session = Session(engine)
    """Return a list of content_rating counts """
    results = session.query(Movies.country,func.count(Movies.country)).\
                            group_by(Movies.country)
    session.close()
    print(results)
#     # Create a dictionary from the row data and append to a list of movies
    pie_chart = []
    for country, count in results:
        ratings_dict = {}
        ratings_dict['country'] = country
        ratings_dict['count'] = count
        pie_chart.append(ratings_dict)

    return jsonify(pie_chart)



# @app.route('/get_barchart_data')
# def get_barchart_data():

#     return jsonify(barChartData)
if __name__ == '__main__':
    app.run(debug=True)
# if __name__ =='__main__':
#     app.run(threaded=True, host='0.0.0.0', port=os.environ['PORT'])

