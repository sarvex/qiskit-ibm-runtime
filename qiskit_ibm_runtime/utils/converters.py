# This code is part of Qiskit.
#
# (C) Copyright IBM 2021.
#
# This code is licensed under the Apache License, Version 2.0. You may
# obtain a copy of this license in the LICENSE.txt file in the root directory
# of this source tree or at http://www.apache.org/licenses/LICENSE-2.0.
#
# Any modifications or derivative works of this code must retain this
# copyright notice, and modified files need to carry a notice indicating
# that they have been altered from the originals.

"""Utilities related to conversion."""

from typing import Union, Tuple, Any
from datetime import datetime, timedelta, timezone
from math import ceil
from dateutil import tz, parser

from ..exceptions import IBMInputValueError


def utc_to_local(utc_dt: Union[datetime, str]) -> datetime:
    """Convert a UTC ``datetime`` object or string to a local timezone ``datetime``.

    Args:
        utc_dt: Input UTC `datetime` or string.

    Returns:
        A ``datetime`` with the local timezone.

    Raises:
        TypeError: If the input parameter value is not valid.
    """
    if isinstance(utc_dt, str):
        utc_dt = parser.parse(utc_dt)
    if not isinstance(utc_dt, datetime):
        raise TypeError("Input `utc_dt` is not string or datetime.")
    utc_dt = utc_dt.replace(tzinfo=timezone.utc)  # type: ignore[arg-type]
    return utc_dt.astimezone(tz.tzlocal())


def local_to_utc(local_dt: Union[datetime, str]) -> datetime:
    """Convert a local ``datetime`` object or string to a UTC ``datetime``.

    Args:
        local_dt: Input local ``datetime`` or string.

    Returns:
        A ``datetime`` in UTC.

    Raises:
        TypeError: If the input parameter value is not valid.
    """
    if isinstance(local_dt, str):
        local_dt = parser.parse(local_dt)
    if not isinstance(local_dt, datetime):
        raise TypeError("Input `local_dt` is not string or datetime.")

    # Input is considered local if it's ``utcoffset()`` is ``None`` or none-zero.
    if local_dt.utcoffset() is None or local_dt.utcoffset() != timedelta(0):
        local_dt = local_dt.replace(tzinfo=tz.tzlocal())
        return local_dt.astimezone(tz.UTC)
    return local_dt  # Already in UTC.


def utc_to_local_all(data: Any) -> Any:
    """Recursively convert all ``datetime`` in the input data from local time to UTC.

    Note:
        Only lists and dictionaries are traversed.

    Args:
        data: Data to be converted.

    Returns:
        Converted data.
    """
    if isinstance(data, datetime):
        return utc_to_local(data)
    elif isinstance(data, list):
        return [utc_to_local_all(elem) for elem in data]
    elif isinstance(data, dict):
        return {key: utc_to_local_all(elem) for key, elem in data.items()}
    return data


def seconds_to_duration(seconds: float) -> Tuple[int, int, int, int, int]:
    """Converts seconds in a datetime delta to a duration.

    Args:
        seconds: Number of seconds in time delta.

    Returns:
        A tuple containing the duration in terms of days,
        hours, minutes, seconds, and milliseconds.
    """
    days = int(seconds // (3600 * 24))
    hours = int((seconds // 3600) % 24)
    minutes = int((seconds // 60) % 60)
    seconds %= 60
    millisec = 0
    if seconds < 1:
        millisec = int(ceil(seconds * 1000))
        seconds = 0
    else:
        seconds = seconds
    return days, hours, minutes, seconds, millisec


def duration_difference(date_time: datetime) -> str:
    """Compute the estimated duration until the given datetime.

    Args:
        date_time: The input local datetime.

    Returns:
        String giving the estimated duration.
    """
    time_delta = date_time.replace(tzinfo=None) - datetime.now()
    time_tuple = seconds_to_duration(time_delta.total_seconds())
    # The returned tuple contains the duration in terms of
    # days, hours, minutes, seconds, and milliseconds.
    time_str = ""
    if time_tuple[0]:
        time_str += f"{time_tuple[0]} days"
        time_str += f" {time_tuple[1]} hrs"
    elif time_tuple[1]:
        time_str += f"{time_tuple[1]} hrs"
        time_str += f" {time_tuple[2]} min"
    elif time_tuple[2]:
        time_str += f"{time_tuple[2]} min"
        time_str += f" {time_tuple[3]} sec"
    elif time_tuple[3]:
        time_str += f"{time_tuple[3]} sec"
    return time_str


def hms_to_seconds(hms: str, msg_prefix: str = "") -> int:
    """Convert duration specified as hours minutes seconds to seconds.

    Args:
        hms: The string input duration (in hours minutes seconds). Ex: 2h 10m 20s
        msg_prefix: Additional message to prefix the error.

    Returns:
        Total seconds (int) in the duration.

    Raises:
        IBMInputValueError: when the given hms string is in an invalid format
    """
    try:
        date_time = parser.parse(hms)
        hours = date_time.hour
        minutes = date_time.minute
        seconds = date_time.second
        return int(
            timedelta(hours=hours, minutes=minutes, seconds=seconds).total_seconds()
        )
    except parser.ParserError as parser_error:
        raise IBMInputValueError(msg_prefix + str(parser_error))
