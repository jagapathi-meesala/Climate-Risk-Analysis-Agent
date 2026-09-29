import os
import yaml

def test_agent_yaml_structure():
    """Verify basic openGAP agent.yaml schema compliance locally."""
    manifest_path = os.path.join(os.path.dirname(__file__), "..", "agent.yaml")
    if not os.path.exists(manifest_path):
        pytest.fail("agent.yaml not found")
        
    with open(manifest_path, "r") as f:
        data = yaml.safe_load(f)
        
    assert "name" in data, "name missing from agent.yaml"
    assert "version" in data, "version missing from agent.yaml"
    
    # Specific constraints for our project
    assert data["name"] == "climate-risk-analysis-agent"
    
    # Ensure no unsupported properties like display_name
    assert "display_name" not in data, "Unsupported property 'display_name' found"
