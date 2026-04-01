"""
Crop Comparison Module for Smart Crop Recommendation System.
Compares two crops across multiple features.
"""

import json
import os
from datetime import datetime


# Crop comparison data
CROP_COMPARISON_DATA = {
    "Rice": {
        "profit_per_acre": 17500,
        "water_need": "High",
        "water_requirement_mm": 1200,
        "labor_intensive": "High",
        "machinery_need": "Medium",
        "growth_duration_days": 120,
        "market_demand": "High",
        "storage_difficulty": "Medium",
        "pest_resistance": "Medium",
        "disease_resistance": "Medium",
        "climate_sensitivity": "High",
        "soil_requirement": "Clayey, Loamy",
        "season": "Kharif",
        "yield_per_acre": 1.56,
        "price_per_ton": 25000,
        "cost_per_acre": 21500
    },
    "Wheat": {
        "profit_per_acre": 12000,
        "water_need": "Medium",
        "water_requirement_mm": 600,
        "labor_intensive": "Medium",
        "machinery_need": "High",
        "growth_duration_days": 110,
        "market_demand": "High",
        "storage_difficulty": "Low",
        "pest_resistance": "High",
        "disease_resistance": "High",
        "climate_sensitivity": "Medium",
        "soil_requirement": "Loamy, Sandy",
        "season": "Rabi",
        "yield_per_acre": 1.17,
        "price_per_ton": 22000,
        "cost_per_acre": 15000
    },
    "Cotton": {
        "profit_per_acre": 45000,
        "water_need": "Medium",
        "water_requirement_mm": 800,
        "labor_intensive": "High",
        "machinery_need": "Medium",
        "growth_duration_days": 150,
        "market_demand": "High",
        "storage_difficulty": "Low",
        "pest_resistance": "Low",
        "disease_resistance": "Low",
        "climate_sensitivity": "High",
        "soil_requirement": "Black, Loamy",
        "season": "Kharif",
        "yield_per_acre": 1.70,
        "price_per_ton": 60000,
        "cost_per_acre": 35000
    },
    "Sugarcane": {
        "profit_per_acre": 30000,
        "water_need": "Very High",
        "water_requirement_mm": 2000,
        "labor_intensive": "Very High",
        "machinery_need": "High",
        "growth_duration_days": 365,
        "market_demand": "High",
        "storage_difficulty": "Very High",
        "pest_resistance": "Medium",
        "disease_resistance": "Medium",
        "climate_sensitivity": "High",
        "soil_requirement": "Loamy, Clayey",
        "season": "Annual",
        "yield_per_acre": 15.0,
        "price_per_ton": 3500,
        "cost_per_acre": 50000
    },
    "Maize": {
        "profit_per_acre": 15000,
        "water_need": "Medium",
        "water_requirement_mm": 600,
        "labor_intensive": "Low",
        "machinery_need": "High",
        "growth_duration_days": 90,
        "market_demand": "High",
        "storage_difficulty": "Low",
        "pest_resistance": "Medium",
        "disease_resistance": "Medium",
        "climate_sensitivity": "Medium",
        "soil_requirement": "Loamy, Sandy",
        "season": "Kharif",
        "yield_per_acre": 2.5,
        "price_per_ton": 18000,
        "cost_per_acre": 12000
    },
    "Barley": {
        "profit_per_acre": 10000,
        "water_need": "Low",
        "water_requirement_mm": 400,
        "labor_intensive": "Low",
        "machinery_need": "High",
        "growth_duration_days": 100,
        "market_demand": "Medium",
        "storage_difficulty": "Low",
        "pest_resistance": "High",
        "disease_resistance": "High",
        "climate_sensitivity": "Low",
        "soil_requirement": "Sandy, Loamy",
        "season": "Rabi",
        "yield_per_acre": 1.2,
        "price_per_ton": 20000,
        "cost_per_acre": 8000
    },
    "Millets": {
        "profit_per_acre": 8000,
        "water_need": "Very Low",
        "water_requirement_mm": 300,
        "labor_intensive": "Low",
        "machinery_need": "Low",
        "growth_duration_days": 80,
        "market_demand": "Medium",
        "storage_difficulty": "Low",
        "pest_resistance": "High",
        "disease_resistance": "High",
        "climate_sensitivity": "Low",
        "soil_requirement": "Sandy, Loamy",
        "season": "Kharif",
        "yield_per_acre": 0.8,
        "price_per_ton": 25000,
        "cost_per_acre": 5000
    },
    "Pulses": {
        "profit_per_acre": 20000,
        "water_need": "Low",
        "water_requirement_mm": 400,
        "labor_intensive": "Low",
        "machinery_need": "Low",
        "growth_duration_days": 95,
        "market_demand": "High",
        "storage_difficulty": "Low",
        "pest_resistance": "High",
        "disease_resistance": "High",
        "climate_sensitivity": "Low",
        "soil_requirement": "Loamy, Sandy",
        "season": "Rabi",
        "yield_per_acre": 0.6,
        "price_per_ton": 70000,
        "cost_per_acre": 8000
    },
    "Ground Nuts": {
        "profit_per_acre": 25000,
        "water_need": "Medium",
        "water_requirement_mm": 600,
        "labor_intensive": "Medium",
        "machinery_need": "Medium",
        "growth_duration_days": 110,
        "market_demand": "High",
        "storage_difficulty": "Medium",
        "pest_resistance": "Medium",
        "disease_resistance": "Medium",
        "climate_sensitivity": "Medium",
        "soil_requirement": "Sandy, Loamy",
        "season": "Kharif",
        "yield_per_acre": 1.0,
        "price_per_ton": 55000,
        "cost_per_acre": 15000
    },
    "Oil seeds": {
        "profit_per_acre": 20000,
        "water_need": "Low",
        "water_requirement_mm": 400,
        "labor_intensive": "Low",
        "machinery_need": "Medium",
        "growth_duration_days": 100,
        "market_demand": "High",
        "storage_difficulty": "Low",
        "pest_resistance": "High",
        "disease_resistance": "High",
        "climate_sensitivity": "Low",
        "soil_requirement": "Loamy, Sandy",
        "season": "Rabi",
        "yield_per_acre": 0.7,
        "price_per_ton": 65000,
        "cost_per_acre": 10000
    },
    "Tobacco": {
        "profit_per_acre": 80000,
        "water_need": "Medium",
        "water_requirement_mm": 800,
        "labor_intensive": "Very High",
        "machinery_need": "Low",
        "growth_duration_days": 120,
        "market_demand": "Medium",
        "storage_difficulty": "High",
        "pest_resistance": "Low",
        "disease_resistance": "Low",
        "climate_sensitivity": "High",
        "soil_requirement": "Sandy, Loamy",
        "season": "Annual",
        "yield_per_acre": 1.5,
        "price_per_ton": 150000,
        "cost_per_acre": 50000
    },
    "Paddy": {
        "profit_per_acre": 18000,
        "water_need": "High",
        "water_requirement_mm": 1200,
        "labor_intensive": "High",
        "machinery_need": "Medium",
        "growth_duration_days": 130,
        "market_demand": "High",
        "storage_difficulty": "Medium",
        "pest_resistance": "Medium",
        "disease_resistance": "Medium",
        "climate_sensitivity": "High",
        "soil_requirement": "Clayey, Loamy",
        "season": "Kharif",
        "yield_per_acre": 1.8,
        "price_per_ton": 24000,
        "cost_per_acre": 22000
    },
    "Vegetables": {
        "profit_per_acre": 35000,
        "water_need": "High",
        "water_requirement_mm": 1000,
        "labor_intensive": "Very High",
        "machinery_need": "Low",
        "growth_duration_days": 90,
        "market_demand": "Very High",
        "storage_difficulty": "Very High",
        "pest_resistance": "Low",
        "disease_resistance": "Low",
        "climate_sensitivity": "High",
        "soil_requirement": "Loamy, Sandy",
        "season": "Annual",
        "yield_per_acre": 3.17,
        "price_per_ton": 30000,
        "cost_per_acre": 25000
    }
}

