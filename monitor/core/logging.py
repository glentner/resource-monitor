# This program is free software: you can redistribute it and/or modify it under the
# terms of the Apache License (v2.0) as published by the Apache Software Foundation.
#
# This program is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
# PARTICULAR PURPOSE. See the Apache License for more details.
#
# You should have received a copy of the Apache License along with this program.
# If not, see <https://www.apache.org/licenses/LICENSE-2.0>.

"""Logging configuration for resource-monitor."""

# type annotations
from __future__ import annotations
from typing import List, Callable

# standard libraries
import io
import sys
import socket
from datetime import datetime
from dataclasses import dataclass

# external libraries
from logalpha import levels, colors, messages, handlers, loggers
from cmdkit import logging as _cmdkit_logging

# internal library
from ..__meta__ import __appname__


# get hostname from `socket` instead of `.config`
HOSTNAME = socket.gethostname()

# NOTICE messages won't actually be formatted with color.
LEVELS = levels.Level.from_names(['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'])
COLORS = colors.Color.from_names(['blue', 'green', 'yellow', 'red', 'magenta'])
RESET = colors.Color.reset


# NOTE: global handler list lets `Logger.with_name` instances aware of changes
#       to other logger's handlers. (i.e., changing from SimpleConsoleHandler to ConsoleHandler).
_handlers = []


@dataclass
class Message(messages.Message):
    """A `logalpha.messages.Message` with a timestamp:`datetime` and source:`str`."""
    timestamp: datetime
    source: str


class Logger(loggers.Logger):
    """Logger for resource-monitor."""

    Message: type = Message
    callbacks: dict = {'timestamp': datetime.now,
                       'source': (lambda: __appname__)}

    @classmethod
    def with_name(cls, name: str) -> Logger:
        """Inject alternate `name` into callbacks."""
        self = cls()
        self.callbacks = {**self.callbacks, 'source': (lambda: f'{__appname__}.{name}')}
        return self

    @property
    def handlers(self) -> List[handlers.Handler]:
        """Overide of local handlers to global list."""
        global _handlers
        return _handlers

    # FIXME: explicitly named aliases to satisfy pylint;
    #        these levels are already available but pylint complains
    debug: Callable[[str], None]
    info: Callable[[str], None]
    warning: Callable[[str], None]
    error: Callable[[str], None]
    critical: Callable[[str], None]


@dataclass
class BasicHandler(handlers.Handler):
    """Write shorter messages to <stdout> with color."""

    level: levels.Level = LEVELS[0]
    resource: io.TextIOWrapper = sys.stdout

    def format(self, msg: Message) -> str:
        """Colorize the log level and with only the message."""
        COLOR = Logger.colors[msg.level.value].foreground
        return f'{COLOR}{msg.level.name.lower():<8}{RESET} {msg.content}'


@dataclass
class PlainHandler(handlers.Handler):
    """Messages in syslog style format."""

    level: levels.Level = LEVELS[0]
    resource: io.TextIOWrapper = sys.stdout

    def format(self, msg: Message) -> str:
        timestamp = msg.timestamp.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
        return f'{timestamp} {HOSTNAME} {msg.source} {msg.content}'


@dataclass
class CSVHandler(handlers.Handler):
    """Messages in CSV format."""

    level: levels.Level = LEVELS[0]
    resource: io.TextIOWrapper = sys.stdout

    def format(self, msg: Message) -> str:
        timestamp = msg.timestamp.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
        content = msg.content.replace('[','').replace('] ',',')
        source = msg.source.replace(f'{__appname__}.', '')
        return f'{timestamp},{HOSTNAME},{source},{content}'


BASIC_HANDLER = BasicHandler()
_handlers.append(BASIC_HANDLER)

# formatted output
PLAIN_HANDLER = PlainHandler()
CSV_HANDLER = CSVHandler()

# inject logger back into cmdkit library
_cmdkit_logging.log = Logger()
