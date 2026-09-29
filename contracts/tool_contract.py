from typing import Any, Dict, Protocol

class ToolContract(Protocol):
    """Protocol defining the interface all tools must implement."""
    name: str
    description: str
    input_schema: Dict[str, Any]
    
    def validate_input(self, input_data: Dict[str, Any]) -> bool:
        """Validate input data against schema."""
        ...
        
    def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute the deterministic tool logic."""
        ...
