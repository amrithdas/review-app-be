# Use the official Python image from the Docker Hub
FROM python:3.9-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set the working directory
WORKDIR /reviewapp

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev

# Install Python dependencies
COPY requirements.txt /reviewapp/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy project files to the working directory
COPY . /reviewapp/
