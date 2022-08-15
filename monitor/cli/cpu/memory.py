# This program is free software: you can redistribute it and/or modify it under the
# terms of the Apache License (v2.0) as published by the Apache Software Foundation.
#
# This program is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
# PARTICULAR PURPOSE. See the Apache License for more details.
#
# You should have received a copy of the Apache License along with this program.
# If not, see <https://www.apache.org/licenses/LICENSE-2.0>.

"""Monitor CPU memory utilization."""


# type annotations
from __future__ import annotations
from typing import Callable
from types import ModuleType

# standard libs
import time
import functools

# external libs
import psutil
from cmdkit.app import Application, exit_status
from cmdkit.cli import Interface, ArgumentError

# internal libs
from ...core.exceptions import log_and_exit
from ...core.logging import Logger, PLAIN_HANDLER, CSV_HANDLER
from ... import __appname__

# public interface
__all__ = ['CPUMemory', ]


PROGRAM = f'{__appname__} cpu memory'

USAGE = f"""\
usage: {PROGRAM} [-h] [PID] [-s SECONDS] [--actual [--human-readable]] [--csv [--no-header]]
{__doc__}\
"""

HELP = f"""\
{USAGE}

arguments:
PID                             Process ID (default is system-wide).

options:
    --percent                   Report value as a percentage (default).
    --actual                    Report value as total bytes.
-s, --sample-rate     SECONDS   Time between samples (default: 1).
-H, --human-readable            Human readable values (e.g., "8.2G").
    --plain                     Print messages in syslog format (default).
    --csv                       Print messages in CSV format.
    --no-header                 Suppress printing header in CSV mode.
-h, --help                      Show this message and exit.\
"""


log = Logger.with_name('cpu.memory')


SCALES = ['', 'K', 'M', 'G', 'T']
def format_size(num: float, scale_units: bool = False, divisor: int = 1024) -> str:
    """Convert raw `num` to human-readable string."""
    if scale_units is False:
        return str(num)
    for suffix in SCALES:
        if abs(num) < divisor:
            return f'{num:4.2f}{suffix}'
        num /= divisor


class CPUMemory(Application):
    """Monitor CPU memory utilization."""

    ALLOW_NOARGS = True  # no usage behavior
    interface = Interface(PROGRAM, USAGE, HELP)

    pid: int = None
    interface.add_argument('pid', nargs='?', type=int, default=None)

    sample_rate: float = 1
    interface.add_argument('-s', '--sample-rate', type=float, default=sample_rate)

    human_readable: bool = False
    interface.add_argument('-H', '--human-readable', action='store_true')

    display_type: str = 'percent'
    memory_interface = interface.add_mutually_exclusive_group()
    memory_interface.add_argument('--actual', action='store_const', const='actual', dest='display_type')
    memory_interface.add_argument('--percent', action='store_const', const='percent',
                                  dest='display_type', default=display_type)

    format_type: str = 'plain'
    format_interface = interface.add_mutually_exclusive_group()
    format_interface.add_argument('--csv', action='store_const', const='csv', dest='format_type')
    format_interface.add_argument('--plain', action='store_const', const='plain',
                                  dest='format_type', default=format_type)

    no_header: bool = False
    interface.add_argument('--no-header', action='store_true')

    exceptions = {
        RuntimeError: functools.partial(log_and_exit, logger=log.critical,
                                        status=exit_status.runtime_error),
    }

    def run(self) -> None:
        """Run monitor."""

        if not self.format_type == 'csv' and self.no_header:
            raise ArgumentError('--no-header only applies to --csv mode.')

        if not self.display_type == 'actual' and self.human_readable:
            raise ArgumentError('"--human-readable" only applies to "--actual" values.')

        log.handlers[0] = PLAIN_HANDLER
        if self.format_type == 'csv':
            log.handlers[0] = CSV_HANDLER
            if not self.no_header:
                print(f'timestamp,hostname,resource,memory_{self.display_type}')

        formatter = functools.partial(format_size, scale_units=self.human_readable)
        while True:
            time.sleep(self.sample_rate)
            log.debug(formatter(self.get_memory()))

    @functools.cached_property
    def process(self: CPUMemory) -> psutil.Process:
        """Access single process or all process information."""
        return psutil.Process(pid=self.pid)

    @functools.cached_property
    def get_memory(self: CPUMemory) -> Callable[[], int | float]:
        """Access appropriate method."""
        return self.memory_percent if self.display_type == 'percent' else self.memory_actual

    def memory_actual(self: CPUMemory) -> int:
        """Total memory used by system or specific process."""
        if not self.pid:
            return psutil.virtual_memory().used
        else:
            return int((self.memory_percent() / 100) * psutil.virtual_memory().available)

    def memory_percent(self: CPUMemory) -> float:
        """Percent memory used by system or specific process."""
        if not self.pid:
            return psutil.virtual_memory().percent
        else:
            return round(self._memory_percent(), 2)

    def _memory_percent(self) -> float:
        """Compute percent memory usage for process and all child processes."""
        return (
                self.process.memory_percent() +
                sum(child.memory_percent() for child in self.process.children(recursive=True))
        )
