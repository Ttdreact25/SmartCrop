"""
Equipment Recommendation Module for Smart Crop Recommendation System.
Recommends farming equipment based on crop type and farm size.
"""

import json
import os
from datetime import datetime


# Equipment database with details
EQUIPMENT_DATABASE = {
    "Tractor": {
        "category": "Power",
        "description": "Primary power source for farming operations",
        "uses": ["Plowing", "Harrowing", "Transportation", "PTO operations"],
        "price_range": "₹5,00,000 - ₹15,00,000",
        "fuel_type": "Diesel",
        "maintenance": "Regular servicing every 250 hours",
        "lifespan": "10-15 years"
    },
    "Power Tiller": {
        "category": "Power",
        "description": "Compact power source for small farms",
        "uses": ["Tilling", "Weeding", "Spraying", "Transportation"],
        "price_range": "₹50,000 - ₹2,00,000",
        "fuel_type": "Diesel/Petrol",
        "maintenance": "Regular oil changes",
        "lifespan": "5-8 years"
    },
    "Rotavator": {
        "category": "Tillage",
        "description": "Rotary tillage equipment for seedbed preparation",
        "uses": ["Soil pulverization", "Weed incorporation", "Seedbed preparation"],
        "price_range": "₹30,000 - ₹1,00,000",
        "fuel_type": "PTO driven",
        "maintenance": "Blade sharpening annually",
        "lifespan": "8-10 years"
    },
    "Disc Plough": {
        "category": "Tillage",
        "description": "Primary tillage equipment for breaking hard soil",
        "uses": ["Deep plowing", "Stubble incorporation", "Soil inversion"],
        "price_range": "₹25,000 - ₹80,000",
        "fuel_type": "PTO driven",
        "maintenance": "Disc sharpening",
        "lifespan": "10-12 years"
    },
    "Seed Drill": {
        "category": "Planting",
        "description": "Precision seeding equipment",
        "uses": ["Seed placement", "Row spacing", "Depth control"],
        "price_range": "₹40,000 - ₹1,50,000",
        "fuel_type": "PTO driven",
        "maintenance": "Calibration before use",
        "lifespan": "8-10 years"
    },
    "Transplanter": {
        "category": "Planting",
        "description": "Equipment for transplanting seedlings",
        "uses": ["Rice transplanting", "Vegetable transplanting"],
        "price_range": "₹1,50,000 - ₹5,00,000",
        "fuel_type": "Manual/Motorized",
        "maintenance": "Regular cleaning",
        "lifespan": "5-7 years"
    },
    "Sprayer": {
        "category": "Protection",
        "description": "Equipment for applying pesticides and fertilizers",
        "uses": ["Pesticide application", "Foliar feeding", "Herbicide application"],
        "price_range": "₹5,000 - ₹50,000",
        "fuel_type": "Manual/Battery/Motorized",
        "maintenance": "Nozzle cleaning",
        "lifespan": "3-5 years"
    },
    "Duster": {
        "category": "Protection",
        "description": "Equipment for applying dust formulations",
        "uses": ["Dust pesticide application", "Sulfur dusting"],
        "price_range": "₹3,000 - ₹20,000",
        "fuel_type": "Manual/Battery",
        "maintenance": "Regular cleaning",
        "lifespan": "3-5 years"
    },
    "Harvester": {
        "category": "Harvesting",
        "description": "Mechanical harvesting equipment",
        "uses": ["Crop cutting", "Threshing", "Cleaning"],
        "price_range": "₹5,00,000 - ₹25,00,000",
        "fuel_type": "Diesel",
        "maintenance": "Regular servicing",
        "lifespan": "10-15 years"
    },
    "Reaper": {
        "category": "Harvesting",
        "description": "Equipment for cutting standing crops",
        "uses": ["Crop cutting", "Windrowing"],
        "price_range": "₹50,000 - ₹2,00,000",
        "fuel_type": "PTO driven",
        "maintenance": "Blade sharpening",
        "lifespan": "8-10 years"
    },
    "Thresher": {
        "category": "Harvesting",
        "description": "Equipment for separating grain from stalk",
        "uses": ["Grain separation", "Straw separation"],
        "price_range": "₹30,000 - ₹1,50,000",
        "fuel_type": "Electric/Diesel",
        "maintenance": "Regular cleaning",
        "lifespan": "8-10 years"
    },
    "Winnower": {
        "category": "Harvesting",
        "description": "Equipment for cleaning grain",
        "uses": ["Grain cleaning", "Chaff removal"],
        "price_range": "₹10,000 - ₹50,000",
        "fuel_type": "Electric",
        "maintenance": "Regular cleaning",
        "lifespan": "5-7 years"
    },
    "Irrigation Pump": {
        "category": "Irrigation",
        "description": "Water pumping equipment",
        "uses": ["Water extraction", "Irrigation supply"],
        "price_range": "₹10,000 - ₹1,00,000",
        "fuel_type": "Electric/Diesel",
        "maintenance": "Regular servicing",
        "lifespan": "8-10 years"
    },
    "Drip Irrigation System": {
        "category": "Irrigation",
        "description": "Precision irrigation system",
        "uses": ["Water conservation", "Fertigation", "Root zone irrigation"],
        "price_range": "₹30,000 - ₹1,50,000",
        "fuel_type": "Gravity/Electric",
        "maintenance": "Filter cleaning",
        "lifespan": "10-15 years"
    },
    "Sprinkler System": {
        "category": "Irrigation",
        "description": "Overhead irrigation system",
        "uses": ["Field irrigation", "Frost protection"],
        "price_range": "₹20,000 - ₹1,00,000",
        "fuel_type": "Electric/Diesel",
        "maintenance": "Nozzle cleaning",
        "lifespan": "10-12 years"
    },
    "Weeder": {
        "category": "Weeding",
        "description": "Equipment for removing weeds",
        "uses": ["Weed removal", "Soil aeration"],
        "price_range": "₹5,000 - ₹30,000",
        "fuel_type": "Manual/Power",
        "maintenance": "Blade sharpening",
        "lifespan": "5-7 years"
    },
    "Cultivator": {
        "category": "Tillage",
        "description": "Secondary tillage equipment",
        "uses": ["Weed control", "Soil aeration", "Fertilizer incorporation"],
        "price_range": "₹15,000 - ₹60,000",
        "fuel_type": "PTO driven",
        "maintenance": "Tine replacement",
        "lifespan": "8-10 years"
    },
    "Leveler": {
        "category": "Land Preparation",
        "description": "Land leveling equipment",
        "uses": ["Field leveling", "Water distribution"],
        "price_range": "₹20,000 - ₹80,000",
        "fuel_type": "PTO driven",
        "maintenance": "Regular inspection",
        "lifespan": "10-12 years"
    },
    "Ridger": {
        "category": "Land Preparation",
        "description": "Equipment for creating ridges",
        "uses": ["Ridge formation", "Furrow creation"],
        "price_range": "₹15,000 - ₹50,000",
        "fuel_type": "PTO driven",
        "maintenance": "Blade sharpening",
        "lifespan": "8-10 years"
    },
    "Mulcher": {
        "category": "Land Preparation",
        "description": "Equipment for mulching",
        "uses": ["Residue management", "Soil moisture conservation"],
        "price_range": "₹30,000 - ₹1,00,000",
        "fuel_type": "PTO driven",
        "maintenance": "Blade sharpening",
        "lifespan": "8-10 years"
    }
}

