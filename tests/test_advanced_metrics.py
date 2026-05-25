import unittest
from sentinel.guard import SentinelGuard

class TestEnvironmentalMetrics(unittest.TestCase):
    def setUp(self):
        self.guard = SentinelGuard()

    def test_compliant_ecosystem_telemetry(self):
        """Successful parsing of fully compliant ecosystem telemetry inputs."""
        air_payload = {
            "pm25": 10.0,
            "no2": 30.0,
            "so2": 50.0
        }
        water_payload = {
            "ph": 7.0,
            "dissolved_oxygen": 7.5,
            "turbidity": 20.0
        }
        self.assertTrue(self.guard.evaluate_payload(air_payload))
        self.assertTrue(self.guard.evaluate_payload(water_payload))

    def test_acidic_water_breach(self):
        """Automated catching of acidic water breaches (pH below bounds)."""
        payload = {
            "ph": 5.0,  # Below 6.5
            "dissolved_oxygen": 7.5,
            "turbidity": 20.0
        }
        with self.assertRaisesRegex(ValueError, "CRITICAL ENVIRONMENTAL BREACH: pH out of regulatory safety range"):
            self.guard.evaluate_environmental_payload(payload)

    def test_alkaline_water_breach(self):
        """Automated catching of alkaline water breaches (pH above bounds)."""
        payload = {
            "ph": 9.5,  # Above 8.5
            "dissolved_oxygen": 7.5,
            "turbidity": 20.0
        }
        with self.assertRaisesRegex(ValueError, "CRITICAL ENVIRONMENTAL BREACH: pH out of regulatory safety range"):
            self.guard.evaluate_environmental_payload(payload)

    def test_toxic_air_quality_event(self):
        """Automated catching of toxic air quality events (PM2.5 above ceiling limits)."""
        payload = {
            "pm25": 20.0,  # Above 15.0
            "no2": 30.0,
            "so2": 50.0
        }
        with self.assertRaisesRegex(ValueError, "CRITICAL ENVIRONMENTAL BREACH: PM2.5 above ceiling limits"):
            self.guard.evaluate_environmental_payload(payload)

    def test_dissolved_oxygen_floor_breach(self):
        """Automated catching of low dissolved oxygen."""
        payload = {
            "ph": 7.0,
            "dissolved_oxygen": 4.0,  # Below 5.0
            "turbidity": 20.0
        }
        with self.assertRaisesRegex(ValueError, "CRITICAL ENVIRONMENTAL BREACH: Dissolved Oxygen below floor limits"):
            self.guard.evaluate_environmental_payload(payload)

    def test_turbidity_ceiling_breach(self):
        """Automated catching of high turbidity."""
        payload = {
            "ph": 7.0,
            "dissolved_oxygen": 7.5,
            "turbidity": 60.0  # Above 50.0
        }
        with self.assertRaisesRegex(ValueError, "CRITICAL ENVIRONMENTAL BREACH: Turbidity above ceiling limits"):
            self.guard.evaluate_environmental_payload(payload)
