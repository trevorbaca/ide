import abjad
import os


class Menu(abjad.AbjadObject):
    r'''Menu.

    ..  container:: example

        ::

            >>> menu = ide.Menu()

        ::

            >>> commands = []
            >>> commands.append(('foo - add', 'add'))
            >>> commands.append(('foo - delete', 'delete'))
            >>> commands.append(('foo - modify', 'modify'))
            >>> section = menu.make_command_section(
            ...     commands=commands,
            ...     name='test',
            ...     )

        ::

            >>> menu
            Menu()

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_break_on_return',
        '_header',
        '_io_manager',
        '_menu_sections',
        '_name',
        '_title',
        )

    _action_command_section_order = (
        'star',
        'system',
        'global files',
        'tests',
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

    _navigation_command_section_order = (
        'display navigation',
        'scores',
        'comparison',
        'navigation',
        'sibling navigation',
        'back-home-quit',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        break_on_return=None,
        header=None,
        io_manager=None,
        name=None,
        title=None,
        ):
        self._break_on_return = break_on_return
        self._header = header
        self._io_manager = io_manager
        self._menu_sections = []
        self._name = name
        self._title = title

    ### SPECIAL METHODS ###

    def __call__(self, string=None):
        r'''Calls menu on `string`.

        Returns response.
        '''
        import ide
        if string is not None:
            self._io_manager._pending_input = string
        if self._io_manager._is_redrawing:
            self._redraw()
            self._io_manager._is_redrawing = False
        while True:
            payload = None
            string = self._io_manager._get_input(split_input=True)
            if self._io_manager._is_quitting:
                break
            elif string == '?':
                self._redraw(command_type='action')
                continue
            elif string == ';':
                self._redraw(command_type='navigation')
                continue
            elif string in ('', '<return>'):
                if self.break_on_return:
                    break
                else:
                    self._redraw()
                    continue
            elif bool(self._match_command(string)):
                payload = self._match_command(string)
            elif bool(self._match_asset(string)):
                payload = self._match_asset(string)
            elif bool(self._match_range(string)):
                payload = self._match_range(string)
            break
        known = (payload is not None)
        return ide.Response(known=known, payload=payload, string=string)

    def __getitem__(self, argument):
        r'''Gets menu section in menu.

        Returns menu section.
        '''
        return self.menu_sections.__getitem__(argument)

    ### PRIVATE METHODS ###

    def _enclose_in_list(self, argument):
        if self._has_ranged_section():
            return [argument]
        else:
            return argument

    def _get_terminal_dimensions(self):
        result = os.popen('stty size', 'r').read().split()
        if result:
            terminal_height, terminal_width = result
            terminal_height = int(terminal_height)
            terminal_width = int(terminal_width)
        else:
            terminal_height, terminal_width = 24, 80
        return terminal_height, terminal_width

    def _has_command(self, command_name):
        for section in self.menu_sections:
            for entry in section.menu_entries:
                if entry.key == command_name:
                    return True
        return False

    def _has_numbered_section(self):
        return any(_.is_numbered for _ in self.menu_sections)

    def _has_ranged_section(self):
        return any(_.is_ranged for _ in self.menu_sections)

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

    def _make_asset_lines(self):
        lines = []
        for section in self:
            if not section.is_asset_section:
                continue
            lines_ = section._make_lines()
            lines_ = self._make_bicolumnar(lines_)
            lines.extend(lines_)
        return lines

    def _make_bicolumnar(
        self,
        lines,
        break_only_at_blank_lines=False,
        is_test=False,
        ):
        if self._io_manager._is_test:
            return lines
        terminal_height, terminal_width = self._get_terminal_dimensions()
        if terminal_width < 80:
            return lines
        if len(lines) < terminal_height - 8:
            return lines
        lines = [_.strip() for _ in lines]
        if lines[0] == '':
            lines.pop(0)
        midpoint = int(len(lines)/2)
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
        left_lines = [self._left_justify(_, left_width) for _ in left_lines]
        right_lines = [self._left_justify(_, right_width) for _ in right_lines]
        left_margin_width = 0
        left_margin_width = 4
        gutter_width = 1
        left_margin = left_margin_width * ' '
        gutter = gutter_width * ' '
        conjoined_lines = []
        for _ in abjad.sequence([left_lines, right_lines]).zip(truncate=False):
            if len(_) == 1:
                left_line = _[0]
                conjoined_line = left_margin + left_line
            elif len(_) == 2:
                left_line, right_line = _
                conjoined_line = left_margin + left_line + gutter + right_line
            conjoined_lines.append(conjoined_line)
        return conjoined_lines

    def _make_command_lines(self):
        result = []
        section_names = []
        for section in self.menu_sections:
            if section.name in section_names:
                raise Exception(f'{self!r} contains duplicate {section!r}.')
            else:
                section_names.append(section.name)
            if section.is_hidden:
                continue
            if section.is_asset_section:
                continue
            section_menu_lines = section._make_lines()
            result.extend(section_menu_lines)
        return result

    def _make_help_lines(self, command_type):
        assert command_type in ('action', 'navigation'), repr(command_type)
        lines = []
        menu_sections = self._sort_menu_sections(command_type=command_type)
        for menu_section in menu_sections:
            found_one = False
            if not menu_section.is_command_section:
                continue
            for menu_entry in menu_section:
                if command_type == 'action' and menu_entry.is_navigation:
                    continue
                if (command_type == 'navigation' and not
                    menu_entry.is_navigation):
                    continue
                found_one = True
                key = menu_entry.key
                display_string = menu_entry.display_string
                menu_line = 4 * ' '
                menu_line += f'{display_string} ({key})'
                lines.append(menu_line)
            if found_one:
                lines.append('')
        if lines:
            lines.pop()
        lines = self._make_bicolumnar(lines, break_only_at_blank_lines=True)
        title = self.header
        assert isinstance(title, str), repr(title)
        if command_type == 'action':
            title = title + ' : action commands'
        elif command_type == 'navigation':
            title = title + ' : navigation commands'
        else:
            raise ValueError(repr(command_type))
        title = abjad.String(title).capitalize_start()
        lines[0:0] = [title, '']
        lines.append('')
        return lines

    def _make_lines(self):
        lines = []
        lines.extend(self._make_title_lines())
        lines.extend(self._make_asset_lines())
        if lines and not all(_ == ' ' for _ in lines[-1]):
            lines.append('')
        lines.extend(self._make_command_lines())
        return lines

    def _make_section(
        self,
        display_prepopulated_values=False,
        is_asset_section=False,
        is_command_section=False,
        is_hidden=False,
        is_numbered=False,
        is_ranged=False,
        match_on_display_string=True,
        menu_entries=None,
        name=None,
        return_value_attribute='display_string',
        title=None,
        ):
        import ide
        assert not (is_numbered and self._has_numbered_section())
        assert not (is_ranged and self._has_ranged_section())
        section = ide.MenuSection(
            display_prepopulated_values=display_prepopulated_values,
            is_asset_section=is_asset_section,
            is_command_section=is_command_section,
            is_hidden=is_hidden,
            is_numbered=is_numbered,
            is_ranged=is_ranged,
            match_on_display_string=match_on_display_string,
            menu_entries=menu_entries,
            name=name,
            return_value_attribute=return_value_attribute,
            title=title,
            )
        self.menu_sections.append(section)
        self.menu_sections.sort(key=lambda _: _.name)
        noncommand_sections = [
            _ for _ in self.menu_sections
            if not _.is_command_section
            ]
        for noncommand_section in noncommand_sections:
            self.menu_sections.remove(noncommand_section)
        for noncommand_section in noncommand_sections:
            self.menu_sections.insert(0, noncommand_section)
        return section

    def _make_title_lines(self):
        result = []
        if self.header is not None:
            title = self.header
        elif self.title is not None:
            title = self.title
        else:
            title = ''
        result.append(abjad.String(title).capitalize_start())
        result.append('')
        return result

    def _match_asset(self, result):
        import ide
        for section in self.menu_sections:
            if not section.is_asset_section:
                continue
            return_value = None
            for entry in section:
                if entry.key is not None and result == self.key:
                    return self._enclose_in_list(entry.return_value)
            for entry in section:
                if (entry.menu_section.is_numbered and
                    result == str(entry.number)):
                    return self._enclose_in_list(entry.return_value)
            if not section.match_on_display_string:
                continue
            strings = [abjad.String(_.display_string) for _ in section]
            string = ide.Path._smart_match(strings, result)
            if string is not None:
                entry = section[strings.index(string)]
                return self._enclose_in_list(entry.return_value)

    def _match_command(self, result):
        for section in self.menu_sections:
            if section.is_asset_section:
                continue
            for menu_entry in section:
                if (menu_entry.matches(result)):
                    return_value = menu_entry.return_value
                    result = self._enclose_in_list(return_value)
                    return result

    def _match_range(self, result):
        for section in self.menu_sections:
            if not section.is_ranged:
                continue
            entry_numbers = section._range_string_to_numbers(result)
            if not entry_numbers:
                continue
            entry_indices = [_ - 1 for _ in entry_numbers]
            result = []
            for i in entry_indices:
                entry = section._menu_entry_return_values[i]
                result.append(entry)
            return result

    def _redraw(self, command_type=None):
        self._io_manager.clear_terminal()
        if command_type is not None:
            lines = self._make_help_lines(command_type=command_type)
        else:
            lines = self._make_lines()
        height, width = self._get_terminal_dimensions()
        lines = [_[:width] for _ in lines]
        self._io_manager._display(lines, caps=False, is_menu=True)

    def _sort_menu_sections(self, command_type):
        ordered_menu_sections = []
        menu_sections = {}
        for menu_section in self.menu_sections:
            menu_sections[menu_section.name] = menu_section
        if command_type == 'navigation':
            order = self._navigation_command_section_order
        elif command_type == 'action':
            order = self._action_command_section_order
        else:
            raise ValueError(repr(command_type))
        for section_name in order:
            menu_section = menu_sections.get(section_name)
            if menu_section is not None:
                ordered_menu_sections.append(menu_section)
        return ordered_menu_sections

    ### PUBLIC PROPERTIES ###

    @property
    def break_on_return(self):
        r'''Is true when menu breaks on empty return.

        Returns true, false or none.
        '''
        return self._break_on_return

    @property
    def header(self):
        r'''Gets explicit title.

        Returns string or none.
        '''
        return self._header

    @property
    def io_manager(self):
        r'''Gets IO manager.

        Returns IO manager.
        '''
        return self._io_manager

    @property
    def menu_sections(self):
        r'''Gets menu sections.

        Returns list.
        '''
        return self._menu_sections

    @property
    def name(self):
        r'''Gets name.

        Returns string.
        '''
        return self._name

    @property
    def title(self):
        r'''Gets title.

        Returns string or none.
        '''
        return self._title

    ### PUBLIC METHODS ###

    def make_asset_section(
        self,
        menu_entries=None,
        is_numbered=True,
        name='assets',
        ):
        r'''Makes asset section.

        With these attributes:

            * is asset section
            * is numbered
            * return value set to explicit

        Returns menu section.
        '''
        section = self._make_section(
            is_asset_section=True,
            is_numbered=is_numbered,
            menu_entries=menu_entries,
            name=name,
            return_value_attribute='explicit',
            )
        return section

    def make_command_section(
        self,
        is_hidden=False,
        match_on_display_string=False,
        commands=None,
        name=None,
        ):
        r'''Makes command section.

        Menu section with these attributes:

            * is command section
            * is not hidden
            * does NOT match on display string
            * return value attribute equal to ``'key'``

        Returns menu section.
        '''
        section = self._make_section(
            is_command_section=True,
            is_hidden=is_hidden,
            match_on_display_string=match_on_display_string,
            menu_entries=commands,
            name=name,
            return_value_attribute='key',
            )
        return section
