# Use an official Python base image
FROM python:3.7-slim-stretch

# Developer and mainteiner of the project
LABEL maintainer="Alexander Klein"

# Set the working directory to /app
WORKDIR /app

# Copy the requirements for the Python app
COPY requirements.txt /app/requirements.txt

# Install any needed packages specified in the requirements.txt file
RUN apt-get update \
 && pip install --upgrade pip \
 && apt-get install -y libpq-dev gcc \
 && pip install --trusted-host pypi.python.org -r requirements.txt

# Copy the current directory contents into the container workdir
COPY . /app

# Run app when the container launches
CMD ["python", "run.py"]
