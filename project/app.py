"""
app.py
------
Main Flask application for the AI Crop Disease Prediction System.

Routes:
    GET  /            → Upload dashboard (index.html)
    POST /predict     → Handle image upload + run AI inference → result.html
    GET  /history     → Show last 10 predictions from session
    GET  /clear       → Clear prediction history
    GET  /about       → About page (static)

Run:
    python app.py        (development server on port 5000)
"""

import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'  # Suppress TF logging to save memory/noise
import sys
import uuid
import json
import sqlite3
import requests
from datetime import datetime

from flask import (
    Flask, render_template, request, redirect,
    url_for, flash, session, jsonify
)
from werkzeug.utils import secure_filename

# ─────────────────────────────────────────────────────────────────────────────
# Sys-path fix so imports work whether run from project/ or anywhere else
# ─────────────────────────────────────────────────────────────────────────────
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE_DIR)

from utils.predict        import predict_disease, load_model_once
from utils.recommendations import get_recommendation
from model.disease_classes import get_display_name

# ─────────────────────────────────────────────────────────────────────────────
# Flask app setup
# ─────────────────────────────────────────────────────────────────────────────
app = Flask(__name__)
app.secret_key = "crop-disease-ai-secret-key-2024"   # Change in production

# ─────────────────────────────────────────────────────────────────────────────
# Upload configuration
# ─────────────────────────────────────────────────────────────────────────────
UPLOAD_FOLDER   = os.path.join(BASE_DIR, "static", "uploads")
ALLOWED_EXTENSIONS = {"jpg", "jpeg", "png", "bmp", "webp"}
MAX_CONTENT_LENGTH = 16 * 1024 * 1024   # 16 MB max upload size

app.config["UPLOAD_FOLDER"]     = UPLOAD_FOLDER
app.config["MAX_CONTENT_LENGTH"] = MAX_CONTENT_LENGTH

os.makedirs(UPLOAD_FOLDER, exist_ok=True)   # Create uploads dir if missing

# ─────────────────────────────────────────────────────────────────────────────
# Radar DB configuration
# ─────────────────────────────────────────────────────────────────────────────
RADAR_DB = os.path.join(BASE_DIR, "radar.db")

def init_radar_db():
    with sqlite3.connect(RADAR_DB) as conn:
        c = conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS radar_points (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                lat REAL NOT NULL,
                lng REAL NOT NULL,
                disease_name TEXT NOT NULL,
                severity TEXT NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        conn.commit()

init_radar_db()

# ─────────────────────────────────────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────────────────────────────────────

def allowed_file(filename: str) -> bool:
    """Return True if filename has an allowed extension."""
    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS
    )


def get_confidence_level(confidence: float) -> str:
    """Translate confidence % into a user-friendly label."""
    if confidence >= 90:
        return "Very High"
    elif confidence >= 75:
        return "High"
    elif confidence >= 60:
        return "Moderate"
    else:
        return "Low"


def get_severity_color(severity: str) -> str:
    """Map severity string to Bootstrap color class."""
    return {
        "low"    : "success",
        "medium" : "warning",
        "high"   : "danger",
    }.get(severity, "secondary")


def get_weather_risk(lat: float, lng: float) -> dict:
    """Fetch current weather from Open-Meteo and generate proactive risk warnings."""
    weather_data = {
        "available": False,
        "temperature": None,
        "humidity": None,
        "warnings": []
    }
    try:
        url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lng}&current=temperature_2m,relative_humidity_2m"
        response = requests.get(url, timeout=3)
        if response.status_code == 200:
            data = response.json()
            current = data.get("current", {})
            temp = current.get("temperature_2m")
            humidity = current.get("relative_humidity_2m")
            
            if temp is not None and humidity is not None:
                weather_data["available"] = True
                weather_data["temperature"] = temp
                weather_data["humidity"] = humidity
                
                # Simple proactive rules
                if humidity > 80:
                    weather_data["warnings"].append("High humidity detected. Increased risk of fungal diseases like Blight or Mildew. Ensure good ventilation/spacing.")
                if temp > 35:
                    weather_data["warnings"].append("Extreme heat detected. Increased risk of heat stress and spider mites. Ensure adequate irrigation.")
                if temp < 15 and humidity > 70:
                    weather_data["warnings"].append("Cool, damp conditions detected. Ideal for Late Blight development. Monitor leaves closely.")
                    
    except Exception as e:
        print(f"[WARN] Weather API failed: {e}")
        
    return weather_data


