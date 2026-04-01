"""
Nearby Crop Recommendation Module for Smart Crop Recommendation System.
Provides location-based crop recommendations based on regional farming patterns.
"""

import json
import os
from datetime import datetime


# Regional crop data based on Indian states and cities
REGIONAL_CROP_DATA = {
    "Tamil Nadu": {
        "Chennai": {
            "popular_crops": ["Rice", "Ground Nuts", "Sugarcane", "Cotton"],
            "climate": "Tropical",
            "soil_type": "Clayey, Loamy",
            "rainfall_mm": 1200,
            "temperature_range": "25-35°C",
            "notes": "Chennai region is known for rice cultivation and groundnut farming"
        },
        "Coimbatore": {
            "popular_crops": ["Cotton", "Sugarcane", "Maize", "Vegetables"],
            "climate": "Tropical",
            "soil_type": "Black, Loamy",
            "rainfall_mm": 700,
            "temperature_range": "20-35°C",
            "notes": "Coimbatore is a major cotton and sugarcane producing region"
        },
        "Madurai": {
            "popular_crops": ["Rice", "Cotton", "Sugarcane", "Vegetables"],
            "climate": "Tropical",
            "soil_type": "Clayey, Loamy",
            "rainfall_mm": 900,
            "temperature_range": "25-38°C",
            "notes": "Madurai is known for rice and cotton cultivation"
        }
    },
    "Punjab": {
        "Ludhiana": {
            "popular_crops": ["Wheat", "Rice", "Maize", "Cotton"],
            "climate": "Semi-arid",
            "soil_type": "Loamy, Sandy",
            "rainfall_mm": 600,
            "temperature_range": "5-45°C",
            "notes": "Ludhiana is the breadbasket of India, known for wheat and rice"
        },
        "Amritsar": {
            "popular_crops": ["Wheat", "Rice", "Maize", "Barley"],
            "climate": "Semi-arid",
            "soil_type": "Loamy, Sandy",
            "rainfall_mm": 500,
            "temperature_range": "0-45°C",
            "notes": "Amritsar is a major wheat and rice producing region"
        },
        "Jalandhar": {
            "popular_crops": ["Wheat", "Rice", "Sugarcane", "Vegetables"],
            "climate": "Semi-arid",
            "soil_type": "Loamy, Sandy",
            "rainfall_mm": 550,
            "temperature_range": "5-45°C",
            "notes": "Jalandhar is known for wheat and rice cultivation"
        }
    },
    "Maharashtra": {
        "Mumbai": {
            "popular_crops": ["Rice", "Vegetables", "Sugarcane", "Cotton"],
            "climate": "Tropical",
            "soil_type": "Clayey, Loamy",
            "rainfall_mm": 2000,
            "temperature_range": "20-35°C",
            "notes": "Mumbai region is known for rice and vegetable cultivation"
        },
        "Pune": {
            "popular_crops": ["Sugarcane", "Grapes", "Vegetables", "Wheat"],
            "climate": "Tropical",
            "soil_type": "Black, Loamy",
            "rainfall_mm": 700,
            "temperature_range": "15-35°C",
            "notes": "Pune is known for sugarcane and grape cultivation"
        },
        "Nagpur": {
            "popular_crops": ["Oranges", "Cotton", "Soybean", "Wheat"],
            "climate": "Tropical",
            "soil_type": "Black, Loamy",
            "rainfall_mm": 1200,
            "temperature_range": "15-45°C",
            "notes": "Nagpur is famous for oranges and cotton cultivation"
        }
    },
    "Karnataka": {
        "Bangalore": {
            "popular_crops": ["Ragi", "Vegetables", "Rice", "Sugarcane"],
            "climate": "Tropical",
            "soil_type": "Red, Loamy",
            "rainfall_mm": 900,
            "temperature_range": "15-35°C",
            "notes": "Bangalore is known for ragi and vegetable cultivation"
        },
        "Mysore": {
            "popular_crops": ["Rice", "Sugarcane", "Vegetables", "Ragi"],
            "climate": "Tropical",
            "soil_type": "Red, Loamy",
            "rainfall_mm": 800,
            "temperature_range": "15-35°C",
            "notes": "Mysore is known for rice and sugarcane cultivation"
        },
        "Hubli": {
            "popular_crops": ["Cotton", "Ground Nuts", "Wheat", "Jowar"],
            "climate": "Semi-arid",
            "soil_type": "Black, Loamy",
            "rainfall_mm": 600,
            "temperature_range": "15-40°C",
            "notes": "Hubli is known for cotton and groundnut cultivation"
        }
    },
    "Gujarat": {
        "Ahmedabad": {
            "popular_crops": ["Cotton", "Ground Nuts", "Wheat", "Tobacco"],
            "climate": "Semi-arid",
            "soil_type": "Black, Loamy",
            "rainfall_mm": 800,
            "temperature_range": "10-45°C",
            "notes": "Ahmedabad is a major cotton and groundnut producing region"
        },
        "Surat": {
            "popular_crops": ["Rice", "Sugarcane", "Vegetables", "Cotton"],
            "climate": "Tropical",
            "soil_type": "Clayey, Loamy",
            "rainfall_mm": 1200,
            "temperature_range": "15-40°C",
            "notes": "Surat is known for rice and sugarcane cultivation"
        },
        "Rajkot": {
            "popular_crops": ["Cotton", "Ground Nuts", "Wheat", "Jowar"],
            "climate": "Semi-arid",
            "soil_type": "Black, Loamy",
            "rainfall_mm": 600,
            "temperature_range": "10-45°C",
            "notes": "Rajkot is known for cotton and groundnut cultivation"
        }
    },
    "Andhra Pradesh": {
        "Hyderabad": {
            "popular_crops": ["Rice", "Cotton", "Maize", "Sugarcane"],
            "climate": "Tropical",
            "soil_type": "Clayey, Loamy",
            "rainfall_mm": 800,
            "temperature_range": "15-40°C",
            "notes": "Hyderabad is known for rice and cotton cultivation"
        },
        "Vijayawada": {
            "popular_crops": ["Rice", "Sugarcane", "Cotton", "Tobacco"],
            "climate": "Tropical",
            "soil_type": "Clayey, Loamy",
            "rainfall_mm": 1000,
            "temperature_range": "20-40°C",
            "notes": "Vijayawada is a major rice producing region"
        },
        "Visakhapatnam": {
            "popular_crops": ["Rice", "Sugarcane", "Vegetables", "Cashew"],
            "climate": "Tropical",
            "soil_type": "Red, Loamy",
            "rainfall_mm": 1200,
            "temperature_range": "20-35°C",
            "notes": "Visakhapatnam is known for rice and cashew cultivation"
        }
    },
    "West Bengal": {
        "Kolkata": {
            "popular_crops": ["Rice", "Jute", "Vegetables", "Sugarcane"],
            "climate": "Tropical",
            "soil_type": "Clayey, Loamy",
            "rainfall_mm": 1800,
            "temperature_range": "15-35°C",
            "notes": "Kolkata is known for rice and jute cultivation"
        },
        "Howrah": {
            "popular_crops": ["Rice", "Vegetables", "Jute", "Sugarcane"],
            "climate": "Tropical",
            "soil_type": "Clayey, Loamy",
            "rainfall_mm": 1800,
            "temperature_range": "15-35°C",
            "notes": "Howrah is known for rice and vegetable cultivation"
        },
        "Durgapur": {
            "popular_crops": ["Rice", "Wheat", "Vegetables", "Sugarcane"],
            "climate": "Tropical",
            "soil_type": "Clayey, Loamy",
            "rainfall_mm": 1500,
            "temperature_range": "10-40°C",
            "notes": "Durgapur is known for rice and wheat cultivation"
        }
    },
    "Uttar Pradesh": {
        "Lucknow": {
            "popular_crops": ["Wheat", "Rice", "Sugarcane", "Vegetables"],
            "climate": "Subtropical",
            "soil_type": "Loamy, Sandy",
            "rainfall_mm": 1000,
            "temperature_range": "5-45°C",
            "notes": "Lucknow is known for wheat and rice cultivation"
        },
        "Kanpur": {
            "popular_crops": ["Wheat", "Rice", "Sugarcane", "Cotton"],
            "climate": "Subtropical",
            "soil_type": "Loamy, Sandy",
            "rainfall_mm": 900,
            "temperature_range": "5-45°C",
            "notes": "Kanpur is a major wheat and rice producing region"
        },
        "Varanasi": {
            "popular_crops": ["Rice", "Wheat", "Sugarcane", "Vegetables"],
            "climate": "Subtropical",
            "soil_type": "Loamy, Sandy",
            "rainfall_mm": 1100,
            "temperature_range": "10-45°C",
            "notes": "Varanasi is known for rice and wheat cultivation"
        }
    }
}


