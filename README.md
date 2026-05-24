# Inference Sentinel Guard Engine

[![(Build Matrix Status)](https://github.com/RodrigoAngelCollazo/eis-automation-sentinel/actions/workflows/ci-cd.yml/badge.svg)](https://github.com/RodrigoAngelCollazo/eis-automation-sentinel/actions)
[![(Data Coverage)](https://img.shields.io/badge/Coverage-93%%25-success)](https://github.com/RodrigoAngelCollazo/eis-automation-sentinel)

High-integrity data governance layer utilizing **Pydantic schema validation** to secure model inference pipelines. 
This engine intercepts incoming payload telemetry to block data anomalies, metric drift, and out-of-bounds latency spikes.

## ?? Core Workspace Architecture
* `sentinel/guard.py`: Pydantic telemetry models and threshold controls.
* `tests/`: Structural test cases verifying float edge cases, zero-values, and large tokens.
* `config.json`: Production operational limits configuration matrix.
* `pyproject.toml`: Pytest configuration layers and test coverage rules.
