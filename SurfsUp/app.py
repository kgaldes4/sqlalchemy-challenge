# Import the dependencies and tools

import numpy as np
import pandas as pd
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify
import datetime as dt


#################################################
# Database Setup
#################################################


# reflect an existing database into a new model
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect = True)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################

app = Flask(__name__)


#################################################
# Flask Routes
#################################################


#homepage

@app.route('/')
def welcome():
    return (
        f'Available Routes<br/>'
        f'/api/v1.0/precipitaion<br/>'
        f'/api/v1.0/stations<br/>'
        f'/api/v1.0/tobs<br/>'
       # f'/api/v1.0/<start></end><br/>'
    )
@app.route("/api/v1.0/precipitation")
def precipitaion():
   #create session link
   session = Session(engine)
   #query precipitation data
   rain = session.query(measurement.date, measurement.prcp).filter(measurement.date >= oneyear).all()
   session.colse()


   precipitaion = []
   for date, prcp in rain:
       prepre = {}
       prepre[date] = prcp
       precipitaion.append(prepre)
    
    #return JSON
   return jsonify(precipitation) 

#query and return JSON list of stations

@app.route("/api/v1.0/stations")
def stations():
    #create session link
    session = Session(engine)
    #query stations 
    stations = session.query(Station).all()
    Session.close()

    list_stations = []
    for station in stations:
        store = {}
        store['Station'] = station.station
        store["Station_Details"] = {"Station ID": station.id, "Name": name, "Station Latitude":station.latitude, "Staion Longitude":station.longitude}
        list_stations.append(store)
    #return JSON
    return jsonify(stations)

#query and return JSON list of tobs of most active station

@app.route("/api/v1.0/tobs")
def tobs():
   #start session link
    session = Session(engine)
    #query tobs data
    month_temp = session.query(Measurement.date, Measurement. tobs).filter(Measurement.station == 'USC00519281').filter(Measurement.date >= dt.date(2016,8,18)).all()

    session.close()

    list_tobs = []
    for date, tobs in month_temp:
        store2 = {}
        store2['Date'] = date
        store2["Temperature"] = tobs
        list_tobs.append(store2)
    
    #return JSON
    return jsonify(list_tobs)

# I was not able to get a working dynamic page. Will come back to it later for my own use

if __name__ == '__main__':
    app.run(debug=False)