# Comparison features
COMPARISON_FEATURES = {
    "profit_per_acre": {
        "name": "Profit per Acre",
        "unit": "₹",
        "higher_is_better": True,
        "description": "Expected profit per acre"
    },
    "water_need": {
        "name": "Water Need",
        "unit": "",
        "higher_is_better": False,
        "description": "Water requirement level"
    },
    "water_requirement_mm": {
        "name": "Water Requirement",
        "unit": "mm",
        "higher_is_better": False,
        "description": "Total water needed in mm"
    },
    "labor_intensive": {
        "name": "Labor Intensive",
        "unit": "",
        "higher_is_better": False,
        "description": "Labor requirement level"
    },
    "machinery_need": {
        "name": "Machinery Need",
        "unit": "",
        "higher_is_better": False,
        "description": "Machinery requirement level"
    },
    "growth_duration_days": {
        "name": "Growth Duration",
        "unit": "days",
        "higher_is_better": False,
        "description": "Days from planting to harvest"
    },
    "market_demand": {
        "name": "Market Demand",
        "unit": "",
        "higher_is_better": True,
        "description": "Current market demand level"
    },
    "storage_difficulty": {
        "name": "Storage Difficulty",
        "unit": "",
        "higher_is_better": False,
        "description": "Difficulty in storing the crop"
    },
    "pest_resistance": {
        "name": "Pest Resistance",
        "unit": "",
        "higher_is_better": True,
        "description": "Natural resistance to pests"
    },
    "disease_resistance": {
        "name": "Disease Resistance",
        "unit": "",
        "higher_is_better": True,
        "description": "Natural resistance to diseases"
    },
    "climate_sensitivity": {
        "name": "Climate Sensitivity",
        "unit": "",
        "higher_is_better": False,
        "description": "Sensitivity to climate changes"
    },
    "yield_per_acre": {
        "name": "Yield per Acre",
        "unit": "tons",
        "higher_is_better": True,
        "description": "Expected yield per acre"
    },
    "price_per_ton": {
        "name": "Price per Ton",
        "unit": "₹",
        "higher_is_better": True,
        "description": "Market price per ton"
    },
    "cost_per_acre": {
        "name": "Cost per Acre",
        "unit": "₹",
        "higher_is_better": False,
        "description": "Total cost per acre"
    }
}


