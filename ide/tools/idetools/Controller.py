# -*- encoding: utf-8 -*-
from __future__ import print_function
import codecs
import inspect
import os
import shutil
import sys
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
        '_basic_breadcrumb',
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

    _unicode_directive = '# -*- encoding: utf-8 -*-'

    ### INITIALIZER ###

    def __init__(self, session=None):
        assert session is not None
        self._session = session
        self._basic_breadcrumb = None

    ### SPECIAL METHODS ###

    def __repr__(self):
        r'''Gets interpreter representation of asset controller.

        Returns string.
        '''
        return '{}()'.format(type(self).__name__)

    ### PRIVATE PROPERTIES ###

    @property
    def _command_name_to_method(self):
        result = {}
        methods = self._get_commands()
        for method in methods:
            result[method.command_name] = method
        return result

    ### PRIVATE METHODS ###

    @classmethod
    def _add_metadatum(
        class_,
        session,
        metadata_py_path,
        metadatum_name, 
        metadatum_value,
        ):
        assert ' ' not in metadatum_name, repr(metadatum_name)
        metadata = class_._get_metadata(
            session,
            metadata_py_path,
            )
        metadata[metadatum_name] = metadatum_value
        with session._io_manager._silent(session):
            class_._write_metadata_py(metadata_py_path, metadata)

    @classmethod
    def _copy_boilerplate(
        class_, 
        session,
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
                class_._replace_in_file(candidate_path, old, new)
            if not os.path.exists(destination_path):
                shutil.copyfile(candidate_path, destination_path)
                message = 'wrote {}.'.format(destination_path)
                messages.append(message)
            elif not candidacy:
                message = 'overwrite {}?'
                message = message.format(destination_path)
                result = session._io_manager._confirm(message)
                if session.is_backtracking or not result:
                    return False
                shutil.copyfile(candidate_path, destination_path)
                message = 'overwrote {}.'.format(destination_path)
                messages.append(message)
            elif systemtools.TestManager.compare_files(
                candidate_path, 
                destination_path,
                ):
                messages_ = class_._make_candidate_messages(
                    session,
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
            session._io_manager._display(messages)
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

    def _filter_asset_menu_entries_by_view(self, entries):
        view = self._read_view(
            self._session,
            self._directory_name,
            )
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
    def _find_first_file_name(directory_path):
        for directory_entry in sorted(os.listdir(directory_path)):
            if not directory_entry.startswith('.'):
                path = os.path.join(directory_path, directory_entry)
                if (os.path.isfile(path) and not '__init__.py' in path):
                    return directory_entry

    @staticmethod
    def _format_counted_check_messages(
        paths,
        identifier,
        participal,
        tab,
        ):
        messages = []
        if paths:
            count = len(paths)
            identifier = stringtools.pluralize(identifier, count)
            message = '{} {} {}:'
            message = message.format(count, identifier, participal)
            messages.append(message)
            for path in paths:
                message = tab + path
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

    @staticmethod
    def _format_ratio_check_messages(
        found_paths,
        total_paths,
        identifier,
        participal='found',
        tab=None,
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
            message = tab + path
            messages.append(message)
        return messages

    @classmethod
    def _get_added_asset_paths(class_, session, path):
        paths = []
        git_status_lines = class_._get_git_status_lines(
            session,
            path,
            )
        for line in git_status_lines:
            line = str(line)
            if line.startswith('A'):
                path = line.strip('A')
                path = path.strip()
                root_directory = class_._get_repository_root_directory(
                    session,
                    path,
                    )
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

    @classmethod
    def _get_directory_wranglers(class_, session, path):
        wranglers = []
        directory_names = class_._list_directory_names(path)
        for directory_name in directory_names:
            wrangler = session._get_wrangler(directory_name)
            if wrangler is not None:
                wranglers.append(wrangler)
        return wranglers

    @classmethod
    def _get_file_path_ending_with(class_, directory_path, string):
        for file_name in class_._list_directory(directory_path):
            if file_name.endswith(string):
                file_path = os.path.join(directory_path, file_name)
                return file_path

    @classmethod
    def _get_name_metadatum(class_, session, metadata_py_path):
        name = class_._get_metadatum(
            session,
            metadata_py_path,
            'name',
            )
        if not name:
            parts = metadata_py_path.split(os.path.sep)
            directory_name = parts[-2]
            name = directory_name.replace('_', ' ')
        return name

    @staticmethod
    def _get_git_status_lines(session, directory_path):
        command = 'git status --porcelain {}'
        command = command.format(directory_path)
        with systemtools.TemporaryDirectoryChange(directory=directory_path):
            process = session._io_manager.make_subprocess(command)
        stdout_lines = session._io_manager._read_from_pipe(process.stdout)
        stdout_lines = stdout_lines.splitlines()
        return stdout_lines

    @staticmethod
    def _get_metadata(session, metadata_py_path):
        metadata = None
        if os.path.isfile(metadata_py_path):
            with open(metadata_py_path, 'r') as file_pointer:
                file_contents_string = file_pointer.read()
            try:
                result = session._io_manager.execute_string(
                    file_contents_string,
                    attribute_names=('metadata',),
                    )
                metadata = result[0]
            except SyntaxError:
                message = 'can not interpret metadata py: {!r}.'
                message = message.format(metadata_py_path)
                session._io_manager._display(message)
        metadata = metadata or datastructuretools.TypedOrderedDict()
        return metadata

    @classmethod
    def _get_metadatum(
        class_,
        session,
        metadata_py_path,
        metadatum_name,
        ):
        metadata = class_._get_metadata(
            session,
            metadata_py_path,
            )
        return metadata.get(metadatum_name)

    @classmethod
    def _get_modified_asset_paths(class_, session, path):
        paths = []
        git_status_lines = class_._get_git_status_lines(
            session,
            path,
            )
        for line in git_status_lines:
            line = str(line)
            if line.startswith(('M', ' M')):
                path = line.strip('M ')
                path = path.strip()
                root_directory = class_._get_repository_root_directory(
                    session,
                    path,
                    )
                path = os.path.join(root_directory, path)
                paths.append(path)
        return paths

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

    @staticmethod
    def _get_repository_root_directory(session, path):
        command = 'git rev-parse --show-toplevel'
        with systemtools.TemporaryDirectoryChange(directory=path):
            process = session._io_manager.make_subprocess(command)
        line = session._io_manager._read_one_line_from_pipe(process.stdout)
        return line

    @classmethod
    def _get_score_initializer_file_lines(class_, missing_file):
        lines = []
        lines.append(class_._unicode_directive)
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

    @classmethod
    def _get_title_metadatum(
        class_, 
        session, 
        metadata_py_path, 
        year=True,
        ):
        if year and class_._get_metadatum(
            session,
            metadata_py_path,
            'year',
            ):
            result = '{} ({})'
            result = result.format(
                class_._get_title_metadatum(
                    session,
                    metadata_py_path,
                    year=False,
                    ),
                class_._get_metadatum(
                    session,
                    metadata_py_path,
                    'year',
                    )
                )
            return result
        else:
            result = class_._get_metadatum(
                session,
                metadata_py_path,
                'title',
                )
            result = result or '(untitled score)'
            return result

    @classmethod
    def _get_unadded_asset_paths(class_, session, path):
        paths = []
        root_directory = class_._get_repository_root_directory(
            session,
            path,
            )
        git_status_lines = class_._get_git_status_lines(
            session,
            path,
            )
        for line in git_status_lines:
            line = str(line)
            if line.startswith('?'):
                path = line.strip('?')
                path = path.strip()
                path = os.path.join(root_directory, path)
                paths.append(path)
        return paths

    @staticmethod
    def _get_views_package_manager(session):
        path = configuration.abjad_ide_wrangler_views_directory
        return session._io_manager._make_package_manager(path)

    @classmethod
    def _get_views_py_path(class_, session, directory_name):
        if session.is_in_score:
            directory_path = class_._get_current_directory(
                session,
                directory_name,
                )
            return os.path.join(directory_path, '__views__.py')
        else:
            directory_path = configuration.abjad_ide_wrangler_views_directory
            class_name = class_.__name__
            file_name = '__{}_views__.py'.format(class_name)
            return os.path.join(directory_path, file_name)

    @classmethod
    def _git_add(class_, session, path, dry_run=False):
        change = systemtools.TemporaryDirectoryChange(directory=path)
        with change:
            inputs = class_._get_unadded_asset_paths(session, path)
            outputs = []
            if dry_run:
                return inputs, outputs
            if not inputs:
                message = 'nothing to add.'
                session._io_manager._display(message)
                return
            messages = []
            messages.append('will add ...')
            for path in inputs:
                messages.append(session._io_manager._tab + path)
            session._io_manager._display(messages)
            result = session._io_manager._confirm()
            if session.is_backtracking or not result:
                return
            command = 'git add -A {}'
            command = command.format(path)
            assert isinstance(command, str)
            session._io_manager.run_command(command)

    @classmethod
    def _git_commit(class_, session, path, commit_message=None):
        change = systemtools.TemporaryDirectoryChange(directory=path)
        with change:
            session._attempted_to_commit = True
            if session.is_repository_test:
                return
            if commit_message is None:
                getter = session._io_manager._make_getter()
                getter.append_string('commit message')
                commit_message = getter._run()
                if session.is_backtracking or commit_message is None:
                    return
                message = 'commit message will be: "{}"'
                message = message.format(commit_message)
                session._io_manager._display(message)
                result = session._io_manager._confirm()
                if session.is_backtracking or not result:
                    return
            message = class_._get_score_package_directory_name(path)
            message = message + ' ...'
            command = 'git commit -m "{}" {}; git push'
            command = command.format(commit_message, self._path)
            session._io_manager.run_command(command, capitalize=False)

    @classmethod
    def _git_revert(class_, session, path):
        change = systemtools.TemporaryDirectoryChange(directory=path)
        with change:
            session._attempted_to_revert = True
            if session.is_repository_test:
                return
            paths = []
            paths.extend(class_._get_added_asset_paths(session, path))
            paths.extend(class_._get_modified_asset_paths(session, path))
            messages = []
            messages.append('will revert ...')
            for path in paths:
                messages.append(session._io_manager._tab + path)
            session._io_manager._display(messages)
            result = session._io_manager._confirm()
            if session.is_backtracking or not result:
                return
            commands = []
            for path in paths:
                command = 'git checkout {}'.format(path)
                commands.append(command)
            command = ' && '.join(commands)
            with systemtools.TemporaryDirectoryChange(directory=path):
                session._io_manager.spawn_subprocess(command)

    @classmethod
    def _git_status(class_, session, path):
        change = systemtools.TemporaryDirectoryChange(directory=path)
        with change:
            command = 'git status {}'.format(path)
            messages = []
            session._attempted_display_status = True
            message = 'Repository status for {} ...'
            message = message.format(path)
            messages.append(message)
            with systemtools.TemporaryDirectoryChange(directory=path):
                process = session._io_manager.make_subprocess(command)
            path_ = path + os.path.sep
            clean_lines = []
            stdout_lines = session._io_manager._read_from_pipe(process.stdout)
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
            session._io_manager._display(messages, capitalize=False)

    @classmethod
    def _git_update(class_, session, path, messages_only=False):
        messages = []
        change = systemtools.TemporaryDirectoryChange(directory=path)
        with change:
            session._attempted_to_update = True
            if session.is_repository_test:
                return messages
            root_directory = class_._get_repository_root_directory(
                session,
                path,
                )
            command = 'git pull {}'
            command = command.format(root_directory)
            messages = session._io_manager.run_command(
                command,
                messages_only=True,
                )
        if messages and messages[-1].startswith('At revision'):
            messages = messages[-1:]
        elif messages and 'Already up-to-date' in messages[-1]:
            messages = messages[-1:]
        if messages_only:
            return messages
        session._io_manager._display(messages)

    def _go_to_next_package(self):
        self._session._is_navigating_to_next_asset = True
        self._session._display_command_help = None
        self._set_is_navigating_to_sibling_asset()

    def _go_to_previous_package(self):
        self._session._is_navigating_to_previous_asset = True
        self._session._display_command_help = None
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
            tab = self._session._io_manager._tab
            messages_ = self._make_candidate_messages(
                self._session,
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
        self._session._io_manager._display(messages)

    def _handle_input(self, result):
        assert isinstance(result, str), repr(result)
        if result == '<return>':
            return
        with self._session._io_manager._make_interaction(self._session):
            if result.startswith('!'):
                statement = result[1:]
                self._session._io_manager._invoke_shell(statement)
            elif result in self._command_name_to_method:
                self._command_name_to_method[result]()
            elif (result.endswith('!') and 
                result[:-1] in self._command_name_to_method):
                result = result[:-1]
                with self._session._io_manager._make_interaction(
                    self._session,
                    confirm=False,
                    ):
                    self._command_name_to_method[result]()
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
                manager._run()
        else:
            message = 'must be file or directory: {!r}.'
            message = message.format(result)
            raise Exception(message)

    def _handle_pending_redraw_directive(self, directive):
        if directive in ('b', 'h', 'q', 's', '?', ';'):
            self._session._pending_redraw = True

    def _handle_wrangler_navigation_directive(self, expr):
        directory_name = \
            self._navigation_command_name_to_directory_name.get(expr)
        if directory_name is not None:
            self._session._navigation_target = directory_name

    @staticmethod
    def _is_directory_with_metadata_py(path):
        if os.path.isdir(path):
            for directory_entry in sorted(os.listdir(path)):
                if directory_entry == '__metadata__.py':
                    return True
        return False

    @classmethod
    def _is_git_unknown(class_, session, path):
        if path is None:
            return False
        if not os.path.exists(path):
            return False
        git_status_lines = class_._get_git_status_lines(
            session,
            path,
            )
        git_status_lines = git_status_lines or ['']
        first_line = git_status_lines[0]
        if first_line.startswith('?'):
            return True
        return False

    @classmethod
    def _is_git_versioned(class_, session, path):
        if not class_._is_in_git_repository(session, path):
            return False
        git_status_lines = class_._get_git_status_lines(
            session,
            path,
            )
        git_status_lines = git_status_lines or ['']
        first_line = git_status_lines[0]
        if first_line.startswith('?'):
            return False
        return True

    @classmethod
    def _is_in_git_repository(class_, session, path):
        if path is None:
            return False
        if not os.path.exists(path):
            return False
        git_status_lines = class_._get_git_status_lines(
            session,
            path,
            )
        git_status_lines = git_status_lines or ['']
        first_line = git_status_lines[0]
        if first_line.startswith('fatal:'):
            return False
        return True

    def _is_in_score_directory(self):
        if hasattr(self, '_directory_name'):
            current_directory = self._get_current_directory(
                self._session,
                self._directory_name,
                )
        else:
            current_directory = self._get_current_directory()
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

    @classmethod
    def _is_up_to_date(class_, session, path):
        git_status_lines = class_._get_git_status_lines(
            session,
            path,
            )
        git_status_lines = git_status_lines or ['']
        first_line = git_status_lines[0]
        return first_line == ''

    def _is_valid_directory_entry(self, directory_entry):
        if directory_entry[0].isalpha():
            if not directory_entry.endswith('.pyc'):
                return True
        return False

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
    def _make_candidate_messages(session, result, candidate_path, incumbent_path):
        messages = []
        tab = session._io_manager._tab
        messages.append('the files ...')
        messages.append(tab + candidate_path)
        messages.append(tab + incumbent_path)
        if result:
            messages.append('... compare the same.')
        else:
            messages.append('... compare differently.')
        return messages

    def _make_command_menu_sections(self, menu, menu_section_names=None):
        methods = []
        methods_ = self._get_commands()
        is_in_score = self._session.is_in_score
        if hasattr(self, '_directory_name'):
            current_directory = self._get_current_directory(
                self._session,
                self._directory_name
                )
        else:
            current_directory = self._get_current_directory()
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

    @classmethod
    def _make_score_into_installable_package(
        class_,
        session,
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
        class_._write_enclosing_artifacts(
            session,
            inner_path,
            outer_path,
            )
        return inner_path

    def _make_secondary_asset_menu_entries(self):
        menu_entries = []
        if not self._session.is_in_score:
            return menu_entries
        if hasattr(self, '_directory_name'):
            current_directory = self._get_current_directory(
                self._session,
                self._directory_name,
                )
        else:
            current_directory = self._get_current_directory()
        if not current_directory:
            return menu_entries
        for name in os.listdir(current_directory):
            if name in self._known_secondary_assets:
                path = os.path.join(current_directory, name)
                menu_entry = (name, None, None, path)
                menu_entries.append(menu_entry)
        return menu_entries

    def _open_file(self, path):
        if os.path.isfile(path):
            self._session._io_manager.open_file(path)
        else:
            message = 'can not find file: {}.'
            message = message.format(path)
            self._session._io_manager._display(message)

    @classmethod
    def _parse_paper_dimensions(class_, session):
        manager = session.current_score_package_manager
        if manager is None:
            return
        string = class_._get_metadatum(
            session,
            manager._metadata_py_path, 
            'paper_dimensions',
            )
        string = string or '8.5 x 11 in'
        parts = string.split()
        assert len(parts) == 4
        width, _, height, units = parts
        width = eval(width)
        height = eval(height)
        return width, height, units

    @classmethod
    def _path_to_annotation(class_, session, path, basic_breadcrumb):
        score_storehouses = (
            configuration.abjad_ide_example_scores_directory,
            configuration.composer_scores_directory,
            )
        if path.startswith(score_storehouses):
            score_path = class_._path_to_score_path(path)
            manager = session._io_manager._make_package_manager(
                path=score_path)
            metadata = manager._get_metadata(
                manager._session,
                manager._metadata_py_path,
                )
            if metadata:
                year = metadata.get('year')
                title = metadata.get('title')
                prototype = ('SCORES', 'scores')
                if basic_breadcrumb in prototype and year:
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

    @classmethod
    def _path_to_asset_menu_display_string(
        class_, 
        session, 
        path,
        basic_breadcrumb,
        allow_asset_name_underscores=False,
        ):
        asset_name = os.path.basename(path)
        if '_' in asset_name and not allow_asset_name_underscores:
            asset_name = stringtools.to_space_delimited_lowercase(asset_name)
        if 'segments' in path:
            manager = session._io_manager._make_package_manager(path=path)
            name = manager._get_metadatum(
                manager._session,
                manager._metadata_py_path,
                'name',
                )
            asset_name = name or asset_name
        if session.is_in_score:
            string = asset_name
        else:
            annotation = class_._path_to_annotation(
                session,
                path,
                basic_breadcrumb,
                )
            prototype = ('SCORES', 'scores')
            if basic_breadcrumb in prototype:
                string = annotation
            else:
                string = '{} ({})'.format(asset_name, annotation)
        return string

    @staticmethod
    def _path_to_score_path(path):
        is_user_score = False
        if path.startswith(configuration.composer_scores_directory):
            is_user_score = True
            prefix = len(configuration.composer_scores_directory)
        elif path.startswith(configuration.abjad_ide_example_scores_directory):
            prefix = len(configuration.abjad_ide_example_scores_directory)
        else:
            return
        path_prefix = path[:prefix]
        path_suffix = path[prefix + 1:]
        score_name = path_suffix.split(os.path.sep)[0]
        score_path = os.path.join(path_prefix, score_name)
        # test for installable python package structure
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

    @classmethod
    def _read_view(class_, session, directory_name):
        view_name = class_._read_view_name(
            session,
            directory_name,
            )
        if not view_name:
            return
        view_inventory = class_._read_view_inventory(
            session,
            directory_name,
            )
        if not view_inventory:
            return
        return view_inventory.get(view_name)

    @classmethod
    def _read_view_inventory(class_, session, directory_name):
        from ide.tools import idetools
        views_py_path = class_._get_views_py_path(
            session,
            directory_name,
            )
        if views_py_path is None:
            return
        if not os.path.exists(views_py_path):
            return
        result = session._io_manager.execute_file(
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
            session._io_manager._display(messages)
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

    @classmethod
    def _read_view_name(class_, session, directory_name):
        if session.is_in_score:
            manager = class_._get_current_package_manager(
                session,
                directory_name,
                )
            metadatum_name = 'view_name'
        else:
            manager = class_._get_views_package_manager(session)
            metadatum_name = '{}_view_name'.format(class_.__name__)
        if not manager:
            return
        return manager._get_metadatum(
            manager._session,
            manager._metadata_py_path, 
            metadatum_name,
            )

    @classmethod
    def _remove(class_, session, path):
        # handle score packages correctly
        parts = path.split(os.path.sep)
        if parts[-2] == parts[-1]:
            parts = parts[:-1]
        path = os.path.sep.join(parts)
        message = '{} will be removed.'
        message = message.format(path)
        session._io_manager._display(message)
        getter = session._io_manager._make_getter()
        getter.append_string("type 'remove' to proceed")
        if session.confirm:
            result = getter._run()
            if session.is_backtracking or result is None:
                return
            if not result == 'remove':
                return
        if class_._is_in_git_repository(session, path):
            if class_._is_git_unknown(session, path):
                command = 'rm -rf {}'
            else:
                command = 'git rm --force -r {}'
        else:
            command = 'rm -rf {}'
        command = command.format(path)
        with systemtools.TemporaryDirectoryChange(directory=path):
            process = session._io_manager.make_subprocess(command)
        session._io_manager._read_one_line_from_pipe(process.stdout)
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

    @staticmethod
    def _rename(
        session,
        path,
        file_extension=None,
        file_name_callback=None,
        force_lowercase=True,
        ):
        base_name = os.path.basename(path)
        line = 'current name: {}'.format(base_name)
        session._io_manager._display(line)
        getter = session._io_manager._make_getter()
        getter.append_string('new name')
        new_package_name = getter._run()
        if session.is_backtracking or new_package_name is None:
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
        session._io_manager._display(lines)
        result = session._io_manager._confirm()
        if session.is_backtracking or not result:
            return
        new_path = os.path.join(
            os.path.dirname(path),
            new_package_name,
            )
        if os.path.exists(new_path):
            message = 'path already exists: {!r}.'
            message = message.format(new_path)
            session._io_manager._display(message)
            return
        shutil.move(path, new_path)
        session._is_backtracking_locally = True
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

    def _set_is_navigating_to_sibling_asset(self):
        self._session._navigation_target = self._basic_breadcrumb.lower()

    @staticmethod
    def _sort_ordered_dictionary(dictionary):
        new_dictionary = type(dictionary)()
        for key in sorted(dictionary):
            new_dictionary[key] = dictionary[key]
        return new_dictionary
        
    @classmethod
    def _test_add(class_, session, path):
        assert class_._is_up_to_date(session, path)
        path_1 = os.path.join(path, 'tmp_1.py')
        path_2 = os.path.join(path, 'tmp_2.py')
        with systemtools.FilesystemState(remove=[path_1, path_2]):
            with open(path_1, 'w') as file_pointer:
                file_pointer.write('')
            with open(path_2, 'w') as file_pointer:
                file_pointer.write('')
            assert os.path.exists(path_1)
            assert os.path.exists(path_2)
            assert not class_._is_up_to_date(session, path)
            assert class_._get_unadded_asset_paths(
                session, path) == [path_1, path_2]
            assert class_._get_added_asset_paths(session, path) == []
            with session._io_manager._silent(session):
                class_._git_add(session, path)
            assert class_._get_unadded_asset_paths(session, path) == []
            assert class_._get_added_asset_paths(
                session, path) == [path_1, path_2]
            with session._io_manager._silent(session):
                class_._unadd_added_assets(session, path)
            assert class_._get_unadded_asset_paths(
                session, path) == [path_1, path_2]
            assert class_._get_added_asset_paths(session, path) == []
        assert class_._is_up_to_date(session, path)
        return True

    @classmethod
    def _test_revert(class_, session, path):
        assert class_._is_up_to_date(session, path)
        assert class_._get_modified_asset_paths(session, path) == []
        file_name = class_._find_first_file_name(path)
        if not file_name:
            return
        file_path = os.path.join(path, file_name)
        with systemtools.FilesystemState(keep=[file_path]):
            with open(file_path, 'a') as file_pointer:
                string = '# extra text appended during testing'
                file_pointer.write(string)
            assert not class_._is_up_to_date(session, path)
            assert class_._get_modified_asset_paths(
                session, path) == [file_path]
            with session._io_manager._silent(session):
                class_._get_revert(session, path)
        assert class_._get_modified_asset_paths(session, path) == []
        assert class_._is_up_to_date(session, path)
        return True

    @classmethod
    def _unadd_added_assets(class_, session, path):
        paths = []
        paths.extend(class_._get_added_asset_paths(session, path))
        paths.extend(class_._get_modified_asset_paths(session, path))
        commands = []
        for path in paths:
            command = 'git reset -- {}'.format(path)
            commands.append(command)
        command = ' && '.join(commands)
        with systemtools.TemporaryDirectoryChange(directory=path):
            session._io_manager.spawn_subprocess(command)

    @classmethod
    def _write_enclosing_artifacts(class_, session, inner_path, outer_path):
        class_._copy_boilerplate(
            session,
            'README.md',
            outer_path,
            )
        class_._copy_boilerplate(
            session,
            'requirements.txt',
            outer_path,
            )
        class_._copy_boilerplate(
            session,
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
        class_._copy_boilerplate(
            session,
            'setup.py',
            outer_path,
            replacements=replacements,
            )

    @classmethod
    def _write_metadata_py(class_, metadata_py_path, metadata):
        lines = []
        lines.append(class_._unicode_directive)
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

    @classmethod
    def _write_view_inventory(
        class_, 
        session, 
        directory_name, 
        view_inventory,
        ):
        lines = []
        lines.append(class_._unicode_directive)
        lines.append(class_._abjad_import_statement)
        lines.append('from ide.tools import idetools')
        lines.append('')
        lines.append('')
        view_inventory = class_._sort_ordered_dictionary(view_inventory)
        line = 'view_inventory={}'.format(format(view_inventory))
        lines.append(line)
        contents = '\n'.join(lines)
        views_py_path = class_._get_views_py_path(
            session,
            directory_name,
            )
        session._io_manager.write(views_py_path, contents)
        message = 'view inventory written to disk.'
        session._io_manager._display(message)

    ### PUBLIC METHODS ###

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
        self._go_to_next_package()

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
        self._go_to_previous_package()

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
        self._session._abjad_ide._build_file_wrangler._run()

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
        self._session._abjad_ide._distribution_file_wrangler._run()

    @Command('e', section='navigation', outside_score=False)
    def go_to_score_etc_directory(self):
        r'''Goes to etc files.

        Returns none.
        '''
        self._session._abjad_ide._etc_file_wrangler._run()

    @Command('k', section='navigation', outside_score=False)
    def go_to_score_makers_directory(self):
        r'''Goes to maker files.

        Returns none.
        '''
        self._session._abjad_ide._maker_file_wrangler._run()

    @Command('m', section='navigation', outside_score=False)
    def go_to_score_materials_directory(self):
        r'''Goes to material packages.

        Returns none.
        '''
        self._session._abjad_ide._material_package_wrangler._run()

    @Command('g', section='navigation', outside_score=False)
    def go_to_score_segments_directory(self):
        r'''Goes to segment packages.

        Returns none.
        '''
        self._session._abjad_ide._segment_package_wrangler._run()

    @Command('y', section='navigation', outside_score=False)
    def go_to_score_stylesheets_directory(self):
        r'''Goes to stylesheets.

        Returns none.
        '''
        self._session._abjad_ide._stylesheet_wrangler._run()

    @Command('t', section='navigation', outside_score=False)
    def go_to_score_test_directory(self):
        r'''Goes to score test files.

        Returns none.
        '''
        self._session._abjad_ide._test_file_wrangler._run()

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

    @Command('q', description='quit', section='back-home-quit')
    def quit_abjad_ide(self):
        r'''Quits Abjad IDE.

        Returns none.
        '''
        self._session._is_quitting = True
        self._session._display_command_help = None