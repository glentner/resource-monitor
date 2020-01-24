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
from typing import Mapping, Union, List, Dict, Any

# standard library
from abc import ABC as Abstract, abstractclassmethod
from subprocess import check_output
from datetime import datetime


class StatBase(Abstract):
    """Structured object from text-block."""

    _cmd: str = None
    _fields: List[str] = []

    def __init__(self, other: Union[Mapping, StatBase]) -> None:
        """Initialize directly from initial object."""
        for key, value in dict(other).items():
            if hasattr(self, key):
                setattr(self, key, value)
            else:
                raise AttributeError(f'{self.__class__.__name__} has no attribute "{key}"')

    @classmethod
    def from_text(cls, block: str) -> StatBase:
        """Parse text `block` for attributes."""
        attrs = cls.parse_text(block)
        return cls(attrs)

    @classmethod
    def from_cmd(cls, cmd: str = _cmd, shell: bool = False) -> StatBase:
        """Execute `cmd` in a subprocess and parse text block."""
        block = check_output(cmd, shell=shell).decode()
        return cls.from_text(block)

    @abstractclassmethod
    def parse_text(cls, block: str) -> Mapping:
        """Parse the text `block` and return attributes."""

    def keys(self) -> List[str]:
        """List of fields."""
        return self._fields

    def values(self) -> List[Any]:
        """List of values of fields."""
        return [getattr(self, field) for field in self._fields]

    def __getitem__(self, key: str) -> Any:
        """Access to attribute by key allows dict conversion."""
        return getattr(self, key)

    def __str__(self) -> str:
        """String representation."""
        mappable = dict(self)
        return f'{self.__class__.__name__}({mappable})'

    def __repr__(self) -> str:
        """String representation."""
        return str(self)


class GPUStat(StatBase):
    """Status object for GPU resource utilization."""

    # one per GPU
    temp: List[float] = None
    power: List[float] = None
    usage: List[float] = None
    memory: List[float] = None
    _fields = ['temp', 'power', 'usage', 'memory']


NVIDIA_OUTER = '+-----------------------------------------------------------------------------+'
NVIDIA_TOP_HLINE = '|-------------------------------+----------------------+----------------------+'
NVIDIA_INNER_SINGLE = '+-------------------------------+----------------------+----------------------+'
NVIDIA_INNER_DOUBLE = '|===============================+======================+======================|'

class NvidiaStat(GPUStat):
    """Create GPU stat from `nvidia-smi` command."""

    _cmd: str = 'nvidia-smi'

    @classmethod
    def from_cmd(cls) -> NvidiaStat:
        """Run nvidia-smi to get stats."""
        return super().from_cmd('nvidia-smi')

    @classmethod
    def parse_text(cls, block: str) -> Dict[str, List[float]]:
        """Parse `nvidia-smi` output."""

        lines = block.strip().split('\n')

        timestamp    = lines[0].strip()
        upper_border = lines[1].strip()
        upper_header = lines[2].strip()
        first_hline  = lines[3].strip()
        header_1     = lines[4].strip()
        header_2     = lines[5].strip()
        middle_hline = lines[6].strip()

        i = 7
        top_lines = []
        num_lines = []
        while True:
            top_lines.append(lines[i])
            num_lines.append(lines[i+1])
            if not lines[i+3].strip():
                break
            else:
                i += 3

        try:
            datetime.strptime(timestamp, '%a %b %d %H:%M:%S %Y')
            assert upper_border == NVIDIA_OUTER
            assert first_hline  == NVIDIA_TOP_HLINE
            assert middle_hline == NVIDIA_INNER_DOUBLE
            assert len(upper_header.split()) == 10
            assert len(header_1.split()) == 11
            assert len(header_2.split()) == 11

            for top_line, num_line in zip(top_lines, num_lines):
                assert len(top_line.split()) == 11
                assert len(num_line.split()) == 15

            temp = []
            power = []
            usage = []
            memory = []
            for line in num_lines:
                fields = line.split()

                assert fields[2].endswith('C')
                assert all(f.endswith('W') for f in fields[4:7:2])
                assert all(f.endswith('MiB') for f in fields[8:11:2])
                assert fields[12].endswith('%')

                temp.append(int(fields[2][:-1]))  # strip 'C'

                lo_pow, hi_pow = [int(f[:-1]) for f in  fields[4:7:2]]
                power.append(100 * lo_pow / hi_pow)

                lo_mem, hi_mem = [int(f[:-3]) for f in  fields[8:11:2]]
                mem = 100 * lo_mem / hi_mem
                memory.append(float(f'{mem:.2f}'))

                usage.append(float(fields[12][:-1]))

        except (AssertionError, ValueError):
            raise RuntimeError('nvidia-smi had unrecognized formatting')

        return {'temp': temp, 'power': power,
                'usage': usage, 'memory': memory}
