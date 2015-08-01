# -*- encoding: utf-8 -*-
from __future__ import print_function
import codecs
import os
import shutil
import sys
from abjad.tools import datastructuretools
from abjad.tools import developerscripttools
from abjad.tools import stringtools
from abjad.tools import systemtools
from ide.tools.idetools.Command import Command
from ide.tools.idetools.Controller import Controller


class AssetController(Controller):
    r'''Asset controller.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_asset_identifier',
        '_basic_breadcrumb',
        '_controller_commands',
        )

    known_secondary_assets = (
        '__init__.py',
        '__metadata__.py',
        '__views__.py',
        '__abbreviations__.py',
        )

    ### INITIALIZER ###

    def __init__(self, session=None):
        superclass = super(AssetController, self)
        superclass.__init__(session=session)
        self._asset_identifier = None
        self._basic_breadcrumb = None
        self._controller_commands = []
        self._controller_commands.extend([
            self.go_back,
            self.go_to_all_score_directories,
            self.go_to_score_directory,
            self.quit_abjad_ide,
            self.display_action_commands,
            self.display_navigation_commands,
            self.invoke_shell,
            self.open_lilypond_log,
            ])

    ### PRIVATE PROPERTIES ###

    @property
    def _abjad_import_statement(self):
        return 'from abjad import *'

    @property
    def _navigation_commands(self):
        result = (
            'b', 'q',
            'dd', 'ee', 'gg', 'kk', 'mm', 'h', 'uu', 'yy',
            'd', 'e', 'g', 'k', 'm', 's', 'u', 'y',
            )
        return result

    @property
    def _unicode_directive(self):
        return '# -*- encoding: utf-8 -*-'

    @property
    def _views_package_manager(self):
        path = self._configuration.abjad_ide_wrangler_views_directory
        return self._io_manager._make_package_manager(path)

    @property
    def _views_py_path(self):
        if self._session.is_in_score:
            directory = self._get_current_directory()
            return os.path.join(directory, '__views__.py')
        else:
            directory = self._configuration.abjad_ide_wrangler_views_directory
            class_name = type(self).__name__
            file_name = '__{}_views__.py'.format(class_name)
            return os.path.join(directory, file_name)

    @property
    def _wrangler_navigation_to_session_variable(self):
        result = {
            'd': '_is_navigating_to_distribution_files',
            'e': '_is_navigating_to_etc_files',
            'g': '_is_navigating_to_segments',
            'k': '_is_navigating_to_maker_files',
            'm': '_is_navigating_to_materials',
            'u': '_is_navigating_to_build_files',
            'y': '_is_navigating_to_stylesheets',
        }
        return result

    ### PRIVATE METHODS ###

    def _git_add(self, dry_run=False):
        directory = self._get_current_directory()
        change = systemtools.TemporaryDirectoryChange(directory=directory)
        with change:
            inputs = self._get_unadded_asset_paths()
            outputs = []
            if dry_run:
                return inputs, outputs
            if not inputs:
                message = 'nothing to add.'
                self._io_manager._display(message)
                return
            messages = []
            messages.append('will add ...')
            for path in inputs:
                messages.append(self._tab + path)
            self._io_manager._display(messages)
            result = self._io_manager._confirm()
            if self._session.is_backtracking or not result:
                return
            command = self._repository_add_command
            assert isinstance(command, str)
            self._io_manager.run_command(command)

    def _git_commit(self, commit_message=None):
        directory = self._get_current_directory()
        change = systemtools.TemporaryDirectoryChange(directory=directory)
        with change:
            self._session._attempted_to_commit = True
            if self._session.is_repository_test:
                return
            if commit_message is None:
                getter = self._io_manager._make_getter()
                getter.append_string('commit message')
                commit_message = getter._run()
                if self._session.is_backtracking or commit_message is None:
                    return
                message = 'commit message will be: "{}"'
                message = message.format(commit_message)
                self._io_manager._display(message)
                result = self._io_manager._confirm()
                if self._session.is_backtracking or not result:
                    return
            message = self._get_score_package_directory_name()
            message = message + ' ...'
            command = self._make_repository_commit_command(commit_message)
            self._io_manager.run_command(command, capitalize=False)

    def _git_status(self):
        directory = self._get_current_directory()
        change = systemtools.TemporaryDirectoryChange(directory=directory)
        with change:
            command = 'git status {}'.format(directory)
            messages = []
            self._session._attempted_display_status = True
            message = 'Repository status for {} ...'
            message = message.format(directory)
            messages.append(message)
            directory = self._get_current_directory()
            with systemtools.TemporaryDirectoryChange(directory=directory):
                process = self._io_manager.make_subprocess(command)
            path = directory
            path = path + os.path.sep
            clean_lines = []
            stdout_lines = self._io_manager._read_from_pipe(process.stdout)
            for line in stdout_lines.splitlines():
                line = str(line)
                clean_line = line.strip()
                clean_line = clean_line.replace(path, '')
                clean_lines.append(clean_line)
            everything_ok = False
            for line in clean_lines:
                if 'nothing to commit' in line:
                    everything_ok = True
                    break
            if clean_lines and not everything_ok:
                messages.extend(clean_lines)
            else:
                first_message = messages[0]
                first_message = first_message + ' OK'
                messages[0] = first_message
                clean_lines.append(message)
            self._io_manager._display(messages, capitalize=False)

    def _git_revert(self):
        directory = self._get_current_directory()
        change = systemtools.TemporaryDirectoryChange(directory=directory)
        with change:
            self._session._attempted_to_revert = True
            if self._session.is_repository_test:
                return
            paths = []
            paths.extend(self._get_added_asset_paths())
            paths.extend(self._get_modified_asset_paths())
            messages = []
            messages.append('will revert ...')
            for path in paths:
                messages.append(self._io_manager._tab + path)
            self._io_manager._display(messages)
            result = self._io_manager._confirm()
            if self._session.is_backtracking or not result:
                return
            commands = []
            if self._is_in_git_repository():
                for path in paths:
                    command = 'git checkout {}'.format(path)
                    commands.append(command)
            else:
                raise ValueError(self)
            command = ' && '.join(commands)
            directory = self._get_current_directory()
            with systemtools.TemporaryDirectoryChange(directory=directory):
                self._io_manager.spawn_subprocess(command)

    def _git_update(self, messages_only=False):
        messages = []
        directory = self._get_current_directory()
        change = systemtools.TemporaryDirectoryChange(directory=directory)
        with change:
            self._session._attempted_to_update = True
            if self._session.is_repository_test:
                return messages
            command = self._repository_update_command
            messages = self._io_manager.run_command(
                command,
                messages_only=True,
                )
        if messages and messages[-1].startswith('At revision'):
            messages = messages[-1:]
        elif messages and 'Already up-to-date' in messages[-1]:
            messages = messages[-1:]
        if messages_only:
            return messages
        self._io_manager._display(messages)

    def _enter_run(self):
        if self._basic_breadcrumb == 'build':
            self._session._is_navigating_to_build_files = False   
        elif self._basic_breadcrumb == 'distribution':
            self._session._is_navigating_to_distribution_files = False
        elif self._basic_breadcrumb == 'etc':
            self._session._is_navigating_to_etc_files = False
        elif self._basic_breadcrumb == 'makers':
            self._session._is_navigating_to_maker_files = False
        elif self._basic_breadcrumb == 'stylesheets':
            self._session._is_navigating_to_stylesheets = False
        elif self._basic_breadcrumb == 'segments':
            self._session._is_navigating_to_segments = False
        elif self._basic_breadcrumb == 'materials':
            self._session._is_navigating_to_materials = False
        elif self._asset_identifier == 'package manager':
            self._session._is_navigating_to_next_asset = False
            self._session._is_navigating_to_previous_asset = False
            self._session._last_asset_path = self._path
        elif self._asset_identifier == 'score package manager':
            self._session._is_navigating_to_next_asset = False
            self._session._is_navigating_to_previous_asset = False
            self._session._last_asset_path = self._path
            self._session._last_score_path = self._path

    def _exit_run(self):
        if self._asset_identifier == 'package manager':
            return self._session.is_backtracking
        elif self._asset_identifier == 'score package manager':
            result = self._session.is_backtracking
            if self._session.is_backtracking_to_score:
                self._session._is_backtracking_to_score = False
                result = False
            elif self._session.is_autonavigating_within_score:
                if self._session.is_backtracking_to_all_scores:
                    result = True
                else:
                    result = False
            return result

    def _filter_asset_menu_entries_by_view(self, entries):
        view = self._read_view()
        if view is None:
            return entries
        entries = entries[:]
        filtered_entries = []
        for pattern in view:
            if ':ds:' in pattern:
                for entry in entries:
                    if self._match_display_string_view_pattern(pattern, entry):
                        filtered_entries.append(entry)
            elif 'md:' in pattern:
                for entry in entries:
                    if self._match_metadata_view_pattern(pattern, entry):
                        filtered_entries.append(entry)
            elif ':path:' in pattern:
                for entry in entries:
                    if self._match_path_view_pattern(pattern, entry):
                        filtered_entries.append(entry)
            else:
                for entry in entries:
                    display_string, _, _, path = entry
                    if pattern == display_string:
                        filtered_entries.append(entry)
        return filtered_entries

    @staticmethod
    def _format_messaging(inputs, outputs, verb='interpret'):
        messages = []
        if not inputs and not outputs:
            message = 'no files to {}.'
            message = message.format(verb)
            messages.append(message)
            return messages
        message = 'will {} ...'.format(verb)
        messages.append(message)
        if outputs:
            input_label = '  INPUT: '
        else:
            input_label = '    '
        output_label = ' OUTPUT: '
        if not outputs:
            for path_list in inputs:
                if isinstance(path_list, str):
                    path_list = [path_list]
                for path in path_list:
                    messages.append('{}{}'.format(input_label, path))
        else:
            for inputs_, outputs_ in zip(inputs, outputs):
                if isinstance(inputs_, str):
                    inputs_ = [inputs_]
                assert isinstance(inputs_, (tuple, list)), repr(inputs_)
                for path_list in inputs_:
                    if isinstance(path_list, str):
                        path_list = [path_list]
                    for path in path_list:
                        messages.append('{}{}'.format(input_label, path))
                for path_list in outputs_:
                    if isinstance(path_list, str):
                        path_list = [path_list]
                    for path in path_list:
                        messages.append('{}{}'.format(output_label, path))
                messages.append('')
        return messages

    def _get_current_directory(self):
        score_directory = self._session.current_score_directory
        if score_directory is not None:
            directory = os.path.join(
                score_directory,
                self._directory_name,
                )
            directory = os.path.abspath(directory)
            return directory

    def _get_metadata(self):
        metadata = None
        if os.path.isfile(self._metadata_py_path):
            with open(self._metadata_py_path, 'r') as file_pointer:
                file_contents_string = file_pointer.read()
            try:
                result = self._io_manager.execute_string(
                    file_contents_string,
                    attribute_names=('metadata',),
                    )
                metadata = result[0]
            except SyntaxError:
                message = 'can not interpret metadata py: {!r}.'
                message = message.format(self)
                self._io_manager._display(message)
        metadata = metadata or datastructuretools.TypedOrderedDict()
        return metadata

    def _get_score_metadata(self):
        score_path = self._path_to_score_path(self._path)
        if score_path is None:
            return datastructuretools.TypedOrderedDict()
        score_package_manager = self._io_manager._make_package_manager(
            path=score_path)
        return score_package_manager._get_metadata()

    def _get_sibling_score_directory(self, next_=True):
        paths = self._list_visible_asset_paths()
        if self._session.last_asset_path is None:
            if next_:
                return paths[0]
            else:
                return paths[-1]
        score_path = self._session.last_score_path
        index = paths.index(score_path)
        if next_:
            sibling_index = (index + 1) % len(paths)
        else:
            sibling_index = (index - 1) % len(paths)
        sibling_path = paths[sibling_index]
        return sibling_path

    def _get_sibling_score_path(self):
        if self._session.is_navigating_to_next_score:
            self._session._is_navigating_to_next_score = False
            self._session._is_navigating_to_scores = False
            return self._get_sibling_score_directory(next_=True)
        if self._session.is_navigating_to_previous_score:
            self._session._is_navigating_to_previous_score = False
            self._session._is_navigating_to_scores = False
            return self._get_sibling_score_directory(next_=False)

    def _go_to_next_package(self):
        self._session._is_navigating_to_next_asset = True
        self._session._display_action_commands = False
        self._session._display_navigation_commands = False
        self._set_is_navigating_to_sibling_asset()

    def _go_to_previous_package(self):
        self._session._is_navigating_to_previous_asset = True
        self._session._display_action_commands = False
        self._session._display_navigation_commands = False
        self._set_is_navigating_to_sibling_asset()

    def _handle_candidate(self, candidate_path, destination_path):
        messages = []
        if not os.path.exists(destination_path):
            shutil.copyfile(candidate_path, destination_path)
            message = 'wrote {}.'.format(destination_path)
            messages.append(message)
        elif systemtools.TestManager.compare_files(
            candidate_path,
            destination_path,
            ):
            tab = self._io_manager._tab
            messages_ = self._make_candidate_messages(
                True, candidate_path, destination_path)
            messages.extend(messages_)
            message = 'preserved {}.'.format(destination_path)
            messages.append(message)
        else:
            shutil.copyfile(candidate_path, destination_path)
            message = 'overwrote {}.'.format(destination_path)
            messages.append(message)
        self._io_manager._display(messages)

    def _handle_input(self, result):
        assert isinstance(result, str), repr(result)
        if result == '<return>':
            return
        with self._io_manager._make_interaction():
            if result.startswith('!'):
                statement = result[1:]
                self._io_manager._invoke_shell(statement)
            elif result in self._command_name_to_method:
                self._command_name_to_method[result]()
            elif (result.endswith('!') and 
                result[:-1] in self._command_name_to_method):
                result = result[:-1]
                with self._io_manager._make_interaction(confirm=False):
                    self._command_name_to_method[result]()
            else:
                self._handle_numeric_user_input(result)

    def _handle_numeric_user_input(self, result):
        if os.path.isfile(result):
            self._io_manager.open_file(result)
        elif os.path.isdir(result):
            basename = os.path.basename(result)
            if basename == 'build':
                self.go_to_score_build_directory()
            elif basename == 'distribution':
                self.go_to_score_distribution_directory()
            elif basename == 'etc':
                self.to_to_score_etc_directory()
            elif basename == 'makers':
                self.go_to_score_makers_directory()
            elif basename == 'materials':
                self.go_to_score_materials_directory()
            elif basename == 'segments':
                self.to_to_score_segments_directory()
            elif basename == 'stylesheets':
                self.go_to_score_stylesheets()
            elif basename == 'test':
                self.go_to_score_test_files()
            else:
                manager = self._get_manager(result)
                manager._run()
        else:
            message = 'must be file or directory: {!r}.'
            message = message.format(result)
            raise Exception(message)

    def _handle_wrangler_navigation_directive(self, expr):
        if expr in self._wrangler_navigation_to_session_variable:
            variable = self._wrangler_navigation_to_session_variable[expr]
            setattr(self._session, variable, True)

    @staticmethod
    def _is_directory_with_metadata_py(path):
        if os.path.isdir(path):
            for directory_entry in sorted(os.listdir(path)):
                if directory_entry == '__metadata__.py':
                    return True
        return False

    def _is_valid_directory_entry(self, directory_entry):
        if directory_entry[0].isalpha():
            if not directory_entry.endswith('.pyc'):
                return True
        return False

    @staticmethod
    def _list_directories_with_metadata_pys(path):
        paths = []
        for directory, subdirectory_names, file_names in os.walk(path):
            if AssetController._is_directory_with_metadata_py(directory):
                if directory not in paths:
                    paths.append(directory)
            for subdirectory_name in subdirectory_names:
                path = os.path.join(directory, subdirectory_name)
                if AssetController._is_directory_with_metadata_py(path):
                    if path not in paths:
                        paths.append(path)
        return paths

    def _make_command_menu_sections(self, menu, menu_section_names=None):
        methods = self._get_decorated_methods(only_my_methods=True)
        #raise Exception(methods)
        method_groups = {}
        for method in methods:
            if menu_section_names is not None:
                if method.menu_section_name not in menu_section_names:
                    continue
            if method.menu_section_name not in method_groups:
                method_groups[method.menu_section_name] = []
            method_group = method_groups[method.menu_section_name]
            method_group.append(method)
        for menu_section_name in method_groups:
            method_group = method_groups[menu_section_name]
            is_hidden = True
            if menu_section_name == 'basic':
                is_hidden = False
            menu.make_command_section(
                is_hidden=is_hidden,
                commands=method_group,
                name=menu_section_name,
                )

    def _make_secondary_asset_menu_entries(self):
        menu_entries = []
        if not self._session.is_in_score:
            return menu_entries
        current_directory = self._get_current_directory()
        if not current_directory:
            return menu_entries
        for name in os.listdir(current_directory):
            if name in self.known_secondary_assets:
                path = os.path.join(current_directory, name)
                menu_entry = (name, None, None, path)
                menu_entries.append(menu_entry)
        return menu_entries

    def _make_candidate_messages(self, result, candidate_path, incumbent_path):
        messages = []
        tab = self._io_manager._tab
        messages.append('the files ...')
        messages.append(tab + candidate_path)
        messages.append(tab + incumbent_path)
        if result:
            messages.append('... compare the same.')
        else:
            messages.append('... compare differently.')
        return messages

    def _make_main_menu(self):
        menu = self._io_manager._make_menu(name=self._spaced_class_name)
        self._make_asset_menu_section(menu)
        self._make_command_menu_sections(menu)
        return menu

    def _open_file(self, path):
        if os.path.isfile(path):
            self._io_manager.open_file(path)
        else:
            message = 'can not find file: {}.'
            message = message.format(path)
            self._io_manager._display(message)

    def _path_to_annotation(self, path):
        score_storehouses = (
            self._configuration.abjad_ide_example_scores_directory,
            self._configuration.composer_scores_directory,
            )
        if path.startswith(score_storehouses):
            score_path = self._path_to_score_path(path)
            manager = self._io_manager._make_package_manager(path=score_path)
            metadata = manager._get_metadata()
            if metadata:
                year = metadata.get('year')
                title = metadata.get('title')
                prototype = ('score package manager', 'score package')
                if self._asset_identifier in prototype and year:
                    annotation = '{} ({})'.format(title, year)
                else:
                    annotation = str(title)
            else:
                package_name = os.path.basename(path)
                annotation = package_name
        elif path.startswith(self._configuration.abjad_root_directory):
            annotation = 'Abjad'
        else:
            annotation = None
        return annotation

    def _path_to_asset_menu_display_string(self, path):
        name = os.path.basename(path)
        if '_' in name:
            name = stringtools.to_space_delimited_lowercase(name)
        asset_name = name
        if 'segments' in path:
            manager = self._io_manager._make_package_manager(path=path)
            name = manager._get_metadatum('name')
            asset_name = name or asset_name
        if self._session.is_in_score:
            string = asset_name
        else:
            annotation = self._path_to_annotation(path)
            prototype = ('score package manager', 'score package')
            if self._asset_identifier in prototype:
                string = annotation
            else:
                string = '{} ({})'.format(asset_name, annotation)
        return string

    def _path_to_score_path(self, path):
        is_user_score = False
        if path.startswith(self._configuration.composer_scores_directory):
            is_user_score = True
            prefix = len(self._configuration.composer_scores_directory)
        elif path.startswith(self._configuration.abjad_ide_example_scores_directory):
            prefix = len(self._configuration.abjad_ide_example_scores_directory)
        else:
            return
        path_prefix = path[:prefix]
        path_suffix = path[prefix + 1:]
        score_name = path_suffix.split(os.path.sep)[0]
        score_path = os.path.join(path_prefix, score_name)
        # test for installable Python package structure
        outer_init_path = os.path.join(score_path, '__init__.py')
        inner_init_path = os.path.join(
            score_path, 
            score_name, 
            '__init__.py',
            )
        if (not os.path.exists(outer_init_path) and
            os.path.exists(inner_init_path)):
            score_path = os.path.join(score_path, score_name)
        return score_path

    def _read_view(self):
        view_name = self._read_view_name()
        if not view_name:
            return
        view_inventory = self._read_view_inventory()
        if not view_inventory:
            return
        return view_inventory.get(view_name)

    def _read_view_inventory(self):
        from ide.tools import idetools
        if self._views_py_path is None:
            return
        if not os.path.exists(self._views_py_path):
            return
        result = self._io_manager.execute_file(
            path=self._views_py_path,
            attribute_names=('view_inventory',),
            )
        if result == 'corrupt':
            messages = []
            message = '{} __views.py__ is corrupt:'
            message = message.format(type(self).__name__)
            messages.append(message)
            messages.append('')
            message = '    {}'.format(self._views_py_path)
            messages.append(message)
            self._io_manager._display(messages)
            return
        if not result:
            return
        assert len(result) == 1
        view_inventory = result[0]
        if view_inventory is None:
            view_inventory = idetools.ViewInventory()
        items = list(view_inventory.items())
        view_inventory = idetools.ViewInventory(items)
        return view_inventory

    def _read_view_name(self):
        if self._session.is_in_score:
            manager = self._current_package_manager
            metadatum_name = 'view_name'
        else:
            manager = self._views_package_manager
            metadatum_name = '{}_view_name'.format(type(self).__name__)
        if not manager:
            return
        return manager._get_metadatum(metadatum_name)

    @staticmethod
    def _remove_file_line(file_path, line_to_remove):
        lines_to_keep = []
        with open(file_path, 'r') as file_pointer:
            for line in file_pointer.readlines():
                if line == line_to_remove:
                    pass
                else:
                    lines_to_keep.append(line)
        with open(file_path, 'w') as file_pointer:
            contents = ''.join(lines_to_keep)
            file_pointer.write(contents)

    @staticmethod
    def _replace_in_file(file_path, old, new):
        assert isinstance(old, str), repr(old)
        assert isinstance(new, str), repr(new)
        with open(file_path, 'r') as file_pointer:
            new_file_lines = []
            for line in file_pointer.readlines():
                line = line.replace(old, new)
                new_file_lines.append(line)
        new_file_contents = ''.join(new_file_lines)
        if sys.version_info[0] == 2:
            new_file_contents = unicode(new_file_contents, 'utf-8')
            with codecs.open(file_path, 'w', encoding='utf-8') as file_pointer:
                file_pointer.write(new_file_contents)
        else:
            with open(file_path, 'w') as file_pointer:
                file_pointer.write(new_file_contents)

    def _set_is_navigating_to_sibling_asset(self):
        if self._basic_breadcrumb in ('materials', 'MATERIALS'):
            self._session._is_navigating_to_materials = True            
        elif self._basic_breadcrumb in ('segments', 'SEGMENTS'):
            self._session._is_navigating_to_segments = True

    @staticmethod
    def _sort_ordered_dictionary(dictionary):
        new_dictionary = type(dictionary)()
        for key in sorted(dictionary):
            new_dictionary[key] = dictionary[key]
        return new_dictionary
        
    def _write_metadata_py(self, metadata, metadata_py_path=None):
        lines = []
        lines.append(self._unicode_directive)
        lines.append('from abjad import *')
        lines.append('')
        lines.append('')
        contents = '\n'.join(lines)
        metadata = datastructuretools.TypedOrderedDict(metadata)
        items = list(metadata.items())
        items.sort()
        metadata = datastructuretools.TypedOrderedDict(items)
        metadata_lines = format(metadata, 'storage')
        metadata_lines = 'metadata = {}'.format(metadata_lines)
        contents = contents + '\n' + metadata_lines
        metadata_py_path = metadata_py_path or self._metadata_py_path
        with open(metadata_py_path, 'w') as file_pointer:
            file_pointer.write(contents)

    def _write_view_inventory(self, view_inventory):
        lines = []
        lines.append(self._unicode_directive)
        lines.append(self._abjad_import_statement)
        lines.append('from ide.tools import idetools')
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

    @Command('?', 'display action commands', 'system')
    def display_action_commands(self):
        r'''Displays action commands.

        Returns none.
        '''
        if not self._session.is_in_confirmation_environment:
            show = self._session.display_action_commands
            self._session._display_action_commands = not show

    @Command(';', 'display navigation commands', 'display navigation', True)
    def display_navigation_commands(self):
        r'''Displays navigation commands.

        Returns none.
        '''
        if not self._session.is_in_confirmation_environment:
            show = self._session.display_navigation_commands
            self._session._display_navigation_commands = not show

    @Command('abb', 'edit abbreviations file', 'global files')
    def edit_abbreviations_file(self):
        r'''Edits abbreviations file.

        Returns none.
        '''
        path = self._session.current_abbreviations_file_path
        if not path or not os.path.isfile(path):
            with open(path, 'w') as file_pointer:
                file_pointer.write('')
        self._io_manager.edit(path)

    @Command('sse', 'edit score stylesheet', 'global files')
    def edit_score_stylesheet(self):
        r'''Edits score stylesheet.

        Returns none.
        '''
        path = self._session.current_stylesheet_path
        if not path or not os.path.isfile(path):
            with open(path, 'w') as file_pointer:
                file_pointer.write('')
        self._io_manager.edit(path)

    @Command('b', 'back', 'back-home-quit', True)
    def go_back(self):
        r'''Goes back.

        Returns none.
        '''
        self._session._is_backtracking_locally = True
        self._session._display_action_commands = False
        self._session._display_navigation_commands = False

    @Command('uu', 'go to all build directories', 'comparison', True)
    def go_to_all_build_directories(self):
        r'''Goes to all build files.

        Returns none.
        '''
        self.go_to_all_score_directories()
        self._session._is_navigating_to_build_files = True

    @Command('dd', 'go to all distribution directories', 'comparison', True)
    def go_to_all_distribution_directories(self):
        r'''Goes to all distribution files.

        Returns none.
        '''
        self.go_to_all_score_directories()
        self._session._is_navigating_to_distribution_files = True

    @Command('ee', 'go to all etc directories', 'comparison', True)
    def go_to_all_etc_directories(self):
        r'''Goes to all etc files.

        Returns none.
        '''
        self.go_to_all_score_directories()
        self._session._is_navigating_to_etc_files = True

    @Command('kk', 'go to all makers directories', 'comparison', True)
    def go_to_all_makers_directories(self):
        r'''Goes to all maker files.

        Returns none.
        '''
        self.go_to_all_score_directories()
        self._session._is_navigating_to_maker_files = True

    @Command('mm', 'go to all materials directories', 'comparison', True)
    def go_to_all_materials_directories(self):
        r'''Goes to all materials.

        Returns none.
        '''
        self.go_to_all_score_directories()
        self._session._is_navigating_to_materials = True

    @Command('h', 'home', 'back-home-quit', True)
    def go_to_all_score_directories(self):
        r'''Goes to all score directories.

        Returns none.
        '''
        self._session._is_navigating_home = False
        self._session._is_navigating_to_scores = True
        self._session._display_action_commands = False
        self._session._display_navigation_commands = False

    @Command('gg', 'go to all segments directories', 'comparison', True)
    def go_to_all_segments_directories(self):
        r'''Goes to all segments.

        Returns none.
        '''
        self.go_to_all_score_directories()
        self._session._is_navigating_to_segments = True

    @Command('yy', 'go to all stylesheets directories', 'comparison', True)
    def go_to_all_stylesheets_directories(self):
        r'''Goes to all stylesheets.

        Returns none.
        '''
        self.go_to_all_score_directories()
        self._session._is_navigating_to_stylesheets = True

    @Command('>', 'go to next package', 'sibling package', True)
    def go_to_next_package(self):
        r'''Goes to next package.

        Returns none.
        '''
        self._go_to_next_package()

    @Command('>>', 'go to next score', 'sibling score', True)
    def go_to_next_score(self):
        r'''Goes to next score.

        Returns none.
        '''
        self._session._is_navigating_to_next_score = True
        self._session._is_navigating_to_scores = True
        self._session._display_action_commands = False
        self._session._display_navigation_commands = False

    @Command('<', 'go to previous package', 'sibling package', True)
    def go_to_previous_package(self):
        r'''Goes to previous package.

        Returns none.
        '''
        self._go_to_previous_package()

    @Command('<<', 'go to previous score', 'sibling score', True)
    def go_to_previous_score(self):
        r'''Goes to previous score.

        Returns none.
        '''
        self._session._is_navigating_to_previous_score = True
        self._session._is_navigating_to_scores = True
        self._session._display_action_commands = False
        self._session._display_navigation_commands = False

    @Command('u', 'go to build directory', 'navigation', True)
    def go_to_score_build_directory(self):
        r'''Goes to build files.

        Returns none.
        '''
        self._session._abjad_ide._build_file_wrangler._run()

    @Command('s', 'go to score', 'system', True)
    def go_to_score_directory(self):
        r'''Goes to current score.

        Returns none.
        '''
        if self._session.is_in_score:
            self._session._is_backtracking_to_score = True
            self._session._display_action_commands = False
            self._session._display_navigation_commands = False
            
    @Command('d', 'go to distribution directory', 'navigation', True)
    def go_to_score_distribution_directory(self):
        r'''Goes to distribution files.

        Returns none.
        '''
        self._session._abjad_ide._distribution_file_wrangler._run()

    @Command('e', 'go to etc directory', 'navigation', True)
    def go_to_score_etc_directory(self):
        r'''Goes to etc files.

        Returns none.
        '''
        self._session._abjad_ide._etc_file_wrangler._run()

    @Command('k', 'go to makers directory', 'navigation', True)
    def go_to_score_makers_directory(self):
        r'''Goes to maker files.

        Returns none.
        '''
        self._session._abjad_ide._maker_file_wrangler._run()

    @Command('m', 'go to materials directory', 'navigation', True)
    def go_to_score_materials_directory(self):
        r'''Goes to material packages.

        Returns none.
        '''
        self._session._abjad_ide._material_package_wrangler._run()

    @Command('g', 'go to segments directory', 'navigation', True)
    def go_to_score_segments_directory(self):
        r'''Goes to segment packages.

        Returns none.
        '''
        self._session._abjad_ide._segment_package_wrangler._run()

    @Command('y', 'go to stylehseets directory', 'navigation', True)
    def go_to_score_stylesheets_directory(self):
        r'''Goes to stylesheets.

        Returns none.
        '''
        self._session._abjad_ide._stylesheet_wrangler._run()

    @Command('t', 'go to test directory', 'navigation', True)
    def go_to_score_test_directory(self):
        r'''Geots to score test files.

        Returns none.
        '''
        raise NotImplementedError

    @Command('!', 'invoke shell', 'system')
    def invoke_shell(self):
        r'''Invokes shell.

        Returns none.
        '''
        statement = self._io_manager._handle_input(
            '$',
            include_chevron=False,
            include_newline=False,
            )
        statement = statement.strip()
        self._io_manager._invoke_shell(statement)

    @Command('l', 'open lilypond log', 'global files')
    def open_lilypond_log(self):
        r'''Opens LilyPond log.

        Returns none.
        '''
        from abjad.tools import systemtools
        self._session._attempted_to_open_file = True
        if self._session.is_test:
            return
        systemtools.IOManager.open_last_log()

    @Command('q', 'quit', 'back-home-quit', True)
    def quit_abjad_ide(self):
        r'''Quits Abjad IDE.

        Returns none.
        '''
        self._session._is_quitting = True
        self._session._display_action_commands = False
        self._session._display_navigation_commands = False