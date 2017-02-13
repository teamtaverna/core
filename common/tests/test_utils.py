from django.test import TestCase

from ..utils import timestamp_seconds


class UtilsTest(TestCase):
    """Test utils module."""

    def test_timestamp_seconds(self):
        timestamps = set()
        [timestamps.add(timestamp_seconds()) for _ in range(5)]

        self.assertEqual(5, len(timestamps))