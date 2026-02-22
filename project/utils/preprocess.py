"""
preprocess.py
-------------
Image preprocessing for the crop disease prediction system.

IMPORTANT: The trained model (built in train_model.py) has a Rescaling(1/255)
layer baked into the graph, so this module should output pixel values in the
ORIGINAL [0, 255] uint8 range — NOT normalised.

Pipeline:
    1. Load image with OpenCV (BGR)
    2. Convert BGR -> RGB
    3. Resize to 224 x 224 (MobileNetV2 input size)
    4. Expand dims to add batch dimension -> (1, 224, 224, 3)
    5. Cast to float32 — normalization is handled inside the model graph
"""

import cv2
import numpy as np

# ─────────────────────────────────────────────────────────────
IMG_SIZE  = 224
IMG_SHAPE = (IMG_SIZE, IMG_SIZE, 3)


def preprocess_image(image_path: str) -> np.ndarray:
    """
    Load and prepare an image for model inference.

    Parameters
    ----------
    image_path : str
        Path to a JPG / PNG image file.

    Returns
    -------
    np.ndarray
        Shape (1, 224, 224, 3), dtype float32, values in [0, 255].
        The model's internal Rescaling layer will normalise to [0, 1].

    Raises
    ------
    FileNotFoundError
        If the image cannot be read from the given path.
    """
    img_bgr = cv2.imread(image_path)
    if img_bgr is None:
        raise FileNotFoundError(
            f"Could not load image: {image_path}. "
            "Ensure the file exists and is a valid JPG/PNG."
        )

    img_rgb     = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
    img_resized = cv2.resize(img_rgb, (IMG_SIZE, IMG_SIZE),
                             interpolation=cv2.INTER_AREA)

    # Cast to float32 — values remain in [0, 255], model normalises internally
    img_tensor = np.expand_dims(img_resized.astype(np.float32), axis=0)
    return img_tensor
