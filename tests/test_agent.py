import pytest
from core.agent import AgentCore
from core.registry import DynamicToolRegistry

class MockTool:
    name = "mock-tool"
    description = "A mock tool for testing."
    input_schema = {}
    def validate_input(self, data):
        return True
    def execute(self, data):
        return {"success": True}

def test_agent_initialization():
    agent = AgentCore(name="Test Agent", version="0.1.0")
    assert agent.name == "Test Agent"
    assert agent.version == "0.1.0"
    assert isinstance(agent.registry, DynamicToolRegistry)

def test_agent_tool_registration_and_execution():
    agent = AgentCore()
    tool = MockTool()
    agent.register_tool(tool)
    assert "mock-tool" in agent.list_tools()
    result = agent.execute_tool("mock-tool", {})
    assert result == {"success": True}
