#################################################
# Flask Setup
#################################################

from flask import Flask, jsonify
app = Flask(__name__)

#################################################
# Database Setup
#################################################

import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

engine = create_engine("sqlite:///Resources/hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)

Measurement = Base.classes.measurement
Station = Base.classes.station

session = Session(engine)

#################################################
# Flask Routes
#################################################

@app.route("/")
def home():
    print("Server received request for Home page")
    return(
        f"Welcome to the Climate API!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/yyyy-mm-dd<br/>"
        f"/api/v1.0/yyyy-mm-dd/yyyy-mm-dd<br/>"
    )

@app.route("/api/v1.0/stations")
def stations():
    """Return list of stations as json"""
    list_of_stations = session.query(Station.station, Station.name)
    all_stations = []
    for s, n in list_of_stations:
        station_dict = {}
        station_dict["station"] = s
        station_dict["name"] = n
        all_stations.append(station_dict)
    return jsonify(all_stations)

@app.route("/api/v1.0/precipitation")
def precipitation():
    precipitation_data = session.query(Measurement.station,\
         Measurement.date, Measurement.prcp)
    all_precipitation = []
    for s, d, p in precipitation_data:
        precipitation_dict = {}
        precipitation_dict[d + "_" + s] = p
        all_precipitation.append(precipitation_dict)
    return jsonify(all_precipitation)

@app.route("/api/v1.0/tobs")
def tobs():
    import datetime as dt   
    last_date_result = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    for r in last_date_result:
        last_date = r
    dt1 = dt.datetime.strptime(last_date, "%Y-%m-%d")
    query_date = dt1 - dt.timedelta(days=365)
    tobs_data = session.query(Measurement.station,\
        Measurement.date, Measurement.tobs).\
        filter(Measurement.date == dt.datetime.date(query_date))
    all_tobs = []
    for s, d, t in tobs_data:
        tobs_dict = {}
        tobs_dict["station"] = s
        tobs_dict["date"] = d
        tobs_dict["tobs"] = t
        all_tobs.append(tobs_dict)
    return jsonify(all_tobs)

@app.route("/api/v1.0/<date1>/<date2>")
def beg_end(date1, date2):
    import datetime as dt   
    start_date = date1
    end_date = date2
    TMIN = session.query(func.min(Measurement.tobs)).\
        filter(Measurement.date >= start_date).\
        filter(Measurement.date <= end_date).scalar()
    TMAX = session.query(func.max(Measurement.tobs)).\
        filter(Measurement.date >= start_date).\
        filter(Measurement.date <= end_date).scalar()
    TAVG = session.query(func.avg(Measurement.tobs)).\
        filter(Measurement.date >= start_date).\
        filter(Measurement.date <= end_date).scalar()
    stats = []
    stats_dict = {}
    stats_dict["minimum temperture"] = TMIN
    stats_dict["maximum temperture"] = TMAX
    stats_dict["average temperture"] = TAVG
    stats.append(stats_dict)
    return jsonify(stats)

@app.route("/api/v1.0/<date>")
def beg(date):
    import datetime as dt   
    start_date = date
    TMIN = session.query(func.min(Measurement.tobs)).\
        filter(Measurement.date >= start_date).scalar()
    TMAX = session.query(func.max(Measurement.tobs)).\
        filter(Measurement.date >= start_date).scalar()
    TAVG = session.query(func.avg(Measurement.tobs)).\
        filter(Measurement.date >= start_date).scalar()
    stats = []
    stats_dict = {}
    stats_dict["minimum temperture"] = TMIN
    stats_dict["maximum temperture"] = TMAX
    stats_dict["average temperture"] = TAVG
    stats.append(stats_dict)
    return jsonify(stats)

if __name__ == "__main__":
    app.run(debug=True)
