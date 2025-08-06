import unittest
import tempfile
import os
import shutil
import json
import csv
import warnings
from surquest.utils.appstoreconnect.analyticsreports.handler import Handler
from surquest.utils.appstoreconnect.analyticsreports.errors import (
    PayloadFormatError,
    NoValidIdsError,
    NoValidUrlsError,
)


class TestHandler(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.temp_dir)

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
            {"id": "123", "name": "Alice", "age": 30.5},
            {"id": "456", "name": "Bob", "age": "25"},
            {"id": "123", "name": "Alice", "age": "30.5"},
            {"id": "123", "name": "Alice", "age": "30.5"},
            {"id": "456", "name": "Bob", "age": 25},
        ]
        result = Handler.deduplicate_data(data)
        assert isinstance(result, list)
        assert len(result) == 2
        assert {"id": 123, "name": "Alice", "age": 30.5} in result
        assert {"id": 456, "name": "Bob", "age": 25} in result

    def test_create_directory_creates_dir(self):
        nested_dir = os.path.join(self.temp_dir, "subdir1", "subdir2")
        file_path = os.path.join(nested_dir, "file.txt")

        assert not os.path.exists(nested_dir)

        Handler.create_directory(file_path)

        assert os.path.exists(nested_dir)
        assert os.path.isdir(nested_dir)

    def test_create_directory_existing_dir(self):
        existing_dir = os.path.join(self.temp_dir, "existing_dir")
        os.makedirs(existing_dir)

        file_path = os.path.join(existing_dir, "file.txt")
        # Should not raise or fail if directory exists
        Handler.create_directory(file_path)
        assert os.path.exists(existing_dir)

    def test_list_of_dicts_to_jsonl_creates_file_with_correct_content(self):
        data = [
            {"a": 1, "b": "x"},
            {"a": 2, "b": "y"},
        ]
        file_path = os.path.join(self.temp_dir, "output.jsonl")

        Handler.list_of_dicts_to_jsonl(data, file_path)

        assert os.path.isfile(file_path)

        with open(file_path, "r", encoding="utf-8") as f:
            lines = f.read().splitlines()
            assert len(lines) == 2
            for i, line in enumerate(lines):
                obj = json.loads(line)
                assert obj == data[i]

    def test_list_of_dicts_to_csv_creates_file_with_correct_content(self):
        data = [
            {"name": "Alice", "age": 30},
            {"name": "Bob", "age": 25},
        ]
        file_path = os.path.join(self.temp_dir, "output.csv")

        Handler.list_of_dicts_to_csv(data, file_path)

        assert os.path.isfile(file_path)

        with open(file_path, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            rows = list(reader)
            assert len(rows) == 2
            assert rows[0]["name"] == "Alice"
            assert rows[0]["age"] == "30"  # CSV stores all as strings
            assert rows[1]["name"] == "Bob"
            assert rows[1]["age"] == "25"

    def test_list_of_dicts_to_csv_empty_data_raises_value_error(self):
        data = []
        file_path = os.path.join(self.temp_dir, "empty.csv")

        try:
            Handler.list_of_dicts_to_csv(data, file_path)
        except ValueError as e:
            assert "data list is empty" in str(e)
        else:
            assert False, "ValueError not raised for empty data"

    def test_get_distinct_values_for_attribute(self):
        
        data = [
            {'id': 1, 'name': 'Alice', 'country': 'USA'},
            {'id': 2, 'name': 'Bob', 'country': 'UK'},
            {'id': 3, 'name': 'Alice', 'country': 'USA'},
            {'id': 4, 'name': 'David', 'country': None},
        ]

        result = Handler.get_distinct_values(data, 'country')
        assert sorted(result) == sorted(['USA', 'UK'])

    def test_filter_list_of_dicts(self):

        data = [
            {'id': 1, 'name': 'Alice', 'country': 'USA'},
            {'id': 2, 'name': 'Bob', 'country': 'UK'},
            {'id': 3, 'name': 'Alice', 'country': 'USA'},
            {'id': 4, 'name': 'David', 'country': None},
        ]

        expected = [
            {'id': 2, 'name': 'Bob', 'country': 'UK'}
        ]

        result = Handler.filter_list_of_dicts(
            data=data, 
            attribute='country', 
            value='UK'
        )
        
        assert result == expected