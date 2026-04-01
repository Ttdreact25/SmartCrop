"""
Storage & Preservation Tips Module for Smart Crop Recommendation System.
Provides guidance on how to store crops and avoid spoilage.
"""

import json
import os
from datetime import datetime


# Crop storage database
CROP_STORAGE_DATA = {
    "Rice": {
        "storage_method": "Airtight containers or bags",
        "ideal_temperature": "15-20°C",
        "ideal_humidity": "12-14%",
        "shelf_life": "6-12 months",
        "storage_tips": [
            "Store in airtight containers to prevent moisture absorption",
            "Keep in a cool, dry place away from direct sunlight",
            "Use moisture absorbers like silica gel packets",
            "Check regularly for insects or mold",
            "Avoid storing near strong odors"
        ],
        "spoilage_signs": [
            "Musty or off smell",
            "Discoloration or yellowing",
            "Presence of insects or webs",
            "Clumping or caking"
        ],
        "prevention_tips": [
            "Dry rice to 12-14% moisture before storage",
            "Use hermetic storage bags for long-term storage",
            "Freeze rice for 48 hours to kill insects before storage",
            "Store in small batches to reduce risk"
        ],
        "best_practices": [
            "Clean storage area thoroughly before use",
            "Elevate containers off the floor",
            "Use first-in-first-out (FIFO) method",
            "Label containers with storage date"
        ]
    },
    "Wheat": {
        "storage_method": "Airtight containers or silos",
        "ideal_temperature": "15-20°C",
        "ideal_humidity": "12-14%",
        "shelf_life": "6-12 months",
        "storage_tips": [
            "Store in airtight containers or grain silos",
            "Keep in a cool, dry place",
            "Use moisture absorbers",
            "Check regularly for pests",
            "Avoid storing near strong odors"
        ],
        "spoilage_signs": [
            "Musty or sour smell",
            "Discoloration",
            "Presence of insects",
            "Clumping or caking"
        ],
        "prevention_tips": [
            "Dry wheat to 12-14% moisture before storage",
            "Use hermetic storage for long-term storage",
            "Freeze wheat for 48 hours to kill insects",
            "Store in small batches"
        ],
        "best_practices": [
            "Clean storage area before use",
            "Elevate containers off the floor",
            "Use FIFO method",
            "Label with storage date"
        ]
    },
    "Cotton": {
        "storage_method": "Covered, dry warehouse",
        "ideal_temperature": "15-25°C",
        "ideal_humidity": "50-60%",
        "shelf_life": "1-2 years",
        "storage_tips": [
            "Store in a covered, dry warehouse",
            "Keep bales off the ground on pallets",
            "Maintain good ventilation",
            "Protect from direct sunlight",
            "Keep away from moisture sources"
        ],
        "spoilage_signs": [
            "Yellowing or discoloration",
            "Musty smell",
            "Mold growth",
            "Weak or damaged fibers"
        ],
        "prevention_tips": [
            "Dry cotton to 8-10% moisture before storage",
            "Use dehumidifiers in storage area",
            "Inspect bales regularly",
            "Store in breathable packaging"
        ],
        "best_practices": [
            "Clean warehouse before storage",
            "Use pallets to elevate bales",
            "Maintain proper ventilation",
            "Rotate stock regularly"
        ]
    },
    "Sugarcane": {
        "storage_method": "Process immediately or short-term storage",
        "ideal_temperature": "10-15°C",
        "ideal_humidity": "85-90%",
        "shelf_life": "24-48 hours (fresh), 6-12 months (jaggery/sugar)",
        "storage_tips": [
            "Process sugarcane as soon as possible after harvest",
            "If storing, keep in shaded, cool area",
            "Sprinkle water to maintain moisture",
            "Stack in criss-cross pattern for air circulation",
            "Cover with wet cloth or leaves"
        ],
        "spoilage_signs": [
            "Drying or wilting",
            "Fermentation smell",
            "Discoloration",
            "Soft or mushy texture"
        ],
        "prevention_tips": [
            "Harvest at optimal maturity",
            "Process within 24-48 hours",
            "Keep stalks upright to prevent drying",
            "Avoid bruising during handling"
        ],
        "best_practices": [
            "Plan processing schedule before harvest",
            "Clean processing equipment",
            "Store jaggery in airtight containers",
            "Keep sugar in dry, cool place"
        ]
    },
    "Maize": {
        "storage_method": "Airtight containers or cribs",
        "ideal_temperature": "15-20°C",
        "ideal_humidity": "12-14%",
        "shelf_life": "6-12 months",
        "storage_tips": [
            "Dry maize to 12-14% moisture before storage",
            "Store in airtight containers or cribs",
            "Keep in a cool, dry place",
            "Use moisture absorbers",
            "Check regularly for pests"
        ],
        "spoilage_signs": [
            "Musty smell",
            "Discoloration",
            "Insect infestation",
            "Mold growth"
        ],
        "prevention_tips": [
            "Dry thoroughly before storage",
            "Use hermetic storage bags",
            "Freeze for 48 hours to kill insects",
            "Store in small batches"
        ],
        "best_practices": [
            "Clean storage area",
            "Elevate containers",
            "Use FIFO method",
            "Label with date"
        ]
    },
    "Vegetables": {
        "storage_method": "Refrigeration or cool storage",
        "ideal_temperature": "4-10°C (varies by vegetable)",
        "ideal_humidity": "90-95%",
        "shelf_life": "1-4 weeks (varies)",
        "storage_tips": [
            "Store most vegetables in refrigerator",
            "Keep in perforated plastic bags",
            "Store potatoes, onions, garlic in cool, dark place",
            "Don't wash before storing (except leafy greens)",
            "Separate ethylene-producing fruits from vegetables"
        ],
        "spoilage_signs": [
            "Wilting or softening",
            "Discoloration",
            "Off smell",
            "Mold growth"
        ],
        "prevention_tips": [
            "Harvest at optimal maturity",
            "Cool vegetables quickly after harvest",
            "Handle gently to avoid bruising",
            "Store at correct temperature"
        ],
        "best_practices": [
            "Clean storage area regularly",
            "Check stored vegetables daily",
            "Use older vegetables first",
            "Don't store damaged produce"
        ]
    },
    "Pulses": {
        "storage_method": "Airtight containers",
        "ideal_temperature": "15-20°C",
        "ideal_humidity": "12-14%",
        "shelf_life": "6-12 months",
        "storage_tips": [
            "Store in airtight containers",
            "Keep in a cool, dry place",
            "Use moisture absorbers",
            "Check regularly for insects",
            "Avoid storing near strong odors"
        ],
        "spoilage_signs": [
            "Musty smell",
            "Discoloration",
            "Insect infestation",
            "Clumping"
        ],
        "prevention_tips": [
            "Dry pulses to 12-14% moisture",
            "Use hermetic storage",
            "Freeze for 48 hours to kill insects",
            "Store in small batches"
        ],
        "best_practices": [
            "Clean storage area",
            "Elevate containers",
            "Use FIFO method",
            "Label with date"
        ]
    },
    "Ground Nuts": {
        "storage_method": "Airtight containers or bags",
        "ideal_temperature": "15-20°C",
        "ideal_humidity": "7-8%",
        "shelf_life": "3-6 months",
        "storage_tips": [
            "Store in airtight containers",
            "Keep in a cool, dry place",
            "Use moisture absorbers",
            "Check regularly for aflatoxin contamination",
            "Avoid storing near strong odors"
        ],
        "spoilage_signs": [
            "Rancid smell",
            "Discoloration",
            "Mold growth",
            "Bitter taste"
        ],
        "prevention_tips": [
            "Dry groundnuts to 7-8% moisture",
            "Store in cool, dry conditions",
            "Inspect regularly for mold",
            "Use within 3-6 months"
        ],
        "best_practices": [
            "Clean storage area",
            "Elevate containers",
            "Use FIFO method",
            "Label with date"
        ]
    },
    "Oil seeds": {
        "storage_method": "Airtight containers",
        "ideal_temperature": "15-20°C",
        "ideal_humidity": "8-10%",
        "shelf_life": "6-12 months",
        "storage_tips": [
            "Store in airtight containers",
            "Keep in a cool, dry place",
            "Use moisture absorbers",
            "Check regularly for pests",
            "Avoid storing near strong odors"
        ],
        "spoilage_signs": [
            "Rancid smell",
            "Discoloration",
            "Insect infestation",
            "Mold growth"
        ],
        "prevention_tips": [
            "Dry seeds to 8-10% moisture",
            "Use hermetic storage",
            "Freeze for 48 hours to kill insects",
            "Store in small batches"
        ],
        "best_practices": [
            "Clean storage area",
            "Elevate containers",
            "Use FIFO method",
            "Label with date"
        ]
    },
    "Tobacco": {
        "storage_method": "Curing and drying",
        "ideal_temperature": "20-30°C",
        "ideal_humidity": "65-75%",
        "shelf_life": "1-2 years (cured)",
        "storage_tips": [
            "Cure tobacco properly before storage",
            "Store in a cool, dry place",
            "Maintain proper humidity levels",
            "Protect from direct sunlight",
            "Use breathable packaging"
        ],
        "spoilage_signs": [
            "Mold growth",
            "Off smell",
            "Discoloration",
            "Brittle texture"
        ],
        "prevention_tips": [
            "Cure to proper moisture content",
            "Store in controlled environment",
            "Inspect regularly",
            "Use proper packaging"
        ],
        "best_practices": [
            "Clean storage area",
            "Maintain proper ventilation",
            "Monitor humidity levels",
            "Rotate stock"
        ]
    },
    "Barley": {
        "storage_method": "Airtight containers or silos",
        "ideal_temperature": "15-20°C",
        "ideal_humidity": "12-14%",
        "shelf_life": "6-12 months",
        "storage_tips": [
            "Store in airtight containers or silos",
            "Keep in a cool, dry place",
            "Use moisture absorbers",
            "Check regularly for pests",
            "Avoid storing near strong odors"
        ],
        "spoilage_signs": [
            "Musty smell",
            "Discoloration",
            "Insect infestation",
            "Mold growth"
        ],
        "prevention_tips": [
            "Dry barley to 12-14% moisture",
            "Use hermetic storage",
            "Freeze for 48 hours to kill insects",
            "Store in small batches"
        ],
        "best_practices": [
            "Clean storage area",
            "Elevate containers",
            "Use FIFO method",
            "Label with date"
        ]
    },
    "Millets": {
        "storage_method": "Airtight containers",
        "ideal_temperature": "15-20°C",
        "ideal_humidity": "12-14%",
        "shelf_life": "6-12 months",
        "storage_tips": [
            "Store in airtight containers",
            "Keep in a cool, dry place",
            "Use moisture absorbers",
            "Check regularly for pests",
            "Avoid storing near strong odors"
        ],
        "spoilage_signs": [
            "Musty smell",
            "Discoloration",
            "Insect infestation",
            "Clumping"
        ],
        "prevention_tips": [
            "Dry millets to 12-14% moisture",
            "Use hermetic storage",
            "Freeze for 48 hours to kill insects",
            "Store in small batches"
        ],
        "best_practices": [
            "Clean storage area",
            "Elevate containers",
            "Use FIFO method",
            "Label with date"
        ]
    },
    "Paddy": {
        "storage_method": "Airtight containers or bags",
        "ideal_temperature": "15-20°C",
        "ideal_humidity": "12-14%",
        "shelf_life": "6-12 months",
        "storage_tips": [
            "Store in airtight containers or bags",
            "Keep in a cool, dry place",
            "Use moisture absorbers",
            "Check regularly for insects",
            "Avoid storing near strong odors"
        ],
        "spoilage_signs": [
            "Musty smell",
            "Discoloration",
            "Insect infestation",
            "Clumping"
        ],
        "prevention_tips": [
            "Dry paddy to 12-14% moisture",
            "Use hermetic storage",
            "Freeze for 48 hours to kill insects",
            "Store in small batches"
        ],
        "best_practices": [
            "Clean storage area",
            "Elevate containers",
            "Use FIFO method",
            "Label with date"
        ]
    }
}


