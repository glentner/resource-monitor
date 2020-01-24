# This program is free software: you can redistribute it and/or modify it under the
# terms of the Apache License (v2.0) as published by the Apache Software Foundation.
#
# This program is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
# PARTICULAR PURPOSE. See the Apache License for more details.
#
# You should have received a copy of the Apache License along with this program.
# If not, see <https://www.apache.org/licenses/LICENSE-2.0>.

"""Monitor GPU power consumption (percent maximum)."""

# type annotations
from __future__ import annotations

# standard libs
import time
import functools

# internal libs
from ...core.stat import NvidiaStat
from ...core.exceptions import log_and_exit
from ...core.logging import Logger, PLAIN_HANDLER, CSV_HANDLER
from ...__meta__ import __appname__, __copyright__, __website__, __license__

# external libs
from cmdkit.app import Application, exit_status
from cmdkit.cli import Interface, ArgumentError


PROGRAM = f'{__appname__} gpu power'
PADDING = ' ' * len(PROGRAM)

USAGE = f"""\
usage: {PROGRAM} [--sample-rate SECONDS]
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
-s, --sample-rate  SECONDS     Time between samples (default: 1).
    --plain                    Print messages in syslog format (default).
    --csv                      Print messages in CSV format.
    --no-header                Suppress printing header in CSV mode.
-h, --help                     Show this message and exit.

{EPILOG}\
"""


# initialize module level logger
log = Logger.with_name('gpu.power')


class GPUPower(Application):
    """Monitor GPU power consumption (percent maximum)."""

    ALLOW_NOARGS = True
    interface = Interface(PROGRAM, USAGE, HELP)

    sample_rate: int = 1
    interface.add_argument('-s', '--sample-rate', type=int, default=sample_rate)

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
                print('timestamp,hostname,resource,gpu_id,gpu_power')

        while True:
            time.sleep(self.sample_rate)
            stat = NvidiaStat.from_cmd()
            for gpu_id, gpu_power in enumerate(stat.power):
                log.debug(f'[{gpu_id}] {gpu_power}')
