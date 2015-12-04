# -*- coding: utf-8 -*-
import os
import re
import shlex
from abjad.tools import sequencetools
from abjad.tools import stringtools


class Menu(object):
    r'''Menu.

    ..  container:: example

        ::

            >>> menu = ide.tools.idetools.Menu()

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
            <Menu (1)>

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_asset_section',
        '_explicit_header',
        '_io_manager',
        '_menu_sections',
        '_name',
        '_subtitle',
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
        'build-preliminary',
        'build-generate',
        'build-interpret',
        'build',
        'basic',
        'git',
        )

    _navigation_command_section_order = (
        'display navigation',
        'back-home-quit',
        'comparison',
        'navigation',
        'sibling navigation',
        )

    _tab = 4 * ' '

    ### INITIALIZER ###

    def __init__(
        self,
        explicit_header=None,
        name=None,
        subtitle=None,
        title=None,
        ):
        self._explicit_header = explicit_header
        self._io_manager = None
        self._menu_sections = []
        self._name = name
        self._subtitle = subtitle
        self._title = title

    ### SPECIAL METHODS ###

    def __getitem__(self, expr):
        r'''Gets menu section indexed by `expr`.

        Returns menu section with name equal to `expr` when `expr` is a string.

        Returns menu section at index `expr` when `expr` is an integer.
        '''
        if isinstance(expr, str):
            for section in self.menu_sections:
                if section.name == expr:
                    return section
            raise KeyError(expr)
        else:
            return self.menu_sections.__getitem__(expr)

    def __len__(self):
        r'''Gets number of menu sections in menu.

        Returns nonnegative integer.
        '''
        return len(self.menu_sections)

    def __repr__(self):
        r'''Gets interpreter representation of menu.

        Returns string.
        '''
        if self.name:
            string = '<{} {!r} ({})>'
            string = string.format(type(self).__name__, self.name, len(self))
        else:
            string = '<{} ({})>'
            string = string.format(type(self).__name__, len(self))
        return string

    ### PRIVATE METHODS ###

    def _change_input_to_directive(self, input_):
        r'''Match order:
        
            1. all command sections
            2. assets section, if it exists

        This avoids file name new-stylesheet.ily aliasing the (new) command.
        '''
        input_ = stringtools.strip_diacritics(input_)
        if input_.startswith(('@', '#', '%')):
            return input_
        if input_.startswith('!') and self._has_command('!'):
            return input_
        ends_with_bang = input_.endswith('!')
        if ends_with_bang and input_[:-1] == 'q':
            self._io_manager._clear_terminal_after_quit = True
        input_ = input_.strip('!')
        if self._user_enters_nothing(input_):
            default_value = None
            for section in self.menu_sections:
                if section._has_default_value:
                    default_value = section._default_value
            if default_value is not None:
                return self._enclose_in_list(default_value)
        asset_section = None
        for section in self.menu_sections:
            if section.is_asset_section:
                asset_section = section
                continue
            for menu_entry in section:
                if (menu_entry.matches(input_)):
                    return_value = menu_entry.return_value
                    if ends_with_bang:
                        return_value = return_value + '!'
                    return self._enclose_in_list(return_value)
        if asset_section is not None:
            for menu_entry in asset_section:
                if (menu_entry.matches(input_)):
                    return_value = menu_entry.return_value
                    if ends_with_bang:
                        return_value = return_value + '!'
                    return self._enclose_in_list(return_value)
        if self._user_enters_argument_range(input_):
            return self._handle_argument_range_input(input_)
        return (input_,)

    def _enclose_in_list(self, expr):
        if self._has_ranged_section():
            return [expr]
        else:
            return expr

    def _get_first_nonhidden_return_value_in_menu(self):
        for section in self.menu_sections:
            if section.is_hidden:
                continue
            if section._menu_entry_return_values:
                return section._menu_entry_return_values[0]

    def _handle_argument_range_input(self, input_):
        if not self._has_ranged_section():
            return
        for section in self.menu_sections:
            if section.is_ranged:
                ranged_section = section
        entry_numbers = ranged_section._argument_range_string_to_numbers(
            input_)
        if not entry_numbers:
            return
        entry_indices = [entry_number - 1 for entry_number in entry_numbers]
        result = []
        for i in entry_indices:
            entry = ranged_section._menu_entry_return_values[i]
            result.append(entry)
        return result

    def _handle_user_input(self):
        input_ = self._io_manager._handle_input(
            '', 
            prompt_character=self.prompt_character,
            )
        if input_ == '<return>':
            input_ = ''
        user_entered_lone_return = input_ in ('', '<return>')
        directive = None
        parts = shlex.split(input_, posix=False)
        length = len(parts)
        for i in range(len(parts)):
            count = length - i
            candidate = ' '.join(parts[:count])
            directive = self._change_input_to_directive(candidate)
            if directive is not None:
                if count < length:
                    remaining_count = length - count
                    remaining_parts = parts[-remaining_count:]
                    glued_remaining_parts = []
                    for remaining_part in remaining_parts:
                        remaining_part = remaining_part.replace(' ', '~')
                        glued_remaining_parts.append(remaining_part)
                    remaining_input = ' '.join(glued_remaining_parts)
                    pending_input = self._io_manager._session._pending_input or ''
                    pending_input = pending_input + remaining_input
                    self._io_manager._session._pending_input = pending_input
                    self._io_manager._session._pending_redraw = True
                break
        directive = self._strip_default_notice_from_strings(directive)
        if directive is None and user_entered_lone_return:
            result = '<return>'
        elif directive is None and not user_entered_lone_return:
            message = 'unknown command: {!r}.'
            message = message.format(input_)
            self._io_manager._display([message, ''])
            result = None
            if (self._io_manager._session.is_test and 
                not self._io_manager._session._allow_unknown_command_during_test):
                message = 'tests should contain no unknown commands.'
                raise Exception(message)
        else:
            result = directive
        return result

    def _has_command(self, command_name):
        for section in self.menu_sections:
            for entry in section.menu_entries:
                if entry.key == command_name:
                    return True
        return False

    def _has_numbered_section(self):
        return any(x.is_numbered for x in self.menu_sections)

    def _has_ranged_section(self):
        return any(x.is_ranged for x in self.menu_sections)

    @staticmethod
    def _left_justify(string, width):
        start_width = len(stringtools.strip_diacritics(string))
        if start_width < width:
            needed = width - start_width
            suffix = needed * ' '
            result = string + suffix
        else:
            result = string
        return result

    def _make_asset_lines(self):
        has_asset_section = False
        for section in self:
            if section.is_asset_section:
                has_asset_section = True
                break
        if not has_asset_section:
            return []
        assert section.is_asset_section
        lines = section._make_lines()
        lines = self._make_bicolumnar(lines, strip=False)
        return lines

    def _make_bicolumnar(
        self, 
        lines, 
        break_only_at_blank_lines=False,
        strip=True,
        ):
        # http://stackoverflow.com/questions/566746/
        # how-to-get-console-window-width-in-python
        result = os.popen('stty size', 'r').read().split()
        if result:
            terminal_height, terminal_width = result
            terminal_height = int(terminal_height)
            terminal_width = int(terminal_width)
        # returns none when run under py.test
        else:
            terminal_height, terminal_width = 24, 80
        if terminal_width <= 80:
            return lines
        if len(lines) < terminal_height - 8:
            return lines
        if strip:
            lines = [_.strip() for _ in lines]
        all_packages_lines = [_ for _ in lines if _.startswith('all')]
        lines = [_ for _ in lines if not _.startswith('all')]
        # remove consecutive blank lines from comprehension above
        clean_lines = []
        for line in lines:
            if line == '':
                if clean_lines and clean_lines[-1] == '':
                    continue
            clean_lines.append(line)
        # remove initial blank line
        if clean_lines[0] == '':
            clean_lines.pop(0)
        lines = clean_lines
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
        left_count, right_count = len(left_lines), len(right_lines)
        #assert right_count <= left_count, repr((left_count, right_count))
        if strip:
            left_width = max(len(_.strip()) for _ in left_lines)
            right_width = max(len(_.strip()) for _ in right_lines)
        else:
            left_width = max(len(_) for _ in left_lines)
            right_width = max(len(_) for _ in right_lines)
        left_lines = [self._left_justify(_, left_width) for _ in left_lines]
        right_lines = [self._left_justify(_, right_width) for _ in right_lines]
        if strip:
            left_margin_width, gutter_width = 4, 4 
        else:
            left_margin_width, gutter_width = 0, 4 
        left_margin = left_margin_width * ' '
        gutter = gutter_width * ' '
        conjoined_lines = []
        for _ in sequencetools.zip_sequences(
            [left_lines, right_lines],
            truncate=False,
            ):
            if len(_) == 1:
                left_line = _[0]
                conjoined_line = left_margin + left_line
            elif len(_) == 2:
                left_line, right_line = _
                conjoined_line = left_margin + left_line + gutter + right_line
            conjoined_lines.append(conjoined_line)
        if all_packages_lines:
            blank_line = left_margin
            conjoined_lines.append(blank_line)
        for line in all_packages_lines:
            conjoined_line = left_margin + line
            conjoined_lines.append(conjoined_line)
        return conjoined_lines

    def _make_command_lines(self):
        result = []
        section_names = []
        for section in self.menu_sections:
            if section.name in section_names:
                message = '{!r} contains duplicate {!r}.'
                message = message.format(self, section)
                raise Exception(message)
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
                menu_line = self._tab
                menu_line += '{} ({})'.format(display_string, key)
                lines.append(menu_line)
            if found_one:
                lines.append('')
        if lines:
            lines.pop()
        lines = self._make_bicolumnar(
            lines, 
            break_only_at_blank_lines=True,
            )
        title = self.explicit_header
        if command_type == 'action':
            title = title + ' - action commands'
        elif command_type == 'navigation':
            title = title + ' - navigation commands'
        else:
            raise ValueError(repr(command_type))
        title = stringtools.capitalize_start(title)
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
        default_index=None,
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
        from ide.tools import idetools
        assert not (is_numbered and self._has_numbered_section())
        assert not (is_ranged and self._has_ranged_section())
        section = idetools.MenuSection(
            default_index=default_index,
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
        self.menu_sections.sort(key=lambda x: x.name)
        noncommand_sections = [
            x for x in self.menu_sections
            if not x.is_command_section
            ]
        for noncommand_section in noncommand_sections:
            self.menu_sections.remove(noncommand_section)
        for noncommand_section in noncommand_sections:
            self.menu_sections.insert(0, noncommand_section)
        return section

    def _make_title_lines(self):
        result = []
        if self.explicit_header is not None:
            title = self.explicit_header
        elif self.title is not None:
            title = self.title
        else:
            title = ''
        result.append(stringtools.capitalize_start(title))
        if self.subtitle is not None:
            line = '  ' + self.subtitle
            result.append('')
            result.append(line)
        result.append('')
        return result

    def _redraw(self, command_type=None):
        self._io_manager._session._pending_redraw = False
        self._io_manager.clear_terminal()
        if command_type is not None:
            lines = self._make_help_lines(command_type=command_type)
        else:
            lines = self._make_lines()
        self._io_manager._display(
            lines, 
            capitalize=False, 
            is_menu=True,
            )

    def _return_value_to_location_pair(self, return_value):
        for i, section in enumerate(self.menu_sections):
            if return_value in section._menu_entry_return_values:
                j = section._menu_entry_return_values.index(return_value)
                return i, j

    def _run(self, io_manager):
        self._io_manager = io_manager
        while True:
            if self._io_manager._session.pending_redraw:
                self._redraw()
                message = self._io_manager._session._after_redraw_messages
                if message:
                    previous_input = self._io_manager._session.previous_input
                    prompt_string = '> ' + previous_input
                    self._io_manager._display(prompt_string)
                    self._io_manager._display(message)
                    self._io_manager._display('')
                    self._io_manager._session._after_redraw_messages = None
            result = None
            if not result:
                result = self._handle_user_input()
                self._io_manager._session._previous_input = result
            if self._io_manager._session.is_quitting:
                return result
            elif result == '<return>':
                self._io_manager._session._pending_redraw = True
                self._io_manager = None
                return
            elif result == '?':
                self._redraw(command_type='action')
            elif result == ';':
                self._redraw(command_type='navigation')
            else:
                self._io_manager = None
                return result
        self._io_manager = None

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

    @staticmethod
    def _strip_default_notice_from_strings(expr):
        if isinstance(expr, list):
            cleaned_list = []
            for element in expr:
                if element.endswith(' (default)'):
                    element = element.replace(' (default)', '')
                cleaned_list.append(element)
            return cleaned_list
        elif isinstance(expr, str):
            if expr.endswith(' (default)'):
                expr = expr.replace(' (default)', '')
            return expr
        else:
            return expr

    @staticmethod
    def _user_enters_argument_range(input_):
        if ',' in input_:
            return True
        if '-' in input_:
            return True
        return False

    @staticmethod
    def _user_enters_nothing(input_):
        if not input_:
            return True
        if 3 <= len(input_) and '<return>'.startswith(input_):
            return True
        return False

    ### PUBLIC PROPERTIES ###

    @property
    def explicit_header(self):
        r'''Gets explicit title.

        Returns string or none.
        '''
        return self._explicit_header

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
    def prompt_character(self):
        r'''Gets prompt character.

        Returns '>'.
        '''
        return '>'

    @property
    def subtitle(self):
        r'''Gets subtitle.

        Returns string or none.
        '''
        return self._subtitle

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
            is_numbered=True,
            menu_entries=menu_entries,
            name=name,
            return_value_attribute='explicit',
            )
        self._asset_section = section
        return section

    def make_command_section(
        self,
        is_hidden=False,
        default_index=None,
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
            default_index=default_index,
            is_command_section=True,
            is_hidden=is_hidden,
            match_on_display_string=match_on_display_string,
            menu_entries=commands,
            name=name,
            return_value_attribute='key',
            )
        return section