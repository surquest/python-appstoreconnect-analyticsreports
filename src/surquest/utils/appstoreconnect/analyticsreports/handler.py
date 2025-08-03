import warnings
from typing import Any

from .errors import PayloadFormatError, NoValidIdsError, NoValidUrlsError


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
    def deduplicate_data(data: list) -> list:
        """
        Remove duplicated entries (dictionaries)

        Args:
            data (list): List of dictionaries

        Returns:
            list: Deduplicated list of dictionaries
        """

        # Deduplicate using frozenset
        unique_data = [dict(t) for t in {frozenset(d.items()) for d in data}]
        return unique_data