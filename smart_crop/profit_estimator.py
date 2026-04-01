"""
Profit Estimation Module for Smart Crop Recommendation System.
Calculates expected yield, revenue, and profit/loss for farming operations.
"""

import json
import os
from datetime import datetime


# Crop yield and price data (per acre)
CROP_DATA = {
    "Rice": {
        "yield_per_acre": 1.56,  # tons
        "price_per_ton": 25000,  # INR
        "growing_season": "Kharif",
        "duration_days": 120
    },
    "Wheat": {
        "yield_per_acre": 1.17,
        "price_per_ton": 22000,
        "growing_season": "Rabi",
        "duration_days": 110
    },
    "Cotton": {
        "yield_per_acre": 1.70,
        "price_per_ton": 60000,
        "growing_season": "Kharif",
        "duration_days": 150
    },
    "Sugarcane": {
        "yield_per_acre": 15.0,
        "price_per_ton": 3500,
        "growing_season": "Annual",
        "duration_days": 365
    },
    "Maize": {
        "yield_per_acre": 2.5,
        "price_per_ton": 18000,
        "growing_season": "Kharif",
        "duration_days": 90
    },
    "Barley": {
        "yield_per_acre": 1.2,
        "price_per_ton": 20000,
        "growing_season": "Rabi",
        "duration_days": 100
    },
    "Millets": {
        "yield_per_acre": 0.8,
        "price_per_ton": 25000,
        "growing_season": "Kharif",
        "duration_days": 80
    },
    "Pulses": {
        "yield_per_acre": 0.6,
        "price_per_ton": 70000,
        "growing_season": "Rabi",
        "duration_days": 95
    },
    "Ground Nuts": {
        "yield_per_acre": 1.0,
        "price_per_acre": 55000,
        "growing_season": "Kharif",
        "duration_days": 110
    },
    "Oil seeds": {
        "yield_per_acre": 0.7,
        "price_per_ton": 65000,
        "growing_season": "Rabi",
        "duration_days": 100
    },
    "Tobacco": {
        "yield_per_acre": 1.5,
        "price_per_ton": 150000,
        "growing_season": "Annual",
        "duration_days": 120
    },
    "Paddy": {
        "yield_per_acre": 1.8,
        "price_per_ton": 24000,
        "growing_season": "Kharif",
        "duration_days": 130
    },
    "Vegetables": {
        "yield_per_acre": 3.17,
        "price_per_ton": 30000,
        "growing_season": "Annual",
        "duration_days": 90
    }
}

# Default cost estimates (per acre)
DEFAULT_COSTS = {
    "seeds": 3000,
    "fertilizer": 4500,
    "irrigation": 2500,
    "labor": 6000,
    "equipment": 2500,
    "pesticides": 1500,
    "other": 1500
}


def get_crop_info(crop_name: str) -> dict:
    """
    Get information about a specific crop.
    
    Args:
        crop_name: Name of the crop
    
    Returns:
        dict: Crop information or default values
    """
    return CROP_DATA.get(crop_name, {
        "yield_per_acre": 1.0,
        "price_per_ton": 25000,
        "growing_season": "Annual",
        "duration_days": 120
    })


def get_all_crops() -> list:
    """
    Get list of all available crops.
    
    Returns:
        list: List of crop names
    """
    return list(CROP_DATA.keys())


def calculate_profit(
    crop: str,
    land_size: float,
    seed_cost: float = None,
    fertilizer_cost: float = None,
    irrigation_cost: float = None,
    labor_cost: float = None,
    equipment_cost: float = None,
    pesticide_cost: float = None,
    other_cost: float = None,
    custom_yield: float = None,
    custom_price: float = None
) -> dict:
    """
    Calculate profit/loss for a farming operation.
    
    Args:
        crop: Name of the crop
        land_size: Land size in acres
        seed_cost: Cost of seeds (optional, uses default if None)
        fertilizer_cost: Cost of fertilizer (optional)
        irrigation_cost: Cost of irrigation (optional)
        labor_cost: Cost of labor (optional)
        equipment_cost: Cost of equipment (optional)
        pesticide_cost: Cost of pesticides (optional)
        other_cost: Other costs (optional)
        custom_yield: Custom yield per acre (optional, overrides crop default)
        custom_price: Custom price per ton (optional, overrides crop default)
    
    Returns:
        dict: Profit calculation results
    """
    # Get crop information
    crop_info = get_crop_info(crop)
    
    # Use custom values if provided, otherwise use crop defaults
    yield_per_acre = custom_yield if custom_yield is not None else crop_info["yield_per_acre"]
    price_per_ton = custom_price if custom_price is not None else crop_info["price_per_ton"]
    
    # Calculate total yield
    total_yield = yield_per_acre * land_size
    
    # Calculate total revenue
    total_revenue = total_yield * price_per_ton
    
    # Calculate costs (use provided values or defaults)
    costs = {
        "seeds": seed_cost if seed_cost is not None else DEFAULT_COSTS["seeds"] * land_size,
        "fertilizer": fertilizer_cost if fertilizer_cost is not None else DEFAULT_COSTS["fertilizer"] * land_size,
        "irrigation": irrigation_cost if irrigation_cost is not None else DEFAULT_COSTS["irrigation"] * land_size,
        "labor": labor_cost if labor_cost is not None else DEFAULT_COSTS["labor"] * land_size,
        "equipment": equipment_cost if equipment_cost is not None else DEFAULT_COSTS["equipment"] * land_size,
        "pesticides": pesticide_cost if pesticide_cost is not None else DEFAULT_COSTS["pesticides"] * land_size,
        "other": other_cost if other_cost is not None else DEFAULT_COSTS["other"] * land_size
    }
    
    # Calculate total cost
    total_cost = sum(costs.values())
    
    # Calculate profit/loss
    profit_loss = total_revenue - total_cost
    
    # Calculate profit margin
    profit_margin = (profit_loss / total_revenue * 100) if total_revenue > 0 else 0
    
    # Calculate ROI (Return on Investment)
    roi = (profit_loss / total_cost * 100) if total_cost > 0 else 0
    
    # Determine status
    if profit_loss > 0:
        status = "Profit"
        status_icon = "✅"
    elif profit_loss < 0:
        status = "Loss"
        status_icon = "❌"
    else:
        status = "Break-even"
        status_icon = "⚖️"
    
    return {
        "crop": crop,
        "land_size": land_size,
        "yield_per_acre": yield_per_acre,
        "total_yield": round(total_yield, 2),
        "price_per_ton": price_per_ton,
        "total_revenue": round(total_revenue, 2),
        "costs": {k: round(v, 2) for k, v in costs.items()},
        "total_cost": round(total_cost, 2),
        "profit_loss": round(profit_loss, 2),
        "profit_margin": round(profit_margin, 2),
        "roi": round(roi, 2),
        "status": status,
        "status_icon": status_icon,
        "growing_season": crop_info["growing_season"],
        "duration_days": crop_info["duration_days"],
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }


