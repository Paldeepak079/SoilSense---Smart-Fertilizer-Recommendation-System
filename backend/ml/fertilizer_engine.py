"""
Fertilizer recommendation engine
Maps nutrient requirements to actual fertilizer products and quantities
"""
from typing import Dict, List, Tuple


class Fertilizer:
    """Fertilizer product specification"""
    def __init__(self, name: str, n_percent: float, p_percent: float, k_percent: float, cost_per_kg: float):
        self.name = name
        self.n_percent = n_percent / 100  # Convert to fraction
        self.p_percent = p_percent / 100
        self.k_percent = k_percent / 100
        self.cost_per_kg = cost_per_kg  # Cost in INR per kg


# Common fertilizers available in India
FERTILIZERS = [
    Fertilizer("Urea", n_percent=46, p_percent=0, k_percent=0, cost_per_kg=6),
    Fertilizer("DAP (Diammonium Phosphate)", n_percent=18, p_percent=46, k_percent=0, cost_per_kg=27),
    Fertilizer("MOP (Muriate of Potash)", n_percent=0, p_percent=0, k_percent=60, cost_per_kg=17),
    Fertilizer("SSP (Single Super Phosphate)", n_percent=0, p_percent=16, k_percent=0, cost_per_kg=8),
    Fertilizer("NPK 10-26-26", n_percent=10, p_percent=26, k_percent=26, cost_per_kg=22),
    Fertilizer("NPK 12-32-16", n_percent=12, p_percent=32, k_percent=16, cost_per_kg=24),
    Fertilizer("NPK 14-35-14", n_percent=14, p_percent=35, k_percent=14, cost_per_kg=25),
    Fertilizer("NPK 17-17-17", n_percent=17, p_percent=17, k_percent=17, cost_per_kg=20),
    Fertilizer("NPK 19-19-19", n_percent=19, p_percent=19, k_percent=19, cost_per_kg=21),
    Fertilizer("NPK 20-20-0-13", n_percent=20, p_percent=20, k_percent=0, cost_per_kg=18),
    Fertilizer("NPK 28-28-0", n_percent=28, p_percent=28, k_percent=0, cost_per_kg=23),
]


