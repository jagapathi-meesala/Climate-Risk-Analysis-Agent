# Explainability

## Inputs and Data Sources
The agent uses structured input data supplied directly to its deterministic climate-analysis tools. The data source is the structured input supplied by the caller, and the input values provide the location identifiers and environmental data required by the implemented calculations.

## Decision and Reasoning
The agent's decision process applies deterministic rules and formulas implemented by its analysis tools. The agent decides each resulting metric or category from the supplied input values and the defined thresholds or weights, without hidden reasoning or external LLM inference.

## Limits and Constraints
A key limitation is that the agent only processes structured climate data and calculations implemented by its tools. A key constraint is that it does not automatically discover external data or provide unsupported scientific interpretations beyond its implemented formulas.

## Agent Purpose
The Climate Risk Analysis Agent is a fully deterministic, framework-independent analytical system. It is designed to analyze structured climate and environmental risk data strictly based on user-supplied inputs. The core agent architecture relies entirely on hard-coded Python logic and mathematical formulas; it **does not** rely on Generative AI, machine learning models, or external LLMs to perform any of its risk, exposure, hazard, or vulnerability calculations.

## Input Mechanisms
All input reaches the agent and its tools via structured dictionaries matching the schemas defined by the `ToolContract`.
- **Tool-Specific Input Contracts**: Each tool validates its own arguments against its required properties.
- **Required and Optional Fields**: Each tool explicitly dictates which fields must be present and which are optional (e.g., threshold limits).
- **Validation Behavior**: All inputs undergo rigorous validation. The agent checks data types (e.g., ensuring numeric values where required), boundaries (e.g., preventing negative values for precipitation), and mathematical soundness (e.g., explicitly blocking `drainage_capacity <= 0` to prevent division-by-zero errors).

## Decision Mechanisms
Decisions and calculated outcomes are produced exclusively by deterministic rules and formulas written into the `execute` methods of the tool classes. 
The seven tools transform numeric and boolean input data into analytical outputs (such as risk anomalies or categorical assessments). 
There is no hidden reasoning, no non-deterministic generation, and no LLM reasoning process evaluating the risk scores. It is 100% rules-based.

## Execution Limits
- **No External Discovery**: The agent makes no external API calls to discover missing attributes (e.g., fetching satellite weather data).
- **No Automatic Unit Conversion**: Input values are assumed to be supplied in uniform, compatible formats.
- **Not Official Warnings**: Calculated categories (like "Severe", "Critical") represent arbitrary output buckets based on internal logic. They are **not** official climate classifications or governmental emergency warnings.
- **No Unsupported Interpretations**: The agent explicitly avoids making subjective scientific interpretations of data. Results strictly reflect the provided input multiplied by the documented static formulas.

## Output Contract
Outputs are strictly returned as structured dictionaries. 
- **Tool-Specific Fields**: Each tool returns a customized schema reflecting its calculation, including fields like `location_id`, `_score`, `_anomaly`, `contributing_factors`, and `calculation_explanation`.
- **Validation/Error Behavior**: If validation fails during `validate_input()`, the dynamic tool registry intercepts the failure and securely returns `{"error": "Invalid input provided.", "status": "failed"}` or a specific Python exception safely caught and converted to an error dictionary. There is no universal response schema beyond the registry failure wrapper.

## Complete Execution Lifecycle
1. **Input Generation**: A request dictating the tool to use and its structured arguments arrives.
2. **Validation**: The `DynamicToolRegistry` locates the tool and executes `validate_input(input_data)`.
3. **Tool Selection / Registry Execution**: Upon successful validation, the registry securely invokes `execute(input_data)`.
4. **Deterministic Calculation**: The isolated Python logic performs strict arithmetic steps based on the validated inputs.
5. **Structured Result**: A result dictionary is assembled with numeric metrics, threshold categories, and explanations.
6. **Explanation/Provenance Information**: The output includes explicit `calculation_explanation` or `limitations` strings clearly linking the result to the arithmetic formula applied.

## Decision/Rule Transparency (Tool-by-Tool) & Tool-by-Tool Examples

**Tool 1: analyze-climate-exposure**

### Input Requirements
- **Exact Required Inputs**: `location_id` (string).
- **Exact Optional Inputs**: `location_name` (string), `temperature_exposure` (boolean), `precipitation_exposure` (boolean), `drought_exposure` (boolean), `flood_exposure` (boolean), `extreme_weather_exposure` (boolean).
- **Accepted Types**: Strings for identifiers, booleans for exposure factors.
- **Validation Boundaries**: Input must be a valid dictionary structure containing the `location_id`.

