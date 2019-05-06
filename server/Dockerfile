# Creates the docker container

FROM python:latest # The base (python) image

# setup enviornment variables

ENV PYTHONUNBUFFERED 1

ENV FLASK_APP api

ENV FLASK_DEBUG true

WORKDIR /usr/src/

ADD . /usr/src/ # Add entire directory to the container

RUN pip install --no-cache-dir -r requirements.txt # run through and install all required python modules

Add ./uwsgi.ini /etc/uwsgi.ini # uwsgi config file

EXPOSE 5000 # default flask port

CMD uwsgi --ini /etc/uwsgi.ini
