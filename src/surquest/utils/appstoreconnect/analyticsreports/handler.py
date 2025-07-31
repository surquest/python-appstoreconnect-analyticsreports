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
        data = payload.get("data")

        if not isinstance(data, list):
            raise PayloadFormatError(f"'data' key must be a list in the payload: {payload}")

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
    def extract_attribute_values(payload: dict, attribute: str) -> list[str]:
        """
        Extracts a list of 'attribute' values from each item's attributes in the payload.

        Raises:
            PayloadFormatError: if 'data' is missing or not a list.
            NoValidUrlsError: if no valid URLs are found in the payload.
        """
        data = payload.get("data")

        if not isinstance(data, list):
            raise PayloadFormatError(f"'data' key must be a list in the payload: {payload}")

        urls = []
        for item in data:
            if not isinstance(item, dict):
                warnings.warn(f"Skipped: item is not a dictionary: {item}")
                continue

            attributes = item.get("attributes")
            if not isinstance(attributes, dict):
                warnings.warn(f"Skipped: missing or malformed 'attributes' in item: {item}")
                continue

            url = attributes.get(attribute)
            if not url:
                warnings.warn(f"Skipped: missing or empty `{attribute}` in attributes: {attributes}")
                continue

            urls.append(url)

        if not urls:
            raise NoValidUrlsError(f"No valid `{attribute}` found in the payload.")

        return urls