def get_all_crops() -> list:
    """Get list of all crops with storage data."""
    return list(CROP_STORAGE_DATA.keys())


def get_crop_storage_info(crop: str) -> dict:
    """Get storage information for a specific crop."""
    return CROP_STORAGE_DATA.get(crop, {})


def get_storage_summary(crop: str) -> dict:
    """
    Get comprehensive storage summary for a crop.
    
    Args:
        crop: Crop name
    
    Returns:
        dict: Storage summary
    """
    storage_info = get_crop_storage_info(crop)
    
    if not storage_info:
        return {
            "error": f"No storage information available for {crop}",
            "general_tips": [
                "Store in a cool, dry place",
                "Use airtight containers",
                "Check regularly for spoilage",
                "Maintain proper humidity levels"
            ]
        }
    
    return {
        "crop": crop,
        "storage_method": storage_info.get("storage_method", "Airtight containers"),
        "ideal_temperature": storage_info.get("ideal_temperature", "15-20°C"),
        "ideal_humidity": storage_info.get("ideal_humidity", "12-14%"),
        "shelf_life": storage_info.get("shelf_life", "6-12 months"),
        "storage_tips": storage_info.get("storage_tips", []),
        "spoilage_signs": storage_info.get("spoilage_signs", []),
        "prevention_tips": storage_info.get("prevention_tips", []),
        "best_practices": storage_info.get("best_practices", [])
    }


