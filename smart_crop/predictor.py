import joblib
import os

# Resolve model path relative to the project root so imports work
# regardless of the current working directory when running Streamlit.
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
MODEL_PATH = os.path.join(BASE_DIR, "saved_models", "crop_model.pkl")

def load_model():
    """Load the trained crop model from disk.

    Raises a FileNotFoundError with a helpful message if the model file is missing.
    """
    if not os.path.exists(MODEL_PATH):
        raise FileNotFoundError(
            f"Model file not found at expected path: {MODEL_PATH}.\n"
            "Make sure you have run the training notebook to generate 'saved_models/crop_model.pkl',\n"
            "or place the model file at that location. See notebooks/train_model.ipynb for details."
        )
    return joblib.load(MODEL_PATH)

def predict_crop(model, features: list):
    """
    Predicts the crop using the given features.

    Parameters:
    - model: Trained model object.
    - features: List of inputs [N, P, K, temperature, humidity, ph, rainfall].

    Returns:
    - The predicted crop name.
    """
    return model.predict([features])[0]


# --- Crop Duration and Information ---

_CROP_DURATION_CACHE = None

def load_crop_duration_data():
    """Load crop duration data from CSV file."""
    global _CROP_DURATION_CACHE
    
    if _CROP_DURATION_CACHE is not None:
        return _CROP_DURATION_CACHE
    
    import pandas as pd
    
    crops_csv_path = os.path.join(BASE_DIR, "data", "crops_duration.csv")
    
    if not os.path.exists(crops_csv_path):
        # Return empty dict if file doesn't exist yet
        _CROP_DURATION_CACHE = {}
        return _CROP_DURATION_CACHE
    
    df = pd.read_csv(crops_csv_path)
    crop_dict = {}
    
    for _, row in df.iterrows():
        crop_dict[row['crop_name'].lower()] = {
            'duration': row['growing_duration_days'],
            'season': row['season']
        }
    
    _CROP_DURATION_CACHE = crop_dict
    return crop_dict


def load_crop_duration_new_data():
    """Load crop duration data - alias for load_crop_duration_data for compatibility."""
    return load_crop_duration_data()


def get_crop_info(crop_name: str):
    """Get growing duration and season information for a crop.
    
    Parameters:
    - crop_name: Name of the crop (e.g., 'rice', 'wheat').
    
    Returns:
    - Dictionary with 'duration' (days) and 'season' keys, or None if not found.
    """
    crop_data = load_crop_duration_data()
    crop_lower = crop_name.lower()
    
    if crop_lower in crop_data:
        return crop_data[crop_lower]
    
    # Return default if not found
    return {'duration': 'Unknown', 'season': 'Unknown'}


# --- Fertilizer recommendation helpers ---

# paths are relative to project root for use in Streamlit
FERT_MODEL_PATH = os.path.join(BASE_DIR, "saved_models", "fertilizer_model.pkl")
SOIL_ENCODER_PATH = os.path.join(BASE_DIR, "saved_models", "soil_encoder.pkl")
CROP_ENCODER_PATH = os.path.join(BASE_DIR, "saved_models", "crop_encoder.pkl")
FERT_SCALER_PATH = os.path.join(BASE_DIR, "saved_models", "fertilizer_scaler.pkl")


