# 📦 Smart Crop Recommendation System - Module Documentation

This document provides detailed information about each module and process in the Smart Crop Recommendation System.

---

## 📋 Table of Contents

1. [System Architecture Overview](#system-architecture-overview)
2. [Authentication Module](#1-authentication-module-authpy)
3. [Data Loader Module](#2-data-loader-module-data_loaderpy)
4. [Predictor Module](#3-predictor-module-predictorpy)
5. [Weather API Module](#4-weather-api-module-weather_apipy)
6. [Location Mapper Module](#5-location-mapper-module-location_mapperpy)
7. [Leaf Detector Module](#6-leaf-detector-module-leaf_detectorpy)
8. [Translator Module](#7-translator-module-translatorpy)
9. [Main Application](#8-main-application-streamlit_appapppy)
10. [Farmer Dashboard](#9-farmer-dashboard-integrated-feature)
11. [Data Files](#10-data-files)
12. [Machine Learning Models](#11-machine-learning-models)
13. [Process Flow](#process-flow)

---

## System Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                    Streamlit Web Interface                        │
│                     (app.py)                                     │
└─────────────────────────────────────────────────────────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
        ▼                     ▼                     ▼
┌───────────────┐    ┌───────────────┐    ┌───────────────┐
│ Authentication│    │   Prediction  │    │    Weather    │
│    Module     │    │    Module     │    │     API       │
│   (auth.py)   │    │ (predictor.py)│    │(weather_api.py)│
└───────────────┘    └───────────────┘    └───────────────┘
        │                     │                     │
        ▼                     ▼                     ▼
┌───────────────┐    ┌───────────────┐    ┌───────────────┐
│  User Data    │    │  ML Models    │    │  Weather Data │
│  (.users/)    │    │(saved_models/)│    │   (External)  │
└───────────────┘    └───────────────┘    └───────────────┘
```

---

## 1. Authentication Module (`auth.py`)

### Purpose
Handles user registration, login, and session management with secure password hashing.

### Location
```
smart_crop/auth.py
```

### Key Functions

#### `register_user(username, email, password, confirm_password)`
Registers a new user with validation.

**Parameters:**
- `username` (str): Username (minimum 3 characters)
- `email` (str): Valid email address
- `password` (str): Password with uppercase, lowercase, digit, and special character
- `confirm_password` (str): Password confirmation

**Returns:**
- `tuple`: (success: bool, message: str)

**Validation Rules:**
- Username must be at least 3 characters
- Email must be valid format
- Password must be at least 8 characters
- Password must contain: uppercase, lowercase, digit, special character
- Passwords must match

#### `login_user(username, password)`
Authenticates a user against stored credentials.

**Parameters:**
- `username` (str): Username
- `password` (str): Password

**Returns:**
- `tuple`: (success: bool, message: str)

### Security Features
- ✅ Password hashing using bcrypt
- ✅ Strong password validation
- ✅ Duplicate username/email prevention
- ✅ Secure session management

### Data Storage
- User data stored in `.users/users.json`
- Passwords are hashed (never stored in plain text)

### Dependencies
```python
import json
import os
import bcrypt
import re
```

---

## 2. Data Loader Module (`data_loader.py`)

### Purpose
Handles loading and preprocessing of all data files used in the application.

### Location
```
smart_crop/data_loader.py
```

### Key Functions

#### `load_crop_data(path='data/Crop_Recommendation.csv')`
Loads the crop recommendation dataset.

**Parameters:**
- `path` (str): Path to the CSV file

**Returns:**
- `pd.DataFrame`: DataFrame containing crop data with columns:
  - N (Nitrogen)
  - P (Phosphorus)
  - K (Potassium)
  - temperature
  - humidity
  - ph
  - rainfall
  - label (crop name)

#### `load_location_data(path='data/Indian_cities_coordinates.csv')`
Loads location coordinates for Indian cities.

**Parameters:**
- `path` (str): Path to the CSV file

**Returns:**
- `pd.DataFrame`: DataFrame with city coordinates

#### `load_fertilizer_data(path='data/Fertilizer Prediction.csv')`
Loads fertilizer prediction dataset.

**Parameters:**
- `path` (str): Path to the CSV file

**Returns:**
- `pd.DataFrame`: DataFrame with fertilizer data

### Data Files Used
- `data/Crop_Recommendation.csv` - 2200+ crop records
- `data/Indian_cities_coordinates.csv` - City coordinates
- `data/Fertilizer Prediction.csv` - Fertilizer data
- `data/crops_duration.csv` - Crop growing durations

### Dependencies
```python
import pandas as pd
import os
```

---

## 3. Predictor Module (`predictor.py`)

### Purpose
Core machine learning module that handles crop prediction, fertilizer recommendation, and model management.

### Location
```
smart_crop/predictor.py
```

### Key Functions

#### `load_model(model_path='saved_models/crop_model.pkl')`
Loads the trained crop recommendation model.

**Parameters:**
- `model_path` (str): Path to the pickle file

**Returns:**
- `sklearn.ensemble.RandomForestClassifier`: Trained model

#### `predict_crop(input_data, model)`
Predicts the best crop based on input parameters.

**Parameters:**
- `input_data` (dict): Dictionary containing:
  - `N`: Nitrogen content (0-140 ppm)
  - `P`: Phosphorus content (5-145 ppm)
  - `K`: Potassium content (5-205 ppm)
  - `temperature`: Temperature in Celsius
  - `humidity`: Humidity percentage
  - `ph`: Soil pH level
  - `rainfall`: Rainfall in mm
- `model`: Trained ML model

**Returns:**
- `tuple`: (predicted_crop: str, probabilities: dict)

#### `load_fertilizer_resources()`
Loads fertilizer recommendation model and encoders.

**Returns:**
- `tuple`: (model, soil_encoder, crop_encoder, scaler)

#### `predict_fertilizer(soil_type, crop_name, nitrogen, phosphorus, potassium, temperature, humidity, moisture)`
Recommends fertilizer based on soil and crop conditions.

**Parameters:**
- `soil_type` (str): Type of soil
- `crop_name` (str): Name of the crop
- `nitrogen` (float): Nitrogen content
- `phosphorus` (float): Phosphorus content
- `potassium` (float): Potassium content
- `temperature` (float): Temperature
- `humidity` (float): Humidity
- `moisture` (float): Soil moisture

**Returns:**
- `str`: Recommended fertilizer name

#### `load_crop_duration_new_data()`
Loads crop duration information.

**Returns:**
- `dict`: Dictionary mapping crop names to duration info

### Model Details
- **Algorithm**: Random Forest Classifier
- **Training Data**: 2200+ records
- **Features**: 7 input parameters
- **Output Classes**: 22 crop types
- **Accuracy**: ~99.3%

### Dependencies
```python
import pickle
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder, StandardScaler
```

---

## 4. Weather API Module (`weather_api.py`)

### Purpose
Integrates with external weather API to fetch real-time weather data for location-based recommendations.

### Location
```
smart_crop/weather_api.py
```

### Key Functions

#### `get_weather_data(city_name, api_key)`
Fetches current weather data for a given city.

**Parameters:**
- `city_name` (str): Name of the city
- `api_key` (str): Weather API key

**Returns:**
- `dict`: Weather data containing:
  - `temperature`: Current temperature (°C)
  - `humidity`: Humidity percentage
  - `pressure`: Atmospheric pressure (hPa)
  - `wind_speed`: Wind speed (m/s)
  - `description`: Weather description
  - `feels_like`: Feels like temperature

### API Integration
- Uses OpenWeatherMap API
- Requires API key stored in `.env` file
- Handles API rate limits and errors gracefully

### Environment Variables
```bash
WEATHER_API_KEY=your_api_key_here
```

### Dependencies
```python
import requests
import os
from dotenv import load_dotenv
```

---

## 5. Location Mapper Module (`location_mapper.py`)

### Purpose
Manages geographic location data and provides state-city mapping for location-based recommendations.

### Location
```
smart_crop/location_mapper.py
```

### Key Functions

#### `get_state_city_mapping(location_df)`
Creates a mapping of states to their cities.

**Parameters:**
- `location_df` (pd.DataFrame): Location DataFrame

**Returns:**
- `dict`: Dictionary mapping states to list of cities

#### `get_coordinates(city_name, location_df)`
Retrieves latitude and longitude for a city.

**Parameters:**
- `city_name` (str): Name of the city
- `location_df` (pd.DataFrame): Location DataFrame

**Returns:**
- `tuple`: (latitude: float, longitude: float)

### Coverage
- All major Indian states
- 500+ cities and towns
- GPS coordinates for mapping

### Dependencies
```python
import pandas as pd
```

---

## 6. Leaf Detector Module (`leaf_detector.py`)

### Purpose
Provides plant disease detection by analyzing leaf images using machine learning.

### Location
```
smart_crop/leaf_detector.py
```

### Key Functions

#### `load_leaf_model(model_path='saved_models/leaf_model.pkl')`
Loads the trained leaf detection model.

**Parameters:**
- `model_path` (str): Path to the model file

**Returns:**
- `model`: Trained classification model

#### `predict_disease(image_path, model)`
Predicts plant disease from a leaf image.

**Parameters:**
- `image_path` (str): Path to the image file
- `model`: Trained model

**Returns:**
- `dict`: Prediction results containing:
  - `disease`: Disease name
  - `confidence`: Confidence score
  - `healthy`: Boolean indicating if plant is healthy

### Supported Diseases
- Healthy
- Late Blight
- Early Blight
- And more (depending on training data)

### Training Data
- Located in `data/Training/` and `data/Validation/`
- Organized by disease category
- JPEG/PNG image formats

### Model Training
To train a new model:
```bash
python train_leaf_model_advanced.py
```

### Dependencies
```python
import pickle
import numpy as np
from PIL import Image
import tensorflow as tf  # Optional
import cv2  # Optional
```

---

## 7. Translator Module (`translator.py`)

### Purpose
Provides multi-language support for recommendations and UI elements.

### Location
```
smart_crop/translator.py
```

### Key Functions

#### `translate_text(text, target_language)`
Translates text to the target language.

**Parameters:**
- `text` (str): Text to translate
- `target_language` (str): Target language code

**Returns:**
- `str`: Translated text

### Supported Languages
- English (en)
- Hindi (hi)
- Tamil (ta)
- Telugu (te)
- Kannada (kn)
- Malayalam (ml)
- Bengali (bn)
- Marathi (mr)
- Gujarati (gu)
- Punjabi (pa)

### Language Names Mapping
```python
LANGUAGE_NAMES = {
    'en': 'English',
    'hi': 'हिंदी',
    'ta': 'தமிழ்',
    'te': 'తెలుగు',
    'kn': 'ಕನ್ನಡ',
    'ml': 'മലയാളം',
    'bn': 'বাংলা',
    'mr': 'मराठी',
    'gu': 'ગુજરાતી',
    'pa': 'ਪੰਜਾਬੀ'
}
```

### Dependencies
```python
from googletrans import Translator  # or similar translation library
```

---

## 8. Main Application (`streamlit_app/app.py`)

### Purpose
The main Streamlit application that provides the web interface and orchestrates all modules.

### Location
```
streamlit_app/app.py
```

### Application Modes

#### 1. Farmer Dashboard
- **Dashboard Overview**: Key metrics (farm area, active crops, expected yield, profit)
- **Farm Analytics**: Historical yield data with predictions and recommendations
- **Crop Calendar**: Season activities, upcoming tasks with priorities
- **Profit Estimation**: Revenue, costs, and profit breakdown with charts
- **Weather History Trends**: Monthly weather patterns and forecasts
- **Crop Health Monitoring**: Health status of different crop fields
- **Quick Actions**: Generate reports, add tasks, check irrigation, contact experts

#### 2. Crop Recommendation
- Input soil parameters (N, P, K, pH, rainfall)
- Select location (state/city)
- Fetch real-time weather
- Get AI-powered crop recommendations
- View top-5 alternatives with probabilities

#### 2. Fertilizer Recommendation
- Input soil type and crop name
- Enter soil parameters
- Get fertilizer recommendations
- View application guidelines

#### 3. Crop Demand Prediction
- Analyze market trends
- Predict crop demand
- View demand forecasts

#### 4. Plant Leaf Detection
- Upload leaf image
- Detect plant diseases
- Get treatment recommendations

#### 5. About Page
- View algorithm information
- See model performance metrics
- Explore interactive visualizations
- Review technology stack

### Session State Management
```python
st.session_state.logged_in      # User login status
st.session_state.username       # Current username
st.session_state.auth_mode      # 'login' or 'register'
```

### UI Features
- Modern dark theme with green accents
- Responsive layout
- Interactive charts (Plotly)
- Real-time updates
- Custom CSS styling

### Dependencies
```python
import streamlit as st
import pandas as pd
import plotly.express as px
import sys
import os
```

---

## 9. Farmer Dashboard (Integrated Feature)

### Purpose
Comprehensive farming analytics and management center that provides farmers with actionable insights, yield predictions, profit estimation, and weather trends.

### Location
Integrated within `streamlit_app/app.py` (Farmer Dashboard mode)

### Key Features

#### 📊 Dashboard Overview
- **Total Farm Area**: Displays total acreage with year-over-year changes
- **Active Crops**: Number of crops currently being cultivated
- **Expected Yield**: Predicted harvest quantity with comparison to previous year
- **Estimated Profit**: Projected financial returns with growth indicators

#### 📈 Farm Analytics & Yield Prediction
- **Historical Yield Chart**: Line graph showing yield trends over multiple years
- **Revenue Tracking**: Financial performance visualization
- **Prediction Factors**: Temperature, rainfall, soil quality, crop health indicators
- **Confidence Score**: ML-based prediction confidence percentage
- **Recommendations**: Actionable farming advice based on analytics

#### 📅 Crop Calendar
- **Season Activities**: Current season farming tasks with status tracking
- **Upcoming Tasks**: Prioritized task list with deadlines
- **Status Indicators**: ✅ Completed, 🔄 In Progress, ⏳ Pending, 📅 Scheduled
- **Priority Levels**: 🔴 High, 🟡 Medium, 🟢 Low

#### 💰 Profit Estimation
- **Profit Breakdown Chart**: Visual comparison of revenue, costs, and profit
- **Financial Summary**: Detailed table with total revenue, costs, and net profit
- **Profit Margin**: Percentage calculation of profitability
- **Cost Breakdown**: Itemized expenses (seeds, fertilizers, irrigation, labor, equipment)

#### 🌦️ Weather History Trends
- **Monthly Weather Chart**: Multi-line graph showing temperature, rainfall, and humidity trends
- **Current Weather Display**: Real-time weather conditions
- **Weather Alerts**: Notifications about upcoming weather events
- **Seasonal Forecast**: Long-term weather predictions for planning

#### 🌱 Crop Health Monitoring
- **Health Progress Bars**: Visual representation of crop health percentages
- **Field Status**: Individual health tracking for different crop fields
- **Last Checked**: Timestamp of last health assessment

#### ⚡ Quick Actions
- **Generate Report**: Create comprehensive farm reports
- **Add Task**: Quick task creation for farm management
- **Check Irrigation**: Monitor irrigation system status
- **Contact Expert**: Access to agricultural expert consultation

### Data Visualization
- **Interactive Charts**: Plotly-based dynamic visualizations
- **Real-time Updates**: Live data refresh capabilities
- **Responsive Design**: Mobile-friendly dashboard layout

### Dependencies
```python
import streamlit as st
import pandas as pd
import plotly.express as px
```

---

## 10. Data Files

### Crop Recommendation Dataset
**File**: `data/Crop_Recommendation.csv`

**Columns:**
| Column | Description | Range |
|--------|-------------|-------|
| N | Nitrogen content | 0-140 ppm |
| P | Phosphorus content | 5-145 ppm |
| K | Potassium content | 5-205 ppm |
| temperature | Temperature | -5 to 50°C |
| humidity | Humidity | 0-100% |
| ph | Soil pH | 3.5-10.0 |
| rainfall | Rainfall | 20-300 mm |
| label | Crop name | 22 types |

### Location Coordinates
**File**: `data/Indian_cities_coordinates.csv`

**Columns:**
- city: City name
- state: State name
- latitude: GPS latitude
- longitude: GPS longitude

### Fertilizer Prediction
**File**: `data/Fertilizer Prediction.csv`

**Columns:**
- Temparature: Temperature
- Humidity: Humidity
- Moisture: Soil moisture
- Soil_Type: Type of soil
- Crop_Type: Type of crop
- Nitrogen: Nitrogen content
- Potassium: Potassium content
- Phosphorous: Phosphorus content
- Fertilizer: Recommended fertilizer

### Crop Duration
**Files**: 
- `data/crops_duration.csv`
- `data/crops_duration_new.csv`

**Columns:**
- Crop: Crop name
- Duration: Growing duration in days

### Leaf Disease Images
**Directories:**
- `data/Training/` - Training images
- `data/Validation/` - Validation images

**Categories:**
- Healthy
- Late_Blight
- Early_Blight

---

## 10. Machine Learning Models

### Crop Recommendation Model
**File**: `saved_models/crop_model.pkl`

**Details:**
- Algorithm: Random Forest Classifier
- Training Data: 2200+ records
- Features: 7 parameters
- Output: 22 crop classes
- Accuracy: 99.3%
- Validation: 80-20 train-test split

### Fertilizer Recommendation Model
**File**: `saved_models/fertilizer_model.pkl`

**Details:**
- Algorithm: Decision Tree Classifier
- Training Data: 500+ records
- Features: 8 parameters
- Output: 7 fertilizer types
- Accuracy: 95%+

### Leaf Detection Model
**File**: `saved_models/leaf_model.pkl`

**Details:**
- Algorithm: CNN or Classical Classifier
- Training Data: Leaf images
- Features: Image pixels
- Output: Disease classification
- Accuracy: 92%+

---

## Process Flow

### 1. User Authentication Flow
```
User Access → Login Page → Enter Credentials → Validate → Session Created
                    ↓
              Registration → Validate Input → Hash Password → Store User → Login
```

### 2. Crop Recommendation Flow
```
User Input → Location Selection → Weather API Call → Soil Parameters
    ↓
Feature Scaling → ML Model Prediction → Probability Calculation
    ↓
Top-5 Recommendations → Visualization → Display Results
```

### 3. Fertilizer Recommendation Flow
```
User Input → Soil Type + Crop Selection → NPK Values
    ↓
Feature Encoding → Model Prediction → Fertilizer Recommendation
    ↓
Application Guidelines → Display Results
```

### 4. Leaf Detection Flow
```
Image Upload → Image Preprocessing → Feature Extraction
    ↓
Model Prediction → Disease Classification → Confidence Score
    ↓
Treatment Recommendations → Display Results
```

### 5. Weather Integration Flow
```
City Selection → API Request → Weather Data Fetch
    ↓
Data Parsing → Temperature, Humidity, Pressure, Wind
    ↓
Integration with Crop Model → Enhanced Recommendations
```

---

## 🔧 Configuration Files

### Environment Variables (`.env`)
```bash
WEATHER_API_KEY=your_api_key_here
```

### Requirements (`requirements.txt`)
```
streamlit
pandas
numpy
scikit-learn
plotly
bcrypt
python-dotenv
requests
googletrans==4.0.0-rc1
```

### Python Version (`.python-version`)
```
3.8
```

---

## 🚀 Running the Application

### Start the Application
```bash
streamlit run streamlit_app/app.py
```

### Create Demo User
```bash
python setup_demo_user.py
```

### Train Leaf Detection Model
```bash
python train_leaf_model_advanced.py
```

### Train Fertilizer Model
```bash
python train_fertilizer_model.py
```

---

## 📊 Module Dependencies Graph

```
app.py
├── auth.py
│   └── .users/users.json
├── data_loader.py
│   ├── data/Crop_Recommendation.csv
│   ├── data/Indian_cities_coordinates.csv
│   └── data/Fertilizer Prediction.csv
├── predictor.py
│   ├── saved_models/crop_model.pkl
│   └── saved_models/fertilizer_model.pkl
├── weather_api.py
│   └── .env (WEATHER_API_KEY)
├── location_mapper.py
│   └── data/Indian_cities_coordinates.csv
├── leaf_detector.py
│   └── saved_models/leaf_model.pkl
├── translator.py
└── Farmer Dashboard (Integrated)
    ├── Farm Analytics
    ├── Crop Calendar
    ├── Profit Estimation
    └── Weather Trends
```

---

## 🎯 Key Features Summary

| Module | Purpose | Key Function |
|--------|---------|--------------|
| Authentication | User management | `login_user()`, `register_user()` |
| Data Loader | Data preprocessing | `load_crop_data()`, `load_location_data()` |
| Predictor | ML predictions | `predict_crop()`, `predict_fertilizer()` |
| Weather API | Real-time weather | `get_weather_data()` |
| Location Mapper | Geographic data | `get_state_city_mapping()` |
| Leaf Detector | Disease detection | `predict_disease()` |
| Translator | Multi-language | `translate_text()` |
| Main App | UI orchestration | Streamlit interface |
| Farmer Dashboard | Farm analytics | Yield prediction, profit estimation |

---

## 📝 Notes

- All modules are located in the `smart_crop/` directory
- The main application entry point is `streamlit_app/app.py`
- Machine learning models are stored in `saved_models/`
- Training data is organized in `data/` directory
- User data is securely stored in `.users/` directory

---

**Last Updated**: 2024
**Version**: 1.0.0
**Maintainer**: Smart Crop Recommendation System Team
