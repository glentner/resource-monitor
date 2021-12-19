# This program is free software: you can redistribute it and/or modify it under the
# terms of the Apache License (v2.0) as published by the Apache Software Foundation.
#
# This program is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
# PARTICULAR PURPOSE. See the Apache License for more details.
#
# You should have received a copy of the Apache License along with this program.
# If not, see <https://www.apache.org/licenses/LICENSE-2.0>.

"""Simple support for external metrics (subprocess call to external commands)."""


# type annotations
from __future__ import annotations
from typing import Mapping, Union, List, Dict, TypeVar

# standard library
from abc import ABC, abstractclassmethod
from subprocess import check_output

# public interface
__all__ = ['ExternalMetric', ]


# value type for metrics
# either individual value, a list, or indexed collection
T = TypeVar('T', float, List[float], Dict[int, float])


class ExternalMetric(ABC):
    """Structured object from text-block."""

    _cmd: str = None
    _data: Dict[str, T]

    def __init__(self, other: Union[Mapping, ExternalMetric]) -> None:
        """Initialize directly from initial object."""
        self.data = other if not isinstance(other, ExternalMetric) else other.data

    @property
    def data(self) -> Dict[str, T]:
        return self._data

    @data.setter
    def data(self, other: Dict[str, T]) -> None:
        self._data = dict(other)

    @classmethod
    def from_cmd(cls) -> ExternalMetric:
        """Execute `_cmd` in a subprocess and parse text block."""
        block = check_output(cls._cmd, shell=True).decode()
        return cls.from_text(block)

    @classmethod
    def from_text(cls, block: str) -> ExternalMetric:
        """Parse text `block` for attributes."""
        attrs = cls.parse_text(block)
        return cls(attrs)

    @abstractclassmethod
    def parse_text(cls, block: str) -> Mapping:
        """Parse the text `block` and return attributes."""

    def __str__(self) -> str:
        """String representation."""
        return str(self._data)

    def __repr__(self) -> str:
        """Interactive representation."""
        return f'{self.__class__.__name__}({self._data})'
