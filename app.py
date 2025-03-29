from flask import Flask, render_template, request, send_from_directory
import cv2
import numpy as np
import os
import time

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
RESULT_FOLDER = "static/results"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(RESULT_FOLDER, exist_ok=True)

# Load YOLO
net = cv2.dnn.readNet("yolov3.weights", "yolov3.cfg")
with open("coco.names", "r") as f:
    classes = [line.strip() for line in f.readlines()]
layer_names = net.getLayerNames()
output_layers = [layer_names[i - 1] for i in net.getUnconnectedOutLayers()]

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Get uploaded file
        file = request.files["file"]
        if not file:
            return "No file uploaded!", 400
        
        # Save the uploaded file
        file_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(file_path)

        # Process image with YOLO
        img = cv2.imread(file_path)
        height, width, _ = img.shape

        # Prepare YOLO input
        blob = cv2.dnn.blobFromImage(img, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
        net.setInput(blob)
        detections = net.forward(output_layers)

        for detection in detections:
            for obj in detection:
                scores = obj[5:]
                class_id = np.argmax(scores)
                confidence = scores[class_id]

                if confidence > 0.5:
                    # Get bounding box coordinates
                    center_x, center_y, w, h = (obj[0:4] * [width, height, width, height]).astype(int)
                    x, y = center_x - w // 2, center_y - h // 2

                    # Draw bounding box
                    color = (0, 255, 0)  # Green
                    cv2.rectangle(img, (x, y), (x + w, y + h), color, 2)
                    cv2.putText(img, f"{classes[class_id]} {confidence:.2f}", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

        # Save processed image
        result_path = os.path.join(RESULT_FOLDER, file.filename)
        cv2.imwrite(result_path, img)

        return render_template("index.html", uploaded=True, result_image=file.filename)

    return render_template("index.html", uploaded=False)

@app.route("/static/results/<filename>")
def result_file(filename):
    return send_from_directory(RESULT_FOLDER, filename)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

