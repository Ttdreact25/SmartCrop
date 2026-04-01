"""
Organic Farming Suggestions Module for Smart Crop Recommendation System.
Provides natural fertilizers, organic alternatives, and composting tips.
"""

import json
import os
from datetime import datetime


# Natural fertilizers database
NATURAL_FERTILIZERS = {
    "Vermicompost": {
        "description": "Compost made using earthworms",
        "nutrients": "Rich in NPK, micronutrients",
        "application": "2-3 tons per acre",
        "benefits": [
            "Improves soil structure",
            "Enhances water retention",
            "Increases microbial activity",
            "Slow-release nutrients"
        ],
        "preparation": "Use earthworms (Eisenia fetida) in organic waste",
        "cost": "₹3,000 - ₹5,000 per ton"
    },
    "Neem Cake": {
        "description": "Residue after neem oil extraction",
        "nutrients": "High in NPK, azadirachtin",
        "application": "200-300 kg per acre",
        "benefits": [
            "Natural pest repellent",git init
            "Improves soil fertility",
            "Controls nematodes",
            "Slow nitrogen release"
                        ],
        "preparation": "Available commercially",
        "cost": "₹40 - ₹60 per kg"
    },
    "Bone Meal": {
        "description": "Crushed animal bones",
        "nutrients": "High in phosphorus, calcium",
        "application": "100-200 kg per acre",
        "benefits": [
            "Promotes root development",
            "Improves flowering",
            "Long-lasting effect",
            "Natural source of phosphorus"
        ],
        "preparation": "Sterilize and crush bones",
        "cost": "₹30 - ₹50 per kg"
    },
    "Fish Meal": {
        "description": "Ground dried fish",
        "nutrients": "Rich in nitrogen, phosphorus",
        "application": "100-150 kg per acre",
        "benefits": [
            "Fast-acting nitrogen",
            "Improves soil biology",
            "Enhances plant growth",
            "Good for leafy vegetables"
        ],
        "preparation": "Dry and grind fish waste",
        "cost": "₹50 - ₹80 per kg"
    },
    "Wood Ash": {
        "description": "Ash from burned wood",
        "nutrients": "High in potassium, calcium",
        "application": "50-100 kg per acre",
        "benefits": [
            "Raises soil pH",
            "Provides potassium",
            "Deters slugs and snails",
            "Free and readily available"
        ],
        "preparation": "Collect from clean wood burning",
        "cost": "Free - ₹10 per kg"
    },
    "Compost Tea": {
        "description": "Liquid extract from compost",
        "nutrients": "Balanced NPK, beneficial microbes",
        "application": "Foliar spray or soil drench",
        "benefits": [
            "Fast nutrient uptake",
            "Improves plant immunity",
            "Enhances soil biology",
            "Easy to apply"
        ],
        "preparation": "Steep compost in water for 24-48 hours",
        "cost": "₹50 - ₹100 per liter"
    },
    "Green Manure": {
        "description": "Plants grown and plowed into soil",
        "nutrients": "Nitrogen, organic matter",
        "application": "Grow for 45-60 days, then incorporate",
        "benefits": [
            "Adds organic matter",
            "Fixes nitrogen (legumes)",
            "Prevents erosion",
            "Improves soil structure"
        ],
        "preparation": "Grow dhaincha, sunhemp, or cowpea",
        "cost": "₹200 - ₹500 per acre (seeds)"
    },
    "Jeevamrut": {
        "description": "Traditional Indian organic fertilizer",
        "nutrients": "Beneficial microbes, nutrients",
        "application": "200 liters per acre",
        "benefits": [
            "Enhances soil biology",
            "Cost-effective",
            "Easy to prepare",
            "Traditional wisdom"
        ],
        "preparation": "Mix cow dung, cow urine, jaggery, pulse flour, water",
        "cost": "₹50 - ₹100 per batch"
    },
    "Panchagavya": {
        "description": "Five products from cow",
        "nutrients": "Growth hormones, nutrients",
        "application": "3% spray solution",
        "benefits": [
            "Growth promoter",
            "Pest deterrent",
            "Improves yield",
            "Traditional organic solution"
        ],
        "preparation": "Mix cow dung, cow urine, milk, curd, ghee",
        "cost": "₹100 - ₹200 per liter"
    },
    "Biofertilizers": {
        "description": "Living microorganisms",
        "nutrients": "Nitrogen fixers, phosphate solubilizers",
        "application": "Seed treatment or soil application",
        "benefits": [
            "Fix atmospheric nitrogen",
            "Solubilize phosphorus",
            "Improve nutrient uptake",
            "Eco-friendly"
        ],
        "preparation": "Available commercially (Rhizobium, Azotobacter, PSB)",
        "cost": "₹100 - ₹300 per packet"
    }
}

