# -*- encoding: utf-8 -*-
import copy
import datetime
import glob
import os
import shutil
import subprocess
import time
import traceback
from abjad.tools import datastructuretools
from abjad.tools import developerscripttools
from abjad.tools import lilypondfiletools
from abjad.tools import sequencetools
from abjad.tools import stringtools
from abjad.tools import systemtools
from ide.idetools.AssetController import AssetController


class Wrangler(AssetController):
    r'''Wrangler.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_allow_depot',
        '_asset_identifier',
        '_basic_breadcrumb',
        '_extension',
        '_extra_commands',
        '_file_name_predicate',
        '_force_lowercase',
        '_in_score_commands',
        '_main_menu',
        '_mandatory_copy_target_storehouse',
        '_new_file_contents',
        '_only_example_scores_during_test',
        '_score_storehouse_path_infix_parts',
        '_sort_by_annotation',
        '_use_dash_case',
        )

    ### INITIALIZER ###

    def __init__(self, session=None):
        from ide import idetools
        assert session is not None
        superclass = super(Wrangler, self)
        superclass.__init__(session=session)
        self._allow_depot = True
        self._asset_identifier = None
        self._basic_breadcrumb = None
        self._extension = ''
        self._extra_commands = []
        self._file_name_predicate = None
        self._force_lowercase = True
        self._in_score_commands = []
        self._mandatory_copy_target_storehouse = None
        self._new_file_contents = ''
        self._score_storehouse_path_infix_parts = ()
        self._sort_by_annotation = True
        self._use_dash_case = False

    ### PRIVATE PROPERTIES ###

    @property
    def _breadcrumb(self):
        if self._session.is_in_score and not self._has_breadcrumb_in_score:
            return
        breadcrumb = self._basic_breadcrumb
        if not self._allow_depot:
            pass
        elif self._session.is_in_score:
            breadcrumb = '{} directory'.format(breadcrumb)
        else:
            breadcrumb = '{} depot'.format(breadcrumb)
        view_name = self._read_view_name()
        if not view_name:
            return breadcrumb
        view_inventory = self._read_view_inventory()
        if view_inventory is not None and view_name in view_inventory:
            breadcrumb = '{} [{}]'.format(breadcrumb, view_name)
        return breadcrumb

    @property
    def _command_to_method(self):
        superclass = super(Wrangler, self)
        result = superclass._command_to_method
        result = result.copy()
        result.update({
            'cp': self.copy,
            'new': self.make,
            'ren': self.rename,
            'rm': self.remove,
            #
            'ws': self.set_view,
            #
            '<': self.go_to_previous_package,
            '>': self.go_to_next_package,
            #
            'ck*': self.check_every_package,
            'dc*': self.check_every_definition_py,
            'de*': self.edit_every_definition_py,
            'di*': self.illustrate_every_definition_py,  
            'ii*': self.interpret_every_illustration_ly,
            'io*': self.open_every_illustration_pdf,
            'so*': self.open_every_score_pdf,
            })
        result.update(self._commands)
        return result

    @property
    def _current_package_manager(self):
        path = self._get_current_directory()
        if path is None:
            return
        return self._io_manager._make_package_manager(path)

    @property
    def _current_storehouse_path(self):
        if self._session.is_in_score:
            parts = []
            parts.append(self._session.current_score_directory)
            parts.extend(self._score_storehouse_path_infix_parts)
            return os.path.join(*parts)
        else:
            return self._configuration.user_score_packages_directory

    @property
    def _init_py_file_path(self):
        path = self._get_current_directory()
        if path:
            return os.path.join(path, '__init__.py')

    @property
    def _metadata_py_path(self):
        if self._session.is_in_score:
            manager = self._current_package_manager
        else:
            manager = self._views_package_manager
        return manager._metadata_py_path

    @property
    def _views_py_path(self):
        if self._session.is_in_score:
            directory = self._get_current_directory()
            return os.path.join(directory, '__views__.py')
        else:
            directory = self._configuration.wrangler_views_directory
            class_name = type(self).__name__
            file_name = '__{}_views__.py'.format(class_name)
            return os.path.join(directory, file_name)

    ### PRIVATE METHODS ###

    def _call_lilypond_on_file_ending_with(self, string):
        file_path = self._get_file_path_ending_with(string)
        if file_path:
            self._io_manager.run_lilypond(file_path)
        else:
            message = 'file ending in {!r} not found.'
            message = message.format(string)
            self._io_manager._display(message)

    def _clear_view(self):
        if self._session.is_in_score:
            manager = self._current_package_manager
            metadatum_name = 'view_name'
        else:
            manager = self._views_package_manager
            metadatum_name = '{}_view_name'.format(type(self).__name__)
        manager._add_metadatum(metadatum_name, None)

    def _collect_segment_files(self, file_name):
        segments_directory = self._session.current_segments_directory
        build_directory = self._session.current_build_directory
        directory_entries = sorted(os.listdir(segments_directory))
        source_file_paths, target_file_paths = [], []
        _, extension = os.path.splitext(file_name)
        for directory_entry in directory_entries:
            segment_directory = os.path.join(
                segments_directory,
                directory_entry,
                )
            if not os.path.isdir(segment_directory):
                continue
            source_file_path = os.path.join(
                segment_directory,
                file_name,
                )
            if not os.path.isfile(source_file_path):
                continue
            score_path = self._session.current_score_directory
            score_package = self._configuration.path_to_package(
                score_path)
            score_name = score_package.replace('_', '-')
            directory_entry = directory_entry.replace('_', '-')
            target_file_name = directory_entry + extension
            target_file_path = os.path.join(
                build_directory,
                target_file_name,
                )
            source_file_paths.append(source_file_path)
            target_file_paths.append(target_file_path)
        if source_file_paths:
            messages = []
            messages.append('will copy ...')
            pairs = zip(source_file_paths, target_file_paths)
            for source_file_path, target_file_path in pairs:
                message = ' FROM: {}'.format(source_file_path)
                messages.append(message)
                message = '   TO: {}'.format(target_file_path)
                messages.append(message)
            self._io_manager._display(messages)
            if not self._io_manager._confirm():
                return
            if self._session.is_backtracking:
                return
        if not os.path.exists(build_directory):
            os.mkdir(build_directory)
        pairs = zip(source_file_paths, target_file_paths)
        return pairs

    def _confirm_segment_names(self):
        wrangler = self._session._abjad_ide._segment_package_wrangler
        view_name = wrangler._read_view_name()
        view_inventory = wrangler._read_view_inventory()
        if not view_inventory or view_name not in view_inventory:
            view_name = None
        segment_paths = wrangler._list_visible_asset_paths()
        segment_paths = segment_paths or []
        segment_names = []
        for segment_path in segment_paths:
            segment_name = os.path.basename(segment_path)
            segment_names.append(segment_name)
        messages = []
        if view_name:
            message = 'the {!r} segment view is currently selected.'
            message = message.format(view_name)
            messages.append(message)
        if segment_names:
            message = 'will assemble segments in this order:'
            messages.append(message)
            for segment_name in segment_names:
                message = '    ' + segment_name
                messages.append(message)
        else:
            message = 'no segments found:'
            message += ' will generate source without segments.'
            messages.append(message)
        self._io_manager._display(messages)
        result = self._io_manager._confirm()
        if self._session.is_backtracking or not result:
            return False
        return segment_names

    def _copy_boilerplate(self, file_name, candidacy=True, replacements=None):
        replacements = replacements or {}
        manager = self._session.current_score_package_manager
        assert manager is not None
        width, height, unit = manager._parse_paper_dimensions()
        source_path = os.path.join(
            self._configuration.abjad_ide_directory,
            'boilerplate',
            file_name,
            )
        destination_path = os.path.join(
            manager._path,
            'build',
            file_name,
            )
        base_name, extension = os.path.splitext(file_name)
        candidate_name = base_name + '.candidate' + extension
        candidate_path = os.path.join(
            manager._path,
            'build',
            candidate_name,
            )
        messages = []
        with systemtools.FilesystemState(remove=[candidate_path]):
            shutil.copyfile(source_path, candidate_path)
            old = '{PAPER_SIZE}'
            new = '{{{}{}, {}{}}}'
            new = new.format(width, unit, height, unit)
            self._replace_in_file(candidate_path, old, new)
            for old in replacements:
                new = replacements[old]
                self._replace_in_file(candidate_path, old, new)
            if not os.path.exists(destination_path):
                shutil.copyfile(candidate_path, destination_path)
                message = 'wrote {}.'.format(destination_path)
                messages.append(message)
            elif not candidacy:
                message = 'overwrite {}?'
                message = message.format(destination_path)
                result = self._io_manager._confirm(message)
                if self._session.is_backtracking or not result:
                    return False
                shutil.copyfile(candidate_path, destination_path)
                message = 'overwrote {}.'.format(destination_path)
                messages.append(message)
            elif systemtools.TestManager.compare_files(
                candidate_path, 
                destination_path,
                ):
                messages_ = self._make_candidate_messages(
                    True, 
                    candidate_path, 
                    destination_path,
                    )
                messages.extend(messages_)
                message = 'preserved {}.'.format(destination_path)
                messages.append(message)
            else:
                shutil.copyfile(candidate_path, destination_path)
                message = 'overwrote {}.'.format(destination_path)
                messages.append(message)
            self._io_manager._display(messages)
            return True

    def _edit_file_ending_with(self, string):
        file_path = self._get_file_path_ending_with(string)
        if file_path:
            self._io_manager.edit(file_path)
        else:
            message = 'file ending in {!r} not found.'
            message = message.format(string)
            self._io_manager._display(message)

    def _extract_common_parent_directories(self, paths):
        parent_directories = []
        example_score_packages_directory = \
            self._configuration.example_score_packages_directory
        user_score_packages_directory = \
            self._configuration.user_score_packages_directory
        for path in paths:
            parent_directory = os.path.dirname(path)
            if parent_directory == user_score_packages_directory:
                parent_directories.append(path)
            elif parent_directory == example_score_packages_directory:
                parent_directories.append(path)
            elif parent_directory not in parent_directories:
                parent_directories.append(parent_directory)
        return parent_directories

    def _find_git_manager(self, inside_score=True, must_have_file=False):
        if self._basic_breadcrumb == 'scores':
            inside_score = False
        manager = self._find_up_to_date_manager(
            inside_score=inside_score,
            must_have_file=must_have_file,
            system=True,
            )
        return manager

    def _find_up_to_date_manager(
        self,
        inside_score=True,
        must_have_file=False,
        system=True,
        ):
        from ide import idetools
        example_score_packages = False
        user_score_packages = False
        if system and inside_score:
            example_score_packages = True
        elif not system and inside_score:
            user_score_packages = True
        else:
            Exception
        asset_paths = self._list_asset_paths(
            example_score_packages=example_score_packages,
            user_score_packages=user_score_packages,
            )
        if self._basic_breadcrumb == 'scores':
            if system:
                scores_directory = \
                    self._configuration.example_score_packages_directory
            else:
                scores_directory = \
                    self._configuration.user_score_packages_directory
            asset_paths = []
            for directory_entry in sorted(os.listdir(scores_directory)):
                if not directory_entry[0].isalpha():
                    continue
                path = os.path.join(scores_directory, directory_entry)
                if os.path.isdir(path):
                    asset_paths.append(path)
        session = idetools.Session()
        for asset_path in asset_paths:
            manager = self._get_manager(asset_path)
            if (manager._is_git_versioned() and
                manager._is_up_to_date() and
                (not must_have_file or manager._find_first_file_name())):
                return manager

    def _get_available_path(
        self,
        message=None,
        storehouse_path=None,
        ):
        storehouse_path = storehouse_path or self._current_storehouse_path
        while True:
            default_prompt = 'enter {} name'.format(self._asset_identifier)
            message = message or default_prompt
            getter = self._io_manager._make_getter()
            getter.append_string(message)
            name = getter._run()
            if self._session.is_backtracking or not name:
                return
            name = stringtools.strip_diacritics(name)
            words = stringtools.delimit_words(name)
            words = [_.lower() for _ in words]
            name = '_'.join(words)
            if not stringtools.is_snake_case_package_name(name):
                continue
            path = os.path.join(storehouse_path, name)
            if os.path.exists(path):
                line = 'path already exists: {!r}.'
                line = line.format(path)
                self._io_manager._display(line)
            else:
                return path

    def _get_file_path_ending_with(self, string):
        path = self._get_current_directory()
        for file_name in self._list():
            if file_name.endswith(string):
                file_path = os.path.join(path, file_name)
                return file_path

    def _get_manager(self, path):
        from ide import idetools
        assert os.path.sep in path, repr(path)
        manager = idetools.PackageManager(
            path=path,
            session=self._session,
            )
        if self._asset_identifier == 'material package':
            manager._configure_as_material_package_manager()
        elif self._asset_identifier == 'score package':
            manager._configure_as_score_package_manager()
        elif self._asset_identifier == 'segment package':
            manager._configure_as_segment_package_manager()
        return manager

    def _get_next_asset_path(self):
        last_path = self._session.last_asset_path
        menu_entries = self._make_asset_menu_entries()
        paths = [x[-1] for x in menu_entries]
        if self._session.is_in_score:
            score_directory = self._session.current_score_directory
            paths = [x for x in paths if x.startswith(score_directory)]
        if last_path is None:
            return paths[0]
        if last_path not in paths:
            return paths[0]
        index = paths.index(last_path)
        next_index = (index + 1) % len(paths)
        next_path = paths[next_index]
        return next_path

    def _get_previous_asset_path(self):
        last_path = self._session.last_asset_path
        menu_entries = self._make_asset_menu_entries()
        paths = [x[-1] for x in menu_entries]
        if self._session.is_in_score:
            score_directory = self._session.current_score_directory
            paths = [x for x in paths if x.startswith(score_directory)]
        if last_path is None:
            return paths[-1]
        if last_path not in paths:
            return paths[-1]
        index = paths.index(last_path)
        previous_index = (index - 1) % len(paths)
        previous_path = paths[previous_index]
        return previous_path

    def _get_sibling_asset_path(self):
        if self._session.is_navigating_to_next_asset:
            return self._get_next_asset_path()
        if self._session.is_navigating_to_previous_asset:
            return self._get_previous_asset_path()

    def _get_visible_storehouses(self):
        menu = self._make_asset_selection_menu()
        asset_section = menu['assets']
        storehouses = set()
        for menu_entry in asset_section:
            path = menu_entry.return_value
            storehouse = self._configuration._path_to_storehouse(path)
            storehouses.add(storehouse)
        storehouses = list(sorted(storehouses))
        return storehouses

    def _interpret_file_ending_with(self, string):
        r'''Typesets TeX file.
        Calls ``pdflatex`` on file TWICE.
        Some LaTeX packages like ``tikz`` require two passes.
        '''
        file_path = self._get_file_path_ending_with(string)
        if not file_path:
            message = 'file ending in {!r} not found.'
            message = message.format(string)
            self._io_manager._display(message)
            return
        input_directory = os.path.dirname(file_path)
        output_directory = input_directory
        basename = os.path.basename(file_path)
        input_file_name_stem, extension = os.path.splitext(basename)
        job_name = '{}.candidate'.format(input_file_name_stem)
        candidate_name = '{}.candidate.pdf'.format(input_file_name_stem)
        candidate_path = os.path.join(output_directory, candidate_name)
        destination_name = '{}.pdf'.format(input_file_name_stem)
        destination_path = os.path.join(output_directory, destination_name)
        command = 'pdflatex --jobname={} -output-directory={} {}/{}.tex'
        command = command.format(
            job_name,
            output_directory,
            input_directory,
            input_file_name_stem,
            )
        command_called_twice = '{}; {}'.format(command, command)
        filesystem = systemtools.FilesystemState(remove=[candidate_path])
        directory = systemtools.TemporaryDirectoryChange(input_directory)
        with filesystem, directory:
            self._io_manager.spawn_subprocess(command_called_twice)
            for file_name in glob.glob('*.aux'):
                path = os.path.join(output_directory, file_name)
                os.remove(path)
            for file_name in glob.glob('*.aux'):
                path = os.path.join(output_directory, file_name)
                os.remove(path)
            for file_name in glob.glob('*.log'):
                path = os.path.join(output_directory, file_name)
                os.remove(path)
            self._handle_candidate(candidate_path, destination_path)

    def _is_valid_file_directory_entry(self, expr):
        superclass = super(Wrangler, self)
        if superclass._is_valid_directory_entry(expr):
            name, extension = os.path.splitext(expr)
            if self._file_name_predicate(name):
                if self._extension == '':
                    return True
                elif self._extension == extension:
                    return True
        return False

    def _is_valid_package_directory_entry(self, expr):
        superclass = super(Wrangler, self)
        if superclass._is_valid_directory_entry(expr):
            if '.' not in expr:
                return True
        return False

    def _list(self, public_entries_only=False):
        result = []
        path = self._get_current_directory()
        result = self._io_manager._list_directory(
            path, 
            public_entries_only=public_entries_only,
            )
        return result

    def _list_all_directories_with_metadata_pys(self):
        directories = []
        paths = self._list_visible_asset_paths()
        for path in paths:
            result = self._list_directories_with_metadata_pys(path)
            directories.extend(result)
        return directories

    def _list_storehouse_paths(
        self,
        example_score_packages=True,
        user_score_packages=True,
        ):
        result = []
        if user_score_packages:
            result.append(self._configuration.user_score_packages_directory)
        if (example_score_packages and
            self._score_storehouse_path_infix_parts):
            for score_directory in \
                self._configuration.list_score_directories(abjad=True):
                score_directory = self._configuration._path_to_score_path(
                    score_directory)
                parts = [score_directory]
                if self._score_storehouse_path_infix_parts:
                    parts.extend(self._score_storehouse_path_infix_parts)
                storehouse_path = os.path.join(*parts)
                result.append(storehouse_path)
        elif (example_score_packages and
            not self._score_storehouse_path_infix_parts):
            result.append(self._configuration.example_score_packages_directory)
        if user_score_packages and self._score_storehouse_path_infix_parts:
            for directory in \
                self._configuration.list_score_directories(user=True):
                parts = [directory]
                if self._score_storehouse_path_infix_parts:
                    parts.extend(self._score_storehouse_path_infix_parts)
                path = os.path.join(*parts)
                result.append(path)
        return result

    def _list_visible_asset_managers(self):
        paths = self._list_visible_asset_paths()
        managers = []
        for path in paths:
            manager = self._get_manager(path)
            managers.append(manager)
        return managers

    def _list_visible_asset_paths(self):
        entries = self._make_asset_menu_entries()
        paths = [_[-1] for _ in entries]
        return paths

    def _make_asset(self, asset_name):
        if os.path.sep in asset_name:
            asset_name = os.path.basename(asset_name)
        assert stringtools.is_snake_case(asset_name)
        path = os.path.join(
            self._current_storehouse_path,
            asset_name,
            )
        manager = self._get_manager(path)
        if hasattr(manager, '_write_stub'):
            self._io_manager.write_stub(path)
        else:
            with self._io_manager._silent():
                manager.check_package(
                    return_supply_messages=True,
                    supply_missing=True,
                    )
        paths = self._list_visible_asset_paths()
        if path not in paths:
            with self._io_manager._silent():
                self._clear_view()
        self._session._pending_redraw = True

    def _make_asset_selection_breadcrumb(
        self,
        infinitival_phrase=None,
        is_storehouse=False,
        ):
        name = self._asset_identifier
        name = stringtools.to_space_delimited_lowercase(name)
        if infinitival_phrase:
            return 'select {} {}:'.format(
                name,
                infinitival_phrase,
                )
        elif is_storehouse:
            return 'select storehouse'
        else:
            return 'select {}:'.format(name)

    def _make_asset_selection_menu(self):
        menu = self._io_manager._make_menu(name='asset selection')
        menu_entries = self._make_asset_menu_entries()
        menu.make_asset_section(menu_entries=menu_entries)
        return menu

    def _make_basic_operations_menu_section(self, menu):
        commands = []
        commands.append(('copy', 'cp'))
        commands.append(('new', 'new'))
        commands.append(('rename', 'ren'))
        commands.append(('remove', 'rm'))
        menu.make_command_section(
            commands=commands,
            name='basic operations',
            )

    def _make_extra_commands_menu_section(self, menu):
        commands = []
        commands.extend(self._extra_commands)
        if commands:
            menu.make_command_section(
                is_hidden=True,
                commands=commands,
                name='extra commands',
                )

    def _make_file(
        self, 
        extension=None, 
        message='file name', 
        ):
        contents = self._new_file_contents
        extension = extension or getattr(self, '_extension', '')
        if self._session.is_in_score:
            path = self._get_current_directory()
        else:
            path = self._select_storehouse_path()
            if self._session.is_backtracking or path is None:
                return
        getter = self._io_manager._make_getter()
        getter.append_string(message)
        name = getter._run()
        if self._session.is_backtracking or name is None:
            return
        name = stringtools.strip_diacritics(name)
        if self._use_dash_case:
            name = self._to_dash_case(name)
        name = name.replace(' ', '_')
        if self._force_lowercase:
            name = name.lower()
        if not name.endswith(extension):
            name = name + extension
        path = os.path.join(path, name)
        self._io_manager.write(path, contents)
        self._io_manager.edit(path)

    def _make_in_score_commands_menu_section(self, menu):
        commands = []
        commands.extend(self._in_score_commands)
        if commands:
            menu.make_command_section(
                commands=self._in_score_commands,
                is_hidden=True,
                name='in score commands',
                )

    def _make_main_menu(self):
        superclass = super(Wrangler, self)
        menu = superclass._make_main_menu()
        self._make_asset_menu_section(menu)
        self._make_basic_operations_menu_section(menu)
        self._make_extra_commands_menu_section(menu)
        self._make_in_score_commands_menu_section(menu)
        self._make_views_menu_section(menu)
        return menu

    def _make_package(self):
        if self._session.is_in_score:
            storehouse_path = self._current_storehouse_path
        else:
            example_score_packages = self._session.is_test
            storehouse_path = self._select_storehouse_path(
                example_score_packages=example_score_packages,
                )
            if self._session.is_backtracking or storehouse_path is None:
                return
        path = self._get_available_path(storehouse_path=storehouse_path)
        if self._session.is_backtracking or not path:
            return
        message = 'path will be {}.'.format(path)
        self._io_manager._display(message)
        result = self._io_manager._confirm()
        if self._session.is_backtracking or not result:
            return
        manager = self._get_manager(path)
        manager._make_package()
        paths = self._list_visible_asset_paths()
        if path not in paths:
            with self._io_manager._silent():
                self._clear_view()
        manager._run()

    def _make_storehouse_menu_entries(
        self,
        example_score_packages=True,
        user_score_packages=True,
        ):
        from ide import idetools
        display_strings, keys = [], []
        wrangler = self._session._abjad_ide._score_package_wrangler
        paths = wrangler._list_asset_paths(
            example_score_packages=example_score_packages,
            user_score_packages=user_score_packages,
            )
        for path in paths:
            manager = wrangler._get_manager(path)
            display_strings.append(manager._get_title(year=False))
            path_parts = (manager._path,)
            path_parts = path_parts + self._score_storehouse_path_infix_parts
            key = os.path.join(*path_parts)
            keys.append(key)
        assert len(display_strings) == len(keys), repr((display_strings, keys))
        sequences = [display_strings, [None], [None], keys]
        return sequencetools.zip_sequences(sequences, cyclic=True)

    def _make_views_menu_section(self, menu):
        commands = []
        commands.append(('set view', 'ws'))
        menu.make_command_section(
            is_hidden=True,
            commands=commands,
            name='views',
            )

    def _match_display_string_view_pattern(self, pattern, entry):
        display_string, _, _, path = entry
        token = ':ds:'
        assert token in pattern, repr(pattern)
        pattern = pattern.replace(token, repr(display_string))
        try:
            result = eval(pattern)
        except:
            traceback.print_exc()
            return False
        return result

    def _match_metadata_view_pattern(self, pattern, entry):
        display_string, _, _, path = entry
        manager = self._io_manager._make_package_manager(path)
        count = pattern.count('md:')
        for _ in range(count+1):
            parts = pattern.split()
            for part in parts:
                if part.startswith('md:'):
                    metadatum_name = part[3:]
                    metadatum = manager._get_metadatum(
                        metadatum_name,
                        include_score=True,
                        )
                    metadatum = repr(metadatum)
                    pattern = pattern.replace(part, metadatum)
        try:
            result = eval(pattern)
        except:
            traceback.print_exc()
            return False
        return result

    def _match_path_view_pattern(self, pattern, entry):
        display_string, _, _, path = entry
        token = ':path:'
        assert token in pattern, repr(pattern)
        pattern = pattern.replace(token, repr(path))
        try:
            result = eval(pattern)
        except:
            traceback.print_exc()
            return False
        return result

    def _open_file_ending_with(self, string):
        path = self._get_file_path_ending_with(string)
        if path:
            self._io_manager.open_file(path)
        else:
            message = 'file ending in {!r} not found.'
            message = message.format(string)
            self._io_manager._display(message)

    def _open_in_every_package(self, file_name, verb='open'):
        paths = []
        for path in self._list_visible_asset_paths():
            path = os.path.join(path, file_name)
            if os.path.isfile(path):
                paths.append(path)
        if not paths:
            message = 'no {} files found.'
            message = message.format(file_name)
            self._io_manager._display(message)
            return
        messages = []
        message = 'will {} ...'.format(verb)
        messages.append(message)
        for path in paths:
            message = '   ' + path
            messages.append(message)
        self._io_manager._display(messages)
        result = self._io_manager._confirm()
        if self._session.is_backtracking or not result:
            return
        self._io_manager.open_file(paths)

    def _run(self):
        controller = self._io_manager._controller(
            consume_local_backtrack=True,
            controller=self,
            on_enter_callbacks=(self._enter_run,),
            )
        directory = systemtools.NullContextManager()
        if self._session.is_in_score:
            path = self._get_current_directory()
            directory = systemtools.TemporaryDirectoryChange(path)
        with controller, directory:
            result = None
            self._session._pending_redraw = True
            while True:
                result = self._get_sibling_asset_path()
                if not result:
                    menu = self._make_main_menu()
                    result = menu._run()
                if self._session.is_backtracking:
                    return
                if result:
                    self._handle_input(result)
                    if self._session.is_backtracking:
                        return

    def _select_asset_path(self):
        menu = self._make_asset_selection_menu()
        while True:
            result = menu._run()
            if self._session.is_backtracking:
                return
            elif not result:
                continue
            elif result == '<return>':
                return
            else:
                break
        return result

    def _select_storehouse_path(
        self,
        example_score_packages=False,
        ):
        from ide import idetools
        menu_entries = self._make_storehouse_menu_entries(
            example_score_packages=example_score_packages,
            user_score_packages=False,
            )
        selector = idetools.Selector(
            breadcrumb='storehouse',
            menu_entries=menu_entries,
            session=self._session,
            )
        result = selector._run()
        if self._session.is_backtracking or result is None:
            return
        return result

    def _select_view(self, infinitive_phrase=None, is_ranged=False):
        from ide import idetools
        view_inventory = self._read_view_inventory()
        if view_inventory is None:
            message = 'no views found.'
            self._io_manager._display(message)
            return
        view_names = list(view_inventory.keys())
        view_names.append('none')
        if is_ranged:
            breadcrumb = 'view(s)'
        else:
            breadcrumb = 'view'
        if infinitive_phrase:
            breadcrumb = '{} {}'.format(breadcrumb, infinitive_phrase)
        selector = self._io_manager._make_selector(
            breadcrumb=breadcrumb,
            is_ranged=is_ranged,
            items=view_names,
            )
        result = selector._run()
        if self._session.is_backtracking or result is None:
            return
        return result

    def _select_visible_asset_path(self, infinitive_phrase=None):
        getter = self._io_manager._make_getter()
        message = 'enter {}'.format(self._asset_identifier)
        if infinitive_phrase:
            message = message + ' ' + infinitive_phrase
        if hasattr(self, '_make_asset_menu_section'):
            dummy_menu = self._io_manager._make_menu()
            self._make_asset_menu_section(dummy_menu)
            asset_section = dummy_menu._asset_section
        else:
            menu = self._make_asset_selection_menu()
            asset_section = menu['assets']
        getter.append_menu_section_item(
            message, 
            asset_section,
            )
        numbers = getter._run()
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
        plural_identifier = stringtools.pluralize(self._asset_identifier)
        message = 'enter {}(s) to remove'
        message = message.format(plural_identifier)
        menu = self._make_asset_selection_menu()
        asset_section = menu['assets']
        getter.append_menu_section_range(
            message, 
            asset_section,
            )
        numbers = getter._run()
        if self._session.is_backtracking or numbers is None:
            return
        indices = [_ - 1 for _ in numbers]
        paths = [_.return_value for _ in asset_section.menu_entries]
        paths = sequencetools.retain_elements(paths, indices)
        return paths

    @staticmethod
    def _strip_annotation(display_string):
        if not display_string.endswith(')'):
            return display_string
        index = display_string.find('(')
        result = display_string[:index]
        result = result.strip()
        return result

    @staticmethod
    def _to_dash_case(file_name):
        file_name = file_name.replace(' ', '-')
        file_name = file_name.replace('_', '-')
        return file_name

    @staticmethod
    def _trim_lilypond_file(file_path):
        lines = []
        with open(file_path, 'r') as file_pointer:
            found_score_block = False
            for line in file_pointer.readlines():
                if line.startswith(r'\score'):
                    found_score_block = True
                    continue
                if line.startswith('}'):
                    found_score_block = False
                    lines.append('\n')
                    continue
                if found_score_block:
                    lines.append(line)
        if lines and lines[-1] == '\n':
            lines.pop()
        lines = ''.join(lines)
        with open(file_path, 'w') as file_pointer:
            file_pointer.write(lines)

    def _update_order_dependent_segment_metadata(self):
        managers = self._list_visible_asset_managers()
        if not managers:
            return
        segment_count = len(managers)
        # update segment numbers and segment count
        for segment_index, manager in enumerate(managers):
            segment_number = segment_index + 1
            manager._add_metadatum('segment_number', segment_number)
            manager._add_metadatum('segment_count', segment_count)
        # update first bar numbers and measure counts
        manager = managers[0]
        first_bar_number = 1
        manager._add_metadatum('first_bar_number', first_bar_number)
        measure_count = manager._get_metadatum('measure_count')
        if not measure_count:
            return
        next_bar_number = first_bar_number + measure_count
        for manager in managers[1:]:
            first_bar_number = next_bar_number
            manager._add_metadatum('first_bar_number', next_bar_number)
            measure_count = manager._get_metadatum('measure_count')
            if not measure_count:
                return
            next_bar_number = first_bar_number + measure_count
            
    def _write_view_inventory(self, view_inventory):
        lines = []
        lines.append(self._configuration.unicode_directive)
        lines.append(self._abjad_import_statement)
        lines.append('from ide import idetools')
        lines.append('')
        lines.append('')
        view_inventory = self._sort_ordered_dictionary(view_inventory)
        line = 'view_inventory={}'.format(format(view_inventory))
        lines.append(line)
        contents = '\n'.join(lines)
        self._io_manager.write(self._views_py_path, contents)
        message = 'view inventory written to disk.'
        self._io_manager._display(message)

    ### PUBLIC METHODS ###

    def add_every_asset(self):
        r'''Adds every asset to repository.

        Returns none.
        '''
        self._session._attempted_to_add = True
        if self._session.is_repository_test:
            return
        managers = self._list_visible_asset_managers()
        inputs, outputs = [], []
        method_name = 'add'
        for manager in managers:
            method = getattr(manager, method_name)
            inputs_, outputs_ = method(dry_run=True)
            inputs.extend(inputs_)
            outputs.extend(outputs_)
        messages = self._format_messaging(inputs, outputs, verb='add')
        self._io_manager._display(messages)
        if not inputs:
            return
        result = self._io_manager._confirm()
        if self._session.is_backtracking or not result:
            return
        with self._io_manager._silent():
            for manager in managers:
                method = getattr(manager, method_name)
                method()
        count = len(inputs)
        identifier = stringtools.pluralize('file', count)
        message = 'added {} {} to repository.'
        message = message.format(count, identifier)
        self._io_manager._display(message)
        
    def check_every_definition_py(self):
        r'''Checks ``definition.py`` in every package.

        Returns none.
        '''
        managers = self._list_visible_asset_managers()
        inputs, outputs = [], []
        method_name = 'check_definition_py'
        for manager in managers:
            method = getattr(manager, method_name)
            inputs_, outputs_ = method(dry_run=True)
            inputs.extend(inputs_)
            outputs.extend(outputs_)
        messages = self._format_messaging(inputs, outputs, verb='check')
        self._io_manager._display(messages)
        result = self._io_manager._confirm()
        if self._session.is_backtracking or not result:
            return
        start_time = time.time()
        for manager in managers:
            method = getattr(manager, method_name)
            method()
        stop_time = time.time()
        total_time = stop_time - start_time
        total_time = int(total_time)
        message = 'total time: {} seconds.'
        message = message.format(total_time)
        self._io_manager._display(message)

    def check_every_file(self):
        r'''Checks every file.

        Returns none.
        '''
        paths = self._list_asset_paths(valid_only=False)
        paths = [_ for _ in paths if os.path.basename(_)[0].isalpha()]
        paths = [_ for _ in paths if not _.endswith('.pyc')]
        current_directory = self._get_current_directory()
        if current_directory:
            paths = [_ for _ in paths if _.startswith(current_directory)]
        invalid_paths = []
        for path in paths:
            file_name = os.path.basename(path)
            if not self._is_valid_directory_entry(file_name):
                invalid_paths.append(path)
        messages = []
        if not invalid_paths:
            count = len(paths)
            message = '{} ({} files): OK'.format(self._breadcrumb, count)
            messages.append(message)
        else:
            message = '{}:'.format(self._breadcrumb)
            messages.append(message)
            identifier = 'file'
            count = len(invalid_paths)
            identifier = stringtools.pluralize(identifier, count)
            message = '{} unrecognized {} found:'
            message = message.format(count, identifier)
            tab = self._io_manager._tab
            message = tab + message
            messages.append(message)
            for invalid_path in invalid_paths:
                message = tab + tab + invalid_path
                messages.append(message)
        self._io_manager._display(messages)
        missing_files, missing_directories = [], []
        return messages, missing_files, missing_directories

    def check_every_package(
        self, 
        indent=0,
        problems_only=None, 
        supply_missing=None,
        ):
        r'''Checks every package.

        Returns none.
        '''
        messages = []
        missing_directories, missing_files = [], []
        supplied_directories, supplied_files = [], []
        tab = indent * self._io_manager._tab
        if problems_only is None:
            prompt = 'show problem assets only?'
            result = self._io_manager._confirm(prompt)
            if self._session.is_backtracking or result is None:
                return messages, missing_directories, missing_files
            problems_only = bool(result)
        managers = self._list_visible_asset_managers()
        found_problem = False
        for manager in managers:
            with self._io_manager._silent():
                result = manager.check_package(
                    return_messages=True,
                    problems_only=problems_only,
                    )
            messages_, missing_directories_, missing_files_ = result
            missing_directories.extend(missing_directories_)
            missing_files.extend(missing_files_)
            messages_ = [stringtools.capitalize_start(_) for _ in messages_]
            messages_ = [tab + _ for _ in messages_]
            if messages_:
                found_problem = True
                messages.extend(messages_)
            else:
                message = 'No problem assets found.'
                message = tab + tab + message
                messages.append(message)
        found_problems = bool(messages)
        if self._session.is_in_score:
            path = self._get_current_directory()
            name = os.path.basename(path)
            count = len(managers)
            message = '{} directory ({} packages):'.format(name, count)
            if not found_problems:
                message = '{} OK'.format(message)
            messages.insert(0, message)
        self._io_manager._display(messages)
        if not found_problem:
            return messages, missing_directories, missing_files
        if supply_missing is None:
            prompt = 'supply missing directories and files?'
            result = self._io_manager._confirm(prompt)
            if self._session.is_backtracking or result is None:
                return messages, missing_directories, missing_files
            supply_missing = bool(result)
        if not supply_missing:
            return messages, missing_directories, missing_files
        messages = []
        for manager in managers:
            with self._io_manager._silent():
                result = manager.check_package(
                    return_supply_messages=True,
                    supply_missing=True,
                    )
            messages_, supplied_directories_, supplied_files_ = result
            supplied_directories.extend(supplied_directories_)
            supplied_files.extend(supplied_files_)
            if messages_:
                messages_ = [tab + tab + _ for _ in messages_]
                messages.extend(messages_)
        self._io_manager._display(messages)
        return messages, supplied_directories, supplied_files

    def collect_segment_lilypond_files(self):
        r'''Copies ``illustration.ly`` files from segment packages to build 
        directory.

        Trims top-level comments, includes and directives from each
        ``illustration.ly`` file.

        Trims header and paper block from each ``illustration.ly`` file.

        Leaves score block in each ``illustration.ly`` file.

        Returns none.
        '''
        pairs = self._collect_segment_files('illustration.ly')
        if not pairs:
            return
        for source_file_path, target_file_path in pairs:
            candidate_file_path = target_file_path.replace(
                '.ly',
                '.candidate.ly',
                )
            with systemtools.FilesystemState(remove=[candidate_file_path]):
                shutil.copyfile(source_file_path, candidate_file_path)
                self._trim_lilypond_file(candidate_file_path)
                self._handle_candidate(candidate_file_path, target_file_path)
                self._io_manager._display('')

    def collect_segment_pdfs(self):
        r'''Copies ``illustration.pdf`` files from segment packages to build 
        directory.

        Returns none.
        '''
        pairs = self._collect_segment_files('illustration.pdf')
        if not pairs:
            return
        for source_file_path, target_file_path in pairs:
            self._handle_candidate(source_file_path, target_file_path)
            self._io_manager._display('')

    def commit_every_asset(self):
        r'''Commits every asset to repository.

        Returns none.
        '''
        self._session._attempted_to_commit = True
        if self._session.is_repository_test:
            return
        getter = self._io_manager._make_getter()
        getter.append_string('commit message')
        commit_message = getter._run()
        if self._session.is_backtracking or commit_message is None:
            return
        line = 'commit message will be: "{}"'.format(commit_message)
        self._io_manager._display(line)
        result = self._io_manager._confirm()
        if self._session.is_backtracking or not result:
            return
        paths = self._list_visible_asset_paths()
        for path in paths:
            manager = self._get_manager(path)
            with self._io_manager._silent():
                manager.commit(commit_message=commit_message)

    def copy(
        self, 
        extension=None,
        new_storehouse=None
        ):
        r'''Copies asset.

        Returns none.
        '''
        visible_asset_paths = self._list_visible_asset_paths()
        if not visible_asset_paths:
            messages = ['nothing to copy.']
            messages.append('')
            self._io_manager._display(messages)
            return
        extension = extension or getattr(self, '_extension', '')
        old_path = self._select_visible_asset_path(infinitive_phrase='to copy')
        if not old_path:
            return
        old_name = os.path.basename(old_path)
        new_storehouse = self._mandatory_copy_target_storehouse
        if new_storehouse:
            pass
        elif self._session.is_in_score:
            new_storehouse = self._get_current_directory()
        else:
            new_storehouse = self._select_storehouse_path()
            if self._session.is_backtracking or new_storehouse is None:
                return
        message = 'existing {} name> {}'
        message = message.format(self._asset_identifier, old_name)
        self._io_manager._display(message)
        message = 'new {} name'
        message = message.format(self._asset_identifier)
        getter = self._io_manager._make_getter()
        getter.append_string(message)
        help_template = getter.prompts[0].help_template
        string = 'Press <return> to preserve existing name.'
        help_template = help_template + ' ' + string
        getter.prompts[0]._help_template = help_template
        new_name = getter._run()
        new_name = new_name or old_name
        if self._session.is_backtracking or new_name is None:
            return
        new_name = stringtools.strip_diacritics(new_name)
        if self._use_dash_case:
            new_name = self._to_dash_case(new_name)
        new_name = new_name.replace(' ', '_')
        if self._force_lowercase:
            new_name = new_name.lower()
        if extension and not new_name.endswith(extension):
            new_name = new_name + extension
        new_path = os.path.join(new_storehouse, new_name)
        if os.path.exists(new_path):
            message = 'already exists: {}'.format(new_path)
            self._io_manager._display(message)
            self._io_manager._acknowledge()
            return
        messages = []
        messages.append('will copy ...')
        messages.append(' FROM: {}'.format(old_path))
        messages.append('   TO: {}'.format(new_path))
        self._io_manager._display(messages)
        result = self._io_manager._confirm()
        if self._session.is_backtracking or not result:
            return
        if os.path.isfile(old_path):
            shutil.copyfile(old_path, new_path)
        elif os.path.isdir(old_path):
            shutil.copytree(old_path, new_path)
        else:
            raise TypeError(old_path)
        if os.path.isdir(new_path):
            for directory_entry in sorted(os.listdir(new_path)):
                if not directory_entry.endswith('.py'):
                    continue
                path = os.path.join(new_path, directory_entry)
                self._replace_in_file(
                    path,
                    old_name,
                    new_name,
                    )

    def display_every_asset_status(self):
        r'''Displays repository status of every asset.

        Returns none.
        '''
        self._session._attempted_display_status = True
        paths = self._list_visible_asset_paths()
        paths = self._extract_common_parent_directories(paths)
        paths.sort()
        for path in paths:
            manager = self._io_manager._make_package_manager(path)
            manager.display_status()
        if not paths:
            message = 'Repository status for {} ... OK'
            directory = self._get_current_directory()
            message = message.format(directory)
            self._io_manager._display(message)

    def edit_every_definition_py(self):
        r'''Opens ``definition.py`` in every package.

        Returns none.
        '''
        self._open_in_every_package('definition.py')

    def generate_back_cover_source(self):
        r'''Generates ``back-cover.tex``.

        Returns none.
        '''
        replacements = {}
        manager = self._session.current_score_package_manager
        catalog_number = manager._get_metadatum('catalog_number')
        if catalog_number:
            old = 'CATALOG NUMBER'
            new = str(catalog_number)
            replacements[old] = new
        composer_website = self._configuration.composer_website
        if self._session.is_test:
            composer_website = 'www.composer-website.com'
        if composer_website:
            old = 'COMPOSER WEBSITE'
            new = str(composer_website)
            replacements[old] = new
        price = manager._get_metadatum('price')
        if price:
            old = 'PRICE'
            new = str(price)
            replacements[old] = new
        self._copy_boilerplate('back-cover.tex', replacements=replacements)

    def generate_front_cover_source(self):
        r'''Generates ``front-cover.tex``.

        Returns none.
        '''
        file_name = 'front-cover.tex'
        replacements = {}
        manager = self._session.current_score_package_manager
        score_title = manager._get_title(year=False)
        if score_title:
            old = 'TITLE'
            new = str(score_title.upper())
            replacements[old] = new
        forces_tagline = manager._get_metadatum('forces_tagline')
        if forces_tagline:
            old = 'FOR INSTRUMENTS'
            new = str(forces_tagline)
            replacements[old] = new
        year = manager._get_metadatum('year')
        if year:
            old = 'YEAR'
            new = str(year)
            replacements[old] = new
        composer = self._configuration.upper_case_composer_full_name
        if self._session.is_test:
            composer = 'EXAMPLE COMPOSER NAME'
        if composer:
            old = 'COMPOSER'
            new = str(composer)
            replacements[old] = new
        self._copy_boilerplate(file_name, replacements=replacements)

    def generate_interpret_open_front_cover(self):
        r'''Generates ``front-cover.tex``.

        Then interprets ``front-cover.tex``.

        Then opens ``front-cover.pdf``.

        Returns none.
        '''
        self.generate_front_cover_source()
        self.interpret_front_cover()
        self.open_front_cover_pdf()
        
    def generate_music_source(self):
        r'''Generates ``music.ly``.

        Returns none.
        '''
        result = self._confirm_segment_names()
        if self._session.is_backtracking or not isinstance(result, list):
            return
        segment_names = result
        lilypond_names = [_.replace('_', '-') for _ in segment_names]
        source_path = os.path.join(
            self._configuration.abjad_ide_directory,
            'boilerplate',
            'music.ly',
            )
        manager = self._session.current_score_package_manager
        destination_path = os.path.join(
            manager._path,
            'build',
            'music.ly',
            )
        candidate_path = os.path.join(
            manager._path,
            'build',
            'music.candidate.ly',
            )
        with systemtools.FilesystemState(remove=[candidate_path]):
            shutil.copyfile(source_path, candidate_path)
            width, height, unit = manager._parse_paper_dimensions()
            old = '{PAPER_SIZE}'
            new = '{{{}{}, {}{}}}'
            new = new.format(width, unit, height, unit)
            self._replace_in_file(candidate_path, old, new)
            lines = []
            for lilypond_name in lilypond_names:
                file_name = lilypond_name + '.ly'
                tab = 4 * ' '
                line = tab + r'\include "{}"'
                line = line.format(file_name)
                lines.append(line)
            if lines:
                new = '\n'.join(lines)
                old = '%%% SEGMENTS %%%'
                self._replace_in_file(candidate_path, old, new)
            else:
                line_to_remove = '%%% SEGMENTS %%%\n'
                self._remove_file_line(candidate_path, line_to_remove)
            stylesheet_path = self._session.current_stylesheet_path
            if stylesheet_path:
                old = '% STYLESHEET_INCLUDE_STATEMENT'
                new = r'\include "../stylesheets/stylesheet.ily"'
                self._replace_in_file(candidate_path, old, new)
            language_token = lilypondfiletools.LilyPondLanguageToken()
            lilypond_language_directive = format(language_token)
            old = '% LILYPOND_LANGUAGE_DIRECTIVE'
            new = lilypond_language_directive
            self._replace_in_file(candidate_path, old, new)
            version_token = lilypondfiletools.LilyPondVersionToken()
            lilypond_version_directive = format(version_token)
            old = '% LILYPOND_VERSION_DIRECTIVE'
            new = lilypond_version_directive
            self._replace_in_file(candidate_path, old, new)
            score_title = manager._get_title(year=False)
            if score_title:
                old = 'SCORE_NAME'
                new = score_title
                self._replace_in_file(candidate_path, old, new)
            annotated_title = manager._get_title(year=True)
            if annotated_title:
                old = 'SCORE_TITLE'
                new = annotated_title
                self._replace_in_file(candidate_path, old, new)
            forces_tagline = manager._get_metadatum('forces_tagline')
            if forces_tagline:
                old = 'FORCES_TAGLINE'
                new = forces_tagline
                self._replace_in_file(candidate_path, old, new)
            self._handle_candidate(candidate_path, destination_path)

    def generate_preface_source(self):
        r'''Generates ``preface.tex``.

        Returns none.
        '''
        self._copy_boilerplate('preface.tex')

    def generate_score_source(self):
        r'''Generates ``score.tex``.

        Returns none.
        '''
        self._copy_boilerplate('score.tex')

    def go_to_next_package(self):
        r'''Goes to next package.

        Returns none.
        '''
        self._go_to_next_package()

    def go_to_previous_package(self):
        r'''Goes to previous package.

        Returns none.
        '''
        self._go_to_previous_package()

    def make(self):
        r'''Makes asset.

        Returns none.
        '''
        if self._asset_identifier == 'file':
            self._make_file()
        else:
            self._make_package()

    def make_score_package(self):
        r'''Makes score package.

        Returns none.
        '''
        message = 'enter title'
        getter = self._io_manager._make_getter()
        getter.append_string(message)
        title = getter._run()
        if self._session.is_backtracking or not title:
            return
        package_name = stringtools.strip_diacritics(title)
        package_name = stringtools.to_snake_case(package_name)
        confirmed = False 
        while not confirmed:
            package_path = os.path.join(
                self._configuration.user_score_packages_directory,
                package_name,
                )
            message = 'path will be {}.'.format(package_path)
            self._io_manager._display(message)
            result = self._io_manager._confirm()
            if self._session.is_backtracking:
                return
            confirmed = result
            if confirmed:
                break
            message = 'enter package name'
            getter = self._io_manager._make_getter()
            getter.append_string(message)
            package_name = getter._run()
            if self._session.is_backtracking or not package_name:
                return
            package_name = stringtools.strip_diacritics(package_name)
            package_name = stringtools.to_snake_case(package_name)
        manager = self._get_manager(package_path)
        manager._make_package()
        manager._add_metadatum('title', title)
        year = datetime.date.today().year
        manager._add_metadatum('year', year)
        package_paths = self._list_visible_asset_paths()
        if package_path not in package_paths:
            with self._io_manager._silent():
                self._clear_view()
        manager._run()

    def illustrate_every_definition_py(self):
        r'''Illustrates ``definition.py`` in every package.

        Returns none.
        '''
        managers = self._list_visible_asset_managers()
        inputs, outputs = [], []
        method_name = 'illustrate_definition_py'
        for manager in managers:
            method = getattr(manager, method_name)
            inputs_, outputs_ = method(dry_run=True)
            inputs.extend(inputs_)
            outputs.extend(outputs_)
        messages = self._format_messaging(inputs, outputs, verb='illustrate')
        self._io_manager._display(messages)
        result = self._io_manager._confirm()
        if self._session.is_backtracking or not result:
            return
        for manager in managers:
            method = getattr(manager, method_name)
            method()

    def interpret_back_cover(self):
        r'''Interprets ``back-cover.tex``.

        Returns none.
        '''
        self._interpret_file_ending_with('back-cover.tex')

    def interpret_every_illustration_ly(
        self, 
        open_every_illustration_pdf=True,
        ):
        r'''Interprets ``illustration.ly`` in every package.

        Makes ``illustration.pdf`` in every package.

        Returns none.
        '''
        managers = self._list_visible_asset_managers()
        inputs, outputs = [], []
        method_name = 'interpret_illustration_ly'
        for manager in managers:
            method = getattr(manager, method_name)
            inputs_, outputs_ = method(dry_run=True)
            inputs.extend(inputs_)
            outputs.extend(outputs_)
        messages = self._format_messaging(inputs, outputs)
        self._io_manager._display(messages)
        result = self._io_manager._confirm()
        if self._session.is_backtracking or not result:
            return
        for manager in managers:
            with self._io_manager._silent():
                method = getattr(manager, method_name)
                subprocess_messages, candidate_messages = method()
            if subprocess_messages:
                self._io_manager._display(subprocess_messages)
                self._io_manager._display(candidate_messages)
                self._io_manager._display('')
                
    def interpret_front_cover(self):
        r'''Interprets ``front-cover.tex``.

        Returns none.
        '''
        self._interpret_file_ending_with('front-cover.tex')

    def interpret_music(self):
        r'''Interprets ``music.ly``.

        Returns none.
        '''
        self._call_lilypond_on_file_ending_with('music.ly')

    def interpret_open_front_cover(self):
        r'''Interprets ``front-cover.tex`` and then opens ``front-cover.pdf``.

        Returns none.
        '''
        self.interpret_front_cover()
        self.open_front_cover_pdf()
        
    def interpret_preface(self):
        r'''Interprets ``preface.tex``.

        Returns none.
        '''
        self._interpret_file_ending_with('preface.tex')

    def interpret_score(self):
        r'''Interprets ``score.tex``.

        Returns none.
        '''
        self._interpret_file_ending_with('score.tex')

    def open_every_illustration_pdf(self):
        r'''Opens ``illustration.pdf`` in every package.

        Returns none.
        '''
        self._open_in_every_package('illustration.pdf')

    def open_every_score_pdf(self):
        r'''Opens ``score.pdf`` in every package.

        Returns none.
        '''
        managers = self._list_visible_asset_managers()
        paths = []
        for manager in managers:
            inputs, outputs = manager.open_score_pdf(dry_run=True)
            paths.extend(inputs)
        messages = ['will open ...']
        tab = self._io_manager._tab
        paths = [tab + _ for _ in paths]
        messages.extend(paths)
        self._io_manager._display(messages)
        result = self._io_manager._confirm()
        if self._session.is_backtracking or not result:
            return
        if paths:
            self._io_manager.open_file(paths)

    def push_score_pdf_to_distribution_directory(self):
        r'''Pushes ``score.pdf`` to distribution directory.

        Returns none.
        '''
        path = self._session.current_build_directory
        build_score_path = os.path.join(path, 'score.pdf')
        if not os.path.exists(build_score_path):
            message = 'does not exist: {!r}.'
            message = message.format(build_score_path)
            self._io_manager._display(message)
            return
        score_package_name = self._session.current_score_package_name
        score_package_name = score_package_name.replace('_', '-')
        distribution_file_name = '{}-score.pdf'.format(score_package_name)
        distribution_directory = self._session.current_distribution_directory
        distribution_score_path = os.path.join(
            distribution_directory,
            distribution_file_name,
            )
        shutil.copyfile(build_score_path, distribution_score_path)
        messages = []
        messages.append('Copied')
        message = ' FROM: {}'.format(build_score_path)
        messages.append(message)
        message = '   TO: {}'.format(distribution_score_path)
        messages.append(message)
        self._io_manager._display(messages)

    def remove(self):
        r'''Removes asset.

        Returns none.
        '''
        from ide import idetools
        self._session._attempted_to_remove = True
        if self._session.is_repository_test:
            return
        paths = self._select_visible_asset_paths()
        if not paths:
            return
        count = len(paths)
        messages = []
        if count == 1:
            message = 'will remove {}'.format(paths[0])
            messages.append(message)
        else:
            messages.append('will remove ...')
            for path in paths:
                message = '    {}'.format(path)
                messages.append(message)
        self._io_manager._display(messages)
        if count == 1:
            confirmation_string = 'remove'
        else:
            confirmation_string = 'remove {}'
            confirmation_string = confirmation_string.format(count)
        message = "type {!r} to proceed"
        message = message.format(confirmation_string)
        getter = self._io_manager._make_getter()
        getter.append_string(message)
        if self._session.confirm:
            result = getter._run()
            if self._session.is_backtracking or result is None:
                return
            if not result == confirmation_string:
                return
        for path in paths:
            manager = self._get_manager(path)
            with self._io_manager._silent():
                manager._remove()
        self._session._pending_redraw = True

    def remove_every_unadded_asset(self):
        r'''Removes files not yet added to repository of every asset.

        Returns none.
        '''
        self._session._attempted_remove_unadded_assets = True
        if self._session.is_test and not self._session.is_in_score:
            return
        paths = self._list_visible_asset_paths()
        paths = self._extract_common_parent_directories(paths)
        paths.sort()
        inputs, outputs = [], []
        managers = []
        method_name = 'remove_unadded_assets'
        for path in paths:
            manager = self._io_manager._make_package_manager(path)
            managers.append(manager)
            method = getattr(manager, method_name)
            inputs_, outputs_ = method(dry_run=True)
            inputs.extend(inputs_)
            outputs.extend(outputs_)
        messages = self._format_messaging(inputs, outputs, verb='remove')
        self._io_manager._display(messages)
        if not inputs:
            return
        result = self._io_manager._confirm()
        if self._session.is_backtracking or not result:
            return
        with self._io_manager._silent():
            for manager in managers:
                method = getattr(manager, method_name)
                method()
        count = len(inputs)
        identifier = stringtools.pluralize('asset', count)
        message = 'removed {} unadded {}.'
        message = message.format(count, identifier)
        self._io_manager._display(message)

    def rename(
        self,
        extension=None,
        file_name_callback=None, 
        ):
        r'''Renames asset.

        Returns none.
        '''
        extension = extension or getattr(self, '_extension', '')
        path = self._select_visible_asset_path(infinitive_phrase='to rename')
        if not path:
            return
        file_name = os.path.basename(path)
        message = 'existing file name> {}'
        message = message.format(file_name)
        self._io_manager._display(message)
        manager = self._get_manager(path)
        manager._asset_identifier = self._asset_identifier
        manager._rename_interactively(
            extension=extension,
            file_name_callback=file_name_callback,
            force_lowercase=self._force_lowercase,
            )
        self._session._is_backtracking_locally = False

    def revert_every_asset(self):
        r'''Reverts every asset to repository.

        Returns none.
        '''
        self._session._attempted_to_revert = True
        if self._session.is_repository_test:
            return
        paths = self._list_visible_asset_paths()
        for path in paths:
            manager = self._io_manager._make_package_manager(path)
            manager.revert()

    def set_view(self):
        r'''Sets view.

        Writes view name to ``__metadata.py__``.

        Returns none.
        '''
        infinitive_phrase = 'to apply'
        view_name = self._select_view(infinitive_phrase=infinitive_phrase)
        if self._session.is_backtracking or view_name is None:
            return
        if view_name == 'none':
            view_name = None
        if self._session.is_in_score:
            manager = self._current_package_manager
            metadatum_name = 'view_name'
        else:
            manager = self._views_package_manager
            metadatum_name = '{}_view_name'.format(type(self).__name__)
        manager._add_metadatum(metadatum_name, view_name)

    def update_every_asset(self):
        r'''Updates every asset from repository.

        Returns none.
        '''
        tab = self._io_manager._tab
        managers = self._list_visible_asset_managers()
        for manager in managers:
            messages = []
            message = self._path_to_asset_menu_display_string(manager._path)
            message = self._strip_annotation(message)
            message = message + ':'
            messages_ = manager.update(messages_only=True)
            if len(messages_) == 1:
                message = message + ' ' + messages_[0]
                messages.append(message)
            else:
                messages_ = [tab + _ for _ in messages_]
                messages.extend(messages_)
            self._io_manager._display(messages, capitalize=False)