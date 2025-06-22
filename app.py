from flask import Flask, request, jsonify
import base64
import requests

app = Flask(__name__)

# Hugging Face endpoint
HF_API_URL = "https://hf.space/embed/LYAC/quest-ai/+/api/predict"

@app.route("/", methods=["GET"])
def hello():
    return "Helper API is running."

@app.route("/classify", methods=["POST"])
def classify():
    # Check if image was uploaded as a file
    if 'file' not in request.files:
        return jsonify({"error": "No file sent"}), 400

    file = request.files['file']
    image_bytes = file.read()

    # Convert image to base64
    b64_string = base64.b64encode(image_bytes).decode("utf-8")
    data_url = f"data:image/jpeg;base64,{b64_string}"

    # Create payload for Hugging Face model
    payload = {
        "data": [data_url]
    }

    try:
        # Send to Hugging Face API
        response = requests.post(HF_API_URL, json=payload)

        # Return Hugging Face result to MIT App Inventor
        return jsonify(response.json())

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Optional: to test GET method in browser
@app.route("/test", methods=["GET"])
def test():
    return "API is live and reachable."
