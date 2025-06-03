#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Stéphane Caron

"""Loop rate limiters."""

__version__ = "1.1.1"

from .async_rate_limiter import AsyncRateLimiter
from .rate_limiter import RateLimiter

__all__ = [
    "AsyncRateLimiter",
    "RateLimiter",
]
