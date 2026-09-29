from typing import Any, Dict
from contracts.tool_contract import ToolContract

class AnalyzeClimateExposureTool:
    name = "analyze-climate-exposure"
    description = "Analyze structured climate exposure for a location or asset."
    input_schema = {
        "type": "object",
        "properties": {
            "location_id": {"type": "string"},
            "location_name": {"type": "string"},
            "temperature_exposure": {"type": "boolean"},
            "precipitation_exposure": {"type": "boolean"},
            "drought_exposure": {"type": "boolean"},
            "flood_exposure": {"type": "boolean"},
            "extreme_weather_exposure": {"type": "boolean"}
        },
        "required": ["location_id"]
    }
    
    def validate_input(self, input_data: Dict[str, Any]) -> bool:
        if not isinstance(input_data, dict):
            return False
        if "location_id" not in input_data:
            return False
        return True
        
    def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        exposure_factors = [
            "temperature_exposure", "precipitation_exposure", 
            "drought_exposure", "flood_exposure", "extreme_weather_exposure"
        ]
        
        available_factors = []
        missing_factors = []
        active_exposures = []
        
        for factor in exposure_factors:
            if factor in input_data:
                available_factors.append(factor)
                if input_data[factor]:
                    active_exposures.append(factor)
            else:
                missing_factors.append(factor)
                
        exposure_score = len(active_exposures) / len(exposure_factors)
        
        return {
            "location_id": input_data["location_id"],
            "exposure_indicators": active_exposures,
            "available_exposure_factors": available_factors,
            "missing_factors": missing_factors,
            "normalized_exposure_value": exposure_score,
            "structured_findings": f"{len(active_exposures)} out of {len(exposure_factors)} exposures are active.",
            "calculation_explanation": "Normalized exposure is the count of true boolean exposure flags divided by total possible flags."
        }
