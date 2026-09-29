from typing import Any, Dict
from contracts.tool_contract import ToolContract

class AnalyzeTemperatureRiskTool:
    name = "analyze-temperature-risk"
    description = "Calculate deterministic temperature indicators."
    input_schema = {
        "type": "object",
        "properties": {
            "location_id": {"type": "string"},
            "observed_temperature": {"type": "number"},
            "historical_average": {"type": "number"},
            "heat_threshold": {"type": "number"}
        },
        "required": ["location_id", "observed_temperature", "historical_average"]
    }
    
    def validate_input(self, input_data: Dict[str, Any]) -> bool:
        if not isinstance(input_data, dict):
            return False
        for req in ["location_id", "observed_temperature", "historical_average"]:
            if req not in input_data:
                return False
        
        if not isinstance(input_data["observed_temperature"], (int, float)):
            return False
        if not isinstance(input_data["historical_average"], (int, float)):
            return False
            
        if "heat_threshold" in input_data and not isinstance(input_data["heat_threshold"], (int, float)):
            return False
            
        return True
        
    def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        obs_temp = float(input_data["observed_temperature"])
        hist_avg = float(input_data["historical_average"])
        
        temp_anomaly = obs_temp - hist_avg
        result = {
            "location_id": input_data["location_id"],
            "temperature_anomaly": temp_anomaly,
            "observation_summary": f"Observed {obs_temp} vs historical {hist_avg}."
        }
        
        if "heat_threshold" in input_data:
            thresh = float(input_data["heat_threshold"])
            exceedance = max(0.0, obs_temp - thresh)
            result["threshold_exceedance"] = exceedance
            result["heat_exposure_indicator"] = exceedance > 0
            
        result["calculation_explanation"] = "temperature_anomaly = observed_temperature - historical_average"
        
        return result
