from typing import Any, Dict, List
from core.registry import DynamicToolRegistry
from contracts.tool_contract import ToolContract

class AgentCore:
    """Core framework-independent Agent logic."""
    
    def __init__(self, name: str = "Climate Risk Analysis Agent", version: str = "1.0.0"):
        self.name = name
        self.version = version
        self.description = "A deterministic, framework-independent agent for analyzing structured climate and environmental risk data."
        self.registry = DynamicToolRegistry()
        
    def register_tool(self, tool: ToolContract) -> None:
        """Register a tool in the dynamic registry."""
        self.registry.register(tool)
        
    def execute_tool(self, tool_name: str, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a registered tool."""
        return self.registry.execute(tool_name, input_data)
        
    def list_tools(self) -> List[str]:
        """List all available tools."""
        return self.registry.list_tools()
