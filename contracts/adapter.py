from typing import Any, Dict, Protocol

class AdapterContract(Protocol):
    """Protocol defining the interface for framework adapters."""
    
    def adapt(self, agent: Any) -> Any:
        """Adapt the agent to a specific framework's format."""
        ...
