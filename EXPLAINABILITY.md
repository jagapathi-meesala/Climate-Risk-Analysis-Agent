# Explainability

This document details the calculations, validations, and limitations for every tool to ensure full transparency of the deterministic logic.

### 1. analyze-climate-exposure
- **Purpose**: Analyze structured climate exposure for a location.
- **Inputs**: `location_id` (required), `location_name`, `temperature_exposure`, `precipitation_exposure`, `drought_exposure`, `flood_exposure`, `extreme_weather_exposure`.
- **Outputs**: `location_id`, `exposure_indicators`, `available_exposure_factors`, `missing_factors`, `normalized_exposure_value`, `structured_findings`, `calculation_explanation`.
- **Formulas & Weights**: `normalized_exposure_value = (count of active boolean exposure flags) / (total possible flags)`. All 5 standard factors carry equal weight (0.2 each).
- **Thresholds**: None explicitly categorized.
- **Assumptions**: Missing exposure flags are assumed to be unverified, not implicitly `False`.
- **Missing-Data Behavior**: Missing boolean flags are tracked in `missing_factors` and do not contribute to `active_exposures`.
- **Validation Behavior**: Requires `location_id`. `input_data` must be a dictionary.
- **Limitations**: Only analyzes supplied exposure data; makes no external API calls to discover missing attributes.

### 2. analyze-temperature-risk
- **Purpose**: Calculate deterministic temperature indicators.
- **Inputs**: `location_id`, `observed_temperature`, `historical_average` (all required), `heat_threshold` (optional).
- **Outputs**: `location_id`, `temperature_anomaly`, `observation_summary`, and conditionally `threshold_exceedance` and `heat_exposure_indicator`.
- **Formulas**: `temperature_anomaly = observed_temperature - historical_average`. If threshold is provided: `threshold_exceedance = max(0.0, observed_temperature - heat_threshold)`.
- **Thresholds**: Evaluated only if a user-supplied `heat_threshold` is provided. Exceedance sets `heat_exposure_indicator` to `True`.
- **Assumptions**: Uses exact numeric values provided. No unit conversion is automatically performed.
- **Missing-Data Behavior**: Missing required fields result in a validation error rather than assuming defaults.
- **Validation Behavior**: Requires numeric inputs for temperatures.
- **Limitations**: Calculations are strictly arithmetical and do not constitute an official heat warning.

### 3. analyze-precipitation-risk
- **Purpose**: Calculate deterministic precipitation indicators.
- **Inputs**: `location_id`, `observed_precipitation`, `historical_precipitation` (all required), `precipitation_threshold` (optional).
- **Outputs**: `location_id`, `precipitation_anomaly`, `percentage_difference`, `threshold_exceedance`, `precipitation_condition`.
- **Formulas**: `precipitation_anomaly = observed_precipitation - historical_precipitation`. `percentage_difference = (anomaly / historical_precipitation) * 100`. 
- **Thresholds**: If `precipitation_threshold` is provided, `precipitation_condition = "high" if exceedance > 0 else "normal"`.
- **Assumptions**: Precipitation values cannot be negative.
- **Missing-Data Behavior**: Safely handles zero `historical_precipitation` by omitting the `percentage_difference` calculation to prevent division-by-zero errors.
- **Validation Behavior**: Inputs must be >= 0 numeric values.
- **Limitations**: Analyzes only the supplied indicators and makes no hydrological predictions.

### 4. calculate-drought-risk
- **Purpose**: Compute drought score based on precipitation deficit and dry days.
- **Inputs**: `precipitation_deficit`, `dry_days` (both required).
- **Outputs**: `drought_score`, `contributing_factors`, `applied_thresholds`, `risk_category`.
- **Formulas & Weights**: `score = (precipitation_deficit * 0.6) + (dry_days * 0.4)`.
- **Thresholds**: `Severe` (> 50), `Moderate` (> 20), else `Low`.
- **Assumptions**: The deficit and dry days use standardized numeric scales provided by the user.
- **Missing-Data Behavior**: Requires both factors; fails validation safely if either is missing.
- **Validation Behavior**: `dry_days` cannot be negative.
- **Limitations**: Result is a deterministically calculated score and NOT an official drought classification.

### 5. calculate-flood-risk
- **Purpose**: Compute deterministic flood risk score.
- **Inputs**: `cumulative_rainfall`, `drainage_capacity` (both required).
- **Outputs**: `flood_risk_score`, `contributing_factors`, `threshold_conditions`, `risk_category`.
- **Formulas**: `risk_score = (cumulative_rainfall / drainage_capacity) * 100`.
- **Thresholds**: `High` (>= 100), `Medium` (>= 75), else `Low`.
- **Assumptions**: Inputs represent compatible standardized units (e.g., mm/hr).
- **Missing-Data Behavior**: Fails safely if either factor is missing.
- **Validation Behavior**: Prevents division by zero by validating that `drainage_capacity > 0`. Inputs must not be negative.
- **Limitations**: Does not claim an actual flood is occurring. Only analyzes supplied structured indicators.

### 6. calculate-climate-vulnerability
- **Purpose**: Compute vulnerability score based on population and infrastructure exposures.
- **Inputs**: `population_exposure`, `infrastructure_exposure` (both required).
- **Outputs**: `vulnerability_score`, `factor_contributions`, `category`, `missing_data`.
- **Formulas & Weights**: `vulnerability_score = (population_exposure * 0.5) + (infrastructure_exposure * 0.5)`.
- **Thresholds**: `High` (>= 80), `Medium` (>= 40), else `Low`.
- **Assumptions**: Equal weight given to population and infrastructure exposure metrics.
- **Missing-Data Behavior**: Returns empty `missing_data` list if complete. Validation fails if required parameters are missing.
- **Validation Behavior**: Requires numeric types for both inputs.
- **Limitations**: Not an internationally standardized climate vulnerability index. Avoids subjective judgments.

### 7. calculate-climate-priority
- **Purpose**: Determine overall priority using hazard, exposure, and vulnerability scores.
- **Inputs**: `hazard_score`, `exposure_score`, `vulnerability_score` (all required).
- **Outputs**: `calculated_priority_score`, `contributing_factors`, `weights`, `thresholds`, `priority_category`.
- **Formulas & Weights**: `priority_score = (hazard_score * 0.4) + (exposure_score * 0.3) + (vulnerability_score * 0.3)`.
- **Thresholds**: `Critical` (>= 75), `Elevated` (>= 50), else `Standard`.
- **Assumptions**: Inputs are pre-calculated standardized metrics on a 0-100 scale.
- **Missing-Data Behavior**: Validation rejects requests lacking any of the three required scores.
- **Validation Behavior**: Ensures numeric inputs.
- **Limitations**: Not an industry-standard score. No machine learning used. Internal priority metric only.
