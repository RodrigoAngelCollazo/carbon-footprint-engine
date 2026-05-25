import os
import json
from pydantic import BaseModel, Field, field_validator, ValidationError, ConfigDict

class AirQualityMetrics(BaseModel):
    model_config = ConfigDict(frozen=True)
    pm25: float = Field(...)
    no2: float = Field(...)
    so2: float = Field(...)

    @field_validator('pm25')
    @classmethod
    def check_pm25(cls, v):
        if v > 15.0:
            raise ValueError("CRITICAL ENVIRONMENTAL BREACH: PM2.5 above ceiling limits.")
        return v

    @field_validator('no2')
    @classmethod
    def check_no2(cls, v):
        if v > 40.0:
            raise ValueError("CRITICAL ENVIRONMENTAL BREACH: NO2 above ceiling limits.")
        return v

    @field_validator('so2')
    @classmethod
    def check_so2(cls, v):
        if v > 75.0:
            raise ValueError("CRITICAL ENVIRONMENTAL BREACH: SO2 above ceiling limits.")
        return v

class WaterQualityMetrics(BaseModel):
    model_config = ConfigDict(frozen=True)
    ph: float = Field(...)
    dissolved_oxygen: float = Field(...)
    turbidity: float = Field(...)

    @field_validator('ph')
    @classmethod
    def check_ph(cls, v):
        if v < 6.5 or v > 8.5:
            raise ValueError("CRITICAL ENVIRONMENTAL BREACH: pH out of regulatory safety range.")
        return v

    @field_validator('dissolved_oxygen')
    @classmethod
    def check_do(cls, v):
        if v < 5.0:
            raise ValueError("CRITICAL ENVIRONMENTAL BREACH: Dissolved Oxygen below floor limits.")
        return v

    @field_validator('turbidity')
    @classmethod
    def check_turbidity(cls, v):
        if v > 50.0:
            raise ValueError("CRITICAL ENVIRONMENTAL BREACH: Turbidity above ceiling limits.")
        return v

class SentinelGuard:
    def __init__(self, config_path=None):
        self.config = {}
        if config_path and os.path.exists(config_path):
            with open(config_path, 'r') as f:
                self.config = json.load(f)

    def evaluate_environmental_payload(self, payload: dict):
        """
        Evaluates an environmental telemetry payload against regulatory limits.
        """
        if not isinstance(payload, dict):
             raise ValueError("Payload must be a dictionary.")

        try:
            # Try to validate as Air Quality
            if all(k in payload for k in ['pm25', 'no2', 'so2']):
                return AirQualityMetrics(**payload)
            # Try to validate as Water Quality
            elif all(k in payload for k in ['ph', 'dissolved_oxygen', 'turbidity']):
                return WaterQualityMetrics(**payload)
            else:
                raise ValueError("Invalid payload schema: Missing required environmental metrics.")
        except ValidationError as e:
            # Extract the custom error message if it exists
            for error in e.errors():
                if error['type'] in ('value_error', 'assertion_error'):
                    raise ValueError(error['msg'])
            raise ValueError(str(e))
        except Exception as e:
            raise ValueError(str(e))

    def evaluate_payload(self, payload: dict) -> bool:
        """
        Legacy support for boolean evaluation.
        """
        try:
            self.evaluate_environmental_payload(payload)
            return True
        except:
            if not isinstance(payload, dict):
                raise ValueError("Payload must be a dictionary.")
            return False

def evaluate_environmental_payload(payload_dict):
    guard = SentinelGuard()
    return guard.evaluate_environmental_payload(payload_dict)
