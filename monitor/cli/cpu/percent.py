# This program is free software: you can redistribute it and/or modify it under the
# terms of the Apache License (v2.0) as published by the Apache Software Foundation.
#
# This program is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
# PARTICULAR PURPOSE. See the Apache License for more details.
#
# You should have received a copy of the Apache License along with this program.
# If not, see <https://www.apache.org/licenses/LICENSE-2.0>.

"""Monitor CPU percent utilization."""


# type annotations
from __future__ import annotations

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
__all__ = ['CPUPercent', ]


PROGRAM = f'{__appname__} cpu percent'
PADDING = ' ' * len(PROGRAM)

USAGE = f"""\
usage: {PROGRAM} [-h] [--all-cores] [-s SECONDS] [--csv [--no-header]]
{__doc__}\
"""

HELP = f"""\
{USAGE}

options:
-t, --total                    Show values for total cpu usage (default).
-a, --all-cores                Show values for individual cores.
-s, --sample-rate  SECONDS     Time between samples (default: 1).
    --plain                    Print messages in syslog format (default).
    --csv                      Print messages in CSV format.
    --no-header                Suppress printing header in CSV mode.
-h, --help                     Show this message and exit.\
"""


log = Logger.with_name('cpu.percent')


def cpu_total(callback, template: str = '{value}') -> None:
    """Log the total CPU utilization."""
    value = psutil.cpu_percent()
    callback(template.format(value=value))


def cpu_per_core(callback, template: str = '[{i}] {value}') -> None:
    """Log the CPU utilization per core."""
    for i, value in enumerate(psutil.cpu_percent(percpu=True)):  # noqa: type iterable
        callback(template.format(i=i, value=value))


class CPUPercent(Application):
    """Monitor CPU percent utilization."""

    ALLOW_NOARGS = True
    interface = Interface(PROGRAM, USAGE, HELP)

    sample_rate: float = 1
    interface.add_argument('-s', '--sample-rate', type=float, default=sample_rate)

    total: bool = False
    all_cores: bool = False
    core_interface = interface.add_mutually_exclusive_group()
    core_interface.add_argument('-t', '--total', action='store_true')
    core_interface.add_argument('-a', '--all-cores', action='store_true')

    format_plain: bool = True
    format_csv: bool = False
    format_interface = interface.add_mutually_exclusive_group()
    format_interface.add_argument('--plain', action='store_true', dest='format_plain')
    format_interface.add_argument('--csv', action='store_true', dest='format_csv')

    no_header: bool = False
    interface.add_argument('--no-header', action='store_true')

    exceptions = {
        RuntimeError: functools.partial(log_and_exit, logger=log.critical,
                                        status=exit_status.runtime_error),
    }

    def run(self) -> None:
        """Run monitor."""

        if not self.format_csv and self.no_header:
            raise ArgumentError('--no-header only applies to --csv mode.')

        log.handlers[0] = PLAIN_HANDLER
        if self.format_csv:
            log.handlers[0] = CSV_HANDLER
            if not self.no_header:
                if not self.all_cores:
                    print('timestamp,hostname,resource,cpu_percent')
                else:
                    print('timestamp,hostname,resource,cpu_id,cpu_percent')

        if not self.all_cores:
            log_usage = functools.partial(cpu_total, log.debug)
        else:
            log_usage = functools.partial(cpu_per_core, log.debug)

        while True:
            time.sleep(self.sample_rate)
            log_usage()
