# Use an official Python runtime as a parent image
FROM python:3.9

# Sets the container working directory
WORKDIR /app

# Adds the current directory (on the host machine) to the path `/app` in the image
ADD . /app

# Update/upgrade the system
RUN apt -y update
RUN apt -y upgrade

# Install App dependencies and chrome webdriver
RUN apt install -yqq unzip curl wget python3-pip
RUN DEBIAN_FRONTEND="noninteractive" apt-get -y install tzdata
RUN wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
RUN apt install -y --no-install-recommends ./google-chrome-stable_current_amd64.deb
RUN wget -O /tmp/chromedriver.zip http://chromedriver.storage.googleapis.com/$(curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE)/chromedriver_linux64.zip
RUN unzip /tmp/chromedriver.zip chromedriver -d /usr/local/bin/

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Install additional dependencies for Selenium
RUN apt-get update && apt-get install -y \
    wget \
    xvfb \
    unzip

RUN apt-get install chromium -y

RUN python -c "import nltk; nltk.download('stopwords')"
COPY . /app/
# Set display port to avoid crash
ENV DISPLAY=:99

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Define environment variable
ENV NAME World
ENV env production

# Run app.py when the container launches
CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 app:app
