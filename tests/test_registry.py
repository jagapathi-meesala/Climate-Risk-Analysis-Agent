import pytest
from core.registry import DynamicToolRegistry

class ValidTool:
    name = "valid-tool"
    def validate_input(self, data): return True
    def execute(self, data): return {"status": "ok"}

class InvalidToolNoName:
    def validate_input(self, data): return True
    def execute(self, data): return {}

class InvalidToolNoExecute:
    name = "no-execute"
    def validate_input(self, data): return True

def test_registry_valid_registration():
    registry = DynamicToolRegistry()
    registry.register(ValidTool())
    assert "valid-tool" in registry.list_tools()

def test_registry_duplicate_registration():
    registry = DynamicToolRegistry()
    registry.register(ValidTool())
    with pytest.raises(ValueError, match="is already registered"):
        registry.register(ValidTool())

def test_registry_missing_tool():
    registry = DynamicToolRegistry()
    with pytest.raises(KeyError):
        registry.get("nonexistent")

def test_registry_invalid_tool_no_name():
    registry = DynamicToolRegistry()
    with pytest.raises(ValueError, match="valid 'name'"):
        registry.register(InvalidToolNoName())

def test_registry_invalid_tool_no_execute():
    registry = DynamicToolRegistry()
    with pytest.raises(ValueError, match="'execute' method"):
        registry.register(InvalidToolNoExecute())
