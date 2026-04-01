"""
Script to train the fertilizer model and save the required pickle files.
This reproduces the code from the Fertilizer Recommendation System.ipynb
"""

import numpy as np
import pandas as pd
import pickle
import os
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier

# Load the fertilizer dataset
print("Loading fertilizer dataset...")
fertilizer = pd.read_csv("data/Fertilizer Prediction.csv")
print(f"Dataset shape: {fertilizer.shape}")
print(f"Columns: {fertilizer.columns.tolist()}")

# Encoding the target column
fert_dict = {
    'Urea': 1,
    'DAP': 2,
    '14-35-14': 3,
    '28-28': 4,
    '17-17-17': 5,
    '20-20': 6,
    '10-26-26': 7,
}

# Replacing each fertilizer name with its corresponding number from fert_dict
fertilizer['fert_no'] = fertilizer['Fertilizer Name'].map(fert_dict)
print(f"\nFertilizer distribution:\n{fertilizer['fert_no'].value_counts()}")

# Drop the target column with name and keep the target column with numbers
fertilizer.drop('Fertilizer Name', axis=1, inplace=True)

# Convert the categorical columns to numerical columns using labelencoder
soil_encoder = LabelEncoder()
crop_encoder = LabelEncoder()

fertilizer["Soil Type"] = soil_encoder.fit_transform(fertilizer['Soil Type'])
fertilizer["Crop Type"] = crop_encoder.fit_transform(fertilizer['Crop Type'])

print(f"\nSoil Type classes: {soil_encoder.classes_}")
print(f"Crop Type classes: {crop_encoder.classes_}")

# Splitting
x = fertilizer.drop('fert_no', axis=1)
y = fertilizer['fert_no']

print(f"\nFeatures shape: {x.shape}")
print(f"Target shape: {y.shape}")

# Split the dataset into training and testing sets
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)

print(f"Training set size: {x_train.shape[0]}")
print(f"Testing set size: {x_test.shape[0]}")

# Scaling
sc = StandardScaler()
x_train = sc.fit_transform(x_train)
x_test = sc.transform(x_test)

# Training the model
print("\nTraining Decision Tree model...")
model = DecisionTreeClassifier()
model.fit(x_train, y_train)

# Evaluate the model
train_accuracy = model.score(x_train, y_train)
test_accuracy = model.score(x_test, y_test)
print(f"Training accuracy: {train_accuracy*100:.2f}%")
print(f"Testing accuracy: {test_accuracy*100:.2f}%")

# Ensure saved_models directory exists
SAVE_DIR = "saved_models"
os.makedirs(SAVE_DIR, exist_ok=True)

# Save the model and encoders
print(f"\nSaving models to {SAVE_DIR}...")

with open(os.path.join(SAVE_DIR, "fertilizer_model.pkl"), "wb") as f:
    pickle.dump(model, f)
print("  - fertilizer_model.pkl saved")

with open(os.path.join(SAVE_DIR, "soil_encoder.pkl"), "wb") as f:
    pickle.dump(soil_encoder, f)
print("  - soil_encoder.pkl saved")

with open(os.path.join(SAVE_DIR, "crop_encoder.pkl"), "wb") as f:
    pickle.dump(crop_encoder, f)
print("  - crop_encoder.pkl saved")

with open(os.path.join(SAVE_DIR, "fertilizer_scaler.pkl"), "wb") as f:
    pickle.dump(sc, f)
print("  - fertilizer_scaler.pkl saved")

print("\n✅ All fertilizer model files have been generated successfully!")
print(f"\nFiles in saved_models directory:")
for f in os.listdir(SAVE_DIR):
    print(f"  - {f}")

