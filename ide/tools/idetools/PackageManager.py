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

    ### PUBLIC METHODS ###

    @Command(
        'ck', 
        argument_names=(
            '_path',
            '_basic_breadcrumb',
            '_optional_directories',
            '_optional_files',
            '_required_directories',
            '_required_files',
            ),
        outside_score=False,
        section='package', 
        )
    def check_package(
        self,
        directory,
        basic_breadcrumb,
        OPTIONAL_DIRECTORIES, 
        OPTIONAL_FILES,
        REQUIRED_DIRECTORIES,
        REQUIRED_FILES,
        problems_only=None,
        return_messages=False,
        return_supply_messages=False,
        supply_missing=None,
        ):
        r'''Checks package.

        Returns none.
        '''
        if problems_only is None:
            prompt = 'show problem assets only?'
            result = self._io_manager._confirm(prompt)
            if self._io_manager._is_backtracking or result is None:
                return
            problems_only = bool(result)
        optional_directories, optional_files = [], []
        missing_directories, missing_files = [], []
        required_directories, required_files = [], []
        supplied_directories, supplied_files = [], []
        unrecognized_directories, unrecognized_files = [], []
        names = self._list_directory(directory)
        if 'makers' in names:
            makers_initializer = os.path.join('makers', '__init__.py')
            if makers_initializer in REQUIRED_FILES:
                path = os.path.join(directory, makers_initializer)
                if os.path.isfile(path):
                    required_files.append(path)
        if 'materials' in names:
            materials_initializer = os.path.join('materials', '__init__.py')
            if materials_initializer in REQUIRED_FILES:
                path = os.path.join(directory, materials_initializer)
                if os.path.isfile(path):
                    required_files.append(path)
        if 'segments' in names:
            segments_initializer = os.path.join('segments', '__init__.py')
            if segments_initializer in REQUIRED_FILES:
                path = os.path.join(directory, segments_initializer)
                if os.path.isfile(path):
                    required_files.append(path)
        for name in names:
            path = os.path.join(directory, name)
            if os.path.isdir(path):
                if name in REQUIRED_DIRECTORIES:
                    required_directories.append(path)
                elif name in OPTIONAL_DIRECTORIES:
                    optional_directories.append(path)
                else:
                    unrecognized_directories.append(path)
            elif os.path.isfile(path):
                if name in REQUIRED_FILES:
                    required_files.append(path)
                elif name in OPTIONAL_FILES:
                    optional_files.append(path)
                else:
                    unrecognized_files.append(path)
            else:
                raise TypeError(path)
        recognized_directories = required_directories + optional_directories
        recognized_files = required_files + optional_files
        for required_directory in REQUIRED_DIRECTORIES:
            path = os.path.join(directory, required_directory)
            if path not in recognized_directories:
                missing_directories.append(path)
        for required_file in REQUIRED_FILES:
            path = os.path.join(directory, required_file)
            if path not in recognized_files:
                missing_files.append(path)
        messages = []
        if not problems_only:
            messages_ = self._format_ratio_check_messages(
                required_directories,
                REQUIRED_DIRECTORIES,
                'required directory',
                participal='found',
                )
            messages.extend(messages_)
        if missing_directories:
            messages_ = self._format_ratio_check_messages(
                missing_directories,
                REQUIRED_DIRECTORIES,
                'required directory',
                'missing',
                )
            messages.extend(messages_)
        if not problems_only:
            messages_ = self._format_ratio_check_messages(
                required_files,
                REQUIRED_FILES,
                'required file',
                'found',
                )
            messages.extend(messages_)
        if missing_files:
            messages_ = self._format_ratio_check_messages(
                missing_files,
                REQUIRED_FILES,
                'required file',
                'missing',
                )
            messages.extend(messages_)
        if not problems_only:
            messages_ = self._format_counted_check_messages(
                optional_directories,
                'optional directory',
                participal='found',
                )
            messages.extend(messages_)
            messages_ = self._format_counted_check_messages(
                optional_files,
                'optional file',
                participal='found',
                )
            messages.extend(messages_)
        messages_ = self._format_counted_check_messages(
            unrecognized_directories,
            'unrecognized directory',
            participal='found',
            )
        messages.extend(messages_)
        messages_ = self._format_counted_check_messages(
            unrecognized_files,
            'unrecognized file',
            participal='found',
            )
        messages.extend(messages_)
        messages = [self._tab + _ for _ in messages]
        name = self._path_to_asset_menu_display_string(
            directory,
            basic_breadcrumb,
            )
        found_problems = (
            missing_directories or
            missing_files or
            unrecognized_directories or
            unrecognized_files
            )
        count = len(names)
        wranglers = self._get_directory_wranglers(
            self._session,
            directory,
            )
        if wranglers or not return_messages:
            message = 'top level ({} assets):'.format(count)
            if not found_problems:
                message = '{} OK'.format(message)
            messages.insert(0, message)
            messages = [stringtools.capitalize_start(_) for _ in messages]
            messages = [self._tab + _ for _ in messages]
        message = '{}:'.format(name)
        if not wranglers and not found_problems and return_messages:
            message = '{} OK'.format(message)
        messages.insert(0, message)
        if wranglers:
            controller = self._io_manager._controller(
                controller=self,
                current_score_directory=directory,
                )
            silence = self._io_manager._silent()
            with controller, silence:
                for wrangler in wranglers:
                    self._io_manager._display(repr(wrangler))
                    if wrangler._asset_identifier == 'file':
                        directory_token = \
                            wrangler._get_current_directory_token(
                            wrangler._session,
                            wrangler._directory_name,
                            )
                        result = wrangler._check_every_file(
                            directory_token,
                            wrangler._directory_entry_predicate,
                            wrangler._hide_breadcrumb_while_in_score,
                            )
                    else:
                        result = wrangler.check_every_package(
                            indent=1,
                            problems_only=problems_only,
                            supply_missing=False,
                            )
                    messages_, missing_directories_, missing_files_ = result
                    missing_directories.extend(missing_directories_)
                    missing_files.extend(missing_files_)
                    messages_ = [
                        stringtools.capitalize_start(_) for _ in messages_]
                    messages_ = [self._tab + _ for _ in messages_]
                    messages.extend(messages_)
        if return_messages:
            return messages, missing_directories, missing_files
        else:
            self._io_manager._display(messages)
        if not missing_directories + missing_files:
            return messages, missing_directories, missing_files
        if supply_missing is None:
            directory_count = len(missing_directories)
            file_count = len(missing_files)
            directories = stringtools.pluralize('directory', directory_count)
            files = stringtools.pluralize('file', file_count)
            if missing_directories and missing_files:
                prompt = 'supply missing {} and {}?'.format(directories, files)
            elif missing_directories:
                prompt = 'supply missing {}?'.format(directories)
            elif missing_files:
                prompt = 'supply missing {}?'.format(files)
            else:
                raise ValueError
            result = self._io_manager._confirm(prompt)
            if self._io_manager._is_backtracking or result is None:
                return
            supply_missing = bool(result)
        if not supply_missing:
            return messages, missing_directories, missing_files
        messages = []
        messages.append('made:')
        for missing_directory in missing_directories:
            os.makedirs(missing_directory)
            gitignore_path = os.path.join(missing_directory, '.gitignore')
            with open(gitignore_path, 'w') as file_pointer:
                file_pointer.write('')
            message = self._tab + missing_directory
            messages.append(message)
            supplied_directories.append(missing_directory)
        for missing_file in missing_files:
            if missing_file.endswith('__init__.py'):
                if self._is_score_package_outer_path(directory):
                    lines = self._get_score_initializer_file_lines(
                        missing_file)
                else:
                    lines = [self._unicode_directive]
            elif missing_file.endswith('__metadata__.py'):
                lines = []
                lines.append(self._unicode_directive)
                lines.append('from abjad import *')
                lines.append('')
                lines.append('')
                line = 'metadata = datastructuretools.TypedOrderedDict()'
                lines.append(line)
            elif missing_file.endswith('__views__.py'):
                lines = []
                lines.append(self._unicode_directive)
                lines.append(self._abjad_import_statement)
                lines.append('from ide.tools import idetools')
                lines.append('')
                lines.append('')
                line = 'view_inventory = idetools.ViewInventory([])'
                lines.append(line)
            elif missing_file.endswith('definition.py'):
                source_path = os.path.join(
                    configuration.abjad_ide_boilerplate_directory,
                    'definition.py',
                    )
                with open(source_path, 'r') as file_pointer:
                    lines = file_pointer.readlines()
                lines = [_.strip() for _ in lines]
            else:
                message = 'do not know how to make stub for {}.'
                message = message.format(missing_file)
                raise ValueError(message)
            contents = '\n'.join(lines)
            with open(missing_file, 'w') as file_pointer:
                file_pointer.write(contents)
            message = self._tab + missing_file
            messages.append(message)
            supplied_files.append(missing_file)
        if return_supply_messages:
            return messages, supplied_directories, supplied_files
        else:
            self._io_manager._display(messages)
        return messages, supplied_directories, supplied_files