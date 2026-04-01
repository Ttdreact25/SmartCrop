"""
Prediction History Module for Smart Crop Recommendation System.
Handles storing and retrieving user prediction history.
"""

import json
import os
from datetime import datetime
from pathlib import Path


# Prediction history database file path
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
HISTORY_DB_PATH = os.path.join(BASE_DIR, ".users", "prediction_history.json")


def ensure_history_db_exists():
    """Ensure the prediction history database directory and file exist."""
    db_dir = os.path.dirname(HISTORY_DB_PATH)
    os.makedirs(db_dir, exist_ok=True)
    if not os.path.exists(HISTORY_DB_PATH):
        with open(HISTORY_DB_PATH, "w") as f:
            json.dump({}, f)


def load_history():
    """Load all prediction history from the database."""
    ensure_history_db_exists()
    try:
        with open(HISTORY_DB_PATH, "r") as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        return {}


def save_history(history):
    """Save prediction history to the database."""
    ensure_history_db_exists()
    with open(HISTORY_DB_PATH, "w") as f:
        json.dump(history, f, indent=2)


def add_prediction(username: str, prediction_data: dict) -> bool:
    """
    Add a new prediction to user's history.
    
    Args:
        username: The username who made the prediction
        prediction_data: Dictionary containing prediction details:
            - type: 'crop' or 'fertilizer'
            - crop: Recommended crop name
            - location: Location of the farm
            - input_params: Dictionary of input parameters used
            - confidence: Prediction confidence percentage
            - yield_estimate: Estimated yield (optional)
            - status: 'success' or 'failed'
    
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        history = load_history()
        
        if username not in history:
            history[username] = []
        
        # Add timestamp to prediction
        prediction_data["timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        prediction_data["date"] = datetime.now().strftime("%Y-%m-%d")
        
        # Add to beginning of list (most recent first)
        history[username].insert(0, prediction_data)
        
        # Keep only last 100 predictions per user
        if len(history[username]) > 100:
            history[username] = history[username][:100]
        
        save_history(history)
        return True
    except Exception as e:
        print(f"Error adding prediction: {e}")
        return False


def get_user_predictions(username: str, limit: int = 50) -> list:
    """
    Get prediction history for a specific user.
    
    Args:
        username: The username to get predictions for
        limit: Maximum number of predictions to return
    
    Returns:
        list: List of prediction dictionaries
    """
    history = load_history()
    if username in history:
        return history[username][:limit]
    return []


def get_prediction_stats(username: str) -> dict:
    """
    Get statistics about user's predictions.
    
    Args:
        username: The username to get stats for
    
    Returns:
        dict: Statistics including total predictions, success rate, etc.
    """
    predictions = get_user_predictions(username, limit=1000)
    
    if not predictions:
        return {
            "total_predictions": 0,
            "successful_predictions": 0,
            "failed_predictions": 0,
            "success_rate": 0,
            "crop_predictions": 0,
            "fertilizer_predictions": 0,
            "most_predicted_crop": "N/A",
            "last_prediction_date": "N/A"
        }
    
    total = len(predictions)
    successful = sum(1 for p in predictions if p.get("status") == "success")
    failed = total - successful
    success_rate = (successful / total * 100) if total > 0 else 0
    
    crop_predictions = sum(1 for p in predictions if p.get("type") == "crop")
    fertilizer_predictions = sum(1 for p in predictions if p.get("type") == "fertilizer")
    
    # Find most predicted crop
    crop_counts = {}
    for p in predictions:
        if p.get("type") == "crop" and p.get("crop"):
            crop = p["crop"]
            crop_counts[crop] = crop_counts.get(crop, 0) + 1
    
    most_predicted_crop = max(crop_counts.items(), key=lambda x: x[1])[0] if crop_counts else "N/A"
    
    last_prediction_date = predictions[0].get("date", "N/A") if predictions else "N/A"
    
    return {
        "total_predictions": total,
        "successful_predictions": successful,
        "failed_predictions": failed,
        "success_rate": round(success_rate, 1),
        "crop_predictions": crop_predictions,
        "fertilizer_predictions": fertilizer_predictions,
        "most_predicted_crop": most_predicted_crop,
        "last_prediction_date": last_prediction_date
    }


def get_crop_distribution(username: str) -> dict:
    """
    Get distribution of crops predicted for a user.
    
    Args:
        username: The username to get distribution for
    
    Returns:
        dict: Dictionary with crop names as keys and counts as values
    """
    predictions = get_user_predictions(username, limit=1000)
    
    crop_counts = {}
    for p in predictions:
        if p.get("type") == "crop" and p.get("crop"):
            crop = p["crop"]
            crop_counts[crop] = crop_counts.get(crop, 0) + 1
    
    return crop_counts


def get_monthly_prediction_trend(username: str, months: int = 12) -> dict:
    """
    Get monthly prediction trend for a user.
    
    Args:
        username: The username to get trend for
        months: Number of months to include
    
    Returns:
        dict: Dictionary with months as keys and prediction counts as values
    """
    predictions = get_user_predictions(username, limit=1000)
    
    monthly_counts = {}
    for p in predictions:
        if p.get("date"):
            month = p["date"][:7]  # YYYY-MM format
            monthly_counts[month] = monthly_counts.get(month, 0) + 1
    
    # Sort by month and take last N months
    sorted_months = sorted(monthly_counts.items())[-months:]
    return dict(sorted_months)


def get_location_distribution(username: str) -> dict:
    """
    Get distribution of locations predicted for a user.
    
    Args:
        username: The username to get distribution for
    
    Returns:
        dict: Dictionary with locations as keys and counts as values
    """
    predictions = get_user_predictions(username, limit=1000)
    
    location_counts = {}
    for p in predictions:
        if p.get("location"):
            location = p["location"]
            location_counts[location] = location_counts.get(location, 0) + 1
    
    return location_counts


def delete_prediction(username: str, timestamp: str) -> bool:
    """
    Delete a specific prediction from user's history.
    
    Args:
        username: The username who owns the prediction
        timestamp: The timestamp of the prediction to delete
    
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        history = load_history()
        
        if username not in history:
            return False
        
        # Find and remove the prediction with matching timestamp
        history[username] = [
            p for p in history[username] 
            if p.get("timestamp") != timestamp
        ]
        
        save_history(history)
        return True
    except Exception as e:
        print(f"Error deleting prediction: {e}")
        return False


