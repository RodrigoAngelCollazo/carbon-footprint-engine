# Enterprise Carbon Footprint Ingestion Engine

[![Compliance Matrix Status](https://img.shields.io/badge/Compliance-ISO%2014064%20%7C%20ISO%2014067-blue)](https://github.com/RodrigoAngelCollazo/carbon-footprint-engine)
[![Audit Audit Trail Status](https://img.shields.io/badge/Data%20Quality-100%25-success)](https://github.com/RodrigoAngelCollazo/carbon-footprint-engine)

A high-integrity, Test-Driven Development (TDD) data governance gateway built under a **Process-as-Code** methodology. This engine ingests, structures, and audits incoming emissions telemetry data, providing structural validation against strict international carbon standards before committing telemetry metrics to long-term storage.

---

## 🏗️ Compliance Data Pipeline Architecture

              [ Streaming Emission Telemetry ]
                             │
                             ▼
     ┌────────────────────────────────────────────────┐
     │          sentinel/guard.py (Pydantic)          │
     ├────────────────────────────────────────────────┤
     │ ✔ ISO 14067: Cradle-to-Grave Product LCA Bounds│
     │ ✔ ISO 14064: Corporate Scope 1, 2, & 3 Auditing│
     └───────────────────────┬────────────────────────┘
                             │
              ┌──────────────┴──────────────┐
              ▼                             ▼
   [ Compliant Payload ]          [ Audit Compliance Breach ]
              │                             │
              ▼                             ▼
┌─────────────────────────────┐┌─────────────────────────────┐
│  Execute DB Upsert Merge    ││  Raise Explicit ValueError  │
│  (TimescaleDB Staging Sync) ││  (Drop Payload & Alert Log) │
└─────────────────────────────┘└─────────────────────────────┘


The system separates incoming tracking models into distinct operational layers to maintain data lineage from raw ingestion right through downstream analytics nodes.

---

## 📊 Implemented International Standards

The validation layer dynamically checks schemas against standardized carbon protocol matrices:

### 1. ISO 14067 — Product Carbon Footprint (PCF)
Tracks life cycle assessment data points across all standard lifecycle stages:
* **`raw_material_kg`**: Upstream resource extraction mass footprint tracking.
* **`production_processing_kwh`**: Utility and manufacturing power draw conversion tracking.
* **`distribution_transport_km`**: Logistics supply chain transport distance metrics.
* **`end_of_life_disposal_kg`**: Final decomposition processing emissions mapping.

### 2. ISO 14064 — Organizational Greenhouse Gas Inventories
Establishes corporate ecosystem tracking boundaries to log organizational impacts:
* **Scope 1 (Direct Emissions):** Tracks site-specific stationary fuel combustion variables (`scope1_direct_combustion_liters`).
* **Scope 2 (Indirect Emissions):** Monitors purchased energy, electricity, and local grid load draws (`scope2_indirect_electricity_kwh`).
* **Scope 3 (Value Chain):** Captures upstream and downstream indirect supply chain metrics (`scope3_value_chain_emissions_co2e`).

---

## 📂 System Manifest

* `sentinel/guard.py` — Immutable Pydantic baseline validation schemas for ISO mapping frameworks.
* `config.json` — Static lookup matrix defining current IPCC greenhouse global emission coefficients.
* `tests/` — Test suites asserting rigorous mathematical calculation bounds for structural boundary exceptions.
* `pyproject.toml` — Automation runner configuration settings for local pipeline testing routines.
