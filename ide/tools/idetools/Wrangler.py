# -*- encoding: utf-8 -*-
import os
from abjad.tools import sequencetools
from abjad.tools import stringtools
from abjad.tools import systemtools
from ide.tools.idetools.AbjadIDEConfiguration import AbjadIDEConfiguration
from ide.tools.idetools.Controller import Controller
configuration = AbjadIDEConfiguration()


class Wrangler(Controller):
    r'''Wrangler.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_directory_name',
        )

    ### INITIALIZER ###

    def __init__(self, session=None, io_manager=None):
        assert session is not None
        assert io_manager is not None
        superclass = super(Wrangler, self)
        superclass.__init__(session=session, io_manager=io_manager)
        self._directory_name = None

    ### SPECIAL METHODS ###

    def __repr__(self):
        r'''Gets interpreter representation of wrangler.

        Returns string.
        '''
        return '{}({!r})'.format(type(self).__name__, self._directory_name)

    ### PRIVATE METHODS ###

    def _make_wrangler_asset_menu_section(self, menu, directory=None):
        menu_entries = []
        if directory is not None:
            current_directory = directory
        else:
            current_directory = self._get_current_directory()
        if current_directory:
            menu_entries_ = self._make_secondary_asset_menu_entries(
                current_directory)
            menu_entries.extend(menu_entries_)
        menu_entries.extend(
            self._make_asset_menu_entries(self._directory_name))
        if menu_entries:
            section = menu.make_asset_section(menu_entries=menu_entries)
            assert section is not None
            section._group_by_annotation = not self._directory_name == 'scores'

    def _select_storehouse(self, example_score_packages=False):
        menu_entries = self._make_storehouse_menu_entries(
            self._directory_name,
            composer_score_packages=False,
            example_score_packages=example_score_packages,
            )
        current_directory = self._get_current_directory()
        if current_directory is not None:
            menu_header = self._path_to_menu_header(current_directory)
        elif self._directory_name == 'scores':
            menu_header = 'Abjad IDE - all score directories'
        else:
            menu_header = 'Abjad IDE - all {} directories'
            menu_header = menu_header.format(self._directory_name)
        selector = self._io_manager._make_selector(
            menu_entries=menu_entries,
            menu_header=menu_header,
            target_name='storehouse',
            )
        result = selector._run(io_manager=self._io_manager)
        if self._session.is_backtracking or result is None:
            return
        return result

    def _select_view(self, infinitive_phrase=None, is_ranged=False):
        from ide.tools import idetools
        directory_token = self._get_current_directory_token()
        view_inventory = self._read_view_inventory(
            directory_token,
            )
        if view_inventory is None:
            message = 'no views found.'
            self._io_manager._display(message)
            return
        view_names = list(view_inventory.keys())
        view_names.append('none')
        if is_ranged:
            target_name = 'view(s)'
        else:
            target_name = 'view'
        if infinitive_phrase:
            target_name = '{} {}'.format(target_name, infinitive_phrase)
        current_directory = self._get_current_directory()
        if current_directory is not None:
            menu_header = self._path_to_menu_header(current_directory)
        elif self._directory_name == 'scores':
            menu_header = 'Abjad IDE - all score directories'
        else:
            menu_header = 'Abjad IDE - all {} directories'
            menu_header = menu_header.format(self._directory_name)
        selector = self._io_manager._make_selector(
            is_ranged=is_ranged,
            items=view_names,
            menu_header=menu_header,
            target_name=target_name,
            )
        result = selector._run(io_manager=self._io_manager)
        if self._session.is_backtracking or result is None:
            return
        return result

    def _select_visible_asset_path(self, infinitive_phrase=None):
        getter = self._io_manager._make_getter()
        asset_identifier = self._directory_name_to_asset_identifier[
            self._directory_name]
        message = 'enter {}'.format(asset_identifier)
        if infinitive_phrase:
            message = message + ' ' + infinitive_phrase
        if hasattr(self, '_make_wrangler_asset_menu_section'):
            dummy_menu = self._io_manager._make_menu()
            self._make_wrangler_asset_menu_section(dummy_menu)
            asset_section = dummy_menu._asset_section
        else:
            menu = self._make_asset_selection_menu()
            asset_section = menu['assets']
        getter.append_menu_section_item(
            message, 
            asset_section,
            )
        numbers = getter._run(io_manager=self._io_manager)
        if self._session.is_backtracking or numbers is None:
            return
        if not len(numbers) == 1:
            return
        number = numbers[0]
        index = number - 1
        paths = [_.return_value for _ in asset_section.menu_entries]
        path = paths[index]
        return path

    def _select_visible_asset_paths(self):
        getter = self._io_manager._make_getter()
        asset_identifier = self._directory_name_to_asset_identifier[
            self._directory_name]
        message = 'enter {}(s) to remove'
        message = message.format(asset_identifier)
        menu = self._make_asset_selection_menu()
        asset_section = menu['assets']
        getter.append_menu_section_range(
            message, 
            asset_section,
            )
        numbers = getter._run(io_manager=self._io_manager)
        if self._io_manager._is_backtracking or numbers is None:
            return
        indices = [_ - 1 for _ in numbers]
        paths = [_.return_value for _ in asset_section.menu_entries]
        paths = sequencetools.retain_elements(paths, indices)
        return paths