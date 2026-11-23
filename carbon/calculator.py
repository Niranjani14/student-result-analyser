"""Carbon Footprint Calculator Module.

Provides accurate CO2e emissions calculations based on user lifestyle inputs.
All values in kg CO2e per unit (see EMISSION_FACTORS documentation).
"""

from typing import Dict, Any

# Standard emission factors (kg CO2e per unit)
EMISSION_FACTORS: Dict[str, Dict[str, float]] = {
    # Transport (per km)
    "transport": {
        "petrol_car": 0.170,     # 170g per km
        "diesel_car": 0.171,     # 171g per km
        "hybrid_car": 0.100,     # 100g per km
        "electric_car": 0.050,    # 50g per km (average grid mix)
        "bus": 0.080,             # 80g per km
        "train": 0.040,           # 40g per km
        "motorbike": 0.110        # 110g per km
    },
    # Flights (per round-trip flight)
    "flights": {
        "short_haul": 250.0,     # Average short-haul flight (~250kg CO2e)
        "long_haul": 1500.0      # Average long-haul flight (~1500kg CO2e)
    },
    # Home Energy
    "energy": {
        "electricity_kwh": 0.38, # ~380g CO2e/kWh
        "gas_kwh": 0.18          # ~180g CO2e/kWh
    },
    # Diet (per year based on category)
    "diet": {
        "heavy_meat": 2800.0,    # High meat eater
        "medium_meat": 2000.0,   # Average meat eater
        "low_meat": 1500.0,      # Flexitarian
        "pescatarian": 1300.0,
        "vegetarian": 1100.0,
        "vegan": 800.0
    },
    # Waste (per person per year based on recycling)
    "waste": {
        "no_recycling": 600.0,   # Sends everything to landfill
        "partial_recycling": 350.0,
        "full_recycling": 150.0
    }
}

# Average annual footprint references for comparison (in kg CO2e)
AVERAGE_FOOTPRINTS: Dict[str, float] = {
    "US": 16000.0,
    "Europe": 7000.0,
    "Global": 4500.0,
    "Target": 2000.0
}

# Input validation limits (prevent abuse and errors)
INPUT_LIMITS: Dict[str, tuple] = {
    "car_dist": (0, 100000),           # km/year
    "public_bus": (0, 100000),         # km/year
    "public_train": (0, 100000),       # km/year
    "flights_short": (0, 365),         # flights/year
    "flights_long": (0, 365),          # flights/year
    "electricity": (0, 10000),         # kWh/month
    "gas": (0, 10000)                  # kWh/month
}

def _safe_float(value: Any, default: float = 0.0, min_val: float = 0.0, max_val: float = float('inf')) -> float:
    """Safely convert input to float with bounds checking."""
    try:
        result = float(value) if value else default
        return max(min_val, min(result, max_val))
    except (ValueError, TypeError):
        return default

def calculate_footprint(form_data: Dict[str, Any]) -> Dict[str, Any]:
    """Calculate annual carbon footprint in kg CO2e based on user inputs.
    
    Args:
        form_data: Dictionary containing user lifestyle inputs.
        
    Returns:
        Dictionary with 'total' (float) and 'categories' (dict of category breakdowns).
        
    Raises:
        ValueError: If form_data is None or empty.
    """
    if not form_data:
        raise ValueError("Form data cannot be empty")
    # 1. Transport calculations
    car_type = form_data.get("car_type", "none")
    car_dist = max(0.0, float(form_data.get("car_dist", 0.0)))
    public_bus = max(0.0, float(form_data.get("public_bus", 0.0)))
    public_train = max(0.0, float(form_data.get("public_train", 0.0)))

    transport_co2 = 0.0
    if car_type != "none" and car_type in EMISSION_FACTORS["transport"]:
        transport_co2 += car_dist * EMISSION_FACTORS["transport"][car_type]
    
    transport_co2 += public_bus * EMISSION_FACTORS["transport"]["bus"]
    transport_co2 += public_train * EMISSION_FACTORS["transport"]["train"]

    # 2. Flight calculations
    flights_short = max(0.0, float(form_data.get("flights_short", 0.0)))
    flights_long = max(0.0, float(form_data.get("flights_long", 0.0)))
    
    flight_co2 = (flights_short * EMISSION_FACTORS["flights"]["short_haul"]) + \
                 (flights_long * EMISSION_FACTORS["flights"]["long_haul"])

    total_transport = transport_co2 + flight_co2

    # 3. Home Energy calculations
    electricity_kwh = max(0.0, float(form_data.get("electricity", 0.0))) * 12.0 # monthly to annual
    gas_kwh = max(0.0, float(form_data.get("gas", 0.0))) * 12.0
    
    energy_co2 = (electricity_kwh * EMISSION_FACTORS["energy"]["electricity_kwh"]) + \
                 (gas_kwh * EMISSION_FACTORS["energy"]["gas_kwh"])

    # 4. Diet & Waste
    diet_type = form_data.get("diet_type", "medium_meat")
    diet_co2 = EMISSION_FACTORS["diet"].get(diet_type, 2000.0)

    recycling_type = form_data.get("recycling", "partial_recycling")
    waste_co2 = EMISSION_FACTORS["waste"].get(recycling_type, 350.0)

    # Combined total in kg CO2e
    total_co2 = total_transport + energy_co2 + diet_co2 + waste_co2

    return {
        "total": round(total_co2, 1),
        "categories": {
            "transport": round(total_transport, 1),
            "energy": round(energy_co2, 1),
            "diet": round(diet_co2, 1),
            "waste": round(waste_co2, 1)
        }
    }
