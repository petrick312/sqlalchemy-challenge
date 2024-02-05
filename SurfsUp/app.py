## please note that I worked with my team: Kat, Haritha, and Carmen to complete this homework

# Import the dependencies.
import numpy as np

import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

#################################################
# Database Setup
#################################################

# Create engine using the `hawaii.sqlite` database file
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# Declare a Base using `automap_base()`
Base = automap_base()

# Use the Base class to reflect the database tables
Base.prepare(engine, reflect=True)

# View all of the classes that automap found
Base.classes.keys()
print(Base.classes.keys())

# Assign the measurement class to a variable called `Measurement` and
# the station class to a variable called `Station`
Measurement = Base.classes.measurement
Station = Base.classes.station


#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################

# Define what to do when the user hits the homepage
# Start at the homepage.
# List all the available routes.

@app.route("/")
def homepage():
    return (
        f"<h1>Available Routes for Hawaii Weather Data:</h1><br/>"
        f"<a href='/api/v1.0/precipitation'> For Daily Precipitation Totals for Previous 12 Months of Data</a>"
        f"<p><strong>/api/v1.0/precipitation </strong></p><br/><br/>"
        f"<a href='/api/v1.0/stations'> For Active Weather Stations</a>"
        f"<p><strong>/api/v1.0/stations </strong></p><br/><br/>"
        f"<a href='/api/v1.0/tobs'> For Daily Temperature Observations for Station USC00519281 for Previous 12 Months of Data</a>"
        f"<p><strong>/api/v1.0/tobs </strong></p><br/><br/>"
        f"<a href='/api/v1.0/&lt;start&gt'> For Min, Average & Max Temperatures for Specific Date</a>"
        f"<p><strong>/api/v1.0/&lt;start&gt (replace &lt;start&gt  with date in yyyy-mm-dd format) </strong></p><br/><br/>"
        f"<a href='/api/v1.0/&lt;start&gt;/&lt;end&gt'> For Min, Average & Max Temperatures for Date Range</a>"
        f"<p><strong>/api/v1.0/&lt;start&gt;/&lt;end&gt; (replace &lt;start&gt and &lt;end&gt with dates in yyyy-mm-dd format) </strong></p></a><br/>"
    )


# Define what to do when the user hits the precipitation URL
# Convert the query results from your precipitation analysis (i.e. retrieve only the last 12 months of data) to a dictionary using date as the key and prcp as the value.
# Return the JSON representation of your dictionary.

@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create the session
    session = Session(engine)

    # Query precipitation data from last 12 months from the most recent date from Measurement table
    prcp_data = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= "2016-08-24").\
    filter(Measurement.date <= "2017-08-23").\
    order_by(Measurement.date).all()

    # Close the session                   
    session.close()
    
    # Create a dictionary from the row data and append to a list of prcp_list
    prcp_list = {date: prcp for date, prcp in prcp_data}
    
    # Return a list of jsonified precipitation data for the previous 12 months 
    return jsonify(prcp_list)


# Define what to do when the user hits the station URL
# Return a JSON list of stations from the dataset.

@app.route("/api/v1.0/stations")
def stations():
    # Create the session
    session = Session(engine)

    # Query station data from the Station dataset
    station_data = session.query(Station.station, Station.name).all()

    # Close the session                   
    session.close()

    # Set data to be printed
    station_list = {station: name for station, name in station_data}

    # Return a list of jsonified station data
    return jsonify(station_list)
    

# Define what to do when the user hits the URL
# Query the dates and temperature observations of the most-active station for the previous year of data.
# Return a JSON list of temperature observations for the previous year.

@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session
    session = Session(engine)

    # Query tobs data from last 12 months from the most recent date from Measurement table
    tobs_data = session.query(Measurement.date, Measurement.prcp).filter(Measurement.station == 'USC00519281').\
        filter(Measurement.date >= "2016-08-24").\
        filter(Measurement.date <= "2017-08-23").all()
    
    # Close the session                   
    session.close()
    
    # Display list of data
    #tobs_list = {tobs: tobs for date, tobs in tobs_data}

    # Create a dictionary from the row data and append to a list of tobs_list
    tobs_list = []
    for date, tobs in tobs_data:
        tobs_dict = {}
        tobs_dict["date"] = date
        tobs_dict["tobs"] = tobs
        tobs_list.append(tobs_dict)
    # # Return a list of jsonified tobs data for the previous 12 months
    return jsonify(tobs_list)


# Define what to do when the user hits the URL with a specific start date
# Return a JSON list of the minimum temperature, the average temperature, and the maximum temperature for a specified date
# For a specified start, calculate TMIN, TAVG, and TMAX for all the dates greater than or equal to the start date.

@app.route("/api/v1.0/<start>")
def start_date(start):
    # Create our session (link) from Python to the DB
    session = Session(engine)
    """Return a JSON list of the minimum temperature, the average temperature, and the maximum temperature for a specified start or start-end range."""
    
    # For a specified start, calculate TMIN, TAVG, and TMAX for all the dates greater than or equal to the start date.
    start_tobs = session.query(func.min(Measurement.tobs),func.max(Measurement.tobs),func.avg(Measurement.tobs)).filter(Measurement.date >= start).all()
    
    # Close Session
    session.close()
    
    # Create a dictionary from the row data and append to a list of start_tobs_list
    start_tobs_list = []
    for min, max, avg in start_tobs:
        start_dict = {}
        start_dict["min"] = min
        start_dict["max"] = max
        start_dict["avg"] = avg
        start_tobs_list.append(start_dict)
    return jsonify(start_tobs_list)


# Define what to do when the user hits the URL with a specific start-end range
# Return a JSON list of the minimum temperature, the average temperature, and the maximum temperature for a specified start-end range.
# For a specified start date and end date, calculate TMIN, TAVG, and TMAX for the dates from the start date to the end date, inclusive.

@app.route("/api/v1.0/<start>/<end>")
def start_end_date(start,end):
    # Create our session (link) from Python to the DB
    session = Session(engine)
    """Return a JSON list of the minimum temperature, the average temperature, and the maximum temperature for a specified start or start-end range."""
    
    # For a specified start, calculate TMIN, TAVG, and TMAX for all the dates greater than or equal to the start date.
    start_end_tobs = session.query(func.min(Measurement.tobs),func.max(Measurement.tobs),func.avg(Measurement.tobs)).filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    # Close Session
    session.close()

    # Create a dictionary from the row data and append to a list of start_end_tobs_list
    start_end_tobs_list = []
    for min, max, avg in start_end_tobs:
        start_end_dict = {}
        start_end_dict["min"] = min
        start_end_dict["max"] = max
        start_end_dict["avg"] = avg
        start_end_tobs_list.append(start_end_dict)
    return jsonify(start_end_tobs_list)


# Define main branch 
if __name__ == '__main__':
    app.run(debug=True)
