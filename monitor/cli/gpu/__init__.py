# This program is free software: you can redistribute it and/or modify it under the
# terms of the Apache License (v2.0) as published by the Apache Software Foundation.
#
# This program is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
# PARTICULAR PURPOSE. See the Apache License for more details.
#
# You should have received a copy of the Apache License along with this program.
# If not, see <https://www.apache.org/licenses/LICENSE-2.0>.

"""Monitor GPU resources."""

# standard libs
import sys

# internal libs
from ...core.logging import Logger
from ...core.exceptions import CompletedCommand
from ...__meta__ import __appname__, __copyright__, __license__, __website__

# external libs
from cmdkit.app import Application
from cmdkit.cli import Interface, ArgumentError

# resource commands
from .percent import GPUPercent
from .memory import GPUMemory
from .power import GPUPower
from .temp import GPUTemp


RESOURCES = {
    'percent': GPUPercent,
    'memory': GPUMemory,
    'power': GPUPower,
    'temp': GPUTemp,
}


PROGRAM = f'{__appname__} gpu'
PADDING = ' ' * len(PROGRAM)

USAGE = f"""\
usage: {PROGRAM} <resource> [<args>...]
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

resources:
percent            {GPUPercent.__doc__}
memory             {GPUMemory.__doc__}
power              {GPUPower.__doc__}
temp               {GPUTemp.__doc__}

options:
-h, --help         Show this message and exit.

Use the -h/--help flag with the above resource groups to
learn more about their usage.

{EPILOG}\
"""


log = Logger.with_name('gpu')


class GPUDevice(Application):
    """Monitor GPU resources."""

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
            raise ArgumentError(f'"{self.resource}" is not a GPU resource.')
