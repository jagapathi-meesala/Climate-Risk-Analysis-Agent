from typing import Any, Dict
from contracts.tool_contract import ToolContract

class CalculateFloodRiskTool:
    name = "calculate-flood-risk"
    description = "Calculate flood risk score."
    input_schema = {
        "type": "object",
        "properties": {
            "cumulative_rainfall": {"type": "number"},
            "drainage_capacity": {"type": "number"}
        },
        "required": ["cumulative_rainfall", "drainage_capacity"]
    }
    
    def validate_input(self, input_data: Dict[str, Any]) -> bool:
        if not isinstance(input_data, dict):
            return False
        for req in ["cumulative_rainfall", "drainage_capacity"]:
            if req not in input_data:
                return False
            if not isinstance(input_data[req], (int, float)):
                return False
            if input_data[req] < 0:
                return False
        
        if input_data.get("drainage_capacity", 0) <= 0:
            return False
            
        return True
        
    def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        rainfall = float(input_data["cumulative_rainfall"])
        capacity = float(input_data["drainage_capacity"])
        
        score = (rainfall / capacity) * 100
        category = "High" if score >= 100 else ("Medium" if score >= 75 else "Low")
        
        return {
            "flood_risk_score": score,
            "contributing_factors": {"cumulative_rainfall": rainfall, "drainage_capacity": capacity},
            "threshold_conditions": {"high": 100, "medium": 75},
            "risk_category": category,
            "calculation_explanation": "score = (cumulative_rainfall / drainage_capacity) * 100",
            "limitations": "Does not claim an actual flood is occurring. Only analyzes supplied structured indicators."
        }
