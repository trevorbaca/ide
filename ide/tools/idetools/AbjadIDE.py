# -*- coding: utf-8 -*-
from __future__ import print_function
import codecs
import collections
import datetime
import glob
import inspect
import os
import shutil
import sys
import time
from abjad.tools import datastructuretools
from abjad.tools import lilypondfiletools
from abjad.tools import mathtools
from abjad.tools import sequencetools
from abjad.tools import stringtools
from abjad.tools import systemtools
from ide.tools.idetools.AbjadIDEConfiguration import AbjadIDEConfiguration
from ide.tools.idetools.Command import Command
configuration = AbjadIDEConfiguration()


class AbjadIDE(object):
    r'''Abjad IDE.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_configuration',
        '_io_manager',
        '_session',
        )

    _abjad_import_statement = 'from abjad import *'

    _secondary_names = (
        '__init__.py',
        '__illustrate__.py',
        '__metadata__.py',
        '__views__.py',
        '__abbreviations__.py',
        '.travis.yml',
        'README.md',
        'requirements.txt',
        'setup.cfg',
        'setup.py',
        )

    _tab = 4 * ' '

    _unicode_directive = '# -*- coding: utf-8 -*-'

    ### INITIALIZER ###

    def __init__(self, session=None, is_example=False, is_test=False):
        from ide.tools import idetools
        self._configuration = configuration
        if session is None:
            session = idetools.Session()
            session._is_example = is_example
            session._is_test = is_test
        self._session = session
        io_manager = idetools.IOManager(session=session)
        self._io_manager = io_manager

    ### SPECIAL METHODS ###

    def __repr__(self):
        r'''Gets interpreter representation of AbjadIDE.

        Returns string.
        '''
        return '{}()'.format(type(self).__name__)

    ### PRIVATE PROPERTIES ###

    @property
    def _command_name_to_command(self):
        result = {}
        methods = self._get_commands()
        for method in methods:
            result[method.command_name] = method
        return result

    ### PRIVATE METHODS ###

    def _add_metadatum(self, directory, metadatum_name, metadatum_value):
        assert os.path.isdir(directory)
        assert ' ' not in metadatum_name, repr(metadatum_name)
        metadata = self._get_metadata(directory)
        metadata[metadatum_name] = metadatum_value
        self._write_metadata_py(directory, metadata)

    def _call_latex_on_file(self, file_path):
        r'''Interprets TeX file.
        Calls ``pdflatex`` on file TWICE.
        Some LaTeX packages like ``tikz`` require two passes.
        '''
        if not os.path.isfile(file_path):
            message = 'can not find {} ...'
            message = message.format(self._trim_path(file_path))
            self._io_manager._display(message)
            return
        message = 'calling LaTeX on {} ...'
        message = message.format(self._trim_path(file_path))
        self._io_manager._display(message)
        input_directory = os.path.dirname(file_path)
        output_directory = input_directory
        basename = os.path.basename(file_path)
        input_file_name_stem, file_extension = os.path.splitext(basename)
        job_name = '{}.candidate'.format(input_file_name_stem)
        candidate_name = '{}.candidate.pdf'.format(input_file_name_stem)
        candidate_path = os.path.join(output_directory, candidate_name)
        destination_name = '{}.pdf'.format(input_file_name_stem)
        destination_path = os.path.join(output_directory, destination_name)
        command = 'date > {};'
        command += ' pdflatex --jobname={} -output-directory={} {}/{}.tex'
        command += ' >> {} 2>&1'
        command = command.format(
            configuration.latex_log_file_path,
            job_name,
            output_directory,
            input_directory,
            input_file_name_stem,
            configuration.latex_log_file_path,
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
            messages = self._handle_candidate(
                candidate_path,
                destination_path,
                )
            return messages

    def _clear_view(self, directory):
        assert os.path.isdir(directory), repr(directory)
        self._add_metadatum(directory, 'view_name', None)

    def _coerce_name(self, directory, name):
        dash_case_prototype = ('build', 'distribution', 'etc')
        package_prototype = ('scores', 'materials', 'segments')
        if self._is_score_directory(directory, 'scores'):
            name = self._to_package_name(name)
        elif self._is_score_directory(directory, dash_case_prototype):
            name = self._to_dash_case_file_name(name)
        elif self._is_score_directory(directory, 'makers'):
            name = self._to_classfile_name(name)
        elif self._is_score_directory(directory, package_prototype):
            name = self._to_package_name(name)
        elif self._is_score_directory(directory, 'stylesheets'):
            name = self._to_stylesheet_name(name)
        elif self._is_score_directory(directory, 'test'):
            name = self._to_test_file_name(name)
        else:
            raise ValueError(directory)
        return name

    def _collect_all_display_strings_in_score(self, directory):
        assert os.path.isdir(directory), repr(directory)
        strings, paths = [], []
        names = (
            'segments',
            'materials',
            'makers',
            'stylesheets',
            'etc',
            'distribution',
            'test',
            )
        for name in names:
            directory_ = self._to_score_directory(directory, name)
            paths_ = self._list_visible_paths(directory_)
            paths.extend(paths_)
            strings_ = [self._to_menu_string(_) for _ in paths_]
            strings.extend(strings_)
            file_name = '__abbreviations__.py'
            file_path = os.path.join(directory_, file_name)
            if os.path.isfile(file_path):
                paths.append(file_path)
                strings.append(file_name)
        assert len(strings) == len(paths), repr((len(strings), len(paths)))
        return strings, paths

    def _collect_similar_directories(self, directory, example_scores=False):
        assert os.path.isdir(directory), repr(directory)
        directories = []
        scores_directories = [configuration.composer_scores_directory]
        if example_scores:
            scores_directory = configuration.abjad_ide_example_scores_directory
            scores_directories.append(scores_directory)
        if self._is_score_directory(directory, 'scores'):
            return scores_directories
        score_directories = []
        for scores_directory in scores_directories:
            for name in os.listdir(scores_directory):
                if not name[0].isalpha():
                    continue
                score_directory = os.path.join(scores_directory, name)
                if not os.path.isdir(score_directory):
                    continue
                score_directories.append(score_directory)
        if self._is_score_directory(directory, 'outer'):
            return score_directories
        outer_score_directories = score_directories
        score_directories = []
        for outer_score_directory in outer_score_directories:
            base_name = os.path.basename(outer_score_directory)
            score_directory = os.path.join(
                outer_score_directory,
                base_name,
                )
            if not os.path.isdir(score_directory):
                continue
            score_directories.append(score_directory)
        if self._is_score_directory(directory, ('inner', 'score')):
            return score_directories
        if self._is_score_directory(directory, ('material', 'segment')):
            directories = []
            parent_directory = os.path.dirname(directory)
            parent_directories = self._collect_similar_directories(
                parent_directory,
                example_scores=example_scores,
                )
            for parent_directory in parent_directories:
                for name in os.listdir(parent_directory):
                    if not name[0].isalpha():
                        continue
                    directory_ = os.path.join(parent_directory, name)
                    if not os.path.isdir(directory_):
                        continue
                    directories.append(directory_)
            return directories
        base_name = os.path.basename(directory)
        for score_directory in score_directories:
            directory_ = os.path.join(score_directory, base_name)
            if os.path.isdir(directory_):
                directories.append(directory_)
        return directories

    def _copy_boilerplate(
        self,
        source_file_name,
        destination_directory,
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
            with open(candidate_path, 'r') as file_pointer:
                template = file_pointer.read()
            completed_template = template.format(**replacements)
            with open(candidate_path, 'w') as file_pointer:
                file_pointer.write(completed_template)
            if not os.path.exists(destination_path):
                shutil.copyfile(candidate_path, destination_path)
                message = 'writing {} ...'.format(destination_path)
                messages.append(message)
            elif systemtools.TestManager.compare_files(
                candidate_path,
                destination_path,
                ):
                message = 'preserving {} ...'
                message = message.format(self._trim_path(destination_path))
                messages.append(message)
            else:
                message = 'overwriting {} ...'
                message = message.format(self._trim_path(destination_path))
                messages.append(message)
                shutil.copyfile(candidate_path, destination_path)
            return messages

    def _filter_by_view(self, directory, entries):
        assert os.path.isdir(directory), repr(directory)
        view = self._read_view(directory)
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
    def _find_first_file_name(directory):
        for entry in sorted(os.listdir(directory)):
            if not entry.startswith('.'):
                path = os.path.join(directory, entry)
                if (os.path.isfile(path) and not '__init__.py' in path):
                    return entry

    def _format_messaging(self, inputs, outputs, verb='interpret'):
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
                    messages.append('{}{}'.format(
                        input_label, 
                        self._trim_path(path),
                        ))
        else:
            for inputs_, outputs_ in zip(inputs, outputs):
                if isinstance(inputs_, str):
                    inputs_ = [inputs_]
                assert isinstance(inputs_, (tuple, list)), repr(inputs_)
                for path_list in inputs_:
                    if isinstance(path_list, str):
                        path_list = [path_list]
                    for path in path_list:
                        messages.append('{}{}'.format(
                            input_label, 
                            self._trim_path(path),
                            ))
                for path_list in outputs_:
                    if isinstance(path_list, str):
                        path_list = [path_list]
                    for path in path_list:
                        messages.append('{}{}'.format(
                            output_label, 
                            self._trim_path(path),
                            ))
                messages.append('')
        return messages

    def _gather_segment_lys(self, directory):
        score_directory = self._to_score_directory(directory, 'inner')
        segments_directory = self._to_score_directory(directory, 'segments')
        build_directory = self._to_score_directory(directory, 'build')
        entries = sorted(os.listdir(segments_directory))
        source_ly_paths, target_ly_paths = [], []
        for entry in entries:
            segment_directory = os.path.join(segments_directory, entry)
            if not os.path.isdir(segment_directory):
                continue
            source_ly_path = os.path.join(segment_directory, 'illustration.ly')
            if not os.path.isfile(source_ly_path):
                continue
            score_package = os.path.basename(score_directory)
            score_name = score_package.replace('_', '-')
            entry = entry.replace('_', '-')
            target_ly_name = entry + '.ly'
            target_ly_path = os.path.join(build_directory, target_ly_name)
            source_ly_paths.append(source_ly_path)
            target_ly_paths.append(target_ly_path)
        if not os.path.exists(build_directory):
            os.mkdir(build_directory)
        pairs = zip(source_ly_paths, target_ly_paths)
        return pairs

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

    def _get_available_path(self, directory):
        asset_identifier = self._to_asset_identifier(directory)
        while True:
            default_prompt = 'enter {} name'
            default_prompt = default_prompt.format(asset_identifier)
            getter = self._io_manager._make_getter()
            getter.append_string(default_prompt)
            name = getter._run(io_manager=self._io_manager)
            if not name:
                return
            name = stringtools.strip_diacritics(name)
            words = stringtools.delimit_words(name)
            words = [_.lower() for _ in words]
            name = '_'.join(words)
            if not stringtools.is_snake_case_package_name(name):
                continue
            path = os.path.join(directory, name)
            if os.path.exists(path):
                line = 'path already exists: {!r}.'
                line = line.format(path)
                self._io_manager._display(line)
            else:
                return path

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

    def _get_file_path_ending_with(self, directory, string):
        if not os.path.isdir(directory):
            return
        for name in os.listdir(directory):
            if name.endswith(string):
                path = os.path.join(directory, name)
                if os.path.isfile(path):
                    return path

    def _get_git_status_lines(self, path):
        assert os.path.sep in path,repr(path)
        command = 'git status --porcelain {}'
        command = command.format(path)
        directory = self._to_score_directory(path, 'outer')
        with systemtools.TemporaryDirectoryChange(directory=directory):
            lines = self._io_manager.run_command(command)
        return lines

    def _get_metadata(self, directory):
        assert os.path.isdir(directory), repr(directory)
        metadata_py_path = os.path.join(
            directory,
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
                message = message.format(self._trim_path(metadata_py_path))
                self._io_manager._display(message)
        metadata = metadata or datastructuretools.TypedOrderedDict()
        return metadata

    def _get_metadatum(self, directory, metadatum_name, default=None):
        assert os.path.isdir(directory), repr(directory)
        metadata = self._get_metadata(directory)
        metadatum = metadata.get(metadatum_name)
        if not metadatum:
            metadatum = default
        return metadatum

    def _get_next_package(self, directory):
        assert os.path.isdir(directory), repr(directory)
        if self._is_score_directory(directory, 'material'):
            materials_directory = os.path.dirname(directory)
            paths = self._list_visible_paths(materials_directory)
            index = paths.index(directory)
            paths = datastructuretools.CyclicTuple(paths)
            path = paths[index+1]
        elif self._is_score_directory(directory, 'materials'):
            paths = self._list_visible_paths(directory)
            path = paths[0]
        elif self._is_score_directory(directory, 'segment'):
            segments_directory = os.path.dirname(directory)
            paths = self._list_visible_paths(segments_directory)
            index = paths.index(directory)
            paths = datastructuretools.CyclicTuple(paths)
            path = paths[index+1]
        elif self._is_score_directory(directory, 'segments'):
            paths = self._list_visible_paths(directory)
            path = paths[0]
        else:
            raise ValueError(directory)
        return path

    def _get_previous_package(self, directory):
        assert os.path.isdir(directory), repr(directory)
        if self._is_score_directory(directory, 'material'):
            materials_directory = os.path.dirname(directory)
            paths = self._list_visible_paths(materials_directory)
            index = paths.index(directory)
            paths = datastructuretools.CyclicTuple(paths)
            path = paths[index-1]
        elif self._is_score_directory(directory, 'materials'):
            paths = self._list_visible_paths(directory)
            path = paths[-1]
        elif self._is_score_directory(directory, 'segment'):
            segments_directory = os.path.dirname(directory)
            paths = self._list_visible_paths(segments_directory)
            index = paths.index(directory)
            paths = datastructuretools.CyclicTuple(paths)
            path = paths[index-1]
        elif self._is_score_directory(directory, 'segments'):
            paths = self._list_visible_paths(directory)
            path = paths[-1]
        else:
            raise ValueError(directory)
        return path

    def _get_previous_segment_directory(self, directory):
        segments_directory = self._to_score_directory(
            directory,
            'segments',
            )
        paths = self._list_visible_paths(segments_directory)
        for i, path in enumerate(paths):
            if path == directory:
                break
        else:
            message = 'can not find segment directory path.'
            raise Exception(message)
        current_path_index = i
        if current_path_index == 0:
            return
        previous_path_index = current_path_index - 1
        previous_path = paths[previous_path_index]
        return previous_path

    def _get_repository_root_directory(self, path):
        command = 'git rev-parse --show-toplevel'
        with systemtools.TemporaryDirectoryChange(directory=path):
            lines = self._io_manager.run_command(command)
            first_line = lines[0]
            return first_line

    def _get_segment_metadata(self, directory):
        assert self._is_score_directory(directory, 'segment'), repr(directory)
        previous_directory = self._get_previous_directory(directory)
        assert self._is_score_directory(previous_directory, 'segment')
        segment_metadata = self._get_metadata(directory)
        segments_directory = self._to_score_directory(directory, 'segments')
        paths = self._list_visible_paths(segments_directory)
        if directory == paths[0]:
            return segment_metadata
        previous_segment_metadata = self._get_metadata(previous_directory)
        return segment_metadata, previous_segment_metadata

    def _get_title_metadatum(self, score_directory, year=True):
        if year and self._get_metadatum(score_directory, 'year'):
            result = '{} ({})'
            result = result.format(
                self._get_title_metadatum(score_directory, year=False),
                self._get_metadatum(score_directory, 'year')
                )
            return result
        else:
            result = self._get_metadatum(score_directory, 'title')
            result = result or '(untitled score)'
            return result

    def _get_unadded_asset_paths(self, directory):
        assert os.path.isdir(directory), repr(directory)
        paths = []
        root_directory = self._get_repository_root_directory(directory)
        git_status_lines = self._get_git_status_lines(directory)
        for line in git_status_lines:
            line = str(line)
            if line.startswith('?'):
                path = line.strip('?')
                path = path.strip()
                path = os.path.join(root_directory, path)
                paths.append(path)
            elif line.startswith('M'):
                path = line.strip('M')
                path = path.strip()
                path = os.path.join(root_directory, path)
                paths.append(path)
        return paths

    def _git_add(self, directory, dry_run=False, interaction=True):
        assert os.path.isdir(directory), repr(directory)
        directory = self._to_score_directory(directory, 'outer')
        change = systemtools.TemporaryDirectoryChange(directory=directory)
        do_it = interaction and not dry_run
        interaction = self._io_manager._make_interaction(dry_run=not do_it)
        with change, interaction:
            inputs = self._get_unadded_asset_paths(directory)
            outputs = []
            nothing_message = '{} ... nothing to add.'
            nothing_message = nothing_message.format(directory)
            if dry_run:
                return inputs, outputs
            if not inputs:
                self._io_manager._display(nothing_message)
                return
            command = 'git add -A {}'
            for file_ in inputs:
                command = command.format(directory)
                self._io_manager.run_command(command)
            messages = []
            for file_ in inputs:
                message = '{} ... added.'
                message = message.format(self._trim_path(file_))
                messages.append(message)
            self._io_manager._display(messages, capitalize=False)

    def _handle_candidate(self, candidate_path, destination_path):
        messages = []
        if not os.path.exists(destination_path):
            message = 'writing {} ...'
            message = message.format(self._trim_path(destination_path))
            messages.append(message)
            shutil.copyfile(candidate_path, destination_path)
        elif systemtools.TestManager.compare_files(
            candidate_path,
            destination_path,
            ):
            message = 'preserving {} ...'
            message = message.format(self._trim_path(destination_path))
            messages.append(message)
        else:
            message = 'overwriting {} ...'
            message = message.format(self._trim_path(destination_path))
            messages.append(message)
            shutil.copyfile(candidate_path, destination_path)
        return messages

    def _handle_input(self, result):
        assert isinstance(result, (str, tuple)), repr(result)
        if result == '<return>':
            return
        package_prototype = ('inner', 'material', 'segment')
        if isinstance(result, tuple):
            assert len(result) == 1, repr(result)
            result = result[0]
            message = 'unknown command: {!r}.'
            message = message.format(result)
            self._io_manager._display([message, ''])
        elif result.startswith('!'):
            statement = result[1:]
            self._io_manager._invoke_shell(statement)
            self._io_manager._display('')
        elif result.startswith(('@', '%')):
            directory = self._session.current_directory
            prefix = result[0]
            body = result[1:]
            line_number = None
            if '+' in body:
                index = body.find('+')
                line_number = body[index+1:]
                if mathtools.is_integer_equivalent_expr(line_number):
                    line_number = int(line_number)
                else:
                    line_number = None
                body = body[:index]
            path = self._match_display_string_in_score(directory, body)
            if path:
                if prefix == '@':
                    if self._is_score_directory(path, ('material', 'segment')):
                        path = os.path.join(path, 'definition.py')
                    self._io_manager.open_file(path, line_number=line_number)
                elif prefix == '%':
                    self._manage_directory(path)
                else:
                    raise ValueError(prefix)
            else:
                message = 'matches no display string: {!r}.'
                message = message.format(result)
                self._io_manager._display([message, ''])
        elif result in self._command_name_to_command:
            command = self._command_name_to_command[result]
            if command.argument_name == 'current_directory':
                command(self._session.current_directory)
            else:
                command()
        elif (result.endswith('!') and
            result[:-1] in self._command_name_to_command):
            result = result[:-1]
            self._command_name_to_command[result]()
        elif os.path.isfile(result):
            self._io_manager.open_file(result)
        elif self._is_score_directory(result, package_prototype):
            self._manage_directory(result)
        elif self._is_score_directory(result):
            self._manage_directory(result)
        else:
            message = 'unknown command: {!r}.'
            message = message.format(result)
            self._io_manager._display([message, ''])

    def _has_pending_commit(self, directory):
        assert os.path.isdir(directory), repr(directory)
        command = 'git status {}'.format(directory)
        with systemtools.TemporaryDirectoryChange(directory=directory):
            lines = self._io_manager.run_command(command)
        path = directory + os.path.sep
        clean_lines = []
        for line in lines:
            line = str(line)
            clean_line = line.strip()
            clean_line = clean_line.replace(path, '')
            clean_lines.append(clean_line)
        for line in clean_lines:
            if 'Changes not staged for commit:' in line:
                return True
            if 'Changes to be committed:' in line:
                return True

    @staticmethod
    def _is_classfile_name(expr):
        if not isinstance(expr, str):
            return False
        file_name, file_extension = os.path.splitext(expr)
        if not stringtools.is_upper_camel_case(file_name):
            return False
        if not file_extension == '.py':
            return False
        return True

    @staticmethod
    def _is_dash_case_file_name(expr):
        if not isinstance(expr, str):
            return False
        if not expr == expr.lower():
            return False
        file_name, file_extension = os.path.splitext(expr)
        if not stringtools.is_dash_case(file_name):
            return False
        if not file_extension:
            return False
        return True

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

    @staticmethod
    def _is_lowercase_file_name(expr):
        if not isinstance(expr, str):
            return False
        if not expr == expr.lower():
            return False
        file_name, file_extension = os.path.splitext(expr)
        if not (stringtools.is_snake_case(file_name) or
            stringtools.is_dash_case(file_name)):
            return False
        if not file_extension in ('.py', '.ly', '.pdf'):
            return False
        return True

    @staticmethod
    def _is_module_file_name(expr):
        if not isinstance(expr, str):
            return False
        if not expr == expr.lower():
            return False
        file_name, file_extension = os.path.splitext(expr)
        if not stringtools.is_snake_case(file_name):
            return False
        if not file_extension == '.py':
            return False
        return True

    @staticmethod
    def _is_package_name(expr):
        if not isinstance(expr, str):
            return False
        if not expr == expr.lower():
            return False
        if os.path.sep in expr:
            return False
        if not stringtools.is_snake_case(expr):
            return False
        return True

    def _is_score_directory(self, directory, prototype=()):
        if not isinstance(directory, str):
            return False
        if not os.path.isdir(directory):
            return False
        if isinstance(prototype, str):
            prototype = (prototype,)
        if not prototype:
            scores_directory = configuration.composer_scores_directory
            if directory.startswith(scores_directory):
                return True
            scores_directory = configuration.abjad_ide_example_scores_directory
            if directory.startswith(scores_directory):
                return True
        assert all(isinstance(_, str) for _ in prototype)
        if 'scores'in prototype:
            if directory == configuration.composer_scores_directory:
                return True
            if directory == configuration.abjad_ide_example_scores_directory:
                return True
        scores_directory = self._to_score_directory(directory, 'scores')
        if 'outer' in prototype and scores_directory:
            scores_directory_parts_count = len(
                scores_directory.split(os.path.sep))
            parts = directory.split(os.path.sep)
            if len(parts) == scores_directory_parts_count + 1:
                return True
        if 'inner' in prototype and scores_directory:
            scores_directory_parts_count = len(
                scores_directory.split(os.path.sep))
            parts = directory.split(os.path.sep)
            if len(parts) == scores_directory_parts_count + 2:
                if parts[-1] == parts[-2]:
                    return True
        parent_directory = os.path.dirname(directory)
        if 'material' in prototype and scores_directory:
            scores_directory_parts_count = len(
                scores_directory.split(os.path.sep))
            parts = directory.split(os.path.sep)
            if len(parts) == scores_directory_parts_count + 4:
                if parts[-2] == 'materials':
                    return True
        if 'segment' in prototype and scores_directory:
            scores_directory_parts_count = len(
                scores_directory.split(os.path.sep))
            parts = directory.split(os.path.sep)
            if len(parts) == scores_directory_parts_count + 4:
                if parts[-2] == 'segments':
                    return True
        base_name = os.path.basename(directory)
        if base_name not in (
            'build',
            'distribution',
            'etc',
            'makers',
            'material',
            'materials',
            'score',
            'scores',
            'segment',
            'segments',
            'stylesheets',
            'test',
            ):
            return False
        if prototype is None or base_name in prototype:
            return True
        return False

    @staticmethod
    def _is_stylesheet_name(expr):
        if not isinstance(expr, str):
            return False
        if not expr == expr.lower():
            return False
        file_name, file_extension = os.path.splitext(expr)
        if not stringtools.is_dash_case(file_name):
            return False
        if not file_extension == '.ily':
            return False
        return True

    @staticmethod
    def _is_test_file_name(expr):
        if not isinstance(expr, str):
            return False
        if not expr.startswith('test_'):
            return False
        file_name, file_extension = os.path.splitext(expr)
        if not stringtools.is_snake_case(file_name):
            return False
        if not file_extension == '.py':
            return False
        return True

    def _is_up_to_date(self, path):
        git_status_lines = self._get_git_status_lines(path)
        git_status_lines = git_status_lines or ['']
        first_line = git_status_lines[0]
        return first_line == ''

    def _list_paths(self, directory, example_scores=True):
        assert os.path.isdir(directory), repr(directory)
        paths = []
        directories = self._collect_similar_directories(
            directory,
            example_scores=example_scores,
            )
        directory_ = directory
        for directory in directories:
            if not directory:
                continue
            if not os.path.exists(directory):
                continue
            name_predicate = self._to_name_predicate(directory)
            entries = sorted(os.listdir(directory))
            for entry in entries:
                if not name_predicate(entry):
                    continue
                path = os.path.join(directory, entry)
                if self._is_score_directory(directory, 'scores'):
                    path = os.path.join(path, entry)
                if not path.startswith(directory_):
                    continue
                paths.append(path)
        return paths

    def _list_secondary_paths(self, directory):
        assert os.path.isdir(directory), repr(directory)
        paths = []
        for name in os.listdir(directory):
            if name in sorted(self._secondary_names):
                path = os.path.join(directory, name)
                paths.append(path)
        return paths

    def _list_visible_paths(self, directory):
        assert os.path.isdir(directory), repr(directory)
        paths = self._list_paths(directory)
        strings = [self._to_menu_string(_) for _ in paths]
        entries = []
        pairs = list(zip(strings, paths))
        for string, path in pairs:
            entry = (string, None, None, path)
            entries.append(entry)
        entries = self._filter_by_view(directory, entries)
        if self._is_score_directory(directory, 'scores'):
            if self._session.is_test or self._session.is_example:
                entries = [_ for _ in entries if 'Example Score' in _[0]]
            else:
                entries = [_ for _ in entries if 'Example Score' not in _[0]]
        paths = [_[-1] for _ in entries]
        return paths

    def _make_candidate_messages(self, result, candidate_path, incumbent_path):
        messages = []
        messages.append('the files ...')
        candidate_path = self._trim_path(candidate_path)
        messages.append(self._tab + candidate_path)
        incumbent_path = self._trim_path(incumbent_path)
        messages.append(self._tab + incumbent_path)
        if result:
            messages.append('... compare the same.')
        else:
            messages.append('... compare differently.')
        return messages

    def _make_command_menu_sections(self, directory, menu):
        assert os.path.isdir(directory), repr(directory)
        commands = []
        for command in self._get_commands():
            if not self._is_score_directory(directory, command.directories):
                continue
            if (command.forbidden_directories and
                self._is_score_directory(
                directory, command.forbidden_directories)):
                continue
            commands.append(command)
        command_groups = {}
        for command in commands:
            if command.section not in command_groups:
                command_groups[command.section] = []
            command_group = command_groups[command.section]
            command_group.append(command)
        for menu_section_name in command_groups:
            command_group = command_groups[menu_section_name]
            is_hidden = not menu_section_name == 'basic'
            menu.make_command_section(
                is_hidden=is_hidden,
                commands=command_group,
                name=menu_section_name,
                )

    def _make_file(self, directory):
        assert os.path.isdir(directory), repr(directory)
        getter = self._io_manager._make_getter()
        getter.append_string('file name')
        file_name = getter._run(io_manager=self._io_manager)
        if file_name is None:
            return
        file_name = self._coerce_name(directory, file_name)
        name_predicate = self._to_name_predicate(directory)
        if not name_predicate(file_name):
            message = 'invalid file name: {!r}.'
            message = message.format(self._trim_path(file_name))
            self._io_manager._display(message)
            self._io_manager._acknowledge()
            return
        file_path = os.path.join(directory, file_name)
        if self._is_score_directory(directory, 'makers'):
            source_file = os.path.join(
                configuration.abjad_ide_boilerplate_directory,
                'Maker.py',
                )
            shutil.copyfile(source_file, file_path)
            with open(file_path, 'r') as file_pointer:
                template = file_pointer.read()
            class_name, _ = os.path.splitext(file_name)
            completed_template = template.format(class_name=class_name)
            with open(file_path, 'w') as file_pointer:
                file_pointer.write(completed_template)
        else:
            contents = ''
            file_name, file_extension = os.path.splitext(file_name)
            if file_extension == '.py':
                contents = self._unicode_directive
            self._io_manager.write(file_path, contents)
        self._io_manager.edit(file_path)

    def _make_main_menu(self, directory, explicit_header):
        assert os.path.isdir(directory), repr(directory)
        assert isinstance(explicit_header, str), repr(explicit_header)
        name = stringtools.to_space_delimited_lowercase(type(self).__name__)
        menu = self._io_manager._make_menu(
            explicit_header=explicit_header,
            name=name,
            )
        menu_entries = []
        secondary_menu_entries = self._make_secondary_menu_entries(directory)
        secondary_menu_entries = []
        for path in self._list_secondary_paths(directory):
            base_name = os.path.basename(path)
            menu_entry = (base_name, None, None, path)
            secondary_menu_entries.append(menu_entry)
        secondary_menu_entries.sort(key=lambda _: _[0])
        menu_entries.extend(secondary_menu_entries)
        asset_menu_entries = []
        paths = self._list_visible_paths(directory)
        strings = [self._to_menu_string(_) for _ in paths]
        pairs = list(zip(strings, paths))
        if self._is_score_directory(directory, 'scores'):
            def sort_function(pair):
                string = pair[0]
                string = stringtools.strip_diacritics(string)
                string = string.replace("'", '')
                return string
            pairs.sort(key=lambda _: sort_function(_))
        for string, path in pairs:
            asset_menu_entry = (string, None, None, path)
            asset_menu_entries.append(asset_menu_entry)
        menu_entries.extend(asset_menu_entries)
        if menu_entries:
            section = menu.make_asset_section(menu_entries=menu_entries)
        self._make_command_menu_sections(directory, menu)
        return menu

    def _make_material_ly(self, directory):
        assert os.path.isdir(directory), repr(directory)
        definition_path = os.path.join(directory, 'definition.py')
        if not os.path.isfile(definition_path):
            message = 'can not find {} ...'
            message = message.format(self._trim_path(definition_path))
            self._io_manager._display(message)
            return
        illustrate_file_path = os.path.join(directory, '__illustrate__.py')
        if not os.path.isfile(illustrate_file_path):
            message = 'can not find {} ...'
            message = message.format(self._trim_path(illustrate_file_path))
            self._io_manager._display(message)
            return
        candidate_ly_path = os.path.join(
            directory,
            'illustration.candidate.ly'
            )
        source_make_ly_file = os.path.join(
            configuration.abjad_ide_boilerplate_directory,
            '__make_material_ly__.py',
            )
        target_make_ly_file = os.path.join(
            directory, 
            '__make_material_ly__.py',
            )
        temporary_files = (
            candidate_ly_path,
            target_make_ly_file,
            )
        for path in temporary_files:
            if os.path.exists(path):
                os.remove(path)
        ly_path = os.path.join(directory, 'illustration.ly')
        inputs, outputs = [], []
        with systemtools.FilesystemState(remove=temporary_files):
            shutil.copyfile(source_make_ly_file, target_make_ly_file)
            result = self._io_manager.interpret_file(target_make_ly_file)
            stdout_lines, stderr_lines = result
            if stderr_lines:
                self._io_manager._display_errors(stderr_lines)
                return
            if not os.path.isfile(candidate_ly_path):
                message = 'could not make {}.'
                message = message.format(self._trim_path(candidate_ly_path))
                self._io_manager._display(message)
                return
            result = systemtools.TestManager.compare_files(
                candidate_ly_path,
                ly_path,
                )
            messages = self._make_candidate_messages(
                result,
                candidate_ly_path,
                ly_path,
                )
            self._io_manager._display(messages)
            if result:
                message = 'preserved {}.'
                message = message.format(self._trim_path(ly_path))
                self._io_manager._display(message)
                return
            else:
                message = 'overwriting {} ...'
                message = message.format(self._trim_path(ly_path))
                self._io_manager._display(message)
                try:
                    shutil.move(
                        candidate_ly_path,
                        ly_path,
                        )
                except IOError:
                    pass
                if not self._session.is_test:
                    message = 'opening {} ...'
                    message = message.format(self._trim_path(ly_path))
                    self._io_manager._display(message)
                    self._io_manager.open_file(ly_path)

    def _make_material_pdf(self, directory, subroutine=False):
        definition_path = os.path.join(directory, 'definition.py')
        if not os.path.isfile(definition_path):
            message = 'can not find {} ...'
            message = message.format(self._trim_path(definition_path))
            self._io_manager._display(message)
            return
        illustrate_file_path = os.path.join(directory, '__illustrate__.py')
        if not os.path.isfile(illustrate_file_path):
            message = 'can not find {} ...'
            message = message.format(self._trim_path(illustrate_file_path))
            self._io_manager._display(message)
            return
        candidate_ly_path = os.path.join(
            directory,
            'illustration.candidate.ly'
            )
        ly_path = os.path.join(directory, 'illustration.ly')
        ly_path_existed = os.path.exists(ly_path)
        candidate_pdf_path = os.path.join(
            directory,
            'illustration.candidate.pdf'
            )
        pdf_path = os.path.join(directory, 'illustration.pdf')
        pdf_path_existed = os.path.exists(pdf_path)
        source_make_pdf_file = os.path.join(
            configuration.abjad_ide_boilerplate_directory,
            '__make_material_pdf__.py',
            )
        target_make_pdf_file = os.path.join(
            directory, 
            '__make_material_pdf__.py',
            )
        temporary_files = (
            candidate_ly_path,
            candidate_pdf_path,
            target_make_pdf_file,
            )
        for path in temporary_files:
            if os.path.exists(path):
                os.remove(path)
        with systemtools.FilesystemState(remove=temporary_files):
            shutil.copyfile(source_make_pdf_file, target_make_pdf_file)
            message = 'Calling Python on {} ...'
            message = message.format(self._trim_path(target_make_pdf_file))
            self._io_manager._display(message)
            result = self._io_manager.interpret_file(target_make_pdf_file)
            stdout_lines, stderr_lines = result
            self._io_manager._display(stdout_lines)
            if stderr_lines:
                self._io_manager._display_errors(stderr_lines)
                return
            if not os.path.isfile(candidate_ly_path):
                message = 'could not make {}.'
                message = message.format(self._trim_path(candidate_ly_path))
                self._io_manager._display(message)
                return
            if not ly_path_existed:
                assert os.path.isfile(candidate_ly_path)
                message = 'writing {} ...'
                message = message.format(self._trim_path(ly_path))
                self._io_manager._display(message)
                shutil.move(candidate_ly_path, ly_path)
            else:
                same = systemtools.TestManager.compare_files(
                    candidate_ly_path,
                    ly_path,
                    )
                if same:
                    messages = []
                    message = 'preserving {} ...'
                    message = message.format(self._trim_path(ly_path))
                    messages.append(message)
                    message = 'preserving {} ...'
                    message = message.format(self._trim_path(pdf_path))
                    messages.append(message)
                    self._io_manager._display(messages)
                    return
                else:
                    message = 'overwriting {} ...'
                    message = message.format(self._trim_path(ly_path))
                    self._io_manager._display(message)
                    shutil.move(candidate_ly_path, ly_path)
            if not os.path.isfile(candidate_pdf_path):
                message = 'could not make {}.'
                message = message.format(self._trim_path(candidate_pdf_path))
                self._io_manager._display(message)
                return
            if not pdf_path_existed:
                assert os.path.isfile(candidate_pdf_path)
                message = 'writing {} ...'
                message = message.format(self._trim_path(pdf_path))
                self._io_manager._display(message)
                shutil.move(candidate_pdf_path, pdf_path)
            else:
                same = systemtools.TestManager.compare_files(
                    candidate_pdf_path,
                    pdf_path,
                    )
                if same:
                    messages = []
                    message = 'preserving {} ...'
                    message = message.format(self._trim_path(pdf_path))
                    messages.append(message)
                    self._io_manager._display(messages)
                    return
                else:
                    message = 'overwriting {} ...'
                    message = message.format(self._trim_path(pdf_path))
                    self._io_manager._display(message)
                    shutil.move(candidate_pdf_path, pdf_path)
            if not self._session.is_test and not subroutine:
                message = 'opening {} ...'
                message = message.format(self._trim_path(pdf_path))
                self._io_manager._display(message)
                self._io_manager.open_file(pdf_path)

    def _make_package(self, directory):
        assert os.path.isdir(directory), repr(directory)
        path = self._get_available_path(directory)
        if not path:
            return
        assert not os.path.exists(path)
        os.mkdir(path)
        required_files = (
            '__init__.py',
            '__metadata__.py',
            'definition.py',
            )
        for required_file in required_files:
            if required_file == '__init__.py':
                source_path = os.path.join(
                    configuration.abjad_ide_boilerplate_directory,
                    'empty_unicode.py',
                    )
            elif required_file == '__metadata__.py':
                source_path = os.path.join(
                    configuration.abjad_ide_boilerplate_directory,
                    '__metadata__.py',
                    )
            elif required_file == 'definition.py':
                source_path = os.path.join(
                    configuration.abjad_ide_boilerplate_directory,
                    'definition.py',
                    )
            else:
                raise ValueError(required_file)
            target_path = os.path.join(path, required_file)
            shutil.copyfile(source_path, target_path)
        new_path = path
        paths = self._list_visible_paths(directory)
        if path not in paths:
            self._clear_view(directory)
        self._manage_directory(new_path)

    def _make_score_package(self):
        message = 'enter title'
        getter = self._io_manager._make_getter()
        getter.append_string(message)
        title = getter._run(io_manager=self._io_manager)
        if not title:
            return
        package_name = stringtools.strip_diacritics(title)
        package_name = stringtools.to_snake_case(package_name)
        scores_directory = configuration.composer_scores_directory
        if self._session.is_test or self._session.is_example:
            scores_directory = configuration.abjad_ide_example_scores_directory
        outer_score_directory = os.path.join(scores_directory, package_name)
        if os.path.exists(outer_score_directory):
            message = 'directory already exists: {}.'
            message = message.format(outer_score_directory)
            self._io_manager._display(message)
            return
        year = datetime.date.today().year
        systemtools.IOManager._make_score_package(
            outer_score_directory,
            title,
            year,
            configuration.composer_full_name,
            configuration.composer_email,
            configuration.composer_github_username,
            )
        self._clear_view(scores_directory)
        inner_score_directory = os.path.join(
            outer_score_directory, 
            package_name,
            )
        self._manage_directory(inner_score_directory)

    def _make_secondary_menu_entries(self, directory):
        menu_entries = []
        for path in self._list_secondary_paths(directory):
            base_name = os.path.basename(path)
            menu_entry = (base_name, None, None, path)
            menu_entries.append(menu_entry)
        return menu_entries

    def _make_segment_ly(self, directory, dry_run=False):
        assert os.path.isdir(directory), repr(directory)
        assert self._is_score_directory(directory, 'segment')
        definition_path = os.path.join(directory, 'definition.py')
        if not os.path.isfile(definition_path):
            message = 'can not find {} ...'
            message = message.format(self._trim_path(definition_path))
            self._io_manager._display(message)
            return
        self._update_order_dependent_segment_metadata(directory)
        boilerplate_path = os.path.join(
            configuration.abjad_ide_boilerplate_directory,
            '__make_segment_ly__.py',
            )
        illustrate_path = os.path.join(directory, '__make_segment_ly__.py')
        candidate_ly_path = os.path.join(
            directory,
            'illustration.candidate.ly'
            )
        temporary_files = (
            illustrate_path,
            candidate_ly_path,
            )
        for path in temporary_files:
            if os.path.exists(path):
                os.remove(path)
        ly_path = os.path.join(directory, 'illustration.ly')
        inputs, outputs = [], []
        if dry_run:
            inputs.append(definition_path)
            outputs.append(illustration_source_path)
            return inputs, outputs
        with systemtools.FilesystemState(remove=temporary_files):
            shutil.copyfile(boilerplate_path, illustrate_path)
            previous_segment_path = self._get_previous_segment_directory(
                directory)
            if previous_segment_path is None:
                statement = 'previous_segment_metadata = None'
            else:
                score_directory = self._to_score_directory(directory)
                score_name = os.path.basename(score_directory)
                previous_segment_name = previous_segment_path
                previous_segment_name = os.path.basename(previous_segment_path)
                statement = 'from {}.segments.{}.__metadata__'
                statement += ' import metadata as previous_segment_metadata'
                statement = statement.format(score_name, previous_segment_name)
            with open(illustrate_path, 'r') as file_pointer:
                template = file_pointer.read()
            completed_template = template.format(
                previous_segment_metadata_import_statement=statement
                )
            with open(illustrate_path, 'w') as file_pointer:
                file_pointer.write(completed_template)
            result = self._io_manager.interpret_file(illustrate_path)
            stdout_lines, stderr_lines = result
            if stderr_lines:
                self._io_manager._display_errors(stderr_lines)
                return
            if not os.path.isfile(candidate_ly_path):
                message = 'can not make {}.'
                message = message.format(self._trim_path(candidate_ly_path))
                self._io_manager._display(message)
                return
            result = systemtools.TestManager.compare_files(
                candidate_ly_path,
                ly_path,
                )
            messages = self._make_candidate_messages(
                result,
                candidate_ly_path,
                ly_path,
                )
            self._io_manager._display(messages)
            if result:
                message = 'preserved {}.'
                message = message.format(self._trim_path(ly_path))
                self._io_manager._display(message)
                return
            shutil.move(candidate_ly_path, ly_path)
            message = 'wrote {}.'
            message = message.format(self._trim_path(ly_path))
            self._io_manager._display(message)

    def _make_segment_pdf(self, directory, subroutine=False):
        assert os.path.isdir(directory), repr(directory)
        definition_path = os.path.join(directory, 'definition.py')
        if not os.path.isfile(definition_path):
            message = 'can not find {} ...'
            message = message.format(self._trim_path(definition_path))
            self._io_manager._display(message)
            return
        self._update_order_dependent_segment_metadata(directory)
        boilerplate_path = os.path.join(
            configuration.abjad_ide_boilerplate_directory,
            '__illustrate_segment__.py',
            )
        illustrate_file_path = os.path.join(
            directory,
            '__illustrate__.py',
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
            illustrate_file_path,
            candidate_ly_path,
            candidate_pdf_path,
            )
        for path in temporary_files:
            if os.path.exists(path):
                os.remove(path)
        ly_path = os.path.join(directory, 'illustration.ly')
        pdf_path = os.path.join(directory, 'illustration.pdf')
        with systemtools.FilesystemState(remove=temporary_files):
            message = 'calling Python on {} ...'
            message = message.format(self._trim_path(illustrate_file_path))
            self._io_manager._display(message)
            shutil.copyfile(boilerplate_path, illustrate_file_path)
            previous_segment_directory = self._get_previous_segment_directory(
                directory)
            if previous_segment_directory is None:
                statement = 'previous_segment_metadata = None'
            else:
                assert os.path.isdir(previous_segment_directory)
                score_directory = self._to_score_directory(directory)
                score_name = os.path.basename(score_directory)
                previous_segment_name = previous_segment_directory
                previous_segment_name = os.path.basename(
                    previous_segment_directory,
                    )
                statement = 'from {}.segments.{}.__metadata__'
                statement += ' import metadata as previous_segment_metadata'
                statement = statement.format(score_name, previous_segment_name)
            with open(illustrate_file_path, 'r') as file_pointer:
                template = file_pointer.read()
            completed_template = template.format(
                previous_segment_metadata_import_statement=statement
                )
            with open(illustrate_file_path, 'w') as file_pointer:
                file_pointer.write(completed_template)
            result = self._io_manager.interpret_file(illustrate_file_path)
            stdout_lines, stderr_lines = result
            self._io_manager._display(stdout_lines)
            if stderr_lines:
                self._io_manager._display_errors(stderr_lines)
                return
            made_new_pdf = False
            if (not os.path.exists(ly_path) and
                os.path.isfile(candidate_ly_path)):
                message = 'writing {} ...'
                message = message.format(self._trim_path(ly_path))
                self._io_manager._display(message)
                shutil.move(candidate_ly_path, ly_path)
                made_new_pdf = True
            if (not os.path.exists(pdf_path) and
                os.path.isfile(candidate_pdf_path)):
                message = 'writing {} ...'
                message = message.format(self._trim_path(pdf_path))
                self._io_manager._display(message)
                shutil.move(candidate_pdf_path, pdf_path)
            if (os.path.exists(ly_path) and
                os.path.isfile(candidate_ly_path)):
                same = systemtools.TestManager.compare_files(
                    candidate_ly_path,
                    ly_path,
                    )
                if same:
                    message = 'preserving {} ...'
                    message = message.format(self._trim_path(ly_path))
                    self._io_manager._display(message)
                else:
                    message = 'overwriting {} ...'
                    message = message.format(self._trim_path(ly_path))
                    self._io_manager._display(message)
                    shutil.move(candidate_ly_path, ly_path)
            if (os.path.exists(pdf_path) and
                os.path.isfile(candidate_pdf_path)):
                same = systemtools.TestManager.compare_files(
                    candidate_pdf_path,
                    pdf_path,
                    )
                if same:
                    message = 'preserving {} ...'
                    message = message.format(self._trim_path(pdf_path))
                    self._io_manager._display(message)
                else:
                    message = 'overwriting {} ...'
                    message = message.format(self._trim_path(pdf_path))
                    self._io_manager._display(message)
                    shutil.move(candidate_pdf_path, pdf_path)
                    made_new_pdf = True
            if made_new_pdf and not subroutine:
                message = 'opening {} ...'
                message = message.format(self._trim_path(pdf_path))
                self._io_manager._display(message)
                self._io_manager.open_file(pdf_path)

    def _manage_directory(self, directory):
        if not os.path.exists(directory):
            message = 'directory does not exist: {}.'
            message = message.format(directory)
            self._io_manager._display(message)
            return
        self._session._pending_redraw = True
        if not self._session.current_directory == directory:
            self._session._previous_directory = \
                self._session.current_directory
            self._session._current_directory = directory
        menu_header = self._to_menu_header(directory)
        menu = self._make_main_menu(directory, menu_header)
        while True:
            if not self._session.current_directory == directory:
                self._session._previous_directory = \
                    self._session.current_directory
                self._session._current_directory = directory
            os.chdir(directory)
            if self._session._pending_menu_rebuild:
                menu = self._make_main_menu(directory, menu_header)
                self._session._pending_menu_rebuild = False
            result = menu._run(io_manager=self._io_manager)
            if isinstance(result, tuple):
                assert len(result) == 1, repr(result)
                unknown_string = result[0]
                path = self._match_alias(directory, unknown_string)
                if path:
                    result = None
                    if os.path.isfile(path):
                        self._io_manager.open_file(path)
                        parent_directory = os.path.dirname(path)
                        names = ('material', 'segment')
                        if self._is_score_directory(parent_directory, names):
                            self._manage_directory(parent_directory)
                    else:
                        message = 'file does not exist: {}.'
                        message = message.format(self._trim_path(path))
                        self._io_manager._display([message, ''])
            assert isinstance(result, (str, tuple, type(None))), repr(result)
            if self._session.is_quitting:
                return
            if result is None:
                continue
            self._handle_input(result)
            if self._session.is_quitting:
                return

    def _match_alias(self, directory, string):
        if self._is_score_directory(directory, 'scores'):
            return
        aliases = configuration.aliases
        if not aliases:
            return
        path = configuration.aliases.get(string)
        if not path:
            return
        score_directory = self._to_score_directory(directory, 'inner')
        path = os.path.join(score_directory, path)
        return path

    def _match_display_string_in_score(self, directory, expr):
        strings, paths = self._collect_all_display_strings_in_score(directory)
        for string, path in zip(strings, paths):
            if string == expr:
                return path
        for string, path in zip(strings, paths):
            if string.startswith(expr):
                return path
        for string, path in zip(strings, paths):
            if expr in string:
                return path
        initial_strings = []
        initial_paths = []
        for string, path in zip(strings, paths):
            string, _ = os.path.splitext(string)
            words = stringtools.delimit_words(string)
            initial_letters = [_[0] for _ in words]
            if not initial_letters:
                continue
            initial_string = ''.join(initial_letters)
            initial_strings.append(initial_string)
            initial_paths.append(path)
        pairs = zip(initial_strings, initial_paths)
        for initial_string, initial_path in pairs:
            if initial_string == expr:
                return initial_path

    @staticmethod
    def _match_display_string_view_pattern(pattern, entry):
        display_string, _, _, path = entry
        token = ':ds:'
        assert token in pattern, repr(pattern)
        pattern = pattern.replace(token, repr(display_string))
        try:
            result = eval(pattern)
        except:
            traceback.print_exc()
            result = False
        return result

    def _match_metadata_view_pattern(self, pattern, entry):
        display_string, _, _, path = entry
        count = pattern.count('md:')
        for _ in range(count+1):
            parts = pattern.split()
            for part in parts:
                if part.startswith('md:'):
                    metadatum_name = part[3:]
                    metadatum = self._get_metadatum(
                        path,
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

    def _match_visible_path(self, secondary_paths, visible_paths, input_):
        assert isinstance(input_, (str, int)), repr(input_)
        paths = secondary_paths + visible_paths
        if isinstance(input_, int):
            path_number = input_
            path_index = path_number - 1
            path = paths[path_index]
            if path in secondary_paths:
                message = 'can not rename secondary asset {}.'
                message = message.format(self._trim_path(path))
                self._io_manager._display(message)
                return
            return path
        elif isinstance(input_, str):
            name = input_
            name = name.lower()
            for path in visible_paths:
                base_name = os.path.basename(path)
                base_name = base_name.lower()
                if base_name.startswith(name):
                    return path
                base_name = base_name.replace('_', ' ')
                if base_name.startswith(name):
                    return path
                if not os.path.isdir(path):
                    continue
                title = self._get_metadatum(path, 'title')
                if not title:
                    continue
                title = title.lower()
                if title.startswith(name):
                    return path
            message = 'does not match visible path: {!r}.'
            message = message.format(name)
            self._io_manager._display(message)
            return
        else:
            raise ValueError(repr(input_))

    def _open_in_every_package(self, directories, file_name, verb='open'):
        paths = []
        for path in directories:
            path = os.path.join(path, file_name)
            if os.path.isfile(path):
                paths.append(path)
        if not paths:
            message = 'no {} files found.'
            message = message.format(file_name)
            self._io_manager._display(message)
            return
        messages = []
        for path in paths:
            message = 'opening {} ...'
            message = message.format(self._trim_path(path))
            messages.append(message)
        self._io_manager._display(messages)
        self._io_manager.open_file(paths)

    def _parse_paper_dimensions(self, directory):
        score_directory = self._to_score_directory(directory)
        string = self._get_metadatum(score_directory, 'paper_dimensions')
        string = string or '8.5 x 11 in'
        parts = string.split()
        assert len(parts) == 4
        width, _, height, units = parts
        width = eval(width)
        height = eval(height)
        return width, height, units

    def _read_view(self, directory):
        assert os.path.isdir(directory), repr(directory)
        view_name = self._get_metadatum(directory, 'view_name')
        if not view_name:
            return
        view_inventory = self._read_view_inventory(directory)
        if not view_inventory:
            return
        return view_inventory.get(view_name)

    def _read_view_inventory(self, directory):
        from ide.tools import idetools
        assert os.path.isdir(directory), repr(directory)
        views_py_path = os.path.join(directory, '__views__.py')
        result = self._io_manager.execute_file(
            path=views_py_path,
            attribute_names=('view_inventory',),
            )
        if result == 'corrupt':
            messages = []
            message = '{} __views.py__ is corrupt:'
            message = message.format(self._trim_path(directory))
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
            view_inventory = collections.OrderedDict()
        items = list(view_inventory.items())
        view_inventory = collections.OrderedDict(items)
        return view_inventory

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

    def _run_lilypond(self, ly_path):
        if systemtools.IOManager.find_executable('lilypond'):
            executable = 'lilypond'
        else:
            message = 'cannot find LilyPond executable.'
            raise ValueError(message)
        directory = os.path.dirname(ly_path)
        file_name, file_extension = os.path.splitext(ly_path)
        pdf_path = file_name + '.pdf'
        pdf_existed = os.path.exists(pdf_path)
        backup_file_name = '{}._backup.pdf'
        backup_file_name = backup_file_name.format(file_name)
        backup_pdf_path = os.path.join(directory, backup_file_name)
        assert not os.path.exists(backup_pdf_path)
        directory_change = systemtools.TemporaryDirectoryChange(directory)
        filesystem_state = systemtools.FilesystemState(
            remove=[backup_pdf_path]
            )
        messages = []
        with directory_change, filesystem_state:
            if not os.path.exists(pdf_path):
                backup_pdf_path = None
            else:
                shutil.move(pdf_path, backup_pdf_path)
                assert not os.path.exists(pdf_path)
            systemtools.IOManager.run_lilypond(ly_path)
            if not os.path.isfile(pdf_path):
                message = 'can not produce {} ...'
                message = message.format(self._trim_path(pdf_path))
                messages.append(message)
                if backup_pdf_path:
                    shutil.move(backup_pdf_path, pdf_path)
                return messages
            if backup_pdf_path is None:
                message = 'writing {} ...'
                message = message.format(self._trim_path(pdf_path))
                messages.append(message)
                return messages
            if systemtools.TestManager.compare_files(
                pdf_path,
                backup_pdf_path,
                ):
                message = 'preserving {} ...'
                message = message.format(self._trim_path(pdf_path))
                messages.append(message)
                return messages
            else:
                message = 'overwriting {} ...'
                message = message.format(self._trim_path(pdf_path))
                messages.append(message)
                return messages

    def _select_view(self, directory, is_ranged=False):
        assert os.path.isdir(directory), repr(directory)
        view_inventory = self._read_view_inventory(directory)
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
        target_name = '{} to apply'.format(target_name)
        menu_header = self._to_menu_header(directory)
        selector = self._io_manager._make_selector(
            is_ranged=is_ranged,
            items=view_names,
            menu_header=menu_header,
            target_name=target_name,
            )
        result = selector._run(io_manager=self._io_manager)
        if result is None:
            return
        return result

    def _select_visible_path(self, directory, infinitive_phrase=None):
        assert os.path.isdir(directory), repr(directory)
        secondary_paths = self._list_secondary_paths(directory)
        visible_paths = self._list_visible_paths(directory)
        if not visible_paths:
            message = 'no visible paths'
            if infinitive_phrase is not None:
                message = message + ' ' + infinitive_phrase
            message = message + '.'
            self._io_manager._display(message)
            return
        paths = secondary_paths + visible_paths
        asset_identifier = self._to_asset_identifier(directory)
        message = 'enter {}'.format(asset_identifier)
        if infinitive_phrase:
            message = message + ' ' + infinitive_phrase
        getter = self._io_manager._make_getter()
        getter.append_string_or_integer(message)
        result = getter._run(io_manager=self._io_manager)
        if not result:
            return
        path = self._match_visible_path(secondary_paths, visible_paths, result)
        return path

    def _select_visible_paths(self, directory, infinitive_phrase=None):
        assert os.path.isdir(directory), repr(directory)
        secondary_paths = self._list_secondary_paths(directory)
        visible_paths = self._list_visible_paths(directory)
        if not visible_paths:
            message = 'no visible paths'
            if infinitive_phrase is not None:
                message = message + ' ' + infinitive_phrase
            message = message + '.'
            self._io_manager._display(message)
            return
        paths = secondary_paths + visible_paths
        asset_identifier = self._to_asset_identifier(directory)
        message = 'enter {}(s)'
        if infinitive_phrase is not None:
            message += ' ' + infinitive_phrase
        message = message.format(asset_identifier)
        getter = self._io_manager._make_getter()
        getter.append_anything(message)
        result = getter._run(io_manager=self._io_manager)
        if not result:
            return
        if isinstance(result, int):
            result = [result]
        elif isinstance(result, str) and ',' in result:
            result_ = result.split(',')
            result = []
            for part in result_:
                part = part.strip()
                if mathtools.is_integer_equivalent_expr(part):
                    part = int(part)
                result.append(part)
        elif isinstance(result, str) and not ',' in result:
            result = [result]
        paths = []
        for input_ in result:
            path = self._match_visible_path(
                secondary_paths, 
                visible_paths,
                input_,
                )
            if path:
                paths.append(path)
        return paths

    def _start(self, input_=None):
        self._session._reinitialize()
        type(self).__init__(self, session=self._session)
        if input_:
            self._session._pending_input = input_
        self._session._pending_redraw = True
        directory = configuration.composer_scores_directory
        if self._session.is_test or self._session.is_example:
            directory = configuration.abjad_ide_example_scores_directory
        while True:
            self._manage_directory(directory)
            if self._session.is_quitting:
                break
        self._io_manager._clean_up()
        self._io_manager.clear_terminal()

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
            self._git_add(path)
            assert self._get_unadded_asset_paths(path) == []
            assert self._get_added_asset_paths(path) == [path_1, path_2]
            self._unadd_added_assets(path)
            assert self._get_unadded_asset_paths(path) == [path_1, path_2]
            assert self._get_added_asset_paths(path) == []
        assert self._is_up_to_date(path)
        return True

    def _to_asset_identifier(self, directory):
        assert os.path.isdir(directory), repr(directory)
        file_prototype = (
            'build',
            'distribution',
            'etc',
            'makers',
            'material',
            'segment',
            'stylesheets',
            'test',
            )
        package_prototype = (
            'scores',
            'materials',
            'segments',
            )
        if self._is_score_directory(directory, package_prototype):
            return 'package'
        elif self._is_score_directory(directory, file_prototype):
            return 'file'
        else:
            raise ValueError(directory)

    def _to_classfile_name(self, name):
        assert isinstance(name, str), repr(name)
        name = stringtools.strip_diacritics(name)
        name, extension = os.path.splitext(name)
        name = stringtools.to_upper_camel_case(name)
        name = name + '.py'
        assert self._is_classfile_name(name), repr(name)
        return name

    def _to_dash_case_file_name(self, name):
        assert isinstance(name, str), repr(name)
        name = stringtools.strip_diacritics(name)
        name = name.lower()
        name, extension = os.path.splitext(name)
        name = stringtools.to_dash_case(name)
        extension = extension or '.txt'
        name = name + extension
        assert self._is_dash_case_file_name(name), repr(name)
        return name

    def _to_menu_header(self, directory):
        assert os.path.isdir(directory), repr(directory)
        header_parts = []
        if self._is_score_directory(directory, 'scores'):
            return 'Abjad IDE - all score directories'
        score_directory = self._to_score_directory(directory)
        score_part = self._get_title_metadatum(score_directory)
        header_parts.append(score_part)
        if self._is_score_directory(directory, 'outer'):
            header_parts.append('package wrapper')
        trimmed_path = self._trim_path(directory)
        path_parts = trimmed_path.split(os.path.sep)
        path_parts = path_parts[2:]
        if not path_parts:
            directory_part, package_part = None, None
        elif len(path_parts) == 1:
            directory_part, package_part = path_parts[0], None
        elif len(path_parts) == 2:
            directory_part, package_part = path_parts
        else:
            raise ValueError(directory)
        if directory_part:
            directory_part = directory_part + ' directory'
            header_parts.append(directory_part)
        if package_part:
            package_part = package_part.replace('_', ' ')
            package_part = self._get_metadatum(directory, 'name', package_part)
            header_parts.append(package_part)
        header = ' - '.join(header_parts)
        return header

    def _to_menu_string(self, path):
        assert os.path.sep in path, repr(path)
        if self._is_score_directory(path, 'inner'):
            annotation = None
            metadata = self._get_metadata(path)
            if metadata:
                year = metadata.get('year')
                title = metadata.get('title')
                if year:
                    annotation = '{} ({})'.format(title, year)
                else:
                    annotation = str(title)
            else:
                annotation = os.path.basename(path)
            return annotation
        name = os.path.basename(path)
        directory = path 
        if os.path.isfile(directory):
            directory = os.path.dirname(directory)
        if '_' in name and not self._is_score_directory(directory, 'test'):
            name = stringtools.to_space_delimited_lowercase(name)
        if self._is_score_directory(path, 'segment'):
            return self._get_metadatum(path, 'name', name)
        else:
            return name

    def _to_module_file_name(self, name):
        assert isinstance(name, str), repr(name)
        name = stringtools.strip_diacritics(name)
        name = name.lower()
        name, extension = os.path.splitext(name)
        name = stringtools.to_snake_case(name)
        name = name + '.py'
        assert self._is_module_file_name(name), repr(name)
        return name

    def _to_name_predicate(self, directory):
        file_prototype = ('build', 'distribution', 'etc')
        package_prototype = ('materials', 'segments', 'scores')
        if self._is_score_directory(directory, file_prototype):
            return self._is_dash_case_file_name
        elif self._is_score_directory(directory, package_prototype):
            return self._is_package_name
        elif self._is_score_directory(directory, 'scores'):
            return self._is_package_name
        elif self._is_score_directory(directory, 'outer'):
            return self._is_package_name
        elif self._is_score_directory(directory, ('score', 'inner')):
            return self._is_package_name
        elif self._is_score_directory(directory, 'makers'):
            return self._is_classfile_name
        elif self._is_score_directory(directory, ('material', 'segment')):
            return self._is_lowercase_file_name
        elif self._is_score_directory(directory, 'stylesheets'):
            return self._is_stylesheet_name
        elif self._is_score_directory(directory, 'test'):
            return self._is_module_file_name
        else:
            raise ValueError(directory)

    def _to_package_name(self, name):
        assert isinstance(name, str), repr(name)
        name = stringtools.strip_diacritics(name)
        name = name.lower()
        name, extension = os.path.splitext(name)
        name = stringtools.to_snake_case(name)
        assert self._is_package_name(name), repr(name)
        return name

    @staticmethod
    def _to_score_directory(path, name=None):
        assert os.path.sep in path, repr(path)
        if name == 'scores':
            scores_directory = configuration.composer_scores_directory
            if path.startswith(scores_directory):
                return scores_directory
            scores_directory = configuration.abjad_ide_example_scores_directory
            if path.startswith(scores_directory):
                return scores_directory
        if path.startswith(configuration.composer_scores_directory):
            prefix = len(configuration.composer_scores_directory)
        elif path.startswith(configuration.abjad_ide_example_scores_directory):
            prefix = len(configuration.abjad_ide_example_scores_directory)
        else:
            return
        path_prefix = path[:prefix]
        path_suffix = path[prefix + 1:]
        score_name = path_suffix.split(os.path.sep)[0]
        score_directory = os.path.join(path_prefix, score_name)
        score_directory = os.path.join(score_directory, score_name)
        if os.path.normpath(score_directory) == os.path.normpath(
            configuration.composer_scores_directory):
            return
        if os.path.normpath(score_directory) == os.path.normpath(
            configuration.abjad_ide_example_scores_directory):
            return
        if name in ('inner', 'score'):
            return score_directory
        if name == 'outer':
            outer_score_directory = os.path.dirname(score_directory)
            return outer_score_directory
        if name is not None:
            score_directory = os.path.join(score_directory, name)
        return score_directory

    def _to_stylesheet_name(self, name):
        assert isinstance(name, str), repr(name)
        name = stringtools.strip_diacritics(name)
        name = name.lower()
        name, extension = os.path.splitext(name)
        name = stringtools.to_dash_case(name)
        name = name + '.ily'
        assert self._is_stylesheet_name(name), repr(name)
        return name

    def _to_test_file_name(self, name):
        assert isinstance(name, str), repr(name)
        name = stringtools.strip_diacritics(name)
        name = name.lower()
        name, extension = os.path.splitext(name)
        name = stringtools.to_snake_case(name)
        if not name.startswith('test_'):
            name = 'test_' + name
        name = name + '.py'
        assert self._is_test_file_name(name), repr(name)
        return name

    @staticmethod
    def _trim_ly(ly_path):
        lines = []
        with open(ly_path, 'r') as file_pointer:
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
        with open(ly_path, 'w') as file_pointer:
            file_pointer.write(lines)

    @staticmethod
    def _trim_path(path):
        assert os.path.sep in path, repr(path)
        if path.startswith(configuration.composer_scores_directory):
            scores_directory = configuration.composer_scores_directory
        elif path.startswith(configuration.abjad_ide_example_scores_directory):
            scores_directory = configuration.abjad_ide_example_scores_directory
        else:
            return path
        count = len(scores_directory.split(os.path.sep))
        parts = path.split(os.path.sep)
        parts = parts[count:]
        path = os.path.join(*parts)
        return path

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

    def _update_order_dependent_segment_metadata(self, directory):
        assert os.path.isdir(directory), repr(directory)
        directory = self._to_score_directory(directory, 'segments')
        paths = self._list_visible_paths(directory)
        if not paths:
            return
        segment_count = len(paths)
        # update segment numbers and segment count
        for segment_index, path in enumerate(paths):
            segment_number = segment_index + 1
            self._add_metadatum(
                path,
                'segment_number',
                segment_number,
                )
            self._add_metadatum(
                path,
                'segment_count',
                segment_count,
                )
        # update first bar numbers and measure counts
        path = paths[0]
        first_bar_number = 1
        self._add_metadatum(
            path,
            'first_bar_number',
            first_bar_number,
            )
        measure_count = self._get_metadatum(path, 'measure_count')
        if not measure_count:
            return
        next_bar_number = first_bar_number + measure_count
        for path in paths[1:]:
            first_bar_number = next_bar_number
            self._add_metadatum(
                path,
                'first_bar_number',
                next_bar_number,
                )
            measure_count = self._get_metadatum(path, 'measure_count')
            if not measure_count:
                return
            next_bar_number = first_bar_number + measure_count

    def _write_metadata_py(self, directory, metadata):
        assert os.path.isdir(directory), repr(directory)
        metadata_py_path = os.path.join(directory, '__metadata__.py')
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

    ### PUBLIC METHODS ###

    @Command(
        'bld',
        argument_name='current_directory',
        description='score pdf - build',
        directories=('build',),
        section='build',
        )
    def build_score(self, directory):
        r'''Builds score from the ground up.

        Returns none.
        '''
        assert os.path.isdir(directory), repr(directory)
        build_directory = self._to_score_directory(directory, 'build')
        message = 'building score ...'
        self._io_manager._display(message)
        with self._io_manager._make_interaction():
            self.copy_segment_lys(directory, subroutine=True)
            self.generate_music_ly(directory, subroutine=True)
            self.interpret_music(directory, subroutine=True)
            tex_file_path = os.path.join(build_directory, 'front-cover.tex')
            pdf_path = os.path.join(build_directory, 'front-cover.pdf')
            if tex_file_path:
                self.interpret_front_cover(directory, subroutine=True)
            elif pdf_path:
                message = 'using existing {} ...'
                message = message.format(self._trim_path(pdf_path))
                self._io_manager._display(message)
            else:
                message = 'can make front cover ...'
                self._io_manager._display(message)
                return
            tex_file_path = os.path.join(build_directory, 'preface.tex')
            pdf_path = os.path.join(build_directory, 'preface.pdf')
            if tex_file_path:
                self.interpret_preface(directory, subroutine=True)
            elif pdf_path:
                message = 'using existing {} ...'
                message = message.format(self._trim_path(pdf_path))
                self._io_manager._display(message)
            else:
                message = 'can make front cover ...'
                self._io_manager._display(message)
                return
            tex_file_path = os.path.join(build_directory, 'back-cover.tex')
            pdf_path = os.path.join(build_directory, 'back-cover.pdf')
            if tex_file_path:
                self.interpret_back_cover(directory, subroutine=True)
            elif pdf_path:
                message = 'using existing {} ...'
                message = message.format(self._trim_path(pdf_path))
                self._io_manager._display(message)
            else:
                message = 'can make front cover ...'
                self._io_manager._display(message)
                return
            self.generate_score_source(directory, subroutine=True)
            messages = self.interpret_score(directory, subroutine=True)
            if not messages[0].startswith('preserving'):
                file_path = os.path.join(build_directory, 'score.pdf')
                message = 'opening {} ...'
                message = message.format(self._trim_path(file_path))
                self._io_manager._display(message)
                self._io_manager.open_file(file_path)
    
    @Command(
        'dfk',
        argument_name='current_directory',
        description='definition file - check',
        directories=('material', 'segment',),
        section='definition_file',
        )
    def check_definition_file(self, directory, subroutine=False):
        r'''Checks definition file.

        Returns none.
        '''
        assert os.path.isdir(directory), repr(directory)
        with self._io_manager._make_interaction(dry_run=subroutine):
            definition_path = os.path.join(directory, 'definition.py')
            if not os.path.isfile(definition_path):
                message = 'can not find {} ...'
                message = message.format(self._trim_path(definition_path))
                self._io_manager._display(message)
                return
            with systemtools.Timer() as timer:
                result = self._io_manager.interpret_file(definition_path)
            stdout_lines, stderr_lines = result
            self._io_manager._display(stdout_lines)
            if stderr_lines:
                messages = [definition_path + ' FAILED:']
                messages.extend(stderr_lines)
                self._io_manager._display(messages)
            else:
                message = '{} ... OK'
                message = message.format(self._trim_path(definition_path))
                self._io_manager._display(message, capitalize=False)
            if not subroutine:
                self._io_manager._display(timer.total_time_message)

    @Command(
        'dfk*',
        argument_name='current_directory',
        description='every definition file - check',
        directories=('materials', 'segments'),
        section='star',
        )
    def check_every_definition_file(self, directory):
        r'''Checks definition file in every package.

        Returns none.
        '''
        assert os.path.isdir(directory), repr(directory)
        with self._io_manager._make_interaction():
            paths = self._list_visible_paths(directory)
            start_time = time.time()
            with systemtools.Timer() as timer:
                for path in paths:
                    self.check_definition_file(path, subroutine=True)
            self._io_manager._display(timer.total_time_message)

    @Command(
        'cp',
        argument_name='current_directory',
        forbidden_directories=('inner',),
        section='basic',
        )
    def copy(self, directory):
        r'''Copies into `directory`.

        Returns none.
        '''
        assert os.path.isdir(directory), repr(directory)
        with self._io_manager._make_interaction():
            example_scores = self._session.is_test or self._session.is_example
            directories = self._collect_similar_directories(
                directory,
                example_scores=example_scores,
                )
            paths = []
            for directory_ in directories:
                for name in os.listdir(directory_):
                    if name.endswith('.pyc'):
                        continue
                    if name.startswith('.'):
                        continue
                    if name == '__pycache__':
                        continue
                    path = os.path.join(directory_, name)
                    paths.append(path)
            trimmed_paths = [self._trim_path(_) for _ in paths]
            menu_header = self._to_menu_header(directory)
            menu_header = menu_header + ' - select:'
            selector = self._io_manager._make_selector(
                items=trimmed_paths,
                menu_header=menu_header,
                )
            trimmed_source_path = selector._run(io_manager=self._io_manager)
            if not trimmed_source_path:
                return
            if trimmed_source_path not in trimmed_paths:
                return
            scores_directory = configuration.composer_scores_directory
            if self._session.is_test or self._session.is_example:
                scores_directory = \
                    configuration.abjad_ide_example_scores_directory
            source_path = os.path.join(scores_directory, trimmed_source_path)
            asset_name = os.path.basename(source_path)
            target_path = os.path.join(directory, asset_name)
            if os.path.isfile(source_path):
                shutil.copyfile(source_path, target_path)
            elif os.path.isdir(source_path):
                shutil.copytree(source_path, target_path)
            else:
                raise ValueError(source_path)
            self._session._pending_menu_rebuild = True
            self._session._pending_redraw = True

    @Command(
        'lyc',
        argument_name='current_directory',
        description='segment lys - copy',
        directories=('build'),
        section='build-preliminary',
        )
    def copy_segment_lys(self, directory, subroutine=False):
        r'''Copies segment lys.
        
        Copies from egment directories to build directory.

        Trims top-level comments.
        
        Preserves includes and directives from each ly.

        Trims header and paper block from each ly.

        Preserves score block in each ly.

        Returns none.
        '''
        assert os.path.isdir(directory), repr(directory)
        with self._io_manager._make_interaction(dry_run=subroutine):
            message = 'copying segment LilyPond files into build directory ...'
            self._io_manager._display(message)
            directory = self._to_score_directory(directory)
            pairs = self._gather_segment_lys(directory)
            if not pairs:
                message = 'no segment lys found.'
                self._io_manager._display(message)
                return
            messages = []
            for source_ly_path, target_ly_path in pairs:
                candidate_ly_path = target_ly_path.replace(
                    '.ly',
                    '.candidate.ly',
                    )
                with systemtools.FilesystemState(remove=[candidate_ly_path]):
                    shutil.copyfile(source_ly_path, candidate_ly_path)
                    self._trim_ly(candidate_ly_path)
                    messages_ = self._handle_candidate(
                        candidate_ly_path,
                        target_ly_path,
                        )
                    messages.extend(messages_)
            for message in messages:
                if message[0].startswith('writing') and not subroutine:
                    self._session._pending_menu_rebuild = True
                    self._session._pending_redraw = True
                    self._session._after_redraw_messages = messages
                    return
            self._io_manager._display(messages)

    @Command('?', section='system')
    def display_action_command_help(self):
        r'''Displays action commands.

        Returns none.
        '''
        pass

    @Command(';', section='display navigation')
    def display_navigation_command_help(self):
        r'''Displays navigation commands.

        Returns none.
        '''
        pass

    @Command(
        'als', 
        description='aliases - edit',
        section='global files',
        )
    def edit_aliases_file(self):
        r'''Edits aliases file.

        Returns none.
        '''
        self._session._attempted_to_open_file = True
        if self._session.is_test:
            return
        path = configuration.abjad_ide_aliases_file_path
        self._io_manager.edit(path)
        configuration._read_aliases_file()

    @Command(
        'df',
        argument_name='current_directory',
        description='definition file - edit',
        directories=('material', 'segment',),
        section='definition_file',
        )
    def edit_definition_file(self, directory):
        r'''Edits definition file.

        Returns none.
        '''
        assert os.path.isdir(directory), repr(directory)
        definition_path = os.path.join(directory, 'definition.py')
        self._io_manager.edit(definition_path)

    @Command(
        'df*',
        argument_name='current_directory',
        description='every definition file - edit',
        directories=('materials', 'segments'),
        section='star',
        )
    def edit_every_definition_file(self, directory):
        r'''Edits definition file in every subdirectory of `directory`.

        Returns none.
        '''
        assert os.path.isdir(directory), repr(directory)
        with self._io_manager._make_interaction():
            paths = self._list_visible_paths(directory)
            self._open_in_every_package(paths, 'definition.py')

    @Command(
        'ff*',
        argument_name='current_directory',
        section='star',
        )
    def edit_every_file(self, directory):
        r'''Edits files in every subdirectory of `directory`.

        Returns none.
        '''
        assert os.path.isdir(directory), repr(directory)
        with self._io_manager._make_interaction():
            getter = self._io_manager._make_getter()
            getter.append_string('enter filename')
            name = getter._run(io_manager=self._io_manager)
            if not name:
                return
            command = 'find {} -name {}'
            command = command.format(directory, name)
            paths = self._io_manager.run_command(command)
            self._io_manager.open_file(paths)

    @Command(
        'ill',
        argument_name='current_directory',
        description='illustrate file - edit',
        directories=('material',),
        section='illustrate_file',
        )
    def edit_illustrate_file(self, directory):
        r'''Edits illustrate file.

        Returns none.
        '''
        assert os.path.isdir(directory), repr(directory)
        illustrate_py_path = os.path.join(directory, '__illustrate__.py')
        self._io_manager.edit(illustrate_py_path)

    @Command(
        'lxg', 
        description='latex log - edit',
        section='global files',
        )
    def edit_latex_log(self):
        r'''Edits LaTeX log.

        Returns none.
        '''
        self._session._attempted_to_open_file = True
        if not os.path.isfile(configuration.latex_log_file_path):
            message = 'can not find {}.'
            message = message.format(configuration.latex_log_file_path)
            self._io_manager._display([message, ''])
        else:
            self._io_manager.open_file(configuration.latex_log_file_path)

    @Command(
        'lpg', 
        description='lilypond log - edit',
        section='global files',
        )
    def edit_lilypond_log(self):
        r'''Edits LilyPond log.

        Returns none.
        '''
        self._session._attempted_to_open_file = True
        if self._session.is_test:
            return
        self._io_manager.open_last_log()

    @Command(
        'ly',
        argument_name='current_directory',
        description='ly - edit',
        directories=('material', 'segment',),
        section='ly',
        )
    def edit_ly(self, directory):
        r'''Edits ``illustration.ly`` in `directory`.

        Returns none.
        '''
        assert os.path.isdir(directory), repr(directory)
        file_path = os.path.join(directory, 'illustration.ly')
        self._io_manager.open_file(file_path)

    @Command(
        'bcg',
        argument_name='current_directory',
        description='back cover - generate',
        directories=('build'),
        section='build-generate',
        )
    def generate_back_cover_source(self, directory):
        r'''Generates ``back-cover.tex``.

        Returns none.
        '''
        assert os.path.isdir(directory), repr(directory)
        with self._io_manager._make_interaction():
            score_directory = self._to_score_directory(directory)
            replacements = {}
            catalog_number = self._get_metadatum(
                score_directory, 
                'catalog_number',
                '',
                )
            replacements['catalog_number'] = catalog_number
            composer_website = configuration.composer_website or ''
            if self._session.is_test or self._session.is_example:
                composer_website = 'www.composer-website.com'
            replacements['composer_website'] = composer_website
            price = self._get_metadatum(score_directory, 'price')
            replacements['price'] = price
            width, height, unit = self._parse_paper_dimensions(score_directory)
            paper_size = '{{{}{}, {}{}}}'
            paper_size = paper_size.format(width, unit, height, unit)
            replacements['paper_size'] = paper_size
            messages = self._copy_boilerplate(
                'back-cover.tex',
                os.path.join(score_directory, 'build'),
                replacements=replacements,
                )
            if messages[0].startswith('writing'):
                self._session._pending_menu_rebuild = True
                self._session._pending_redraw = True
                self._session._after_redraw_messages = messages
            else:
                self._io_manager._display(messages)

    @Command(
        'fcg',
        argument_name='current_directory',
        description='front cover - generate',
        directories=('build'),
        section='build-generate',
        )
    def generate_front_cover_source(self, directory):
        r'''Generates ``front-cover.tex``.

        Returns none.
        '''
        assert os.path.isdir(directory), repr(directory)
        with self._io_manager._make_interaction():
            score_directory = self._to_score_directory(directory)
            file_name = 'front-cover.tex'
            replacements = {}
            score_title = self._get_title_metadatum(
                score_directory,
                year=False,
                )
            score_title = score_title.upper()
            replacements['score_title'] = score_title
            forces_tagline = self._get_metadatum(
                score_directory, 
                'forces_tagline',
                '',
                )
            replacements['forces_tagline'] = forces_tagline
            year = self._get_metadatum(score_directory, 'year', '')
            replacements['year'] = str(year)
            composer = configuration.composer_uppercase_name
            if self._session.is_test or self._session.is_example:
                composer = 'EXAMPLE COMPOSER NAME'
            replacements['composer'] = str(composer)
            width, height, unit = self._parse_paper_dimensions(score_directory)
            paper_size = '{{{}{}, {}{}}}'
            paper_size = paper_size.format(width, unit, height, unit)
            replacements['paper_size'] = paper_size
            messages = self._copy_boilerplate(
                file_name,
                os.path.join(score_directory, 'build'),
                replacements=replacements,
                )
            if messages[0].startswith('writing'):
                self._session._pending_menu_rebuild = True
                self._session._pending_redraw = True
                self._session._after_redraw_messages = messages
            else:
                self._io_manager._display(messages)

    @Command(
        'mg',
        argument_name='current_directory',
        description='music - generate',
        directories=('build'),
        section='build-generate',
        )
    def generate_music_ly(self, directory, subroutine=False):
        r'''Generates ``music.ly``.

        Returns none.
        '''
        assert os.path.isdir(directory), repr(directory)
        with self._io_manager._make_interaction(dry_run=subroutine):
            message = 'generating music LilyPond file ...'
            self._io_manager._display(message)
            messages = []
            score_directory = self._to_score_directory(directory)
            segments_directory = self._to_score_directory(
                directory,
                'segments',
                )
            ly_paths = self._list_visible_paths(segments_directory)
            if ly_paths:
                view_name = self._get_metadatum(
                    segments_directory, 
                    'view_name',
                    )
                view_inventory = self._read_view_inventory(segments_directory)
                if not view_inventory or view_name not in view_inventory:
                    view_name = None
                if view_name:
                    message = 'examining segments in {!r} order ...'
                    message = message.format(view_name)
                    messages.append(message)
                else:
                    message = 'examining segments in alphabetical order ...'
                    messages.append(message)
            else:
                message = 'no segments found ...'
                messages.append(message)
            for ly_path in ly_paths:
                message = 'examining {} ...'
                message = message.format(self._trim_path(ly_path))
                messages.append(message)
            segment_names = []
            for ly_path in ly_paths:
                segment_name = os.path.basename(ly_path)
                segment_name, _ = os.path.splitext(segment_name)
                segment_names.append(segment_name)
            lilypond_names = [_.replace('_', '-') for _ in segment_names]
            source_path = os.path.join(
                configuration.abjad_ide_boilerplate_directory,
                'music.ly',
                )
            destination_path = os.path.join(
                score_directory,
                'build',
                'music.ly',
                )
            candidate_path = os.path.join(
                score_directory,
                'build',
                'music.candidate.ly',
                )
            with systemtools.FilesystemState(remove=[candidate_path]):
                shutil.copyfile(source_path, candidate_path)
                lines = []
                segment_include_statements = ''
                for i, lilypond_name in enumerate(lilypond_names):
                    file_name = lilypond_name + '.ly'
                    line = r'\include "{}"'
                    if 0 < i:
                        line = self._tab + line
                    line = line.format(file_name)
                    lines.append(line)
                if lines:
                    new = '\n'.join(lines)
                    segment_include_statements = new
                stylesheet_path = os.path.join(
                    score_directory,
                    'stylesheets',
                    'stylesheet.ily',
                    )
                stylesheet_include_statement = ''
                if stylesheet_path:
                    line = r'\include "../stylesheets/stylesheet.ily"'
                    stylesheet_include_statement = line
                language_token = lilypondfiletools.LilyPondLanguageToken()
                lilypond_language_directive = format(language_token)
                version_token = lilypondfiletools.LilyPondVersionToken()
                lilypond_version_directive = format(version_token)
                annotated_title = self._get_title_metadatum(
                    score_directory,
                    year=True,
                    )
                if annotated_title:
                    score_title = annotated_title
                else:
                    score_title = self._get_title_metadatum(
                        score_directory,
                        year=False,
                        )
                forces_tagline = self._get_metadatum(
                    score_directory,
                    'forces_tagline',
                    ''
                    )
                with open(candidate_path, 'r') as file_pointer:
                    template = file_pointer.read()
                completed_template = template.format(
                    forces_tagline=forces_tagline,
                    lilypond_language_directive=lilypond_language_directive,
                    lilypond_version_directive=lilypond_version_directive,
                    score_title=score_title,
                    segment_include_statements=segment_include_statements,
                    stylesheet_include_statement=stylesheet_include_statement,
                    )
                with open(candidate_path, 'w') as file_pointer:
                    file_pointer.write(completed_template)
                messages_ = self._handle_candidate(
                    candidate_path,
                    destination_path,
                    )
                messages.extend(messages_)
                if messages_[0].startswith('writing') and not subroutine:
                    self._session._pending_menu_rebuild = True
                    self._session._pending_redraw = True
                    self._session._after_redraw_messages = messages
                else:
                    self._io_manager._display(messages)

    @Command(
        'pg',
        argument_name='current_directory',
        description='preface - generate',
        directories=('build'),
        section='build-generate',
        )
    def generate_preface_source(self, directory):
        r'''Generates ``preface.tex``.

        Returns none.
        '''
        assert os.path.isdir(directory), repr(directory)
        with self._io_manager._make_interaction():
            score_directory = self._to_score_directory(directory)
            replacements = {}
            width, height, unit = self._parse_paper_dimensions(score_directory)
            paper_size = '{{{}{}, {}{}}}'
            paper_size = paper_size.format(width, unit, height, unit)
            replacements['paper_size'] = paper_size
            messages = self._copy_boilerplate(
                'preface.tex',
                os.path.join(score_directory, 'build'),
                replacements=replacements,
                )
            if messages[0].startswith('writing'):
                self._session._pending_menu_rebuild = True
                self._session._pending_redraw = True
                self._session._after_redraw_messages = messages
            else:
                self._io_manager._display(messages)

    @Command(
        'sg',
        argument_name='current_directory',
        description='score - generate',
        directories=('build'),
        section='build-generate',
        )
    def generate_score_source(self, directory, subroutine=False):
        r'''Generates ``score.tex``.

        Returns none.
        '''
        assert os.path.isdir(directory)
        with self._io_manager._make_interaction(dry_run=subroutine):
            message = 'generating score LaTeX file ...'
            self._io_manager._display(message)
            score_directory = self._to_score_directory(directory)
            replacements = {}
            width, height, unit = self._parse_paper_dimensions(score_directory)
            paper_size = '{{{}{}, {}{}}}'
            paper_size = paper_size.format(width, unit, height, unit)
            replacements['paper_size'] = paper_size
            messages = self._copy_boilerplate(
                'score.tex',
                os.path.join(score_directory, 'build'),
                replacements=replacements,
                )
            if messages[0].startswith('writing') and not subroutine:
                self._session._pending_menu_rebuild = True
                self._session._pending_redraw = True
                self._session._after_redraw_messages = messages
            else:
                self._io_manager._display(messages)

    @Command(
        'add*',
        argument_name='current_directory',
        directories=('scores',),
        section='git',
        )
    def git_add_every_package(self, directory):
        r'''Adds every asset to repository.

        Returns none.
        '''
        assert os.path.isdir(directory), repr(directory)
        with self._io_manager._make_interaction():
            directories = self._list_visible_paths(directory)
            self._session._attempted_method = 'git_add_every_package'
            if self._session.is_test:
                return
            inputs, outputs = [], []
            method_name = '_git_add'
            for directory in directories:
                inputs_, outputs_ = self._git_add(directory, dry_run=True)
                inputs.extend(inputs_)
                outputs.extend(outputs_)
            if inputs:
                messages = self._format_messaging(inputs, outputs, verb='add')
                self._io_manager._display(messages)
                result = self._io_manager._confirm()
                if not result:
                    return
            for directory in directories:
                self._git_add(directory, interaction=False)
            if inputs:
                count = len(inputs)
                identifier = stringtools.pluralize('file', count)
                message = 'added {} {} to repository.'
                message = message.format(count, identifier)
                self._io_manager._display(message)

    @Command(
        'ci',
        argument_name='current_directory',
        description='git - commit',
        forbidden_directories=('scores',),
        section='git',
        )
    def git_commit(
        self, 
        directory, 
        commit_message=None, 
        dry_run=False,
        interaction=True,
        ):
        r'''Commits working copy of current score package to repository.

        Returns none.
        '''
        assert os.path.isdir(directory), repr(directory)
        self._io_manager._session._attempted_method = 'git_commit'
        if self._io_manager._session.is_test:
            return
        self._git_add(directory, interaction=False)
        self.git_status(directory, subroutine=True)
        directory = self._to_score_directory(directory, 'outer')
        change = systemtools.TemporaryDirectoryChange(directory=directory)
        interaction = self._io_manager._make_interaction(
            dry_run=not interaction)
        with change, interaction:
            pending_commit = self._has_pending_commit(directory)
            if pending_commit:
                if dry_run:
                    message = '{} ... PENDING COMMIT.'
                    message = message.format(directory)
                    messages = [message]
                    self._io_manager._display(messages)
                    return True
            else:
                message = '{} ... nothing to commit.'
                message = message.format(directory)
                messages = [message]
                self._io_manager._display(messages)
                return
            if commit_message is None:
                self._io_manager._display('')
                getter = self._io_manager._make_getter()
                getter.append_string('commit message')
                commit_message = getter._run(io_manager=self._io_manager)
                if not commit_message:
                    return
            message = directory
            scores_directory = configuration.abjad_ide_example_scores_directory
            message = message.replace(scores_directory, '')
            scores_directory = configuration.composer_scores_directory
            message = message.replace(scores_directory, '')
            message = message.lstrip(os.path.sep)
            message = message + ' ...'
            command = 'git commit -m "{}" {}; git push'
            command = command.format(commit_message, directory)
            lines = self._io_manager.run_command(command)
            self._io_manager._display(lines, capitalize=False)

    @Command(
        'ci*',
        argument_name='current_directory',
        directories=('scores',),
        section='git',
        )
    def git_commit_every_package(self, directory):
        r'''Commits every asset to repository.

        Returns none.
        '''
        assert os.path.isdir(directory), repr(directory)
        assert self._is_score_directory(directory, 'scores'), repr(directory)
        self._session._attempted_method = 'git_commit_every_package'
        if self._session.is_test:
            return
        with self._io_manager._make_interaction():
            directories = self._list_visible_paths(directory)
            directories_to_commit = []
            for directory in directories:
                result = self.git_commit(
                    directory, 
                    dry_run=True,
                    interaction=False,
                    )
                if result:
                    directories_to_commit.append(directory)
            if not directories_to_commit:
                return
            self._io_manager._display('')
            getter = self._io_manager._make_getter()
            getter.append_string('commit message')
            commit_message = getter._run(io_manager=self._io_manager)
            if not commit_message:
                return
            for directory in directories_to_commit:
                result = self.git_commit(
                    directory, 
                    commit_message=commit_message,
                    interaction=False,
                    )

    @Command(
        'st',
        argument_name='current_directory',
        description='git - status',
        forbidden_directories=('scores',),
        section='git',
        )
    def git_status(self, directory, dry_run=False, subroutine=False):
        r'''Displays Git status of current score package.

        Returns none.
        '''
        assert os.path.isdir(directory), repr(directory)
        directory = self._to_score_directory(directory, 'outer')
        change = systemtools.TemporaryDirectoryChange(directory=directory)
        hold_off = dry_run or subroutine
        interaction = self._io_manager._make_interaction(dry_run=hold_off)
        with change, interaction:
            command = 'git status {}'.format(directory)
            messages = []
            self._io_manager._session._attempted_method = 'git_status'
            message = '{} ...'
            message = message.format(directory)
            messages.append(message)
            with systemtools.TemporaryDirectoryChange(directory=directory):
                lines = self._io_manager.run_command(command)
            path_ = directory + os.path.sep
            clean_lines = []
            for line in lines:
                line = str(line)
                clean_line = line.strip()
                clean_line = clean_line.replace(path_, '')
                clean_lines.append(clean_line)
            clean_lines = [_ for _ in clean_lines if not _ == '']
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

    @Command(
        'st*',
        argument_name='current_directory',
        directories=('scores',),
        section='git',
        )
    def git_status_every_package(self, directory):
        r'''Displays Git status of every package.

        Returns none.
        '''
        assert os.path.isdir(directory), repr(directory)
        with self._io_manager._make_interaction():
            directories = self._list_visible_paths(directory)
            self._session._attempted_method = 'git_status_every_package'
            directories.sort()
            for directory in directories:
                self.git_status(directory, dry_run=True)

    @Command(
        'up',
        argument_name='current_directory',
        description='git - update',
        forbidden_directories=('scores',),
        section='git',
        )
    def git_update(self, directory, interaction=True):
        r'''Updates working copy of current score package.

        Returns none.
        '''
        assert os.path.isdir(directory), repr(directory)
        directory = self._to_score_directory(directory, 'outer')
        messages = []
        change = systemtools.TemporaryDirectoryChange(directory=directory)
        dry_run = not interaction
        interaction = self._io_manager._make_interaction(dry_run=dry_run)
        with change, interaction:
            if self._io_manager._session.is_test:
                return messages
            root_directory = self._get_repository_root_directory(directory)
            command = 'git pull {}'
            command = command.format(root_directory)
            lines = self._io_manager.run_command(command)
            if lines and 'Already up-to-date' in lines[-1]:
                line = '{} ... already up-to-date.'
                line = line.format(directory)
                lines = [line]
            self._io_manager._display(lines)

    @Command(
        'up*',
        argument_name='current_directory',
        directories=('scores',),
        section='git',
        )
    def git_update_every_package(self, directory):
        r'''Updates every asset from repository.

        Returns none.
        '''
        assert os.path.isdir(directory), repr(directory)
        with self._io_manager._make_interaction():
            directories = self._list_visible_paths(directory)
            self._session._attempted_method = 'git_update_every_package'
            for directory in directories:
                messages = []
                message = self._to_menu_string(directory)
                if message.endswith(')'):
                    index = message.find('(')
                    message = message[:index]
                    message = message.strip()
                message = message + ':'
                self.git_update(directory, interaction=False)

    @Command('-', description='back', section='back-home-quit')
    def go_back(self):
        r'''Goes back.

        Returns none.
        '''
        directory = self._session.previous_directory
        if directory:
            self._manage_directory(directory)

    @Command('h', description='home', section='back-home-quit')
    def go_home(self):
        r'''Goes home.

        Returns none.
        '''
        directory = configuration.composer_scores_directory
        if self._session.is_test or self._session.is_example:
            directory = configuration.abjad_ide_example_scores_directory
        self._manage_directory(directory)

    @Command(
        'bb',
        argument_name='current_directory',
        forbidden_directories=('scores',),
        section='navigation',
        )
    def go_to_build_directory(self, directory):
        r'''Goes to build directory.

        Returns none.
        '''
        assert os.path.isdir(directory)
        directory = self._to_score_directory(directory, 'build')
        self._manage_directory(directory)

    @Command(
        'dd',
        argument_name='current_directory',
        forbidden_directories=('scores',),
        section='navigation',
        )
    def go_to_distribution_directory(self, directory):
        r'''Goes to distribution directory.

        Returns none.
        '''
        assert os.path.isdir(directory)
        directory = self._to_score_directory(directory, 'distribution')
        self._manage_directory(directory)

    @Command(
        'ee',
        argument_name='current_directory',
        forbidden_directories=('scores',),
        section='navigation',
        )
    def go_to_etc_directory(self, directory):
        r'''Goes to etc directory.

        Returns none.
        '''
        assert os.path.isdir(directory)
        directory = self._to_score_directory(directory, 'etc')
        self._manage_directory(directory)

    @Command(
        'kk',
        argument_name='current_directory',
        forbidden_directories=('scores',),
        section='navigation',
        )
    def go_to_makers_directory(self, directory):
        r'''Goes to makers directory.

        Returns none.
        '''
        assert os.path.isdir(directory)
        directory = self._to_score_directory(directory, 'makers')
        self._manage_directory(directory)

    @Command(
        'mm',
        argument_name='current_directory',
        forbidden_directories=('scores',),
        section='navigation',
        )
    def go_to_materials_directory(self, directory):
        r'''Goes to materials directory.

        Returns none.
        '''
        assert os.path.isdir(directory)
        directory = self._to_score_directory(directory, 'materials')
        self._manage_directory(directory)

    @Command(
        '>',
        argument_name='current_directory',
        directories=('material', 'materials', 'segment', 'segments'),
        section='sibling navigation',
        )
    def go_to_next_package(self, directory):
        r'''Goes to next package.

        Returns none.
        '''
        assert os.path.isdir(directory), repr(directory)
        directory = self._get_next_package(directory)
        self._manage_directory(directory)

    @Command(
        '<',
        argument_name='current_directory',
        directories=('material', 'materials', 'segment', 'segments'),
        section='sibling navigation',
        )
    def go_to_previous_package(self, directory):
        r'''Goes to previous package.

        Returns none.
        '''
        assert os.path.isdir(directory), repr(directory)
        directory = self._get_previous_package(directory)
        self._manage_directory(directory)

    @Command(
        'ss',
        argument_name='current_directory',
        forbidden_directories=('scores',),
        section='navigation',
        )
    def go_to_score_directory(self, directory):
        r'''Goes to score directory.

        Returns none.
        '''
        assert os.path.isdir(directory)
        directory = self._to_score_directory(directory)
        self._manage_directory(directory)

    @Command(
        'ww',
        argument_name='current_directory',
        forbidden_directories=('scores',),
        section='navigation',
        )
    def go_to_score_package_wrapper(self, directory):
        r'''Goes to score directory wrapper.

        Returns none.
        '''
        assert os.path.isdir(directory)
        directory = self._to_score_directory(directory, 'outer')
        self._manage_directory(directory)

    @Command(
        'gg',
        argument_name='current_directory',
        forbidden_directories=('scores',),
        section='navigation',
        )
    def go_to_segments_directory(self, directory):
        r'''Goes to segments directory.

        Returns none.
        '''
        assert os.path.isdir(directory)
        directory = self._to_score_directory(directory, 'segments')
        self._manage_directory(directory)

    @Command(
        'yy',
        argument_name='current_directory',
        forbidden_directories=('scores',),
        section='navigation',
        )
    def go_to_stylesheets_directory(self, directory):
        r'''Goes to stylesheets directory.

        Returns none.
        '''
        assert os.path.isdir(directory)
        directory = self._to_score_directory(directory, 'stylesheets')
        self._manage_directory(directory)

    @Command(
        'tt',
        argument_name='current_directory',
        forbidden_directories=('scores',),
        section='navigation',
        )
    def go_to_test_directory(self, directory):
        r'''Goes to test directory.

        Returns none.
        '''
        assert os.path.isdir(directory)
        directory = self._to_score_directory(directory, 'test')
        self._manage_directory(directory)

    @Command(
        'bci',
        argument_name='current_directory',
        description='back cover - interpret',
        directories=('build'),
        section='build-interpret',
        )
    def interpret_back_cover(self, directory, subroutine=False):
        r'''Interprets ``back-cover.tex``.

        Returns none.
        '''
        assert os.path.isdir(directory), repr(directory)
        with self._io_manager._make_interaction(dry_run=subroutine):
            score_directory = self._to_score_directory(directory)
            build_directory = os.path.join(score_directory, 'build')
            file_path = os.path.join(build_directory, 'back-cover.tex')
            messages = self._call_latex_on_file(file_path)
            if messages[0].startswith('writing') and not subroutine:
                self._session._pending_menu_rebuild = True
                self._session._pending_redraw = True
                self._session._after_redraw_messages = messages
            else:
                self._io_manager._display(messages)

    @Command(
        'lyi*',
        argument_name='current_directory',
        description='every ly - interpret',
        directories=('materials', 'segments'),
        section='star',
        )
    def interpret_every_ly(self, directory):
        r'''Interprets LilyPond file in every directory.

        Makes PDF in every directory.

        Returns none.
        '''
        assert os.path.isdir(directory), repr(directory)
        with self._io_manager._make_interaction():
            directories = self._list_visible_paths(directory)
            ly_files = []
            for directory in directories:
                ly_file = os.path.join(directory, 'illustration.ly')
                if os.path.isfile(ly_file):
                    ly_files.append(ly_file)
            if not ly_files:
                message = 'no LilyPond files found.'
                message._io_manager._display(message)
                return
            with systemtools.Timer() as timer:
                for ly_file in ly_files:
                    directory = os.path.dirname(ly_file)
                    result = self.interpret_ly(directory, subroutine=True)
                self._io_manager._display(timer.total_time_message)

    @Command(
        'fci',
        argument_name='current_directory',
        description='front cover - interpret',
        directories=('build'),
        section='build-interpret',
        )
    def interpret_front_cover(self, directory, subroutine=False):
        r'''Interprets ``front-cover.tex``.

        Returns none.
        '''
        assert os.path.isdir(directory), repr(directory)
        with self._io_manager._make_interaction(dry_run=subroutine):
            score_directory = self._to_score_directory(directory)
            build_directory = os.path.join(score_directory, 'build')
            file_path = os.path.join(build_directory, 'front-cover.tex')
            messages = self._call_latex_on_file(file_path)
            if messages[0].startswith('writing') and not subroutine:
                self._session._pending_menu_rebuild = True
                self._session._pending_redraw = True
                self._session._after_redraw_messages = messages
            else:
                self._io_manager._display(messages)

    @Command(
        'lyi',
        argument_name='current_directory',
        description='ly - interpret',
        directories=('material', 'segment',),
        section='ly',
        )
    def interpret_ly(self, directory, subroutine=False):
        r'''Interprets illustration ly in `directory`.

        Makes illustration PDF.

        Returns a pair.
        
        Pairs equals list of STDERR messages from LilyPond together
        with list of candidate messages.
        '''
        assert os.path.isdir(directory), repr(directory)
        with self._io_manager._make_interaction(dry_run=subroutine):
            ly_path = os.path.join(directory, 'illustration.ly')
            if not os.path.isfile(ly_path):
                message = 'the file {} does not exist.'
                message = message.format(self._trim_path(ly_path))
                self._io_manager._display(message)
                return
            message = 'calling LilyPond on {} ...'
            message = message.format(self._trim_path(ly_path))
            self._io_manager._display(message)
            messages = self._run_lilypond(ly_path)
            self._io_manager._display(messages)

    @Command(
        'mi',
        argument_name='current_directory',
        description='music - interpret',
        directories=('build'),
        section='build-interpret',
        )
    def interpret_music(self, directory, subroutine=False):
        r'''Interprets ``music.ly``.

        Returns none.
        '''
        assert os.path.isdir(directory), repr(directory)
        with self._io_manager._make_interaction(dry_run=subroutine):
            score_directory = self._to_score_directory(directory)
            build_directory = os.path.join(score_directory, 'build')
            ly_path = os.path.join(build_directory, 'music.ly')
            if not ly_path:
                message = 'can not find {} ...'
                message = message.format(self._trim_path(ly_path))
                self._io_manager._display(message)
                return
            message = 'calling LilyPond on {} ...'
            message = message.format(self._trim_path(ly_path))
            self._io_manager._display(message)
            messages = self._run_lilypond(ly_path)
            if messages[0].startswith('writing') and not subroutine:
                self._session._pending_menu_rebuild = True
                self._session._pending_redraw = True
                self._session._after_redraw_messages = messages
            else:
                self._io_manager._display(messages)

    @Command(
        'pi',
        argument_name='current_directory',
        description='preface - interpret',
        directories=('build'),
        section='build-interpret',
        )
    def interpret_preface(self, directory, subroutine=False):
        r'''Interprets ``preface.tex``.

        Returns none.
        '''
        assert os.path.isdir(directory), repr(directory)
        with self._io_manager._make_interaction(dry_run=subroutine):
            score_directory = self._to_score_directory(directory)
            build_directory = os.path.join(score_directory, 'build')
            file_path = os.path.join(build_directory, 'preface.tex')
            messages = self._call_latex_on_file(file_path)
            if messages[0].startswith('writing') and not subroutine:
                self._session._pending_menu_rebuild = True
                self._session._pending_redraw = True
                self._session._after_redraw_messages = messages
            else:
                self._io_manager._display(messages)

    @Command(
        'si',
        argument_name='current_directory',
        description='score - interpret',
        directories=('build'),
        section='build-interpret',
        )
    def interpret_score(self, directory, subroutine=False):
        r'''Interprets ``score.tex``.

        Returns none.
        '''
        assert os.path.isdir(directory), repr(directory)
        with self._io_manager._make_interaction(dry_run=subroutine):
            score_directory = self._to_score_directory(directory)
            build_directory = os.path.join(score_directory, 'build')
            file_path = os.path.join(build_directory, 'score.tex')
            messages = self._call_latex_on_file(file_path)
            if messages[0].startswith('writing') and not subroutine:
                self._session._pending_menu_rebuild = True
                self._session._pending_redraw = True
                self._session._after_redraw_messages = messages
            else:
                self._io_manager._display(messages)
            return messages

    @Command('!', section='system')
    def invoke_shell(self):
        r'''Invokes shell.

        Returns none.
        '''
        with self._io_manager._make_interaction():
            statement = self._io_manager._handle_input(
                '$',
                include_chevron=False,
                include_newline=False,
                )
            statement = statement.strip()
            self._io_manager._invoke_shell(statement)

    @Command(
        'pdfm*',
        argument_name='current_directory',
        description='every pdf - make',
        directories=('materials', 'segments'),
        section='star',
        )
    def make_every_pdf(self, directory):
        r'''Makes PDF in every directory.

        Returns none.
        '''
        assert os.path.isdir(directory), repr(directory)
        assert self._is_score_directory(directory, ('materials', 'segments'))
        with self._io_manager._make_interaction():
            directories = self._list_visible_paths(directory)
            valid_directories = directories[:]
            with systemtools.Timer() as timer:
                for directory in valid_directories:
                    self.make_pdf(directory, subroutine=True)
                self._io_manager._display(timer.total_time_message)

    @Command(
        'illm',
        argument_name='current_directory',
        description='illustrate file - make',
        directories=('material',),
        section='illustrate_file',
        )
    def make_illustrate_file(self, directory):
        r'''Makes illustrate file.

        Returns none.
        '''
        assert os.path.isdir(directory), repr(directory)
        score_directory = self._to_score_directory(directory)
        score_package_name = os.path.basename(score_directory)
        material_package_name = os.path.basename(directory)
        source_path = os.path.join(
            configuration.abjad_ide_boilerplate_directory,
            '__illustrate_material__.py',
            )
        target_path = os.path.join(
            directory,
            '__illustrate__.py',
            )
        shutil.copyfile(source_path, target_path)
        with open(target_path, 'r') as file_pointer:
            template = file_pointer.read()
        completed_template = template.format(
            score_package_name=score_package_name,
            material_package_name=material_package_name,
            )
        with open(target_path, 'w') as file_pointer:
            file_pointer.write(completed_template)
        self._session._pending_menu_rebuild = True
        self._session._pending_redraw = True

    @Command(
        'lym',
        argument_name='current_directory',
        description='ly - make',
        directories=('material', 'segment',),
        section='ly',
        )
    def make_ly(self, directory, dry_run=False):
        r'''Makes illustration ly.

        Returns none.
        '''
        assert os.path.isdir(directory), repr(directory)
        with self._io_manager._make_interaction():
            if self._is_score_directory(directory, 'material'):
                self._make_material_ly(directory)
            elif self._is_score_directory(directory, 'segment'):
                self._make_segment_ly(directory)
            else:
                raise ValueError(directory)

    @Command(
        'pdfm',
        argument_name='current_directory',
        description='pdf - make',
        directories=('material', 'segment',),
        section='pdf',
        )
    def make_pdf(self, directory, subroutine=False):
        r'''Makes illustration PDF.

        Returns none.
        '''
        assert os.path.isdir(directory), repr(directory)
        interaction = self._io_manager._make_interaction(dry_run=subroutine)
        timer = systemtools.Timer()
        with interaction, timer:
            if self._is_score_directory(directory, 'material'):
                result = self._make_material_pdf(
                    directory,
                    subroutine=subroutine,
                    )
            elif self._is_score_directory(directory, 'segment'):
                result = self._make_segment_pdf(
                    directory,
                    subroutine=subroutine,
                    )
            else:
                raise ValueError(directory)
            self._io_manager._display(timer.total_time_message)
            return result

    @Command(
        'new',
        argument_name='current_directory',
        forbidden_directories=('inner',),
        section='basic',
        )
    def new(self, directory):
        r'''Makes new asset.

        Returns none.
        '''
        assert os.path.isdir(directory), repr(directory)
        if self._is_score_directory(directory, 'scores'):
            self._make_score_package()
        elif self._is_score_directory(directory, ('materials', 'segments')):
            self._make_package(directory)
        else:
            self._make_file(directory)
        self._session._pending_menu_rebuild = True
        self._session._pending_redraw = True

    @Command(
        'pdf*',
        argument_name='current_directory',
        description='every pdf - open',
        directories=('materials', 'segments'),
        section='star',
        )
    def open_every_pdf(self, directory):
        r'''Opens PDF in every package.

        Returns none.
        '''
        assert os.path.isdir(directory), repr(directory)
        with self._io_manager._make_interaction():
            directories = self._list_visible_paths(directory)
            self._open_in_every_package(directories, 'illustration.pdf')

    @Command(
        'so*',
        argument_name='current_directory',
        directories=('scores',),
        section='star',
        )
    def open_every_score_pdf(self, directory):
        r'''Opens score PDF in every package.

        Returns none.
        '''
        assert os.path.isdir(directory), repr(directory)
        with self._io_manager._make_interaction():
            directories = self._list_visible_paths(directory)
            paths = []
            for directory in directories:
                inputs, outputs = self.open_score_pdf(directory, dry_run=True)
                paths.extend(inputs)
            for path in paths:
                message = 'opening {} ...'
                message = message.format(self._trim_path(path))
                self._io_manager._display(message)
            if paths:
                self._io_manager.open_file(paths)

    @Command(
        'pdf',
        argument_name='current_directory',
        description='pdf - open',
        directories=('material', 'segment',),
        section='pdf',
        )
    def open_pdf(self, directory):
        r'''Opens illustration PDF.

        Returns none.
        '''
        assert os.path.isdir(directory), repr(directory)
        file_path = os.path.join(directory, 'illustration.pdf')
        if not os.path.isfile(file_path):
            message = 'file does not exist: {}.'
            message = message.format(self._trim_path(file_path))
            self._io_manager._display([message, ''])
        else:
            self._io_manager.open_file(file_path)

    @Command(
        'so',
        argument_name='current_directory',
        description='score pdf - open',
        directories=('inner',),
        section='pdf',
        )
    def open_score_pdf(self, directory, dry_run=False):
        r'''Opens ``score.pdf``.

        Returns none.
        '''
        file_name = 'score.pdf'
        directory = os.path.join(directory, 'distribution')
        path = self._get_file_path_ending_with(directory, file_name)
        if not path:
            directory = os.path.join(directory, 'build')
            path = self._get_file_path_ending_with(
                directory,
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

    @Command(
        'spp',
        argument_name='current_directory',
        description='score pdf - publish',
        directories=('build'),
        section='build',
        )
    def publish_score_pdf(self, directory):
        r'''Publishes score PDF in distribution directory.

        Returns none.
        '''
        assert os.path.isdir(directory), repr(directory)
        score_directory = self._to_score_directory(directory)
        path = os.path.join(score_directory, 'build')
        build_score_path = os.path.join(path, 'score.pdf')
        if not os.path.exists(build_score_path):
            message = 'does not exist: {!r}.'
            message = message.format(self._trim_path(build_score_path))
            self._io_manager._display(message)
            return
        score_package_name = os.path.basename(score_directory)
        score_package_name = score_package_name.replace('_', '-')
        distribution_file_name = '{}-score.pdf'.format(score_package_name)
        distribution_directory = os.path.join(score_directory, 'distribution')
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

    @Command('q', description='quit', section='back-home-quit')
    def quit_abjad_ide(self):
        r'''Quits Abjad IDE.

        Returns none.
        '''
        self._session._is_quitting = True

    @Command(
        'rm',
        argument_name='current_directory',
        forbidden_directories=('inner',),
        section='basic',
        )
    def remove(self, directory):
        r'''Removes file or directory.

        Returns none.
        '''
        assert os.path.isdir(directory), repr(directory)
        paths = self._select_visible_paths(directory, 'to remove')
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
        result = getter._run(io_manager=self._io_manager)
        if result is None:
            return
        if not result == confirmation_string:
            return
        for path in paths:
            if self._is_score_directory(path, 'inner'):
                path = self._to_score_directory(path, 'outer')
            if self._is_in_git_repository(path):
                if self._is_git_unknown(path):
                    command = 'rm -rf {}'
                else:
                    command = 'git rm --force -r {}'
            else:
                command = 'rm -rf {}'
            command = command.format(path)
            with systemtools.TemporaryDirectoryChange(directory=path):
                self._io_manager.run_command(command)
            cleanup_command = 'rm -rf {}'
            cleanup_command = cleanup_command.format(path)
            self._io_manager.run_command(command)
        self._session._pending_menu_rebuild = True
        self._session._pending_redraw = True

    @Command(
        'ren',
        argument_name='current_directory',
        forbidden_directories=('inner',),
        section='basic',
        )
    def rename(self, directory):
        r'''Renames asset.

        Returns none.
        '''
        assert os.path.isdir(directory), repr(directory)
        source_path = self._select_visible_path(directory, 'to rename')
        if self._is_score_directory(source_path, 'inner'):
            source_path = os.path.dirname(source_path)
        if not source_path:
            return
        message = 'Will rename]> {}'
        message = message.format(self._trim_path(source_path))
        self._io_manager._display(message)
        getter = self._io_manager._make_getter()
        getter.append_string('new name or return to cancel')
        original_target_name = getter._run(io_manager=self._io_manager)
        if not original_target_name:
            return
        target_name = self._coerce_name(directory, original_target_name)
        source_name = os.path.basename(source_path)
        target_path = os.path.join(
            os.path.dirname(source_path),
            target_name,
            )
        if os.path.exists(target_path):
            message = 'path already exists: {!r}.'
            message = message.format(self._trim_path(target_path))
            self._io_manager._display(message)
            return
        messages = []
        messages.append('will rename ...')
        message = ' FROM: {}'.format(self._trim_path(source_path))
        messages.append(message)
        message = '   TO: {}'.format(self._trim_path(target_path))
        messages.append(message)
        self._io_manager._display(messages)
        if not self._io_manager._confirm():
            return
        shutil.move(source_path, target_path)
        if os.path.isdir(target_path):
            for directory_entry in sorted(os.listdir(target_path)):
                if not directory_entry.endswith('.py'):
                    continue
                path = os.path.join(target_path, directory_entry)
                self._replace_in_file(
                    path,
                    source_name,
                    target_name,
                    )
        if self._is_score_directory(target_path, 'outer'):
            false_inner_path = os.path.join(target_path, source_name)
            assert os.path.exists(false_inner_path)
            correct_inner_path = os.path.join(target_path, target_name)
            shutil.move(false_inner_path, correct_inner_path)
            self._add_metadatum(
                correct_inner_path, 
                'title',
                original_target_name,
                )
            for directory_entry in sorted(os.listdir(correct_inner_path)):
                if not directory_entry.endswith('.py'):
                    continue
                path = os.path.join(correct_inner_path, directory_entry)
                self._replace_in_file(
                    path,
                    source_name,
                    target_name,
                    )
        self._session._pending_menu_rebuild = True
        self._session._pending_redraw = True

    @Command(
        'rp',
        argument_name='current_directory',
        section='system',
        )
    def replace(self, directory):
        r'''Replaces expression.

        Returns none.
        '''
        assert os.path.isdir(directory), repr(directory)
        change = systemtools.TemporaryDirectoryChange(directory)
        with self._io_manager._make_interaction(), change:
            getter = self._io_manager._make_getter()
            getter.append_string('enter search string')
            search_string = getter._run(io_manager=self._io_manager)
            if not search_string:
                return
            getter = self._io_manager._make_getter()
            getter.append_string('enter replace string')
            replace_string = getter._run(io_manager=self._io_manager)
            if not replace_string:
                return
            complete_words = False
            result = self._io_manager._confirm('complete words only?')
            if result:
                complete_words = True
            command = 'ajv replace {!r} {!r}'
            command = command.format(search_string, replace_string)
            if complete_words:
                command += ' -Y'  
            lines = self._io_manager.run_command(command)
            lines = [_.strip() for _ in lines if not _ == '']
            self._io_manager._display(lines, capitalize=False)

    @Command(
        'dt',
        argument_name='current_directory',
        description='doctest - run',
        forbidden_directories=('scores',),
        section='tests',
        )
    def run_doctest(self, directory):
        r'''Runs doctest on entire score.

        Returns none.
        '''
        assert os.path.isdir(directory), repr(directory)
        directory = self._to_score_directory(directory, 'inner')
        interaction = self._io_manager._make_interaction()
        change = systemtools.TemporaryDirectoryChange(directory=directory)
        with interaction, change:
            command = 'ajv doctest {}'
            command = command.format(directory)
            lines = self._io_manager.run_command(command)
            lines = [_ for _ in lines if not _ == '']
            self._io_manager._display(lines, capitalize=False)

    @Command(
        'pt',
        argument_name='current_directory',
        description='pytest - run',
        forbidden_directories=('scores',),
        section='tests',
        )
    def run_pytest(self, directory):
        r'''Runs pytest on entire score.

        Returns none.
        '''
        assert os.path.isdir(directory), repr(directory)
        with self._io_manager._make_interaction():
            directory = self._to_score_directory(directory, 'inner')
            command = 'py.test -rf {}'
            command = command.format(directory)
            lines = self._io_manager.run_command(command)
            lines = [_ for _ in lines if not _ == '']
            self._io_manager._display(lines, capitalize=False)

    @Command(
        'sr',
        argument_name='current_directory',
        section='system',
        )
    def search(self, directory):
        r'''Searches for expression

        Delegates to ack.

        Returns none.
        '''
        assert os.path.isdir(directory), repr(directory)
        with self._io_manager._make_interaction():
            assert self._io_manager.find_executable('ack')
            getter = self._io_manager._make_getter()
            getter.append_string('enter search string')
            search_string = getter._run(io_manager=self._io_manager)
            if not search_string:
                return
            command = r'ack {!r}'
            command = command.format(search_string)
            lines = self._io_manager.run_command(command)
            self._io_manager._display(lines, capitalize=False)