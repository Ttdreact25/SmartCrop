# TODO: Replace Dataset with Free Plant Leaf Detection API

## ✅ COMPLETED
1. Updated `smart_crop/leaf_detector.py` - Added PlantNet API integration
2. Updated `streamlit_app/app.py` - Added API key input and improved UI

## Usage Instructions
1. Get a free API key from: https://my.plantnet.org/
2. Enter the API key in the Streamlit app
3. Upload a leaf image for instant plant identification!

## Files Modified
- `smart_crop/leaf_detector.py` - Added PlantNet API support
- `streamlit_app/app.py` - Updated UI with API key input

## Note
- The local training scripts (train_leaf_model.py, train_leaf_model_advanced.py) are still available but optional
- Default detection is now via API (no training required)
- 500 free requests per day with PlantNet API

