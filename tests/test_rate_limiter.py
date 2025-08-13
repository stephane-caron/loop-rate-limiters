#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Stéphane Caron

"""
Test rate limiter.
"""

import time

import pytest

from loop_rate_limiters import RateLimiter


@pytest.fixture
def rate():
    """Initialize a rate with 1 ms period."""
    return RateLimiter(frequency=1000.0)


def test_init(rate):
    """Constructor completed."""
    assert rate is not None


def test_next_tick(rate):
    call_tick = time.perf_counter()
    rate.sleep()
    assert rate.next_tick >= call_tick + rate.dt


def test_period_dt(rate):
    """Check that period and dt are the same."""
    assert rate.period == pytest.approx(rate.dt)


def test_remaining(rate):
    """
    After one period has expired, the "remaining" time becomes negative.
    """
    rate.sleep()
    time.sleep(rate.period)
    remaining = rate.remaining()
    assert remaining < 0.0


def test_slack(rate):
    """
    Slack becomes negative as well after one period has expired.
    """
    rate.sleep()
    time.sleep(rate.period)
    rate.sleep()  # computes slack of previous period
    assert rate.slack < 0.0


def test_sleep(rate):
    rate.sleep()
    rate.sleep()  # presumably slack > 0.0
    time.sleep(rate.period)
    rate.sleep()  # now for sure slack < 0.0
