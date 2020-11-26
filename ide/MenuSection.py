import typing

import abjad

from .Configuration import Configuration
from .MenuEntry import MenuEntry


class MenuSection:
    """
    Menu section.
    """

    ### CLASS VARIABLES ###

    __slots__ = ("_command", "_entries", "_force_single_column", "_secondary")

    configuration = Configuration()

    ### INITIALIZER ###

    def __init__(
        self,
        command: bool = None,
        entries: typing.List[MenuEntry] = None,
        force_single_column: bool = None,
        secondary: bool = None,
    ) -> None:
        object.__init__(self)
        if command is not None:
            assert isinstance(command, str), repr(command)
        self._command = command
        self._force_single_column = force_single_column
        self._secondary = secondary
        self._initialize_entries(entries)

    ### SPECIAL METHODS ###

    def __getitem__(self, argument) -> MenuEntry:
        """
        Gets entry indexed by ``argument``.
        """
        return self.entries.__getitem__(argument)

    def __iter__(self) -> typing.Iterator:
        """
        Iterates entries.
        """
        return self.entries.__iter__()

    ### PRIVATE METHODS ###

    def _initialize_entries(self, entries):
        self._entries = []
        for i, entry in enumerate(entries):
            if not self.command and not self.secondary:
                number = i + 1
            else:
                number = None
            if isinstance(entry, MenuEntry):
                display = entry.display
                value = entry.value
            elif isinstance(entry, tuple):
                assert len(entry) == 2, repr(entry)
                display = entry[0]
                value = entry[1]
            else:
                raise TypeError(entry)
            entry = MenuEntry(
                display=display,
                command=self.command,
                number=number,
                value=value,
            )
            self.entries.append(entry)
        if self.command:
            self.entries.sort()

    ### PUBLIC PROPERTIES ###

    @property
    def command(self) -> typing.Optional[bool]:
        """Is true when section lists commands."""
        return self._command

    @property
    def entries(self) -> typing.List[MenuEntry]:
        """
        Gets entries.
        """
        return self._entries

    @property
    def force_single_column(self) -> typing.Optional[bool]:
        """
        Is true when section forces single column.
        """
        return self._force_single_column

    @property
    def secondary(self) -> typing.Optional[bool]:
        """
        Is true when section lists secondary assets.
        """
        return self._secondary

    ### PUBLIC METHODS ###

    def make_lines(self, left_margin_width) -> typing.List[str]:
        """
        Makes lines.
        """
        lines = [_.make_line(left_margin_width) for _ in self]
        if lines:
            lines.append("")
        return lines

    def match(self, string) -> typing.Optional[MenuEntry]:
        """
        Gets entry that matches ``string``.
        """
        if self.command:
            for entry in self:
                if entry.value == string:
                    return entry
        elif abjad.math.is_integer_equivalent(string):
            for entry in self:
                if str(entry.number) == string:
                    return entry
        else:
            strings = [_.display for _ in self]
            for i in abjad.String.match_strings(strings, string):
                return self[i]
        return None

    def range_string_to_numbers(
        self, string
    ) -> typing.Optional[typing.List[typing.Optional[int]]]:
        """
        Changes range ``string`` to numbers.
        """
        string = string.strip()
        assert self.entries
        if not self.entries[0].number:
            return None
        numbers = []
        if "," in string:
            parts = string.split(",")
        else:
            parts = [string]
        for part in parts:
            part = part.strip()
            entry = self.match(part)
            if entry is not None:
                numbers.append(entry.number)
                continue
            if part == "all":
                numbers.extend(range(1, len(self.entries) + 1))
            elif part.count("-") == 1:
                start, stop = part.split("-")
                start = start.strip()
                stop = stop.strip()
                entry = self.match(start)
                if entry is not None:
                    start = entry.number
                else:
                    start = None
                entry = self.match(stop)
                if entry is not None:
                    stop = entry.number
                else:
                    stop = None
                if start is None or stop is None:
                    break
                if start <= stop:
                    new_numbers = range(start, stop + 1)
                    numbers.extend(new_numbers)
                else:
                    new_numbers = range(start, stop - 1, -1)
                    numbers.extend(new_numbers)
            else:
                entry = self.match(part)
                if entry is None:
                    break
                numbers.append(entry.number)
        return numbers
