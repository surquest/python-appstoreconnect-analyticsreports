class PayloadFormatError(ValueError):
    """Raised when the payload format is invalid (e.g. missing or malformed 'data' key)."""
    pass


class NoValidIdsError(ValueError):
    """Raised when no valid IDs are found in the payload."""
    pass


class NoValidUrlsError(ValueError):
    """Raised when no valid URLs are found in the payload."""
    pass
