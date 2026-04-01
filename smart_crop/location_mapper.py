import pandas as pd
import os

def get_state_city_mapping(location_df: pd.DataFrame) -> dict:
    if 'state_name' not in location_df.columns or 'name_of_city' not in location_df.columns:
        raise ValueError("Location DataFrame must contain 'state_name' and 'name_of_city' columns.")

    df_processed = location_df.drop_duplicates(subset=["name_of_city", "state_name"]).copy()
    return df_processed.groupby("state_name")["name_of_city"].unique().apply(list).to_dict()

def get_lat_lon(location_df: pd.DataFrame, city_name: str):
    if 'name_of_city' not in location_df.columns or 'location' not in location_df.columns:
        raise ValueError("Location DataFrame must contain 'name_of_city' and 'location' columns.")

    row = location_df[location_df["name_of_city"].str.lower() == city_name.lower()]
    if not row.empty:
        location_str = row.iloc[0]["location"]
        try:
            lat_str, lon_str = map(str.strip, location_str.split(","))
            return float(lat_str), float(lon_str)
        except ValueError:
            print(f"Warning: Could not parse latitude/longitude from '{location_str}' for city '{city_name}'")
            return None, None
    return None, None