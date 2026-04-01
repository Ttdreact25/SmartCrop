#!/usr/bin/env python
"""
Advanced training script for plant leaf disease detection.

Based on plant-disease-identifier-v3 notebook architecture:
- Uses CNN with Conv2D layers, MaxPooling2D, Dropout, and Dense layers
- Supports 38+ plant disease classes
- Saves model in both H5 (Keras) and PKL (sklearn wrapper) formats

Usage:
    python train_leaf_model_advanced.py

Requirements:
    - PlantVillage dataset organized in train/valid directories
    - TensorFlow/Keras
    - numpy, pandas, pillow
"""

import os
import sys
import numpy as np
from pathlib import Path

# Add parent directory to path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE_DIR)

# Try to import TensorFlow and optionally scipy
try:
    import tensorflow as tf
    from tensorflow import keras
    from tensorflow.keras.models import Sequential
    from tensorflow.keras.layers import (
        Conv2D, MaxPooling2D, Dense, Dropout, Flatten, 
        AveragePooling2D, BatchNormalization, Activation
    )
    from tensorflow.keras.preprocessing.image import ImageDataGenerator
    KERAS_AVAILABLE = True
except ImportError as e:
    print(f"Error: TensorFlow not installed: {e}")
    print("Install with: pip install tensorflow")
    KERAS_AVAILABLE = False

# some TensorFlow ops may hint at scipy; warn if unavailable
try:
    import scipy
except ImportError:
    scipy = None
    if KERAS_AVAILABLE:
        print("⚠️ scipy not installed. Install with `pip install scipy` if you encounter related errors.")

import joblib

# Configuration
IMG_WIDTH, IMG_HEIGHT = 256, 256
INPUT_SHAPE = (IMG_WIDTH, IMG_HEIGHT, 3)
BATCH_SIZE = 64
EPOCHS = 20

TRAIN_DIR = os.path.join(BASE_DIR, 'data', 'Training')
VALID_DIR = os.path.join(BASE_DIR, 'data', 'Validation')
SAVE_DIR = os.path.join(BASE_DIR, 'saved_models')
MODEL_H5_PATH = os.path.join(SAVE_DIR, 'leaf_model.h5')
MODEL_PKL_PATH = os.path.join(SAVE_DIR, 'leaf_model.pkl')


def build_cnn_model(num_classes):
    """Build CNN model based on plant-disease-identifier notebook.
    
    Architecture:
    - 3 Conv2D blocks with MaxPooling
    - Flatten and Dense layers
    - Dropout for regularization
    """
    model = Sequential([
        # Block 1
        Conv2D(16, (5, 5), input_shape=INPUT_SHAPE, activation='relu', padding='same'),
        MaxPooling2D(pool_size=(3, 3)),
        
        # Block 2
        Conv2D(32, (3, 3), activation='relu', padding='same'),
        MaxPooling2D(pool_size=(2, 2)),
        
        # Block 3
        Conv2D(64, (3, 3), activation='relu', padding='same'),
        MaxPooling2D(pool_size=(2, 2)),
        
        # Dense layers
        Flatten(),
        Dense(512, activation='relu'),
        Dropout(0.25),
        Dense(128, activation='relu'),
        Dense(num_classes, activation='softmax')
    ])
    
    model.compile(
        optimizer='adam',
        loss='categorical_crossentropy',
        metrics=['accuracy']
    )
    
    return model


def count_files(directory):
    """Count files in directory recursively."""
    if not os.path.exists(directory):
        return 0
    count = 0
    for root, dirs, files in os.walk(directory):
        count += len([f for f in files if f.lower().endswith(('.png', '.jpg', '.jpeg'))])
    return count


def get_num_classes(directory):
    """Get number of class subdirectories."""
    if not os.path.exists(directory):
        return 0
    return len([d for d in os.listdir(directory) if os.path.isdir(os.path.join(directory, d))])


