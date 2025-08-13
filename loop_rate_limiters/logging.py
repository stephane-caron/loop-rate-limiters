#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# SPDX-License-Identifier: Apache-2.0

"""Custom logging configuration for loop rate limiters."""

import logging


class RateLimiterFormatter(logging.Formatter):
    """Custom formatter for rate limiter messages with nice styling."""

    def format(self, record):
        if "is late by" in record.getMessage():
            # Extract rate limiter name and lateness from the message
            parts = record.getMessage().split(" is late by ")
            if len(parts) == 2:
                limiter_name = parts[0]
                lateness = parts[1]
                return f"⚠️  {limiter_name} running {lateness} behind schedule"
        return super().format(record)


def setup_logging():
    """Configure logging with the custom formatter for rate limiters only."""
    logger = logging.getLogger("loop_rate_limiters")

    if not logger.handlers:
        handler = logging.StreamHandler()
        handler.setFormatter(RateLimiterFormatter())
        logger.addHandler(handler)
        logger.setLevel(logging.WARNING)
        # Don't propagate to root logger to avoid duplicate messages
        logger.propagate = False

    return logger


# Library-specific logger
logger = setup_logging()