# ─────────────────────────────────────────────────────────────────────────────
# Load model at startup
# ─────────────────────────────────────────────────────────────────────────────
with app.app_context():
    load_model_once()   # Warm-up model load (uses singleton)


# ─────────────────────────────────────────────────────────────────────────────
# Routes
# ─────────────────────────────────────────────────────────────────────────────

@app.route("/")
def index():
    """Landing page with drag-and-drop upload interface."""
    return render_template("index.html")


@app.route("/predict", methods=["POST"])
def predict():
    """
    Handle image upload, run AI prediction, and return results page.
    """
    # ── Validate file presence ─────────────────────────────────────────────
    if "file" not in request.files:
        flash("No file uploaded. Please select a crop leaf image.", "danger")
        return redirect(url_for("index"))

    file = request.files["file"]

    if file.filename == "":
        flash("No file selected. Please choose a JPG or PNG image.", "danger")
        return redirect(url_for("index"))

    if not allowed_file(file.filename):
        flash("Invalid file type. Please upload a JPG, PNG, or BMP image.", "warning")
        return redirect(url_for("index"))

    # ── Save file ──────────────────────────────────────────────────────────
    ext       = file.filename.rsplit(".", 1)[1].lower()
    unique_id = uuid.uuid4().hex[:10]
    filename  = f"{unique_id}.{ext}"
    save_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)

    file.save(save_path)

    # ── Run prediction ─────────────────────────────────────────────────────
    try:
        prediction = predict_disease(save_path)
    except Exception as exc:
        flash(f"Prediction error: {exc}", "danger")
        return redirect(url_for("index"))

    # ── Fetch recommendations ──────────────────────────────────────────────
    recommendation = get_recommendation(prediction["class_name"])

    # ── Weather Risk Analysis ──────────────────────────────────────────────
    lat_str = request.form.get("lat")
    lng_str = request.form.get("lng")
    weather_info = {"available": False}
    
    if lat_str and lng_str:
        try:
            weather_info = get_weather_risk(float(lat_str), float(lng_str))
        except ValueError:
            pass
            
    # ── Save Radar Data if Coordinates Provided ────────────────────────────
    severity = recommendation.get("severity", "medium")
    
    if lat_str and lng_str and not prediction.get("is_demo", False): # Don't log demo predictions
        try:
            with sqlite3.connect(RADAR_DB) as conn:
                c = conn.cursor()
                c.execute('''
                    INSERT INTO radar_points (lat, lng, disease_name, severity) 
                    VALUES (?, ?, ?, ?)
                ''', (float(lat_str), float(lng_str), prediction["display_name"], severity))
                conn.commit()
        except Exception as e:
            print(f"[WARN] Failed to save radar data: {e}")

    # ── Build result context ───────────────────────────────────────────────
    conf_level = get_confidence_level(prediction["confidence"])
    sev_color  = get_severity_color(recommendation.get("severity", "medium"))

    result = {
        "image_url"      : url_for("static", filename=f"uploads/{filename}"),
        "class_name"     : prediction["class_name"],
        "display_name"   : prediction["display_name"],
        "confidence"     : prediction["confidence"],
        "confidence_level": conf_level,
        "is_healthy"     : prediction["is_healthy"],
        "is_demo"        : prediction.get("is_demo", False),
        "heatmap_url"    : prediction.get("heatmap_url"),
        "description"    : recommendation.get("description", ""),
        "symptoms"       : recommendation.get("symptoms", ""),
        "treatment"      : recommendation.get("treatment", []),
        "prevention"     : recommendation.get("prevention", []),
        "severity"       : recommendation.get("severity", "medium"),
        "severity_color" : sev_color,
        "pesticides"     : recommendation.get("pesticides", []),
        "estimated_yield_loss_pct": recommendation.get("estimated_yield_loss_pct", ""),
        "estimated_loss_inr": recommendation.get("estimated_loss_inr", ""),
        "treatment_cost_inr": recommendation.get("treatment_cost_inr", ""),
        "weather": weather_info,
        "timestamp"      : datetime.now().strftime("%d %b %Y, %I:%M %p"),
    }

    # ── Save to session history ────────────────────────────────────────────
    if "history" not in session:
        session["history"] = []

    history_entry = {
        "id"          : unique_id,
        "image_url"   : result["image_url"],
        "display_name": result["display_name"],
        "class_name"  : result["class_name"],
        "confidence"  : result["confidence"],
        "severity"    : result["severity"],
        "heatmap_url" : result.get("heatmap_url"),
        "timestamp"   : result["timestamp"],
    }
    session["history"] = ([history_entry] + session["history"])[:10]
    session.modified = True

    return render_template("result.html", result=result)


