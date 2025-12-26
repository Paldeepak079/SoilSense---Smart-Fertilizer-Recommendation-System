"""
Crop-specific Application Schedules
Provides fertilizer application timing based on crop growth stages
"""
from typing import Dict, List


def get_application_schedule(crop_name: str, total_n: float, total_p: float, total_k: float) -> List[Dict]:
    """
    Get fertilizer application schedule for specific crop
    
    Returns:
        List of application stages with timing, fertilizer, and quantity percentage
    """
    crop_lower = crop_name.lower()
    
    # Crop-specific schedules
    if 'rice' in crop_lower or 'paddy' in crop_lower:
        return get_rice_schedule()
    elif 'wheat' in crop_lower:
        return get_wheat_schedule()
    elif 'maize' in crop_lower or 'corn' in crop_lower:
        return get_maize_schedule()
    elif 'cotton' in crop_lower:
        return get_cotton_schedule()
    elif 'sugarcane' in crop_lower:
        return get_sugarcane_schedule()
    elif 'potato' in crop_lower:
        return get_potato_schedule()
    elif 'tomato' in crop_lower:
        return get_tomato_schedule()
    else:
        # Default schedule for general crops
        return get_default_schedule()


def get_rice_schedule() -> List[Dict]:
    """Rice/Paddy application schedule"""
    return [
        {
            'stage': 'Basal (At transplanting)',
            'time': 'Day 0',
            'fertilizer': 'DAP + MOP',
            'quantity_percent': 100,  # All P and K
            'note': 'Apply 1 day before transplanting'
        },
        {
            'stage': 'First Top Dressing',
            'time': '20-25 days after transplanting',
            'fertilizer': 'Urea',
            'quantity_percent': 50,  # 50% of N
            'note': 'Apply during active tillering stage'
        },
        {
            'stage': 'Second Top Dressing',
            'time': '40-45 days after transplanting',
            'fertilizer': 'Urea',
            'quantity_percent': 50,  # Remaining 50% of N
            'note': 'Apply before panicle initiation'
        }
    ]


def get_wheat_schedule() -> List[Dict]:
    """Wheat application schedule"""
    return [
        {
            'stage': 'Basal (At sowing)',
            'time': 'Day 0',
            'fertilizer': 'DAP + MOP + Urea (33%)',
            'quantity_percent': 33,
            'note': 'Apply with seed drill or broadcast before sowing'
        },
        {
            'stage': 'Crown Root Initiation',
            'time': '21 days after sowing',
            'fertilizer': 'Urea',
            'quantity_percent': 33,
            'note': 'First irrigation + fertilizer application'
        },
        {
            'stage': 'Late Jointing/Booting',
            'time': '40-45 days after sowing',
            'fertilizer': 'Urea',
            'quantity_percent': 34,
            'note': 'Second irrigation + final N application'
        }
    ]


def get_maize_schedule() -> List[Dict]:
    """Maize/Corn application schedule"""
    return [
        {
            'stage': 'Basal (At sowing)',
            'time': 'Day 0',
            'fertilizer': 'DAP + MOP',
            'quantity_percent': 100,  # All P and K
            'note': 'Apply 5-7cm below and beside seed'
        },
        {
            'stage': 'Knee-High Stage',
            'time': '25-30 days after sowing',
            'fertilizer': 'Urea',
            'quantity_percent': 50,
            'note': 'Side dress before first irrigation'
        },
        {
            'stage': 'Pre-Tasseling',
            'time': '45-50 days after sowing',
            'fertilizer': 'Urea',
            'quantity_percent': 50,
            'note': 'Apply before flowering for good cob development'
        }
    ]


def get_cotton_schedule() -> List[Dict]:
    """Cotton application schedule"""
    return [
        {
            'stage': 'Basal (At sowing)',
            'time': 'Day 0',
            'fertilizer': 'DAP + MOP + Urea (25%)',
            'quantity_percent': 25,
            'note': 'Apply in furrows before sowing'
        },
        {
            'stage': 'Square Formation',
            'time': '30-35 days after sowing',
            'fertilizer': 'Urea',
            'quantity_percent': 37.5,
            'note': 'Apply with first irrigation'
        },
        {
            'stage': 'Flowering Stage',
            'time': '60-65 days after sowing',
            'fertilizer': 'Urea',
            'quantity_percent': 37.5,
            'note': 'Apply during peak flowering'
        }
    ]


def get_sugarcane_schedule() -> List[Dict]:
    """Sugarcane application schedule"""
    return [
        {
            'stage': 'Basal (At planting)',
            'time': 'Day 0',
            'fertilizer': 'DAP + MOP',
            'quantity_percent': 100,  # All P and K
            'note': 'Apply in furrows, mix with soil'
        },
        {
            'stage': 'Tillering Stage',
            'time': '30-40 days after planting',
            'fertilizer': 'Urea',
            'quantity_percent': 50,
            'note': 'Apply and earthing up'
        },
        {
            'stage': 'Grand Growth',
            'time': '90-120 days after planting',
            'fertilizer': 'Urea',
            'quantity_percent': 50,
            'note': 'Apply before rapid cane elongation'
        }
    ]


def get_potato_schedule() -> List[Dict]:
    """Potato application schedule"""
    return [
        {
            'stage': 'Basal (At planting)',
            'time': 'Day 0',
            'fertilizer': 'DAP + MOP + Urea (33%)',
            'quantity_percent': 33,
            'note': 'Apply in furrows, cover with soil'
        },
        {
            'stage': 'Earthing Up',
            'time': '25-30 days after planting',
            'fertilizer': 'Urea',
            'quantity_percent': 33,
            'note': 'Apply and earth up ridges'
        },
        {
            'stage': 'Tuber Bulking',
            'time': '45-50 days after planting',
            'fertilizer': 'Urea + MOP',
            'quantity_percent': 34,
            'note': 'Final application for tuber development'
        }
    ]


def get_tomato_schedule() -> List[Dict]:
    """Tomato application schedule"""
    return [
        {
            'stage': 'Basal (Before transplanting)',
            'time': 'Day -1',
            'fertilizer': 'DAP + MOP',
            'quantity_percent': 100,
            'note': 'Apply and incorporate into beds'
        },
        {
            'stage': 'Vegetative Growth',
            'time': '15-20 days after transplanting',
            'fertilizer': 'Urea',
            'quantity_percent': 33,
            'note': 'Apply around plants, avoid stem contact'
        },
        {
            'stage': 'Flowering & Fruiting',
            'time': '35-40 days after transplanting',
            'fertilizer': 'Urea',
            'quantity_percent': 67,
            'note': 'Split into 2 applications during fruit development'
        }
    ]


def get_default_schedule() -> List[Dict]:
    """Default schedule for crops not specifically listed"""
    return [
        {
            'stage': 'Basal (At sowing/planting)',
            'time': 'Day 0',
            'fertilizer': 'DAP + MOP',
            'quantity_percent': 100,  # All P and K at basal
            'note': 'Apply before or at planting'
        },
        {
            'stage': 'First Top Dressing',
            'time': '3-4 weeks after planting',
            'fertilizer': 'Urea',
            'quantity_percent': 50,  # 50% of N
            'note': 'Apply during active vegetative growth'
        },
        {
            'stage': 'Second Top Dressing',
            'time': '6-7 weeks after planting',
            'fertilizer': 'Urea',
            'quantity_percent': 50,  # Remaining 50% of N
            'note': 'Apply before flowering/fruiting'
        }
    ]
