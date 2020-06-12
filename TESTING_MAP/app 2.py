import os
import numpy as np

from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from sqlalchemy import Column, Integer, String, Float

from flask import Flask, jsonify


SQLITE = "sqlite:///" + os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data', 'zipcode_db.sqlite')
print(SQLITE)

engine = create_engine(SQLITE)
Base.metadata.create_all(engine)
session = Session(bind=engine)

class Zipcode(Base):
    __tablename__ = 'zipcode'
    zip = Column(Integer, primary_key = True)
    latitude = Column(Float)
    longitude = Column(Float)

app = Flask(__name__)

@app.route("/")
def welcome():
    return (
        f"/zipcodes<br/>"
    )

@app.route("/zipcodes")
def zipcode():
    session = Session(engine)

    results = session.query(Zipcode.zip, Zipcode.latitude, Zipcode.longitude).all()

    session.close()

    all_zipcodes = []
    for zip, latitude, longitude  in results:
        zipcode_dict = {}
        zipcode_dict["zip"] = zip
        zipcode_dict["lat"] = latitude
        zipcode_dict["lon"] = longitude
        all_zipcodes.append(zipcode_dict)
        
    return jsonify(all_zipcodes)





@app.route("/hike") 
def hike():

    #session = Session(engine)

    #results = session.query(Zipcode.zip, Zipcode.latitude, Zipcode.longitude).all()

    #session.close()

    #zipcode = [result[0] for result in results]
    #lat = [result[1] for result in results]
    #lon = [result[2] for result in results]

    #hike_data = [{
       # "zip": zipcode,
        #"lat": lat,
       # "lon": lon
    #}]

    #return jsonify(hike_data)



if __name__ == '__main__':
    app.run(debug=True, threaded = True, host='localhost', port = 5444)