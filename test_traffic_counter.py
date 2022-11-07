import unittest
from TrafficCounterClass import TrafficCounter


class TestTrafficCounter(unittest.TestCase):

    def test_empty_file(self):
        filename = "test/empty.txt"
        traffic_obj = TrafficCounter(filename)
        self.assertEqual(traffic_obj.get_total_cars(), 0)
        self.assertEqual(traffic_obj.get_count_daywise(), "")
        self.assertEqual(traffic_obj.get_top_3_hours(), "Can't find top 3")
        self.assertEqual(traffic_obj.get_least_consecutive_hours(), "No contigous interval found")

    def test_wrong_format_file(self):

        filename = "test/wrong_format.txt"
        traffic_obj = TrafficCounter(filename)
        # Only records with correct format should be considered
        self.assertEqual(traffic_obj.get_total_cars(), 88)

    def test_short_file(self):

        filename = "test/file_2_record.txt"
        traffic_obj = TrafficCounter(filename)
        self.assertEqual(traffic_obj.get_total_cars(), 17)
        self.assertEqual(traffic_obj.get_top_3_hours(), "Can't find top 3")
        self.assertEqual(traffic_obj.get_least_consecutive_hours(), "No contigous interval found")

    # test for file with no continuous 1.5 hour interval
    def test_no_contiguous_interval(self):

        filename = "test/no_contiguous.txt"
        traffic_obj = TrafficCounter(filename)
        self.assertNotEqual(traffic_obj.get_top_3_hours(), "Can't find top 3")
        self.assertEqual(traffic_obj.get_least_consecutive_hours(), "No contigous interval found")


if __name__ == '__main__':
    unittest.main()