# Organic alternatives to chemical pesticides
ORGANIC_PESTICIDES = {
    "Neem Oil": {
        "description": "Extract from neem seeds",
        "targets": "Aphids, whiteflies, mealybugs",
        "preparation": "Mix 2-3 ml neem oil per liter water",
        "application": "Spray in evening, repeat weekly",
        "safety": "Safe for humans, toxic to pests"
    },
    "Garlic Spray": {
        "description": "Garlic-based insect repellent",
        "targets": "Aphids, beetles, caterpillars",
        "preparation": "Blend 100g garlic in 1 liter water, strain",
        "application": "Spray on affected plants",
        "safety": "Strong smell, use sparingly"
    },
    "Chili Spray": {
        "description": "Hot pepper extract",
        "targets": "Ants, aphids, caterpillars",
        "preparation": "Blend 100g chili in 1 liter water",
        "application": "Spray on plants, avoid contact with eyes",
        "safety": "Irritating, use protective gear"
    },
    "Tobacco Decoction": {
        "description": "Tobacco leaf extract",
        "targets": "Aphids, thrips, whiteflies",
        "preparation": "Soak 100g tobacco in 1 liter water overnight",
        "application": "Dilute and spray",
        "safety": "Toxic, use with caution"
    },
    "Turmeric Powder": {
        "description": "Antifungal and antibacterial",
        "targets": "Fungal diseases, bacterial infections",
        "preparation": "Mix 10g turmeric in 1 liter water",
        "application": "Spray on affected areas",
        "safety": "Safe, may stain"
    },
    "Cow Urine": {
        "description": "Natural pest deterrent",
        "targets": "Various insects, fungal diseases",
        "preparation": "Dilute 1:10 with water",
        "application": "Spray on plants",
        "safety": "Safe, traditional method"
    },
    "Baking Soda": {
        "description": "Fungicide alternative",
        "targets": "Powdery mildew, black spot",
        "preparation": "Mix 1 tsp per liter water",
        "application": "Spray on affected leaves",
        "safety": "Safe, may affect soil pH"
    },
    "Diatomaceous Earth": {
        "description": "Fossilized algae",
        "targets": "Slugs, snails, crawling insects",
        "preparation": "Dust around plants",
        "application": "Apply when dry",
        "safety": "Safe, avoid inhaling dust"
    }
}

# Composting tips
COMPOSTING_TIPS = {
    "Basic Composting": {
        "materials": [
            "Kitchen scraps (vegetable peels, fruit waste)",
            "Garden waste (leaves, grass clippings)",
            "Cardboard, paper",
            "Cow dung or manure"
        ],
        "steps": [
            "Choose a shady spot",
            "Layer brown and green materials",
            "Keep moist but not wet",
            "Turn every 2-3 weeks",
            "Ready in 3-6 months"
        ],
        "tips": [
            "Maintain 3:1 brown to green ratio",
            "Avoid meat, dairy, oily foods",
            "Chop materials for faster decomposition",
            "Cover to retain moisture"
        ]
    },
    "Vermicomposting": {
        "materials": [
            "Red wiggler worms (Eisenia fetida)",
            "Organic waste (no citrus, onions)",
            "Bedding (newspaper, cardboard)",
            "Shallow container"
        ],
        "steps": [
            "Prepare bedding with moist newspaper",
            "Add worms (1 kg per square foot)",
            "Feed with kitchen scraps",
            "Harvest castings after 2-3 months",
            "Use worm tea as liquid fertilizer"
        ],
        "tips": [
            "Keep in shade, 15-25°C",
            "Avoid overfeeding",
            "Maintain moisture like wrung sponge",
            "Harvest from bottom"
        ]
    },
    "Bokashi Composting": {
        "materials": [
            "Bokashi bran (EM inoculant)",
            "Airtight bucket",
            "Kitchen scraps (including meat, dairy)",
            "Drainage spigot"
        ],
        "steps": [
            "Add scraps to bucket",
            "Sprinkle bokashi bran",
            "Press down to remove air",
            "Drain liquid every 2 days",
            "Bury in soil after 2 weeks"
        ],
        "tips": [
            "Works anaerobically",
            "Ferments rather than decomposes",
            "Can handle all food waste",
            "Use bokashi tea as fertilizer"
        ]
    },
    "Pit Composting": {
        "materials": [
            "Dig a pit (3x3x3 feet)",
            "Organic waste",
            "Soil",
            "Water"
        ],
        "steps": [
            "Dig pit in garden",
            "Layer waste with soil",
            "Keep moist",
            "Cover with plastic sheet",
            "Ready in 4-6 months"
        ],
        "tips": [
            "Good for large quantities",
            "Add cow dung for faster decomposition",
            "Turn occasionally",
            "Use in same location next season"
        ]
    }
}