### Failure Handling
- **Missing Required Input Behavior**: Fails validation if `location_id` is missing.
- **Invalid Type Behavior**: Returns `{"error": "Invalid input provided.", "status": "failed"}` via the registry if `input_data` is not a dictionary.
- **Invalid Numeric Boundary Behavior**: Not applicable (no numeric inputs).
- **Zero-Division Protection**: Not applicable (denominator is a hardcoded constant of 5.0).
- **Exact Validation/Error Behavior**: Securely intercepts missing/invalid types at the `validate_input` stage.

### Tools and Capabilities
- **Exact Tool Name**: `analyze-climate-exposure`
- **Capability Provided**: Analyzes structured climate exposure for a location or asset.
- **Deterministic Operation**: Calculates a normalized exposure score by dividing the number of active boolean exposure flags by the total standard exposure factors.

### Rules Applied
- **Exact Deterministic Rule**: Counts the provided `True` values and divides by 5.
- **Formula**: `normalized_exposure_value = len(active_exposures) / 5.0`
- **Weights**: All 5 standard factors carry equal weight (0.2 each).
- **Thresholds**: None explicitly categorized.
- **Branching Logic**: Loops over standard factors; if a factor is present in input, it tracks it as available; if `True`, it tracks as active.

### Expected Outputs
- **Exact Output Field Names**: `location_id`, `exposure_indicators`, `available_exposure_factors`, `missing_factors`, `normalized_exposure_value`, `structured_findings`, `calculation_explanation`.
- **Conditional Output Fields**: None.
- **Categories/Indicators**: Lists of specific active and missing indicators.
- **Error Output Behavior**: Returns error dict natively through `AgentCore` registry on validation failure.

### Worked Example
- **Input**: `{"location_id": "L1", "temperature_exposure": True, "flood_exposure": False}`
- **Validation**: Ensures `location_id` "L1" exists and input is a dict.
- **Calculation/Rule**: Evaluates 2 provided factors -> counts 1 `True` factor -> `1 / 5.0 = 0.2`.
- **Output**: `{"location_id": "L1", "exposure_indicators": ["temperature_exposure"], "available_exposure_factors": ["temperature_exposure", "flood_exposure"], "missing_factors": ["drought_exposure", "precipitation_exposure", "extreme_weather_exposure"], "normalized_exposure_value": 0.2, ...}`
- **Explanation**: 1 out of 5 possible total exposures is active, yielding 0.2.


**Tool 2: analyze-temperature-risk**

### Input Requirements
- **Exact Required Inputs**: `location_id` (string), `observed_temperature` (numeric), `historical_average` (numeric).
- **Exact Optional Inputs**: `heat_threshold` (numeric).
- **Accepted Types**: Integers or floats for temperatures.
- **Validation Boundaries**: All numeric fields are strictly verified for numeric type (`int` or `float`).

### Failure Handling
- **Missing Required Input Behavior**: Fails validation immediately if required keys are absent.
- **Invalid Type Behavior**: Rejects string representations of numbers.
- **Invalid Numeric Boundary Behavior**: None explicitly checked for temperature.
- **Zero-Division Protection**: Not applicable (no division).
- **Exact Validation/Error Behavior**: Returns `False` from `validate_input` if types mismatch or required fields are missing.

### Tools and Capabilities
- **Exact Tool Name**: `analyze-temperature-risk`
- **Capability Provided**: Calculates deterministic temperature indicators.
- **Deterministic Operation**: Computes the temperature anomaly by subtracting historical average from observed temperature, and checks exceedance against a threshold.

### Rules Applied
- **Exact Deterministic Rule**: Subtracts historical from observed values.
- **Formula**: `temperature_anomaly = observed_temperature - historical_average`
- **Weights**: None.
- **Thresholds**: If `heat_threshold` supplied: `exceedance = max(0.0, observed_temperature - heat_threshold)`.
- **Branching Logic**: Optional fields trigger additional dictionary inclusions (`threshold_exceedance`, `heat_exposure_indicator`).

### Expected Outputs
- **Exact Output Field Names**: `location_id`, `temperature_anomaly`, `observation_summary`, `calculation_explanation`.
- **Conditional Output Fields**: `threshold_exceedance`, `heat_exposure_indicator`.
- **Categories/Indicators**: `heat_exposure_indicator` is a boolean.
- **Error Output Behavior**: Safe rejection returning error dict.

