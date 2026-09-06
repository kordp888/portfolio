from __future__ import annotations

import copy
import json
import unittest
from pathlib import Path

from evidence.onda.speed_fallback import legacy_speed, speed_with_fallback


ROOT = Path(__file__).resolve().parent


def load(name: str) -> dict:
    return json.loads((ROOT / name).read_text(encoding="utf-8"))


class SpeedFallbackEvidenceTest(unittest.TestCase):
    def setUp(self):
        self.samples = load("gps.samples.synthetic.json")["samples"]
        self.previous, self.current = self.samples

    def test_published_legacy_trace_matches(self):
        self.assertEqual(load("expected.legacy.json"), legacy_speed(self.previous, self.current))

    def test_published_fixed_trace_matches(self):
        self.assertEqual(
            load("expected.fixed.json"),
            speed_with_fallback(self.previous, self.current),
        )

    def test_manifest_separates_observed_reconstructed_and_verified(self):
        manifest = load("manifest.json")
        self.assertEqual("synthetic", manifest["data_class"])
        self.assertEqual(
            ["Observed", "Reconstructed", "Verified"],
            [item["classification"] for item in manifest["evidence"]],
        )

    def test_monotonic_sensor_clock_is_preferred(self):
        current = copy.deepcopy(self.current)
        current["sensor_timestamp_ms"] = self.previous["sensor_timestamp_ms"] + 1000
        result = speed_with_fallback(self.previous, current)
        self.assertTrue(result["accepted"])
        self.assertEqual("sensor", result["clock"])
        self.assertEqual(30.0, result["speed_kmh"])

    def test_both_non_monotonic_clocks_are_rejected(self):
        current = copy.deepcopy(self.current)
        current["wall_timestamp_ms"] = self.previous["wall_timestamp_ms"]
        result = speed_with_fallback(self.previous, current)
        self.assertFalse(result["accepted"])
        self.assertIsNone(result["speed_kmh"])

    def test_fixture_contains_no_geographic_coordinates(self):
        text = json.dumps(load("gps.samples.synthetic.json"))
        self.assertNotIn("latitude", text)
        self.assertNotIn("longitude", text)


if __name__ == "__main__":
    unittest.main()
