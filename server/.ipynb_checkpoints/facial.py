from flask import Flask, request, jsonify
import cv2
import mediapipe as mp

app = Flask(__name__)

# Initialize MediaPipe face mesh
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(static_image_mode=True, max_num_faces=1, min_detection_confidence=0.5, min_tracking_confidence=0.5)
draw = mp.solutions.drawing_utils

@app.route('/detect_face_landmarks', methods=['POST', 'GET'])
def detect_face_landmarks():
    if request.method == 'POST':
        # Read the uploaded image
        file = request.files['image']
        image = cv2.imdecode(np.fromstring(file.read(), np.uint8), cv2.IMREAD_COLOR)

        # Convert the BGR image to RGB
        rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        # Process the image with MediaPipe face mesh
        results = face_mesh.process(rgb_image)

        # Draw face landmarks
        if results.multi_face_landmarks:
            for face_landmarks in results.multi_face_landmarks:
                # Draw the face landmarks
                for landmark in face_landmarks.landmark:
                    x = int(landmark.x * image.shape[1])
                    y = int(landmark.y * image.shape[0])
                    cv2.circle(image, (x, y), 2, (0, 255, 0), -1)

        # Encode the processed image to send back as response
        _, img_encoded = cv2.imencode('.jpg', image)
        response = img_encoded.tobytes()

        return response, 200, {'Content-Type': 'image/jpeg'}

    elif request.method == 'GET':
        return "Use POST method to upload an image.", 200

if __name__ == '__main__':
    app.run(debug=True)