### Worked Example
- **Input**: `{"location_id": "L2", "observed_temperature": 35.0, "historical_average": 30.0, "heat_threshold": 32.0}`
- **Validation**: Passes numeric checks for all fields.
- **Calculation/Rule**: `35.0 - 30.0 = 5.0` anomaly. `max(0.0, 35.0 - 32.0) = 3.0` exceedance.
- **Output**: `{"location_id": "L2", "temperature_anomaly": 5.0, "observation_summary": "Observed 35.0 vs historical 30.0.", "threshold_exceedance": 3.0, "heat_exposure_indicator": True, "calculation_explanation": "temperature_anomaly = observed_temperature - historical_average"}`
- **Explanation**: The anomaly derives strictly from subtracting historical from observed.


**Tool 3: analyze-precipitation-risk**

### Input Requirements
- **Exact Required Inputs**: `location_id` (string), `observed_precipitation` (numeric), `historical_precipitation` (numeric).
- **Exact Optional Inputs**: `precipitation_threshold` (numeric).
- **Accepted Types**: Integers or floats.
- **Validation Boundaries**: Precipitation inputs cannot be negative (`< 0`).

### Failure Handling
- **Missing Required Input Behavior**: Validation fails if omitted.
- **Invalid Type Behavior**: Non-numeric values rejected.
- **Invalid Numeric Boundary Behavior**: Negative precipitation values immediately return `False` during validation.
- **Zero-Division Protection**: Percentage difference is skipped entirely if `historical_precipitation == 0`.
- **Exact Validation/Error Behavior**: Secure boundaries ensure no impossible (negative) rain values are processed.

### Tools and Capabilities
- **Exact Tool Name**: `analyze-precipitation-risk`
- **Capability Provided**: Calculates deterministic precipitation indicators.
- **Deterministic Operation**: Finds the raw difference (anomaly) and percent difference in precipitation against historical norms.

### Rules Applied
- **Exact Deterministic Rule**: Subtracts historical from observed precipitation.
- **Formula**: `anomaly = observed_precipitation - historical_precipitation`. `percentage_difference = (anomaly / historical_precipitation) * 100`.
- **Weights**: None.
- **Thresholds**: If `precipitation_threshold` provided, exceedance is computed.
- **Branching Logic**: If `historical_precipitation > 0`, adds percentage difference. If threshold provided, adds `precipitation_condition` ("high" or "normal").

### Expected Outputs
- **Exact Output Field Names**: `location_id`, `precipitation_anomaly`, `calculation_explanation`.
- **Conditional Output Fields**: `percentage_difference`, `threshold_exceedance`, `precipitation_condition`.
- **Categories/Indicators**: `precipitation_condition` can be "high" or "normal".
- **Error Output Behavior**: Fails via registry safely.

### Worked Example
- **Input**: `{"location_id": "L3", "observed_precipitation": 120, "historical_precipitation": 100}`
- **Validation**: Validates numeric types and >= 0 bounds.
- **Calculation/Rule**: `120 - 100 = 20`. `(20 / 100) * 100 = 20%`.
- **Output**: `{"location_id": "L3", "precipitation_anomaly": 20.0, "percentage_difference": 20.0, ...}`
- **Explanation**: Mathematical percentage difference applies because history is safely non-zero and positive.


**Tool 4: calculate-drought-risk**

### Input Requirements
- **Exact Required Inputs**: `precipitation_deficit` (numeric), `dry_days` (numeric).
- **Exact Optional Inputs**: None.
- **Accepted Types**: Integers or floats.
- **Validation Boundaries**: `dry_days` cannot be `< 0`.

### Failure Handling
- **Missing Required Input Behavior**: Immediately fails.
- **Invalid Type Behavior**: Reject strings.
- **Invalid Numeric Boundary Behavior**: Negative `dry_days` fails validation.
- **Zero-Division Protection**: Not applicable.
- **Exact Validation/Error Behavior**: Safely returns `False` in `validate_input`.

### Tools and Capabilities
- **Exact Tool Name**: `calculate-drought-risk`
- **Capability Provided**: Computes a drought score.
- **Deterministic Operation**: Calculates a weighted score combining precipitation deficit and consecutive dry days.

### Rules Applied
- **Exact Deterministic Rule**: Linearly combines inputs using hardcoded weights.
- **Formula**: `score = (precipitation_deficit * 0.6) + (dry_days * 0.4)`
- **Weights**: 0.6 for precipitation_deficit, 0.4 for dry_days.
- **Thresholds**: `Severe` (> 50), `Moderate` (> 20), else `Low`.
- **Branching Logic**: Standard `if/elif/else` threshold bucket categorization.

