import pytest
from core.agent import AgentCore
from adapters.portable_adapter import PortableAdapter
from adapters.registry import AdapterRegistry

def test_portable_adapter():
    agent = AgentCore(name="TestAdapterAgent", version="1.0.0")
    adapter = PortableAdapter()
    result = adapter.adapt(agent)
    assert result["name"] == "TestAdapterAgent"
    assert result["version"] == "1.0.0"
    assert "tools" in result

def test_adapter_registry():
    registry = AdapterRegistry()
    adapter = PortableAdapter()
    registry.register("portable", adapter)
    assert registry.get("portable") == adapter
    
    with pytest.raises(KeyError):
        registry.get("nonexistent")
