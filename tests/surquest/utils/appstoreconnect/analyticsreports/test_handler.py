import unittest
from src.surquest.utils.appstoreconnect.analyticsreports.handler import Handler
from src.surquest.utils.appstoreconnect.analyticsreports.errors import PayloadFormatError, NoValidIdsError, NoValidUrlsError

class TestHandler(unittest.TestCase):

    def test_extract_ids_valid_payload(self):
        payload = {
            "data": [
                {"id": "123", "type": "reportRequests"},
                {"id": "456", "type": "reportRequests"},
                {"id": "789", "type": "reportRequests"}
            ]
        }
        ids = Handler.extract_ids(payload)
        self.assertEqual(ids, ["123", "456", "789"])

    def test_extract_ids_empty_data(self):
        payload = {"data": []}
        with self.assertRaises(NoValidIdsError):
            Handler.extract_ids(payload)

    def test_extract_ids_missing_data(self):
        payload = {}
        with self.assertRaises(PayloadFormatError):
            Handler.extract_ids(payload)

    def test_extract_ids_data_not_list(self):
        payload = {"data": "not a list"}
        with self.assertRaises(PayloadFormatError):
            Handler.extract_ids(payload)

    def test_extract_ids_items_not_dict(self):
        payload = {"data": ["not a dict", {"id": "123"}]}
        ids = Handler.extract_ids(payload)
        self.assertEqual(ids, ["123"])

    def test_extract_ids_missing_id(self):
        payload = {"data": [{"type": "reportRequests"}, {"id": "123"}]}
        ids = Handler.extract_ids(payload)
        self.assertEqual(ids, ["123"])

    def test_extract_ids_null_id(self):
        payload = {"data": [{"id": None}, {"id": "123"}]}
        ids = Handler.extract_ids(payload)
        self.assertEqual(ids, ["123"])

    def test_extract_attribute_values_valid_payload(self):
        payload = {
            "data": [
                {"attributes": {"url": "http://example.com/report1"}},
                {"attributes": {"url": "http://example.com/report2"}}
            ]
        }
        urls = Handler.extract_attribute_values(payload, "url")
        self.assertEqual(urls, ["http://example.com/report1", "http://example.com/report2"])

    def test_extract_attribute_values_empty_data(self):
        payload = {"data": []}
        with self.assertRaises(NoValidUrlsError):
            Handler.extract_attribute_values(payload, "url")

    def test_extract_attribute_values_missing_data(self):
        payload = {}
        with self.assertRaises(PayloadFormatError):
            Handler.extract_attribute_values(payload, "url")

    def test_extract_attribute_values_data_not_list(self):
        payload = {"data": "not a list"}
        with self.assertRaises(PayloadFormatError):
            Handler.extract_attribute_values(payload, "url")

    def test_extract_attribute_values_items_not_dict(self):
        payload = {"data": ["not a dict", {"attributes": {"url": "http://example.com/report1"}}]}
        urls = Handler.extract_attribute_values(payload, "url")
        self.assertEqual(urls, ["http://example.com/report1"])

    def test_extract_attribute_values_missing_attributes(self):
        payload = {"data": [{"type": "report"}, {"attributes": {"url": "http://example.com/report1"}}]}
        urls = Handler.extract_attribute_values(payload, "url")
        self.assertEqual(urls, ["http://example.com/report1"])

    def test_extract_attribute_values_attributes_not_dict(self):
        payload = {"data": [{"attributes": "not a dict"}, {"attributes": {"url": "http://example.com/report1"}}]}
        urls = Handler.extract_attribute_values(payload, "url")
        self.assertEqual(urls, ["http://example.com/report1"])

    def test_extract_attribute_values_missing_attribute(self):
        payload = {"data": [{"attributes": {"other_attr": "value"}}, {"attributes": {"url": "http://example.com/report1"}}]}
        urls = Handler.extract_attribute_values(payload, "url")
        self.assertEqual(urls, ["http://example.com/report1"])

    def test_extract_attribute_values_empty_attribute(self):
        payload = {"data": [{"attributes": {"url": ""}}, {"attributes": {"url": "http://example.com/report1"}}]}
        urls = Handler.extract_attribute_values(payload, "url")
        self.assertEqual(urls, ["http://example.com/report1"])
