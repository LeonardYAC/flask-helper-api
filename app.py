from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/classify", methods=["POST"])
def classify():
    if 'file' not in request.files:
        return jsonify({"error": "No file sent"}), 400
    return jsonify({"success": "File received"}), 200