# Crop-specific equipment recommendations
CROP_EQUIPMENT_RECOMMENDATIONS = {
    "Rice": {
        "essential": ["Tractor", "Rotavator", "Transplanter", "Sprayer", "Irrigation Pump"],
        "recommended": ["Leveler", "Harvester", "Thresher", "Winnower"],
        "optional": ["Drip Irrigation System", "Weeder"],
        "notes": "Rice requires precise water management. Transplanter is essential for paddy cultivation."
    },
    "Wheat": {
        "essential": ["Tractor", "Disc Plough", "Seed Drill", "Sprayer", "Harvester"],
        "recommended": ["Rotavator", "Thresher", "Winnower", "Cultivator"],
        "optional": ["Irrigation Pump", "Leveler"],
        "notes": "Wheat is a Rabi crop. Seed drill ensures proper seed placement and spacing."
    },
    "Cotton": {
        "essential": ["Tractor", "Disc Plough", "Seed Drill", "Sprayer", "Duster"],
        "recommended": ["Cultivator", "Weeder", "Harvester", "Irrigation Pump"],
        "optional": ["Drip Irrigation System", "Ridger"],
        "notes": "Cotton requires regular pest management. Sprayer and duster are critical."
    },
    "Sugarcane": {
        "essential": ["Tractor", "Disc Plough", "Ridger", "Sprayer", "Irrigation Pump"],
        "recommended": ["Rotavator", "Cultivator", "Harvester", "Leveler"],
        "optional": ["Drip Irrigation System", "Mulcher"],
        "notes": "Sugarcane is a long-duration crop. Ridger is essential for furrow planting."
    },
    "Maize": {
        "essential": ["Tractor", "Rotavator", "Seed Drill", "Sprayer", "Harvester"],
        "recommended": ["Cultivator", "Weeder", "Thresher", "Irrigation Pump"],
        "optional": ["Drip Irrigation System", "Leveler"],
        "notes": "Maize is a versatile crop. Seed drill ensures proper spacing."
    },
    "Barley": {
        "essential": ["Tractor", "Disc Plough", "Seed Drill", "Sprayer", "Harvester"],
        "recommended": ["Rotavator", "Thresher", "Winnower", "Cultivator"],
        "optional": ["Irrigation Pump", "Leveler"],
        "notes": "Barley is similar to wheat. Seed drill is essential for proper planting."
    },
    "Millets": {
        "essential": ["Tractor", "Rotavator", "Seed Drill", "Sprayer"],
        "recommended": ["Cultivator", "Weeder", "Harvester", "Thresher"],
        "optional": ["Irrigation Pump", "Leveler"],
        "notes": "Millets are hardy crops. Basic equipment is sufficient."
    },
    "Pulses": {
        "essential": ["Tractor", "Rotavator", "Seed Drill", "Sprayer"],
        "recommended": ["Cultivator", "Weeder", "Harvester", "Thresher"],
        "optional": ["Irrigation Pump", "Leveler"],
        "notes": "Pulses are nitrogen-fixing crops. Minimal equipment needed."
    },
    "Ground Nuts": {
        "essential": ["Tractor", "Disc Plough", "Seed Drill", "Sprayer", "Digger"],
        "recommended": ["Rotavator", "Cultivator", "Weeder", "Thresher"],
        "optional": ["Irrigation Pump", "Leveler"],
        "notes": "Ground nuts require digging equipment for harvest."
    },
    "Oil seeds": {
        "essential": ["Tractor", "Rotavator", "Seed Drill", "Sprayer"],
        "recommended": ["Cultivator", "Weeder", "Harvester", "Thresher"],
        "optional": ["Irrigation Pump", "Leveler"],
        "notes": "Oil seeds include mustard, sunflower, etc. Basic equipment is sufficient."
    },
    "Tobacco": {
        "essential": ["Tractor", "Rotavator", "Transplanter", "Sprayer", "Irrigation Pump"],
        "recommended": ["Cultivator", "Weeder", "Curing equipment"],
        "optional": ["Drip Irrigation System", "Leveler"],
        "notes": "Tobacco requires careful management. Transplanter is essential."
    },
    "Paddy": {
        "essential": ["Tractor", "Rotavator", "Transplanter", "Sprayer", "Irrigation Pump"],
        "recommended": ["Leveler", "Harvester", "Thresher", "Winnower"],
        "optional": ["Drip Irrigation System", "Weeder"],
        "notes": "Paddy is similar to rice. Water management is critical."
    },
    "Vegetables": {
        "essential": ["Power Tiller", "Sprayer", "Irrigation Pump", "Weeder"],
        "recommended": ["Drip Irrigation System", "Rotavator", "Transplanter"],
        "optional": ["Sprinkler System", "Mulcher"],
        "notes": "Vegetables require precision irrigation. Drip system is highly recommended."
    }
}


