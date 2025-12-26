"""
State-wise fertilizer prices (Government NBS Scheme)
Prices vary by state subsidy and dealer margins
"""

# State-wise prices per 50kg bag (₹)
STATE_PRICES = {
    'Maharashtra': {
        'Urea': 266,
        'DAP': 1350,
        'MOP': 1700,
        'NPK': 1450,
    },
    'Punjab': {
        'Urea': 268,
        'DAP': 1360,
        'MOP': 1720,
        'NPK': 1460,
    },
    'Haryana': {
        'Urea': 267,
        'DAP': 1355,
        'MOP': 1710,
        'NPK': 1455,
    },
    'Uttar Pradesh': {
        'Urea': 265,
        'DAP': 1345,
        'MOP': 1695,
        'NPK': 1445,
    },
    'Madhya Pradesh': {
        'Urea': 266,
        'DAP': 1350,
        'MOP': 1700,
        'NPK': 1450,
    },
    'Karnataka': {
        'Urea': 270,
        'DAP': 1365,
        'MOP': 1730,
        'NPK': 1470,
    },
    'Tamil Nadu': {
        'Urea': 268,
        'DAP': 1358,
        'MOP': 1715,
        'NPK': 1460,
    },
    'Andhra Pradesh': {
        'Urea': 269,
        'DAP': 1360,
        'MOP': 1720,
        'NPK': 1465,
    },
    'Telangana': {
        'Urea': 269,
        'DAP': 1360,
        'MOP': 1720,
        'NPK': 1465,
    },
    'Gujarat': {
        'Urea': 267,
        'DAP': 1355,
        'MOP': 1710,
        'NPK': 1455,
    },
    'Rajasthan': {
        'Urea': 266,
        'DAP': 1350,
        'MOP': 1705,
        'NPK': 1450,
    },
    'West Bengal': {
        'Urea': 268,
        'DAP': 1358,
        'MOP': 1715,
        'NPK': 1460,
    },
    'Bihar': {
        'Urea': 265,
        'DAP': 1345,
        'MOP': 1695,
        'NPK': 1445,
    },
    'Odisha': {
        'Urea': 268,
        'DAP': 1358,
        'MOP': 1715,
        'NPK': 1460,
    },
    'Kerala': {
        'Urea': 272,
        'DAP': 1370,
        'MOP': 1735,
        'NPK': 1475,
    },
}

# National average (fallback if state not found)
NATIONAL_PRICES = {
    'Urea': 266,
    'DAP': 1350,
    'MOP': 1700,
    'NPK': 1450,
}


def get_fertilizer_price(fertilizer_name: str, state: str = None) -> int:
    """
    Get state-specific fertilizer price per 50kg bag
    
    Args:
        fertilizer_name: Name of fertilizer (Urea, DAP, MOP, NPK)
        state: State name
    
    Returns:
        Price per 50kg bag in rupees
    """
    if state and state in STATE_PRICES:
        return STATE_PRICES[state].get(fertilizer_name, NATIONAL_PRICES.get(fertilizer_name, 1450))
    
    return NATIONAL_PRICES.get(fertilizer_name, 1450)


def get_all_states():
    """Get list of all states with pricing data"""
    return sorted(STATE_PRICES.keys())
