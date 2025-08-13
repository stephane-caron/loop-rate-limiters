#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# SPDX-License-Identifier: Apache-2.0

"""
Test logging functionality.
"""

import logging
from io import StringIO

import pytest

from loop_rate_limiters.logging import (
    SpdlogFormatter,
    disable_warnings,
    logger,
)


@pytest.fixture
def formatter():
    """Set up formatter for testing."""
    return SpdlogFormatter()


@pytest.fixture
def log_record():
    """Create a basic log record for testing."""

    def _make_record(level, msg):
        return logging.LogRecord(
            name="test",
            level=level,
            pathname="test.py",
            lineno=42,
            msg=msg,
            args=(),
            exc_info=None,
        )

    return _make_record


class TestSpdlogFormatter:
    def test_init(self, formatter):
        """Constructor completed."""
        assert formatter is not None
        assert isinstance(formatter.level_format, dict)

    def test_format_warning(self, formatter, log_record):
        """Format warning message correctly."""
        record = log_record(logging.WARNING, "Test warning message")
        formatted = formatter.format(record)

        # Check that formatted string contains expected components
        assert "[test]" in formatted
        assert "warning" in formatted  # Color codes may surround this
        assert "Test warning message" in formatted
        assert "(test.py:42)" in formatted

    def test_format_error(self, formatter, log_record):
        """Format error message correctly."""
        record = log_record(logging.ERROR, "Test error message")
        formatted = formatter.format(record)

        # Check that formatted string contains expected components
        assert "[test]" in formatted
        assert "error" in formatted  # Color codes may surround this
        assert "Test error message" in formatted
        assert "(test.py:42)" in formatted

    def test_format_info(self, formatter, log_record):
        """Format info message correctly."""
        record = log_record(logging.INFO, "Test info message")
        formatted = formatter.format(record)

        # Check that formatted string contains expected components
        assert "[test]" in formatted
        assert "info" in formatted  # Color codes may surround this
        assert "Test info message" in formatted
        assert "(test.py:42)" in formatted

    def test_format_debug(self, formatter, log_record):
        """Format debug message correctly."""
        record = log_record(logging.DEBUG, "Test debug message")
        formatted = formatter.format(record)

        # Check that formatted string contains expected components
        assert "[test]" in formatted
        assert "[debug]" in formatted
        assert "Test debug message" in formatted
        assert "(test.py:42)" in formatted

    def test_format_critical(self, formatter, log_record):
        """Format critical message correctly."""
        record = log_record(logging.CRITICAL, "Test critical message")
        formatted = formatter.format(record)

        # Check that formatted string contains expected components
        assert "[test]" in formatted
        assert "critical" in formatted  # Color codes may surround this
        assert "Test critical message" in formatted
        assert "(test.py:42)" in formatted

    def test_format_unknown_level(self, formatter):
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
        formatted = formatter.format(record)

        # Check that formatted string contains expected components
        assert "[test]" in formatted
        assert "[???]" in formatted
        assert "Test unknown level message" in formatted
        assert "(test.py:42)" in formatted


class TestLogger:
    def test_logger_exists(self):
        """Logger is properly initialized."""
        assert logger is not None
        assert logger.name == "loop_rate_limiters"

    def test_logger_has_handler(self):
        """Logger has a handler configured."""
        assert len(logger.handlers) > 0

    def test_logger_propagate_disabled(self):
        """Logger propagation is disabled."""
        assert logger.propagate is False

    def test_logger_formatter_type(self):
        """Logger uses SpdlogFormatter."""
        handler = logger.handlers[0]
        assert isinstance(handler.formatter, SpdlogFormatter)

    def test_disable_warnings(self):
        """disable_warnings function works correctly."""
        original_level = logger.level
        disable_warnings()
        assert logger.level == logging.ERROR

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
        assert "[test_logger]" in output
        assert "warning" in output  # Color codes may surround this
        assert "Test warning message" in output
        assert "(test_logging.py:" in output

        # Clean up
        test_logger.removeHandler(test_handler)