def get_crop_equipment(crop_name: str) -> dict:
    """
    Get equipment recommendations for a specific crop.
    
    Args:
        crop_name: Name of the crop
    
    Returns:
        dict: Equipment recommendations
    """
    return CROP_EQUIPMENT_RECOMMENDATIONS.get(crop_name, {
        "essential": ["Tractor", "Rotavator", "Seed Drill", "Sprayer"],
        "recommended": ["Cultivator", "Weeder", "Harvester"],
        "optional": ["Irrigation Pump", "Leveler"],
        "notes": "General farming equipment recommendations."
    })


def get_equipment_details(equipment_name: str) -> dict:
    """
    Get detailed information about specific equipment.
    
    Args:
        equipment_name: Name of the equipment
    
    Returns:
        dict: Equipment details
    """
    return EQUIPMENT_DATABASE.get(equipment_name, {
        "category": "General",
        "description": "Farming equipment",
        "uses": ["General farming"],
        "price_range": "Varies",
        "fuel_type": "Varies",
        "maintenance": "Regular maintenance",
        "lifespan": "Varies"
    })


def get_all_equipment() -> list:
    """
    Get list of all available equipment.
    
    Returns:
        list: List of equipment names
    """
    return list(EQUIPMENT_DATABASE.keys())


def get_equipment_by_category(category: str) -> list:
    """
    Get equipment filtered by category.
    
    Args:
        category: Equipment category
    
    Returns:
        list: List of equipment in the category
    """
    return [
        name for name, details in EQUIPMENT_DATABASE.items()
        if details.get("category") == category
    ]


