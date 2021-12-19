# This program is free software: you can redistribute it and/or modify it under the
# terms of the Apache License (v2.0) as published by the Apache Software Foundation.
#
# This program is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
# PARTICULAR PURPOSE. See the Apache License for more details.
#
# You should have received a copy of the Apache License along with this program.
# If not, see <https://www.apache.org/licenses/LICENSE-2.0>.

"""Monitor GPU memory utilization."""


# type annotations
from __future__ import annotations

# standard libs
import time
import functools

# external libs
from cmdkit.app import Application, exit_status
from cmdkit.cli import Interface, ArgumentError

# internal libs
from ... import __appname__
from ...contrib import SMIData
from ...core.exceptions import log_and_exit
from ...core.logging import Logger, PLAIN_HANDLER, CSV_HANDLER

# public interface
__all__ = ['GPUMemory', ]


PROGRAM = f'{__appname__} gpu memory'

USAGE = f"""\
usage: {PROGRAM} [-h] [-s SECONDS] [--csv [--no-header]]
{__doc__}\
"""

HELP = f"""\
{USAGE}

options:
-s, --sample-rate  SECONDS     Time between samples (default: 1).
    --plain                    Print messages in syslog format (default).
    --csv                      Print messages in CSV format.
    --no-header                Suppress printing header in CSV mode.
-h, --help                     Show this message and exit.\
"""


log = Logger.with_name('gpu.memory')


class GPUMemory(Application):
    """Monitor GPU memory utilization."""

    ALLOW_NOARGS = True
    interface = Interface(PROGRAM, USAGE, HELP)

    sample_rate: float = 1
    interface.add_argument('-s', '--sample-rate', type=float, default=sample_rate)

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
                print('timestamp,hostname,resource,gpu_id,gpu_memory')

        smi = SMIData()
        while True:
            time.sleep(self.sample_rate)
            for gpu_id, gpu_memory in smi.memory.items():
                log.debug(f'[{gpu_id}] {gpu_memory}')