@app.route("/history")
def history():
    """Show the last 10 predictions made in this session."""
    history_list = session.get("history", [])
    return render_template("history.html", history=history_list)


@app.route("/clear")
def clear_history():
    """Clear prediction history from session."""
    session.pop("history", None)
    flash("Prediction history cleared.", "info")
    return redirect(url_for("history"))


@app.route("/history/view/<entry_id>")
def view_history_entry(entry_id):
    """Reconstruct and show result page for a specific history entry."""
    history_list = session.get("history", [])
    entry = next((item for item in history_list if item.get("id") == entry_id), None)
    
    if not entry:
        flash("History entry not found.", "warning")
        return redirect(url_for("history"))
    
    # Reconstruct result object
    # The history entry already has some fields. We need to re-fetch recommendations.
    recommendation = get_recommendation(entry["class_name"])
    
    # Helper values
    from utils.predict import _get_display, _is_healthy
    conf_level = get_confidence_level(entry["confidence"])
    sev_color  = get_severity_color(recommendation.get("severity", "medium"))
    
    result = {
        "image_url"      : entry["image_url"],
        "class_name"     : entry["class_name"],
        "display_name"   : entry["display_name"],
        "confidence"     : entry["confidence"],
        "confidence_level": conf_level,
        "is_healthy"     : _is_healthy(entry["class_name"]),
        "is_demo"        : False, # Assume real if it's in history (at least for now)
        "heatmap_url"    : entry.get("heatmap_url"),
        "description"    : recommendation.get("description", ""),
        "symptoms"       : recommendation.get("symptoms", ""),
        "treatment"      : recommendation.get("treatment", []),
        "prevention"     : recommendation.get("prevention", []),
        "severity"       : recommendation.get("severity", "medium"),
        "severity_color" : sev_color,
        "pesticides"     : recommendation.get("pesticides", []),
        "estimated_yield_loss_pct": recommendation.get("estimated_yield_loss_pct", ""),
        "estimated_loss_inr": recommendation.get("estimated_loss_inr", ""),
        "treatment_cost_inr": recommendation.get("treatment_cost_inr", ""),
        "weather": {"available": False}, # History implies past context; keep it simple
        "timestamp"      : entry["timestamp"],
    }
    
    return render_template("result.html", result=result)


@app.route("/about")
def about():
    """Simple about/instructions page."""
    return render_template("about.html")


@app.route("/radar")
def radar():
    """Disease Outbreak Radar Map."""
    return render_template("radar.html")


@app.route("/api/radar_data")
def api_radar_data():
    """Return radar points as JSON."""
    try:
        with sqlite3.connect(RADAR_DB) as conn:
            conn.row_factory = sqlite3.Row
            c = conn.cursor()
            # Get last 500 reports
            c.execute("SELECT lat, lng, disease_name, severity, timestamp FROM radar_points ORDER BY id DESC LIMIT 500")
            rows = c.fetchall()
            
            # Format nicely for the frontend
            data = [dict(row) for row in rows]
            return jsonify(data)
    except Exception as e:
        print(f"[ERROR] Radar query failed: {e}")
        return jsonify([])


