# -*- encoding: utf-8 -*-
from abjad.tools import stringtools
from ide.idetools.Controller import Controller


class Selector(Controller):
    r'''Selector.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_breadcrumb',
        '_is_numbered',
        '_is_ranged',
        '_items',
        '_menu_entries',
        '_return_value_attribute',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        breadcrumb=None,
        is_numbered=True,
        is_ranged=False,
        items=None,
        menu_entries=None,
        return_value_attribute='explicit',
        session=None,
        ):
        assert session is not None
        assert not (menu_entries and items)
        Controller.__init__(self, session=session)
        self._breadcrumb = breadcrumb
        self._is_numbered = is_numbered
        self._is_ranged = is_ranged
        self._items = items or []
        self._menu_entries = menu_entries or []
        self._return_value_attribute = return_value_attribute

    ### PRIVATE PROPERTIES ###

    @property
    def breadcrumb(self):
        r'''Gets selector breadcrumb.

        Returns string or none.
        '''
        if self._breadcrumb is None:
            return 'select:'
        else:
            return 'select {}:'.format(self._breadcrumb)

    ### PRIVATE METHODS ###

    def _make_asset_menu_section(self, menu):
        menu_entries = self.menu_entries
        menu_entries = menu_entries or self._make_menu_entries()
        if not menu_entries:
            return
        menu._make_section(
            group_by_annotation=False,
            is_asset_section=True,
            is_numbered=self.is_numbered,
            is_ranged=self.is_ranged,
            menu_entries=menu_entries,
            name='assets',
            return_value_attribute=self.return_value_attribute,
            )

    def _make_main_menu(self):
        name = self._spaced_class_name
        subtitle = stringtools.capitalize_start(self.breadcrumb)
        menu = self._io_manager._make_menu(name=name, subtitle=subtitle)
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

    def _run(self):
        with self._io_manager._controller(
            clear_terminal=True,
            consume_local_backtrack=True,
            controller=self,
            ):
            while True:
                menu = self._make_main_menu()
                result = menu._run()
                if self._session.is_backtracking:
                    return
                if result and not result == '<return>':
                    return result

    ### PUBLIC PROPERTIES ###

    @property
    def is_numbered(self):
        r'''Is true when selector is numbered. Otherwise false.

        Returns boolean.
        '''
        return self._is_numbered

    @property
    def is_ranged(self):
        r'''Is true when selector is ranged. Otherwise false.

        Returns boolean.
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
    def return_value_attribute(self):
        r'''Gets return value attribute of selector.

        Returns string.
        '''
        return self._return_value_attribute