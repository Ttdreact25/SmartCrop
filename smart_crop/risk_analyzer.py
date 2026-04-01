"""
Risk Analysis Module for Smart Crop Recommendation System.
Predicts crop failure risk based on environmental factors.
"""

import json
import os
from datetime import datetime


# Risk factors and weights
RISK_FACTORS = {
    "rainfall": {
        "weight": 0.35,
        "optimal_range": {
            "Rice": (150, 300),
            "Wheat": (75, 150),
            "Cotton": (100, 200),
            "Sugarcane": (150, 250),
            "Maize": (100, 200),
            "Barley": (75, 150),
            "Millets": (50, 100),
            "Pulses": (75, 150),
            "Ground Nuts": (100, 200),
            "Oil seeds": (75, 150),
            "Tobacco": (100, 200),
            "Paddy": (150, 300),
            "Vegetables": (100, 200)
        },
        "risk_levels": {
            "very_low": (0, 50),
            "low": (50, 100),
            "moderate": (100, 200),
            "high": (200, 300),
            "very_high": (300, float('inf'))
        }
    },
    "temperature": {
        "weight": 0.30,
        "optimal_range": {
            "Rice": (25, 35),
            "Wheat": (15, 25),
            "Cotton": (25, 35),
            "Sugarcane": (25, 35),
            "Maize": (20, 30),
            "Barley": (15, 25),
            "Millets": (25, 35),
            "Pulses": (20, 30),
            "Ground Nuts": (25, 35),
            "Oil seeds": (20, 30),
            "Tobacco": (20, 30),
            "Paddy": (25, 35),
            "Vegetables": (20, 30)
        },
        "risk_levels": {
            "very_low": (0, 10),
            "low": (10, 20),
            "moderate": (20, 30),
            "high": (30, 40),
            "very_high": (40, float('inf'))
        }
    },
    "soil_ph": {
        "weight": 0.15,
        "optimal_range": {
            "Rice": (5.5, 7.0),
            "Wheat": (6.0, 7.5),
            "Cotton": (6.0, 7.5),
            "Sugarcane": (6.0, 7.5),
            "Maize": (5.5, 7.0),
            "Barley": (6.0, 7.5),
            "Millets": (5.5, 7.0),
            "Pulses": (6.0, 7.5),
            "Ground Nuts": (5.5, 7.0),
            "Oil seeds": (6.0, 7.5),
            "Tobacco": (5.5, 7.0),
            "Paddy": (5.5, 7.0),
            "Vegetables": (6.0, 7.0)
        },
        "risk_levels": {
            "very_low": (6.5, 7.5),
            "low": (6.0, 6.5),
            "moderate": (5.5, 6.0),
            "high": (5.0, 5.5),
            "very_high": (0, 5.0)
        }
    },
    "humidity": {
        "weight": 0.10,
        "optimal_range": {
            "Rice": (70, 90),
            "Wheat": (50, 70),
            "Cotton": (60, 80),
            "Sugarcane": (70, 90),
            "Maize": (60, 80),
            "Barley": (50, 70),
            "Millets": (50, 70),
            "Pulses": (50, 70),
            "Ground Nuts": (60, 80),
            "Oil seeds": (50, 70),
            "Tobacco": (60, 80),
            "Paddy": (70, 90),
            "Vegetables": (60, 80)
        },
        "risk_levels": {
            "very_low": (0, 40),
            "low": (40, 60),
            "moderate": (60, 80),
            "high": (80, 90),
            "very_high": (90, 100)
        }
    },
    "soil_nitrogen": {
        "weight": 0.10,
        "optimal_range": {
            "Rice": (60, 100),
            "Wheat": (60, 100),
            "Cotton": (60, 100),
            "Sugarcane": (80, 120),
            "Maize": (60, 100),
            "Barley": (60, 100),
            "Millets": (40, 80),
            "Pulses": (20, 40),
            "Ground Nuts": (40, 80),
            "Oil seeds": (40, 80),
            "Tobacco": (60, 100),
            "Paddy": (60, 100),
            "Vegetables": (60, 100)
        },
        "risk_levels": {
            "very_low": (80, 120),
            "low": (60, 80),
            "moderate": (40, 60),
            "high": (20, 40),
            "very_high": (0, 20)
        }
    }
}

