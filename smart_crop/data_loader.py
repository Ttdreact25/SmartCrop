import pandas as pd

def load_crop_data(path = "../data/Crop_Recommendation.csv"):
    return pd.read_csv(path)

def load_location_data(path = "../data/Indian_cities_coordinates.csv"):
    return pd.read_csv(path)