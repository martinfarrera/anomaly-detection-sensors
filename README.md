# Sensor Anomaly Detection

A dependency-free data science example that flags unusual sensor readings with the **median absolute deviation (MAD)**, a robust alternative to standard-deviation-based z-scores. It can analyze the built-in sample or a numeric column in your own CSV.

## Quick start

Requires Python 3.10+.

```bash
python src/anomaly_detector.py
python -m unittest discover -v
```

The built-in sample prints:

```text
Anomaly indices (0-based): [5]
```

## Analyze a CSV

Pass the file and the exact name of its numeric column:

```bash
python src/anomaly_detector.py --csv sensor.csv --column temperature
```

For a column with readings `20, 21, 19, 20, 22, 95`, the command reports:

```text
Anomalies (data row, value): 6, 95.0
```

Rows are numbered from 1, excluding the header. A missing column or nonnumeric reading is reported on stderr and exits with status 2; the command prints no partial results.

The default modified z-score threshold is 3.5. If the MAD is zero, readings that differ from the median are returned as anomalies. This is an illustrative detector, not a calibrated production monitoring system; validate thresholds against the sensor and operating context.
