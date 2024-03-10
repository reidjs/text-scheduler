import unittest
from send_scheduled_messages import parse_human_datetime
from datetime import datetime


def datetime_to_string(datetime):
    return datetime.strftime("%m/%d/%Y, %H:%M:%S")


class TestParseDatetime(unittest.TestCase):
    def test_parse_human_datetime(self):
        self.assertEqual(
            datetime_to_string(parse_human_datetime("now")),
            datetime_to_string(datetime.now()),
        )
        self.assertEqual(
            datetime_to_string(parse_human_datetime("asap")),
            datetime_to_string(datetime.now()),
        )
        self.assertEqual(
            datetime_to_string(parse_human_datetime("March 10, 2024 5:00PM")),
            datetime_to_string(datetime(2024, 3, 10, 17, 0)),
        )
        self.assertEqual(
            datetime_to_string(parse_human_datetime("December 03, 2024 3:21AM")),
            datetime_to_string(datetime(2024, 12, 3, 3, 21)),
        )


if __name__ == "__main__":
    unittest.main()
