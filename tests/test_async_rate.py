#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Stéphane Caron

"""
Test asyncio rate limiter.
"""

import asyncio

import pytest
import pytest_asyncio

from loop_rate_limiters import AsyncRateLimiter


@pytest_asyncio.fixture
async def rate():
    """
    Initialize a rate with 1 ms period.
    """
    return AsyncRateLimiter(1000.0)


@pytest.mark.asyncio
async def test_init(rate):
    """
    Constructor completed.
    """
    assert rate is not None


def test_period_dt():
    """Check that period and dt are the same."""
    rate = AsyncRateLimiter(1000.0)
    assert rate.period == pytest.approx(rate.dt)


@pytest.mark.asyncio
async def test_remaining(rate):
    """
    After one period has expired, the "remaining" time becomes negative.
    """
    await rate.sleep()
    await asyncio.sleep(rate.period)
    remaining = await rate.remaining()
    assert remaining < 0.0


@pytest.mark.asyncio
async def test_slack(rate):
    """
    Slack becomes negative as well after one period has expired.

    Notes:
        We wait slightly less than a period because Windows (windows-latest
        in the CI) has imprecise timers.
    """
    await rate.sleep()
    await asyncio.sleep(rate.period * 2.0)  # sleep more than rate
    await rate.sleep()  # computes slack of previous period
    assert rate.slack < 0.0


@pytest.mark.asyncio
async def test_sleep(rate):
    await rate.sleep()
    await rate.sleep()  # presumably slack > 0.0
    await asyncio.sleep(rate.period)
    await rate.sleep()  # now for sure slack < 0.0