def train_advanced_model():
    """Train the CNN model on plant disease dataset."""
    if not KERAS_AVAILABLE:
        print("❌ TensorFlow not available. Install with: pip install tensorflow")
        return
    
    print("=" * 70)
    print("🌿 Advanced Plant Disease Detection - CNN Model Training")
    print("=" * 70)
    
    # Check for data
    train_count = count_files(TRAIN_DIR)
    valid_count = count_files(VALID_DIR)
    num_classes = get_num_classes(TRAIN_DIR)
    
    if train_count == 0 or num_classes == 0:
        print("\n❌ Training data not found")
        print(f"   Expected: {TRAIN_DIR}/class_name/image.jpg")
        print(f"   Get dataset from: https://www.kaggle.com/vipoooool/new-plant-diseases-dataset")
        return False
    
    print(f"\n📊 Dataset Information:")
    print(f"   Classes: {num_classes}")
    print(f"   Training samples: {train_count}")
    print(f"   Validation samples: {valid_count}")
    print(f"   Image size: {IMG_WIDTH}x{IMG_HEIGHT}")
    
    # Prepare data generators
    print("\n📁 Setting up data generators...")
    train_gen = ImageDataGenerator(
        rescale=1./255,
        shear_range=0.2,
        zoom_range=0.2,
        horizontal_flip=True,
        fill_mode='nearest'
    )
    
    valid_gen = ImageDataGenerator(rescale=1./255)
    
    train_flow = train_gen.flow_from_directory(
        TRAIN_DIR,
        target_size=(IMG_WIDTH, IMG_HEIGHT),
        batch_size=BATCH_SIZE,
        class_mode='categorical'
    )
    
    valid_flow = valid_gen.flow_from_directory(
        VALID_DIR,
        target_size=(IMG_WIDTH, IMG_HEIGHT),
        batch_size=BATCH_SIZE,
        class_mode='categorical'
    )
    
    class_mapping = train_flow.class_indices
    class_names = {v: k for k, v in class_mapping.items()}
    print(f"✅ Data generators created")
    print(f"   Classes: {list(class_names.values())}")
    
    # Build model
    print("\n🧠 Building CNN model...")
    model = build_cnn_model(num_classes)
    print("✅ Model built")
    print(model.summary())
    
    # Train model
    print("\n📚 Training model...")
    history = model.fit(
        train_flow,
        epochs=EPOCHS,
        validation_data=valid_flow,
        callbacks=[
            keras.callbacks.EarlyStopping(
                monitor='val_loss',
                patience=5,
                restore_best_weights=True
            )
        ],
        verbose=1
    )
    
    # Save model
    print("\n💾 Saving model...")
    os.makedirs(SAVE_DIR, exist_ok=True)
    
    # Save Keras model
    model.save(MODEL_H5_PATH)
    print(f"✅ Keras model saved to {MODEL_H5_PATH}")
    
    # Wrap and save for sklearn compatibility
    class KerasWrapper:
        def __init__(self, keras_model, class_names):
            self.keras_model = keras_model
            self.classes_ = np.array(list(class_names.values()))
            self.class_names = list(class_names.values())
        
        def predict(self, features):
            # Handle both batched and single predictions
            if len(features.shape) == 1:
                features = features.reshape(1, -1)
            # Reshape for CNN
            predictions = self.keras_model.predict(features.reshape(-1, IMG_HEIGHT, IMG_WIDTH, 3))
            return self.classes_[np.argmax(predictions, axis=1)]
    
    wrapper = KerasWrapper(model, class_names)
    joblib.dump(wrapper, MODEL_PKL_PATH)
    print(f"✅ Wrapped model saved to {MODEL_PKL_PATH}")
    
    # Training summary
    print("\n" + "=" * 70)
    print("✅ Training Complete!")
    print("=" * 70)
    print(f"Final training accuracy: {history.history['accuracy'][-1]:.4f}")
    print(f"Final validation accuracy: {history.history['val_accuracy'][-1]:.4f}")
    print(f"\nModels saved:")
    print(f"  - {MODEL_H5_PATH} (Keras)")
    print(f"  - {MODEL_PKL_PATH} (sklearn wrapper)")
    print(f"\n🚀 Ready to use with Streamlit app!")
    print("   Run: streamlit run streamlit_app/app.py")
    
    return True


if __name__ == '__main__':
    success = train_advanced_model()
    sys.exit(0 if success else 1)
