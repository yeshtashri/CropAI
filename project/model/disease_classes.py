"""
disease_classes.py
------------------
Maps integer class indices (as produced by Keras ImageDataGenerator with
alphabetical class ordering) to human-readable disease label strings.

The 16 classes come from the PlantVillage dataset subset stored under
c:/Users/DELL/Downloads/archive/PlantVillage/
"""

# =============================================================================
# Class index → disease name mapping
# (alphabetical order — matches Keras flow_from_directory default)
# =============================================================================
CLASS_NAMES = [
    "Pepper__bell___Bacterial_spot",
    "Pepper__bell___healthy",
    "Potato___Early_blight",
    "Potato___Late_blight",
    "Potato___healthy",
    "Tomato_Bacterial_spot",
    "Tomato_Early_blight",
    "Tomato_Late_blight",
    "Tomato_Leaf_Mold",
    "Tomato_Septoria_leaf_spot",
    "Tomato_Spider_mites_Two_spotted_spider_mite",
    "Tomato__Target_Spot",
    "Tomato__Tomato_YellowLeaf__Curl_Virus",
    "Tomato__Tomato_mosaic_virus",
    "Tomato_healthy",
    # Inner PlantVillage sub-folder (mixed) - treated as extra healthy bucket
    "PlantVillage_mixed",
]

# Pretty display names (shown in UI)
DISPLAY_NAMES = {
    "Pepper__bell___Bacterial_spot"                  : "Pepper Bell – Bacterial Spot",
    "Pepper__bell___healthy"                          : "Pepper Bell – Healthy",
    "Potato___Early_blight"                           : "Potato – Early Blight",
    "Potato___Late_blight"                            : "Potato – Late Blight",
    "Potato___healthy"                                : "Potato – Healthy",
    "Tomato_Bacterial_spot"                           : "Tomato – Bacterial Spot",
    "Tomato_Early_blight"                             : "Tomato – Early Blight",
    "Tomato_Late_blight"                              : "Tomato – Late Blight",
    "Tomato_Leaf_Mold"                                : "Tomato – Leaf Mold",
    "Tomato_Septoria_leaf_spot"                       : "Tomato – Septoria Leaf Spot",
    "Tomato_Spider_mites_Two_spotted_spider_mite"     : "Tomato – Spider Mites",
    "Tomato__Target_Spot"                             : "Tomato – Target Spot",
    "Tomato__Tomato_YellowLeaf__Curl_Virus"           : "Tomato – Yellow Leaf Curl Virus",
    "Tomato__Tomato_mosaic_virus"                     : "Tomato – Mosaic Virus",
    "Tomato_healthy"                                  : "Tomato – Healthy",
    "PlantVillage_mixed"                              : "Healthy (Mixed)",
}

# Is this class a "healthy" class?
HEALTHY_CLASSES = {
    "Pepper__bell___healthy",
    "Potato___healthy",
    "Tomato_healthy",
    "PlantVillage_mixed",
}

def get_display_name(class_name: str) -> str:
    """Return a human-readable label for a raw class name."""
    return DISPLAY_NAMES.get(class_name, class_name.replace("_", " "))

def is_healthy(class_name: str) -> bool:
    """Return True if the class represents a healthy plant."""
    return class_name in HEALTHY_CLASSES
