# -*- coding: utf-8 -*-
from abjad.tools import stringtools
from abjad.tools.abctools.AbjadObject import AbjadObject


class MenuEntry(AbjadObject):
    r'''Menu entry.

    ..  container:: example

        ::

            >>> menu = ide.tools.idetools.Menu()
            >>> commands = []
            >>> commands.append(('foo - add', 'add'))
            >>> commands.append(('foo - delete', 'delete'))
            >>> commands.append(('foo - modify', 'modify'))
            >>> section = menu.make_command_section(
            ...     commands=commands,
            ...     name='test',
            ...     )

        ::

            >>> for entry in section.menu_entries:
            ...     entry
            <MenuEntry: 'foo - add'>
            <MenuEntry: 'foo - delete'>
            <MenuEntry: 'foo - modify'>

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_display_string',
        '_explicit_return_value',
        '_key',
        '_is_navigation',
        '_menu_section',
        '_prepopulated_value',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        display_string=None,
        explicit_return_value=None,
        is_navigation=False,
        key=None,
        menu_section=None,
        prepopulated_value=None,
        ):
        self._display_string = display_string
        self._explicit_return_value = explicit_return_value
        assert MenuEntry._is_valid_key(key), repr(key)
        self._key = key
        self._is_navigation = is_navigation
        self._menu_section = menu_section
        self._prepopulated_value = prepopulated_value

    ### SPECIAL METHODS ###

    def __lt__(self, expr):
        r'''Is true when `expr` is a menu entry with a display string greater
        than that of this menu entry. Otherwise false.

        Returns true or false.
        '''
        if not isinstance(expr, type(self)):
            raise TypeError(expr)
        return self.display_string < expr.display_string

    def __repr__(self):
        r'''Gets interpreter representation of menu entry.

        Returns string.
        '''
        return '<{}: {!r}>'.format(type(self).__name__, self.display_string)

    ### PRIVATE PROPERTIES ###

    @property
    def _storage_format_specification(self):
        from abjad.tools import systemtools
        positional_argument_values = ()
        keyword_argument_names = (
            'display_string',
            'explicit_return_value',
            'key',
            'prepopulated_value',
            )
        return systemtools.StorageFormatSpecification(
            self,
            keyword_argument_names=keyword_argument_names,
            positional_argument_values=positional_argument_values,
            )

    ### PRIVATE METHODS ###

    @staticmethod
    def _is_valid_key(key):
        if key is None:
            return True
        if isinstance(key, str) and key.lower() == key:
            return True
        return False

    ### PUBLIC PROPERTIES ###

    @property
    def display_string(self):
        r'''Gets display string.

        Returns string.
        '''
        return self._display_string

    @property
    def explicit_return_value(self):
        r'''Gets explicit return value.

        Returns arbitrary value or none.
        '''
        return self._explicit_return_value

    @property
    def is_navigation(self):
        r'''Is true when menu entry is navigation. Otherwise false.

        Returns true or false.
        '''
        return self._is_navigation

    @property
    def key(self):
        r'''Gets key.

        Returns string or none.
        '''
        return self._key

    @property
    def menu_section(self):
        r'''Gets menu section.

        Returns menu section.
        '''
        return self._menu_section

    @property
    def number(self):
        r'''Gets number.

        Returns nonnegative integer or none.
        '''
        if self.menu_section.is_numbered:
            return self.menu_section.menu_entries.index(self) + 1

    @property
    def prepopulated_value(self):
        r'''Gets prepopulated value.

        Returns arbitrary value or none.
        '''
        return self._prepopulated_value

    @property
    def return_value(self):
        r'''Gets return value.

        Returns arbitrary value.
        '''
        if self.menu_section.return_value_attribute == 'number':
            return_value = str(self.number)
        elif self.menu_section.return_value_attribute == 'display_string':
            return_value = self.display_string
        elif self.menu_section.return_value_attribute == 'key':
            return_value = self.key
        elif self.menu_section.return_value_attribute == 'explicit':
            return_value = self.explicit_return_value
        assert return_value, repr((
            self.menu_section,
            self.menu_section.return_value_attribute,
            self,
            return_value,
            ))
        return return_value

    ### PUBLIC METHODS ###

    def matches(self, input_):
        r'''Is true when menu entry matches `input_` string.

        ..  container:: example

            ::

                >>> entry.matches('modify')
                True

        Otherwise false:

        ..  container:: example

            ::

                >>> entry.matches('asdf')
                False

        Returns true or false.
        '''
        normalized_display_string = stringtools.strip_diacritics(
            self.display_string)
        normalized_display_string = normalized_display_string.lower()
        display_capital_letters = [
            _ for _ in self.display_string
            if _.isupper()
            ]
        display_capital_letters = ''.join(display_capital_letters)
        if (self.menu_section.match_on_display_string and
            display_capital_letters and
            input_ == display_capital_letters):
            return True
        if self.key is not None and input_ == self.key:
            return True
        if self.menu_section.is_numbered and input_ == str(self.number):
            return True
        if (self.menu_section.match_on_display_string and 
            3 <= len(input_)):
            if normalized_display_string.startswith(input_.lower()):
                return True
        if (self.menu_section.match_on_display_string and
            input_ == self.display_string):
            return True
        if (self.menu_section.match_on_display_string and
            3 <= len(input_) and
            input_ in normalized_display_string):
            return True
        return False