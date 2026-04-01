"""
Plant leaf disease detection module.

Supports both:
1. API-based detection (PlantNet - free API)
2. Local Keras CNN models and sklearn classifiers

Usage:
    - API mode: Uses PlantNet API for free plant identification
    - Local mode: Uses trained local model (requires training first)

Get free API key from: https://my.plantnet.org/
"""

import os
import joblib
import requests
import io
from PIL import Image
import numpy as np

# Path setup
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
LEAF_MODEL_H5_PATH = os.path.join(BASE_DIR, "saved_models", "leaf_model.h5")
LEAF_MODEL_PKL_PATH = os.path.join(BASE_DIR, "saved_models", "leaf_model.pkl")

# PlantNet API configuration (FREE)
PLANTNET_API_URL = "https://my-api.plantnet.org/v2/identify/all"
PLANTNET_API_KEY = "2b10Vb3petRgAf2bKSNWax6Lee"  # User needs to get free key from https://my.plantnet.org/

# Try importing TensorFlow
try:
    import tensorflow as tf
    from tensorflow.keras.models import load_model
    TF_AVAILABLE = True
except ImportError:
    TF_AVAILABLE = False


def load_leaf_model():
    """Load plant disease detection model (Keras CNN or sklearn).
    
    Tries Keras model first (.h5), falls back to sklearn (.pkl).
    Returns None if no model found (will use API instead).
    """
    # Try Keras first
    if os.path.exists(LEAF_MODEL_H5_PATH) and TF_AVAILABLE:
        try:
            model = load_model(LEAF_MODEL_H5_PATH)
            return model
        except Exception as e:
            print(f"Warning: Could not load Keras model: {e}")
    
    # Try sklearn
    if os.path.exists(LEAF_MODEL_PKL_PATH):
        return joblib.load(LEAF_MODEL_PKL_PATH)
    
    # No model found - will use API
    print("⚠️ No local model found. Using PlantNet API for detection.")
    return None


def _preprocess_image(image: Image.Image, size=(256, 256)) -> np.ndarray:
    """Preprocess image to 256x256 normalized array."""
    image = image.convert("RGB")
    image = image.resize(size)
    arr = np.asarray(image, dtype=np.float32) / 255.0
    return arr


