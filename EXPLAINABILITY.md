# Explainability

## Agent Purpose
The Climate Risk Analysis Agent is a fully deterministic, framework-independent analytical system. It is designed to analyze structured climate and environmental risk data strictly based on user-supplied inputs. The core agent architecture relies entirely on hard-coded Python logic and mathematical formulas; it **does not** rely on Generative AI, machine learning models, or external LLMs to perform any of its risk, exposure, hazard, or vulnerability calculations.

## Inputs
All input reaches the agent and its tools via structured dictionaries matching the schemas defined by the `ToolContract`.
- **Tool-Specific Input Contracts**: Each tool validates its own arguments against its required properties.
- **Required and Optional Fields**: Each tool explicitly dictates which fields must be present and which are optional (e.g., threshold limits).
- **Validation Behavior**: All inputs undergo rigorous validation. The agent checks data types (e.g., ensuring numeric values where required), boundaries (e.g., preventing negative values for precipitation), and mathematical soundness (e.g., explicitly blocking `drainage_capacity <= 0` to prevent division-by-zero errors).

## Decision
Decisions and calculated outcomes are produced exclusively by deterministic rules and formulas written into the `execute` methods of the tool classes. 
The seven tools transform numeric and boolean input data into analytical outputs (such as risk anomalies or categorical assessments). 
There is no hidden reasoning, no non-deterministic generation, and no LLM reasoning process evaluating the risk scores. It is 100% rules-based.

## Limits
- **No External Discovery**: The agent makes no external API calls to discover missing attributes (e.g., fetching satellite weather data).
- **No Automatic Unit Conversion**: Input values are assumed to be supplied in uniform, compatible formats.
- **Not Official Warnings**: Calculated categories (like "Severe", "Critical") represent arbitrary output buckets based on internal logic. They are **not** official climate classifications or governmental emergency warnings.
- **No Unsupported Interpretations**: The agent explicitly avoids making subjective scientific interpretations of data. Results strictly reflect the provided input multiplied by the documented static formulas.

## Output Contract
Outputs are strictly returned as structured dictionaries. 
- **Tool-Specific Fields**: Each tool returns a customized schema reflecting its calculation, including fields like `location_id`, `_score`, `_anomaly`, `contributing_factors`, and `calculation_explanation`.
- **Validation/Error Behavior**: If validation fails during `validate_input()`, the dynamic tool registry intercepts the failure and securely returns `{"error": "Invalid input provided.", "status": "failed"}` or a specific Python exception safely caught and converted to an error dictionary. There is no universal response schema beyond the registry failure wrapper.

## Complete Execution Lifecycle
1. **Input**: A request dictating the tool to use and its structured arguments arrives.
2. **Validation**: The `DynamicToolRegistry` locates the tool and executes `validate_input(input_data)`.
3. **Tool Selection / Registry Execution**: Upon successful validation, the registry securely invokes `execute(input_data)`.
4. **Deterministic Calculation**: The isolated Python logic performs strict arithmetic steps based on the validated inputs.
5. **Structured Result**: A result dictionary is assembled with numeric metrics, threshold categories, and explanations.
6. **Explanation/Provenance Information**: The output includes explicit `calculation_explanation` or `limitations` strings clearly linking the result to the arithmetic formula applied.

## Decision/Rule Transparency (Tool-by-Tool) & Tool-by-Tool Examples

### 1. analyze-climate-exposure
- **Purpose**: Analyze structured climate exposure for a location or asset.
- **Exact Input Fields**: `location_id` (req), `location_name` (opt), `temperature_exposure` (opt bool), `precipitation_exposure` (opt bool), `drought_exposure` (opt bool), `flood_exposure` (opt bool), `extreme_weather_exposure` (opt bool).
- **Validation**: Requires `location_id`. Expects dictionary structure.
- **Exact Output Fields**: `location_id`, `exposure_indicators`, `available_exposure_factors`, `missing_factors`, `normalized_exposure_value`, `structured_findings`, `calculation_explanation`.
- **Exact Calculation**: `normalized_exposure_value = len(active_exposures) / 5.0`
- **Missing-Data Behavior**: Missing boolean flags are tracked in `missing_factors` and do not contribute to `active_exposures`.
- **Assumptions & Limitations**: Unsupplied flags are not treated as actively `False` but strictly as missing.
- **Example**: 
  - **Input**: `{"location_id": "L1", "temperature_exposure": True, "flood_exposure": False}`
  - **Decision Logic**: Validates `L1` -> evaluates 2 provided factors -> counts 1 `True` factor -> 1 / 5 = 0.2.
  - **Output**: `{"location_id": "L1", "exposure_indicators": ["temperature_exposure"], "available_exposure_factors": ["temperature_exposure", "flood_exposure"], "missing_factors": ["drought_exposure", "precipitation_exposure", "extreme_weather_exposure"], "normalized_exposure_value": 0.2, ...}`
  - **Explanation**: 1 out of 5 possible total exposures is active.

### 2. analyze-temperature-risk
- **Purpose**: Calculate deterministic temperature indicators.
- **Exact Input Fields**: `location_id` (req), `observed_temperature` (req), `historical_average` (req), `heat_threshold` (opt).
- **Validation**: Inputs must be numeric types (int/float).
- **Exact Output Fields**: `location_id`, `temperature_anomaly`, `observation_summary`, conditionally `threshold_exceedance`, conditionally `heat_exposure_indicator`.
- **Exact Calculation**: `temperature_anomaly = observed_temperature - historical_average`
- **Exact Thresholds**: If `heat_threshold` supplied: `exceedance = max(0.0, observed_temperature - heat_threshold)`.
- **Missing-Data Behavior**: Missing required fields fails validation immediately.
- **Example**:
  - **Input**: `{"location_id": "L2", "observed_temperature": 35.0, "historical_average": 30.0, "heat_threshold": 32.0}`
  - **Decision Logic**: `35.0 - 30.0 = 5.0` anomaly. `max(0.0, 35.0 - 32.0) = 3.0` exceedance.
  - **Output**: `{"location_id": "L2", "temperature_anomaly": 5.0, "observation_summary": "Observed 35.0 vs historical 30.0.", "threshold_exceedance": 3.0, "heat_exposure_indicator": True, ...}`
  - **Explanation**: The anomaly derives strictly from subtracting historical from observed.

