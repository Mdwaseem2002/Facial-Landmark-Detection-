import flask
from flask import request, jsonify
import dlib
import cv2
import numpy as np
import base64
from PIL import Image
import io
from flask_cors import CORS

app = flask.Flask(__name__)
CORS(app)

# Load facial landmark detector
predictor_path = "/home/waseem/project/server/shape_predictor_68_face_landmarks.dat"  # Download from http://dlib.net/files/
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor(predictor_path)


def process_image(image_data):
    """Decodes, detects faces, finds landmarks, and returns processed image in base64"""
    img_bytes = base64.b64decode(image_data)
    img_array = np.frombuffer(img_bytes, dtype=np.uint8)  # Efficient conversion
    img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = detector(gray)

    for face in faces:
        landmarks = predictor(gray, face)

        # Draw landmarks (modify if needed)
        for n in range(68):
            x = landmarks.part(n).x
            y = landmarks.part(n).y
            cv2.circle(img, (x, y), 2, (0, 255, 0), -1)  

    # Convert back to base64 for sending
    retval, buffer = cv2.imencode('.jpg', img)
    # Save the processed image
    with open("last_processed_image.jpg", "wb") as f:
        f.write(buffer)
    jpg_as_text = base64.b64encode(buffer).decode('utf-8')
    return jpg_as_text

@app.route("/")
def home():
    return 'hello'


@app.route("/process", methods=["POST"])
def process():
    if request.method == "POST":
        image_data = request.json.get("image")
        if not image_data:
            return jsonify({"error": "Please provide a base64-encoded image."}), 400

        try:
            processed_image = process_image(image_data)
            return jsonify({"processed_image": processed_image})
        except Exception as e:
            return jsonify({"error": f"Image processing failed: {str(e)}"}), 500


@app.route("/processed", methods=["GET"])
def get_processed_image():
    # Assumes you have stored the last processed image somewhere

    with open("last_processed_image.jpg", "rb") as f:
        image_data = f.read()
    base64_image = base64.b64encode(image_data).decode('utf-8')
    return jsonify({"image": base64_image})


if __name__ == "__main__":
    app.run(debug=True)