@app.route("/api/tts", methods=["POST"])
def api_tts():
    """
    Generate Text-to-Speech audio from the provided text and language.
    Expects JSON: {"text": "Hello World", "lang": "en"}
    Returns JSON: {"audio_url": "/static/uploads/tts_abc123.mp3"}
    """
    try:
        data = request.get_json()
        if not data or "text" not in data:
            return jsonify({"error": "Missing 'text' in request"}), 400
        
        text = data["text"].strip()
        lang = data.get("lang", "en")  # Default to English
        
        if not text:
            return jsonify({"error": "Text is empty"}), 400

        from gtts import gTTS
        tts = gTTS(text=text, lang=lang)
        
        audio_filename = f"tts_{uuid.uuid4().hex[:10]}.mp3"
        # We save directly to static/uploads instead of app.config (which isn't set)
        upload_dir = os.path.join(app.root_path, "static", "uploads")
        os.makedirs(upload_dir, exist_ok=True)
        audio_path = os.path.join(upload_dir, audio_filename)
        
        tts.save(audio_path)
        
        return jsonify({
            "audio_url": url_for("static", filename=f"uploads/{audio_filename}")
        })
    except Exception as exc:
        print(f"[ERROR] TTS failed: {exc}")
        return jsonify({"error": str(exc)}), 500


@app.route("/api/predict", methods=["POST"])
def api_predict():
    """
    JSON API endpoint for programmatic access.
    Accepts multipart/form-data with 'file' field.
    Returns JSON with prediction and recommendation.
    """
    if "file" not in request.files:
        return jsonify({"error": "No file provided"}), 400

    file = request.files["file"]
    if file.filename == "" or not allowed_file(file.filename):
        return jsonify({"error": "Invalid file"}), 400

    ext       = file.filename.rsplit(".", 1)[1].lower()
    unique_id = uuid.uuid4().hex[:10]
    filename  = f"api_{unique_id}.{ext}"
    save_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
    file.save(save_path)

    try:
        prediction     = predict_disease(save_path)
        recommendation = get_recommendation(prediction["class_name"])
        return jsonify({
            "class_name"  : prediction["class_name"],
            "display_name": prediction["display_name"],
            "confidence"  : prediction["confidence"],
            "is_healthy"  : prediction["is_healthy"],
            "is_demo"     : prediction.get("is_demo", False),
            "heatmap_url" : prediction.get("heatmap_url"),
            "recommendation": {
                "description": recommendation.get("description", ""),
                "treatment"  : recommendation.get("treatment", []),
                "prevention" : recommendation.get("prevention", []),
                "severity"   : recommendation.get("severity", ""),
                "pesticides" : recommendation.get("pesticides", []),
                "estimated_yield_loss_pct": recommendation.get("estimated_yield_loss_pct", ""),
                "estimated_loss_inr": recommendation.get("estimated_loss_inr", ""),
                "treatment_cost_inr": recommendation.get("treatment_cost_inr", ""),
            }
        })
    except Exception as exc:
        return jsonify({"error": str(exc)}), 500


# ─────────────────────────────────────────────────────────────────────────────
# Error handlers
# ─────────────────────────────────────────────────────────────────────────────

@app.errorhandler(413)
def file_too_large(e):
    flash("File too large. Maximum upload size is 16 MB.", "danger")
    return redirect(url_for("index"))


@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404


# ─────────────────────────────────────────────────────────────────────────────
# Entry point
# ─────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    import sys
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    print("\n" + "=" * 60)
    print("  AI Crop Disease Prediction System")
    print("=" * 60)
    print("  URL : http://127.0.0.1:5000")
    print("  Mode: Development (debug=True)")
    print("  Stop: Ctrl + C")
    print("=" * 60 + "\n")
    app.run(debug=True, host="0.0.0.0", port=5000)