def get_crop_data(crop: str) -> dict:
    """Get comparison data for a specific crop."""
    return CROP_COMPARISON_DATA.get(crop, {})


def get_all_crops() -> list:
    """Get list of all crops available for comparison."""
    return list(CROP_COMPARISON_DATA.keys())


def compare_crops(crop1: str, crop2: str) -> dict:
    """
    Compare two crops across all features.
    
    Args:
        crop1: First crop name
        crop2: Second crop name
    
    Returns:
        dict: Comparison results
    """
    data1 = get_crop_data(crop1)
    data2 = get_crop_data(crop2)
    
    if not data1 or not data2:
        return {"error": "One or both crops not found"}
    
    comparison = {
        "crop1": crop1,
        "crop2": crop2,
        "features": {},
        "winner": {},
        "summary": {}
    }
    
    # Compare each feature
    for feature_key, feature_info in COMPARISON_FEATURES.items():
        value1 = data1.get(feature_key, 0)
        value2 = data2.get(feature_key, 0)
        
        # Determine winner
        if feature_info["higher_is_better"]:
            if value1 > value2:
                winner = crop1
            elif value2 > value1:
                winner = crop2
            else:
                winner = "Tie"
        else:
            if value1 < value2:
                winner = crop1
            elif value2 < value1:
                winner = crop2
            else:
                winner = "Tie"
        
        comparison["features"][feature_key] = {
            "name": feature_info["name"],
            "unit": feature_info["unit"],
            "crop1_value": value1,
            "crop2_value": value2,
            "winner": winner,
            "description": feature_info["description"]
        }
        
        # Count wins
        if winner == crop1:
            comparison["winner"][crop1] = comparison["winner"].get(crop1, 0) + 1
        elif winner == crop2:
            comparison["winner"][crop2] = comparison["winner"].get(crop2, 0) + 1
    
    # Generate summary
    crop1_wins = comparison["winner"].get(crop1, 0)
    crop2_wins = comparison["winner"].get(crop2, 0)
    
    if crop1_wins > crop2_wins:
        comparison["summary"]["overall_winner"] = crop1
        comparison["summary"]["recommendation"] = f"{crop1} is better overall with {crop1_wins} advantages"
    elif crop2_wins > crop1_wins:
        comparison["summary"]["overall_winner"] = crop2
        comparison["summary"]["recommendation"] = f"{crop2} is better overall with {crop2_wins} advantages"
    else:
        comparison["summary"]["overall_winner"] = "Tie"
        comparison["summary"]["recommendation"] = "Both crops are equally good, choose based on your priorities"
    
    comparison["summary"]["crop1_wins"] = crop1_wins
    comparison["summary"]["crop2_wins"] = crop2_wins
    
    return comparison


def get_comparison_chart_data(comparison: dict) -> dict:
    """
    Prepare data for comparison charts.
    
    Args:
        comparison: Comparison results from compare_crops()
    
    Returns:
        dict: Chart-ready data
    """
    features = comparison.get("features", {})
    
    # Radar chart data
    radar_data = {
        "features": [],
        "crop1_values": [],
        "crop2_values": []
    }
    
    # Bar chart data
    bar_data = {
        "features": [],
        "crop1_values": [],
        "crop2_values": []
    }
    
    for feature_key, feature_info in features.items():
        radar_data["features"].append(feature_info["name"])
        radar_data["crop1_values"].append(feature_info["crop1_value"])
        radar_data["crop2_values"].append(feature_info["crop2_value"])
        
        bar_data["features"].append(feature_info["name"])
        bar_data["crop1_values"].append(feature_info["crop1_value"])
        bar_data["crop2_values"].append(feature_info["crop2_value"])
    
    return {
        "radar": radar_data,
        "bar": bar_data
    }


def get_crop_recommendation_comparison(crop1: str, crop2: str, priority: str = "profit") -> dict:
    """
    Get recommendation based on user priority.
    
    Args:
        crop1: First crop name
        crop2: Second crop name
        priority: User priority (profit, water, labor, duration, market)
    
    Returns:
        dict: Recommendation
    """
    comparison = compare_crops(crop1, crop2)
    
    priority_mapping = {
        "profit": "profit_per_acre",
        "water": "water_requirement_mm",
        "labor": "labor_intensive",
        "duration": "growth_duration_days",
        "market": "market_demand"
    }
    
    priority_feature = priority_mapping.get(priority, "profit_per_acre")
    feature_info = comparison["features"].get(priority_feature, {})
    
    if not feature_info:
        return {"error": "Priority feature not found"}
    
    winner = feature_info["winner"]
    
    if winner == "Tie":
        recommendation = f"Both crops are equal in terms of {priority}"
    else:
        recommendation = f"{winner} is better for {priority} priority"
    
    return {
        "priority": priority,
        "feature": feature_info["name"],
        "crop1_value": feature_info["crop1_value"],
        "crop2_value": feature_info["crop2_value"],
        "winner": winner,
        "recommendation": recommendation
    }
