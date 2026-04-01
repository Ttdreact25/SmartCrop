#!/usr/bin/env python
"""
Standalone script to train a plant leaf detection model.

This script:
1. Loads leaf images from data/leaf_dataset/ (organized as leaf_dataset/class_name/image.jpg)
2. Builds and trains a CNN classifier
3. Saves the model to saved_models/leaf_model.pkl (Keras format) for use in the Streamlit app

Usage:
    python train_leaf_model.py

Requirements:
    - Images in data/leaf_dataset/ organized by class subdirectories
    - TensorFlow/Keras installed
    - scikit-learn, numpy, pandas, pillow installed
"""

import os
import sys
import numpy as np
import pandas as pd
import joblib
from PIL import Image
from pathlib import Path

# Add parent directory to path for imports
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE_DIR)

try:
    from tensorflow.keras import layers, models, callbacks
    import tensorflow as tf
    KERAS_AVAILABLE = True
except ImportError:
    KERAS_AVAILABLE = False
    print("⚠️  TensorFlow not available - will attempt to create a simple sklearn model instead")

# Configuration
IMAGE_SIZE = (128, 128)
# Updated to use the Training directory with Early_Blight, Healthy, Late_Blight classes
DATA_DIR = os.path.join(BASE_DIR, 'data', 'Training')
SAVE_DIR = os.path.join(BASE_DIR, 'saved_models')
MODEL_PATH = os.path.join(SAVE_DIR, 'leaf_model.pkl')


def load_data():
    """Load images from leaf_dataset directory and return as arrays with labels."""
    if not os.path.exists(DATA_DIR):
        print(f"❌ Dataset directory not found at {DATA_DIR}")
        print("   Create the folder and organize images like: data/leaf_dataset/class_name/image.jpg")
        return None, None, None

    classes = [d for d in os.listdir(DATA_DIR) if os.path.isdir(os.path.join(DATA_DIR, d))]
    if not classes:
        print(f"❌ No class subdirectories found in {DATA_DIR}")
        return None, None, None

    print(f"✓ Found {len(classes)} classes: {classes}")

    # Collect all image paths and labels
    records = []
    for cls in classes:
        cls_path = os.path.join(DATA_DIR, cls)
        img_count = 0
        for fname in os.listdir(cls_path):
            if fname.lower().endswith(('.jpg', '.jpeg', '.png')):
                records.append((os.path.join(cls_path, fname), cls))
                img_count += 1
        print(f"  {cls}: {img_count} images")

    if not records:
        print("❌ No images found in dataset")
        return None, None, None

    return records, classes, len(records)


def preprocess_image(image_path):
    """Load and preprocess a single image."""
    try:
        img = Image.open(image_path).convert('RGB')
        img = img.resize(IMAGE_SIZE)
        arr = np.asarray(img, dtype=np.float32) / 255.0
        return arr
    except Exception as e:
        print(f"⚠️  Error processing {image_path}: {e}")
        return None


def prepare_data(records):
    """Prepare image arrays and labels from records."""
    print("\n📊 Preprocessing images...")
    valid_records = []
    images = []

    for path, label in records:
        img_arr = preprocess_image(path)
        if img_arr is not None:
            images.append(img_arr)
            valid_records.append((path, label))

    if not images:
        print("❌ No valid images could be loaded")
        return None, None

    data = np.stack(images)
    labels_df = pd.DataFrame(valid_records, columns=['path', 'label'])
    labels_encoded = pd.get_dummies(labels_df['label']).values

    print(f"✓ Loaded {len(data)} valid images")
    print(f"  Data shape: {data.shape}, Labels shape: {labels_encoded.shape}")

    return data, labels_encoded


