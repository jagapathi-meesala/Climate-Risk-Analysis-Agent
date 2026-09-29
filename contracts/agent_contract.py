from typing import Any, Dict, Protocol, List

class AgentContract(Protocol):
    """Protocol defining the interface for the agent core."""
    name: str
    version: str
    description: str
    
    def execute_tool(self, tool_name: str, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a registered tool."""
        ...
        
    def list_tools(self) -> List[str]:
        """List all available tools."""
        ...
