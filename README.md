# Sensor Anomaly Detection

A tiny, dependency-free data science example that flags unusual sensor readings with the **median absolute deviation (MAD)**, a robust alternative to standard-deviation-based z-scores.

## Run

Requires Python 3.10+.

```bash
python src/anomaly_detector.py
python -m unittest discover -v
```

Expected demo output:

```text
Anomaly indices (0-based): [5]
```

Use the function directly with your own numeric readings:

```python
from src.anomaly_detector import detect_anomalies

print(detect_anomalies([20, 21, 19, 20, 22, 95]))  # [5]
```

The default modified z-score threshold is 3.5. If the MAD is zero, readings that differ from the median are returned as anomalies. This is a small illustrative detector, not a calibrated production monitoring system; validate thresholds against the sensor and operating context.
