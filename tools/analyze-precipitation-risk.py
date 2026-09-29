from typing import Any, Dict
from contracts.tool_contract import ToolContract

class AnalyzePrecipitationRiskTool:
    name = "analyze-precipitation-risk"
    description = "Calculate deterministic precipitation indicators."
    input_schema = {
        "type": "object",
        "properties": {
            "location_id": {"type": "string"},
            "observed_precipitation": {"type": "number"},
            "historical_precipitation": {"type": "number"},
            "precipitation_threshold": {"type": "number"}
        },
        "required": ["location_id", "observed_precipitation", "historical_precipitation"]
    }
    
    def validate_input(self, input_data: Dict[str, Any]) -> bool:
        if not isinstance(input_data, dict):
            return False
        for req in ["location_id", "observed_precipitation", "historical_precipitation"]:
            if req not in input_data:
                return False
        if not isinstance(input_data["observed_precipitation"], (int, float)):
            return False
        if not isinstance(input_data["historical_precipitation"], (int, float)):
            return False
        if input_data["observed_precipitation"] < 0 or input_data["historical_precipitation"] < 0:
            return False
        return True
        
    def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        obs = float(input_data["observed_precipitation"])
        hist = float(input_data["historical_precipitation"])
        
        anomaly = obs - hist
        
        result = {
            "location_id": input_data["location_id"],
            "precipitation_anomaly": anomaly,
            "calculation_explanation": "precipitation_anomaly = observed_precipitation - historical_precipitation"
        }
        
        if hist > 0:
            pct_diff = (anomaly / hist) * 100
            result["percentage_difference"] = pct_diff
            
        if "precipitation_threshold" in input_data:
            thresh = float(input_data["precipitation_threshold"])
            exceedance = max(0.0, obs - thresh)
            result["threshold_exceedance"] = exceedance
            result["precipitation_condition"] = "high" if exceedance > 0 else "normal"
            
        return result
