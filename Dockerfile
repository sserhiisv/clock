FROM python:3.6.9-slim-buster

# Install Apt packages
RUN apt-get update && \
    apt-get install -y --no-install-recommends procps gcc build-essential libpq-dev wget curl vim less && \
    rm -rf /var/lib/apt/lists/*

# Python requirements
COPY . /opt/clock/

WORKDIR /opt/clock
RUN pip install -r requirements.txt