def get_equipment_categories() -> list:
    """
    Get all equipment categories.
    
    Returns:
        list: List of categories
    """
    categories = set()
    for details in EQUIPMENT_DATABASE.values():
        categories.add(details.get("category", "General"))
    return sorted(list(categories))


def calculate_equipment_cost(equipment_list: list, farm_size: float) -> dict:
    """
    Calculate estimated equipment cost based on farm size.
    
    Args:
        equipment_list: List of equipment names
        farm_size: Farm size in acres
    
    Returns:
        dict: Cost calculation
    """
    # Base costs per equipment (in INR)
    base_costs = {
        "Tractor": 800000,
        "Power Tiller": 100000,
        "Rotavator": 50000,
        "Disc Plough": 40000,
        "Seed Drill": 70000,
        "Transplanter": 250000,
        "Sprayer": 15000,
        "Duster": 8000,
        "Harvester": 1200000,
        "Reaper": 100000,
        "Thresher": 60000,
        "Winnower": 25000,
        "Irrigation Pump": 40000,
        "Drip Irrigation System": 80000,
        "Sprinkler System": 50000,
        "Weeder": 12000,
        "Cultivator": 30000,
        "Leveler": 40000,
        "Ridger": 25000,
        "Mulcher": 50000
    }
    
    total_cost = 0
    equipment_costs = {}
    
    for equipment in equipment_list:
        base_cost = base_costs.get(equipment, 50000)
        # Scale cost based on farm size (larger farms need larger equipment)
        if farm_size > 10:
            scaled_cost = base_cost * 1.5
        elif farm_size > 5:
            scaled_cost = base_cost * 1.2
        else:
            scaled_cost = base_cost
        
        equipment_costs[equipment] = round(scaled_cost)
        total_cost += scaled_cost
    
    return {
        "equipment_costs": equipment_costs,
        "total_cost": round(total_cost),
        "farm_size": farm_size
    }


def get_equipment_recommendation_summary(crop: str, farm_size: float) -> dict:
    """
    Get comprehensive equipment recommendation summary.
    
    Args:
        crop: Crop name
        farm_size: Farm size in acres
    
    Returns:
        dict: Complete recommendation summary
    """
    crop_equipment = get_crop_equipment(crop)
    
    essential_cost = calculate_equipment_cost(crop_equipment["essential"], farm_size)
    recommended_cost = calculate_equipment_cost(crop_equipment["recommended"], farm_size)
    optional_cost = calculate_equipment_cost(crop_equipment["optional"], farm_size)
    
    all_equipment = crop_equipment["essential"] + crop_equipment["recommended"] + crop_equipment["optional"]
    total_cost = calculate_equipment_cost(all_equipment, farm_size)
    
    return {
        "crop": crop,
        "farm_size": farm_size,
        "essential": {
            "equipment": crop_equipment["essential"],
            "cost": essential_cost["total_cost"]
        },
        "recommended": {
            "equipment": crop_equipment["recommended"],
            "cost": recommended_cost["total_cost"]
        },
        "optional": {
            "equipment": crop_equipment["optional"],
            "cost": optional_cost["total_cost"]
        },
        "total_equipment": len(all_equipment),
        "total_cost": total_cost["total_cost"],
        "notes": crop_equipment["notes"]
    }


def save_equipment_recommendation(username: str, recommendation: dict) -> bool:
    """
    Save equipment recommendation to user's history.
    
    Args:
        username: Username
        recommendation: Recommendation data
    
    Returns:
        bool: True if successful
    """
    try:
        history_path = os.path.join(os.path.dirname(__file__), "..", ".users", "equipment_history.json")
        os.makedirs(os.path.dirname(history_path), exist_ok=True)
        
        history = {}
        if os.path.exists(history_path):
            with open(history_path, "r") as f:
                history = json.load(f)
        
        if username not in history:
            history[username] = []
        
        history[username].insert(0, recommendation)
        
        # Keep only last 30 recommendations
        if len(history[username]) > 30:
            history[username] = history[username][:30]
        
        with open(history_path, "w") as f:
            json.dump(history, f, indent=2)
        
        return True
    except Exception as e:
        print(f"Error saving equipment recommendation: {e}")
        return False


def get_equipment_history(username: str, limit: int = 10) -> list:
    """
    Get equipment recommendation history for a user.
    
    Args:
        username: Username
        limit: Maximum number of records
    
    Returns:
        list: List of recommendations
    """
    try:
        history_path = os.path.join(os.path.dirname(__file__), "..", ".users", "equipment_history.json")
        
        if not os.path.exists(history_path):
            return []
        
        with open(history_path, "r") as f:
            history = json.load(f)
        
        if username in history:
            return history[username][:limit]
        return []
    except Exception as e:
        print(f"Error loading equipment history: {e}")
        return []
