from __future__ import annotations


def _speed(distance_m: float, elapsed_ms: int) -> float:
    return round(distance_m / (elapsed_ms / 1000) * 3.6, 1)


def legacy_speed(previous: dict, current: dict) -> dict:
    elapsed_ms = current["sensor_timestamp_ms"] - previous["sensor_timestamp_ms"]
    if elapsed_ms <= 0:
        return {
            "accepted": False,
            "clock": "sensor",
            "elapsed_ms": elapsed_ms,
            "speed_kmh": None,
            "reason": "non_monotonic_time",
        }
    return {
        "accepted": True,
        "clock": "sensor",
        "elapsed_ms": elapsed_ms,
        "speed_kmh": _speed(current["distance_from_previous_m"], elapsed_ms),
        "reason": None,
    }


def speed_with_fallback(previous: dict, current: dict) -> dict:
    sensor_elapsed = current["sensor_timestamp_ms"] - previous["sensor_timestamp_ms"]
    if sensor_elapsed > 0:
        elapsed_ms = sensor_elapsed
        clock = "sensor"
    else:
        elapsed_ms = current["wall_timestamp_ms"] - previous["wall_timestamp_ms"]
        clock = "wall_fallback"

    if elapsed_ms <= 0:
        return {
            "accepted": False,
            "clock": clock,
            "elapsed_ms": elapsed_ms,
            "speed_kmh": None,
            "reason": "non_monotonic_time",
        }
    return {
        "accepted": True,
        "clock": clock,
        "elapsed_ms": elapsed_ms,
        "speed_kmh": _speed(current["distance_from_previous_m"], elapsed_ms),
        "reason": None,
    }
