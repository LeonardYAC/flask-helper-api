from flask import Flask, request, jsonify
import base64
import requests

app = Flask(__name__)

HF_API_URL = "https://hf.space/embed/LYAC/quest-ai/+/api/predict"

@app.route("/", methods=["GET"])
def hello():
    return "Helper API is running."

@app.route("/upload", methods=["POST"])
def upload():
    if 'file' not in request.files:
        return jsonify({"error": "No file sent"}), 400

    file = request.files['file']
    image_bytes = file.read()

    b64_string = base64.b64encode(image_bytes).decode("utf-8")
    data_url = f"data:image/jpeg;base64,{b64_string}"

    payload = {
        "data": [data_url]
    }

    try:
        res = requests.post(HF_API_URL, json=payload)
        return jsonify(res.json())
    except Exception as e:
        return jsonify({"error": str(e)}), 500