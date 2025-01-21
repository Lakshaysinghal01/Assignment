import unittest
from unittest.mock import patch, mock_open
import main
import json


class TestMain(unittest.TestCase):
    @patch("main.requests.get")
    def test_fetch_data(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = [{"userId": 1, "id": 1, "title": "test", "body": "sample body"}]
        data = main.fetch_data("https://jsonplaceholder.typicode.com/posts", "test_data.json")
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["title"], "test")

    @patch("builtins.open", new_callable=mock_open, read_data=json.dumps([{"userId": 1, "body": "test body"}]))
    def test_analyze_data(self, mock_file):
        total_posts, unique_users, avg_words = main.analyze_data("test_data.json")
        self.assertEqual(total_posts, 1)
        self.assertEqual(unique_users, 1)
        self.assertAlmostEqual(avg_words, 2)

    @patch("builtins.open", new_callable=mock_open)
    def test_generate_summary(self, mock_file):
        main.generate_summary("summary.txt", 10, 5, 15.5)
        mock_file().write.assert_called_with("Average Words per Post: 15.50\n")


if __name__ == "__main__":
    unittest.main()
