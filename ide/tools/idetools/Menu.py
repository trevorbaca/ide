import abjad
from ide.tools.idetools.IOManager import IOManager
from ide.tools.idetools.MenuEntry import MenuEntry
from ide.tools.idetools.MenuSection import MenuSection
from ide.tools.idetools.Path import Path
from ide.tools.idetools.Response import Response


class Menu(abjad.AbjadObject):
    r'''Menu.

    ..  container:: example

        ::

            >>> ide.Menu()
            Menu(io=IOManager(), navigations={}, sections=[])

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_aliases',
        '_getter',
        '_header',
        '_io',
        '_loop',
        '_navigations',
        '_prompt',
        '_sections',
        )

    # TODO: move up to AbjadIDE
    _action_command_section_order = (
        'star',
        'system',
        'global files',
        'tests',
        'clipboard',
        'definition_file',
        'illustrate_file',
        'ly',
        'pdf',
        'ly & pdf',
        'midi',
        'build-preliminary',
        'build-generate',
        'build-edit',
        'build-interpret',
        'build-open',
        'builds',
        'scripts',
        'basic',
        'git',
        )

    # TODO: move up to AbjadIDE
    _navigation_command_section_order = (
        'display navigation',
        'scores',
        'comparison',
        'navigation',
        'sibling navigation',
        'back-home-quit',
        )

    left_margin_width = 6

    ### INITIALIZER ###

    def __init__(
        self,
        aliases=None,
        getter=None,
        header=None,
        io=None,
        loop=None,
        navigations=None,
        prompt=None,
        sections=None,
        ):
        self._aliases = aliases
        self._getter = getter
        self._header = header
        self._io = io or IOManager()
        self._loop = loop
        self._navigations = navigations or {}
        self._prompt = prompt
        self._sections = sections or []

    ### SPECIAL METHODS ###

    def __call__(self, string=None, redraw=True, force_single_column=False):
        r'''Calls menu on `string`.

        Returns response.
        '''
        if string is not None:
            self.io.pending_input(string)
        self.redraw(redraw, force_single_column=force_single_column)
        string = self.io.get(
            prompt=self.prompt,
            split_input=not self.getter,
            )
        if string == '!!':
            return self(force_single_column=True)
        elif string == '?':
            return self(redraw='action')
        elif string == ';':
            return self(redraw='navigation')
        elif string == '' and self.loop:
            return self()
        elif string in self.navigations:
            payload = None
        elif self.aliases and string in self.aliases:
            payload = None
        elif bool(self._match_command(string)):
            payload = self._match_command(string)
        elif bool(self._match_asset(string)):
            payload = self._match_asset(string)
        elif bool(self._match_range(string)):
            payload = self._match_range(string)
        else:
            payload = None
        return Response(payload=payload, string=string)

    def __getitem__(self, argument):
        r'''Gets section in menu.

        Returns section.
        '''
        return self.sections.__getitem__(argument)

    ### PRIVATE METHODS ###

    def _enclose_in_list(self, argument):
        for section in self:
            if section.multiple:
                return [argument]
        return argument

    @staticmethod
    def _left_justify(string, width):
        start_width = len(string)
        if start_width < width:
            needed = width - start_width
            suffix = needed * ' '
            result = string + suffix
        else:
            result = string
        return result

    def _make_bicolumnar(
        self,
        lines,
        lines_above,
        break_only_at_blank_lines=False,
        ):
        if lines and lines[-1] != '':
            lines.append('')
        dimensions = self.io._terminal_dimensions
        if not dimensions:
            return lines
        if len(lines) < 4:
            return lines
        lines = [_.rstrip() for _ in lines]
        height, width = dimensions
        if len(lines) < height - lines_above:
            return lines
        midpoint = int(len(lines) / 2)
        if break_only_at_blank_lines:
            while lines[midpoint] != '':
                midpoint += 1
            assert lines[midpoint] == ''
        left_lines = lines[:midpoint]
        if break_only_at_blank_lines:
            right_lines = lines[midpoint+1:]
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
            self._left_justify(_, right_width + right_margin)
            for _ in right_lines
            ]
        conjoined_lines = []
        sequence = abjad.sequence([left_lines, right_lines])
        lines = []
        for pair in sequence.zip(truncate=False):
            if len(pair) == 1:
                line = pair[0]
            elif len(pair) == 2:
                left_line, right_line = pair
                line = left_line + gutter_width * ' ' + right_line
            lines.append(line)
        if lines[-1].isspace():
            lines[-1] = ''
        if lines[-1] != '':
            lines.append('')
        return lines

    def _match_asset(self, string):
        for section in self.sections:
            if section.command:
                continue
            for entry in section:
                if (entry.number is not None and string == str(entry.number)):
                    return self._enclose_in_list(entry.value)
            strings = [abjad.String(_.display) for _ in section]
            result = Path.smart_match(strings, string)
            if result is not None:
                entry = section[strings.index(result)]
                return self._enclose_in_list(entry.value)

    def _match_command(self, string):
        for section in self.sections:
            if not section.command:
                continue
            entry = section.match(string)
            if entry is not None:
                return self._enclose_in_list(entry.value)

    def _match_range(self, string):
        for section in self.sections:
            if not section.multiple:
                continue
            numbers = section.range_string_to_numbers(string)
            if not numbers:
                continue
            indices = [_ - 1 for _ in numbers]
            string = []
            for i in indices:
                entry = [_.value for _ in section][i]
                string.append(entry)
            return string

    def _sort_command_sections(self, command_type):
        ordered_sections = []
        sections = {}
        for section in self.sections:
            if section.command:
                sections[section.command] = section
        if command_type == 'navigation':
            order = self._navigation_command_section_order
        elif command_type == 'action':
            order = self._action_command_section_order
        else:
            raise ValueError(repr(command_type))
        for command in order:
            section = sections.get(command)
            if section is not None:
                ordered_sections.append(section)
        return ordered_sections

    ### PUBLIC PROPERTIES ###

    @property
    def aliases(self):
        r'''Gets aliases.

        Returns dictionary or none.
        '''
        return self._aliases

    @property
    def getter(self):
        r'''Is true when menu consumes all input with spaces at one time.

        Returns true, false or none.
        '''
        return self._getter

    @property
    def header(self):
        r'''Gets header.

        Returns string or none.
        '''
        return self._header

    @property
    def io(self):
        r'''Gets IO manager.

        Returns IO manager.
        '''
        return self._io

    @property
    def loop(self):
        r'''Is true when menu loops.

        Returns true, false or none.
        '''
        return self._loop

    @property
    def navigations(self):
        r'''Gets navigation context.

        Returns dictionary or none.
        '''
        return self._navigations

    @property
    def prompt(self):
        r'''Gets prompt.

        Returns string or none.
        '''
        return self._prompt

    @property
    def sections(self):
        r'''Gets menu sections.

        Returns list.
        '''
        return self._sections

    ### PUBLIC METHODS ###

    @staticmethod
    def from_directory(
        directory,
        aliases=None,
        io=None,
        navigations=None,
        sections=None,
        ):
        r'''Makes menu from `directory`.

        Returns menu.
        '''
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
            header=directory.get_header(),
            io=io,
            loop=True,
            navigations=navigations,
            sections=sections,
            )
        return menu

    def make_help_lines(self, command_type):
        r'''Makes help lines.

        Returns list.
        '''
        assert command_type in ('action', 'navigation'), repr(command_type)
        lines = []
        sections = self._sort_command_sections(command_type=command_type)
        for section in sections:
            if not section.command:
                continue
            lines_ = section.make_lines(left_margin_width=4)
            lines.extend(lines_)
        lines = self._make_bicolumnar(
            lines,
            lines_above=2,
            break_only_at_blank_lines=True,
            )
        assert lines[-1] == ''
        header = self.header
        assert isinstance(header, str), repr(header)
        if command_type == 'action':
            header = header + ' : action commands'
        elif command_type == 'navigation':
            header = header + ' : navigation commands'
        else:
            raise ValueError(repr(command_type))
        header = abjad.String(header).capitalize_start()
        lines[0:0] = [header, '']
        return lines

    def make_lines(self, force_single_column=False):
        r'''Makes lines.

        Returns list.
        '''
        header = abjad.String(self.header or '').capitalize_start()
        lines = [header, '']
        names = []
        for section in self:
            if section.command:
                if section.command in names:
                    raise Exception(f'Duplicate section {section.command!r}.')
                names.append(section.command)
            if section.command:
                continue
            lines_ = section.make_lines(self.left_margin_width)
            if (not section.secondary and
                not force_single_column and
                not section.force_single_column):
                lines_ = self._make_bicolumnar(lines_, len(lines))
            lines.extend(lines_)
        return lines

    def redraw(self, value, force_single_column=False):
        r'''Redraws menu.

        Returns none.
        '''
        if not value:
            return
        self.io.clear_terminal()
        if value is True:
            lines = self.make_lines(force_single_column=force_single_column)
        else:
            lines = self.make_help_lines(command_type=value)
        if self.io._terminal_dimensions:
            height, width = self.io._terminal_dimensions
            lines = [_[:width] for _ in lines]
        self.io.display(lines, is_menu=True, raw=True)
