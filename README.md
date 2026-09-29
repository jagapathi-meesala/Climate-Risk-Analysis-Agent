# Climate Risk Analysis Agent

## Overview
A complete, deterministic, testable, and documented agent designed for the HiDevs Agent Passport / OpenGAP ecosystem. It analyzes structured climate and environmental risk information supplied by the user.

## Features
- Framework-independent design
- Deterministic calculations
- No generative AI required for core system
- Seven built-in tools for climate data analysis
- Extensive test coverage
- Secure execution (no eval/exec)

## Architecture
See `AGENTS.md` for full architecture details.

## Tools
See `EXPLAINABILITY.md` for tools and formulas.

## Input/Output Examples
Input: `{"location_id": "LOC-1", "observed_temperature": 35.0, "historical_average": 30.0}`
Output: `{"temperature_anomaly": 5.0}`

## Installation
```bash
pip install -r requirements.txt
```

## Configuration
Copy `.env.example` to `.env` and adjust as necessary. The core system operates deterministically and requires no API keys for its base functions.

## Running Tests
```bash
pytest -q
```

## Validation
```bash
python -m verification.readiness_audit
```

## Security
No arbitrary code execution, no secrets hardcoded. Validates all input.

## Portability
Uses adapters (see `adapters/`) to integrate with any runtime framework without modifying core logic.

## OpenGAP Compliance
Follows OpenGAP schema guidelines. Uses `agent.yaml`, `SOUL.md`, `RULES.md`, etc.

## Climate-Data Limitations
Calculations rely entirely on user-provided structured data. The agent does NOT have live weather data and should NOT be used for real-time emergency forecasts.

## Project Structure
Standard OpenGAP structure with `core`, `tools`, `contracts`, `adapters`, `tests`, and `verification`.

## Extension Guide
Implement the `ToolContract` (see `contracts/tool_contract.py`) to add new tools.