def get_all_states() -> list:
    """Get list of all states with regional data."""
    return list(REGIONAL_CROP_DATA.keys())


def get_cities_in_state(state: str) -> list:
    """Get list of cities in a specific state."""
    state_data = REGIONAL_CROP_DATA.get(state, {})
    return list(state_data.keys())


def get_regional_data(state: str, city: str) -> dict:
    """Get regional crop data for a specific location."""
    return REGIONAL_CROP_DATA.get(state, {}).get(city, {})


def get_nearby_crops(state: str, city: str) -> dict:
    """
    Get popular crops grown near a location.
    
    Args:
        state: State name
        city: City name
    
    Returns:
        dict: Nearby crop recommendations
    """
    regional_data = get_regional_data(state, city)
    
    if not regional_data:
        return {
            "error": f"No data available for {city}, {state}",
            "suggestion": "Try a nearby major city"
        }
    
    popular_crops = regional_data.get("popular_crops", [])
    
    # Get crop details
    crop_details = []
    for crop in popular_crops:
        from smart_crop import profit_estimator
        crop_info = profit_estimator.get_crop_info(crop)
        crop_details.append({
            "name": crop,
            "yield_per_acre": crop_info.get("yield_per_acre", 0),
            "price_per_ton": crop_info.get("price_per_ton", 0),
            "season": crop_info.get("growing_season", "Annual"),
            "duration_days": crop_info.get("duration_days", 120)
        })
    
    return {
        "state": state,
        "city": city,
        "climate": regional_data.get("climate", "Unknown"),
        "soil_type": regional_data.get("soil_type", "Unknown"),
        "rainfall_mm": regional_data.get("rainfall_mm", 0),
        "temperature_range": regional_data.get("temperature_range", "Unknown"),
        "popular_crops": popular_crops,
        "crop_details": crop_details,
        "notes": regional_data.get("notes", ""),
        "recommendation": f"Farmers near {city} typically grow: {', '.join(popular_crops)}"
    }