def build_and_train_model(data, labels, classes):
    """Build and train a CNN model if TensorFlow is available."""
    if not KERAS_AVAILABLE:
        print("⚠️  TensorFlow not available - skipping model training")
        return None

    print("\n🧠 Building CNN model...")

    model = models.Sequential([
        layers.Input(shape=(*IMAGE_SIZE, 3)),
        layers.Conv2D(32, 3, activation='relu', padding='same'),
        layers.MaxPooling2D(2),
        layers.Conv2D(64, 3, activation='relu', padding='same'),
        layers.MaxPooling2D(2),
        layers.Conv2D(128, 3, activation='relu', padding='same'),
        layers.MaxPooling2D(2),
        layers.Flatten(),
        layers.Dense(256, activation='relu'),
        layers.layers.Dropout(0.5),
        layers.Dense(len(classes), activation='softmax')
    ])

    model.compile(
        loss='categorical_crossentropy',
        optimizer='adam',
        metrics=['accuracy']
    )

    print(f"✓ Model compiled")
    print("  Model summary:")
    model.summary()

    print("\n📚 Training model...")
    history = model.fit(
        data, labels,
        epochs=20,
        batch_size=16,
        validation_split=0.2,
        callbacks=[
            callbacks.EarlyStopping(monitor='val_loss', patience=5, restore_best_weights=True)
        ],
        verbose=1
    )

    print(f"\n✓ Training complete!")
    print(f"  Final accuracy: {history.history['accuracy'][-1]:.4f}")
    print(f"  Final validation accuracy: {history.history['val_accuracy'][-1]:.4f}")

    return model


def save_model(model, classes):
    """Save the trained model."""
    os.makedirs(SAVE_DIR, exist_ok=True)

    if model is not None and KERAS_AVAILABLE:
        # Save as Keras model (recommended)
        keras_path = os.path.join(SAVE_DIR, 'leaf_model')
        model.save(keras_path)
        print(f"\n💾 Keras model saved to {keras_path}")

        # Also wrap in joblib for compatibility with leaf_detector.py
        class KerasWrapper:
            """Wrapper to make Keras model compatible with leaf_detector.predict_leaf"""
            def __init__(self, keras_model, class_list):
                self.keras_model = keras_model
                self.classes_ = np.array(class_list)  # Ensure numpy array

            def predict(self, features):
                predictions = self.keras_model.predict(features)
                class_indices = np.argmax(predictions, axis=1)
                return self.classes_[class_indices]

        wrapped_model = KerasWrapper(model, classes)
        joblib.dump(wrapped_model, MODEL_PATH)
        print(f"✓ Wrapped model saved to {MODEL_PATH}")
    else:
        print("⚠️  No model to save (TensorFlow not available)")
        print(f"   Install TensorFlow to train: pip install tensorflow")


def create_demo_model():
    """Create a simple demo model without real data."""
    print("\n⚠️  No dataset found - creating a simple demo classifier...")

    from sklearn.ensemble import RandomForestClassifier

    # Create dummy data for demo (5 samples per class)
    demo_classes = ['leaf_healthy', 'leaf_diseased', 'leaf_unknown']
    n_samples = 15
    n_features = 128 * 128 * 3  # Flattened 128x128 RGB image

    X_demo = np.random.rand(n_samples, n_features)
    y_demo = np.repeat(demo_classes, 5)

    print(f"✓ Created {n_samples} demo samples with {len(demo_classes)} classes")

    # Train simple classifier
    print("📚 Training demo RandomForest classifier...")
    clf = RandomForestClassifier(n_estimators=10, random_state=42, n_jobs=-1)
    clf.fit(X_demo, y_demo)
    # sklearn automatically sets classes_ but ensure it's a numpy array
    clf.classes_ = np.array(clf.classes_)

    print("✓ Demo model trained")

    # Save it
    os.makedirs(SAVE_DIR, exist_ok=True)
    joblib.dump(clf, MODEL_PATH)
    print(f"💾 Demo model saved to {MODEL_PATH}")

    return True


def main():
    """Main training pipeline."""
    print("=" * 60)
    print("🌿 Plant Leaf Detection Model Training")
    print("=" * 60)

    # Check for data
    records, classes, count = load_data()

    if records is None:
        print("\n📝 No actual dataset found. Creating a demo model for testing...")
        create_demo_model()
        print("\n✅ Demo model created successfully!")
        print(f"📂 Location: {MODEL_PATH}")
        print("\nTo train with real data:")
        print(f"1. Create dataset folder structure: {DATA_DIR}/class_name/image.jpg")
        print("2. Run this script again")
        return

    # Prepare data
    data, labels = prepare_data(records)
    if data is None:
        return

    # Train model
    model = build_and_train_model(data, labels, classes)

    # Save
    save_model(model, classes)

    print("\n" + "=" * 60)
    print("✅ Model training complete!")
    print(f"📂 Model saved to: {MODEL_PATH}")
    print("=" * 60)
    print("\n🚀 You can now use the Streamlit app:")
    print("   streamlit run streamlit_app/app.py")


if __name__ == '__main__':
    main()
