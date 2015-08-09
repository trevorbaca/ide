# -*- encoding: utf-8 -*-
from __future__ import print_function
import codecs
import inspect
import os
import shutil
import sys
import time
from abjad.tools import datastructuretools
from abjad.tools import developerscripttools
from abjad.tools import stringtools
from abjad.tools import systemtools
from ide.tools.idetools.AbjadIDEConfiguration import AbjadIDEConfiguration
from ide.tools.idetools.Command import Command
configuration = AbjadIDEConfiguration()


class Controller(object):
    r'''Asset controller.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_breadcrumb_callback',
        '_io_manager',
        '_session',
        )

    _abjad_import_statement = 'from abjad import *'

    _known_secondary_assets = (
        '__init__.py',
        '__metadata__.py',
        '__views__.py',
        '__abbreviations__.py',
        )

    _navigation_command_name_to_directory_name = {
        'd': 'distribution',
        'e': 'etc',
        'g': 'segments',
        'k': 'makers',
        'm': 'materials',
        't': 'test',
        'u': 'build',
        'y': 'stylesheets',
        }

    _known_directory_names = \
        _navigation_command_name_to_directory_name.values()
    _known_directory_names.sort()

    _tab = 4 * ' '

    _unicode_directive = '# -*- encoding: utf-8 -*-'

    ### INITIALIZER ###

    def __init__(self, session=None):
        assert session is not None
        self._breadcrumb_callback = None
        self._io_manager = session._io_manager
        self._session = session

    ### SPECIAL METHODS ###

    def __repr__(self):
        r'''Gets interpreter representation of asset controller.

        Returns string.
        '''
        return '{}()'.format(type(self).__name__)

    ### PRIVATE PROPERTIES ###

    @property
    def _breadcrumb(self):
        if self._breadcrumb_callback is not None:
            metadata_py_path = os.path.join(self._path, '__metadata__.py')
            return self._breadcrumb_callback(metadata_py_path)
        if hasattr(self, '_path'):
            base_name = os.path.basename(self._path)
            result = base_name.replace('_', ' ')
            return result
        else:
            directory_token = self._get_current_directory_token(
                self._session,
                self._directory_name,
                )
            return self._get_breadcrumb(
                directory_token,
                self._hide_breadcrumb_while_in_score,
                )

    @property
    def _command_name_to_command(self):
        result = {}
        methods = self._get_commands()
        for method in methods:
            result[method.command_name] = method
        return result

    ### PRIVATE METHODS ###

    def _add_metadatum(
        self,
        metadata_py_path,
        metadatum_name, 
        metadatum_value,
        ):
        if not metadata_py_path.endswith('__metadata__.py'):
            metadata_py_path = os.path.join(
                metadata_py_path,
                '__metadata__.py',
                )
        assert ' ' not in metadatum_name, repr(metadatum_name)
        metadata = self._get_metadata(metadata_py_path)
        metadata[metadatum_name] = metadatum_value
        with self._io_manager._silent():
            self._write_metadata_py(metadata_py_path, metadata)

    def _call_lilypond_on_file_ending_with(
        self,
        directory,
        string,
        ):
        file_path = self._get_file_path_ending_with(directory, string)
        if file_path:
            self._io_manager.run_lilypond(file_path)
        else:
            message = 'file ending in {!r} not found.'
            message = message.format(string)
            self._io_manager._display(message)
            
    def _check_every_file(
        self,
        directory_token,
        directory_entry_predicate=None,
        hide_breadcrumb_while_in_score=None,
        ):
        directory_name = os.path.basename(directory_token)
        paths = self._list_asset_paths(
            directory_name,
            directory_entry_predicate,
            valid_only=False,
            )
        paths = [_ for _ in paths if os.path.basename(_)[0].isalpha()]
        paths = [_ for _ in paths if not _.endswith('.pyc')]
        if os.path.sep in directory_token:
            paths = [_ for _ in paths if _.startswith(directory_token)]
        invalid_paths = []
        for path in paths:
            file_name = os.path.basename(path)
            if not self._is_valid_directory_entry(file_name):
                invalid_paths.append(path)
        messages = []
        breadcrumb = self._get_breadcrumb(
            directory_token,
            hide_breadcrumb_while_in_score,
            )
        if not invalid_paths:
            count = len(paths)
            message = '{} ({} files): OK'.format(breadcrumb, count)
            messages.append(message)
        else:
            message = '{}:'.format(breadcrumb)
            messages.append(message)
            identifier = 'file'
            count = len(invalid_paths)
            identifier = stringtools.pluralize(identifier, count)
            message = '{} unrecognized {} found:'
            message = message.format(count, identifier)
            message = self._tab + message
            messages.append(message)
            for invalid_path in invalid_paths:
                message = self._tab + self._tab + invalid_path
                messages.append(message)
        self._io_manager._display(messages)
        missing_files, missing_directories = [], []
        return messages, missing_files, missing_directories

    @classmethod
    def _clear_view(class_, io_manager, directory_token):
        if os.path.sep in directory_token:
            manager = self._get_current_package_manager(
                io_manager,
                directory_token,
                )
            metadatum_name = 'view_name'
        else:
            manager = class_._get_views_package_manager(io_manager)
            metadatum_name = '{}_view_name'.format(class_.__name__)
        manager._add_metadatum(
            manager._path,
            metadatum_name,
            None,
            )

    @classmethod
    def _collect_segment_files(class_, session, io_manager, file_name):
        segments_directory = session.current_segments_directory
        build_directory = session.current_build_directory
        directory_entries = sorted(os.listdir(segments_directory))
        source_file_paths, target_file_paths = [], []
        _, file_extension = os.path.splitext(file_name)
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
            score_path = session.current_score_directory
            score_package = class_._path_to_package(score_path)
            score_name = score_package.replace('_', '-')
            directory_entry = directory_entry.replace('_', '-')
            target_file_name = directory_entry + file_extension
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
            io_manager._display(messages)
            if not io_manager._confirm():
                return
            if session.is_backtracking:
                return
        if not os.path.exists(build_directory):
            os.mkdir(build_directory)
        pairs = zip(source_file_paths, target_file_paths)
        return pairs

    def _copy_boilerplate(
        self, 
        source_file_name, 
        destination_directory,
        candidacy=True, 
        replacements=None,
        ):
        replacements = replacements or {}
        source_path = os.path.join(
            configuration.abjad_ide_boilerplate_directory,
            source_file_name,
            )
        destination_path = os.path.join(
            destination_directory,
            source_file_name,
            )
        base_name, file_extension = os.path.splitext(source_file_name)
        candidate_name = base_name + '.candidate' + file_extension
        candidate_path = os.path.join(
            destination_directory,
            candidate_name,
            )
        messages = []
        with systemtools.FilesystemState(remove=[candidate_path]):
            shutil.copyfile(source_path, candidate_path)
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
                if self._io_manager._is_backtracking or not result:
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

    def _enter_run(self):
        if (self._session.navigation_target is not None and
            self._session.navigation_target == self._basic_breadcrumb):
            self._session._navigation_target = None
        elif self._basic_breadcrumb in ('MATERIALS', 'SEGMENTS'):
            self._session._is_navigating_to_next_asset = False
            self._session._is_navigating_to_previous_asset = False
            self._session._last_asset_path = self._path
        elif self._basic_breadcrumb == 'SCORES':
            self._session._is_navigating_to_next_asset = False
            self._session._is_navigating_to_previous_asset = False
            self._session._last_asset_path = self._path
            self._session._last_score_path = self._path

    def _exit_run(self):
        if self._basic_breadcrumb in ('MATERIALS', 'SEGMENTS'):
            return self._session.is_backtracking
        elif self._basic_breadcrumb == 'SCORES':
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

    def _filter_asset_menu_entries_by_view(
        self,
        directory_token,
        entries,
        ):
        view = self._read_view(directory_token)
        if view is None:
            return entries
        entries = entries[:]
        filtered_entries = []
        for pattern in view:
            if ':ds:' in pattern:
                for entry in entries:
                    if self._match_display_string_view_pattern(
                        pattern, entry):
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
    def _find_first_file_name(directory_path):
        for directory_entry in sorted(os.listdir(directory_path)):
            if not directory_entry.startswith('.'):
                path = os.path.join(directory_path, directory_entry)
                if (os.path.isfile(path) and not '__init__.py' in path):
                    return directory_entry

    def _format_counted_check_messages(
        self,
        paths,
        identifier,
        participal,
        ):
        messages = []
        if paths:
            count = len(paths)
            identifier = stringtools.pluralize(identifier, count)
            message = '{} {} {}:'
            message = message.format(count, identifier, participal)
            messages.append(message)
            for path in paths:
                message = self._tab + path
                messages.append(message)
        return messages

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

    def _format_ratio_check_messages(
        self,
        found_paths,
        total_paths,
        identifier,
        participal='found',
        ):
        messages = []
        denominator = len(total_paths)
        numerator = len(found_paths)
        identifier = stringtools.pluralize(identifier, denominator)
        if denominator:
            message = '{} of {} {} {}:'
        else:
            message = '{} of {} {} {}.'
        message = message.format(
            numerator, denominator, identifier, participal)
        messages.append(message)
        for path in sorted(found_paths):
            message = self._tab + path
            messages.append(message)
        return messages

    def _get_added_asset_paths(self, path):
        paths = []
        git_status_lines = self._get_git_status_lines(path)
        for line in git_status_lines:
            line = str(line)
            if line.startswith('A'):
                path = line.strip('A')
                path = path.strip()
                root_directory = self._get_repository_root_directory(path)
                path = os.path.join(root_directory, path)
                paths.append(path)
        return paths

    def _get_commands(self):
        result = []
        for name in dir(self):
            if name.startswith('_'):
                continue
            command = getattr(self, name)
            if not inspect.ismethod(command):
                continue
            result.append(command)
        return result

    @staticmethod
    def _get_current_directory_token(session, directory_name):
        assert isinstance(directory_name, str), repr(directory_name)
        assert os.path.sep not in directory_name, repr(directory_name)
        score_directory = session.current_score_directory
        if score_directory is not None:
            directory = os.path.join(
                score_directory,
                directory_name,
                )
            directory = os.path.abspath(directory)
            return directory
        else:
            return directory_name

    @classmethod
    def _get_directory_wranglers(class_, session, path):
        wranglers = []
        directory_names = class_._list_directory_names(path)
        for directory_name in directory_names:
            wrangler = session._get_wrangler(directory_name)
            if wrangler is not None:
                wranglers.append(wrangler)
        return wranglers

    def _get_file_path_ending_with(self, directory, string):
        for file_name in self._list_directory(directory):
            if file_name.endswith(string):
                file_path = os.path.join(directory, file_name)
                return file_path

    def _get_name_metadatum(self, metadata_py_path):
        name = self._get_metadatum(metadata_py_path, 'name')
        if not name:
            parts = metadata_py_path.split(os.path.sep)
            directory_name = parts[-2]
            name = directory_name.replace('_', ' ')
        return name

    def _get_git_status_lines(self, directory):
        command = 'git status --porcelain {}'
        command = command.format(directory)
        with systemtools.TemporaryDirectoryChange(directory=directory):
            process = self._io_manager.make_subprocess(command)
        stdout_lines = self._io_manager._read_from_pipe(process.stdout)
        stdout_lines = stdout_lines.splitlines()
        return stdout_lines

    def _get_metadata(self, metadata_py_path):
        if not metadata_py_path.endswith('__metadata__.py'):
            metadata_py_path = os.path.join(
                metadata_py_path,
                '__metadata__.py',
                )
        metadata = None
        if os.path.isfile(metadata_py_path):
            with open(metadata_py_path, 'r') as file_pointer:
                file_contents_string = file_pointer.read()
            try:
                result = self._io_manager.execute_string(
                    file_contents_string,
                    attribute_names=('metadata',),
                    )
                metadata = result[0]
            except SyntaxError:
                message = 'can not interpret metadata py: {!r}.'
                message = message.format(metadata_py_path)
                self._io_manager._display(message)
        metadata = metadata or datastructuretools.TypedOrderedDict()
        return metadata

    def _get_metadatum(
        self,
        metadata_py_path,
        metadatum_name,
        ):
        metadata = self._get_metadata(metadata_py_path)
        return metadata.get(metadatum_name)

    def _get_modified_asset_paths(self, path):
        paths = []
        git_status_lines = self._get_git_status_lines(path)
        for line in git_status_lines:
            line = str(line)
            if line.startswith(('M', ' M')):
                path = line.strip('M ')
                path = path.strip()
                root_directory = self._get_repository_root_directory(path)
                path = os.path.join(root_directory, path)
                paths.append(path)
        return paths

    @staticmethod
    def _get_outer_score_package_path(path):
        if path.startswith(configuration.composer_scores_directory):
            return os.path.join(
                configuration.composer_scores_directory,
                os.path.basename(path),
                )
        else:
            return os.path.join(
                configuration.abjad_ide_example_scores_directory,
                os.path.basename(path),
                )

    @staticmethod
    def _get_previous_segment_manager(session, path):
        wrangler = session._abjad_ide._segment_package_wrangler
        managers = wrangler._list_visible_asset_managers()
        for i, manager in enumerate(managers):
            if manager._path == path:
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

    def _get_repository_root_directory(self, path):
        command = 'git rev-parse --show-toplevel'
        with systemtools.TemporaryDirectoryChange(directory=path):
            process = self._io_manager.make_subprocess(command)
        line = self._io_manager._read_one_line_from_pipe(process.stdout)
        return line

    def _get_score_initializer_file_lines(self, missing_file):
        lines = []
        lines.append(self._unicode_directive)
        if 'materials' in missing_file or 'makers' in missing_file:
            lines.append('from abjad.tools import systemtools')
            lines.append('')
            line = 'systemtools.ImportManager.import_material_packages('
            lines.append(line)
            lines.append('    __path__[0],')
            lines.append('    globals(),')
            lines.append('    )')
        elif 'segments' in missing_file:
            pass
        else:
            lines.append('import makers')
            lines.append('import materials')
            lines.append('import segments')
        return lines

    @staticmethod
    def _get_score_package_directory_name(path):
        line = path
        path = configuration.abjad_ide_example_scores_directory
        line = line.replace(path, '')
        path = configuration.composer_scores_directory
        line = line.replace(path, '')
        line = line.lstrip(os.path.sep)
        return line

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

    def _get_title_metadatum(
        self,
        metadata_py_path, 
        year=True,
        ):
        if year and self._get_metadatum(metadata_py_path, 'year'):
            result = '{} ({})'
            result = result.format(
                self._get_title_metadatum(metadata_py_path, year=False),
                self._get_metadatum(metadata_py_path, 'year')
                )
            return result
        else:
            result = self._get_metadatum(metadata_py_path, 'title')
            result = result or '(untitled score)'
            return result

    def _get_unadded_asset_paths(self, path):
        paths = []
        root_directory = self._get_repository_root_directory(path)
        git_status_lines = self._get_git_status_lines(path)
        for line in git_status_lines:
            line = str(line)
            if line.startswith('?'):
                path = line.strip('?')
                path = path.strip()
                path = os.path.join(root_directory, path)
                paths.append(path)
        return paths

    @staticmethod
    def _get_views_metadata_py_path(session):
        path = configuration.abjad_ide_views_directory
        manager = session._io_manager._make_package_manager(path)
        return os.path.join(manager._path, '__metadata__.py')

    @staticmethod
    def _get_views_package_manager(io_manager):
        path = configuration.abjad_ide_views_directory
        return io_manager._make_package_manager(path)

    @staticmethod
    def _get_views_py_path(directory_token):
        if os.path.sep in directory_token:
            return os.path.join(directory_token, '__views__.py')
        else:
            directory_path = configuration.abjad_ide_views_directory
            file_name = '__all_{}_directories_views__.py'
            file_name = file_name.format(directory_token)
            return os.path.join(
                configuration.abjad_ide_views_directory,
                file_name,
                )

    def _git_add(self, path, dry_run=False):
        change = systemtools.TemporaryDirectoryChange(directory=path)
        with change:
            inputs = self._get_unadded_asset_paths(path)
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
            if io_manager._is_backtracking or not result:
                return
            command = 'git add -A {}'
            command = command.format(path)
            assert isinstance(command, str)
            self._io_manager.run_command(command)

    def _git_commit(self, path, commit_message=None):
        change = systemtools.TemporaryDirectoryChange(directory=path)
        with change:
            self._io_manager._session._attempted_to_commit = True
            if self._io_manager._session.is_repository_test:
                return
            if commit_message is None:
                getter = self._io_manager._make_getter()
                getter.append_string('commit message')
                commit_message = getter._run()
                if self._io_manager._session.is_backtracking:
                    return
                if commit_message is None:
                    return
                message = 'commit message will be: "{}"'
                message = message.format(commit_message)
                self._io_manager._display(message)
                result = self._io_manager._confirm()
                if io_manager._is_backtracking or not result:
                    return
            message = self._get_score_package_directory_name(path)
            message = message + ' ...'
            command = 'git commit -m "{}" {}; git push'
            command = command.format(commit_message, self._path)
            self._io_manager.run_command(command, capitalize=False)

    def _git_revert(self, path):
        change = systemtools.TemporaryDirectoryChange(directory=path)
        with change:
            self._io_manager._session._attempted_to_revert = True
            if self._io_manager._session.is_repository_test:
                return
            paths = []
            paths.extend(self._get_added_asset_paths(path))
            paths.extend(self._get_modified_asset_paths(path))
            messages = []
            messages.append('will revert ...')
            for path in paths:
                messages.append(self._tab + path)
            self._io_manager._display(messages)
            result = self._io_manager._confirm()
            if self._io_manager._is_backtracking or not result:
                return
            commands = []
            for path in paths:
                command = 'git checkout {}'.format(path)
                commands.append(command)
            command = ' && '.join(commands)
            with systemtools.TemporaryDirectoryChange(directory=path):
                self._io_manager.spawn_subprocess(command)

    def _git_status(self, path):
        change = systemtools.TemporaryDirectoryChange(directory=path)
        with change:
            command = 'git status {}'.format(path)
            messages = []
            self._io_manager._session._attempted_display_status = True
            message = 'Repository status for {} ...'
            message = message.format(path)
            messages.append(message)
            with systemtools.TemporaryDirectoryChange(directory=path):
                process = self._io_manager.make_subprocess(command)
            path_ = path + os.path.sep
            clean_lines = []
            stdout_lines = self._io_manager._read_from_pipe(process.stdout)
            for line in stdout_lines.splitlines():
                line = str(line)
                clean_line = line.strip()
                clean_line = clean_line.replace(path_, '')
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

    def _git_update(self, path, messages_only=False):
        messages = []
        change = systemtools.TemporaryDirectoryChange(directory=path)
        with change:
            self._io_manager._session._attempted_to_update = True
            if self._io_manager._session.is_repository_test:
                return messages
            root_directory = self._get_repository_root_directory(path)
            command = 'git pull {}'
            command = command.format(root_directory)
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

    def _handle_input(self, result):
        assert isinstance(result, str), repr(result)
        if result == '<return>':
            return
        with self._session._io_manager._make_interaction(self._session):
            if result.startswith('!'):
                statement = result[1:]
                self._session._io_manager._invoke_shell(statement)
            elif result in self._command_name_to_command:
                command = self._command_name_to_command[result]
                arguments = []
                for argument_name in command.argument_names:
                    argument = getattr(self, argument_name)
                    arguments.append(argument)
                command(*arguments)
            elif (result.endswith('!') and 
                result[:-1] in self._command_name_to_command):
                result = result[:-1]
                with self._session._io_manager._make_interaction(
                    self._session,
                    confirm=False,
                    ):
                    self._command_name_to_command[result]()
            else:
                self._handle_numeric_user_input(result)

    def _handle_numeric_user_input(self, result):
        if os.path.isfile(result):
            self._session._io_manager.open_file(result)
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
                manager._run_package_manager()
        else:
            message = 'must be file or directory: {!r}.'
            message = message.format(result)
            raise Exception(message)

    # TODO: implement Command.redraw_immediately_after
    #       so enumeration can be derived introspectively
    @staticmethod
    def _handle_pending_redraw_directive(session, directive):
        if directive in ('b', 'h', 'q', 's', '?', ';'):
            session._pending_redraw = True

    # TODO: implement something on Command
    #       so enumeration can be derived introspectively
    @classmethod
    def _handle_wrangler_navigation_directive(class_, session, expr):
        dictionary = class_._navigation_command_name_to_directory_name
        directory_name = dictionary.get(expr)
        if directory_name is not None:
            session._navigation_target = directory_name

    @staticmethod
    def _is_directory_with_metadata_py(path):
        if os.path.isdir(path):
            for directory_entry in sorted(os.listdir(path)):
                if directory_entry == '__metadata__.py':
                    return True
        return False

    def _is_git_unknown(self, path):
        if path is None:
            return False
        if not os.path.exists(path):
            return False
        git_status_lines = self._get_git_status_lines(path)
        git_status_lines = git_status_lines or ['']
        first_line = git_status_lines[0]
        if first_line.startswith('?'):
            return True
        return False

    def _is_git_versioned(self, path):
        if not self._is_in_git_repository(path):
            return False
        git_status_lines = self._get_git_status_lines(path)
        git_status_lines = git_status_lines or ['']
        first_line = git_status_lines[0]
        if first_line.startswith('?'):
            return False
        return True

    def _is_in_git_repository(self, path):
        if path is None:
            return False
        if not os.path.exists(path):
            return False
        git_status_lines = self._get_git_status_lines(path)
        git_status_lines = git_status_lines or ['']
        first_line = git_status_lines[0]
        if first_line.startswith('fatal:'):
            return False
        return True

    def _is_in_score_directory(self):
        if hasattr(self, '_path'):
            current_directory = self._path
        else:
            current_directory = self._get_current_directory(
                self._session,
                self._directory_name,
                )
        if current_directory is None:
            current_directory = configuration.composer_scores_directory
        current_directory = os.path.normpath(current_directory)
        current_directory_parts = current_directory.split(os.path.sep)
        grandparent_directory_parts = current_directory_parts[:-2]
        scores_directory = configuration.composer_scores_directory
        scores_directory_parts = scores_directory.split(os.path.sep)
        if grandparent_directory_parts == scores_directory_parts:
            return True
        scores_directory = configuration.abjad_ide_example_scores_directory
        scores_directory_parts = scores_directory.split(os.path.sep)
        if grandparent_directory_parts == scores_directory_parts:
            return True
        return False

    @staticmethod
    def _is_score_package_inner_path(path):
        if path.startswith(configuration.composer_scores_directory):
            storehouse = configuration.composer_scores_directory
        elif path.startswith(configuration.abjad_ide_example_scores_directory):
            storehouse = configuration.abjad_ide_example_scores_directory
        else:
            return False
        storehouse_parts_count = len(storehouse.split(os.path.sep))
        parts = path.split(os.path.sep)
        if len(parts) == storehouse_parts_count + 2:
            if parts[-1] == parts[-2]:
                return True
        return False

    @staticmethod
    def _is_score_package_outer_path(path):
        if path.startswith(configuration.composer_scores_directory):
            storehouse = configuration.composer_scores_directory
        elif path.startswith(configuration.abjad_ide_example_scores_directory):
            storehouse = configuration.abjad_ide_example_scores_directory
        else:
            return False
        storehouse_parts_count = len(storehouse.split(os.path.sep))
        parts = path.split(os.path.sep)
        if len(parts) == storehouse_parts_count + 1:
            return True
        return False

    def _is_up_to_date(self, path):
        git_status_lines = self._get_git_status_lines(path)
        git_status_lines = git_status_lines or ['']
        first_line = git_status_lines[0]
        return first_line == ''

    @staticmethod
    def _is_valid_directory_entry(directory_entry):
        if directory_entry[0].isalpha():
            if not directory_entry.endswith('.pyc'):
                return True
        return False

    def _list_asset_paths(
        self,
        directory_name,
        directory_entry_predicate,
        example_score_packages=True,
        composer_score_packages=True,
        valid_only=True,
        ):
        result = []
        directories = self._list_storehouses(
            directory_name,
            example_score_packages=example_score_packages,
            composer_score_packages=composer_score_packages,
            )
        for directory in directories:
            if not directory:
                continue
            if not os.path.exists(directory):
                continue
            directory_entries = sorted(os.listdir(directory))
            for directory_entry in directory_entries:
                if valid_only:
                    if not directory_entry_predicate(directory_entry):
                        continue
                path = os.path.join(directory, directory_entry)
                if directory_name == 'scores':
                    path = os.path.join(path, directory_entry)
                result.append(path)
        return result

    @staticmethod
    def _list_directories_with_metadata_pys(path):
        paths = []
        for directory, subdirectory_names, file_names in os.walk(path):
            if Controller._is_directory_with_metadata_py(directory):
                if directory not in paths:
                    paths.append(directory)
            for subdirectory_name in subdirectory_names:
                path = os.path.join(directory, subdirectory_name)
                if Controller._is_directory_with_metadata_py(path):
                    if path not in paths:
                        paths.append(path)
        return paths

    @staticmethod
    def _list_directory(
        path,
        public_entries_only=False,
        smart_sort=False,
        ):
        entries = []
        if not os.path.exists(path):
            return entries
        if public_entries_only:
            for entry in sorted(os.listdir(path)):
                if entry == '__pycache__':
                    continue
                if entry[0].isalpha():
                    if not entry.endswith('.pyc'):
                        if not entry in ('test',):
                            entries.append(entry)
        else:
            for entry in sorted(os.listdir(path)):
                if entry == '__pycache__':
                    continue
                if not entry.startswith('.'):
                    if not entry.endswith('.pyc'):
                        entries.append(entry)
        if not smart_sort:
            return entries
        files, directories = [], []
        for entry in entries:
            path = os.path.join(path, entry)
            if os.path.isdir(path):
                directories.append(entry + '/')
            else:
                files.append(entry)
        result = files + directories
        return result

    @staticmethod
    def _list_directory_names(path):
        directory_names = []
        for entry in os.listdir(path):
            path_ = os.path.join(path, entry)
            if os.path.isdir(path_):
                if not entry == '__pycache__' :
                    directory_names.append(entry)
        return directory_names

    @staticmethod
    def _list_score_directories(
        example_score_packages=False,
        composer_score_packages=False,
        ):
        result = []
        scores_directories = []
        if example_score_packages:
            scores_directories.append(
                configuration.abjad_ide_example_scores_directory)
        if composer_score_packages:
            scores_directories.append(configuration.composer_scores_directory)
        for scores_directory in scores_directories:
            directory_entries = sorted(os.listdir(scores_directory))
            for directory_entry in directory_entries:
                if not directory_entry[0].isalpha():
                    continue
                path = os.path.join(
                    scores_directory,
                    directory_entry,
                    )
                init_path = os.path.join(path, '__init__.py')
                if not os.path.exists(init_path):
                    path = os.path.join(path, directory_entry)
                    init_path = os.path.join(path, '__init__.py')
                    if not os.path.exists(init_path):
                        continue
                result.append(path)
        return result

    def _list_storehouses(
        self,
        directory_name,
        example_score_packages=True,
        composer_score_packages=True,
        ):
        result = []
        if directory_name == 'scores':
            if example_score_packages:
                result.append(configuration.abjad_ide_example_scores_directory)
            if composer_score_packages:
                result.append(configuration.composer_scores_directory)
        else:
            score_directories = self._list_score_directories(
                example_score_packages=example_score_packages,
                composer_score_packages=composer_score_packages,
                )
            for score_directory in score_directories:
                path = os.path.join(
                    score_directory,
                    directory_name,
                    )
                result.append(path)
        return result

    def _list_visible_asset_paths(self):
        if hasattr(self, '_path'):
            return [self._path]
        else:
            entries = self._make_asset_menu_entries()
            paths = [_[-1] for _ in entries]
            return paths

    def _make_candidate_messages(
        self, 
        result, 
        candidate_path, 
        incumbent_path,
        ):
        messages = []
        messages.append('the files ...')
        messages.append(self._tab + candidate_path)
        messages.append(self._tab + incumbent_path)
        if result:
            messages.append('... compare the same.')
        else:
            messages.append('... compare differently.')
        return messages

    def _make_command_menu_sections(self, menu, menu_section_names=None):
        methods = []
        methods_ = self._get_commands()
        is_in_score = self._session.is_in_score
        if hasattr(self, '_path'):
            current_directory = self._path
        else:
            current_directory = self._get_current_directory(
                self._session,
                self._directory_name
                )
        if current_directory is None:
            current_directory = configuration.composer_scores_directory
        required_files = getattr(self, '_required_files', ())
        optional_files = getattr(self, '_optional_files', ())
        files = required_files + optional_files
        is_in_score_directory = self._is_in_score_directory()
        directory_name = os.path.basename(current_directory)
        parent_directory_name = current_directory.split(os.path.sep)[-2]
        is_home = False
        if current_directory == configuration.composer_scores_directory:
            if self._basic_breadcrumb == 'scores':
                is_home = True
        for method_ in methods_:
            if is_in_score and not method_.in_score:
                continue
            if not is_in_score and not method_.outside_score:
                continue
            if (method_.outside_score == 'home' and
                (not is_home and not is_in_score)):
                continue
            if ((method_.directories or method_.parent_directories) and
                directory_name not in method_.directories and
                parent_directory_name not in method_.parent_directories):
                continue
            if method_.file_ is not None and method_.file_ not in files:
                continue
            if method_.in_score_directory_only and not is_in_score_directory:
                continue
            methods.append(method_)
        method_groups = {}
        for method in methods:
            if menu_section_names is not None:
                if method.menu_section_name not in menu_section_names:
                    continue
            if method.section not in method_groups:
                method_groups[method.section] = []
            method_group = method_groups[method.section]
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

    def _make_main_menu(self):
        name = stringtools.to_space_delimited_lowercase(type(self).__name__)
        menu = self._session._io_manager._make_menu(name=name)
        self._make_asset_menu_section(menu)
        self._make_command_menu_sections(menu)
        return menu

    def _make_package(self, path, package_creation_callback=None):
        assert not os.path.exists(path)
        os.mkdir(path)
        with self._io_manager._silent():
            arguments = []
            for argument_name in self.check_package.argument_names:
                argument = getattr(self, argument_name)
                arguments.append(argument)
            self.check_package(
                *arguments,
                return_supply_messages=True,
                supply_missing=True
                )
        if package_creation_callback is not None:
            outer_path = self._get_outer_score_package_path(path)
            inner_path = os.path.join(outer_path, os.path.basename(path))
            new_path = package_creation_callback(
                inner_path,
                outer_path,
                )
            if new_path is not None:
                return new_path

    def _make_score_into_installable_package(
        self,
        inner_path,
        outer_path,
        ):
        old_path = outer_path
        temporary_path = os.path.join(
            os.path.dirname(outer_path),
            '_TEMPORARY_SCORE_PACKAGE',
            )
        shutil.move(old_path, temporary_path)
        shutil.move(temporary_path, inner_path)
        self._write_enclosing_artifacts(
            inner_path,
            outer_path,
            )
        return inner_path

    def _make_secondary_asset_menu_entries(self, directory_path):
        menu_entries = []
        for entry in os.listdir(directory_path):
            if entry in self._known_secondary_assets:
                path = os.path.join(directory_path, entry)
                menu_entry = (entry, None, None, path)
                menu_entries.append(menu_entry)
        return menu_entries

    @staticmethod
    def _match_path_view_pattern(pattern, entry):
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

    def _parse_paper_dimensions(self, session):
        manager = session.current_score_package_manager
        if manager is None:
            return
        string = self._get_metadatum(
            manager._path, 
            'paper_dimensions',
            )
        string = string or '8.5 x 11 in'
        parts = string.split()
        assert len(parts) == 4
        width, _, height, units = parts
        width = eval(width)
        height = eval(height)
        return width, height, units

    def _path_to_annotation(self, path):
        score_storehouses = (
            configuration.abjad_ide_example_scores_directory,
            configuration.composer_scores_directory,
            )
        if path.startswith(score_storehouses):
            score_directory = self._path_to_score_directory(path)
            metadata_py_path = os.path.join(score_directory, '__metadata__.py')
            metadata = self._get_metadata(metadata_py_path)
            if metadata:
                year = metadata.get('year')
                title = metadata.get('title')
                if self._is_score_package_inner_path(path) and year:
                    annotation = '{} ({})'.format(title, year)
                else:
                    annotation = str(title)
            else:
                package_name = os.path.basename(path)
                annotation = package_name
        elif path.startswith(configuration.abjad_root_directory):
            annotation = 'Abjad'
        else:
            annotation = None
        return annotation

    def _path_to_asset_menu_display_string(
        self, 
        path,
        allow_asset_name_underscores=False,
        ):
        asset_name = os.path.basename(path)
        if '_' in asset_name and not allow_asset_name_underscores:
            asset_name = stringtools.to_space_delimited_lowercase(asset_name)
        # TODO: replace with self._is_segment_package_path()
        if 'segments' in path:
            metadata_py_path = os.path.join(path, '__metadata__.py')
            segment_name = self._get_metadatum(
                metadata_py_path,
                'name',
                )
            asset_name = segment_name or asset_name
        if self._session.is_in_score:
            string = asset_name
        else:
            annotation = self._path_to_annotation(path)
            if self._is_score_package_inner_path(path):
                string = annotation
            else:
                string = '{} ({})'.format(asset_name, annotation)
        return string

    @staticmethod
    def _path_to_package(path):
        if path is None:
            return
        assert isinstance(path, str), repr(path)
        if path.endswith('.py'):
            path, file_extension = os.path.splitext(path)
        if path.startswith(configuration.abjad_ide_example_scores_directory):
            prefix = len(configuration.abjad_ide_example_scores_directory) + 1
        elif path.startswith(configuration.abjad_ide_directory):
            prefix = len(
                os.path.dirname(configuration.abjad_ide_directory)) + 1
        elif path.startswith(configuration.composer_scores_directory):
            prefix = len(configuration.composer_scores_directory) + 1
        else:
            message = 'can not change path to package: {!r}.'
            message = message.format(path)
            raise Exception(message)
        package = path[prefix:]
        if path.startswith(configuration.abjad_ide_example_scores_directory):
            # change red_example_score/red_example_score/materials/foo
            # to red_example_score/materials/foo
            parts = package.split(os.path.sep)
            parts = parts[1:]
            package = os.path.sep.join(parts)
        package = package.replace(os.path.sep, '.')
        return package

    @staticmethod
    def _path_to_score_directory(path):
        is_composer_score = False
        if path.startswith(configuration.composer_scores_directory):
            is_composer_score = True
            prefix = len(configuration.composer_scores_directory)
        elif path.startswith(configuration.abjad_ide_example_scores_directory):
            prefix = len(configuration.abjad_ide_example_scores_directory)
        else:
            return
        path_prefix = path[:prefix]
        path_suffix = path[prefix + 1:]
        score_name = path_suffix.split(os.path.sep)[0]
        score_path = os.path.join(path_prefix, score_name)
        score_path = os.path.join(score_path, score_name)
        return score_path

    @staticmethod
    def _path_to_storehouse(path):
        is_in_score = False
        if path.startswith(configuration.composer_scores_directory):
            is_in_score = True
            prefix = len(configuration.composer_scores_directory)
        elif path.startswith(configuration.abjad_ide_example_scores_directory):
            is_in_score = True
            prefix = len(configuration.abjad_ide_example_scores_directory)
        else:
            message = 'unidentifiable path: {!r}.'
            message = message.format(path)
            raise Exception(message)
        path_prefix = path[:prefix]
        remainder = path[prefix+1:]
        path_parts = remainder.split(os.path.sep)
        assert 1 <= len(path_parts)
        if is_in_score:
            path_parts = path_parts[:3]
        else:
            assert 1 <= len(path_parts)
            path_parts = path_parts[:1]
        storehouse = os.path.join(path_prefix, *path_parts)
        return storehouse

    def _read_view(self, directory_token):
        view_name = self._read_view_name(directory_token)
        if not view_name:
            return
        view_inventory = self._read_view_inventory(directory_token)
        if not view_inventory:
            return
        return view_inventory.get(view_name)

    def _read_view_inventory(self, directory_token):
        from ide.tools import idetools
        views_py_path = self._get_views_py_path(directory_token)
        result = self._io_manager.execute_file(
            path=views_py_path,
            attribute_names=('view_inventory',),
            )
        if result == 'corrupt':
            messages = []
            message = '{} __views.py__ is corrupt:'
            message = message.format(class_.__name__)
            messages.append(message)
            messages.append('')
            message = '    {}'.format(views_py_path)
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

    def _read_view_name(self, directory_token):
        if os.path.sep in directory_token:
            metadata_py_path = os.path.join(directory_token, '__metadata__.py')
            metadatum_name = 'view_name'
        else:
            metadata_py_path = configuration.abjad_ide_views_metadata_py_path
            metadatum_name = '{}_view_name'.format(directory_token)
        return self._get_metadatum(
            metadata_py_path,
            metadatum_name,
            )

    def _remove(self, path):
        # handle score packages correctly
        parts = path.split(os.path.sep)
        if parts[-2] == parts[-1]:
            parts = parts[:-1]
        path = os.path.sep.join(parts)
        message = '{} will be removed.'
        message = message.format(path)
        self._io_manager._display(message)
        getter = self._io_manager._make_getter()
        getter.append_string("type 'remove' to proceed")
        if self._io_manager._session.confirm:
            result = getter._run()
            if io_manager._is_backtracking or result is None:
                return
            if not result == 'remove':
                return
        if self._is_in_git_repository(path):
            if self._is_git_unknown(path):
                command = 'rm -rf {}'
            else:
                command = 'git rm --force -r {}'
        else:
            command = 'rm -rf {}'
        command = command.format(path)
        with systemtools.TemporaryDirectoryChange(directory=path):
            process = self._io_manager.make_subprocess(command)
        self._io_manager._read_one_line_from_pipe(process.stdout)
        return True

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

    def _rename(
        self,
        path,
        file_extension=None,
        file_name_callback=None,
        force_lowercase=True,
        ):
        base_name = os.path.basename(path)
        line = 'current name: {}'.format(base_name)
        self._io_manager._display(line)
        getter = self._io_manager._make_getter()
        getter.append_string('new name')
        new_package_name = getter._run()
        if self._io_manager._is_backtracking or new_package_name is None:
            return
        new_package_name = stringtools.strip_diacritics(new_package_name)
        if file_name_callback:
            new_package_name = file_name_callback(new_package_name)
        new_package_name = new_package_name.replace(' ', '_')
        if force_lowercase:
            new_package_name = new_package_name.lower()
        if file_extension and not new_package_name.endswith(file_extension):
            new_package_name = new_package_name + file_extension
        lines = []
        line = 'current name: {}'.format(base_name)
        lines.append(line)
        line = 'new name:     {}'.format(new_package_name)
        lines.append(line)
        self._io_manager._display(lines)
        result = self._io_manager._confirm()
        if self._io_manager._is_backtracking or not result:
            return
        new_path = os.path.join(
            os.path.dirname(path),
            new_package_name,
            )
        if os.path.exists(new_path):
            message = 'path already exists: {!r}.'
            message = message.format(new_path)
            self._io_manager._display(message)
            return
        shutil.move(path, new_path)
        self._io_manager._session._is_backtracking_locally = True
        return new_path

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

    @staticmethod
    def _sort_ordered_dictionary(dictionary):
        new_dictionary = type(dictionary)()
        for key in sorted(dictionary):
            new_dictionary[key] = dictionary[key]
        return new_dictionary
        
    def _supply_global_metadata_py(self):
        metadata_py_path = configuration.abjad_ide_views_metadata_py_path
        if not os.path.exists(metadata_py_path):
            metadata = class_._get_metadata(metadata_py_path)
            with self._io_manager._silent():
                self._write_metadata_py(metadata_py_path, metadata)

    def _supply_global_views_file(self, directory_name):
        from ide.tools import idetools
        views_py_path = self._get_views_py_path(directory_name)
        if not os.path.isfile(views_py_path):
            self._write_view_inventory(
                self._io_manager,
                directory_name,
                idetools.ViewInventory(),
                )

    def _test_add(self, path):
        assert self._is_up_to_date(path)
        path_1 = os.path.join(path, 'tmp_1.py')
        path_2 = os.path.join(path, 'tmp_2.py')
        with systemtools.FilesystemState(remove=[path_1, path_2]):
            with open(path_1, 'w') as file_pointer:
                file_pointer.write('')
            with open(path_2, 'w') as file_pointer:
                file_pointer.write('')
            assert os.path.exists(path_1)
            assert os.path.exists(path_2)
            assert not self._is_up_to_date(path)
            assert self._get_unadded_asset_paths(path) == [path_1, path_2]
            assert self._get_added_asset_paths(path) == []
            with self._io_manager._silent():
                self._git_add(path)
            assert self._get_unadded_asset_paths(path) == []
            assert self._get_added_asset_paths(path) == [path_1, path_2]
            with self._io_manager._silent():
                self._unadd_added_assets(path)
            assert self._get_unadded_asset_paths(path) == [path_1, path_2]
            assert self._get_added_asset_paths(path) == []
        assert self._is_up_to_date(path)
        return True

    def _test_revert(self, path):
        assert self._is_up_to_date(path)
        assert self._get_modified_asset_paths(path) == []
        file_name = self._find_first_file_name(path)
        if not file_name:
            return
        file_path = os.path.join(path, file_name)
        with systemtools.FilesystemState(keep=[file_path]):
            with open(file_path, 'a') as file_pointer:
                string = '# extra text appended during testing'
                file_pointer.write(string)
            assert not self._is_up_to_date(path)
            assert self._get_modified_asset_paths(path) == [file_path]
            with self._io_manager._silent():
                self._get_revert(path)
        assert self._get_modified_asset_paths(path) == []
        assert self._is_up_to_date(path)
        return True

    def _unadd_added_assets(self, path):
        paths = []
        paths.extend(self._get_added_asset_paths(path))
        paths.extend(self._get_modified_asset_paths(path))
        commands = []
        for path in paths:
            command = 'git reset -- {}'.format(path)
            commands.append(command)
        command = ' && '.join(commands)
        with systemtools.TemporaryDirectoryChange(directory=path):
            self._io_manager.spawn_subprocess(command)

    def _write_enclosing_artifacts(self, inner_path, outer_path):
        self._copy_boilerplate(
            'README.md',
            outer_path,
            )
        self._copy_boilerplate(
            'requirements.txt',
            outer_path,
            )
        self._copy_boilerplate(
            'setup.cfg',
            outer_path,
            )
        package_name = os.path.basename(outer_path)
        replacements = {
            'COMPOSER_EMAIL': configuration.composer_email,
            'COMPOSER_FULL_NAME': configuration.composer_full_name,
            'COMPOSER_GITHUB_USERNAME': configuration.composer_github_username,
            'PACKAGE_NAME': package_name,
            }
        self._copy_boilerplate(
            'setup.py',
            outer_path,
            replacements=replacements,
            )

    def _write_metadata_py(self, metadata_py_path, metadata):
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
        with open(metadata_py_path, 'w') as file_pointer:
            file_pointer.write(contents)

    def _write_view_inventory(
        self, 
        directory_token,
        view_inventory,
        ):
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
        views_py_path = self._get_views_py_path(directory_token)
        self._io_manager.write(views_py_path, contents)

    ### PUBLIC METHODS ###

    @Command(
        'dc', 
        argument_names=('_path',),
        file_='definition.py',
        outside_score=False,
        section='package', 
        )
    def check_definition_py(self, directory, dry_run=False):
        r'''Checks ``definition.py``.

        Displays interpreter errors.

        Returns none.
        '''
        definition_py_path = os.path.join(directory, 'definition.py')
        if not os.path.isfile(definition_py_path):
            message = 'file not found: {}.'
            message = message.format(definition_py_path)
            self._io_manager._display(message)
            return
        inputs, outputs = [], []
        if dry_run:
            inputs.append(definition_py_path)
            return inputs, outputs
        with self._io_manager._silent():
            stdout_lines, stderr_lines = self._io_manager.interpret_file(
                definition_py_path)
        if stderr_lines:
            messages = [definition_py_path + ' FAILED:']
            messages.extend('    ' + _ for _ in stderr_lines)
            self._io_manager._display(messages)
        else:
            message = '{} OK.'.format(definition_py_path)
            self._io_manager._display(message)

    @Command(
        'ck', 
        argument_names=(
            '_path',
            '_optional_directories',
            '_optional_files',
            '_required_directories',
            '_required_files',
            ),
        outside_score=False,
        file_='__init__.py',
        section='package', 
        )
    def check_package(
        self,
        directory,
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
        name = self._path_to_asset_menu_display_string(directory)
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

    @Command('?', section='system')
    def display_action_command_help(self):
        r'''Displays action commands.

        Returns none.
        '''
        if not self._session.is_in_confirmation_environment:
            self._session._display_command_help = 'action'

    @Command(';', section='display navigation')
    def display_navigation_command_help(self):
        r'''Displays navigation commands.

        Returns none.
        '''
        if not self._session.is_in_confirmation_environment:
            self._session._display_command_help = 'navigation'

    @Command('abb', section='global files', outside_score=False)
    def edit_abbreviations_file(self):
        r'''Edits abbreviations file.

        Returns none.
        '''
        path = self._session.current_abbreviations_file_path
        if not path or not os.path.isfile(path):
            with open(path, 'w') as file_pointer:
                file_pointer.write('')
        self._session._io_manager.edit(path)

    @Command(
        'de', 
        argument_names=('_path',),
        file_='definition.py', 
        outside_score=False,
        section='package', 
        )
    def edit_definition_py(self, directory):
        r'''Edits ``definition.py``.

        Returns none.
        '''
        definition_py_path = os.path.join(directory, 'definition.py')
        self._session._io_manager.edit(definition_py_path)

    @Command(
        'le', 
        argument_names=('_path',),
        description='edit __illustrate__.py', 
        file_='__illustrate__.py',
        outside_score=False,
        section='package',
        )
    def edit_illustrate_py(self, directory):
        r'''Edits ``__illustrate.py__``.

        Returns none.
        '''
        illustrate_py_path = os.path.join(directory, '__illustrate__.py')
        self._session._io_manager.edit(illustrate_py_path)

    @Command(
        'ie', 
        argument_names=('_path',),
        file_='illustration.ly', 
        outside_score=False, 
        section='package',
        )
    def edit_illustration_ly(self, directory):
        r'''Opens ``illustration.ly``.

        Returns none.
        '''
        illustration_ly_path = os.path.join(directory, 'illustration.ly')
        self._session._io_manager.open_file(illustration_ly_path)

    @Command('sty', section='global files', outside_score=False)
    def edit_score_stylesheet(self):
        r'''Edits score stylesheet.

        Returns none.
        '''
        path = self._session.current_stylesheet_path
        if not path or not os.path.isfile(path):
            with open(path, 'w') as file_pointer:
                file_pointer.write('')
        self._session._io_manager.edit(path)

    @Command(
        'gl', 
        argument_names=('_path',),
        description='generate __illustrate__.py', 
        file_='__illustrate__.py',
        outside_score=False,
        section='package',
        )
    def generate_illustrate_py(self, directory):
        r'''Generates ``__illustrate.py__``.

        Returns none.
        '''
        illustrate_py_path = os.path.join(directory, '__illustrate__.py')
        message = 'will generate {}.'
        message = message.format(illustrate_py_path)
        self._io_manager._display(message)
        result = self._io_manager._confirm()
        if self._io_manager._is_backtracking or not result:
            return
        lines = []
        lines.append(self._abjad_import_statement)
        line = 'from output import {}'
        line = line.format(os.path.basename(directory))
        lines.append(line)
        lines.append('')
        lines.append('')
        line = 'triple = scoretools.make_piano_score_from_leaves({})'
        line = line.format(os.path.basename(directory))
        lines.append(line)
        line = 'score, treble_staff, bass_staff = triple'
        lines.append(line)
        line = 'illustration = lilypondfiletools.'
        line += 'make_basic_lilypond_file(score)'
        lines.append(line)
        contents = '\n'.join(lines)
        with open(illustrate_py_path, 'w') as file_pointer:
            file_pointer.write(contents)
        message = 'generated {}.'
        message = message.format(illustrate_py_path)
        self._io_manager._display(message)

    @Command('b', description='back', section='back-home-quit')
    def go_back(self):
        r'''Goes back.

        Returns none.
        '''
        self._session._is_backtracking_locally = True
        self._session._display_command_help = None

    @Command('h', description='home', section='back-home-quit')
    def go_home(self):
        r'''Goes home.

        Returns none.
        '''
        self._session._is_navigating_home = False
        self._session._is_navigating_to_scores = True
        self._session._display_command_help = None

    @Command('uu', section='comparison', in_score=False)
    def go_to_all_build_directories(self):
        r'''Goes to all build directories.

        Returns none.
        '''
        self.go_home()
        self._session._navigation_target = 'build'

    @Command('dd', section='comparison', in_score=False)
    def go_to_all_distribution_directories(self):
        r'''Goes to all distribution directories.

        Returns none.
        '''
        self.go_home()
        self._session._navigation_target = 'distribution'

    @Command('ee', section='comparison', in_score=False)
    def go_to_all_etc_directories(self):
        r'''Goes to all etc directories.

        Returns none.
        '''
        self.go_home()
        self._session._navigation_target = 'etc'

    @Command('kk', section='comparison', in_score=False)
    def go_to_all_makers_directories(self):
        r'''Goes to all makers directories.

        Returns none.
        '''
        self.go_home()
        self._session._navigation_target = 'makers'

    @Command('mm', section='comparison', in_score=False)
    def go_to_all_materials_directories(self):
        r'''Goes to all materials directories.

        Returns none.
        '''
        self.go_home()
        self._session._navigation_target = 'materials'

    @Command('gg', section='comparison', in_score=False)
    def go_to_all_segments_directories(self):
        r'''Goes to all segments directories.

        Returns none.
        '''
        self.go_home()
        self._session._navigation_target = 'segments'

    @Command('yy', section='comparison', in_score=False)
    def go_to_all_stylesheets_directories(self):
        r'''Goes to all stylesheets directories.

        Returns none.
        '''
        self.go_home()
        self._session._navigation_target = 'stylesheets'

    @Command('tt', section='comparison', in_score=False)
    def go_to_all_test_directories(self):
        r'''Goes to all test directories.

        Returns none.
        '''
        self.go_home()
        self._session._navigation_target = 'test'

    @Command(
        '>',
        directories=('materials', 'segments'),
        parent_directories=('materials', 'segments'),
        section='sibling package',
        )
    def go_to_next_package(self):
        r'''Goes to next package.

        Returns none.
        '''
        self._session._is_navigating_to_next_asset = True
        self._session._display_command_help = None
        self._session._navigation_target = self._basic_breadcrumb.lower()

    @Command('>>', section='sibling score', outside_score='home')
    def go_to_next_score(self):
        r'''Goes to next score.

        Returns none.
        '''
        self._session._is_navigating_to_next_score = True
        self._session._is_navigating_to_scores = True
        self._session._display_command_help = None

    @Command(
        '<', 
        directories=('materials', 'segments'),
        parent_directories=('materials', 'segments'),
        section='sibling package',
        )
    def go_to_previous_package(self):
        r'''Goes to previous package.

        Returns none.
        '''
        self._session._is_navigating_to_previous_asset = True
        self._session._display_command_help = None
        self._session._navigation_target = self._basic_breadcrumb.lower()

    @Command('<<', section='sibling score', outside_score='home')
    def go_to_previous_score(self):
        r'''Goes to previous score.

        Returns none.
        '''
        self._session._is_navigating_to_previous_score = True
        self._session._is_navigating_to_scores = True
        self._session._display_command_help = None

    @Command('u', section='navigation', outside_score=False)
    def go_to_score_build_directory(self):
        r'''Goes to build files.

        Returns none.
        '''
        self._session._abjad_ide._build_file_wrangler._run_wrangler()

    @Command('s', section='navigation', outside_score=False)
    def go_to_score_directory(self):
        r'''Goes to current score.

        Returns none.
        '''
        if self._session.is_in_score:
            self._session._is_backtracking_to_score = True
            self._session._display_command_help = None
            
    @Command('d', section='navigation', outside_score=False)
    def go_to_score_distribution_directory(self):
        r'''Goes to distribution files.

        Returns none.
        '''
        self._session._abjad_ide._distribution_file_wrangler._run_wrangler()

    @Command('e', section='navigation', outside_score=False)
    def go_to_score_etc_directory(self):
        r'''Goes to etc files.

        Returns none.
        '''
        self._session._abjad_ide._etc_file_wrangler._run_wrangler()

    @Command('k', section='navigation', outside_score=False)
    def go_to_score_makers_directory(self):
        r'''Goes to maker files.

        Returns none.
        '''
        self._session._abjad_ide._maker_file_wrangler._run_wrangler()

    @Command('m', section='navigation', outside_score=False)
    def go_to_score_materials_directory(self):
        r'''Goes to material packages.

        Returns none.
        '''
        self._session._abjad_ide._material_package_wrangler._run_wrangler()

    @Command('g', section='navigation', outside_score=False)
    def go_to_score_segments_directory(self):
        r'''Goes to segment packages.

        Returns none.
        '''
        self._session._abjad_ide._segment_package_wrangler._run_wrangler()

    @Command('y', section='navigation', outside_score=False)
    def go_to_score_stylesheets_directory(self):
        r'''Goes to stylesheets.

        Returns none.
        '''
        self._session._abjad_ide._stylesheet_wrangler._run_wrangler()

    @Command('t', section='navigation', outside_score=False)
    def go_to_score_test_directory(self):
        r'''Goes to score test files.

        Returns none.
        '''
        self._session._abjad_ide._test_file_wrangler._run_wrangler()

    @Command(
        'i', 
        argument_names=('_path',),
        file_='definition.py',
        outside_score=False,
        parent_directories=('segments',),
        section='package', 
        )
    def illustrate_definition_py(self, directory, dry_run=False):
        r'''Illustrates ``definition.py``.

        Makes ``illustration.ly`` and ``illustration.pdf``.

        Returns none.
        '''
        definition_py_path = os.path.join(directory, 'definition.py')
        if not os.path.isfile(definition_py_path):
            message = 'File not found: {}.'
            message = message.format(definition_py_path)
            self._io_manager._display(message)
            return
        # TODO: remove session reference
        wrangler = self._session._abjad_ide._segment_package_wrangler
        wrangler._update_order_dependent_segment_metadata()
        boilerplate_path = os.path.join(
            configuration.abjad_ide_boilerplate_directory,
            '__illustrate_segment__.py',
            )
        illustrate_path = os.path.join(
            directory,
            '__illustrate_segment__.py',
            )
        candidate_ly_path = os.path.join(
            directory,
            'illustration.candidate.ly'
            )
        candidate_pdf_path = os.path.join(
            directory,
            'illustration.candidate.pdf'
            )
        temporary_files = (
            illustrate_path,
            candidate_ly_path,
            candidate_pdf_path,
            )
        for path in temporary_files:
            if os.path.exists(path):
                os.remove(path)
        illustration_ly_path = os.path.join(
            directory,
            'illustration.ly',
            )
        illustration_pdf_path = os.path.join(
            directory,
            'illustration.pdf',
            )
        inputs, outputs = [], []
        if dry_run:
            inputs.append(definition_py_path)
            outputs.append((illustration_ly_path, illustration_pdf_path))
            return inputs, outputs
        with systemtools.FilesystemState(remove=temporary_files):
            shutil.copyfile(boilerplate_path, illustrate_path)
            previous_segment_manager = self._get_previous_segment_manager(
                self._session,
                directory,
                )
            if previous_segment_manager is None:
                statement = 'previous_segment_metadata = None'
            else:
                # TODO: remove session reference
                score_name = self._session.current_score_directory
                score_name = os.path.basename(score_name)
                previous_segment_name = previous_segment_manager._path
                previous_segment_name = os.path.basename(previous_segment_name)
                statement = 'from {}.segments.{}.__metadata__'
                statement += ' import metadata as previous_segment_metadata'
                statement = statement.format(score_name, previous_segment_name)
            self._replace_in_file(
                illustrate_path,
                'PREVIOUS_SEGMENT_METADATA_IMPORT_STATEMENT',
                statement,
                )
            with self._io_manager._silent():
                start_time = time.time()
                result = self._io_manager.interpret_file(
                    illustrate_path,
                    strip=False,
                    )
                stop_time = time.time()
                total_time = stop_time - start_time
            stdout_lines, stderr_lines = result
            if stderr_lines:
                self._io_manager._display_errors(stderr_lines)
                return
            message = 'total time: {} seconds.'
            message = message.format(int(total_time))
            self._io_manager._display(message)
            if not os.path.exists(illustration_pdf_path):
                messages = []
                messages.append('Wrote ...')
                if os.path.exists(candidate_ly_path):
                    shutil.move(candidate_ly_path, illustration_ly_path)
                    messages.append(self._tab + illustration_ly_path)
                if os.path.exists(candidate_pdf_path):
                    shutil.move(candidate_pdf_path, illustration_pdf_path)
                    messages.append(self._tab + illustration_pdf_path)
                self._io_manager._display(messages)
            else:
                result = systemtools.TestManager.compare_files(
                candidate_pdf_path,
                illustration_pdf_path,
                )
                messages = self._make_candidate_messages(
                    result,
                    candidate_pdf_path,
                    illustration_pdf_path,
                    )
                self._io_manager._display(messages)
                if result:
                    message = 'preserved {}.'.format(illustration_pdf_path)
                    self._io_manager._display(message)
                    return
                else:
                    message = 'overwrite existing PDF with candidate PDF?'
                    result = self._io_manager._confirm(message=message)
                    if self._io_manager._is_backtracking or not result:
                        return
                    try:
                        shutil.move(candidate_ly_path, illustration_ly_path)
                    except IOError:
                        pass
                    try:
                        shutil.move(candidate_pdf_path, illustration_pdf_path)
                    except IOError:
                        pass

    @Command(
        'ii', 
        argument_names=('_path',),
        file_='illustration.ly',
        outside_score=False,
        section='package', 
        )
    def interpret_illustration_ly(self, directory, dry_run=False):
        r'''Interprets ``illustration.ly``.

        Makes ``illustration.pdf``.

        Returns pair. List of STDERR messages from LilyPond together
        with list of candidate messages.
        '''
        illustration_ly_path = os.path.join(directory, 'illustration.ly')
        illustration_pdf_path = os.path.join(directory, 'illustration.pdf')
        inputs, outputs = [], []
        if os.path.isfile(illustration_ly_path):
            inputs.append(illustration_ly_path)
            outputs.append((illustration_pdf_path,))
        if dry_run:
            return inputs, outputs
        if not os.path.isfile(illustration_ly_path):
            message = 'the file {} does not exist.'
            message = message.format(illustration_ly_path)
            self._io_manager._display(message)
            return [], []
        messages = self._format_messaging(inputs, outputs)
        self._io_manager._display(messages)
        result = self._io_manager._confirm()
        if self._io_manager._is_backtracking or not result:
            return [], []
        result = self._io_manager.run_lilypond(illustration_ly_path)
        subprocess_messages, candidate_messages = result
        return subprocess_messages, candidate_messages

    @Command('!', section='system')
    def invoke_shell(self):
        r'''Invokes shell.

        Returns none.
        '''
        statement = self._session._io_manager._handle_input(
            '$',
            include_chevron=False,
            include_newline=False,
            )
        statement = statement.strip()
        self._session._io_manager._invoke_shell(statement)

    @Command(
        'io', 
        argument_names=('_path',),
        file_='illustration.pdf',
        outside_score=False,
        section='package', 
        )
    def open_illustration_pdf(self, directory):
        r'''Opens ``illustration.pdf``.

        Returns none.
        '''
        illustration_pdf_path = os.path.join(directory, 'illustration.pdf')
        self._session._io_manager.open_file(illustration_pdf_path)

    @Command('log', section='global files')
    def open_lilypond_log(self):
        r'''Opens LilyPond log.

        Returns none.
        '''
        from abjad.tools import systemtools
        self._session._attempted_to_open_file = True
        if self._session.is_test:
            return
        systemtools.IOManager.open_last_log()

    @Command(
        'so', 
        argument_names=('_path',),
        in_score_directory_only=True,
        outside_score=False,
        section='package', 
        )
    def open_score_pdf(self, directory, dry_run=False):
        r'''Opens ``score.pdf``.

        Returns none.
        '''
        # TODO: remove session from _make_interaction() signature
        with self._io_manager._make_interaction(
            self._session,
            dry_run=dry_run,
            ):
            file_name = 'score.pdf'
            directory = os.path.join(directory, 'distribution')
            # TODO: remove call to _make_package_manager()
            manager = self._io_manager._make_package_manager(directory)
            path = manager._get_file_path_ending_with(manager._path, file_name)
            if not path:
                directory = os.path.join(self._path, 'build')
                # TODO: remove call to _make_package_manager()
                manager = self._io_manager._make_package_manager(directory)
                path = manager._get_file_path_ending_with(
                    manager._path, 
                    file_name,
                    )
            if dry_run:
                inputs, outputs = [], []
                if path:
                    inputs = [path]
                return inputs, outputs
            if path:
                self._io_manager.open_file(path)
            else:
                message = "no score.pdf file found"
                message += ' in either distribution/ or build/ directories.'
                self._io_manager._display(message)

    @Command('q', description='quit', section='back-home-quit')
    def quit_abjad_ide(self):
        r'''Quits Abjad IDE.

        Returns none.
        '''
        self._session._is_quitting = True
        self._session._display_command_help = None