class FertilizerRecommendationEngine:
    """Generate fertilizer recommendations from nutrient requirements"""
    
    @staticmethod
    def recommend_fertilizers(
        required_n: float,
        required_p: float,
        required_k: float,
        field_area_hectares: float = 1.0
    ) -> Dict:
        """
        Recommend fertilizers based on nutrient requirements
        
        Args:
            required_n: Required nitrogen (kg/ha)
            required_p: Required phosphorus as P₂O₅ (kg/ha)
            required_k: Required potassium as K₂O (kg/ha)
            field_area_hectares: Field area in hectares
        
        Returns:
            Dictionary with fertilizer recommendations
        """
        # Strategy: Use combination of DAP/Urea/MOP for cost optimization
        # 1. Use DAP to meet phosphorus needs (also provides some N)
        # 2. Use MOP to meet potassium needs
        # 3. Use Urea to meet remaining nitrogen needs
        
        recommendations = []
        total_cost = 0
        
        n_remaining = required_n
        p_remaining = required_p
        k_remaining = required_k
        
        # Step 1: Use DAP for phosphorus (also satisfies some nitrogen)
        if p_remaining > 0:
            dap = next(f for f in FERTILIZERS if f.name.startswith("DAP"))
            dap_needed_kg = p_remaining / dap.p_percent
            n_from_dap = dap_needed_kg * dap.n_percent
            
            recommendations.append({
                "fertilizer": "DAP (Diammonium Phosphate)",
                "quantity_kg_per_hectare": round(dap_needed_kg, 2),
                "quantity_kg_per_acre": round(dap_needed_kg * 0.4047, 2),
                "quantity_total": round(dap_needed_kg * field_area_hectares, 2),
                "provides": f"{round(n_from_dap, 1)} kg N + {round(p_remaining, 1)} kg P₂O₅",
                "cost": round(dap_needed_kg * dap.cost_per_kg, 2)
            })
            
            total_cost += dap_needed_kg * dap.cost_per_kg
            n_remaining -= n_from_dap
            p_remaining = 0
        
        # Step 2: Use MOP for potassium
        if k_remaining > 0:
            mop = next(f for f in FERTILIZERS if f.name.startswith("MOP"))
            mop_needed_kg = k_remaining / mop.k_percent
            
            recommendations.append({
                "fertilizer": "MOP (Muriate of Potash)",
                "quantity_kg_per_hectare": round(mop_needed_kg, 2),
                "quantity_kg_per_acre": round(mop_needed_kg * 0.4047, 2),
                "quantity_total": round(mop_needed_kg * field_area_hectares, 2),
                "provides": f"{round(k_remaining, 1)} kg K₂O",
                "cost": round(mop_needed_kg * mop.cost_per_kg, 2)
            })
            
            total_cost += mop_needed_kg * mop.cost_per_kg
            k_remaining = 0
        
        # Step 3: Use Urea for remaining nitrogen
        if n_remaining > 0:
            urea = next(f for f in FERTILIZERS if f.name == "Urea")
            urea_needed_kg = n_remaining / urea.n_percent
            
            recommendations.append({
                "fertilizer": "Urea",
                "quantity_kg_per_hectare": round(urea_needed_kg, 2),
                "quantity_kg_per_acre": round(urea_needed_kg * 0.4047, 2),
                "quantity_total": round(urea_needed_kg * field_area_hectares, 2),
                "provides": f"{round(n_remaining, 1)} kg N",
                "cost": round(urea_needed_kg * urea.cost_per_kg, 2)
            })
            
            total_cost += urea_needed_kg * urea.cost_per_kg
            n_remaining = 0
        
        # Application timing and method
        application_timing = FertilizerRecommendationEngine._get_application_timing(required_n, required_p, required_k)
        application_method = FertilizerRecommendationEngine._get_application_method()
        
        return {
            "fertilizers": recommendations,
            "total_cost": round(total_cost, 2),
            "application_timing": application_timing,
            "application_method": application_method
        }
    
    @staticmethod
    def _get_application_timing(n: float, p: float, k: float) -> str:
        """Generate application timing guidance"""
        timing = []
        
        # Phosphorus and potassium are typically applied as basal dose
        if p > 0 or k > 0:
            timing.append("**Basal Application** (at sowing/planting): Apply all DAP and MOP")
        
        # Nitrogen is split between basal and top dressing
        if n > 0:
            timing.append("**Basal Application** (at sowing): 25-30% of Urea")
            timing.append("**First Top Dressing** (3-4 weeks after sowing): 35-40% of Urea")
            timing.append("**Second Top Dressing** (6-7 weeks after sowing): 30-35% of Urea")
        
        return " | ".join(timing)
    
    @staticmethod
    def _get_application_method() -> str:
        """Generate application method guidance"""
        method = """
**Application Methods:**
- **Broadcasting**: Spread fertilizer evenly before final plowing
- **Drilling**: Place fertilizer in rows 5-7 cm deep alongside seeds
- **Band Placement**: Apply in bands 5 cm away from plant rows
- **Top Dressing**: Broadcast nitrogen fertilizer and irrigate immediately

**Important Notes:**
- Apply fertilizers on moist soil
- Incorporate fertilizers into soil to prevent loss
- Avoid direct contact with seeds
- Irrigate after top dressing to activate nutrients
        """
        return method.strip()


def generate_recommendation_summary(fertilizer_data: Dict) -> str:
    """
    Generate a formatted summary of fertilizer recommendations
    """
    summary_parts = []
    
    summary_parts.append("### Fertilizer Recommendations\n")
    
    for i, fert in enumerate(fertilizer_data['fertilizers'], 1):
        summary_parts.append(f"**{i}. {fert['fertilizer']}**")
        summary_parts.append(f"   - Quantity: {fert['quantity_kg_per_hectare']} kg/hectare ({fert['quantity_kg_per_acre']} kg/acre)")
        summary_parts.append(f"   - Provides: {fert['provides']}")
        summary_parts.append(f"   - Cost: ₹{fert['cost']}\n")
    
    summary_parts.append(f"**Total Estimated Cost:** ₹{fertilizer_data['total_cost']}\n")
    summary_parts.append(f"**Application Timing:**\n{fertilizer_data['application_timing']}\n")
    summary_parts.append(f"**Application Method:**\n{fertilizer_data['application_method']}")
    
    return "\n".join(summary_parts)