# Crop-specific organic recommendations
CROP_ORGANIC_RECOMMENDATIONS = {
    "Rice": {
        "fertilizers": ["Vermicompost", "Green Manure", "Jeevamrut"],
        "pesticides": ["Neem Oil", "Chili Spray"],
        "tips": [
            "Use azolla as green manure in paddy fields",
            "Apply neem cake to prevent stem borer",
            "Use fish meal for nitrogen boost"
        ]
    },
    "Wheat": {
        "fertilizers": ["Vermicompost", "Bone Meal", "Biofertilizers"],
        "pesticides": ["Neem Oil", "Garlic Spray"],
        "tips": [
            "Apply bone meal for root development",
            "Use PSB for phosphorus solubilization",
            "Spray neem oil for aphid control"
        ]
    },
    "Cotton": {
        "fertilizers": ["Neem Cake", "Vermicompost", "Panchagavya"],
        "pesticides": ["Neem Oil", "Tobacco Decoction"],
        "tips": [
            "Neem cake controls bollworm",
            "Apply vermicompost at flowering",
            "Use panchagavya as growth promoter"
        ]
    },
    "Vegetables": {
        "fertilizers": ["Vermicompost", "Compost Tea", "Biofertilizers"],
        "pesticides": ["Neem Oil", "Garlic Spray", "Chili Spray"],
        "tips": [
            "Use compost tea for foliar feeding",
            "Apply vermicompost every 2 weeks",
            "Rotate crops to prevent disease"
        ]
    },
    "Sugarcane": {
        "fertilizers": ["Vermicompost", "Press Mud", "Jeevamrut"],
        "pesticides": ["Neem Oil", "Chili Spray"],
        "tips": [
            "Use press mud from sugar mills",
            "Apply jeevamrut monthly",
            "Trash mulching for moisture retention"
        ]
    }
}


def get_all_natural_fertilizers() -> list:
    """Get list of all natural fertilizers."""
    return list(NATURAL_FERTILIZERS.keys())


def get_fertilizer_details(fertilizer_name: str) -> dict:
    """Get details of a specific natural fertilizer."""
    return NATURAL_FERTILIZERS.get(fertilizer_name, {})


def get_all_organic_pesticides() -> list:
    """Get list of all organic pesticides."""
    return list(ORGANIC_PESTICIDES.keys())


def get_pesticide_details(pesticide_name: str) -> dict:
    """Get details of a specific organic pesticide."""
    return ORGANIC_PESTICIDES.get(pesticide_name, {})


def get_composting_tips(method: str = None) -> dict:
    """Get composting tips for a specific method or all methods."""
    if method:
        return COMPOSTING_TIPS.get(method, {})
    return COMPOSTING_TIPS


def get_crop_organic_recommendations(crop: str) -> dict:
    """Get organic farming recommendations for a specific crop."""
    return CROP_ORGANIC_RECOMMENDATIONS.get(crop, {
        "fertilizers": ["Vermicompost", "Compost Tea"],
        "pesticides": ["Neem Oil", "Garlic Spray"],
        "tips": [
            "Use vermicompost as base fertilizer",
            "Apply neem oil for pest control",
            "Practice crop rotation"
        ]
    })


def get_all_crops() -> list:
    """Get list of all crops with organic recommendations."""
    return list(CROP_ORGANIC_RECOMMENDATIONS.keys())


def get_organic_farming_summary(crop: str) -> dict:
    """Get comprehensive organic farming summary for a crop."""
    crop_rec = get_crop_organic_recommendations(crop)
    
    fertilizer_details = []
    for fert in crop_rec["fertilizers"]:
        details = get_fertilizer_details(fert)
        if details:
            fertilizer_details.append({
                "name": fert,
                "description": details.get("description", ""),
                "application": details.get("application", ""),
                "cost": details.get("cost", "")
            })
    
    pesticide_details = []
    for pest in crop_rec["pesticides"]:
        details = get_pesticide_details(pest)
        if details:
            pesticide_details.append({
                "name": pest,
                "description": details.get("description", ""),
                "targets": details.get("targets", ""),
                "preparation": details.get("preparation", "")
            })
    
    return {
        "crop": crop,
        "fertilizers": fertilizer_details,
        "pesticides": pesticide_details,
        "tips": crop_rec["tips"]
    }
