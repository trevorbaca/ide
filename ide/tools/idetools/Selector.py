# -*- coding: utf-8 -*-
from abjad.tools import stringtools


class Selector(object):
    r'''Selector.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_io_manager',
        '_is_numbered',
        '_is_ranged',
        '_items',
        '_menu_entries',
        '_menu_header',
        '_return_value_attribute',
        '_target_name',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        is_numbered=True,
        is_ranged=False,
        items=None,
        menu_entries=None,
        menu_header=None,
        return_value_attribute='explicit',
        target_name=None,
        ):
        assert not (menu_entries and items)
        self._io_manager = None
        self._is_numbered = is_numbered
        self._is_ranged = is_ranged
        self._items = items or []
        self._menu_entries = menu_entries or []
        self._menu_header = menu_header
        self._return_value_attribute = return_value_attribute
        self._target_name = target_name

    ### SPECIAL METHODS ###

    def __repr__(self):
        r'''Gets interpreter representation of selector.

        Returns string.
        '''
        return '{}()'.format(type(self).__name__)

    ### PRIVATE METHODS ###

    def _make_asset_menu_section(self, menu):
        menu_entries = self.menu_entries
        menu_entries = menu_entries or self._make_menu_entries()
        if not menu_entries:
            return
        menu._make_section(
            is_asset_section=True,
            is_numbered=self.is_numbered,
            is_ranged=self.is_ranged,
            menu_entries=menu_entries,
            name='assets',
            return_value_attribute=self.return_value_attribute,
            )

    def _make_main_menu(self):
        name = stringtools.to_space_delimited_lowercase(type(self).__name__)
        menu = self._io_manager._make_menu(
            explicit_header=self.menu_header,
            name=name, 
            )
        self._make_asset_menu_section(menu)
        return menu

    def _make_menu_entries(self):
        entries = []
        for item in self.items:
            entry = (
                self._io_manager._get_one_line_menu_summary(item),
                None,
                None,
                item,
                )
            entries.append(entry)
        return entries

    def _run(self, io_manager):
        assert io_manager is not None
        self._io_manager = io_manager
        self._io_manager._session._pending_redraw = True
        while True:
            menu = self._make_main_menu()
            print(menu.menu_sections)
            result = menu._run(io_manager=self._io_manager)
            if result is None:
                self._io_manager = None
                return
            elif result:
                self._io_manager = None
                return result
        self._io_manager = None

    ### PUBLIC PROPERTIES ###

    @property
    def is_numbered(self):
        r'''Is true when selector is numbered. Otherwise false.

        Returns true or false.
        '''
        return self._is_numbered

    @property
    def is_ranged(self):
        r'''Is true when selector is ranged. Otherwise false.

        Returns true or false.
        '''
        return self._is_ranged

    @property
    def items(self):
        r'''Gets selector items.

        Returns list.
        '''
        return self._items

    @property
    def menu_entries(self):
        r'''Gets menu entries of selector.

        Returns list.
        '''
        return self._menu_entries

    @property
    def menu_header(self):
        r'''Gets menu header of selector.

        Returns list.
        '''
        return self._menu_header

    @property
    def return_value_attribute(self):
        r'''Gets return value attribute of selector.

        Returns string.
        '''
        return self._return_value_attribute

    @property
    def target_name(self):
        r'''Gets selector target_name.

        Returns string or none.
        '''
        if self._target_name is None:
            return 'select:'
        else:
            return 'select {}:'.format(self._target_name)