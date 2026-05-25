import unittest
import os
from sentinel.guard import SentinelGuard

class TestSentinelGuard(unittest.TestCase):
    def setUp(self):
        # Resolve path to the default config.json
        dir_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.config_path = os.path.join(dir_path, "config.json")
        self.guard = SentinelGuard(self.config_path)

    def test_payload_within_bounds_passes(self):
        """
        Validates that a telemetry payload where all metrics are within bounds successfully evaluates to True.
        """
        payload = {
            "pm25": 10.0,
            "no2": 30.0,
            "so2": 50.0
        }
        self.assertTrue(self.guard.evaluate_payload(payload))

    def test_pm25_violation_raises_error_or_returns_false(self):
        """
        Validates that a telemetry payload where pm25 exceeds limit returns False.
        """
        payload = {
            "pm25": 20.0,  # limit: 15.0
            "no2": 30.0,
            "so2": 50.0
        }
        self.assertFalse(self.guard.evaluate_payload(payload))

    def test_malformed_payload_schema_interception(self):
        """
        Validates that malformed telemetry payloads trigger schema validation exceptions (ValueError).
        """
        # Constraint 1: Non-dictionary payload
        with self.assertRaises(ValueError):
            self.guard.evaluate_payload("not-a-dict")

        # Constraint 2: Missing key 'so2'
        with self.assertRaises(ValueError):
            self.guard.evaluate_environmental_payload({
                "pm25": 10.0,
                "no2": 30.0
            })

        # Constraint 3: Non-numeric value type
        with self.assertRaises(ValueError):
            self.guard.evaluate_environmental_payload({
                "pm25": 10.0,
                "no2": 30.0,
                "so2": "high"
            })
