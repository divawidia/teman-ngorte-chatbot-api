# Use the official lightweight Python image.
# https://hub.docker.com/_/python
FROM python:3.10-slim
# FROM ubuntu:22.04

# Allow statements and log messages to immediately appear in the Knative logs
#ENV PYTHONUNBUFFERED True

ENV PORT 8080
ENV HOST 0.0.0.0
ENV APP_HOME /app

WORKDIR $APP_HOME

# RUN apt-get update -y && apt-get install -y python3-pip

COPY requirements.txt .

# Install production dependencies.
RUN pip install --no-cache-dir -r requirements.txt

# Copy local code to the container image.
COPY . .

# RUN [ "python3", "-c", "import nltk; nltk.download('punkt', download_dir='/usr/local/nltk_data')" ] 
# RUN [ "python3", "-c", "import nltk; nltk.download('stopwords', download_dir='/usr/local/nltk_data')" ] 

# ENTRYPOINT [ "python3" ]

EXPOSE 8080

# Run the web service on container startup. Here we use the gunicorn
# webserver, with one worker process and 8 threads.
# For environments with multiple CPU cores, increase the number of workers
# to be equal to the cores available.
# Timeout is set to 0 to disable the timeouts of the workers to allow Cloud Run to handle instance scaling.
CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 app:app