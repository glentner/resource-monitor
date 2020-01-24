# This program is free software: you can redistribute it and/or modify it under the
# terms of the Apache License (v2.0) as published by the Apache Software Foundation.
#
# This program is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
# PARTICULAR PURPOSE. See the Apache License for more details.
#
# You should have received a copy of the Apache License along with this program.
# If not, see <https://www.apache.org/licenses/LICENSE-2.0>.

"""Monitor main memory usage."""

# type annotations
from __future__ import annotations

# standard libs
import time
import functools

# internal libs
from ..core.exceptions import log_and_exit
from ..core.logging import Logger, PLAIN_HANDLER, CSV_HANDLER
from ..__meta__ import __appname__, __copyright__, __website__, __license__

# external libs
import psutil
from cmdkit.app import Application, exit_status
from cmdkit.cli import Interface, ArgumentError


# program name is constructed from module file name
PROGRAM = f'{__appname__} memory'
PADDING = ' ' * len(PROGRAM)

USAGE = f"""\
usage: {PROGRAM} [--percent | --actual] [--sample-rate SECONDS] [--human-readable]
       {PADDING} [--plain | --csv [--no-header]]
       {PADDING} [--help]

{__doc__}\
"""

EPILOG = f"""\
Documentation and issue tracking at:
{__website__}

Copyright {__copyright__}
{__license__}.\
"""

HELP = f"""\
{USAGE}

options:
    --percent                   Report value as a percentage (default).
    --actual                    Report value as total bytes.
-s, --sample-rate     SECONDS   Time between samples (default: 1).
-H, --human-readable            Human readable values (e.g., "8.2G").
    --plain                     Print messages in syslog format (default).
    --csv                       Print messages in CSV format.
    --no-header                 Suppress printing header in CSV mode.
-h, --help                      Show this message and exit.

{EPILOG}\
"""


# initialize module level logger
log = Logger.with_name('memory')


SCALES = ['', 'K', 'M', 'G', 'T']
def format_size(num: float, scale_units: bool = False, divisor: int = 1024) -> str:
    """Convert raw `num` to human-readable string."""
    if scale_units is False:
        return str(num)
    for suffix in SCALES:
        if abs(num) < divisor:
            return f'{num:4.2f}{suffix}'
        num /= divisor


class Memory(Application):
    """Monitor main memory usage."""

    ALLOW_NOARGS = True  # no usage behavior
    interface = Interface(PROGRAM, USAGE, HELP)

    sample_rate: int = 1
    interface.add_argument('-s', '--sample-rate', type=int, default=sample_rate)

    human_readable: bool = False
    interface.add_argument('-H', '--human-readable', action='store_true')

    memory_actual: bool = False
    memory_percent: bool = True
    memory_interface = interface.add_mutually_exclusive_group()
    memory_interface.add_argument('--actual', action='store_true', dest='memory_actual')
    memory_interface.add_argument('--percent', action='store_true', dest='memory_percent')

    format_csv: bool = False
    format_plain: bool = True
    format_interface = interface.add_mutually_exclusive_group()
    format_interface.add_argument('--csv', action='store_true', dest='format_csv')
    format_interface.add_argument('--plain', action='store_true', dest='format_plain')

    no_header: bool = False
    interface.add_argument('--no-header', action='store_true')

    exceptions = {
        RuntimeError: functools.partial(log_and_exit, logger=log.critical,
                                        status=exit_status.runtime_error),
    }

    def run(self) -> None:
        """Run cpu monitor."""

        if not self.format_csv and self.no_header:
            raise ArgumentError('--no-header only applies to --csv mode.')

        mem_attr = 'used' if self.memory_actual else 'percent'
        if not self.memory_actual and self.human_readable:
            raise ArgumentError('"--human-readable" only applies to "--actual" values.')

        log.handlers[0] = PLAIN_HANDLER
        if self.format_csv:
            log.handlers[0] = CSV_HANDLER
            if not self.no_header:
                print(f'timestamp,hostname,resource,memory_{mem_attr}')

        formatter = functools.partial(format_size, scale_units=self.human_readable)
        while True:
            time.sleep(self.sample_rate)
            value = getattr(psutil.virtual_memory(), mem_attr)
            log.debug(formatter(value))

    def __enter__(self) -> Memory:
        """Initialize resources."""
        return self

    def __exit__(self, *exc) -> None:
        """Release resources."""
