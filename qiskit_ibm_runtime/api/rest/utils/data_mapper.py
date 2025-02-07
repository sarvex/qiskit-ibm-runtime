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

"""Utility module for data mapping."""

import re
import keyword
from typing import Dict, Any, Optional


def map_jobs_limit_response(data: Dict[str, Any]) -> Dict[str, Any]:
    """Map jobs limit response data.

    Args:
        data: Data to be mapped.

    Returns:
        Mapped data.
    """
    field_map = {"maximumJobs": "maximum_jobs", "runningJobs": "running_jobs"}
    dict_to_identifier(data, field_map)
    return data


def dict_to_identifier(data: Dict[str, Any], mapper: Optional[dict] = None) -> None:
    """Convert keys in a dictionary to valid identifiers, with optional mapping.

    If a `mapper` is specified, keys in `data` that are also in `mapper` will
    be renamed to the corresponding values in `mapper`.

    Args:
        data: Dictionary to be converted.
        mapper: Mapper of selected field names to rename.
    """
    mapper = mapper or {}
    for key in list(data.keys()):
        new_key = mapper[key] if key in mapper else to_python_identifier(key)
        data[new_key] = data.pop(key)


def to_python_identifier(name: str) -> str:
    """Convert a name to a valid Python identifier.

    Args:
        name: Name to be converted.

    Returns:
        Name that is a valid Python identifier.
    """
    # Python identifiers can only contain alphanumeric characters
    # and underscores and cannot start with a digit.
    pattern = re.compile(r"\W|^(?=\d)", re.ASCII)
    if not name.isidentifier():
        name = re.sub(pattern, "_", name)

    # Convert to snake case
    name = re.sub(
        "((?<=[a-z0-9])[A-Z]|(?!^)(?<!_)[A-Z](?=[a-z]))", r"_\1", name
    ).lower()

    while keyword.iskeyword(name):
        name += "_"

    return name