# Risk level descriptions
RISK_DESCRIPTIONS = {
    "very_low": {
        "level": "Very Low",
        "color": "green",
        "icon": "✅",
        "description": "Conditions are optimal. Crop failure risk is minimal.",
        "recommendations": [
            "Continue current farming practices",
            "Monitor for pests and diseases",
            "Maintain regular irrigation schedule"
        ]
    },
    "low": {
        "level": "Low",
        "color": "lightgreen",
        "icon": "🟢",
        "description": "Conditions are favorable. Minor adjustments may improve yield.",
        "recommendations": [
            "Monitor weather forecasts",
            "Apply balanced fertilization",
            "Ensure proper drainage"
        ]
    },
    "moderate": {
        "level": "Moderate",
        "color": "yellow",
        "icon": "🟡",
        "description": "Some risk factors are outside optimal range. Action recommended.",
        "recommendations": [
            "Adjust irrigation based on rainfall",
            "Apply corrective fertilizers",
            "Consider protective measures"
        ]
    },
    "high": {
        "level": "High",
        "color": "orange",
        "icon": "🟠",
        "description": "Significant risk detected. Immediate action required.",
        "recommendations": [
            "Implement risk mitigation strategies",
            "Consider crop insurance",
            "Consult agricultural expert"
        ]
    },
    "very_high": {
        "level": "Very High",
        "color": "red",
        "icon": "🔴",
        "description": "Critical risk! Crop failure is likely without intervention.",
        "recommendations": [
            "Consider alternative crops",
            "Implement emergency measures",
            "Seek expert consultation immediately"
        ]
    }
}


def calculate_factor_risk(crop: str, factor: str, value: float) -> dict:
    """
    Calculate risk for a specific factor.
    
    Args:
        crop: Crop name
        factor: Risk factor name
        value: Current value of the factor
    
    Returns:
        dict: Risk assessment for the factor
    """
    factor_data = RISK_FACTORS.get(factor, {})
    optimal_range = factor_data.get("optimal_range", {}).get(crop, (0, 100))
    risk_levels = factor_data.get("risk_levels", {})
    
    # Determine risk level
    risk_level = "moderate"
    for level, (min_val, max_val) in risk_levels.items():
        if min_val <= value < max_val:
            risk_level = level
            break
    
    # Calculate deviation from optimal
    optimal_min, optimal_max = optimal_range
    optimal_mid = (optimal_min + optimal_max) / 2
    
    if value < optimal_min:
        deviation = ((optimal_min - value) / optimal_min) * 100
    elif value > optimal_max:
        deviation = ((value - optimal_max) / optimal_max) * 100
    else:
        deviation = 0
    
    return {
        "factor": factor,
        "value": value,
        "optimal_range": optimal_range,
        "risk_level": risk_level,
        "deviation": round(deviation, 1),
        "weight": factor_data.get("weight", 0)
    }


