from typing import Any, Dict
from contracts.tool_contract import ToolContract

class CalculateDroughtRiskTool:
    name = "calculate-drought-risk"
    description = "Calculate drought score based on precipitation deficit and dry days."
    input_schema = {
        "type": "object",
        "properties": {
            "precipitation_deficit": {"type": "number"},
            "dry_days": {"type": "number"}
        },
        "required": ["precipitation_deficit", "dry_days"]
    }
    
    def validate_input(self, input_data: Dict[str, Any]) -> bool:
        if not isinstance(input_data, dict):
            return False
        for req in ["precipitation_deficit", "dry_days"]:
            if req not in input_data:
                return False
            if not isinstance(input_data[req], (int, float)):
                return False
        if input_data["dry_days"] < 0:
            return False
        return True
        
    def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        deficit = float(input_data["precipitation_deficit"])
        dry_days = float(input_data["dry_days"])
        
        score = (deficit * 0.6) + (dry_days * 0.4)
        category = "Severe" if score > 50 else ("Moderate" if score > 20 else "Low")
        
        return {
            "drought_score": score,
            "contributing_factors": {"precipitation_deficit": deficit, "dry_days": dry_days},
            "applied_thresholds": {"severe": 50, "moderate": 20},
            "calculation_explanation": "score = (deficit * 0.6) + (dry_days * 0.4)",
            "risk_category": category,
            "limitations": "Result is a deterministically calculated score and NOT an official drought classification."
        }
