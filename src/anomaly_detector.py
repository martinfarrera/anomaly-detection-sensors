"""Detect unusual readings with a robust median absolute deviation score."""

from statistics import median


def detect_anomalies(readings: list[float], threshold: float = 3.5) -> list[int]:
    """Return indices whose modified z-score exceeds ``threshold``.

    When every reading is identical (MAD is zero), any differing reading is
    treated as an anomaly.
    """
    if threshold <= 0:
        raise ValueError("threshold must be positive")
    if not readings:
        return []

    center = median(readings)
    mad = median([abs(value - center) for value in readings])
    if mad == 0:
        return [index for index, value in enumerate(readings) if value != center]

    return [
        index
        for index, value in enumerate(readings)
        if abs(0.6745 * (value - center) / mad) > threshold
    ]


if __name__ == "__main__":
    sensor_readings = [20, 21, 19, 20, 22, 95]
    anomalies = detect_anomalies(sensor_readings)
    print(f"Anomaly indices (0-based): {anomalies}")