def load_fertilizer_model(train_if_missing: bool = False):
    """Load the fertilizer recommendation model and related encoders/scaler.

    If any of the expected pickle files are missing and ``train_if_missing`` is True,
    the function will attempt to train a new model from
    ``data/Fertilizer Prediction.csv`` and save the resulting artifacts.

    Raises a FileNotFoundError if the files are missing and training is disabled or
    if training fails.
    """
    missing = [p for p in (FERT_MODEL_PATH, SOIL_ENCODER_PATH, CROP_ENCODER_PATH, FERT_SCALER_PATH) if not os.path.exists(p)]
    if missing:
        if train_if_missing:
            # attempt retraining
            train_fertilizer_model()
            missing = [p for p in (FERT_MODEL_PATH, SOIL_ENCODER_PATH, CROP_ENCODER_PATH, FERT_SCALER_PATH) if not os.path.exists(p)]
        if missing:
            raise FileNotFoundError(
                "The following fertilizer-related files were not found:\n" +
                "\n".join(missing) +
                "\nMake sure you have run the fertilizer training notebook or call "
                "predictor.train_fertilizer_model() to generate them."
            )

    fert_model = joblib.load(FERT_MODEL_PATH)
    soil_enc = joblib.load(SOIL_ENCODER_PATH)
    crop_enc = joblib.load(CROP_ENCODER_PATH)
    scaler = joblib.load(FERT_SCALER_PATH)
    return fert_model, soil_enc, crop_enc, scaler


def train_fertilizer_model(csv_path: str = None):
    """Train a fertilizer recommendation classifier and save artifacts.

    Parameters
    ----------
    csv_path : str, optional
        Path to the fertilizer dataset CSV.  Defaults to
        ``data/Fertilizer Prediction.csv`` relative to project root.
    """
    import pandas as _pd
    from sklearn.preprocessing import LabelEncoder as _LE
    from sklearn.preprocessing import StandardScaler as _SS
    from sklearn.model_selection import train_test_split as _tts
    from sklearn.tree import DecisionTreeClassifier as _DTC

    if csv_path is None:
        PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        csv_path = os.path.join(PROJECT_ROOT, "data", "Fertilizer Prediction.csv")

    df = _pd.read_csv(csv_path)

    # encode target
    fert_dict = {
        'Urea':1, 'DAP':2, '14-35-14':3, '28-28':4,
        '17-17-17':5, '20-20':6, '10-26-26':7,
    }
    df['fert_no'] = df['Fertilizer Name'].map(fert_dict)
    df = df.drop(columns=['Fertilizer Name'])

    # encode categorical
    soil_encoder = _LE()
    crop_encoder = _LE()
    df['Soil Type'] = soil_encoder.fit_transform(df['Soil Type'].astype(str))
    df['Crop Type'] = crop_encoder.fit_transform(df['Crop Type'].astype(str))

    X = df.drop('fert_no', axis=1)
    y = df['fert_no']

    scaler = _SS()
    X_scaled = scaler.fit_transform(X)

    model = _DTC()
    model.fit(X_scaled, y)

    # save artifacts
    joblib.dump(model, FERT_MODEL_PATH)
    joblib.dump(soil_encoder, SOIL_ENCODER_PATH)
    joblib.dump(crop_encoder, CROP_ENCODER_PATH)
    joblib.dump(scaler, FERT_SCALER_PATH)


def predict_fertilizer(fert_model, scaler, soil_encoder, crop_encoder, features: list):
    """Predict fertilizer name from the features list.

    Parameters:
    - fert_model: trained fertilizer classifier
    - scaler: the StandardScaler used during training
    - soil_encoder: LabelEncoder used on 'Soil Type'
    - crop_encoder: LabelEncoder used on 'Crop Type'
    - features: list in order [Temperature, Humidity, Moisture, Soil_Type, Crop_Type, Nitrogen, Potassium, Phosphorous]

    Returns:
    - a string fertilizer name (e.g. 'Urea')
    """
    import numpy as _np

    arr = _np.array([features])
    arr[:, 3] = soil_encoder.transform(arr[:, 3].astype(str))
    arr[:, 4] = crop_encoder.transform(arr[:, 4].astype(str))
    arr_scaled = scaler.transform(arr.astype(float))
    fert_no = fert_model.predict(arr_scaled)[0]
    fert_dict = {1: 'Urea', 2: 'DAP', 3: '14-35-14', 4: '28-28', 5: '17-17-17', 6: '20-20', 7: '10-26-26'}
    return fert_dict.get(fert_no, "Unknown")
