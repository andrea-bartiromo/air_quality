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
    # --- helper per generare serie con scale diverse ---
    def build_days(scale_avg=1.0, scale_min=1.0, scale_max=1.0):
        return [
            {
                "date": f"2025-10-{d:02d}",
                "min": round((5 + d * 0.1) * scale_min, 2),
                "average": round((10 + d * 0.2) * scale_avg, 2),
                "max": round((15 + d * 0.3) * scale_max, 2),
                "sample_size": 24,
            }
            for d in range(1, 11)
        ]

    # Ora le metriche hanno dati diversi
    metrics = {
        "PM10":  {"days": build_days(scale_avg=1.00, scale_min=1.00, scale_max=1.00)},
        "PM2_5": {"days": build_days(scale_avg=0.75, scale_min=0.80, scale_max=0.78)},
    }

    # ---- calcolo media ponderata 7 giorni per ogni metrica ----
    def weighted_avg_7d(series_days):
        last7 = series_days[-7:]  # ultimi 7 giorni
        num = den = 0.0
        for d in last7:
            avg = d.get("average")
            n = d.get("sample_size") or 0
            if avg is not None and n:
                num += avg * n
                den += n
        return round(num / den, 2) if den else None

    weighted = {
        k: {"weighted_average_7d": weighted_avg_7d(v.get("days", []))}
        for k, v in metrics.items()
    }
    # -----------------------------------------------------------

    return {
        "id": station_id,
        "name": f"Stazione {station_id.upper()}",
        "metrics": metrics,
        "weighted": weighted,
    }

# avvio stabile su Windows (niente reloader)
if __name__ == "__main__":
    port = int(os.getenv("PORT", "5001"))
    print(f"Avvio Flask su http://127.0.0.1:{port} ...")
    app.run(host="0.0.0.0", port=port, debug=True, use_reloader=False)
