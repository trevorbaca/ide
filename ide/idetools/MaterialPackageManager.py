# -*- encoding: utf-8 -*-
import copy
import os
import shutil
from abjad.tools import datastructuretools
from abjad.tools import stringtools
from abjad.tools import systemtools
from ide.idetools.PackageManager import PackageManager


class MaterialPackageManager(PackageManager):
    r'''Material package manager.
    '''

    ### INTIALIZER ###

    def __init__(self, path=None, session=None):
        superclass = super(MaterialPackageManager, self)
        superclass.__init__(path=path, session=session)
        self._optional_files = (
            '__illustrate__.py',
            'illustration.ly',
            'illustration.pdf',
            'maker.py',
            )
        self._required_files = (
            '__init__.py',
            '__metadata__.py',
            'definition.py',
            )

    ### PRIVATE METHODS ###

    def _make_illustrate_py_menu_section(self, menu):
        commands = []
        if os.path.isfile(self._illustrate_py_path):
            is_hidden = False
            string = '__illustrate__.py - edit'
            commands.append((string, 'le'))
            string = '__illustrate__.py - stub'
            commands.append((string, 'ls'))
        else:
            is_hidden = True
            string = '__illustrate__.py - stub'
            commands.append((string, 'ls'))
        menu.make_command_section(
            is_hidden=is_hidden,
            commands=commands,
            name='__illustrate__.py',
            )

    def _make_illustration_pdf_menu_section(self, menu):
        commands = []
        if os.path.isfile(self._illustration_ly_path):
            commands.append(('illustration.ly - interpret', 'ii'))
            commands.append(('illustration.ly - edit', 'ie'))
        if os.path.isfile(self._illustration_pdf_path):
            commands.append(('illustration.pdf - open', 'io'))
        if commands:
            menu.make_command_section(
                commands=commands,
                name='illustration.pdf',
                )

    def _make_main_menu(self):
        superclass = super(MaterialPackageManager, self)
        menu = superclass._make_main_menu()
        self._make_illustrate_py_menu_section(menu)
        self._make_illustration_pdf_menu_section(menu)
        self._make_definition_py_menu_section(menu)
        self._make_package_menu_section(menu)
        self._make_sibling_asset_tour_menu_section(menu)
        return menu

    def _set_is_navigating_to_sibling_asset(self):
        self._session._is_navigating_to_materials = True