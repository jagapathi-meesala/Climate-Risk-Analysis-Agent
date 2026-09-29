from typing import Any, Dict, List
from contracts.tool_contract import ToolContract

class DynamicToolRegistry:
    """Dynamically manages tools without executing arbitrary code."""
    
    def __init__(self):
        self._tools: Dict[str, ToolContract] = {}
        
    def register(self, tool: ToolContract) -> None:
        """Register a tool instance."""
        if not hasattr(tool, 'name') or not tool.name:
            raise ValueError("Tool must have a valid 'name' property")
            
        if tool.name in self._tools:
            raise ValueError(f"Tool '{tool.name}' is already registered.")
            
        if not hasattr(tool, 'execute') or not callable(tool.execute):
            raise ValueError(f"Tool '{tool.name}' must implement an 'execute' method.")
            
        if not hasattr(tool, 'validate_input') or not callable(tool.validate_input):
            raise ValueError(f"Tool '{tool.name}' must implement a 'validate_input' method.")
            
        self._tools[tool.name] = tool
        
    def get(self, tool_name: str) -> ToolContract:
        """Get a tool by name."""
        if tool_name not in self._tools:
            raise KeyError(f"Tool '{tool_name}' not found in registry.")
        return self._tools[tool_name]
        
    def list_tools(self) -> List[str]:
        """List registered tool names."""
        return list(self._tools.keys())
        
    def execute(self, tool_name: str, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate input and execute tool safely."""
        tool = self.get(tool_name)
        if not tool.validate_input(input_data):
            return {"error": "Invalid input provided.", "status": "failed"}
            
        try:
            return tool.execute(input_data)
        except Exception as e:
            return {"error": str(e), "status": "failed"}