### Expected Outputs
- **Exact Output Field Names**: `drought_score`, `contributing_factors`, `applied_thresholds`, `calculation_explanation`, `risk_category`, `limitations`.
- **Conditional Output Fields**: None.
- **Categories/Indicators**: `Severe`, `Moderate`, `Low`.
- **Error Output Behavior**: Rejects invalid states.

### Worked Example
- **Input**: `{"precipitation_deficit": 60, "dry_days": 10}`
- **Validation**: Ensures fields are numeric and >= 0.
- **Calculation/Rule**: `(60 * 0.6) + (10 * 0.4) = 36 + 4 = 40.0`.
- **Output**: `{"drought_score": 40.0, "risk_category": "Moderate", ...}`
- **Explanation**: Output falls firmly in the moderate threshold boundary (between 20 and 50).


**Tool 5: calculate-flood-risk**

### Input Requirements
- **Exact Required Inputs**: `cumulative_rainfall` (numeric), `drainage_capacity` (numeric).
- **Exact Optional Inputs**: None.
- **Accepted Types**: Integers or floats.
- **Validation Boundaries**: Both must be `>= 0`, and `drainage_capacity` must be `> 0`.

### Failure Handling
- **Missing Required Input Behavior**: Validation fails.
- **Invalid Type Behavior**: Rejects strings/booleans.
- **Invalid Numeric Boundary Behavior**: Negative rainfall fails validation.
- **Zero-Division Protection**: `drainage_capacity` strictly enforced to be `> 0` to prevent `ZeroDivisionError`.
- **Exact Validation/Error Behavior**: Returns `False` internally if parameters are unsafe.

### Tools and Capabilities
- **Exact Tool Name**: `calculate-flood-risk`
- **Capability Provided**: Computes a deterministic flood risk score.
- **Deterministic Operation**: Assesses how close cumulative rainfall is to the drainage capacity.

### Rules Applied
- **Exact Deterministic Rule**: Expresses rainfall as a percentage of drainage capacity.
- **Formula**: `risk_score = (cumulative_rainfall / drainage_capacity) * 100`
- **Weights**: None.
- **Thresholds**: `High` (>= 100), `Medium` (>= 75), else `Low`.
- **Branching Logic**: Standard bounds checking for category string assignment.

### Expected Outputs
- **Exact Output Field Names**: `flood_risk_score`, `contributing_factors`, `threshold_conditions`, `risk_category`, `calculation_explanation`, `limitations`.
- **Conditional Output Fields**: None.
- **Categories/Indicators**: `High`, `Medium`, `Low`.
- **Error Output Behavior**: Wraps validation error safely.

### Worked Example
- **Input**: `{"cumulative_rainfall": 80, "drainage_capacity": 100}`
- **Validation**: Checks numbers and verifies `drainage_capacity` > 0.
- **Calculation/Rule**: `(80 / 100) * 100 = 80.0`.
- **Output**: `{"flood_risk_score": 80.0, "risk_category": "Medium", ...}`
- **Explanation**: Calculates saturation percentage relative to explicit capacity.


**Tool 6: calculate-climate-vulnerability**

### Input Requirements
- **Exact Required Inputs**: `population_exposure` (numeric), `infrastructure_exposure` (numeric).
- **Exact Optional Inputs**: None.
- **Accepted Types**: Integers or floats.
- **Validation Boundaries**: Must be valid numbers.

### Failure Handling
- **Missing Required Input Behavior**: Fails validation.
- **Invalid Type Behavior**: Safely rejects via `isinstance` checks.
- **Invalid Numeric Boundary Behavior**: Not explicitly bounded in code beyond numeric type.
- **Zero-Division Protection**: Not applicable.
- **Exact Validation/Error Behavior**: Checks schema adherence.

### Tools and Capabilities
- **Exact Tool Name**: `calculate-climate-vulnerability`
- **Capability Provided**: Computes vulnerability score based on exposures.
- **Deterministic Operation**: Calculates an evenly weighted score of population and infrastructure.

### Rules Applied
- **Exact Deterministic Rule**: Applies fixed 0.5 weights to both variables.
- **Formula**: `vulnerability_score = (population_exposure * 0.5) + (infrastructure_exposure * 0.5)`
- **Weights**: 0.5 for population, 0.5 for infrastructure.
- **Thresholds**: `High` (>= 80), `Medium` (>= 40), else `Low`.
- **Branching Logic**: Evaluates thresholds for category.