def predict_leaf_api(image: Image.Image, api_key: str = None) -> dict:
    """Use PlantNet API for free plant/disease detection.
    
    Args:
        image: PIL Image object
        api_key: PlantNet API key (get free key from https://my.plantnet.org/)
    
    Returns:
        dict with 'disease', 'confidence', 'scientific_name', 'common_name'
    """
    if not api_key or api_key.strip() == "":
        return {
            'disease': 'API_KEY_REQUIRED',
            'confidence': 0.0,
            'scientific_name': '',
            'common_name': '',
            'description': 'Please enter your PlantNet API key to use the detection feature.',
            'status': '⚠️ API Key Required',
            'recommendations': [
                'Get a free API key from https://my.plantnet.org/',
                'The free tier allows 500 requests per day',
                'Enter your API key in the input field above'
            ]
        }
    
    # Convert image to bytes
    img_byte_arr = io.BytesIO()
    image.save(img_byte_arr, format='JPEG')
    img_byte_arr.seek(0)
    
    # PlantNet API request - using the correct endpoint
    api_url = f"https://my-api.plantnet.org/v2/identify/all?api-key={api_key}"
    files = {'images': ('leaf.jpg', img_byte_arr, 'image/jpeg')}
    data = {
        'project': 'weurope',
        'lang': 'en'
    }
    
    try:
        response = requests.post(api_url, files=files, data=data, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            
            if result.get('results') and len(result['results']) > 0:
                top_result = result['results'][0]
                
                scientific_name = top_result.get('species', {}).get('scientificName', '')
                common_name = ''
                if top_result.get('commonNames'):
                    common_name = top_result['commonNames'][0]
                
                score = top_result.get('score', 0.0)
                
                # Determine disease status based on plant identification
                disease_result = _analyze_plant_health(common_name, scientific_name, score)
                disease_result['confidence'] = score
                disease_result['scientific_name'] = scientific_name
                disease_result['common_name'] = common_name
                
                return disease_result
            else:
                return {
                    'disease': 'UNKNOWN',
                    'confidence': 0.0,
                    'description': 'Could not identify the plant. Try with a clearer image.',
                    'status': '❓ Unknown Plant',
                    'recommendations': [
                        'Take a clearer photo',
                        'Ensure leaf is well-lit',
                        'Include both sides of leaf if possible'
                    ]
                }
        elif response.status_code == 401:
            return {
                'disease': 'INVALID_API_KEY',
                'confidence': 0.0,
                'description': 'Invalid API key. Please check and enter a valid PlantNet API key.',
                'status': '⚠️ Invalid API Key',
                'recommendations': [
                    'Get a new API key from https://my.plantnet.org/',
                    'Make sure to copy the key correctly',
                    'The key should be a long alphanumeric string'
                ]
            }
        elif response.status_code == 403:
            return {
                'disease': 'IP_BLOCKED',
                'confidence': 0.0,
                'description': 'Your IP address is blocked by PlantNet API. This may happen if your IP is not whitelisted.',
                'status': '⚠️ IP Blocked',
                'recommendations': [
                    'Log in to https://my.plantnet.org/ and whitelist your IP in account settings',
                    'Alternatively, use a different network or contact PlantNet support',
                    'Note: This is a PlantNet API restriction, not an app issue'
                ]
            }
        elif response.status_code == 429:
            return {
                'disease': 'RATE_LIMIT',
                'confidence': 0.0,
                'description': 'API rate limit exceeded. Try again later.',
                'status': '⚠️ Rate Limited',
                'recommendations': [
                    'Wait a few minutes before trying again',
                    'The free tier allows 500 requests per day'
                ]
            }
        else:
            return {
                'disease': 'API_ERROR',
                'confidence': 0.0,
                'description': f'API error: {response.status_code} - {response.text[:100]}',
                'status': '⚠️ API Error',
                'recommendations': ['Check your API key', 'Try again later']
            }
            
    except requests.exceptions.ConnectionError:
        return {
            'disease': 'CONNECTION_ERROR',
            'confidence': 0.0,
            'description': 'Could not connect to PlantNet API. Check your internet connection.',
            'status': '❌ Connection Error',
            'recommendations': ['Check internet connection', 'Try again']
        }
    except Exception as e:
        return {
            'disease': 'ERROR',
            'confidence': 0.0,
            'description': f'Error: {str(e)}',
            'status': '❌ Error',
            'recommendations': ['Try again with a different image']
        }


def _analyze_plant_health(common_name: str, scientific_name: str, confidence: float) -> dict:
    """Analyze plant name to determine health status."""
    # Keywords that indicate healthy plants
    healthy_keywords = ['healthy', 'normal', 'healthy plant']
    
    # Check if it's a known healthy plant variety
    name_lower = (common_name + ' ' + scientific_name).lower()
    
    for keyword in healthy_keywords:
        if keyword in name_lower:
            return {
                'disease': 'HEALTHY',
                'description': f'Healthy {common_name or scientific_name}',
                'status': '✅ Healthy Plant',
                'recommendations': [
                    'Continue regular maintenance',
                    'Monitor for early disease signs',
                    'Maintain proper watering schedule',
                    'Ensure adequate sunlight'
                ]
            }
    
    # Plant identified but health unknown - could be diseased
    return {
        'disease': f'PLANT: {common_name or scientific_name}',
        'description': f'Plant identified: {common_name or scientific_name}',
        'status': '📋 Plant Identified',
        'recommendations': [
            'Take a photo of any spots, lesions, or discoloration',
            'Compare with common diseases for this plant type',
            'Consult plant disease databases for specific symptoms',
            'Consider consulting a local agricultural extension'
        ]
    }


def predict_leaf(model, image: Image.Image, use_api: bool = False, api_key: str = None) -> str:
    """Predict disease from leaf image - Simple version.
    
    Uses basic image analysis when no model is available.
    """
    # Use API if requested
    if use_api:
        result = predict_leaf_api(image, api_key)
        return result.get('disease', 'UNKNOWN')
    
    # Try to use local model if it's a Keras model
    if model is not None:
        try:
            # Only try Keras models
            if TF_AVAILABLE and hasattr(model, 'predict') and hasattr(model, 'layers'):
                img_array = _preprocess_image(image, size=(128, 128))
                img_batch = np.expand_dims(img_array, axis=0)
                predictions = model.predict(img_batch, verbose=0)
                class_idx = np.argmax(predictions[0])
                
                if hasattr(model, 'class_names'):
                    return model.class_names[class_idx]
                return _index_to_disease_name(class_idx)
        except Exception as e:
            print(f"Model prediction error: {e}")
    
    # Fallback: Simple color-based analysis
    return _simple_predict(image)


def _simple_predict(image: Image.Image) -> str:
    """Simple prediction based on image color analysis."""
    try:
        # Resize for quick analysis
        img = image.convert('RGB')
        img = img.resize((50, 50))
        arr = np.array(img)
        
        # Calculate average colors
        avg_r = np.mean(arr[:, :, 0])
        avg_g = np.mean(arr[:, :, 1])
        avg_b = np.mean(arr[:, :, 2])
        
        # Simple heuristic based on color
        # Yellow/brown tones suggest disease
        # Green tones suggest healthy
        
        if avg_g > avg_r + 20 and avg_g > avg_b + 20:
            return "Healthy"
        elif avg_r > avg_g + 30 or (avg_r > 100 and avg_g < 80):
            return "Late_Blight"
        else:
            return "Early_Blight"
    except:
        return "Healthy"


def predict_leaf_with_info(model, image: Image.Image, use_api: bool = False, api_key: str = None) -> dict:
    """Predict disease with full information and recommendations.
    
    Args:
        model: Loaded model (can be None if using API)
        image: PIL Image object
        use_api: If True, use PlantNet API instead of local model (default: False)
        api_key: PlantNet API key
    
    Returns:
        Dictionary with disease info and recommendations
    """
    # Use API if requested
    if use_api and api_key:
        return predict_leaf_api(image, api_key)
    
    # Use local model or simple prediction
    disease_name = predict_leaf(model, image, use_api=False)
    return get_disease_info(disease_name)


def _index_to_disease_name(class_idx: int) -> str:
    """Map class index to disease name (PlantVillage dataset)."""
    diseases = {
        0: 'Apple___Apple_scab',
        1: 'Apple___Black_rot',
        2: 'Apple___Cedar_apple_rust',
        3: 'Apple___healthy',
        4: 'Blueberry___healthy',
        5: 'Cherry___Powdery_mildew',
        6: 'Cherry___healthy',
        7: 'Corn___Cercospora_leaf_spot',
        8: 'Corn___Common_rust',
        9: 'Corn___Northern_Leaf_Blight',
        10: 'Corn___healthy',
        11: 'Grape___Black_rot',
        12: 'Grape___Esca',
        13: 'Grape___Leaf_blight',
        14: 'Grape___healthy',
        15: 'Orange___Citrus_greening',
        16: 'Peach___Bacterial_spot',
        17: 'Peach___healthy',
        18: 'Pepper___Bacterial_spot',
        19: 'Pepper___healthy',
        20: 'Potato___Early_blight',
        21: 'Potato___Late_blight',
        22: 'Potato___healthy',
        23: 'Raspberry___healthy',
        24: 'Soybean___healthy',
        25: 'Squash___Powdery_mildew',
        26: 'Strawberry___Leaf_scorch',
        27: 'Strawberry___healthy',
        28: 'Tomato___Bacterial_spot',
        29: 'Tomato___Early_blight',
        30: 'Tomato___Late_blight',
        31: 'Tomato___Leaf_Mold',
        32: 'Tomato___Septoria_leaf_spot',
        33: 'Tomato___Spider_mites',
        34: 'Tomato___Target_Spot',
        35: 'Tomato___Yellow_Leaf_Curl_Virus',
        36: 'Tomato___Tomato_mosaic_virus',
        37: 'Tomato___healthy'
    }
    return diseases.get(class_idx, f'Disease_{class_idx}')


def get_disease_info(disease_name: str) -> dict:
    """Get disease information and treatment recommendations."""
    
    # Your data has these classes: Early_Blight, Healthy, Late_Blight
    treatments = {
        'Early_Blight': {
            'description': 'Early Blight Disease',
            'status': '🟡 Fungal Disease',
            'recommendations': [
                'Remove infected leaves immediately - do not compost them',
                'Apply chlorothalonil or mancozeb fungicide every 7-10 days',
                'Improve air circulation around plants by proper spacing',
                'Water at soil level only, avoid wetting foliage',
                'Mulch around plants to prevent soil splash',
                'Remove plant debris after harvest',
                'Practice crop rotation for 2-3 years'
            ]
        },
        'Late_Blight': {
            'description': 'Late Blight Disease',
            'status': '🔴 Critical Disease',
            'recommendations': [
                'Remove ALL infected parts immediately - destroy do not compost',
                'Apply copper or mancozeb fungicide urgently',
                'Maintain low humidity (below 30%) around plants',
                'Destroy infected plants completely - DO NOT COMPOST',
                'Use 3-year crop rotation with non-solanaceous crops',
                'Plant resistant varieties if available',
                'Monitor nearby plants for early signs'
            ]
        },
        'Healthy': {
            'description': 'Healthy Plant',
            'status': '✅ Healthy',
            'recommendations': [
                'Continue regular maintenance and watering schedule',
                'Monitor for early disease signs weekly',
                'Maintain proper nutrition with balanced fertilizer',
                'Ensure adequate sunlight (6-8 hours daily)',
                'Keep area free of dead plant debris',
                'Avoid overhead watering to prevent fungal growth',
                'Inspect plants regularly for pests'
            ]
        },
        # Also handle lowercase
        'early_blight': {
            'description': 'Early Blight Disease',
            'status': '🟡 Fungal Disease',
            'recommendations': [
                'Remove infected leaves immediately',
                'Apply fungicide regularly',
                'Improve air circulation',
                'Avoid watering on leaves',
                'Use mulch to prevent soil splash',
                'Clean up plant debris',
                'Rotate crops annually'
            ]
        },
        'late_blight': {
            'description': 'Late Blight Disease',
            'status': '🔴 Critical Disease',
            'recommendations': [
                'Remove ALL infected parts immediately',
                'Apply copper fungicide urgently',
                'Destroy infected plants completely',
                'Maintain low humidity',
                'Use resistant varieties',
                'Practice crop rotation',
                'Monitor nearby plants daily'
            ]
        },
        'healthy': {
            'description': 'Healthy Plant',
            'status': '✅ Healthy',
            'recommendations': [
                'Continue regular maintenance',
                'Monitor for disease signs weekly',
                'Maintain proper watering schedule',
                'Ensure good nutrition',
                'Provide adequate sunlight',
                'Keep area clean',
                'Inspect for pests regularly'
            ]
        }
    }
    
    # Exact match
    if disease_name in treatments:
        return treatments[disease_name]
    
    # Case-insensitive match
    disease_lower = disease_name.lower()
    for key, info in treatments.items():
        if key.lower() == disease_lower:
            return info
    
    # Partial match
    for key, info in treatments.items():
        if disease_lower in key.lower() or key.lower() in disease_lower:
            return info
    
    # Generic response
    return {
        'description': disease_name.replace('_', ' ').title(),
        'status': '📋 Identified',
        'recommendations': [
            f'Disease: {disease_name.replace("_", " ")}',
            'Consult plant pathologist for treatment',
            'Isolate infected plant',
            'Monitor symptom progression',
            'Apply preventive measures to nearby plants'
        ]
    }

