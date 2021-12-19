# This program is free software: you can redistribute it and/or modify it under the
# terms of the Apache License (v2.0) as published by the Apache Software Foundation.
#
# This program is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
# PARTICULAR PURPOSE. See the Apache License for more details.
#
# You should have received a copy of the Apache License along with this program.
# If not, see <https://www.apache.org/licenses/LICENSE-2.0>.

"""Monitor CPU resources."""


# standard libs
import sys

# external libs
from cmdkit.app import Application
from cmdkit.cli import Interface, ArgumentError

# internal libs
from ... import __appname__
from ...core.logging import Logger
from ...core.exceptions import CompletedCommand

# resource commands
from .percent import CPUPercent
from .memory import CPUMemory

# public interface
__all__ = ['CPUDevice', ]


RESOURCES = {
    'percent': CPUPercent,
    'memory': CPUMemory,
}


PROGRAM = f'{__appname__} cpu'

USAGE = f"""\
usage: {PROGRAM} [-h] <resource> [<args>...]
{__doc__}\
"""

HELP = f"""\
{USAGE}

resources:
percent            {CPUPercent.__doc__}
memory             {CPUMemory.__doc__}

options:
-h, --help         Show this message and exit.

Use the -h/--help flag with the above resource groups to
learn more about their usage.\
"""


log = Logger.with_name('cpu')


class CPUDevice(Application):
    """Monitor CPU resources."""

    interface = Interface(PROGRAM, USAGE, HELP)

    resource: str = None
    interface.add_argument('resource')

    exceptions = {
        CompletedCommand: (lambda exc: int(exc.args[0])),
    }

    def run(self) -> None:
        """Show usage/help/version or defer to group."""
        if self.resource in RESOURCES:
            status = RESOURCES[self.resource].main(sys.argv[3:])
            raise CompletedCommand(status)
        else:
            raise ArgumentError(f'"{self.resource}" is not a CPU resource.')