def get_profit_comparison(crops: list, land_size: float) -> list:
    """
    Compare profit estimates for multiple crops.
    
    Args:
        crops: List of crop names
        land_size: Land size in acres
    
    Returns:
        list: List of profit calculations sorted by profit
    """
    results = []
    for crop in crops:
        result = calculate_profit(crop, land_size)
        results.append(result)
    
    # Sort by profit (highest first)
    results.sort(key=lambda x: x["profit_loss"], reverse=True)
    return results


def get_cost_breakdown(crop: str, land_size: float) -> dict:
    """
    Get detailed cost breakdown for a crop.
    
    Args:
        crop: Name of the crop
        land_size: Land size in acres
    
    Returns:
        dict: Cost breakdown with percentages
    """
    result = calculate_profit(crop, land_size)
    costs = result["costs"]
    total_cost = result["total_cost"]
    
    breakdown = {}
    for cost_type, amount in costs.items():
        percentage = (amount / total_cost * 100) if total_cost > 0 else 0
        breakdown[cost_type] = {
            "amount": amount,
            "percentage": round(percentage, 1)
        }
    
    return breakdown


def save_profit_calculation(username: str, calculation: dict) -> bool:
    """
    Save a profit calculation to user's history.
    
    Args:
        username: Username
        calculation: Profit calculation data
    
    Returns:
        bool: True if successful
    """
    try:
        # Load existing calculations
        history_path = os.path.join(os.path.dirname(__file__), "..", ".users", "profit_history.json")
        os.makedirs(os.path.dirname(history_path), exist_ok=True)
        
        history = {}
        if os.path.exists(history_path):
            with open(history_path, "r") as f:
                history = json.load(f)
        
        # Add to user's history
        if username not in history:
            history[username] = []
        
        history[username].insert(0, calculation)
        
        # Keep only last 50 calculations
        if len(history[username]) > 50:
            history[username] = history[username][:50]
        
        # Save back to file
        with open(history_path, "w") as f:
            json.dump(history, f, indent=2)
        
        return True
    except Exception as e:
        print(f"Error saving profit calculation: {e}")
        return False


def get_profit_history(username: str, limit: int = 20) -> list:
    """
    Get profit calculation history for a user.
    
    Args:
        username: Username
        limit: Maximum number of records to return
    
    Returns:
        list: List of profit calculations
    """
    try:
        history_path = os.path.join(os.path.dirname(__file__), "..", ".users", "profit_history.json")
        
        if not os.path.exists(history_path):
            return []
        
        with open(history_path, "r") as f:
            history = json.load(f)
        
        if username in history:
            return history[username][:limit]
        return []
    except Exception as e:
        print(f"Error loading profit history: {e}")
        return []


def get_profit_stats(username: str) -> dict:
    """
    Get statistics about user's profit calculations.
    
    Args:
        username: Username
    
    Returns:
        dict: Statistics
    """
    history = get_profit_history(username, limit=100)
    
    if not history:
        return {
            "total_calculations": 0,
            "avg_profit": 0,
            "best_crop": "N/A",
            "worst_crop": "N/A",
            "total_land_analyzed": 0
        }
    
    total_calculations = len(history)
    profits = [calc["profit_loss"] for calc in history]
    avg_profit = sum(profits) / len(profits) if profits else 0
    
    # Find best and worst crops
    best_calc = max(history, key=lambda x: x["profit_loss"])
    worst_calc = min(history, key=lambda x: x["profit_loss"])
    
    total_land = sum(calc["land_size"] for calc in history)
    
    return {
        "total_calculations": total_calculations,
        "avg_profit": round(avg_profit, 2),
        "best_crop": best_calc["crop"],
        "best_profit": best_calc["profit_loss"],
        "worst_crop": worst_calc["crop"],
        "worst_profit": worst_calc["profit_loss"],
        "total_land_analyzed": round(total_land, 2)
    }
