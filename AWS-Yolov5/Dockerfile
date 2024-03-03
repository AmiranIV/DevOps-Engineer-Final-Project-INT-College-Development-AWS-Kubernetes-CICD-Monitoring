# Use an official Python runtime as the base image
FROM python:3.9-slim

# Upgrade pip
RUN pip install --no-cache-dir --upgrade pip

# Install required system packages (including OpenGL and libgthread)
RUN apt-get update && \
    apt-get install -y libgl1-mesa-glx libglib2.0-0 && \
    rm -rf /var/lib/apt/lists/*

# Set the working directory inside the container
WORKDIR /app

# Copy the application code and requirements file into the container
COPY . /app

# Install the required dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Command to run your application
CMD ["python3", "COMBINEDCODES.py"]
