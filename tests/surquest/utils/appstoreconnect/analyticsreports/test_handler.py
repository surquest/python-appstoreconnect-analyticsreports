import unittest
import warnings
from surquest.utils.appstoreconnect.analyticsreports.handler import Handler
from surquest.utils.appstoreconnect.analyticsreports.errors import (
    PayloadFormatError,
    NoValidIdsError,
    NoValidUrlsError,
)


class TestHandler(unittest.TestCase):

    def test_extract_ids_valid(self):
        payload = [{"id": "123"}, {"id": "456"}, {"id": "789"}]
        result = Handler.extract_ids(payload)
        assert result == ["123", "456", "789"]

    def test_extract_ids_with_invalid_items(self):
        payload = [{"id": "123"}, {"no_id": "abc"}, None, {"id": None}]
        with warnings.catch_warnings(record=True) as w:
            result = Handler.extract_ids(payload)
            assert result == ["123"]
            assert len(w) == 3  # Warnings for 3 invalid items

    def test_extract_ids_no_valid_ids(self):
        payload = [{"id": None}, {"foo": "bar"}]
        try:
            Handler.extract_ids(payload)
            assert False, "Expected NoValidIdsError to be raised"
        except NoValidIdsError as e:
            assert str(e) == "No valid IDs found in the payload."

    def test_extract_attribute_values_valid(self):
        payload = [
            {"attributes": {"processingDate": "2025-07-27"}},
            {"attributes": {"processingDate": "2025-07-28"}},
        ]
        result = Handler.extract_attribute_values(payload, attribute="processingDate")
        assert result == ["2025-07-27", "2025-07-28"]

    def test_extract_attribute_values_missing_attribute(self):
        payload = [{"attributes": {"other": "value"}}, {"attributes": {}}]
        with warnings.catch_warnings(record=True) as w:
            try:
                Handler.extract_attribute_values(payload, attribute="processingDate")
                assert False, "Expected NoValidUrlsError to be raised"
            except NoValidUrlsError as e:
                assert "No valid `processingDate`" in str(e)
            assert len(w) == 2

    def test_extract_attribute_values_without_attribute(self):
        payload = [
            {"attributes": {"key": "value"}},
            {"attributes": {"another_key": "another_value"}},
        ]
        result = Handler.extract_attribute_values(payload)
        assert result == [{"key": "value"}, {"another_key": "another_value"}]

    def test_deduplicate_data(self):
        data = [
            {"id": "123", "name": "Alice"},
            {"id": "123", "name": "Alice"},
            {"id": "456", "name": "Bob"},
        ]
        result = Handler.deduplicate_data(data)
        assert isinstance(result, list)
        assert len(result) == 2
        assert {"id": "123", "name": "Alice"} in result
        assert {"id": "456", "name": "Bob"} in result
