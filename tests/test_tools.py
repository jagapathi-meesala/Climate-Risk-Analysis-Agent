import pytest
import importlib.util
import os
import sys

def load_tool_module(filename, class_name):
    module_name = filename.replace(".py", "")
    file_path = os.path.join(os.path.dirname(__file__), "..", "tools", filename)
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return getattr(module, class_name)()

def test_analyze_climate_exposure():
    tool = load_tool_module("analyze-climate-exposure.py", "AnalyzeClimateExposureTool")
    # Validation
    assert tool.validate_input({"location_id": "LOC1"}) == True
    assert tool.validate_input({}) == False
    
    # Execution
    res = tool.execute({"location_id": "LOC1", "temperature_exposure": True, "drought_exposure": False})
    assert res["location_id"] == "LOC1"
    assert "temperature_exposure" in res["exposure_indicators"]
    assert "drought_exposure" not in res["exposure_indicators"]

def test_analyze_temperature_risk():
    tool = load_tool_module("analyze-temperature-risk.py", "AnalyzeTemperatureRiskTool")
    # Validation
    assert tool.validate_input({"location_id": "L1", "observed_temperature": 35.0, "historical_average": 30.0}) == True
    assert tool.validate_input({"location_id": "L1", "observed_temperature": "35"}) == False
    
    # Execution
    res = tool.execute({"location_id": "L1", "observed_temperature": 35.0, "historical_average": 30.0, "heat_threshold": 32.0})
    assert res["temperature_anomaly"] == 5.0
    assert res["threshold_exceedance"] == 3.0

def test_analyze_precipitation_risk():
    tool = load_tool_module("analyze-precipitation-risk.py", "AnalyzePrecipitationRiskTool")
    assert tool.validate_input({"location_id": "L1", "observed_precipitation": 100, "historical_precipitation": 80}) == True
    
    # Execution
    res = tool.execute({"location_id": "L1", "observed_precipitation": 100, "historical_precipitation": 80})
    assert res["precipitation_anomaly"] == 20
    assert res["percentage_difference"] == 25.0
    
    # Zero division protection check (if hist is 0)
    res_zero = tool.execute({"location_id": "L1", "observed_precipitation": 100, "historical_precipitation": 0})
    assert "percentage_difference" not in res_zero

def test_calculate_drought_risk():
    tool = load_tool_module("calculate-drought-risk.py", "CalculateDroughtRiskTool")
    assert tool.validate_input({"precipitation_deficit": 100, "dry_days": 30}) == True
    assert tool.validate_input({"precipitation_deficit": 100, "dry_days": -5}) == False
    
    res = tool.execute({"precipitation_deficit": 100, "dry_days": 30})
    assert "drought_score" in res
    assert res["risk_category"] == "Severe"

def test_calculate_flood_risk():
    tool = load_tool_module("calculate-flood-risk.py", "CalculateFloodRiskTool")
    assert tool.validate_input({"cumulative_rainfall": 150, "drainage_capacity": 100}) == True
    assert tool.validate_input({"cumulative_rainfall": 150, "drainage_capacity": 0}) == False
    
    res = tool.execute({"cumulative_rainfall": 150, "drainage_capacity": 100})
    assert res["flood_risk_score"] == 150.0
    assert res["risk_category"] == "High"

def test_calculate_climate_vulnerability():
    tool = load_tool_module("calculate-climate-vulnerability.py", "CalculateClimateVulnerabilityTool")
    res = tool.execute({"population_exposure": 100, "infrastructure_exposure": 50})
    assert res["vulnerability_score"] == 75.0
    assert res["category"] == "Medium"

def test_calculate_climate_priority():
    tool = load_tool_module("calculate-climate-priority.py", "CalculateClimatePriorityTool")
    res = tool.execute({"hazard_score": 80, "exposure_score": 70, "vulnerability_score": 90})
    # 80*0.4 + 70*0.3 + 90*0.3 = 32 + 21 + 27 = 80
    assert res["calculated_priority_score"] == 80.0
    assert res["priority_category"] == "Critical"
