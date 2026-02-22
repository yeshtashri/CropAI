"""
train_model.py
--------------
Trains a MobileNetV2-based CNN on the PlantVillage dataset.
Compatible with TensorFlow 2.20 / Keras 3.

Usage (run from the project/ folder):
    python model/train_model.py

Dataset location:
    c:/Users/DELL/Downloads/archive/PlantVillage/
"""

import os
import sys

# ─────────────────────────────────────────────────────────────────────────────
# Paths
# ─────────────────────────────────────────────────────────────────────────────
PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATASET_DIR = os.path.join(
    os.path.dirname(PROJECT_DIR),   # archive/
    "PlantVillage",
    "PlantVillage"
)
MODEL_SAVE_PATH = os.path.join(PROJECT_DIR, "model", "plant_disease_model.h5")
CLASS_MAP_PATH  = os.path.join(PROJECT_DIR, "model", "class_indices.txt")

# ─────────────────────────────────────────────────────────────────────────────
# Hyperparameters
# ─────────────────────────────────────────────────────────────────────────────
IMG_SIZE         = 224
BATCH_SIZE       = 32
EPOCHS_PHASE1    = 10    # head-only training
EPOCHS_PHASE2    = 10    # fine-tuning (increased for accuracy)
LEARNING_RATE    = 1e-4
VAL_SPLIT        = 0.20
SEED             = 42


