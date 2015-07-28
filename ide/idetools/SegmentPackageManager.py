# -*- encoding: utf-8 -*-
import os
import shutil
from abjad.tools import systemtools
from ide.idetools.PackageManager import PackageManager


class SegmentPackageManager(PackageManager):
    r'''Segment package manager.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        )

    ### INITIALIZER ###

    def __init__(self, path=None, session=None):
        superclass = super(SegmentPackageManager, self)
        superclass.__init__(path=path, session=session)
        self._breadcrumb_callback = self._get_name_metadatum
        self._optional_files = (
            'illustration.ly',
            'illustration.pdf',
            )
        self._required_files = (
            '__init__.py',
            '__metadata__.py',
            'definition.py',
            )

    ### PRIVATE METHODS ###

    def _get_previous_segment_manager(self):
        wrangler = self._session._abjad_ide._segment_package_wrangler
        managers = wrangler._list_visible_asset_managers()
        for i, manager in enumerate(managers):
            if manager._path == self._path:
                break
        else:
            message = 'can not find segment package manager.'
            raise Exception(message)
        current_manager_index = i
        if current_manager_index == 0:
            return
        previous_manager_index = current_manager_index - 1
        previous_manager = managers[previous_manager_index]
        return previous_manager

    def _make_illustration_ly_menu_section(self, menu):
        commands = []
        if os.path.isfile(self._illustration_ly_path):
            commands.append(('illustration.ly - edit', 'ie'))
            commands.append(('illustration.ly - interpret', 'ii'))
        if commands:
            menu.make_command_section(
                is_hidden=True,
                commands=commands,
                name='illustration',
                )

    def _make_main_menu(self):
        superclass = super(SegmentPackageManager, self)
        menu = superclass._make_main_menu()
        self._make_definition_py_menu_section(menu)
        self._make_illustration_ly_menu_section(menu)
        self._make_package_menu_section(menu)
        self._make_sibling_asset_tour_menu_section(menu)
        self._make_main_visible_menu_section(menu)
        return menu

    def _make_main_visible_menu_section(self, menu):
        commands = []
        commands.append(('definition.py - illustrate', 'i'))
        if os.path.isfile(self._illustration_pdf_path):
            commands.append(('illustration.pdf - open', 'o'))
        if commands:
            menu.make_command_section(
                commands=commands,
                is_hidden=False,
                name='main visible section',
                )

    def _set_is_navigating_to_sibling_asset(self):
        self._session._is_navigating_to_segments = True

    def _update_order_dependent_segment_metadata(self):
        wrangler = self._session._abjad_ide._segment_package_wrangler
        wrangler._update_order_dependent_segment_metadata()