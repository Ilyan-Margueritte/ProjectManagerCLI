"""
Command registry for PMCLI.

Each command module exposes a `COMMAND` instance of `CommandDef`.
The registry collects them and dispatches by name.
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Callable, List, Optional


@dataclass
class CommandDef:
    name: str
    description: str
    handler: Callable
    usage: str = ""          # e.g. "<project> <new_name>"
    min_args: int = 0        # minimum positional args after command name
    aliases: List[str] = field(default_factory=list)


class Registry:
    def __init__(self) -> None:
        self._commands: dict[str, CommandDef] = {}

    def register(self, cmd: CommandDef) -> None:
        self._commands[cmd.name] = cmd
        for alias in cmd.aliases:
            self._commands[alias] = cmd

    def get(self, name: str) -> Optional[CommandDef]:
        return self._commands.get(name)

    def all_commands(self) -> list[CommandDef]:
        """Return unique commands (no duplicates from aliases)."""
        seen = set()
        result = []
        for cmd in self._commands.values():
            if cmd.name not in seen:
                seen.add(cmd.name)
                result.append(cmd)
        return sorted(result, key=lambda c: c.name)

    def dispatch(self, name: str, args: list[str]) -> int:
        """
        Dispatch a command by name with the given args.
        Returns exit code (0 = success, 1 = error).
        """
        cmd = self.get(name)
        if cmd is None:
            return -1  # unknown command signal

        if len(args) < cmd.min_args:
            return -2  # not enough args signal — caller prints usage

        return cmd.handler(args) or 0


# Global singleton
REGISTRY = Registry()
