from flask import Flask, request, jsonify
import base64
import requests

app = Flask(__name__)

HF_API_URL = "https://hf.space/embed/LYAC/quest-ai/+/api/predict"

@app.route("/", methods=["GET"])
def hello():
    return "Helper API is running."

@app.route("/classify", methods=["POST"])  # <- renamed for clarity
def classify():
    if 'file' not in request.files:
        return jsonify({"error": "No file sent"}), 400

    file = request.files['file']
    image_bytes = file.read()

    # Optional: detect image type from MIME
    mime_type = file.mimetype or "image/jpeg"
    if not mime_type.startswith("image/"):
        return jsonify({"error": "Uploaded file is not an image"}), 400

    # Convert to base64
    b64_string = base64.b64encode(image_bytes).decode("utf-8")
    data_url = f"data:{mime_type};base64,{b64_string}"

    payload = {
        "data": [data_url]
    }

    try:
        response = requests.post(HF_API_URL, json=payload)
        return jsonify(response.json())
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
