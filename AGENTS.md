# Architecture

The system follows a modular, framework-independent architecture.

- **Core**: `AgentCore` handles initialization, tool registration, and execution.
- **Contracts**: Defines `ToolContract` and `AgentContract` to ensure type-safety and standard interfaces.
- **Tool Registry**: `DynamicToolRegistry` securely manages tool loading without arbitrary execution.
- **Tools**: Independent modules in the `tools/` directory, adhering to the `ToolContract`.
- **Adapters**: The `adapters/` directory allows the agent to be exported to different frameworks without changing the core.
- **Verification**: Built-in readiness audit to ensure OpenGAP compliance.
- **Interoperability**: The portability layer ensures the agent can function across LangChain, CrewAI, etc., through adapters.
- **Framework Independence**: No third-party AI dependencies in the core runtime logic.
- **Extension Mechanism**: Developers can add new `.py` files in `tools/` that subclass `ToolContract`.