### Expected Outputs
- **Exact Output Field Names**: `vulnerability_score`, `factor_contributions`, `formula`, `assumptions`, `category`, `missing_data`, `limitations`.
- **Conditional Output Fields**: None.
- **Categories/Indicators**: `High`, `Medium`, `Low`.
- **Error Output Behavior**: Rejects unvalidated states.

### Worked Example
- **Input**: `{"population_exposure": 50, "infrastructure_exposure": 50}`
- **Validation**: Validates numeric presence.
- **Calculation/Rule**: `(50 * 0.5) + (50 * 0.5) = 50.0`.
- **Output**: `{"vulnerability_score": 50.0, "category": "Medium", "missing_data": [], ...}`
- **Explanation**: Weights combine uniformly.


**Tool 7: calculate-climate-priority**

### Input Requirements
- **Exact Required Inputs**: `hazard_score` (numeric), `exposure_score` (numeric), `vulnerability_score` (numeric).
- **Exact Optional Inputs**: None.
- **Accepted Types**: Integers or floats.
- **Validation Boundaries**: Type checks for numeric values.

### Failure Handling
- **Missing Required Input Behavior**: Missing any of the 3 fields fails validation.
- **Invalid Type Behavior**: Ensures inputs are proper python numbers.
- **Invalid Numeric Boundary Behavior**: Not bounded by minimums/maximums in the code beyond numbers.
- **Zero-Division Protection**: Not applicable.
- **Exact Validation/Error Behavior**: Native python structural validation.

### Tools and Capabilities
- **Exact Tool Name**: `calculate-climate-priority`
- **Capability Provided**: Determines overall priority score.
- **Deterministic Operation**: Computes a three-factor weighted average using hazard, exposure, and vulnerability.

### Rules Applied
- **Exact Deterministic Rule**: Weighted linear combination.
- **Formula**: `priority_score = (hazard_score * 0.4) + (exposure_score * 0.3) + (vulnerability_score * 0.3)`
- **Weights**: Hazard (0.4), Exposure (0.3), Vulnerability (0.3).
- **Thresholds**: `Critical` (>= 75), `Elevated` (>= 50), else `Standard`.
- **Branching Logic**: Outputs a string based on final score bounds.

### Expected Outputs
- **Exact Output Field Names**: `calculated_priority_score`, `contributing_factors`, `formula`, `weights`, `thresholds`, `priority_category`, `explanation`, `limitations`.
- **Conditional Output Fields**: None.
- **Categories/Indicators**: `Critical`, `Elevated`, `Standard`.
- **Error Output Behavior**: Handles structurally invalid input seamlessly via registry.

### Worked Example
- **Input**: `{"hazard_score": 100, "exposure_score": 100, "vulnerability_score": 100}`
- **Validation**: Type validation passes.
- **Calculation/Rule**: `(100 * 0.4) + (100 * 0.3) + (100 * 0.3) = 100.0`.
- **Output**: `{"calculated_priority_score": 100.0, "priority_category": "Critical", ...}`
- **Explanation**: Result achieves maximum theoretical boundary.

## Explainability of Calculated Results
For every mathematical result produced by this agent:
- The exact **formula** used is systematically hardcoded in the source and transparently embedded inside the returned JSON payload via the `calculation_explanation` or `formula` fields.
- The **input values used** are uniformly reflected in the `contributing_factors` block to trace logic backwards.
- The **weights** and **thresholds applied** are statically defined and exposed directly in response items (e.g., `applied_thresholds` dictionary).
- The **resulting category/indicator** string solely represents where the arithmetic output landed against internal cut-offs (e.g., `score > 50 -> "Severe"`). 
- What the result **does NOT mean**: It does not constitute official science, governmental hazard assessment, or AI-generated situational forecasting.

## Provenance
All calculations and risk scores have a clear provenance lineage:
- **User / Supplied Structured Input**: Every variable affecting the calculation traces directly back to the initial API payload. No databases or live sensors are attached.
- **Deterministic Implementation Logic**: Operations execute strictly through statically written python arithmetic (e.g., `/`, `-`, `+`, `max()`) in isolated execution spaces.
- **Configured Constants / Weights**: All static parameters (such as the 0.6 drought precipitation weighting) are baked into the tool execution contracts, eliminating reliance on shifting models or external scientific authority data points. No external datasets, APIs, official climate standards, or LLM-driven intelligence metrics are used.
