"""
Government of India Fertilizer Pricing Data
Source: Department of Fertilizers, Ministry of Chemicals and Fertilizers
Last Updated: December 2024 (Estimates based on Nutrient Based Subsidy Scheme)
"""

FERTILIZER_PRICES_INR = {
    # Fertilizer prices per 50kg bag (approximate retail prices as of Dec 2024)
    # Source: Department of Fertilizers NBS Scheme + Market Retail Prices
    
    "Urea": {
        "price_per_50kg": 266,  # Controlled price by Govt
        "npk_composition": "46-0-0",
        "nitrogen_percent": 46,
        "phosphorus_percent": 0,
        "potassium_percent": 0,
    },
    "DAP": {
        "price_per_50kg": 1350,  # Market price with subsidy
        "npk_composition": "18-46-0",
        "nitrogen_percent": 18,
        "phosphorus_percent": 46,
        "potassium_percent": 0,
    },
    "MOP": {
        "price_per_50kg": 1700,  # Muriate of Potash
        "npk_composition": "0-0-60",
        "nitrogen_percent": 0,
        "phosphorus_percent": 0,
        "potassium_percent": 60,
    },
    "NPK 10:26:26": {
        "price_per_50kg": 1450,
        "npk_composition": "10-26-26",
        "nitrogen_percent": 10,
        "phosphorus_percent": 26,
        "potassium_percent": 26,
    },
    "NPK 12:32:16": {
        "price_per_50kg": 1500,
        "npk_composition": "12-32-16",
        "nitrogen_percent": 12,
        "phosphorus_percent": 32,
        "potassium_percent": 16,
    },
    "NPK 17:17:17": {
        "price_per_50kg": 1425,
        "npk_composition": "17-17-17",
        "nitrogen_percent": 17,
        "phosphorus_percent": 17,
        "potassium_percent": 17,
    },
    "NPK 20:20:0:13": {
        "price_per_50kg": 1200,
        "npk_composition": "20-20-0-13",  # With Sulphur
        "nitrogen_percent": 20,
        "phosphorus_percent": 20,
        "potassium_percent": 0,
    },
    "SSP": {  # Single Super Phosphate
        "price_per_50kg": 450,
        "npk_composition": "0-16-0",
        "nitrogen_percent": 0,
        "phosphorus_percent": 16,
        "potassium_percent": 0,
    },
}

# Price verification metadata
PRICE_SOURCE = {
    "authority": "Department of Fertilizers, Ministry of Chemicals and Fertilizers, Government of India",
    "scheme": "Nutrient Based Subsidy (NBS) Scheme",
    "last_updated": "December 2024",
    "note": "Prices are indicative retail prices including subsidies and may vary by state and dealer. Urea price is controlled by Government.",
    "official_website": "https://fert.nic.in/",
}
