# import numpy as np
import os
import numpy as np 
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from sqlalchemy import Column, Integer, String, Float

from flask import Flask, jsonify, request


#################################################
# Database Setup
#################################################
# SQLITE = f"sqlite:////{os.path.join(os.path.realpath(__file__).replace(__file__,''), 'data', 'movie_db.sqlite')}"
SQLITE = "sqlite:///" + os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data', 'movie_db.sqlite')
print(SQLITE)
print(__file__)

engine = create_engine(SQLITE)
Base.metadata.create_all(engine)

Session = Session(bind=engine)

#create your class
class Movies(Base):
    __tablename__ = 'movies'
    director_name = Column(String)
    num_critic_for_reviews = Column(Integer)
    duration = Column(Integer)
    director_facebook_likes = Column(Integer)
    actor_3_facebook_likes = Column(Integer)
    actor_2_name = Column(String)
    actor_1_facebook_likes = Column(Integer)
    gross = Column(Integer)
    genres = Column(String)
    actor_1_name = Column(String)
    movie_title = Column(String, primary_key=True)
    num_voted_users = Column(Integer)
    cast_total_facebook_likes = Column(Integer)
    actor_3_name = Column(String)
    facenumber_in_poster = Column(Integer)
    plot_keywords = Column(String)
    movie_imdb_link = Column(String)
    num_user_for_reviews = Column(Integer)
    language = Column(String)
    country = Column(String)
    content_rating = Column(String)
    budget = Column(Integer)
    title_year = Column(Integer)
    actor_2_facebook_likes = Column(Integer)
    imdb_score = Column(Float)
    aspect_ratio = Column(Float)
    movie_facebook_likes = Column(Integer)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

@app.route("/")
def names():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all passenger names"""
    # Query all passengers
    results = session.query(Movies.movie_title).all()

    session.close()

    # Convert list of tuples into normal list
    all_names = list(np.ravel(results))

    return jsonify(all_names)











#################################################
# Flask Routes
#################################################

# @app.route("/movies")
# def pullAllDetail(sql, engine):
#     return engine.execute(sql)


# @app.route("/api/v1.0/names")
# def names():
#     # Create our session (link) from Python to the DB
#     session = Session(engine)

#     """Return a list of all passenger names"""
#     # Query all passengers
#     results = session.query(Movie.movie_title).all()

#     session.close()

#     # Convert list of tuples into normal list
#     all_movies = list(np.ravel(results))

#     return jsonify(all_movies)


# @app.route("/api/v1.0/passengers")
# def passengers():
#     # Create our session (link) from Python to the DB
#     session = Session(engine)

#     """Return a list of passenger data including the name, age, and sex of each passenger"""
#     # Query all passengers
#     results = session.query(Passenger.name, Passenger.age, Passenger.sex).all()

#     session.close()

#     # Create a dictionary from the row data and append to a list of all_passengers
#     all_passengers = []
#     for name, age, sex in results:
#         passenger_dict = {}
#         passenger_dict["name"] = name
#         passenger_dict["age"] = age
#         passenger_dict["sex"] = sex
#         all_passengers.append(passenger_dict)

#     return jsonify(all_passengers)


if __name__ == '__main__':
    app.run(debug=True)
