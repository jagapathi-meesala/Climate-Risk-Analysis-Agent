from typing import Any, Dict
from contracts.adapter import AdapterContract
from core.agent import AgentCore

class PortableAdapter(AdapterContract):
    """A generic portable adapter to wrap the agent for basic portability."""
    
    def adapt(self, agent: AgentCore) -> Dict[str, Any]:
        """Convert the agent to a portable dictionary definition."""
        return {
            "name": agent.name,
            "version": agent.version,
            "description": agent.description,
            "tools": agent.list_tools()
        }
