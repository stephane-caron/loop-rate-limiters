#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Stéphane Caron
# Copyright 2023 Inria

"""Synchronous rate limiter."""

from time import perf_counter, sleep

from .logging import logger


class RateLimiter:
    """Regulate the frequency between calls to the same instruction.

    This rate limniter is meant to be used in e.g. a loop or callback function.
    It is, in essence, the same as rospy.Rate_. It assumes Python's performance
    counter never jumps backward nor forward, so that it does not handle such
    cases contrary to rospy.Rate_.

    .. _rospy.Rate:
        https://github.com/ros/ros_comm/blob/noetic-devel/clients/rospy/src/rospy/timer.py

    Attributes:
        name: Human-readable name used for logging.
        warn: If set (default), warn when the time between two calls
            exceeded the rate clock.
    """

    __period: float
    __slack: float
    __next_tick: float
    name: str
    warn: bool

    def __init__(
        self,
        frequency: float,
        name: str = "rate limiter",
        warn: bool = True,
    ):
        """Initialize rate limiter.

        Args:
            frequency: Desired frequency in hertz.
            name: Human-readable name used for logging.
            warn: If set (default), warn when the time between two calls
                exceeded the rate clock.
        """
        period = 1.0 / frequency
        self.__next_tick = perf_counter() + period
        self.__period = period
        self.__slack = 0.0
        self.name = name
        self.warn = warn

    @property
    def dt(self) -> float:
        """Desired period between two calls to :func:`sleep`, in seconds."""
        return self.__period

    @property
    def next_tick(self) -> float:
        """Time of next clock tick."""
        return self.__next_tick

    @property
    def period(self) -> float:
        """Desired period between two calls to :func:`sleep`, in seconds."""
        return self.__period

    @property
    def slack(self) -> float:
        """Slack duration computed at the last call to :func:`sleep`.

        This duration is in seconds.
        """
        return self.__slack

    def remaining(self) -> float:
        """Get the time remaining until the next expected clock tick.

        Returns:
            Time remaining, in seconds, until the next expected clock tick.
        """
        return self.__next_tick - perf_counter()

    def sleep(self):
        """Sleep for the duration required to regulate inter-call frequency."""
        self.__slack = self.__next_tick - perf_counter()
        if self.__slack > 0.0:
            sleep(self.__slack)
        elif self.__slack < -0.1 * self.period and self.warn:
            logger.warning(
                "%s is late by %.1f [ms]",
                self.name,
                round(-1e3 * self.__slack, 1),
            )
        self.__next_tick = perf_counter() + self.__period
