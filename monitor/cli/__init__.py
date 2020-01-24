# This program is free software: you can redistribute it and/or modify it under the
# terms of the Apache License (v2.0) as published by the Apache Software Foundation.
#
# This program is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
# PARTICULAR PURPOSE. See the Apache License for more details.
#
# You should have received a copy of the Apache License along with this program.
# If not, see <https://www.apache.org/licenses/LICENSE-2.0>.

"""Entry-point for resource-monitor."""

# standard libs
import sys
import platform

# ignore broken pipes
if platform.system() == 'Windows':
    # FIXME: how do we ignore broken pipes on windows?
    pass
else:
    from signal import signal, SIGPIPE, SIG_DFL
    signal(SIGPIPE, SIG_DFL)

# internal libs
from ..core.logging import Logger
from ..core.exceptions import CompletedCommand
from ..__meta__ import (__appname__, __version__, __description__,
                        __copyright__, __license__, __website__)

# external libs
from cmdkit.app import Application
from cmdkit.cli import Interface, ArgumentError

# resource commands
from .cpu import CPU
from .memory import Memory

RESOURCES = {
    'cpu': CPU,
    'memory': Memory,
}

PROGRAM = __appname__
PADDING = ' ' * len(PROGRAM)

USAGE = f"""\
usage: {PROGRAM} <resource> [<args>...]
       {PADDING} [--help] [--version]

{__description__}\
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
cpu                {CPU.__doc__}
memory             {Memory.__doc__}

options:
-h, --help         Show this message and exit.
-v, --version      Show the version and exit.

Use the -h/--help flag with the above resource groups to
learn more about their usage.

{EPILOG}\
"""


# initialize module level logger
log = Logger.with_name(__appname__)


class ResourceMonitor(Application):
    """Application class for resource-monitor."""

    interface = Interface(PROGRAM, USAGE, HELP)
    interface.add_argument('-v', '--version', version=__version__, action='version')

    resource: str = None
    interface.add_argument('resource')

    exceptions = {
        CompletedCommand: (lambda exc: int(exc.args[0])),
    }

    def run(self) -> None:
        """Show usage/help/version or defer to group."""

        if self.resource in RESOURCES:
            status = RESOURCES[self.resource].main(sys.argv[2:])
            raise CompletedCommand(status)
        else:
            raise ArgumentError(f'"{self.resource}" is not a resource.')


def main() -> int:
    """Entry-point for resource-monitor command line interface."""
    return ResourceMonitor.main(sys.argv[1:2])  # only the group if present
