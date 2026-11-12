"""Detect unusual readings with a robust median absolute deviation score."""

import argparse
import csv
from pathlib import Path
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


def read_csv_column(path: str | Path, column: str) -> list[float]:
    """Read one named column of numeric sensor readings from a CSV file."""
    with Path(path).open(newline="", encoding="utf-8") as csv_file:
        reader = csv.DictReader(csv_file)
        if reader.fieldnames is None or column not in reader.fieldnames:
            raise ValueError(f"CSV column not found: {column}")

        readings = []
        for row_number, row in enumerate(reader, start=1):
            try:
                readings.append(float(row[column]))
            except (TypeError, ValueError) as error:
                raise ValueError(
                    f"Invalid numeric value in column {column!r} at data row {row_number}"
                ) from error
        return readings


def main() -> None:
    parser = argparse.ArgumentParser(description="Detect anomalies in sensor readings.")
    parser.add_argument("--csv", type=Path, help="CSV file containing sensor readings")
    parser.add_argument("--column", help="CSV column containing numeric readings")
    args = parser.parse_args()

    if args.csv is None and args.column is None:
        sensor_readings = [20, 21, 19, 20, 22, 95]
        anomalies = detect_anomalies(sensor_readings)
        print(f"Anomaly indices (0-based): {anomalies}")
        return
    if args.csv is None:
        parser.error("--column requires --csv")
    if args.column is None:
        parser.error("--column is required with --csv")

    try:
        readings = read_csv_column(args.csv, args.column)
    except (OSError, ValueError) as error:
        parser.error(str(error))

    anomalies = detect_anomalies(readings)
    if not anomalies:
        print("No anomalies found.")
        return
    summary = ", ".join(f"{index + 1}, {readings[index]}" for index in anomalies)
    print(f"Anomalies (data row, value): {summary}")


if __name__ == "__main__":
    main()
