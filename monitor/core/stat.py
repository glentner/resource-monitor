# This program is free software: you can redistribute it and/or modify it under the
# terms of the Apache License (v2.0) as published by the Apache Software Foundation.
#
# This program is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
# PARTICULAR PURPOSE. See the Apache License for more details.
#
# You should have received a copy of the Apache License along with this program.
# If not, see <https://www.apache.org/licenses/LICENSE-2.0>.

"""Stat class implementations for external tools (e.g., nvidia-smi, rocm-smi)."""


# type annotations
from __future__ import annotations
from typing import Mapping, Union, List, Dict, TypeVar, Type, Optional

# standard library
import re
from abc import ABC, abstractclassmethod
from subprocess import check_output
import functools

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


class RocmStat(StatBase, ABC):
    """Run rocm-smi to collect metrics on GPU usage."""


class RocmPercent(RocmStat):
    """Parse rocm-smi for GPU overall usage as a percentage."""

    _cmd: str = 'rocm-smi --showuse --csv'
    _pattern: re.Pattern = re.compile(r'^card(\d),(\d+(?:\.\d+)?)')

    @classmethod
    def parse_text(cls, block: str) -> Dict[str, Dict[int, float]]:
        """Parse `rocm-smi` output."""
        data = {}
        lines = block.strip().split('\n')  # NOTE: lines[0]  == 'device,GPU use (%)'
        for line in lines[1:]:
            index, percent = cls._pattern.match(line).groups()
            data[int(index)] = float(percent)
        return {'percent': data}


class RocmMemory(RocmStat):
    """Parse rocm-smi for GPU memory usage as a percentage."""

    _cmd: str = 'rocm-smi --showmemuse --csv'
    _pattern: re.Pattern = re.compile(r'^card(\d),(\d+(?:\.\d+)?)')

    @classmethod
    def parse_text(cls, block: str) -> Dict[str, Dict[int, float]]:
        """Parse `rocm-smi` output."""
        data = {}
        lines = block.strip().split('\n')  # NOTE: lines[0]  == 'device,GPU use (%)'
        for line in lines[1:]:
            index, memory = cls._pattern.match(line).groups()
            data[int(index)] = float(memory)
        return {'memory': data}


class RocmTemperature(RocmStat):
    """Parse rocm-smi for GPU temperature in Celsius."""

    _cmd: str = 'rocm-smi --showtemp --csv'
    _pattern: re.Pattern = re.compile(r'^card(\d),(\d+(?:\.\d+)?),(\d+(?:\.\d+)?),(\d+(?:\.\d+)?)')

    @classmethod
    def parse_text(cls, block: str) -> Dict[str, Dict[int, float]]:
        """Parse `rocm-smi` output."""
        data = {}
        # NOTE: lines[0]  == 'device,Temperature (Sensor edge) (C),Temperature ...
        lines = block.strip().split('\n')
        for line in lines[1:]:
            index, t_edge, t_junc, t_mem = cls._pattern.match(line).groups()
            data[int(index)] = float(t_junc)  # TODO: user picks which temp?
        return {'temp': data}


class RocmPower(RocmStat):
    """Parse rocm-smi for GPU total power draw (in Watts)."""

    _cmd: str = 'rocm-smi --showpower --csv'
    _pattern: re.Pattern = re.compile(r'^card(\d),(\d+(?:\.\d+)?)')

    @classmethod
    def parse_text(cls, block: str) -> Dict[str, Dict[int, float]]:
        """Parse `rocm-smi` output."""
        data = {}
        lines = block.strip().split('\n')  # NOTE: lines[0]  == 'device,Average Graphics Package Power (W)'
        for line in lines[1:]:
            index, power = cls._pattern.match(line).groups()
            data[int(index)] = float(power)
        return {'power': data}


class SMIData:
    """High-level interface to external smi tool for GPU telemetry."""

    @property
    def percent(self) -> Dict[int, float]:
        """Current percent usage by GPU index."""
        return self.get_telemetry('percent')

    @property
    def memory(self) -> Dict[int, float]:
        """Current memory usage by GPU index."""
        return self.get_telemetry('memory')

    @property
    def power(self) -> Dict[int, float]:
        """Current power consumption by GPU index (in Watts)."""
        return self.get_telemetry('power')

    @property
    def temp(self) -> Dict[int, float]:
        """Current temperature by GPU index (in Celsius)."""
        return self.get_telemetry('temp')

    def get_telemetry(self, metric: str) -> Dict[int, float]:
        """Current usage of `metric` by GPU index."""
        provider = self.provider_map.get(self.provider).get(metric)
        return provider.from_cmd().data.get(metric)

    @functools.cached_property
    def provider_map(self) -> Dict[str, Dict[str, Type[StatBase]]]:
        """Map of query providers by vendor and resource type."""
        return {
            'nvidia': {
                'percent': NvidiaPercent,
                'memory': NvidiaMemory,
                'power': NvidiaPower,
                'temp': NvidiaTemperature
            },
            'rocm': {
                'percent': RocmPercent,
                'memory': RocmMemory,
                'power': RocmPower,
                'temp': RocmTemperature
            }
        }

    @functools.cached_property
    def provider(self) -> str:
        """Either 'nvidia' or 'rocm' if available."""
        if self._check_nvidia():
            return 'nvidia'
        if self._check_rocm():
            return 'rocm'
        else:
            raise RuntimeError('Neither `nvidia-smi` nor `rocm-smi` found')

    def _check_nvidia(self) -> Optional[str]:
        return self._check_command('nvidia-smi')

    def _check_rocm(self) -> Optional[str]:
        return self._check_command('rocm-smi')

    @staticmethod
    def _check_command(name: str) -> Optional[str]:
        """Return default output of command given `name`, None if command not found."""
        try:
            return check_output([name, ]).decode().strip()
        except FileNotFoundError:
            return None
