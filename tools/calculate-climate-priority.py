from typing import Any, Dict
from contracts.tool_contract import ToolContract

class CalculateClimatePriorityTool:
    name = "calculate-climate-priority"
    description = "Calculate climate priority score based on hazard, exposure, and vulnerability."
    input_schema = {
        "type": "object",
        "properties": {
            "hazard_score": {"type": "number"},
            "exposure_score": {"type": "number"},
            "vulnerability_score": {"type": "number"}
        },
        "required": ["hazard_score", "exposure_score", "vulnerability_score"]
    }
    
    def validate_input(self, input_data: Dict[str, Any]) -> bool:
        if not isinstance(input_data, dict):
            return False
        for req in ["hazard_score", "exposure_score", "vulnerability_score"]:
            if req not in input_data:
                return False
            if not isinstance(input_data[req], (int, float)):
                return False
        return True
        
    def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        hazard = float(input_data["hazard_score"])
        exposure = float(input_data["exposure_score"])
        vuln = float(input_data["vulnerability_score"])
        
        score = (hazard * 0.4) + (exposure * 0.3) + (vuln * 0.3)
        category = "Critical" if score >= 75 else ("Elevated" if score >= 50 else "Standard")
        
        return {
            "calculated_priority_score": score,
            "contributing_factors": {"hazard": hazard, "exposure": exposure, "vulnerability": vuln},
            "formula": "priority_score = (hazard_score * 0.4) + (exposure_score * 0.3) + (vulnerability_score * 0.3)",
            "weights": {"hazard": 0.4, "exposure": 0.3, "vulnerability": 0.3},
            "thresholds": {"critical": 75, "elevated": 50},
            "priority_category": category,
            "explanation": "Weighted combination of hazard, exposure, and vulnerability.",
            "limitations": "Not an industry-standard score. No machine learning used. Internal priority metric only."
        }
