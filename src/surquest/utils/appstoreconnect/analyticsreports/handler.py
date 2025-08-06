import os
import csv
import json
import warnings
import operator
from typing import Any, List, Dict

from .errors import PayloadFormatError, NoValidIdsError, NoValidUrlsError
from .logger import logger


class Handler:
    @staticmethod
    def extract_ids(payload: dict) -> list[str]:
        """
        Extracts a list of 'id' values from a payload dictionary.

        Raises:
            PayloadFormatError: if 'data' is missing or not a list.
            NoValidIdsError: if no valid IDs are found in the payload.
        """

        data = payload

        ids = []
        for item in data:
            if not isinstance(item, dict):
                warnings.warn(f"Skipped: item is not a dictionary: {item}")
                continue
            if "id" not in item or item["id"] is None:
                warnings.warn(f"Skipped: missing or null 'id' in item: {item}")
                continue
            ids.append(item["id"])

        if not ids:
            raise NoValidIdsError("No valid IDs found in the payload.")

        return ids


    @staticmethod
    def extract_attribute_values(payload: dict, attribute: str | None = None) -> list[str]:
        """
        Extracts a list of 'attribute' values from each item's attributes in the payload.

        Args:
            payload (dict): Dictionary representing the payload.
            attribute (str, optional): Name of the attribute to extract. Defaults to None.

        Raises:
            PayloadFormatError: if 'data' is missing or not a list.
            NoValidUrlsError: if no valid URLs are found in the payload.
        """

        data = payload
        out = []
        for item in data:
            if not isinstance(item, dict):
                warnings.warn(f"Skipped: item is not a dictionary: {item}")
                continue

            attributes = item.get("attributes")
            if not isinstance(attributes, dict):
                warnings.warn(f"Skipped: missing or malformed 'attributes' in item: {item}")
                continue
            
            if attribute is not None:
                val = attributes.get(attribute)
                if not val:
                    warnings.warn(f"Skipped: missing or empty `{attribute}` in attributes: {attributes}")
                    continue
                out.append(val)

            else:
                out.append(attributes)

        if not out:
            raise NoValidUrlsError(f"No valid `{attribute}` found in the payload.")

        return out

    @staticmethod
    def deduplicate_data(data: list[dict]) -> list[dict]:
        """
        Remove duplicated entries (dictionaries) and ensure consistent key order.

        Args:
            data (list): List of dictionaries

        Returns:
            list: Deduplicated list of dictionaries with consistent key order
        """
        if not data:
            return []

        # Convert string representations of numbers to actual numbers
        for item in data:
            for key, value in item.items():
                if isinstance(value, str):
                    if "." in value:
                        try:
                            # Try converting to float first (handles integers too)
                            num_value = float(value)
                            item[key] = num_value
                        except ValueError:
                            # Not a numeric string, keep as is
                            pass
                    elif value in [""]:
                        item[key] = None
                    else:
                        try:
                            # Try converting to integer
                            num_value = int(value)
                            item[key] = num_value
                        except ValueError:
                            # Not an integer, keep as is
                            pass

        # Determine consistent key order (from the first dictionary)
        key_order = list(data[0].keys())

        # Deduplicate using tuple representation
        seen = set()
        unique_data = []
        for d in data:
            # Ensure dictionary has all keys (fill missing with None)
            normalized = tuple((k, d.get(k)) for k in key_order)
            if normalized not in seen:
                seen.add(normalized)
                unique_data.append({k: d.get(k) for k in key_order})

        logger.info(
            f"Entries: duplicated {len(data) - len(unique_data)}, "
            f"original: {len(data)}, "
            f"deduplicated: {len(unique_data)}"
        )

        return unique_data

    @staticmethod
    def create_directory(file_path: str) -> None:
        """
        Creates a directory if it doesn't exist.

        Args:
            file_path (str): Path to the file or directory.
        """

        directory = os.path.dirname(file_path)
        if not os.path.exists(directory):
            os.makedirs(directory)

    @staticmethod
    def list_of_dicts_to_jsonl(data: list[dict], file_path: str) -> None:
        """
        Converts a list of dictionaries to JSON Lines format and writes to a file.

        Args:
            data (list[dict]): List of dictionaries to convert.
            file_path (str): Path to the output .jsonl file.
        """

        # Create the directory if it doesn't exist
        Handler.create_directory(file_path)

        with open(file_path, 'w', encoding='utf-8') as f:
            for item in data:
                json_line = json.dumps(item, ensure_ascii=False)
                f.write(json_line + '\n')

    @staticmethod
    def list_of_dicts_to_csv(data: list[dict], file_path: str) -> None:
        """
        Converts a list of dictionaries to CSV format and writes to a file.

        Args:
            data (list[dict]): List of dictionaries to convert.
            file_path (str): Path to the output .csv file.
        """
        if not data:
            raise ValueError("The data list is empty.")

        # Create the directory if it doesn't exist
        Handler.create_directory(file_path)
        
        # Extract headers from keys of the first dictionary
        headers = data[0].keys()
        
        with open(file_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=headers)
            writer.writeheader()
            writer.writerows(data)

    @staticmethod
    def get_distinct_values(data: list[dict], key: str) -> list:
        """
        Extracts distinct values for a given key from a list of dictionaries.

        Args:
            data (list): List of dictionaries.
            key (str): Key for which distinct values are needed.

        Returns:
            list: List of distinct values (excluding None).
        """
        return list({record.get(key) for record in data if key in record and record.get(key) is not None})

    @staticmethod
    def filter_list_of_dicts(
        data: List[Dict[str, Any]],
        attribute: str,
        value: Any,
        comparator: str = '==',
    ) -> List[Dict[str, Any]]:
        """
        Filters a list of dictionaries based on a comparator applied to a specific attribute.

        Args:
            data (list): List of dictionaries.
            attribute (str): Key to filter on.
            value (Any): Value to compare against.
            comparator (str): Comparison operator as a string (e.g., '==', '!=', '>', '<', '>=', '<=', 'in', 'not in').


        Returns:
            list: Filtered list of dictionaries.
        """

        # Supported operators
        ops: dict[str, Callable] = {
            '==': operator.eq,
            '!=': operator.ne,
            '>': operator.gt,
            '<': operator.lt,
            '>=': operator.ge,
            '<=': operator.le,
            'in': lambda a, b: a in b,
            'not in': lambda a, b: a not in b
        }

        if comparator not in ops:
            raise ValueError(f"Unsupported comparator '{comparator}'. Use one of: {list(ops.keys())}")

        func = ops[comparator]

        return [
            item for item in data
            if attribute in item and func(item[attribute], value)
        ]