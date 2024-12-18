#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Stéphane Caron

"""
Test rate limiter.
"""

import time
import unittest

from loop_rate_limiters import RateLimiter


class TestRate(unittest.TestCase):
    def setUp(self):
        """Initialize a rate with 1 ms period."""
        self.rate = RateLimiter(frequency=1000.0)

    def test_init(self):
        """Constructor completed."""
        self.assertIsNotNone(self.rate)

    def test_next_tick(self):
        call_tick = time.perf_counter()
        self.rate.sleep()
        self.assertGreaterEqual(self.rate.next_tick, call_tick + self.rate.dt)

    def test_period_dt(self):
        """Check that period and dt are the same."""
        self.assertAlmostEqual(self.rate.period, self.rate.dt)

    def test_remaining(self):
        """
        After one period has expired, the "remaining" time becomes negative.
        """
        self.rate.sleep()
        time.sleep(self.rate.period)
        remaining = self.rate.remaining()
        self.assertLess(remaining, 0.0)

    def test_slack(self):
        """
        Slack becomes negative as well after one period has expired.
        """
        self.rate.sleep()
        time.sleep(self.rate.period)
        self.rate.sleep()  # computes slack of previous period
        self.assertLess(self.rate.slack, 0.0)

    def test_sleep(self):
        self.rate.sleep()
        self.rate.sleep()  # presumably slack > 0.0
        time.sleep(self.rate.period)
        self.rate.sleep()  # now for sure slack < 0.0
