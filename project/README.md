# 🌿 CropAI — Advanced Crop Disease Prediction System

A comprehensive, AI-powered web application designed to help farmers and agronomists diagnose crop diseases from leaf images, receive actionable recommendations, and understand the broader agricultural context. Built with Flask, TensorFlow, and premium glassmorphism UI.

## ✨ Novel Features Included

This project goes beyond standard image classification by integrating five advanced features:

1. **💰 Economic Yield Loss & ROI Calculator**
   - Provides estimated percentage yield loss and potential financial impact in INR (₹) per acre.
   - Compares potential loss against estimated treatment costs to highlight the ROI of immediate action.

2. **🎙️ "Kisan-Vani" Regional Language Voice Assistant**
   - Accessibility feature that reads out the disease diagnosis, severity, and treatment steps.
   - Powered by `gTTS` (Google Text-to-Speech) with support for English and Hindi (हिंदी).

3. **🌤️ Weather-Driven Proactive Risk Analysis**
   - Captures user geolocation locally and fetches real-time temperature and humidity via the free Open-Meteo API.
   - Generates proactive warnings (e.g., warning about Blight risk if humidity is >80%).

4. **🗺️ Real-Time Disease Outbreak Radar**
   - A live interactive map (powered by Leaflet.js) tracking recent disease detections.
   - Geo-tags predictions (saved to a local SQLite database `radar.db`) to help visualize regional epidemic trends.

5. **🧠 Explainable AI (XAI) via Grad-CAM Heatmaps**
   - Increases trust in the AI by providing visual proof of the diagnosis.
   - Generates a Gradient-weighted Class Activation Map indicating the exact regions of the leaf the neural network focused on.
   - Includes a seamless UI toggle to overlay the heatmap on the original image.

## 🚀 Quick Start Guide

### 1. Prerequisites
- Python 3.8+
- Create a virtual environment (recommended)

### 2. Installation
Install all required dependencies:
```bash
pip install -r requirements.txt
```

### 3. Model Training (If needed)
If you don't have the `model/plant_disease_model.h5` file, the app will run in **Demo Mode** (simulating predictions). To run the actual AI model, you need to train it first.
*Ensure your dataset is in the `dataset/` directory.*
```bash
python model/train_model.py
```

### 4. Running the Application
Start the Flask development server:
```bash
python app.py
```
Then, open your web browser and navigate to: `http://127.0.0.1:5000`

## 📁 Project Structure

* `app.py`: Main Flask application router.
* `model/`: Contains training scripts and the trained `.h5` model.
* `utils/`: Core utilities (`predict.py`, `preprocess.py`, `recommendations.py`, `xai.py`).
* `templates/`: HTML files (Jinja2 templates) including `index.html`, `result.html`, `radar.html`, etc.
* `static/`: CSS styles, JavaScript, and user uploads (`/uploads`).
* `radar.db`: Auto-generated SQLite database storing geo-tagged predictions for the map.

## 🤝 Note for Academic Evaluation
This project is designed to be a complete B.Tech Final Year submission, demonstrating not only core Deep Learning concepts but also practical software engineering (REST APIs, SQLite databases, external API integration, dynamic UI/UX, and AI Explainability).
