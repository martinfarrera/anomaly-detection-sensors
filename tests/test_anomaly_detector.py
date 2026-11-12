import unittest

from src.anomaly_detector import detect_anomalies


class DetectAnomaliesTests(unittest.TestCase):
    def test_detects_spike_and_keeps_typical_sensor_readings(self):
        self.assertEqual(detect_anomalies([20, 21, 19, 20, 22, 95]), [5])

    def test_detects_outlier_when_median_absolute_deviation_is_zero(self):
        self.assertEqual(detect_anomalies([10, 10, 10, 10, 100]), [4])


if __name__ == "__main__":
    unittest.main()
