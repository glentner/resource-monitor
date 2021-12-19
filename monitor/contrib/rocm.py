# This program is free software: you can redistribute it and/or modify it under the
# terms of the Apache License (v2.0) as published by the Apache Software Foundation.
#
# This program is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
# PARTICULAR PURPOSE. See the Apache License for more details.
#
# You should have received a copy of the Apache License along with this program.
# If not, see <https://www.apache.org/licenses/LICENSE-2.0>.

"""External `rocm-smi` metrics."""


# type annotations
from __future__ import annotations
from typing import Dict

# standard libs
import re
from abc import ABC

# internal libs
from ..core.extern import ExternalMetric

# public interface
__all__ = ['RocmMetric', 'RocmPercent', 'RocmMemory', 'RocmPower', 'RocmTemperature', ]


class RocmMetric(ExternalMetric, ABC):
    """Run rocm-smi to collect metrics on GPU usage."""


class RocmPercent(RocmMetric):
    """Parse rocm-smi for GPU overall usage as a percentage."""

    _cmd: str = 'rocm-smi --showuse --csv'
    _pattern: re.Pattern = re.compile(r'^card(\d),(\d+(?:\.\d+)?)')

    @classmethod
    def parse_text(cls, block: str) -> Dict[str, Dict[int, float]]:
        """Parse `rocm-smi` output."""
        try:
            data = {}
            lines = block.strip().split('\n')  # NOTE: lines[0]  == 'device,GPU use (%)'
            for line in lines[1:]:
                index, percent = cls._pattern.match(line).groups()
                data[int(index)] = float(percent)
            return {'percent': data}
        except Exception as error:
            raise RuntimeError(f'Failed to parse output ({cls._cmd}): {error}') from error


class RocmMemory(RocmMetric):
    """Parse rocm-smi for GPU memory usage as a percentage."""

    _cmd: str = 'rocm-smi --showmemuse --csv'
    _pattern: re.Pattern = re.compile(r'^card(\d),(\d+(?:\.\d+)?)')

    @classmethod
    def parse_text(cls, block: str) -> Dict[str, Dict[int, float]]:
        """Parse `rocm-smi` output."""
        try:
            data = {}
            lines = block.strip().split('\n')  # NOTE: lines[0]  == 'device,GPU use (%)'
            for line in lines[1:]:
                index, memory = cls._pattern.match(line).groups()
                data[int(index)] = float(memory)
            return {'memory': data}
        except Exception as error:
            raise RuntimeError(f'Failed to parse output ({cls._cmd}): {error}') from error


class RocmTemperature(RocmMetric):
    """Parse rocm-smi for GPU temperature in Celsius."""

    _cmd: str = 'rocm-smi --showtemp --csv'
    _pattern: re.Pattern = re.compile(r'^card(\d),(\d+(?:\.\d+)?),(\d+(?:\.\d+)?),(\d+(?:\.\d+)?)')

    @classmethod
    def parse_text(cls, block: str) -> Dict[str, Dict[int, float]]:
        """Parse `rocm-smi` output."""
        try:
            data = {}
            # NOTE: lines[0]  == 'device,Temperature (Sensor edge) (C),Temperature ...
            lines = block.strip().split('\n')
            for line in lines[1:]:
                index, t_edge, t_junc, t_mem = cls._pattern.match(line).groups()
                data[int(index)] = float(t_junc)  # TODO: user picks which temp?
            return {'temp': data}
        except Exception as error:
            raise RuntimeError(f'Failed to parse output ({cls._cmd}): {error}') from error


class RocmPower(RocmMetric):
    """Parse rocm-smi for GPU total power draw (in Watts)."""

    _cmd: str = 'rocm-smi --showpower --csv'
    _pattern: re.Pattern = re.compile(r'^card(\d),(\d+(?:\.\d+)?)')

    @classmethod
    def parse_text(cls, block: str) -> Dict[str, Dict[int, float]]:
        """Parse `rocm-smi` output."""
        try:
            data = {}
            lines = block.strip().split('\n')  # NOTE: lines[0]  == 'device,Average Graphics Package Power (W)'
            for line in lines[1:]:
                index, power = cls._pattern.match(line).groups()
                data[int(index)] = float(power)
            return {'power': data}
        except Exception as error:
            raise RuntimeError(f'Failed to parse output ({cls._cmd}): {error}') from error
