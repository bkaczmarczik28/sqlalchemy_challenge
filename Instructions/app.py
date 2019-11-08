#app.py for Homework 10 SQLAlchemy challenge
from flask import Flask, jsonify
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station=Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#Define what to do when the user hits the index route
@app.route("/")
def home():
    print("Server recieved request for 'About' page...")
    return (
        f"Welcome to my 'About' page!</br>"
        f"Avaliable Routes: <br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        "/api/v1.0/temp/start/end"
    )

@app.route('/api/v1.0/precipitation')
def precipitation():
    print("Server recieved request for 'Precipitation' page...")
    #Convert the query results to a Dictionary using date as the key and prcp as the value.
    #Return the JSON representation of your dictionary.
    
    # Query all precipitation date one year from last date it the sqlite file
    lastdate_query=session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= '2016-08-23').all()

    session.close()

    precipitation={date:\
         prcp for date, prcp in lastdate_query}

    return jsonify(precipitation)

@app.route('/api/v1.0/stations')
def stations():
    print("Server recieved request for 'Stations' page...")
    #Return a JSON list of stations from the dataset.
    results=session.query(Station.station).all()

    #convert to a list
    stations=list(np.ravel(results))
    return jsonify(stations)

@app.route('/api/v1.0/tobs')
def tobs():
    print("Server recieved request for 'Jobs' page...")
    #query for the dates and temperature observations from a year from the last data point.
    #Return a JSON list of Temperature Observations (tobs) for the previous year.

    results=session.query(Measurement.tobs).\
        filter(Measurement.date >= '2016-08-23').\
        filter(Measurement.station == "USC00519281").all()

    #convert to list
    temps=list(np.ravel(results))

    return jsonify(temps)

@app.route('/api/v1.0/temp/<start>')
@app.route('/api/v1.0/temp/<start>/<end>')
def tempstats(start=None, end=None):
    print("Server recieved request for 'start temp' page...")
    #Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.
    #When given the start only, calculate TMIN, TAVG, and TMAX for all dates greater than and equal to the start date.
    #When given the start and the end date, calculate the TMIN, TAVG, and TMAX for dates between the start and end date inclusive.
    sel = [func.min(Measurement.tobs),\
            func.avg(Measurement.tobs),\
            func.max(Measurement.tobs)\
          ]

    #query if only given a start date
    if not end:
        results = session.query(*sel).\
            filter(Measurement.date >= start).all()
        temps = list(np.ravel(results))
        return jsonify(temps)

    #query if given a start and end date
    results = session.query(*sel).\
        filter(Measurement.date >= start).\
        filter(Measurement.date <= end).all()
    temps = list(np.ravel(results))
    return jsonify(temps)


if __name__=="__main__":
    app.run(debug=True)