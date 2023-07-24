# Use an official Python runtime as a parent image
FROM python:3.9

# Sets the container working directory
WORKDIR /app

# Adds the current directory (on the host machine) to the path `/app` in the image
ADD . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Install additional dependencies for Selenium
RUN apt-get update && apt-get install -y \
    wget \
    xvfb \
    unzip

# Set display port to avoid crash
ENV DISPLAY=:99

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Define environment variable
ENV NAME World

# Run app.py when the container launches
CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 app:app
