#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# SPDX-License-Identifier: Apache-2.0

"""
Test logging functionality.
"""

import logging
import unittest
from io import StringIO

from loop_rate_limiters.logging import (
    SpdlogFormatter,
    disable_warnings,
    logger,
)


class TestSpdlogFormatter(unittest.TestCase):
    def setUp(self):
        """Set up formatter for testing."""
        self.formatter = SpdlogFormatter()

    def test_init(self):
        """Constructor completed."""
        self.assertIsNotNone(self.formatter)
        self.assertIsInstance(self.formatter.level_format, dict)

    def test_format_warning(self):
        """Format warning message correctly."""
        record = logging.LogRecord(
            name="test",
            level=logging.WARNING,
            pathname="test.py",
            lineno=42,
            msg="Test warning message",
            args=(),
            exc_info=None,
        )
        formatted = self.formatter.format(record)

        # Check that formatted string contains expected components
        self.assertIn("[test]", formatted)
        self.assertIn("warning", formatted)  # Color codes may surround this
        self.assertIn("Test warning message", formatted)
        self.assertIn("(test.py:42)", formatted)

    def test_format_error(self):
        """Format error message correctly."""
        record = logging.LogRecord(
            name="test",
            level=logging.ERROR,
            pathname="test.py",
            lineno=42,
            msg="Test error message",
            args=(),
            exc_info=None,
        )
        formatted = self.formatter.format(record)

        # Check that formatted string contains expected components
        self.assertIn("[test]", formatted)
        self.assertIn("error", formatted)  # Color codes may surround this
        self.assertIn("Test error message", formatted)
        self.assertIn("(test.py:42)", formatted)

    def test_format_info(self):
        """Format info message correctly."""
        record = logging.LogRecord(
            name="test",
            level=logging.INFO,
            pathname="test.py",
            lineno=42,
            msg="Test info message",
            args=(),
            exc_info=None,
        )
        formatted = self.formatter.format(record)

        # Check that formatted string contains expected components
        self.assertIn("[test]", formatted)
        self.assertIn("info", formatted)  # Color codes may surround this
        self.assertIn("Test info message", formatted)
        self.assertIn("(test.py:42)", formatted)

    def test_format_debug(self):
        """Format debug message correctly."""
        record = logging.LogRecord(
            name="test",
            level=logging.DEBUG,
            pathname="test.py",
            lineno=42,
            msg="Test debug message",
            args=(),
            exc_info=None,
        )
        formatted = self.formatter.format(record)

        # Check that formatted string contains expected components
        self.assertIn("[test]", formatted)
        self.assertIn("[debug]", formatted)
        self.assertIn("Test debug message", formatted)
        self.assertIn("(test.py:42)", formatted)

    def test_format_critical(self):
        """Format critical message correctly."""
        record = logging.LogRecord(
            name="test",
            level=logging.CRITICAL,
            pathname="test.py",
            lineno=42,
            msg="Test critical message",
            args=(),
            exc_info=None,
        )
        formatted = self.formatter.format(record)

        # Check that formatted string contains expected components
        self.assertIn("[test]", formatted)
        self.assertIn("critical", formatted)  # Color codes may surround this
        self.assertIn("Test critical message", formatted)
        self.assertIn("(test.py:42)", formatted)

    def test_format_unknown_level(self):
        """Format message with unknown level."""
        record = logging.LogRecord(
            name="test",
            level=99,  # Unknown level
            pathname="test.py",
            lineno=42,
            msg="Test unknown level message",
            args=(),
            exc_info=None,
        )
        formatted = self.formatter.format(record)

        # Check that formatted string contains expected components
        self.assertIn("[test]", formatted)
        self.assertIn("[???]", formatted)
        self.assertIn("Test unknown level message", formatted)
        self.assertIn("(test.py:42)", formatted)


class TestLogger(unittest.TestCase):
    def test_logger_exists(self):
        """Logger is properly initialized."""
        self.assertIsNotNone(logger)
        self.assertEqual(logger.name, "loop_rate_limiters")

    def test_logger_has_handler(self):
        """Logger has a handler configured."""
        self.assertTrue(len(logger.handlers) > 0)

    def test_logger_propagate_disabled(self):
        """Logger propagation is disabled."""
        self.assertFalse(logger.propagate)

    def test_logger_formatter_type(self):
        """Logger uses SpdlogFormatter."""
        handler = logger.handlers[0]
        self.assertIsInstance(handler.formatter, SpdlogFormatter)

    def test_disable_warnings(self):
        """disable_warnings function works correctly."""
        original_level = logger.level
        disable_warnings()
        self.assertEqual(logger.level, logging.ERROR)

        # Restore original level
        logger.setLevel(original_level)

    def test_logger_output_format(self):
        """Logger produces correctly formatted output."""
        # Capture logger output
        stream = StringIO()
        test_handler = logging.StreamHandler(stream)
        test_handler.setFormatter(SpdlogFormatter())

        # Create a temporary logger for testing
        test_logger = logging.getLogger("test_logger")
        test_logger.addHandler(test_handler)
        test_logger.setLevel(logging.WARNING)
        test_logger.propagate = False

        test_logger.warning("Test warning message")
        output = stream.getvalue()

        # Check output format (accounting for ANSI color codes)
        self.assertIn("[test_logger]", output)
        self.assertIn("warning", output)  # Color codes may surround this
        self.assertIn("Test warning message", output)
        self.assertIn("(test_logging.py:", output)

        # Clean up
        test_logger.removeHandler(test_handler)


if __name__ == "__main__":
    unittest.main()
