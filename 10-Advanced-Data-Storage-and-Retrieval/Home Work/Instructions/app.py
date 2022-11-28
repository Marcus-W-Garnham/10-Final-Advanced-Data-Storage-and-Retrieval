import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify

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
Station = Base.classes.station

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################
@app.route("/")
def welcome():
    # List all available api routes.
    return (
        'Available Routes: <br/>' 
        '/api/v1.0/precipitation <br/>'
        '/api/v1.0/stations <br/>'
        '/api/v1.0/tobs <br/>'
        '/api/v1.0/<start> <br/>'
        '/api/v1.0/<start>/<end> <br/>'
    )

# This route will show all our precipitation for all times recorded  
@app.route("/api/v1.0/precipitation")
def precipitation():

    # Convert the query results to a dictionary using `date` as the key and `prcp` as the value.
    session = Session(engine)

    results = session.query(Measurement.date, Measurement.prcp).all()

    session.close()

    all_Measurement = []
    for date, prcp in results:
        Measurement_dict = {}
        Measurement_dict["date"] = date
        Measurement_dict["prcp"] = prcp
        all_Measurement.append(Measurement_dict)

    # Return the JSON representation of your dictionary. 
    return jsonify(
        all_Measurement
        )
        # end of precipitation data route


@app.route("/api/v1.0/stations")
def stations():
    # Return a JSON list of stations from the dataset.

    session = Session(engine)

    results = session.query(Station.id, Station.station).all()

    session.close()

    all_Stations = []
    for id, station in results:
        Stations_dict = {}
        Stations_dict["id"] = id
        Stations_dict["station"] = station
        all_Stations.append(Stations_dict)

    return jsonify(
        all_Stations
    )


if __name__ == '__main__':
    app.run(debug=True)