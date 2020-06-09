import os
import typing

import abjad

from .IO import IO
from .MenuEntry import MenuEntry
from .MenuSection import MenuSection
from .Response import Response


class Menu(object):
    """
    Menu.

    ..  container:: example

        >>> ide.Menu()
        Menu(io=IO(), navigations=OrderedDict([]), sections=[])

    """

    ### CLASS VARIABLES ###

    __slots__ = (
        "_aliases",
        "_getter",
        "_header",
        "_io",
        "_loop",
        "_navigations",
        "_prompt",
        "_sections",
    )

    left_margin_width = 6

    ### INITIALIZER ###

    def __init__(
        self,
        aliases: abjad.OrderedDict = None,
        getter: bool = None,
        header: str = None,
        io: IO = None,
        loop: bool = None,
        navigations: abjad.OrderedDict = None,
        prompt: str = None,
        sections: typing.List[MenuSection] = None,
    ) -> None:
        self._aliases = aliases
        self._getter = getter
        self._header = header
        self._io = io or IO()
        self._loop = loop
        self._navigations = navigations or abjad.OrderedDict()
        self._prompt = prompt
        self._sections = sections or []

    ### SPECIAL METHODS ###

    def __call__(
        self,
        string: str = None,
        dimensions: typing.Tuple[int, int] = None,
        force_single_column: bool = False,
        redraw: typing.Union[bool, str] = True,
    ) -> Response:
        """
        Calls menu on ``string``.
        """
        if string is not None:
            self.io.pending_input(string)
        self.redraw(
            redraw, dimensions=dimensions, force_single_column=force_single_column,
        )
        string = self.io.get(prompt=self.prompt, split_input=not self.getter)
        prefix, string = self._split_prefix(string)
        if string is None:
            payload = None
        elif string == "?":
            return self(dimensions=dimensions, redraw="help")
        elif string == ";":
            return self(dimensions=dimensions, force_single_column=True)
        elif string == "?;":
            return self(dimensions=dimensions, force_single_column=True, redraw="help")
        elif string == "" and self.loop:
            return self(dimensions=dimensions)
        elif string in self.navigations:
            payload = None
        elif bool(self._match_alias(string)):
            payload = self._match_alias(string)
        elif bool(self._match_command(string)):
            payload = self._match_command(string)
        elif bool(self._match_assets(string)):
            payload = self._match_assets(string)
        elif bool(self._match_range(string)):
            payload = self._match_range(string)
        else:
            payload = None
        if string:
            string = prefix + string
        elif prefix:
            string = prefix
        return Response(payload=payload, string=string)

    def __getitem__(self, argument) -> MenuSection:
        """
        Gets section in menu.
        """
        return self.sections.__getitem__(argument)

    def __repr__(self) -> str:
        """
        Gets interpreter representation.
        """
        return abjad.StorageFormatManager(self).get_repr_format()

    ### PRIVATE METHODS ###

    @staticmethod
    def _left_justify(string, width):
        start_width = len(string)
        if start_width < width:
            needed = width - start_width
            suffix = needed * " "
            result = string + suffix
        else:
            result = string
        return result

    def _make_bicolumnar(
        self, lines, lines_above, break_only_at_blank_lines=False, dimensions=None,
    ):
        if lines and lines[-1] != "":
            lines.append("")
        lines = [_.rstrip() for _ in lines]
        if len(lines) < 4:
            return lines
        if dimensions is False:
            return lines
        if isinstance(dimensions, tuple):
            height, width = dimensions
        else:
            result = os.popen("stty size", "r").read().split()
            if not result:
                return lines
            if result:
                height = int(result[0])
                width = int(result[1])
        if len(lines) < height - lines_above:
            return lines
        midpoint = int(len(lines) / 2)
        if break_only_at_blank_lines:
            while lines[midpoint] != "":
                midpoint += 1
            assert lines[midpoint] == ""
        left_lines = lines[:midpoint]
        if break_only_at_blank_lines:
            right_lines = lines[midpoint + 1 :]
            assert len(left_lines) + len(right_lines) == len(lines) - 1
        else:
            right_lines = lines[midpoint:]
        left_width = max(len(_) for _ in left_lines)
        right_width = max(len(_) for _ in right_lines)
        remaining = width - (left_width + right_width)
        if remaining % 2 == 0:
            gutter_width = right_margin = int(remaining / 2)
        else:
            right_margin = int(remaining / 2)
            gutter_width = remaining - right_margin
        assert gutter_width + right_margin == remaining
        left_lines = [self._left_justify(_, left_width) for _ in left_lines]
        right_lines = [
            self._left_justify(_, right_width + right_margin) for _ in right_lines
        ]
        sequence = abjad.sequence([left_lines, right_lines])
        lines = []
        for pair in sequence.zip(truncate=False):
            if len(pair) == 1:
                line = pair[0]
            elif len(pair) == 2:
                left_line, right_line = pair
                line = left_line + gutter_width * " " + right_line
            lines.append(line)
        if lines[-1].isspace():
            lines[-1] = ""
        if lines[-1] != "":
            lines.append("")
        return lines

    def _match_alias(self, string):
        if not self.aliases:
            return
        path = self.aliases.get(string)
        if path is not None:
            return [abjad.Path(path)]

    def _match_assets(self, string):
        for section in self.sections:
            if section.command:
                continue
            if abjad.mathtools.is_integer_equivalent(string):
                number = int(string)
                for entry in section:
                    if entry.number == number:
                        return [entry.value]
            paths = [abjad.Path(_.display) for _ in section]
            for i, path in enumerate(paths):
                for part in path.parts:
                    if part == "/":
                        continue
                    if part == string:
                        entry = section[i]
                        return [entry.value]
            strings, values = [abjad.String(_.display) for _ in section], []
            for i in abjad.String.match_strings(strings, string):
                entry = section[i]
                values.append(entry.value)
            if values:
                return values

    def _match_command(self, string):
        for section in self.sections:
            if not section.command:
                continue
            entry = section.match(string)
            if entry is not None:
                return entry.value

    def _match_range(self, string):
        if string.startswith("!"):
            return
        if "," not in string and "-" not in string:
            return
        for section in self.sections:
            numbers = section.range_string_to_numbers(string)
            if not numbers:
                continue
            indices = [_ - 1 for _ in numbers]
            string = []
            for i in indices:
                entry = [_.value for _ in section][i]
                string.append(entry)
            return string

    @staticmethod
    def _split_prefix(string):
        if string and 2 <= len(string) and string[0] == string[1] and string[0] == "@":
            prefix = string[:2]
            string = string[2:] or None
        elif string and 1 <= len(string) and string[0] == "@":
            prefix = string[:1]
            string = string[1:] or None
        else:
            prefix = ""
        return prefix, string

    ### PUBLIC PROPERTIES ###

    @property
    def aliases(self) -> typing.Optional[abjad.OrderedDict]:
        """
        Gets aliases.
        """
        return self._aliases

    @property
    def getter(self) -> typing.Optional[bool]:
        """
        Is true when menu consumes all input with spaces at one time.
        """
        return self._getter

    @property
    def header(self) -> typing.Optional[str]:
        """
        Gets header.
        """
        return self._header

    @property
    def io(self) -> IO:
        """
        Gets IO manager.
        """
        return self._io

    @property
    def loop(self) -> typing.Optional[bool]:
        """
        Is true when menu loops.
        """
        return self._loop

    @property
    def navigations(self) -> abjad.OrderedDict:
        """
        Gets navigation context.
        """
        return self._navigations

    @property
    def prompt(self) -> typing.Optional[str]:
        """
        Gets prompt.
        """
        return self._prompt

    @property
    def sections(self) -> typing.List[MenuSection]:
        """
        Gets menu sections.
        """
        return self._sections

    ### PUBLIC METHODS ###

    @staticmethod
    def from_directory(
        directory, header, aliases=None, io=None, navigations=None, sections=None
    ) -> "Menu":
        """
        Makes menu from ``directory``.
        """
        sections = sections or []
        entries = []
        for path in directory.list_secondary_paths():
            entry = MenuEntry(display=path.name, value=path)
            entries.append(entry)
        if entries:
            entries.sort(key=lambda _: _.display)
            section = MenuSection(entries=entries, secondary=True)
            sections.append(section)
        entries = []
        for path in directory.list_paths():
            if directory.is_wrapper():
                entry = MenuEntry(display=path.name, value=path)
            else:
                entry = MenuEntry(display=path.get_identifier(), value=path)
            entries.append(entry)
        if entries:
            section = MenuSection(entries=entries)
            sections.append(section)
        menu = Menu(
            aliases=aliases,
            # header=directory.get_header(),
            header=header,
            io=io,
            loop=True,
            navigations=navigations,
            sections=sections,
        )
        return menu

    def make_help_lines(self, dimensions=None, force_single_column=None):
        """
        Makes help lines.

        Returns list.
        """
        lines = []
        for section in self:
            if section.command:
                lines_ = section.make_lines(left_margin_width=4)
                lines.extend(lines_)
        if not force_single_column:
            lines = self._make_bicolumnar(
                lines,
                lines_above=2,
                break_only_at_blank_lines=True,
                dimensions=dimensions,
            )
        header = self.header + " : help"
        header = abjad.String(header).capitalize_start()
        lines[0:0] = [header, ""]
        return lines

    def make_lines(self, dimensions=None, force_single_column=False):
        """
        Makes lines.

        Returns list.
        """
        header = abjad.String(self.header or "").capitalize_start()
        lines = [header, ""]
        names = []
        for section in self:
            if section.command:
                if section.command in names:
                    raise Exception(f"Duplicate section {section.command!r}.")
                names.append(section.command)
            if section.command:
                continue
            lines_ = section.make_lines(self.left_margin_width)
            if (
                not section.secondary
                and not force_single_column
                and not section.force_single_column
            ):
                lines_ = self._make_bicolumnar(
                    lines_, len(lines), dimensions=dimensions
                )
            lines.extend(lines_)
        lines = [_.rstrip() for _ in lines]
        for line in lines:
            assert not line.isspace()
        assert lines[-1] == "", repr(lines)
        return lines

    def redraw(self, value, dimensions=None, force_single_column=False):
        """
        Redraws menu.

        Returns none.
        """
        if not value:
            return
        abjad.IOManager.clear_terminal()
        if value is True:
            lines = self.make_lines(
                dimensions=dimensions, force_single_column=force_single_column
            )
        else:
            lines = self.make_help_lines(
                dimensions=dimensions, force_single_column=force_single_column
            )
        self.io.display(lines, is_menu=True, raw=True)
