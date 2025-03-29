# Use an official Python image
FROM python:3.10

# Set the working directory inside the container
WORKDIR /app

# Install required system libraries to avoid missing dependencies
RUN apt-get update && apt-get install -y \
    libgl1 libglib2.0-0 wget && \
    rm -rf /var/lib/apt/lists/*

# Copy application files
COPY . /app

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Download YOLOv3 model files to avoid missing files error
RUN wget -O yolov3.cfg https://raw.githubusercontent.com/pjreddie/darknet/master/cfg/yolov3.cfg && \
    wget -O yolov3.weights https://pjreddie.com/media/files/yolov3.weights && \
    wget -O coco.names https://raw.githubusercontent.com/pjreddie/darknet/master/data/coco.names

# Expose Flask port
EXPOSE 5000

# Run the Flask app
CMD ["python", "app.py"]

