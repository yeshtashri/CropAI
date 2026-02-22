"""
predict.py
----------
Model loading (singleton) and disease prediction.

The model's class order is read from model/class_indices.txt generated
during training (matches image_dataset_from_directory alphabetical order).
Falls back to demo mode if model or class map are missing.
"""

import os
import random
import numpy as np
import gc

from utils.preprocess import preprocess_image

# ─────────────────────────────────────────────────────────────
# Paths
# ─────────────────────────────────────────────────────────────
_BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH     = os.path.join(_BASE, "model", "plant_disease_model.h5")
CLASS_MAP_PATH = os.path.join(_BASE, "model", "class_indices.txt")

# ─────────────────────────────────────────────────────────────
# Singleton state
# ─────────────────────────────────────────────────────────────
_model      = None
_class_list = []   # ordered list of class name strings
_demo_mode  = False


# ── Pretty display names ──────────────────────────────────────
_DISPLAY = {
    "Pepper__bell___Bacterial_spot"               : "Pepper Bell - Bacterial Spot",
    "Pepper__bell___healthy"                       : "Pepper Bell - Healthy",
    "Potato___Early_blight"                        : "Potato - Early Blight",
    "Potato___Late_blight"                         : "Potato - Late Blight",
    "Potato___healthy"                             : "Potato - Healthy",
    "Tomato_Bacterial_spot"                        : "Tomato - Bacterial Spot",
    "Tomato_Early_blight"                          : "Tomato - Early Blight",
    "Tomato_Late_blight"                           : "Tomato - Late Blight",
    "Tomato_Leaf_Mold"                             : "Tomato - Leaf Mold",
    "Tomato_Septoria_leaf_spot"                    : "Tomato - Septoria Leaf Spot",
    "Tomato_Spider_mites_Two_spotted_spider_mite"  : "Tomato - Spider Mites",
    "Tomato__Target_Spot"                          : "Tomato - Target Spot",
    "Tomato__Tomato_YellowLeaf__Curl_Virus"        : "Tomato - Yellow Leaf Curl Virus",
    "Tomato__Tomato_mosaic_virus"                  : "Tomato - Mosaic Virus",
    "Tomato_healthy"                               : "Tomato - Healthy",
    "PlantVillage"                                 : "Healthy (PlantVillage)",
}

_HEALTHY = {
    "Pepper__bell___healthy", "Potato___healthy",
    "Tomato_healthy", "PlantVillage",
}


def _get_display(class_name):
    return _DISPLAY.get(class_name, class_name.replace("_", " ").replace("  ", " "))


def _is_healthy(class_name):
    return class_name in _HEALTHY


def _load_class_list():
    """Load class list from class_indices.txt saved during training."""
    global _class_list
    if os.path.exists(CLASS_MAP_PATH):
        with open(CLASS_MAP_PATH, "r") as f:
            lines = [l.strip() for l in f if l.strip()]
        _class_list = [line.split(",", 1)[1] for line in lines]
        print(f"[INFO] Loaded {len(_class_list)} classes from {CLASS_MAP_PATH}")
    else:
        # Fallback — alphabetical order of dataset folders
        from model.disease_classes import CLASS_NAMES
        _class_list = CLASS_NAMES
        print("[WARN] class_indices.txt not found, using default CLASS_NAMES list.")


def load_model_once():
    """Load the Keras model from disk exactly once (singleton)."""
    global _model, _demo_mode

    if _model is not None:
        return _model

    if not os.path.exists(MODEL_PATH):
        print(
            f"[WARN] Model not found: {MODEL_PATH}\n"
            "       Running in DEMO MODE. Train with: python model/train_model.py"
        )
        _demo_mode = True
        return None

    try:
        import tensorflow as tf
        print(f"[INFO] Loading model from {MODEL_PATH} ...")
        # Optimization: load with compile=False to save memory/time
        _model = tf.keras.models.load_model(MODEL_PATH, compile=False)
        _load_class_list()
        print("[INFO] Model ready.")
        return _model
    except Exception as exc:
        print(f"[ERROR] Could not load model: {exc}\n       Falling back to demo mode.")
        _demo_mode = True
        return None


def _demo_prediction():
    demo_classes = [
        "Tomato_Early_blight",
        "Tomato_Late_blight",
        "Potato___Early_blight",
        "Tomato__Tomato_YellowLeaf__Curl_Virus",
        "Tomato_healthy",
        "Pepper__bell___Bacterial_spot",
    ]
    chosen     = random.choice(demo_classes)
    confidence = round(random.uniform(72.0, 98.5), 2)
    return {
        "class_name"  : chosen,
        "display_name": _get_display(chosen),
        "confidence"  : confidence,
        "is_healthy"  : _is_healthy(chosen),
        "is_demo"     : True,
    }


def predict_disease(image_path: str) -> dict:
    """
    Full prediction pipeline.

    Returns dict with:
      class_name, display_name, confidence (%), is_healthy, is_demo
    """
    model = load_model_once()

    if _demo_mode or model is None:
        return _demo_prediction()

    try:
        img_tensor  = preprocess_image(image_path)           # (1,224,224,3)
        
        # Optimization: Use __call__ instead of predict() for lower memory overhead
        predictions = model(img_tensor, training=False)
        predictions = predictions.numpy() if hasattr(predictions, 'numpy') else predictions
        
        pred_index  = int(np.argmax(predictions[0]))
        confidence  = float(np.max(predictions[0])) * 100

        if not _class_list:
            _load_class_list()

        if pred_index >= len(_class_list):
            raise IndexError(
                f"Predicted index {pred_index} >= class list length {len(_class_list)}"
            )

        class_name = _class_list[pred_index]

        # Manual cleanup to help Render's OOM issues
        gc.collect()

        return {
            "class_name"  : class_name,
            "display_name": _get_display(class_name),
            "confidence"  : round(confidence, 2),
            "is_healthy"  : _is_healthy(class_name),
            "is_demo"     : False,
        }

    except Exception as exc:
        print(f"[ERROR] Prediction failed: {exc}")
        gc.collect()
        result = _demo_prediction()
        result["error"] = str(exc)
        return result