def clear_user_history(username: str) -> bool:
    """
    Clear all prediction history for a user.
    
    Args:
        username: The username to clear history for
    
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        history = load_history()
        
        if username in history:
            history[username] = []
            save_history(history)
        
        return True
    except Exception as e:
        print(f"Error clearing history: {e}")
        return False


def export_user_history(username: str, format: str = "json") -> str:
    """
    Export user's prediction history.
    
    Args:
        username: The username to export history for
        format: Export format ('json' or 'csv')
    
    Returns:
        str: Exported data as string
    """
    predictions = get_user_predictions(username, limit=1000)
    
    if format == "json":
        return json.dumps(predictions, indent=2)
    elif format == "csv":
        if not predictions:
            return ""
        
        # Get all unique keys
        all_keys = set()
        for p in predictions:
            all_keys.update(p.keys())
        
        # Create CSV header
        header = ",".join(sorted(all_keys))
        
        # Create CSV rows
        rows = []
        for p in predictions:
            row = []
            for key in sorted(all_keys):
                value = p.get(key, "")
                # Escape commas and quotes in CSV
                if isinstance(value, str) and ("," in value or '"' in value):
                    value = '"' + value.replace('"', '""') + '"'
                row.append(str(value))
            rows.append(",".join(row))
        
        return header + "\n" + "\n".join(rows)
    else:
        return json.dumps(predictions, indent=2)