def main():
    import tensorflow as tf

    print("=" * 60)
    print("  AI Crop Disease Prediction -- Model Training")
    print("=" * 60)
    print(f"  TensorFlow : {tf.__version__}")
    print(f"  Dataset    : {DATASET_DIR}")
    print(f"  Save path  : {MODEL_SAVE_PATH}")
    print(f"  Image size : {IMG_SIZE}x{IMG_SIZE}")
    print(f"  Batch size : {BATCH_SIZE}")
    print("=" * 60)

    # ── Validate dataset ───────────────────────────────────────────────────
    if not os.path.isdir(DATASET_DIR):
        print(f"\n[ERROR] Dataset not found: {DATASET_DIR}")
        sys.exit(1)

    # ─────────────────────────────────────────────────────────────────────
    # 1. Load datasets using the Keras 3-compatible API
    # ─────────────────────────────────────────────────────────────────────
    print("\n[INFO] Loading training dataset...")
    train_ds = tf.keras.utils.image_dataset_from_directory(
        DATASET_DIR,
        validation_split=VAL_SPLIT,
        subset="training",
        seed=SEED,
        image_size=(IMG_SIZE, IMG_SIZE),
        batch_size=BATCH_SIZE,
        label_mode="categorical",
        shuffle=True,
    )

    print("\n[INFO] Loading validation dataset...")
    val_ds = tf.keras.utils.image_dataset_from_directory(
        DATASET_DIR,
        validation_split=VAL_SPLIT,
        subset="validation",
        seed=SEED,
        image_size=(IMG_SIZE, IMG_SIZE),
        batch_size=BATCH_SIZE,
        label_mode="categorical",
        shuffle=False,
    )

    class_names = train_ds.class_names
    num_classes = len(class_names)

    print(f"\n[INFO] Found {num_classes} classes:")
    for idx, name in enumerate(class_names):
        print(f"       {idx:2d}  {name}")

    # ── Save class mapping ─────────────────────────────────────────────────
    os.makedirs(os.path.dirname(CLASS_MAP_PATH), exist_ok=True)
    with open(CLASS_MAP_PATH, "w") as f:
        for idx, name in enumerate(class_names):
            f.write(f"{idx},{name}\n")
    print(f"\n[INFO] Class mapping saved -> {CLASS_MAP_PATH}")

    # ─────────────────────────────────────────────────────────────────────
    # 2. Data augmentation layer (built into the model graph)
    # ─────────────────────────────────────────────────────────────────────
    data_augmentation = tf.keras.Sequential([
        tf.keras.layers.RandomFlip("horizontal"),
        tf.keras.layers.RandomRotation(0.15),
        tf.keras.layers.RandomZoom(0.15),
        tf.keras.layers.RandomTranslation(0.1, 0.1),
    ], name="data_augmentation")

    # ─────────────────────────────────────────────────────────────────────
    # 3. Normalise pixel values [0,255] -> [0,1] via Rescaling layer
    # ─────────────────────────────────────────────────────────────────────
    normalization = tf.keras.layers.Rescaling(1.0 / 255)

    # ─────────────────────────────────────────────────────────────────────
    # 4. Build MobileNetV2 model
    # ─────────────────────────────────────────────────────────────────────
    print("\n[INFO] Building MobileNetV2 model...")
    base_model = tf.keras.applications.MobileNetV2(
        input_shape=(IMG_SIZE, IMG_SIZE, 3),
        include_top=False,
        weights="imagenet",
    )
    base_model.trainable = False   # Freeze base

    # Full model using Functional API
    inputs  = tf.keras.Input(shape=(IMG_SIZE, IMG_SIZE, 3))
    x       = data_augmentation(inputs)          # augment (only in training)
    x       = normalization(x)                   # normalize to [0,1]
    x       = base_model(x, training=False)      # frozen feature extractor
    x       = tf.keras.layers.GlobalAveragePooling2D()(x)
    x       = tf.keras.layers.Dense(256, activation="relu")(x)
    x       = tf.keras.layers.Dropout(0.5)(x)
    outputs = tf.keras.layers.Dense(num_classes, activation="softmax")(x)

    model = tf.keras.Model(inputs, outputs)

    model.compile(
        optimizer=tf.keras.optimizers.Adam(learning_rate=LEARNING_RATE),
        loss="categorical_crossentropy",
        metrics=["accuracy"],
    )

    model.summary()

    # ─────────────────────────────────────────────────────────────────────
    # 5. Performance tuning — prefetch only (no cache to avoid RAM overflow)
    # ─────────────────────────────────────────────────────────────────────
    AUTOTUNE = tf.data.AUTOTUNE
    train_ds = train_ds.prefetch(buffer_size=AUTOTUNE)
    val_ds   = val_ds.prefetch(buffer_size=AUTOTUNE)


    # ─────────────────────────────────────────────────────────────────────
    # 6. Callbacks
    # ─────────────────────────────────────────────────────────────────────
    os.makedirs(os.path.dirname(MODEL_SAVE_PATH), exist_ok=True)

    callbacks = [
        tf.keras.callbacks.ModelCheckpoint(
            filepath=MODEL_SAVE_PATH,
            monitor="val_accuracy",
            save_best_only=True,
            verbose=1,
        ),
        tf.keras.callbacks.EarlyStopping(
            monitor="val_accuracy",
            patience=4,
            restore_best_weights=True,
            verbose=1,
        ),
        tf.keras.callbacks.ReduceLROnPlateau(
            monitor="val_loss",
            factor=0.5,
            patience=2,
            min_lr=1e-7,
            verbose=1,
        ),
    ]

    # ─────────────────────────────────────────────────────────────────────
    # 7. Phase 1 — Train classification head (base frozen)
    # ─────────────────────────────────────────────────────────────────────
    print(f"\n[Phase 1] Training classification head for up to {EPOCHS_PHASE1} epochs...")
    history = model.fit(
        train_ds,
        epochs=EPOCHS_PHASE1,
        validation_data=val_ds,
        callbacks=callbacks,
    )

    # ─────────────────────────────────────────────────────────────────────
    # 8. Phase 2 — Fine-tune top 30 layers of MobileNetV2
    # ─────────────────────────────────────────────────────────────────────
    print(f"\n[Phase 2] Fine-tuning top 30 layers of MobileNetV2 for up to {EPOCHS_PHASE2} epochs...")
    base_model.trainable = True
    for layer in base_model.layers[:-30]:
        layer.trainable = False

    model.compile(
        optimizer=tf.keras.optimizers.Adam(learning_rate=LEARNING_RATE / 10),
        loss="categorical_crossentropy",
        metrics=["accuracy"],
    )

    history_ft = model.fit(
        train_ds,
        epochs=EPOCHS_PHASE2,
        validation_data=val_ds,
        callbacks=callbacks,
    )

    # ─────────────────────────────────────────────────────────────────────
    # 9. Save final model
    # ─────────────────────────────────────────────────────────────────────
    model.save(MODEL_SAVE_PATH)
    print(f"\nModel saved -> {MODEL_SAVE_PATH}")

    # ─────────────────────────────────────────────────────────────────────
    # 10. Evaluate
    # ─────────────────────────────────────────────────────────────────────
    print("\n[INFO] Final evaluation on validation set...")
    loss, acc = model.evaluate(val_ds, verbose=0)
    print(f"  Validation Loss     : {loss:.4f}")
    print(f"  Validation Accuracy : {acc * 100:.2f}%")
    print("\nTraining complete! Run the app: python app.py")


if __name__ == "__main__":
    main()