def analyze_crop_risk(
    crop: str,
    rainfall: float,
    temperature: float,
    soil_ph: float,
    humidity: float,
    soil_nitrogen: float
) -> dict:
    """
    Analyze overall crop failure risk.
    
    Args:
        crop: Crop name
        rainfall: Rainfall in mm
        temperature: Temperature in Celsius
        soil_ph: Soil pH level
        humidity: Humidity percentage
        soil_nitrogen: Soil nitrogen in ppm
    
    Returns:
        dict: Complete risk analysis
    """
    # Calculate risk for each factor
    factors = {
        "rainfall": calculate_factor_risk(crop, "rainfall", rainfall),
        "temperature": calculate_factor_risk(crop, "temperature", temperature),
        "soil_ph": calculate_factor_risk(crop, "soil_ph", soil_ph),
        "humidity": calculate_factor_risk(crop, "humidity", humidity),
        "soil_nitrogen": calculate_factor_risk(crop, "soil_nitrogen", soil_nitrogen)
    }
    
    # Calculate weighted risk score
    risk_scores = {
        "very_low": 0,
        "low": 25,
        "moderate": 50,
        "high": 75,
        "very_high": 100
    }
    
    total_weight = 0
    weighted_score = 0
    
    for factor_name, factor_data in factors.items():
        weight = factor_data["weight"]
        risk_level = factor_data["risk_level"]
        score = risk_scores[risk_level]
        
        weighted_score += score * weight
        total_weight += weight
    
    overall_score = weighted_score / total_weight if total_weight > 0 else 50
    
    # Determine overall risk level
    if overall_score < 20:
        overall_risk = "very_low"
    elif overall_score < 40:
        overall_risk = "low"
    elif overall_score < 60:
        overall_risk = "moderate"
    elif overall_score < 80:
        overall_risk = "high"
    else:
        overall_risk = "very_high"
    
    risk_info = RISK_DESCRIPTIONS[overall_risk]
    
    # Generate recommendations
    recommendations = risk_info["recommendations"].copy()
    
    # Add specific recommendations based on factors
    for factor_name, factor_data in factors.items():
        if factor_data["risk_level"] in ["high", "very_high"]:
            if factor_name == "rainfall":
                if factor_data["value"] < factor_data["optimal_range"][0]:
                    recommendations.append("Increase irrigation to compensate for low rainfall")
                else:
                    recommendations.append("Improve drainage to handle excess rainfall")
            elif factor_name == "temperature":
                if factor_data["value"] < factor_data["optimal_range"][0]:
                    recommendations.append("Use mulching to retain soil warmth")
                else:
                    recommendations.append("Provide shade or use heat-resistant varieties")
            elif factor_name == "soil_ph":
                if factor_data["value"] < factor_data["optimal_range"][0]:
                    recommendations.append("Apply lime to raise soil pH")
                else:
                    recommendations.append("Apply sulfur to lower soil pH")
            elif factor_name == "humidity":
                recommendations.append("Ensure proper air circulation to manage humidity")
            elif factor_name == "soil_nitrogen":
                recommendations.append("Apply nitrogen-rich fertilizers or green manure")
    
    return {
        "crop": crop,
        "overall_risk": overall_risk,
        "overall_score": round(overall_score, 1),
        "risk_level": risk_info["level"],
        "risk_color": risk_info["color"],
        "risk_icon": risk_info["icon"],
        "description": risk_info["description"],
        "factors": factors,
        "recommendations": recommendations,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }


def get_risk_comparison(crops: list, conditions: dict) -> list:
    """
    Compare risk levels for multiple crops under same conditions.
    
    Args:
        crops: List of crop names
        conditions: Dictionary with environmental conditions
    
    Returns:
        list: Risk analysis for each crop, sorted by risk (lowest first)
    """
    results = []
    for crop in crops:
        analysis = analyze_crop_risk(
            crop=crop,
            rainfall=conditions.get("rainfall", 100),
            temperature=conditions.get("temperature", 25),
            soil_ph=conditions.get("soil_ph", 6.5),
            humidity=conditions.get("humidity", 70),
            soil_nitrogen=conditions.get("soil_nitrogen", 60)
        )
        results.append(analysis)
    
    # Sort by overall score (lowest risk first)
    results.sort(key=lambda x: x["overall_score"])
    return results


def get_risk_history(username: str, limit: int = 10) -> list:
    """
    Get risk analysis history for a user.
    
    Args:
        username: Username
        limit: Maximum number of records
    
    Returns:
        list: List of risk analyses
    """
    try:
        history_path = os.path.join(os.path.dirname(__file__), "..", ".users", "risk_history.json")
        
        if not os.path.exists(history_path):
            return []
        
        with open(history_path, "r") as f:
            history = json.load(f)
        
        if username in history:
            return history[username][:limit]
        return []
    except Exception as e:
        print(f"Error loading risk history: {e}")
        return []


def save_risk_analysis(username: str, analysis: dict) -> bool:
    """
    Save risk analysis to user's history.
    
    Args:
        username: Username
        analysis: Risk analysis data
    
    Returns:
        bool: True if successful
    """
    try:
        history_path = os.path.join(os.path.dirname(__file__), "..", ".users", "risk_history.json")
        os.makedirs(os.path.dirname(history_path), exist_ok=True)
        
        history = {}
        if os.path.exists(history_path):
            with open(history_path, "r") as f:
                history = json.load(f)
        
        if username not in history:
            history[username] = []
        
        history[username].insert(0, analysis)
        
        # Keep only last 20 analyses
        if len(history[username]) > 20:
            history[username] = history[username][:20]
        
        with open(history_path, "w") as f:
            json.dump(history, f, indent=2)
        
        return True
    except Exception as e:
        print(f"Error saving risk analysis: {e}")
        return False
