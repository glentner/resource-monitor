# This program is free software: you can redistribute it and/or modify it under the
# terms of the Apache License (v2.0) as published by the Apache Software Foundation.
#
# This program is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
# PARTICULAR PURPOSE. See the Apache License for more details.
#
# You should have received a copy of the Apache License along with this program.
# If not, see <https://www.apache.org/licenses/LICENSE-2.0>.

"""Implementation of StatBase class."""


# type annotations
from __future__ import annotations
from typing import Mapping, Union, List, Dict, TypeVar

# standard library
from abc import ABC, abstractclassmethod
from subprocess import check_output


T = TypeVar('T', int, float, List[float], Dict[int, float])

class StatBase(ABC):
    """Structured object from text-block."""

    _cmd: str = None
    _data: Dict[str, T]

    def __init__(self, other: Union[Mapping, StatBase]) -> None:
        """Initialize directly from initial object."""
        self.data = other if not isinstance(other, StatBase) else other.data

    @property
    def data(self) -> Dict[str, T]:
        return self._data

    @data.setter
    def data(self, other: Dict[str, T]) -> None:
        self._data = dict(other)

    @classmethod
    def from_cmd(cls) -> StatBase:
        """Execute `_cmd` in a subprocess and parse text block."""
        block = check_output(cls._cmd, shell=True).decode()
        return cls.from_text(block)

    @classmethod
    def from_text(cls, block: str) -> StatBase:
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


class NvidiaStat(StatBase, ABC):
    """Status object for Nvidia GPU resource."""


class NvidiaPercent(NvidiaStat):
    """Parse nvidia-smi for overall percent utilization."""

    _cmd: str = 'nvidia-smi --format=csv,noheader,nounits --query-gpu=index,utilization.gpu -c1'

    @classmethod
    def parse_text(cls, block: str) -> Dict[str, Dict[int, float]]:
        """Parse `nvidia-smi` output."""
        data = {}
        for line in block.strip().split('\n'):
            index, percent = map(float, line.strip().split(', '))
            data[int(index)] = percent
        return {'percent': data}


class NvidiaMemory(NvidiaStat):
    """Parse nvidia-smi for memory usage."""

    _cmd: str = 'nvidia-smi --format=csv,noheader,nounits --query-gpu=index,memory.used,memory.total -c1'

    @classmethod
    def parse_text(cls, block: str) -> Dict[str, Dict[int, float]]:
        """Parse `nvidia-smi` output."""
        data = {}
        for line in block.strip().split('\n'):
            index, current, total = map(float, line.strip().split(', '))
            data[int(index)] = current / total
        return {'memory': data}


class NvidiaTemperature(NvidiaStat):
    """Parse nvidia-smi for GPU temperature (in degrees C)."""

    _cmd: str = 'nvidia-smi --format=csv,noheader,nounits --query-gpu=index,temperature.gpu -c1'

    @classmethod
    def parse_text(cls, block: str) -> Dict[str, Dict[int, float]]:
        """Parse `nvidia-smi` output."""
        data = {}
        for line in block.strip().split('\n'):
            index, temp = map(float, line.strip().split(', '))
            data[int(index)] = temp
        return {'temp': data}


class NvidiaPower(NvidiaStat):
    """Parse nvidia-smi for GPU total power draw (in Watts +/- 5 Watts)."""

    _cmd: str = 'nvidia-smi --format=csv,noheader,nounits --query-gpu=index,power.draw -c1'

    @classmethod
    def parse_text(cls, block: str) -> Dict[str, Dict[int, float]]:
        """Parse `nvidia-smi` output."""
        data = {}
        for line in block.strip().split('\n'):
            index, power = map(float, line.strip().split(', '))
            data[int(index)] = power
        return {'power': data}
