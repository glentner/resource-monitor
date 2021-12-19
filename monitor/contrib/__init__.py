# This program is free software: you can redistribute it and/or modify it under the
# terms of the Apache License (v2.0) as published by the Apache Software Foundation.
#
# This program is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
# PARTICULAR PURPOSE. See the Apache License for more details.
#
# You should have received a copy of the Apache License along with this program.
# If not, see <https://www.apache.org/licenses/LICENSE-2.0>.

"""External providers of system resource telemetry (e.g., nvidia-smi)."""


# type annotations
from __future__ import annotations
from typing import Dict, Type, Optional

# standard libs
import functools
from subprocess import check_output

# internal libs
from ..core.extern import ExternalMetric
from .nvidia import NvidiaPercent, NvidiaMemory, NvidiaTemperature, NvidiaPower
from .rocm import RocmPercent, RocmMemory, RocmTemperature, RocmPower

# public interface
__all__ = ['SMIData', ]


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
    def provider_map(self) -> Dict[str, Dict[str, Type[ExternalMetric]]]:
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
