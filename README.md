# The Air Quality Measurement Device
The Air Quality Device was built from multiple programs, each of which
are contained within their own directory in this package.

## Display
The display program consists of display.py, graphs.py, and several non-python
files included in this package. The display program communicates with the server
to retrieve data points and draw them to the screen. The display program can be run
using the following command: `python3 display.py`  

## sensor
The sensor program consists of a single python file (sensor.py) and a config file
(config.json). It relies on libraries designed to run specifically on the raspberry pi,
such as grove. The program periodically retrieves data from the pi's sensors and uploads
the data in small packets to the server. The program is run with `python3 sensor.py`

## server
The server directory contains all the necessary files and code to run the server.
Running `docker-compose up` with docker and docker-compose installed will run the full server with database. Running `python app.py` (with all of the dependencies in requirements.txt) will run just the flask server stand alone.
