# Explainability

This document details the calculations for every tool.

### analyze-climate-exposure
- **Purpose**: Analyze structured climate exposure for a location.
- **Calculations**: Sums up boolean existence of exposure flags (e.g. `temperature_exposure`) and normalizes by number of available factors.
- **Limitations**: Only analyzes supplied exposure data.

### analyze-temperature-risk
- **Purpose**: Calculate temperature indicators.
- **Formulas**: `temperature_anomaly = observed_temperature - historical_average`
- **Assumptions**: Uses exact values provided.

### analyze-precipitation-risk
- **Purpose**: Calculate precipitation indicators.
- **Formulas**: `precipitation_anomaly = observed_precipitation - historical_precipitation`
- **Limitations**: Zero historical precipitation is handled safely.

### calculate-drought-risk
- **Purpose**: Compute drought score.
- **Formulas**: Weighted score based on `precipitation_deficit` and `dry_days`.

### calculate-flood-risk
- **Purpose**: Compute flood risk.
- **Formulas**: `risk_score = (cumulative_rainfall / drainage_capacity) * 100`

### calculate-climate-vulnerability
- **Purpose**: Compute vulnerability score.
- **Formulas**: `vulnerability_score = (population_exposure * 0.5) + (infrastructure_exposure * 0.5)`

### calculate-climate-priority
- **Purpose**: Determine overall priority.
- **Formulas**: `priority_score = (hazard_score * 0.4) + (exposure_score * 0.3) + (vulnerability_score * 0.3)`
