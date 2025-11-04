# backend/app.py
import os
from flask import Flask, jsonify, request
from flask_cors import CORS
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

@app.get("/")
def index():
    return {"status": "ok"}

@app.get("/api/ping")
def ping():
    return {"pong": True}

@app.get("/api/stations")
def stations():
    return [
        {"id": "s1", "name": "Stazione Demo 1"},
        {"id": "s2", "name": "Stazione Demo 2"}
    ]

@app.get("/api/stations/<station_id>")
def station_detail(station_id):
    days = [
        {"date": f"2025-10-{d:02d}", "min": 5+d*0.1, "average": 10+d*0.2, "max": 15+d*0.3, "sample_size": 24}
        for d in range(1, 11)
    ]
    return {
        "id": station_id,
        "name": f"Stazione {station_id.upper()}",
        "metrics": {
            "PM10": {"days": days},
            "PM2_5": {"days": days}
        },
        "weighted": {
            "PM10": {"weighted_average_7d": 12.3},
            "PM2_5": {"weighted_average_7d": 8.9}
        }
    }


if __name__ == "__main__":
    port = int(os.getenv("PORT", "5001"))
    app.run(host="0.0.0.0", port=port, debug=True)

