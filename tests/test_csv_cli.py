import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]


class CsvCliTests(unittest.TestCase):
    def run_cli(self, *arguments):
        return subprocess.run(
            [sys.executable, "src/anomaly_detector.py", *map(str, arguments)],
            cwd=PROJECT_ROOT,
            capture_output=True,
            text=True,
            check=False,
        )

    def test_reads_csv_column_and_reports_one_based_data_row(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            csv_path = Path(temp_dir) / "sensor.csv"
            csv_path.write_text(
                "temperature\n20\n21\n19\n20\n22\n95\n",
                encoding="utf-8",
            )

            result = self.run_cli("--csv", csv_path, "--column", "temperature")

        self.assertEqual(result.returncode, 0)
        self.assertEqual(result.stdout, "Anomalies (data row, value): 6, 95.0\n")
        self.assertEqual(result.stderr, "")

    def test_reports_missing_column_without_partial_output(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            csv_path = Path(temp_dir) / "sensor.csv"
            csv_path.write_text("temperature\n20\n", encoding="utf-8")

            result = self.run_cli("--csv", csv_path, "--column", "humidity")

        self.assertEqual(result.returncode, 2)
        self.assertEqual(result.stdout, "")
        self.assertEqual(
            result.stderr,
            "usage: anomaly_detector.py [-h] [--csv CSV] [--column COLUMN]\n"
            "anomaly_detector.py: error: CSV column not found: humidity\n",
        )

    def test_reports_non_numeric_value_and_row_without_partial_output(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            csv_path = Path(temp_dir) / "sensor.csv"
            csv_path.write_text("temperature\n20\nnot-a-number\n", encoding="utf-8")

            result = self.run_cli("--csv", csv_path, "--column", "temperature")

        self.assertEqual(result.returncode, 2)
        self.assertEqual(result.stdout, "")
        self.assertEqual(
            result.stderr,
            "usage: anomaly_detector.py [-h] [--csv CSV] [--column COLUMN]\n"
            "anomaly_detector.py: error: Invalid numeric value in column "
            "'temperature' at data row 2\n",
        )

    def test_no_arguments_preserves_original_demo_output(self):
        result = self.run_cli()

        self.assertEqual(result.returncode, 0)
        self.assertEqual(result.stdout, "Anomaly indices (0-based): [5]\n")
        self.assertEqual(result.stderr, "")


if __name__ == "__main__":
    unittest.main()
