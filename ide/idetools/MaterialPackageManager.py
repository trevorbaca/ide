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


    ..  container:: example

        ::

            >>> import os
            >>> configuration = ide.idetools.Configuration()
            >>> session = ide.idetools.Session()
            >>> path = os.path.join(
            ...     configuration.example_score_packages_directory,
            ...     'red_example_score',
            ...     'materials',
            ...     'performer_inventory',
            ...     )
            >>> manager = ide.idetools.MaterialPackageManager(
            ...     path=path,
            ...     session=session,
            ...     )
            >>> manager
            MaterialPackageManager('.../materials/performer_inventory')

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

    def _make_definition_py_menu_section(self, menu):
        commands = []
        commands.append(('definition.py - check', 'dc'))
        commands.append(('definition.py - edit', 'de'))
        commands.append(('definition.py - stub', 'ds'))
        menu.make_command_section(
            is_hidden=True,
            commands=commands,
            name='definition.py',
            )

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

    def _make_package(self):
        metadata = datastructuretools.TypedOrderedDict()
        assert not os.path.exists(self._path)
        os.mkdir(self._path)
        with self._io_manager._silent():
            self.check_package(
                return_supply_messages=True,
                supply_missing=True,
                )
            self._write_metadata_py(metadata)
            self._write_stub_definition_py()

    def _rename_interactively(
        self,
        extension=None,
        file_name_callback=None,
        force_lowercase=True,
        ):
        getter = self._io_manager._make_getter()
        getter.append_identifier('enter new package name', allow_spaces=True)
        new_package_name = getter._run()
        if self._session.is_backtracking or new_package_name is None:
            return
        new_package_name = stringtools.to_snake_case(new_package_name)
        base_name = os.path.basename(self._path)
        new_directory = self._path.replace(
            base_name,
            new_package_name,
            )
        messages = []
        messages.append('will change ...')
        messages.append(' FROM: {}'.format(self._path))
        messages.append('   TO: {}'.format(new_directory))
        self._io_manager._display(messages)
        result = self._io_manager._confirm()
        if self._session.is_backtracking or not result:
            return
        self._rename(new_directory)
        if not os.path.exists(new_directory):
            return
        for directory_entry in sorted(os.listdir(new_directory)):
            if directory_entry.endswith('.py'):
                path = os.path.join(new_directory, directory_entry)
                result = os.path.splitext(base_name)
                old_package_name, extension = result
                self._replace_in_file(
                    path,
                    old_package_name,
                    new_package_name,
                    )

    def _set_is_navigating_to_sibling_asset(self):
        self._session._is_navigating_to_materials = True

    def _write_stub_definition_py(self):
        lines = []
        lines.append(self._configuration.unicode_directive)
        lines.append(self._abjad_import_statement)
        lines.append('')
        lines.append('')
        line = '{} = None'.format(self._package_name)
        lines.append(line)
        contents = '\n'.join(lines)
        with open(self._definition_py_path, 'w') as file_pointer:
            file_pointer.write(contents)