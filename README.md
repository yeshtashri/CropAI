
🌿 AI Crop Disease Prediction and Management System
A Flask-based web application that uses a MobileNetV2 CNN trained on the PlantVillage dataset to predict crop diseases from leaf images and provide detailed treatment recommendations.

📁 Project Structure
project/
├── app.py                        ← Main Flask application
├── requirements.txt              ← Python dependencies
│
├── model/
│   ├── __init__.py
│   ├── disease_classes.py        ← Class label mapping (16 classes)
│   └── train_model.py            ← Model training script (MobileNetV2)
│
├── utils/
│   ├── __init__.py
│   ├── preprocess.py             ← Image preprocessing pipeline
│   ├── predict.py                ← Model inference (with demo mode)
│   └── recommendations.py       ← Disease → treatment mapping
│
├── templates/
│   ├── index.html                ← Upload dashboard
│   ├── result.html               ← Prediction results page
│   ├── history.html              ← Prediction history
│   ├── about.html                ← About page
│   └── 404.html                  ← Error page
│
└── static/
    ├── css/style.css             ← Custom dark-theme styles
    ├── js/app.js                 ← Drag-drop, preview, animations
    └── uploads/                  ← Uploaded images (auto-created)
🚀 Getting Started
Step 1 — Install Python dependencies
pip install -r requirements.txt
No GPU? Open requirements.txt and replace tensorflow with tensorflow-cpu.

Step 2 — Train the AI model
The PlantVillage dataset must exist at:

c:/Users/DELL/Downloads/archive/PlantVillage/
Run the training script from inside the project/ folder:

cd c:/Users/DELL/Downloads/archive/project
python model/train_model.py
Training takes approximately:

CPU: 25–45 minutes
GPU (CUDA): 5–10 minutes
This creates model/plant_disease_model.h5.

⚡ Demo Mode: If you skip training, the app still runs in demo mode and shows simulated predictions so you can test the full UI immediately.

Step 3 — Run the Flask app
python app.py
Open your browser and go to: http://127.0.0.1:5000

🌿 Supported Disease Classes (16)
#	Crop	Condition
1	Bell Pepper	Bacterial Spot
2	Bell Pepper	Healthy
3	Potato	Early Blight
4	Potato	Late Blight
5	Potato	Healthy
6	Tomato	Bacterial Spot
7	Tomato	Early Blight
8	Tomato	Late Blight
9	Tomato	Leaf Mold
10	Tomato	Septoria Leaf Spot
11	Tomato	Spider Mites
12	Tomato	Target Spot
13	Tomato	Yellow Leaf Curl Virus
14	Tomato	Mosaic Virus
15	Tomato	Healthy
16	Mixed (PlantVillage sub-folder)	—
🔧 Technology Stack
Layer	Technology
Language	Python 3.x
Backend	Flask 3.0
AI Model	TensorFlow / Keras — MobileNetV2 (Transfer Learning)
Image Processing	OpenCV
Frontend	HTML5, Bootstrap 5, Vanilla CSS/JS
Dataset	PlantVillage
📡 JSON API
The app also exposes a REST endpoint for programmatic access:

curl -X POST http://127.0.0.1:5000/api/predict \
  -F "file=@leaf.jpg"
Response:

{
  "class_name": "Tomato_Early_blight",
  "display_name": "Tomato – Early Blight",
  "confidence": 91.34,
  "is_healthy": false,
  "is_demo": false,
  "recommendation": {
    "description": "...",
    "treatment": ["..."],
    "prevention": ["..."],
    "severity": "medium",
    "pesticides": ["..."]
  }
}
❓ Troubleshooting
Problem	Fix
ModuleNotFoundError: tensorflow	pip install tensorflow or pip install tensorflow-cpu
ModuleNotFoundError: cv2	pip install opencv-python-headless
Model not found warning	Run python model/train_model.py or use demo mode
Port 5000 already in use	Change port in app.py: app.run(port=5001)
📝 Academic Reference
This project uses Transfer Learning on the PlantVillage Dataset: Hughes, D.P. & Salathé, M. (2015). An open access repository of images of healthy and diseased plants. arXiv:1511.08060

B.Tech Final Year Project — AI-Driven Crop Disease Prediction and Management System

