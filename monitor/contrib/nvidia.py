# This program is free software: you can redistribute it and/or modify it under the
# terms of the Apache License (v2.0) as published by the Apache Software Foundation.
#
# This program is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
# PARTICULAR PURPOSE. See the Apache License for more details.
#
# You should have received a copy of the Apache License along with this program.
# If not, see <https://www.apache.org/licenses/LICENSE-2.0>.

"""External `nvidia-smi` metrics."""


# type annotations
from __future__ import annotations
from typing import Dict

# standard libs
from abc import ABC

# internal libs
from ..core.extern import ExternalMetric

# public interface
__all__ = ['NvidiaMetric', 'NvidiaPercent', 'NvidiaMemory', 'NvidiaPower', 'NvidiaTemperature', ]


class NvidiaMetric(ExternalMetric, ABC):
    """Status object for Nvidia GPU resource."""


class NvidiaPercent(NvidiaMetric):
    """Parse nvidia-smi for overall percent utilization."""

    _cmd: str = 'nvidia-smi --format=csv,noheader,nounits --query-gpu=index,utilization.gpu -c1'

    @classmethod
    def parse_text(cls, block: str) -> Dict[str, Dict[int, float]]:
        """Parse `nvidia-smi` output."""
        try:
            data = {}
            for line in block.strip().split('\n'):
                index, percent = map(float, line.strip().split(', '))
                data[int(index)] = percent
            return {'percent': data}
        except Exception as error:
            raise RuntimeError(f'Failed to parse output ({cls._cmd}): {error}') from error


class NvidiaMemory(NvidiaMetric):
    """Parse nvidia-smi for memory usage."""

    _cmd: str = 'nvidia-smi --format=csv,noheader,nounits --query-gpu=index,memory.used,memory.total -c1'

    @classmethod
    def parse_text(cls, block: str) -> Dict[str, Dict[int, float]]:
        """Parse `nvidia-smi` output."""
        try:
            data = {}
            for line in block.strip().split('\n'):
                index, current, total = map(float, line.strip().split(', '))
                data[int(index)] = current / total
            return {'memory': data}
        except Exception as error:
            raise RuntimeError(f'Failed to parse output ({cls._cmd}): {error}') from error


class NvidiaTemperature(NvidiaMetric):
    """Parse nvidia-smi for GPU temperature (in degrees C)."""

    _cmd: str = 'nvidia-smi --format=csv,noheader,nounits --query-gpu=index,temperature.gpu -c1'

    @classmethod
    def parse_text(cls, block: str) -> Dict[str, Dict[int, float]]:
        """Parse `nvidia-smi` output."""
        try:
            data = {}
            for line in block.strip().split('\n'):
                index, temp = map(float, line.strip().split(', '))
                data[int(index)] = temp
            return {'temp': data}
        except Exception as error:
            raise RuntimeError(f'Failed to parse output ({cls._cmd}): {error}') from error


class NvidiaPower(NvidiaMetric):
    """Parse nvidia-smi for GPU total power draw (in Watts +/- 5 Watts)."""

    _cmd: str = 'nvidia-smi --format=csv,noheader,nounits --query-gpu=index,power.draw -c1'

    @classmethod
    def parse_text(cls, block: str) -> Dict[str, Dict[int, float]]:
        """Parse `nvidia-smi` output."""
        try:
            data = {}
            for line in block.strip().split('\n'):
                index, power = map(float, line.strip().split(', '))
                data[int(index)] = power
            return {'power': data}
        except Exception as error:
            raise RuntimeError(f'Failed to parse output ({cls._cmd}): {error}') from error