def get_general_storage_tips() -> dict:
    """Get general storage tips applicable to all crops."""
    return {
        "temperature_control": [
            "Store in a cool place (15-20°C for most crops)",
            "Avoid temperature fluctuations",
            "Use insulation for long-term storage",
            "Monitor temperature regularly"
        ],
        "humidity_control": [
            "Maintain optimal humidity for each crop",
            "Use moisture absorbers (silica gel, rice)",
            "Ensure good ventilation",
            "Use dehumidifiers if necessary"
        ],
        "pest_control": [
            "Clean storage area before use",
            "Inspect regularly for pests",
            "Use natural repellents (neem, cloves)",
            "Freeze grains before storage to kill insects"
        ],
        "container_selection": [
            "Use airtight containers for grains",
            "Use breathable bags for vegetables",
            "Elevate containers off the floor",
            "Label containers with date"
        ],
        "spoilage_prevention": [
            "Dry crops to optimal moisture before storage",
            "Store in small batches",
            "Use first-in-first-out (FIFO) method",
            "Check stored crops regularly"
        ]
    }


def get_spoilage_prevention_checklist(crop: str) -> dict:
    """
    Get a spoilage prevention checklist for a specific crop.
    
    Args:
        crop: Crop name
    
    Returns:
        dict: Prevention checklist
    """
    storage_info = get_crop_storage_info(crop)
    
    if not storage_info:
        return {
            "error": f"No information available for {crop}",
            "general_checklist": [
                "Dry crop to optimal moisture",
                "Store in airtight container",
                "Keep in cool, dry place",
                "Check regularly for spoilage"
            ]
        }
    
    checklist = []
    
    # Add prevention tips
    for tip in storage_info.get("prevention_tips", []):
        checklist.append({
            "task": tip,
            "completed": False
        })
    
    # Add best practices
    for practice in storage_info.get("best_practices", []):
        checklist.append({
            "task": practice,
            "completed": False
        })
    
    return {
        "crop": crop,
        "checklist": checklist,
        "ideal_conditions": {
            "temperature": storage_info.get("ideal_temperature", "15-20°C"),
            "humidity": storage_info.get("ideal_humidity", "12-14%"),
            "shelf_life": storage_info.get("shelf_life", "6-12 months")
        }
    }
