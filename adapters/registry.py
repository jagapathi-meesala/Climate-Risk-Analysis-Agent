from typing import Dict, Any, Callable
from contracts.adapter import AdapterContract

class AdapterRegistry:
    """Registry for adapters to other frameworks."""
    
    def __init__(self):
        self._adapters: Dict[str, AdapterContract] = {}
        
    def register(self, name: str, adapter: AdapterContract) -> None:
        self._adapters[name] = adapter
        
    def get(self, name: str) -> AdapterContract:
        if name not in self._adapters:
            raise KeyError(f"Adapter '{name}' not found")
        return self._adapters[name]
