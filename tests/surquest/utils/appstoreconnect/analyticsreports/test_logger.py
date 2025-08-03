import unittest
import logging
from surquest.utils.appstoreconnect.analyticsreports.logger import logger


class TestLoggerSetup(unittest.TestCase):

    def test_logger_level_is_debug(self):
        assert logger.level == logging.DEBUG

    def test_logger_has_one_handler(self):
        assert len(logger.handlers) == 1
        assert isinstance(logger.handlers[0], logging.StreamHandler)

    def test_logger_formatter_format(self):
        handler = logger.handlers[0]
        fmt = handler.formatter._fmt
        expected_fmt = '%(levelname)-8s - %(asctime)s - %(message)s'
        assert fmt == expected_fmt

    def test_logger_propagation_disabled(self):
        assert logger.propagate is False

    def test_duplicate_handler_prevention(self):
        initial_count = len(logger.handlers)

        # Simulate running the initialization code again
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter('%(levelname)-8s - %(asctime)s - %(message)s')
            handler.setFormatter(formatter)
            logger.addHandler(handler)

        # Should not increase handler count
        assert len(logger.handlers) == initial_count