def get_location_based_recommendations(state: str, city: str, farm_size: float) -> dict:
    """
    Get comprehensive location-based crop recommendations.
    
    Args:
        state: State name
        city: City name
        farm_size: Farm size in acres
    
    Returns:
        dict: Complete recommendations
    """
    nearby_data = get_nearby_crops(state, city)
    
    if "error" in nearby_data:
        return nearby_data
    
    # Calculate profit estimates for each popular crop
    from smart_crop import profit_estimator
    
    profit_estimates = []
    for crop in nearby_data["popular_crops"]:
        profit_result = profit_estimator.calculate_profit(crop, farm_size)
        profit_estimates.append({
            "crop": crop,
            "profit": profit_result["profit_loss"],
            "revenue": profit_result["total_revenue"],
            "cost": profit_result["total_cost"],
            "yield": profit_result["total_yield"]
        })
    
    # Sort by profit
    profit_estimates.sort(key=lambda x: x["profit"], reverse=True)
    
    # Get equipment recommendations
    from smart_crop import equipment_recommender
    
    equipment_recommendations = {}
    for crop in nearby_data["popular_crops"][:3]:  # Top 3 crops
        equip_rec = equipment_recommender.get_equipment_recommendation_summary(crop, farm_size)
        equipment_recommendations[crop] = {
            "essential": equip_rec["essential"]["equipment"],
            "total_cost": equip_rec["total_cost"]
        }
    
    return {
        "location": {
            "state": state,
            "city": city,
            "climate": nearby_data["climate"],
            "soil_type": nearby_data["soil_type"],
            "rainfall_mm": nearby_data["rainfall_mm"],
            "temperature_range": nearby_data["temperature_range"]
        },
        "popular_crops": nearby_data["popular_crops"],
        "crop_details": nearby_data["crop_details"],
        "profit_estimates": profit_estimates,
        "equipment_recommendations": equipment_recommendations,
        "notes": nearby_data["notes"],
        "recommendation": nearby_data["recommendation"],
        "farm_size": farm_size
    }


def search_location(query: str) -> list:
    """
    Search for locations matching a query.
    
    Args:
        query: Search query (state or city name)
    
    Returns:
        list: Matching locations
    """
    query_lower = query.lower()
    results = []
    
    for state, cities in REGIONAL_CROP_DATA.items():
        if query_lower in state.lower():
            for city in cities.keys():
                results.append({
                    "state": state,
                    "city": city,
                    "display": f"{city}, {state}"
                })
        else:
            for city in cities.keys():
                if query_lower in city.lower():
                    results.append({
                        "state": state,
                        "city": city,
                        "display": f"{city}, {state}"
                    })
    
    return results[:10]  # Limit to 10 results
