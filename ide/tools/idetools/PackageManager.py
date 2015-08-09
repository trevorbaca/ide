# -*- encoding: utf-8 -*-
from __future__ import print_function
import os
from abjad.tools import stringtools
from abjad.tools import systemtools
from ide.tools.idetools.AbjadIDEConfiguration import AbjadIDEConfiguration
from ide.tools.idetools.Controller import Controller
from ide.tools.idetools.Command import Command
configuration = AbjadIDEConfiguration()


class PackageManager(Controller):
    r'''Package manager.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_basic_breadcrumb',
        '_optional_directories',
        '_optional_files',
        '_package_creation_callback',
        '_path',
        '_required_directories',
        '_required_files',
        )

    ### INITIALIZER ###

    def __init__(self, path=None, session=None):
        assert session is not None
        assert path is not None and os.path.sep in path
        superclass = super(PackageManager, self)
        superclass.__init__(session=session)
        self._basic_breadcrumb = None
        self._breadcrumb_callback = None
        self._optional_directories = (
            '__pycache__',
            'test',
            )
        self._optional_files = ()
        self._package_creation_callback = None
        self._path = path
        self._required_directories = ()
        self._required_files = (
            '__init__.py',
            '__metadata__.py',
            )

    ### SPECIAL METHODS ###

    def __repr__(self):
        r'''Gets interpreter representation of manager.

        Returns string.
        '''
        return '{}({!r})'.format(type(self).__name__, self._path)

    ### PRIVATE METHODS ###

    def _configure_as_material_package_manager(self):
        self._basic_breadcrumb = 'MATERIALS'
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

    def _configure_as_score_package_manager(self):
        self._basic_breadcrumb = 'SCORES'
        self._breadcrumb_callback = self._get_title_metadatum
        self._optional_directories = (
            '__pycache__',
            'etc',
            'test',
            )
        self._package_creation_callback = \
            self._make_score_into_installable_package
        self._required_directories = (
            'build',
            'distribution',
            'makers',
            'materials',
            'segments',
            'stylesheets',
            )
        self._required_files = (
            '__init__.py',
            '__metadata__.py',
            os.path.join('makers', '__init__.py'),
            os.path.join('materials', '__init__.py'),
            os.path.join('segments', '__init__.py'),
            )

    def _configure_as_segment_package_manager(self):
        self._basic_breadcrumb = 'SEGMENTS'
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

    def _make_asset_menu_section(self, menu):
        directory_entries = self._list_directory(self._path, smart_sort=True)
        menu_entries = []
        for directory_entry in directory_entries:
            clean_directory_entry = directory_entry
            if directory_entry.endswith('/'):
                clean_directory_entry = directory_entry[:-1]
            path = os.path.join(self._path, clean_directory_entry)
            menu_entry = (directory_entry, None, None, path)
            menu_entries.append(menu_entry)
        menu.make_asset_section(menu_entries=menu_entries)

    def _make_package(self, path):
        assert not os.path.exists(path)
        os.mkdir(path)
        with self._session._io_manager._silent():
            arguments = []
            for argument_name in self.check_package.argument_names:
                argument = getattr(self, argument_name)
                arguments.append(argument)
            self.check_package(
                *arguments,
                return_supply_messages=True,
                supply_missing=True
                )
        if self._package_creation_callback is not None:
            outer_path = self._get_outer_score_package_path(path)
            inner_path = os.path.join(outer_path, os.path.basename(path))
            new_path = self._package_creation_callback(
                inner_path,
                outer_path,
                )
            if new_path is not None:
                self._path = new_path

    def _run_package_manager(self):
        controller = self._session._io_manager._controller(
            consume_local_backtrack=True,
            controller=self,
            )
        directory = systemtools.TemporaryDirectoryChange(self._path)
        with controller, directory:
                self._enter_run()
                self._session._pending_redraw = True
                while True:
                    result = self._session.navigation_command_name
                    if not result:
                        menu = self._make_main_menu()
                        result = menu._run()
                        self._handle_pending_redraw_directive(
                            self._session,
                            result,
                            )
                        self._handle_wrangler_navigation_directive(
                            self._session,
                            result,
                            )
                    if self._exit_run():
                        break
                    elif not result:
                        continue
                    self._handle_input(result)
                    if self._exit_run():
                        break