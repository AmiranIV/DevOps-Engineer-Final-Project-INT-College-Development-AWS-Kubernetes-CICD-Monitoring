# Dockerfile Yolo 

# First stage: Use the base image you have
FROM amiraniv/amiraniv-k8s-yolov5:v13.0 

# Set the working directory inside the container
WORKDIR /app

# Copy the application code and requirements file into the container
COPY  . . 

# Install the required dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Command to run your application
CMD ["python3", "COMBINEDCODES.py"]
