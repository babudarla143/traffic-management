from flask import Flask, render_template, jsonify, request
import requests  
from config import (
    GRAPH_HOPPER_API_KEY,
    WEATHER_API_KEY,
    GOOGLE_BACKEND_API_KEY,
    GOOGLE_FRONT_END_API_KEY,
    TOMTOM_API_KEY
)

app = Flask(__name__)

@app.route('/')
def index():
    return render_template(
        "index.html",
        google_maps_api_key=GOOGLE_FRONT_END_API_KEY,
        graph_hopper_api_key=GRAPH_HOPPER_API_KEY,
        weather_api_key=WEATHER_API_KEY,
        google_backend_api_key=GOOGLE_BACKEND_API_KEY,
        traffic_api_key=TOMTOM_API_KEY
    )

@app.route("/traffic", methods=["GET"])
def get_traffic_data():
    lat = request.args.get("lat")
    lon = request.args.get("lon")

    if not lat or not lon:
        return jsonify({"error": "Latitude and Longitude are required"}), 400

    try:
        lat = float(lat)
        lon = float(lon)
    except ValueError:
        return jsonify({"error": "Invalid latitude or longitude format"}), 400

    url = f"https://api.tomtom.com/traffic/services/4/flowSegmentData/absolute/10/json?point={lat},{lon}&key={TOMTOM_API_KEY}"

    try:
        response = requests.get(url)
        response.raise_for_status()
        return jsonify(response.json()), 200
    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