### 3. analyze-precipitation-risk
- **Purpose**: Calculate deterministic precipitation indicators.
- **Exact Input Fields**: `location_id` (req), `observed_precipitation` (req), `historical_precipitation` (req), `precipitation_threshold` (opt).
- **Validation (Negative boundaries)**: Precipitation inputs cannot be negative `< 0`.
- **Zero-Division Protection**: Percentage difference is skipped entirely if `historical_precipitation == 0`.
- **Exact Output Fields**: `location_id`, `precipitation_anomaly`, conditionally `percentage_difference`, conditionally `threshold_exceedance`, conditionally `precipitation_condition`.
- **Exact Calculation**: `anomaly = observed - historical`.
- **Example**:
  - **Input**: `{"location_id": "L3", "observed_precipitation": 120, "historical_precipitation": 100}`
  - **Decision Logic**: `120 - 100 = 20`. `(20 / 100) * 100 = 20%`.
  - **Output**: `{"location_id": "L3", "precipitation_anomaly": 20.0, "percentage_difference": 20.0, ...}`
  - **Explanation**: Mathematical percentage difference applies because history is safely non-zero.

### 4. calculate-drought-risk
- **Purpose**: Compute drought score based on precipitation deficit and dry days.
- **Exact Input Fields**: `precipitation_deficit` (req), `dry_days` (req).
- **Validation**: `dry_days` cannot be `< 0`.
- **Exact Output Fields**: `drought_score`, `contributing_factors`, `applied_thresholds`, `calculation_explanation`, `risk_category`, `limitations`.
- **Exact Weights**: 0.6 for precipitation_deficit, 0.4 for dry_days.
- **Exact Thresholds**: `Severe` (> 50), `Moderate` (> 20), else `Low`.
- **Example**:
  - **Input**: `{"precipitation_deficit": 60, "dry_days": 10}`
  - **Decision Logic**: `(60 * 0.6) + (10 * 0.4) = 36 + 4 = 40.0` -> Moderate.
  - **Output**: `{"drought_score": 40.0, "risk_category": "Moderate", ...}`
  - **Explanation**: Output falls firmly in the moderate threshold boundary (between 20 and 50).

### 5. calculate-flood-risk
- **Purpose**: Compute deterministic flood risk score.
- **Exact Input Fields**: `cumulative_rainfall` (req), `drainage_capacity` (req).
- **Zero-Division Protection**: `drainage_capacity` strictly enforced to be `> 0`.
- **Exact Output Fields**: `flood_risk_score`, `contributing_factors`, `threshold_conditions`, `risk_category`, `calculation_explanation`, `limitations`.
- **Exact Calculation**: `risk_score = (cumulative_rainfall / drainage_capacity) * 100`.
- **Exact Thresholds**: `High` (>= 100), `Medium` (>= 75), else `Low`.
- **Example**:
  - **Input**: `{"cumulative_rainfall": 80, "drainage_capacity": 100}`
  - **Decision Logic**: `(80 / 100) * 100 = 80.0` -> Medium.
  - **Output**: `{"flood_risk_score": 80.0, "risk_category": "Medium", ...}`
  - **Explanation**: Calculates saturation percentage relative to explicit capacity.

### 6. calculate-climate-vulnerability
- **Purpose**: Compute vulnerability score based on population and infrastructure exposures.
- **Exact Input Fields**: `population_exposure` (req), `infrastructure_exposure` (req).
- **Exact Output Fields**: `vulnerability_score`, `factor_contributions`, `formula`, `assumptions`, `category`, `missing_data`, `limitations`.
- **Exact Weights**: 0.5 for population, 0.5 for infrastructure.
- **Exact Thresholds**: `High` (>= 80), `Medium` (>= 40), else `Low`.
- **Example**:
  - **Input**: `{"population_exposure": 50, "infrastructure_exposure": 50}`
  - **Decision Logic**: `(50 * 0.5) + (50 * 0.5) = 50.0` -> Medium.
  - **Output**: `{"vulnerability_score": 50.0, "category": "Medium", "missing_data": [], ...}`
  - **Explanation**: Weights combine uniformly.

### 7. calculate-climate-priority
- **Purpose**: Determine overall priority using hazard, exposure, and vulnerability scores.
- **Exact Input Fields**: `hazard_score` (req), `exposure_score` (req), `vulnerability_score` (req).
- **Exact Output Fields**: `calculated_priority_score`, `contributing_factors`, `formula`, `weights`, `thresholds`, `priority_category`, `explanation`, `limitations`.
- **Exact Weights**: Hazard (0.4), Exposure (0.3), Vulnerability (0.3).
- **Exact Thresholds**: `Critical` (>= 75), `Elevated` (>= 50), else `Standard`.
- **Example**:
  - **Input**: `{"hazard_score": 100, "exposure_score": 100, "vulnerability_score": 100}`
  - **Decision Logic**: `(100 * 0.4) + (100 * 0.3) + (100 * 0.3) = 100.0` -> Critical.
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
