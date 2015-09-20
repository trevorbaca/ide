# -*- coding: utf-8 -*-
from __future__ import print_function
import codecs
import datetime
import glob
import inspect
import os
import shutil
import sys
import time
from abjad.tools import datastructuretools
from abjad.tools import lilypondfiletools
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
        '_io_manager',
        '_session',
        )

    _abjad_import_statement = 'from abjad import *'

    _directory_name_to_asset_identifier = {
        'build': 'file',
        'distribution': 'file',
        'etc': 'file',
        'makers': 'file',
        'materials': 'package',
        'segments': 'package',
        'scores': 'package',
        'stylesheets': 'file',
        'test': 'file',
        }

    _directory_name_to_file_extension = {
        'makers': '.py',
        'stylesheets': '.ily',
        'test': '.py',
        }

    _directory_name_to_navigation_command_name = {
        'build': 'u',
        'distribution': 'd',
        'etc': 'c',
        'makers': 'k',
        'materials': 'm',
        'segments': 'g',
        'stylesheets': 'y',
        'test': 't',
        }

    _directory_name_to_package_contents = {
        'materials': {
            'optional_directories': (
                '__pycache__',
                ),
            'optional_files': (
                '__illustrate__.py',
                'illustration.ly',
                'illustration.pdf',
                ),
            'required_directories': (),
            'required_files': (
                '__init__.py',
                '__metadata__.py',
                'definition.py',
                ),
            },
        'score': {
            'optional_directories': (
                '__pycache__',
                ),
            'optional_files': (),
            'required_directories': (
                'build',
                'distribution',
                'etc',
                'makers',
                'materials',
                'segments',
                'stylesheets',
                'test',
                ),
            'required_files': (
                '__init__.py',
                '__metadata__.py',
                os.path.join('makers', '__init__.py'),
                os.path.join('materials', '__abbreviations__.py'),
                os.path.join('materials', '__init__.py'),
                os.path.join('segments', '__init__.py'),
                os.path.join('segments', '__metadata__.py'),
                os.path.join('segments', '__views__.py'),
                ),
            },
        'segments': {
            'optional_directories': (
                '__pycache__',
                ),
            'optional_files': (
                'illustration.ly',
                'illustration.pdf',
                ),
            'required_directories': (),
            'required_files': (
                '__init__.py',
                '__metadata__.py',
                'definition.py',
                ),
            },
        }

    _known_secondary_assets = (
        '__init__.py',
        '__metadata__.py',
        '__views__.py',
        '__abbreviations__.py',
        )

    _navigation_command_name_to_directory_name = {
        'd': 'distribution',
        'c': 'etc',
        'g': 'segments',
        'k': 'makers',
        'm': 'materials',
        't': 'test',
        'u': 'build',
        'y': 'stylesheets',
        }

    _known_directory_names = sorted(
        _navigation_command_name_to_directory_name.values()
        )

    _tab = 4 * ' '

    _unicode_directive = '# -*- coding: utf-8 -*-'

    ### INITIALIZER ###

    def __init__(self, session=None, is_test=False):
        from ide.tools import idetools
        if session is None:
            session = idetools.Session()
            session._is_test = is_test
        self._session = session
        io_manager = idetools.IOManager(session=session)
        self._io_manager = io_manager
        for directory_name in self._known_directory_names:
            self._supply_global_views_file(directory_name)
        self._supply_global_metadata_py()

    ### SPECIAL METHODS ###

    def __repr__(self):
        r'''Gets interpreter representation of asset controller.

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

    def _check_every_file(self, directory_token, score_directory):
        if self._session.is_in_score:
            directory_token = os.path.join(
                self._session.current_score_directory,
                directory_token,
                )
        elif score_directory is not None:
            directory_token = os.path.join(
                score_directory,
                directory_token,
                )
        directory_name = os.path.basename(directory_token)
        paths = self._list_asset_paths(
            directory_name,
            valid_only=False,
            )
        if os.path.sep in directory_token:
            paths = [_ for _ in paths if _.startswith(directory_token)]
        paths = [_ for _ in paths if os.path.basename(_)[0].isalpha()]
        paths = [_ for _ in paths if not _.endswith('.pyc')]
        invalid_paths = []
        for path in paths:
            file_name = os.path.basename(path)
            if not file_name[0].isalpha():
                invalid_paths.append(path)
        messages = []
        base_name = os.path.basename(directory_token)
        directory_label = '{} directory'.format(base_name)
        if not invalid_paths:
            count = len(paths)
            message = '{} ({} files): OK'.format(directory_label, count)
            messages.append(message)
        else:
            message = '{}:'.format(directory_label)
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

    def _clear_view(self, directory_token):
        if os.path.sep in directory_token:
            view_directory = directory_token
            metadatum_name = 'view_name'
        else:
            view_directory = configuration.abjad_ide_views_directory
            metadatum_name = '{}_view_name'.format(directory_token)
        self._add_metadatum(
            view_directory,
            metadatum_name,
            None,
            )

    def _collect_build_files(self, example_scores=False):
        build_files = []
        build_directories = self._collect_canonical_directories(
            'build',
            example_scores=example_scores,
            )
        for build_directory in build_directories:
            for name in os.listdir(build_directory):
                if not name[0].isalpha():
                    continue
                build_file = os.path.join(build_directory, name)
                if not os.path.isfile(build_file):
                    continue
                build_files.append(build_file)
        return build_files

    def _collect_canonical_directories(
        self,
        directory_name,
        example_scores=False,
        ):
        canonical_directories = []
        inner_score_directories = self._collect_inner_score_directories(
            example_scores=example_scores,
            )
        for inner_score_directory in inner_score_directories:
            canonical_directory = os.path.join(
                inner_score_directory, 
                directory_name,
                )
            if os.path.isdir(canonical_directory):
                canonical_directories.append(canonical_directory)
        return canonical_directories

    def _collect_distribution_files(self, example_scores=False):
        distribution_files = []
        distribution_directories = self._collect_canonical_directories(
            'distribution',
            example_scores=example_scores,
            )
        for distribution_directory in distribution_directories:
            for name in os.listdir(distribution_directory):
                if not name[0].isalpha():
                    continue
                distribution_file = os.path.join(distribution_directory, name)
                if not os.path.isfile(distribution_file):
                    continue
                distribution_files.append(distribution_file)
        return distribution_files

    def _collect_etc_files(self, example_scores=False):
        etc_files = []
        etc_directories = self._collect_canonical_directories(
            'etc',
            example_scores=example_scores,
            )
        for etc_directory in etc_directories:
            for name in os.listdir(etc_directory):
                if not name[0].isalpha():
                    continue
                etc_file = os.path.join(etc_directory, name)
                if not os.path.isfile(etc_file):
                    continue
                etc_files.append(etc_file)
        return etc_files

    def _collect_files(self, example_scores=False):
        outer_score_directories = self._collect_outer_score_directories()
        files_ = []
        for outer_score_directory in outer_score_directories:
            triples = os.walk(outer_score_directory)
            for root, directory_names, file_names in triples:
                for file_name in file_names:
                    file_ = os.path.join(root, file_name)
                    files_.append(file_)
        return files_

    def _collect_inner_score_directories(self, example_scores=False):
        inner_score_directories = []
        outer_score_directories = self._collect_outer_score_directories(
            example_scores=example_scores,
            )
        for outer_score_directory in outer_score_directories:
            base_name = os.path.basename(outer_score_directory)
            inner_score_directory = os.path.join(
                outer_score_directory,
                base_name,
                )
            if not os.path.isdir(inner_score_directory):
                continue
            inner_score_directories.append(inner_score_directory)
        return inner_score_directories

    def _collect_maker_files(self, example_scores=False):
        maker_files = []
        makers_directories = self._collect_canonical_directories(
            'makers',
            example_scores=example_scores,
            )
        for makers_directory in makers_directories:
            for name in os.listdir(makers_directory):
                if not name[0].isalpha():
                    continue
                if not name.endswith('.py'):
                    continue
                maker_file = os.path.join(makers_directory, name)
                if not os.path.isfile(maker_file):
                    continue
                maker_files.append(maker_file)
        return maker_files

    def _collect_material_directories(self, example_scores=False):
        material_directories = []
        materials_directories = self._collect_canonical_directories(
            'materials',
            example_scores=example_scores,
            )
        for materials_directory in materials_directories:
            for name in os.listdir(materials_directory):
                if not name[0].isalpha():
                    continue
                material_directory = os.path.join(materials_directory, name)
                if not os.path.isdir(material_directory):
                    continue
                material_directories.append(material_directory)
        return material_directories

    def _collect_material_files(self, example_scores=False):
        material_files = []
        material_directories = self._collect_material_directories(
            example_scores=example_scores,
            )
        for material_directory in material_directories:
            for name in os.listdir(material_directory):
                if not name[0].isalpha():
                    continue
                if name.endswith('.pyc'):
                    continue
                material_file = os.path.join(material_directory, name)
                material_files.append(material_file)
        return material_files

    def _collect_outer_score_directories(self, example_scores=False):
        outer_score_directories = []
        scores_directories = [configuration.composer_scores_directory]
        if example_scores:
            scores_directories.append(
                configuration.abjad_ide_example_scores_directory)
        for scores_directory in scores_directories:
            for name in os.listdir(scores_directory):
                if not name[0].isalpha():
                    continue
                outer_score_directory = os.path.join(scores_directory, name)
                if not os.path.isdir(outer_score_directory):
                    continue
                outer_score_directories.append(outer_score_directory)
        return outer_score_directories
            
    def _collect_segment_directories(self, example_scores=False):
        segment_directories = []
        segments_directories = self._collect_canonical_directories(
            'segments',
            example_scores=example_scores,
            )
        for segments_directory in segments_directories:
            for name in os.listdir(segments_directory):
                if not name[0].isalpha():
                    continue
                segment_directory = os.path.join(segments_directory, name)
                if not os.path.isdir(segment_directory):
                    continue
                segment_directories.append(segment_directory)
        return segment_directories

    def _collect_segment_files(self, example_scores=False):
        segment_files = []
        segment_directories = self._collect_segment_directories(
            example_scores=example_scores,
            )
        for segment_directory in segment_directories:
            for name in os.listdir(segment_directory):
                if not name[0].isalpha():
                    continue
                if name.endswith('.pyc'):
                    continue
                segment_file = os.path.join(segment_directory, name)
                segment_files.append(segment_file)
        return segment_files

    def _collect_stylesheets(self, example_scores=False):
        stylesheets = []
        stylesheets_directories = self._collect_canonical_directories(
            'stylesheets',
            example_scores=example_scores,
            )
        for stylesheets_directory in stylesheets_directories:
            for name in os.listdir(stylesheets_directory):
                if not name[0].isalpha():
                    continue
                stylesheet = os.path.join(stylesheets_directory, name)
                if not os.path.isfile(stylesheet):
                    continue
                stylesheets.append(stylesheet)
        return stylesheets

    def _collect_test_files(self, example_scores=False):
        test_files = []
        test_directories = self._collect_canonical_directories(
            'test',
            example_scores=example_scores,
            )
        for test_directory in test_directories:
            for name in os.listdir(test_directory):
                if not name[0].isalpha():
                    continue
                test_file = os.path.join(test_directory, name)
                if not os.path.isfile(test_file):
                    continue
                test_files.append(test_file)
        return test_files

    def _confirm_segment_names(self, score_directory):
        segments_directory = os.path.join(score_directory, 'segments')
        view_name = self._read_view_name(
            segments_directory,
            )
        view_inventory = self._read_view_inventory(segments_directory)
        if not view_inventory or view_name not in view_inventory:
            view_name = None
        segment_paths = self._list_visible_asset_paths('segments')
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
        if not result:
            return False
        return segment_names

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
                if not result:
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

    def _directory_to_asset_identifier(self, directory):
        assert os.path.isdir(directory), repr(directory)
        directory_name = self._path_to_directory_name(directory)
        asset_identifier = self._directory_name_to_asset_identifier[
            directory_name]
        return asset_identifier

    def _directory_to_file_extension(self, directory):
        file_extension = ''
        if self._is_known_directory(directory, 'makers'):
            file_extension = '.py'
        elif self._is_known_directory(directory, 'stylesheets'):
            file_extension = '.ily'
        elif self._is_known_directory(directory, 'test'):
            file_extension = '.py'
        return file_extension

    def _directory_name_to_directory_entry_predicate(self, directory_name):
        file_prototype = (
            'build',
            'distribution',
            'etc',
            'makers',
            'stylesheets',
            'test',
            )
        package_prototype = (
            'materials',
            'segments',
            'scores',
            )
        if directory_name in file_prototype:
            return self._is_valid_file_directory_entry
        elif directory_name in package_prototype:
            return self._is_valid_package_directory_entry
        else:
            raise ValueError(directory_name)

    def _directory_name_to_file_name_predicate(self, directory_name):
        dash_case_prototype = (
            'build',
            'distribution',
            'etc',
            'stylesheets',
            )
        if directory_name in dash_case_prototype:
            return stringtools.is_dash_case
        elif directory_name == 'makers':
            return stringtools.is_upper_camel_case
        elif directory_name == 'test':
            return stringtools.is_snake_case

    def _directory_to_file_name_predicate(self, directory):
        directory_name = self._path_to_directory_name(directory)
        dash_case_prototype = (
            'build',
            'distribution',
            'etc',
            'stylesheets',
            )
        if directory_name in dash_case_prototype:
            return stringtools.is_dash_case
        elif directory_name == 'makers':
            return stringtools.is_upper_camel_case
        elif directory_name == 'test':
            return stringtools.is_snake_case

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

    def _find_up_to_date_path(
        self,
        directory_name,
        inside_score=True,
        must_have_file=False,
        system=True,
        ):
        example_score_packages = False
        composer_score_packages = False
        if system and inside_score:
            example_score_packages = True
        elif not system and inside_score:
            composer_score_packages = True
        else:
            Exception
        paths = self._list_asset_paths(
            directory_name,
            composer_score_packages=composer_score_packages,
            example_score_packages=example_score_packages,
            )
        if directory_name == 'scores':
            if system:
                scores_directory = \
                    configuration.abjad_ide_example_scores_directory
            else:
                scores_directory = configuration.composer_scores_directory
            paths = []
            for directory_entry in sorted(os.listdir(scores_directory)):
                if not directory_entry[0].isalpha():
                    continue
                path = os.path.join(scores_directory, directory_entry)
                if os.path.isdir(path):
                    paths.append(path)
        for path in paths:
            if (self._is_git_versioned(path) and self._is_up_to_date(path)
                and
                (not must_have_file or self._find_first_file_name(path))):
                return path

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

    def _gather_segment_files(self, score_directory, file_name):
        segments_directory = os.path.join(score_directory, 'segments')
        build_directory = os.path.join(score_directory, 'build')
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
            score_package = self._path_to_package(score_directory)
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
            self._io_manager._display(messages)
            if not self._io_manager._confirm():
                return
        if not os.path.exists(build_directory):
            os.mkdir(build_directory)
        pairs = zip(source_file_paths, target_file_paths)
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

    def _get_available_path_in_directory(self, directory):
        asset_identifier = self._directory_to_asset_identifier(directory)
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

    def _get_current_directory(self):
        if os.path.normpath(self._session.manifest_current_directory) == \
            os.path.normpath(configuration.composer_scores_directory):
            return
        if os.path.normpath(self._session.manifest_current_directory) == \
            os.path.normpath(configuration.abjad_ide_example_scores_directory):
            return
        return self._session.manifest_current_directory

    def _get_directory_names(self, directory):
        result = []
        directory_names = self._list_directory_names(directory)
        for directory_name in directory_names:
            if not directory_name in self._known_directory_names:
                continue
            result.append(directory_name)
        return result

    def _get_file_path_ending_with(self, directory, string):
        for file_name in self._list_directory(directory):
            if file_name.endswith(string):
                file_path = os.path.join(directory, file_name)
                return file_path

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

    def _get_name_metadatum(self, directory):
        metadata_py_path = os.path.join(directory, '__metadata__.py')
        name = self._get_metadatum(metadata_py_path, 'name')
        if not name:
            parts = metadata_py_path.split(os.path.sep)
            directory_name = parts[-2]
            name = directory_name.replace('_', ' ')
        return name

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

    def _get_previous_segment_path(self, directory):
        paths = self._list_visible_asset_paths('segments')
        for i, path in enumerate(paths):
            if path == directory:
                break
        else:
            message = 'can not find segment package path.'
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
            process = self._io_manager.make_subprocess(command)
        line = self._io_manager._read_one_line_from_pipe(process.stdout)
        return line

    @staticmethod
    def _get_score_package_directory_name(path):
        line = path
        path = configuration.abjad_ide_example_scores_directory
        line = line.replace(path, '')
        path = configuration.composer_scores_directory
        line = line.replace(path, '')
        line = line.lstrip(os.path.sep)
        return line

    def _get_title_metadatum(self, score_directory, year=True):
        metadata_py_path = os.path.join(score_directory, '__metadata__.py')
        if year and self._get_metadatum(metadata_py_path, 'year'):
            result = '{} ({})'
            result = result.format(
                self._get_title_metadatum(score_directory, year=False),
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
            if not result:
                return
            command = 'git add -A {}'
            command = command.format(path)
            assert isinstance(command, str)
            self._io_manager.run_command(command)

    def _git_commit(self, path, commit_message=None):
        change = systemtools.TemporaryDirectoryChange(directory=path)
        with change:
            self._io_manager._session._attempted_method = '_git_commit'
            if self._io_manager._session.is_test:
                return
            if commit_message is None:
                getter = self._io_manager._make_getter()
                getter.append_string('commit message')
                commit_message = getter._run(io_manager=self._io_manager)
                if commit_message is None:
                    return
                message = 'commit message will be: "{}"'
                message = message.format(commit_message)
                self._io_manager._display(message)
                result = self._io_manager._confirm()
                if not result:
                    return
            message = self._get_score_package_directory_name(path)
            message = message + ' ...'
            command = 'git commit -m "{}" {}; git push'
            command = command.format(commit_message, path)
            self._io_manager.run_command(command, capitalize=False)

    def _git_revert(self, path):
        change = systemtools.TemporaryDirectoryChange(directory=path)
        with change:
            self._io_manager._session._attempted_method = '_git_revert'
            if self._io_manager._session.is_test:
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
            if not result:
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
            self._io_manager._session._attempted_method = '_git_status'
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
            if self._io_manager._session.is_test:
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
        if result.startswith('!'):
            statement = result[1:]
            self._io_manager._invoke_shell(statement)
        elif result in self._command_name_to_command:
            command = self._command_name_to_command[result]
            if command.argument_name == 'current_directory':
                current_directory = self._session.manifest_current_directory
                command(current_directory)
            else:
                command()
        elif (result.endswith('!') and
            result[:-1] in self._command_name_to_command):
            result = result[:-1]
            self._command_name_to_command[result]()
        elif os.path.sep in result:
            self._handle_numeric_user_input(result)
        else:
            current_score_directory = self._session.current_score_directory
            aliased_path = configuration.aliases.get(result, None)
            if current_score_directory and aliased_path:
                aliased_path = os.path.join(
                    current_score_directory,
                    aliased_path,
                    )
                if os.path.isfile(aliased_path):
                    self._io_manager.open_file(aliased_path)
                else:
                    message = 'file does not exist: {}.'
                    message = message.format(aliased_path)
                    self._io_manager._display(message)
            else:
                message = 'unknown command: {!r}.'
                message = message.format(result)
                self._io_manager._display([message, ''])

    def _handle_numeric_user_input(self, result):
        if os.path.isfile(result):
            self._io_manager.open_file(result)
        elif os.path.isdir(result):
            base_name = os.path.basename(result)
            if base_name in self._known_directory_names:
                self._run_wrangler_menu(base_name)
            else:
                self._run_package_manager_menu(result)
        else:
            message = 'must be file or directory: {!r}.'
            message = message.format(result)
            raise Exception(message)

    def _interpret_file_ending_with(self, directory, string):
        r'''Typesets TeX file.
        Calls ``pdflatex`` on file TWICE.
        Some LaTeX packages like ``tikz`` require two passes.
        '''
        directory_path = directory
        file_path = self._get_file_path_ending_with(directory_path, string)
        if not file_path:
            message = 'file ending in {!r} not found.'
            message = message.format(string)
            self._io_manager._display(message)
            return
        input_directory = os.path.dirname(file_path)
        output_directory = input_directory
        basename = os.path.basename(file_path)
        input_file_name_stem, file_extension = os.path.splitext(basename)
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
            self._handle_candidate(
                candidate_path,
                destination_path,
                )

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
        current_directory = self._session.manifest_current_directory
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
    def _is_inner_score_directory(path):
        if not isinstance(path, str):
            return False
        if path.startswith(configuration.composer_scores_directory):
            scores_directory = configuration.composer_scores_directory
        elif path.startswith(configuration.abjad_ide_example_scores_directory):
            scores_directory = configuration.abjad_ide_example_scores_directory
        else:
            return False
        scores_directory_parts_count = len(scores_directory.split(os.path.sep))
        parts = path.split(os.path.sep)
        if len(parts) == scores_directory_parts_count + 2:
            if parts[-1] == parts[-2]:
                return True
        return False

    def _is_known_directory(self, path, directory_name=None):
        parent_directory = os.path.dirname(path)
        if self._is_inner_score_directory(parent_directory):
            base_name = os.path.basename(path)
            if (directory_name is None and 
                base_name in self._known_directory_names):
                return True
            if (base_name == directory_name and
                base_name in self._known_directory_names):
                return True
        return False

    @staticmethod
    def _is_material_directory(path):
        if not isinstance(path, str):
            return False
        if path.startswith(configuration.composer_scores_directory):
            scores_directory = configuration.composer_scores_directory
        elif path.startswith(configuration.abjad_ide_example_scores_directory):
            scores_directory = configuration.abjad_ide_example_scores_directory
        else:
            return False
        scores_directory_parts_count = len(scores_directory.split(os.path.sep))
        parts = path.split(os.path.sep)
        if len(parts) == scores_directory_parts_count + 4:
            if parts[-2] == 'materials':
                return True
        return False

    @staticmethod
    def _is_outer_score_directory(path):
        if not isinstance(path, str):
            return False
        if path.startswith(configuration.composer_scores_directory):
            scores_directory = configuration.composer_scores_directory
        elif path.startswith(configuration.abjad_ide_example_scores_directory):
            scores_directory = configuration.abjad_ide_example_scores_directory
        else:
            return False
        scores_directory_parts_count = len(scores_directory.split(os.path.sep))
        parts = path.split(os.path.sep)
        if len(parts) == scores_directory_parts_count + 1:
            return True
        return False

    @staticmethod
    def _is_path_in_score(path):
        if not isinstance(path, str):
            return False
        if path.startswith(configuration.composer_scores_directory):
            scores_directory = configuration.composer_scores_directory
        elif path.startswith(configuration.abjad_ide_example_scores_directory):
            scores_directory = configuration.abjad_ide_example_scores_directory
        else:
            return False
        scores_directory_parts_count = len(scores_directory.split(os.path.sep))
        parts = path.split(os.path.sep)
        if scores_directory_parts_count < len(parts):
            return True
        return False

    @staticmethod
    def _is_scores_directory(path):
        if path == configuration.composer_scores_directory:
            return True
        if path == configuration.abjad_ide_example_scores_directory:
            return True
        return False

    @staticmethod
    def _is_segment_directory(path):
        if not isinstance(path, str):
            return False
        if path.startswith(configuration.composer_scores_directory):
            scores_directory = configuration.composer_scores_directory
        elif path.startswith(configuration.abjad_ide_example_scores_directory):
            scores_directory = configuration.abjad_ide_example_scores_directory
        else:
            return False
        scores_directory_parts_count = len(scores_directory.split(os.path.sep))
        parts = path.split(os.path.sep)
        if len(parts) == scores_directory_parts_count + 4:
            if parts[-2] == 'segments':
                return True
        return False

    def _is_up_to_date(self, path):
        git_status_lines = self._get_git_status_lines(path)
        git_status_lines = git_status_lines or ['']
        first_line = git_status_lines[0]
        return first_line == ''

    def _is_valid_file_directory_entry(self, expr, directory_name):
        if expr[0].isalpha():
            if not expr.endswith('.pyc'):
                name, file_extension = os.path.splitext(expr)
                file_name_predicate = \
                    self._directory_name_to_file_name_predicate(directory_name)
                required_file_extension = \
                    self._directory_name_to_file_extension.get(
                        directory_name, '')
                if file_name_predicate(name):
                    if required_file_extension == '':
                        return True
                    elif required_file_extension == file_extension:
                        return True
        return False

    def _is_valid_package_directory_entry(self, expr, directory_name=None):
        if expr[0].isalpha():
            if not expr.endswith('.pyc'):
                if '.' not in expr:
                    return True
        return False

    def _list_asset_paths(
        self,
        directory_name,
        composer_score_packages=True,
        example_score_packages=True,
        valid_only=True,
        ):
        result = []
        directory_entry_predicate = \
            self._directory_name_to_directory_entry_predicate(
            directory_name)
        directories = []
        if directory_name == 'scores':
            if example_score_packages:
                directories.append(
                    configuration.abjad_ide_example_scores_directory)
            if composer_score_packages:
                directories.append(configuration.composer_scores_directory)
        else:
            score_directories = self._list_score_directories(
                composer_score_packages=composer_score_packages,
                example_score_packages=example_score_packages,
                )
            directories = [
                os.path.join(_, directory_name)
                for _ in score_directories
                ]
        for directory in directories:
            if not directory:
                continue
            if not os.path.exists(directory):
                continue
            directory_entries = sorted(os.listdir(directory))
            for directory_entry in directory_entries:
                if valid_only:
                    if not directory_entry_predicate(
                        directory_entry,
                        directory_name,
                        ):
                        continue
                path = os.path.join(directory, directory_entry)
                if directory_name == 'scores':
                    path = os.path.join(path, directory_entry)
                result.append(path)
        return result

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
        composer_score_packages=False,
        example_score_packages=False,
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

    def _list_visible_asset_paths(self, directory_name):
        if os.path.isdir(directory_name):
            directory_name = self._path_to_directory_name(directory_name)
        entries = self._make_asset_menu_entries(directory_name)
        paths = [_[-1] for _ in entries]
        return paths

    def _make_asset_menu_entries(
        self,
        directory_name,
        apply_current_directory=True,
        set_view=True,
        ):
        paths = self._list_asset_paths(directory_name)
        if (apply_current_directory or set_view) and self._session.is_in_score:
            paths = [
                _ for _ in paths
                if _.startswith(self._session.current_score_directory)
                ]
        strings = []
        for path in paths:
            string = self._path_to_asset_menu_display_string(path)
            strings.append(string)
        pairs = list(zip(strings, paths))
        if (not self._session.is_in_score and not directory_name == 'scores'):
            def sort_function(pair):
                string = pair[0]
                if '(' not in string:
                    return string
                open_parenthesis_index = string.find('(')
                assert string.endswith(')')
                annotation = string[open_parenthesis_index:]
                annotation = annotation.replace("'", '')
                annotation = stringtools.strip_diacritics(annotation)
                return annotation
            pairs.sort(key=lambda _: sort_function(_))
        else:
            def sort_function(pair):
                string = pair[0]
                string = stringtools.strip_diacritics(string)
                string = string.replace("'", '')
                return string
            pairs.sort(key=lambda _: sort_function(_))
        entries = []
        for string, path in pairs:
            entry = (string, None, None, path)
            entries.append(entry)
        if set_view:
            current_score_directory = self._session.current_score_directory
            if current_score_directory is None:
                directory_token = directory_name
            else:
                directory_token = os.path.join(
                    current_score_directory,
                    directory_name,
                    )
            entries = self._filter_asset_menu_entries_by_view(
                directory_token,
                entries,
                )
        if not self._session.is_test:
            entries = [_ for _ in entries if 'Example Score' not in _[0]]
        if directory_name == 'scores' and self._session.is_test:
            entries = [_ for _ in entries if 'Example Score' in _[0]]
        return entries

    def _make_asset_selection_menu(self, directory_name):
        menu = self._io_manager._make_menu(name='asset selection')
        menu_entries = self._make_asset_menu_entries(directory_name)
        menu.make_asset_section(menu_entries=menu_entries)
        return menu

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

    def _make_command_menu_sections(
        self,
        menu,
        menu_section_names=None,
        current_path=None,
        ):
        assert current_path is not None, repr(current_path)
        directory = current_path
        methods = []
        methods_ = self._get_commands()
        is_in_score = self._session.is_in_score
        required_files = ()
        optional_files = ()
        directory_name = self._path_to_directory_name(directory)
        if (self._is_material_directory(directory) or
            self._is_segment_directory(directory)):
            package_contents = self._directory_name_to_package_contents[
                directory_name]
            required_files = package_contents['required_files']
            optional_files = package_contents['optional_files']
        files = required_files + optional_files
        is_in_score_directory = self._is_in_score_directory()
        directory_name_ = os.path.basename(directory)
        parent_directory_name = directory.split(os.path.sep)[-2]
        is_home = False
        if self._is_scores_directory(directory):
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
                directory_name_ not in method_.directories and
                parent_directory_name not in method_.parent_directories):
                continue
            if method_.file_ is not None and method_.file_ not in files:
                continue
            if method_.in_score_directory_only and not is_in_score_directory:
                continue
            if method_.never_in_score_directory and is_in_score_directory:
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

    def _make_file(self, directory):
        assert os.path.isdir(directory), repr(directory)
        contents = ''
        file_extension = self._directory_to_file_extension(directory)
        if file_extension == '.py':
            contents == self._unicode_directive
        getter = self._io_manager._make_getter()
        getter.append_string('file name')
        name = getter._run(io_manager=self._io_manager)
        if name is None:
            return
        name = stringtools.strip_diacritics(name)
        directory_name = os.path.basename(directory)
        file_name_predicate = self._directory_to_file_name_predicate(directory)
        if file_name_predicate == stringtools.is_dash_case:
            name = self._to_dash_case(name)
        name = name.replace(' ', '_')
        if not directory_name == 'makers':
            name = name.lower()
        if not name.endswith(file_extension):
            name = name + file_extension
        file_path = os.path.join(directory, name)
        self._io_manager.write(file_path, contents)
        self._io_manager.edit(file_path)

    def _make_main_menu(
        self,
        explicit_header,
        current_path=None,
        directory_name=None,
        ):
        assert directory_name is None, repr(directory_name)
        assert current_path is not None, repr(current_path)
        directory = current_path
        assert isinstance(explicit_header, str), repr(explicit_header)
        name = stringtools.to_space_delimited_lowercase(type(self).__name__)
        menu = self._io_manager._make_menu(
            explicit_header=explicit_header,
            name=name,
            )
        if (self._is_material_directory(directory) or
            self._is_segment_directory(directory) or
            self._is_inner_score_directory(directory)):
            self._make_package_asset_menu_section(directory, menu)
        else:
            self._make_wrangler_asset_menu_section(menu, directory)
        assert os.path.isdir(directory), repr(directory)
        self._make_command_menu_sections(
            menu, 
            #directory_name, 
            current_path=directory,
            )
        return menu

    def _make_material_or_segment_package(self, directory):
        assert os.path.isdir(directory), repr(directory)
        assert self._session.is_in_score
        new_directory = directory
        path = self._get_available_path_in_directory(new_directory)
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
        paths = self._list_visible_asset_paths(directory)
        if path not in paths:
            self._clear_view(directory_name)
        self._run_package_manager_menu(new_path)

    def _make_package_asset_menu_section(self, directory, menu):
        directory_entries = self._list_directory(directory, smart_sort=True)
        menu_entries = []
        for directory_entry in directory_entries:
            clean_directory_entry = directory_entry
            if directory_entry.endswith('/'):
                clean_directory_entry = directory_entry[:-1]
            path = os.path.join(directory, clean_directory_entry)
            menu_entry = (directory_entry, None, None, path)
            menu_entries.append(menu_entry)
        menu.make_asset_section(menu_entries=menu_entries)

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

    def _make_score_package(self):
        message = 'enter title'
        getter = self._io_manager._make_getter()
        getter.append_string(message)
        title = getter._run(io_manager=self._io_manager)
        if not title:
            return
        package_name = stringtools.strip_diacritics(title)
        package_name = stringtools.to_snake_case(package_name)
        outer_score_directory = os.path.join(
            configuration.composer_scores_directory,
            package_name,
            )
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
        self._clear_view('scores')
        inner_score_directory = os.path.join(
            outer_score_directory, 
            package_name,
            )
        self._run_package_manager_menu(inner_score_directory)

    def _make_secondary_asset_menu_entries(self, directory_path):
        menu_entries = []
        for entry in os.listdir(directory_path):
            if entry in self._known_secondary_assets:
                path = os.path.join(directory_path, entry)
                menu_entry = (entry, None, None, path)
                menu_entries.append(menu_entry)
        return menu_entries

    def _make_wrangler_asset_menu_section(
        self,
        menu,
        directory,
        ):
        menu_entries = []
        if directory is not None:
            current_directory = directory
        else:
            current_directory = self._get_current_directory()
        if current_directory:
            menu_entries_ = self._make_secondary_asset_menu_entries(
                current_directory)
            menu_entries.extend(menu_entries_)
        directory_name = self._path_to_directory_name(directory)
        menu_entries.extend(self._make_asset_menu_entries(directory_name))
        if menu_entries:
            section = menu.make_asset_section(menu_entries=menu_entries)
            assert section is not None
            section._group_by_annotation = not directory_name == 'scores'

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
            return False
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
        message = 'will {} ...'.format(verb)
        messages.append(message)
        for path in paths:
            message = '   ' + path
            messages.append(message)
        self._io_manager._display(messages)
        result = self._io_manager._confirm()
        if not result:
            return
        self._io_manager.open_file(paths)

    def _parse_paper_dimensions(self, score_directory):
        string = self._get_metadatum(
            score_directory,
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
        score_directories = (
            configuration.abjad_ide_example_scores_directory,
            configuration.composer_scores_directory,
            )
        if path.startswith(score_directories):
            score_directory = self._path_to_score_directory(path)
            metadata_py_path = os.path.join(score_directory, '__metadata__.py')
            metadata = self._get_metadata(metadata_py_path)
            if metadata:
                year = metadata.get('year')
                title = metadata.get('title')
                if self._is_inner_score_directory(path) and year:
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

    def _path_to_asset_menu_display_string(self, path, score_directory=None):
        asset_name = os.path.basename(path)
        allow_asset_name_underscores = False
        if 'test' in path.split(os.path.sep):
            allow_asset_name_underscores = True
        if '_' in asset_name and not allow_asset_name_underscores:
            asset_name = stringtools.to_space_delimited_lowercase(asset_name)
        if self._is_segment_directory(path):
            metadata_py_path = os.path.join(path, '__metadata__.py')
            segment_name = self._get_metadatum(
                metadata_py_path,
                'name',
                )
            asset_name = segment_name or asset_name
        if self._session.is_in_score or score_directory is not None:
            string = asset_name
        else:
            annotation = self._path_to_annotation(path)
            if self._is_inner_score_directory(path):
                string = annotation
            else:
                string = '{} ({})'.format(asset_name, annotation)
        return string

    def _path_to_directory_name(self, path):
        if self._is_scores_directory(path):
            return 'scores'
        if self._is_outer_score_directory(path):
            return 'score'
        if self._is_inner_score_directory(path):
            return 'score'
        for part in reversed(path.split(os.path.sep)):
            if part in self._known_directory_names:
                return part
        raise ValueError(path)

    def _path_to_menu_header(self, path):
        header_parts = []
        if path == configuration.composer_scores_directory:
            return 'Abjad IDE - all score directories'
        score_directory = self._path_to_score_directory(path)
        score_part = self._get_title_metadatum(score_directory)
        score_part_count = len(score_directory.split(os.path.sep))
        path_parts = path.split(os.path.sep)
        if score_part_count == len(path_parts):
            return score_part
        header_parts.append(score_part)
        interesting_path_parts = path_parts[score_part_count:]
        directory_name = interesting_path_parts[0]
        directory_part = '{} directory'
        directory_part = directory_part.format(directory_name)
        header_parts.append(directory_part)
        if len(interesting_path_parts) == 1:
            header = ' - '.join(header_parts)
            return header
        package_name = interesting_path_parts[1]
        if directory_name in ('materials', 'segments'):
            package_path = path_parts[:score_part_count+2]
            package_path = os.path.join('/', *package_path)
            package_path = os.path.normpath(package_path)
            package_part = self._get_name_metadatum(package_path)
            header_parts.append(package_part)
        else:
            raise ValueError(directory_name)
        if len(interesting_path_parts) == 2:
            header = ' - '.join(header_parts)
            return header
        raise NotImplementedError

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
        if os.path.normpath(score_path) == os.path.normpath(
            configuration.composer_scores_directory):
            return
        if os.path.normpath(score_path) == os.path.normpath(
            configuration.abjad_ide_example_scores_directory):
            return
        return score_path

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
            message = message.format(directory_token)
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

    def _run_main_menu(self, input_=None):
        self._session._reinitialize()
        type(self).__init__(self, session=self._session)
        if input_:
            self._session._pending_input = input_
        state = systemtools.NullContextManager()
        if self._session.is_test:
            views = os.path.join(
                configuration.abjad_ide_views_directory,
                '__metadata__.py',
                )
            empty_views = os.path.join(
                configuration.abjad_ide_boilerplate_directory,
                '__metadata__.py',
                )
            paths_to_keep = []
            paths_to_keep.append(views)
            state = systemtools.FilesystemState(keep=paths_to_keep)
        with state:
            self._session._pending_redraw = True
            if self._session.is_test:
                shutil.copyfile(empty_views, views)
            while True:
                self._run_wrangler_menu('scores')
                if self._session.is_quitting:
                    break
        self._io_manager._clean_up()

    def _run_package_manager_menu(self, directory):
        assert os.path.sep in directory, repr(directory)
        self._session._pending_redraw = True
        while True:
            self._session._manifest_current_directory = directory
            os.chdir(directory)
            menu_header = self._path_to_menu_header(directory)
            menu = self._make_main_menu(
                explicit_header=menu_header,
                current_path=directory,
                )
            result = menu._run(io_manager=self._io_manager)
            if self._session.is_quitting:
                return
            if result is None:
                continue
            self._handle_input(result)
            if self._session.is_quitting:
                return

    def _run_wrangler_menu(self, directory_name):
        assert (directory_name in self._known_directory_names or
            directory_name == 'scores'), repr(directory_name)
        if (directory_name == 'scores' or not self._session.is_in_score):
            current_directory = configuration.composer_scores_directory
        else:
            current_directory = os.path.join(
                self._session.current_score_directory,
                directory_name,
                )
        if not os.path.exists(current_directory):
            message = 'directory does not exist: {}.'
            message = message.format(current_directory)
            self._io_manager._display(message)
            return
        self._session._pending_redraw = True
        self._session._manifest_current_directory = current_directory
        if self._session.is_in_score:
            menu_header = self._path_to_menu_header(
                self._session.manifest_current_directory)
        elif directory_name == 'scores':
            menu_header = 'Abjad IDE - all score directories'
        else:
            menu_header = 'Abjad IDE - all {} directories'
            menu_header = menu_header.format(directory_name)
        menu = self._make_main_menu(
            explicit_header=menu_header,
            #directory_name=directory_name,
            current_path=current_directory,
            )
        while True:
            self._session._manifest_current_directory = current_directory
            os.chdir(current_directory)
            if self._session._pending_menu_rebuild:
                menu = self._make_main_menu(
                    explicit_header=menu_header,
                    #directory_name=directory_name,
                    current_path=current_directory,
                    )
                self._session._pending_menu_rebuild = False
            result = menu._run(io_manager=self._io_manager)
            if self._session.is_quitting:
                return
            if result is None:
                continue
            self._handle_input(result)
            if self._session.is_quitting:
                return

    def _select_score_directory(self, directory_name):
        display_strings, keys = [], []
        paths = self._list_asset_paths('scores')
        for path in paths:
            title = self._get_title_metadatum(path)
            display_strings.append(title)
            keys.append(path)
        assert len(display_strings) == len(keys), repr((display_strings, keys))
        sequences = [display_strings, [None], [None], keys]
        menu_entries = sequencetools.zip_sequences(sequences, cyclic=True)
        menu_entries.sort(key=lambda _: stringtools.strip_diacritics(_[0]))
        current_directory = self._get_current_directory()
        if current_directory is not None:
            menu_header = self._path_to_menu_header(current_directory)
        elif directory_name == 'scores':
            menu_header = 'Abjad IDE - all score directories'
        else:
            menu_header = 'Abjad IDE - all {} directories'
            menu_header = menu_header.format(directory_name)
        selector = self._io_manager._make_selector(
            menu_entries=menu_entries,
            menu_header=menu_header,
            target_name='target score package',
            )
        result = selector._run(io_manager=self._io_manager)
        if result is None:
            return
        if result not in paths:
            return
        return result

    def _select_view(
        self,
        directory_name,
        is_ranged=False,
        ):
        if self._session.is_in_score:
            directory_token = self._session.manifest_current_directory
        else:
            directory_token = directory_name
        view_inventory = self._read_view_inventory(
            directory_token,
            )
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
        current_directory = self._get_current_directory()
        if current_directory is not None:
            menu_header = self._path_to_menu_header(current_directory)
        elif directory_name == 'scores':
            menu_header = 'Abjad IDE - all score directories'
        else:
            menu_header = 'Abjad IDE - all {} directories'
            menu_header = menu_header.format(directory_name)
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

    def _select_visible_asset_path(
        self,
        directory,
        infinitive_phrase=None,
        ):
        getter = self._io_manager._make_getter()
        asset_identifier = self._directory_to_asset_identifier(directory)
        message = 'enter {}'.format(asset_identifier)
        if infinitive_phrase:
            message = message + ' ' + infinitive_phrase
        directory_name = self._path_to_directory_name(directory)
        dummy_menu = self._io_manager._make_menu()
        self._make_wrangler_asset_menu_section(dummy_menu, directory)
        asset_section = dummy_menu._asset_section
        getter.append_menu_section_item(
            message,
            asset_section,
            )
        numbers = getter._run(io_manager=self._io_manager)
        if numbers is None:
            return
        if not len(numbers) == 1:
            return
        number = numbers[0]
        index = number - 1
        paths = [_.return_value for _ in asset_section.menu_entries]
        path = paths[index]
        return path

    def _select_visible_asset_paths(self, directory_name):
        getter = self._io_manager._make_getter()
        asset_identifier = self._directory_name_to_asset_identifier[
            directory_name]
        message = 'enter {}(s) to remove'
        message = message.format(asset_identifier)
        menu = self._make_asset_selection_menu(directory_name)
        asset_section = menu['assets']
        getter.append_menu_section_range(
            message,
            asset_section,
            )
        numbers = getter._run(io_manager=self._io_manager)
        if numbers is None:
            return
        indices = [_ - 1 for _ in numbers]
        paths = [_.return_value for _ in asset_section.menu_entries]
        paths = sequencetools.retain_elements(paths, indices)
        return paths

    @staticmethod
    def _sort_ordered_dictionary(dictionary):
        new_dictionary = type(dictionary)()
        for key in sorted(dictionary):
            new_dictionary[key] = dictionary[key]
        return new_dictionary

    @staticmethod
    def _strip_annotation(display_string):
        if not display_string.endswith(')'):
            return display_string
        index = display_string.find('(')
        result = display_string[:index]
        result = result.strip()
        return result

    def _supply_global_metadata_py(self):
        metadata_py_path = configuration.abjad_ide_views_metadata_py_path
        if not os.path.exists(metadata_py_path):
            metadata = self._get_metadata(metadata_py_path)
            self._write_metadata_py(metadata_py_path, metadata)

    def _supply_global_views_file(self, directory_name):
        from ide.tools import idetools
        views_py_path = self._get_views_py_path(directory_name)
        if not os.path.isfile(views_py_path):
            self._write_view_inventory(
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
            self._git_add(path)
            assert self._get_unadded_asset_paths(path) == []
            assert self._get_added_asset_paths(path) == [path_1, path_2]
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
            self._get_revert(path)
        assert self._get_modified_asset_paths(path) == []
        assert self._is_up_to_date(path)
        return True

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

    def _update_order_dependent_segment_metadata(self):
        paths = self._list_visible_asset_paths('segments')
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
        measure_count = self._get_metadatum(
            path,
            'measure_count',
            )
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
            measure_count = self._get_metadatum(
                path,
                'measure_count',
                )
            if not measure_count:
                return
            next_bar_number = first_bar_number + measure_count

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
        'dfk',
        argument_name='current_directory',
        description='definition file - check',
        file_='definition.py',
        outside_score=False,
        section='definition_file',
        )
    def check_definition_file(self, directory, dry_run=False):
        r'''Checks definition file.

        Returns none.
        '''
        assert os.path.isdir(directory), repr(directory)
        definition_path = os.path.join(directory, 'definition.py')
        if not os.path.isfile(definition_path):
            message = 'file not found: {}.'
            message = message.format(definition_path)
            self._io_manager._display(message)
            return
        inputs, outputs = [], []
        if dry_run:
            inputs.append(definition_path)
            return inputs, outputs
        stdout_lines, stderr_lines = self._io_manager.interpret_file(
            definition_path)
        if stderr_lines:
            messages = [definition_path + ' FAILED:']
            messages.extend('    ' + _ for _ in stderr_lines)
            self._io_manager._display(messages)
        else:
            message = '{} OK.'.format(definition_path)
            self._io_manager._display(message)

    @Command(
        'dfk*',
        argument_name='current_directory',
        directories=('materials', 'segments'),
        outside_score=False,
        section='star',
        )
    def check_every_definition_file(self, directory):
        r'''Checks definition file in every package.

        Returns none.
        '''
        assert os.path.isdir(directory), repr(directory)
        directory_name = self._path_to_directory_name(directory)
        paths = self._list_visible_asset_paths(directory_name)
        inputs, outputs = [], []
        for path in paths:
            inputs_, outputs_ = self.check_definition_file(path, dry_run=True)
            inputs.extend(inputs_)
            outputs.extend(outputs_)
        messages = self._format_messaging(inputs, outputs, verb='check')
        self._io_manager._display(messages)
        result = self._io_manager._confirm()
        if not result:
            return
        start_time = time.time()
        for path in paths:
            self.check_definition_file(path)
        stop_time = time.time()
        total_time = stop_time - start_time
        total_time = int(total_time)
        message = 'total time: {} seconds.'
        message = message.format(total_time)
        self._io_manager._display(message)

    @Command(
        'mc',
        argument_name='current_directory',
        directories=('build'),
        outside_score=False,
        section='build',
        )
    def collect_segment_lilypond_files(self, directory):
        r'''Copies ``illustration.ly`` files from segment packages to build
        directory.

        Trims top-level comments, includes and directives from each
        ``illustration.ly`` file.

        Trims header and paper block from each ``illustration.ly`` file.

        Leaves score block in each ``illustration.ly`` file.

        Returns none.
        '''
        assert os.path.isdir(directory), repr(directory)
        score_directory = self._path_to_score_directory(directory)
        pairs = self._gather_segment_files(
            score_directory,
            'illustration.ly',
            )
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
                self._handle_candidate(
                    candidate_file_path,
                    target_file_path,
                    )
                self._io_manager._display('')

    @Command(
        'cp',
        argument_name='current_directory',
        is_hidden=False,
        never_in_score_directory=True,
        section='basic',
        )
    def copy(self, directory):
        r'''Copies external asset in to `directory`.

        Returns none.
        '''
        assert os.path.isdir(directory), repr(directory)
        example_scores = self._session.is_test
        if self._is_known_directory(directory):
            directory_name = os.path.basename(directory)
            if directory_name == 'build':
                assets_ = self._collect_build_files(
                    example_scores=example_scores)
            elif directory_name == 'distribution':
                assets_ = self._collect_distribution_files(
                    example_scores=example_scores)
            elif directory_name == 'etc':
                assets_ = self._collect_etc_files(
                    example_scores=example_scores)
            elif directory_name == 'makers':
                assets_ = self._collect_maker_files(
                    example_scores=example_scores)
            elif directory_name == 'materials':
                assets_ = self._collect_material_directories(
                    example_scores=example_scores)
            elif directory_name == 'segments':
                assets_ = self._collect_segment_directories(
                    example_scores=example_scores)
            elif directory_name == 'stylesheets':
                assets_ = self._collect_stylesheets(
                    example_scores=example_scores)
            elif directory_name == 'test':
                assets_ = self._collect_test_files(
                    example_scores=example_scores)
        elif self._is_material_directory(directory):
            assets_ = self._collect_material_files(
                example_scores=example_scores)
        elif self._is_segment_directory(directory):
            assets_ = self._collect_segment_files(
                example_scores=example_scores)
        else:
            raise ValueError(directory)
        selector = self._io_manager._make_selector(
            items=assets_,
            )
        source_path = selector._run(io_manager=self._io_manager)
        if not source_path:
            return
        if source_path not in assets_:
            return
        asset_name = os.path.basename(source_path)
        if os.path.sep in directory:
            target_path = os.path.join(
                directory,
                asset_name,
                )
        else:
            current_score_directory = self._session.current_score_directory
            directory_name = os.path.basename(directory)
            asset_name = os.path.basename(source_path)
            target_path = os.path.join(
                current_score_directory,
                directory_name,
                asset_name,
                )
        messages = []
        messages.append('will copy ...')
        messages.append(' FROM: {}'.format(source_path))
        messages.append('   TO: {}'.format(target_path))
        self._io_manager._display(messages)
        result = self._io_manager._confirm()
        if not result:
            return
        if os.path.isfile(source_path):
            shutil.copyfile(source_path, target_path)
        elif os.path.isdir(source_path):
            shutil.copytree(source_path, target_path)
        else:
            raise ValueError(source_path)
        self._session._pending_redraw = True

    @Command(
        '?', 
        section='system',
        )
    def display_action_command_help(self):
        r'''Displays action commands.

        Returns none.
        '''
        pass

    @Command(
        ';', 
        section='display navigation',
        )
    def display_navigation_command_help(self):
        r'''Displays navigation commands.

        Returns none.
        '''
        pass

    @Command(
        'abb',
        argument_name='current_directory',
        description='abbreviations - edit',
        outside_score=False,
        section='global files',
        )
    def edit_abbreviations_file(self, directory):
        r'''Edits abbreviations file.

        Returns none.
        '''
        assert os.path.isdir(directory), repr(directory)
        score_directory = self._path_to_score_directory(directory)
        path = os.path.join(
            score_directory,
            'materials',
            '__abbreviations__.py',
            )
        if not path or not os.path.isfile(path):
            with open(path, 'w') as file_pointer:
                file_pointer.write('')
        self._io_manager.edit(path)

    @Command(
        'df',
        argument_name='current_directory',
        description='definition file - edit',
        file_='definition.py',
        outside_score=False,
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
        directories=('materials', 'segments'),
        section='star',
        )
    def edit_every_definition_file(self, directory):
        r'''Edits definition file in every subdirectory of `directory`.

        Returns none.
        '''
        assert os.path.isdir(directory), repr(directory)
        directory_name = self._path_to_directory_name(directory)
        paths = self._list_visible_asset_paths(directory_name)
        self._open_in_every_package(paths, 'definition.py')

    @Command(
        'ill',
        argument_name='current_directory',
        description='illustrate file - edit',
        file_='__illustrate__.py',
        outside_score=False,
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
        'log', 
        description='log - edit',
        section='global files',
        )
    def edit_lilypond_log(self):
        r'''Edits LilyPond log.

        Returns none.
        '''
        from abjad.tools import systemtools
        self._session._attempted_to_open_file = True
        if self._session.is_test:
            return
        systemtools.IOManager.open_last_log()

    @Command(
        'ly',
        argument_name='current_directory',
        description='ly - edit',
        file_='illustration.ly',
        outside_score=False,
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
        'sty',
        argument_name='current_directory',
        description='stylesheet - edit',
        outside_score=False,
        section='global files',
        )
    def edit_score_stylesheet(self, directory):
        r'''Edits score stylesheet.

        Returns none.
        '''
        assert os.path.isdir(directory), repr(directory)
        score_directory = self._path_to_score_directory(directory)
        path = os.path.join(
            score_directory,
            'stylesheets',
            'stylesheet.ily',
            )
        if not path or not os.path.isfile(path):
            with open(path, 'w') as file_pointer:
                file_pointer.write('')
        self._io_manager.edit(path)

    @Command(
        'bcg',
        argument_name='current_directory',
        directories=('build'),
        outside_score=False,
        section='build',
        )
    def generate_back_cover_source(self, directory):
        r'''Generates ``back-cover.tex``.

        Returns none.
        '''
        assert os.path.isdir(directory), repr(directory)
        score_directory = self._path_to_score_directory(directory)
        replacements = {}
        catalog_number = self._get_metadatum(
            score_directory,
            'catalog_number',
            )
        if catalog_number:
            old = 'CATALOG NUMBER'
            new = str(catalog_number)
            replacements[old] = new
        composer_website = configuration.composer_website
        if self._session.is_test:
            composer_website = 'www.composer-website.com'
        if composer_website:
            old = 'COMPOSER WEBSITE'
            new = str(composer_website)
            replacements[old] = new
        price = self._get_metadatum(
            score_directory,
            'price',
            )
        if price:
            old = 'PRICE'
            new = str(price)
            replacements[old] = new
        width, height, unit = self._parse_paper_dimensions(score_directory)
        if width and height:
            old = '{PAPER_SIZE}'
            new = '{{{}{}, {}{}}}'
            new = new.format(width, unit, height, unit)
            replacements[old] = new
        self._copy_boilerplate(
            'back-cover.tex',
            os.path.join(score_directory, 'build'),
            replacements=replacements,
            )

    @Command(
        'fcg',
        argument_name='current_directory',
        directories=('build'),
        outside_score=False,
        section='build',
        )
    def generate_front_cover_source(self, directory):
        r'''Generates ``front-cover.tex``.

        Returns none.
        '''
        assert os.path.isdir(directory), repr(directory)
        score_directory = self._path_to_score_directory(directory)
        file_name = 'front-cover.tex'
        replacements = {}
        score_title = self._get_title_metadatum(
            score_directory,
            year=False,
            )
        if score_title:
            old = 'TITLE'
            new = str(score_title.upper())
            replacements[old] = new
        forces_tagline = self._get_metadatum(
            score_directory,
            'forces_tagline',
            )
        if forces_tagline:
            old = 'FOR INSTRUMENTS'
            new = str(forces_tagline)
            replacements[old] = new
        year = self._get_metadatum(
            score_directory,
            'year',
            )
        if year:
            old = 'YEAR'
            new = str(year)
            replacements[old] = new
        composer = configuration.composer_uppercase_name
        if self._session.is_test:
            composer = 'EXAMPLE COMPOSER NAME'
        if composer:
            old = 'COMPOSER'
            new = str(composer)
            replacements[old] = new
        width, height, unit = self._parse_paper_dimensions(score_directory)
        if width and height:
            old = '{PAPER_SIZE}'
            new = '{{{}{}, {}{}}}'
            new = new.format(width, unit, height, unit)
            replacements[old] = new
        self._copy_boilerplate(
            file_name,
            os.path.join(score_directory, 'build'),
            replacements=replacements,
            )

    @Command(
        'mg',
        argument_name='current_directory',
        directories=('build'),
        outside_score=False,
        section='build',
        )
    def generate_music_source(self, directory):
        r'''Generates ``music.ly``.

        Returns none.
        '''
        assert os.path.isdir(directory), repr(directory)
        score_directory = self._path_to_score_directory(directory)
        result = self._confirm_segment_names(score_directory)
        if not isinstance(result, list):
            return
        segment_names = result
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
            result = self._parse_paper_dimensions(score_directory)
            width, height, unit = result
            old = '{PAPER_SIZE}'
            new = '{{{}{}, {}{}}}'
            new = new.format(width, unit, height, unit)
            self._replace_in_file(candidate_path, old, new)
            lines = []
            for lilypond_name in lilypond_names:
                file_name = lilypond_name + '.ly'
                line = self._tab + r'\include "{}"'
                line = line.format(file_name)
                lines.append(line)
            if lines:
                new = '\n'.join(lines)
                old = '%%% SEGMENTS %%%'
                self._replace_in_file(candidate_path, old, new)
            else:
                line_to_remove = '%%% SEGMENTS %%%\n'
                self._remove_file_line(candidate_path, line_to_remove)
            stylesheet_path = os.path.join(
                score_directory,
                'stylesheets',
                'stylesheet.ily',
                )
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
            score_title = self._get_title_metadatum(
                score_directory,
                year=False,
                )
            if score_title:
                old = 'SCORE_NAME'
                new = score_title
                self._replace_in_file(candidate_path, old, new)
            annotated_title = self._get_title_metadatum(
                score_directory,
                year=True,
                )
            if annotated_title:
                old = 'SCORE_TITLE'
                new = annotated_title
                self._replace_in_file(candidate_path, old, new)
            forces_tagline = self._get_metadatum(
                score_directory,
                'forces_tagline',
                )
            if forces_tagline:
                old = 'FORCES_TAGLINE'
                new = forces_tagline
                self._replace_in_file(candidate_path, old, new)
            self._handle_candidate(
                candidate_path,
                destination_path,
                )

    @Command(
        'pg',
        argument_name='current_directory',
        directories=('build'),
        outside_score=False,
        section='build',
        )
    def generate_preface_source(self, directory):
        r'''Generates ``preface.tex``.

        Returns none.
        '''
        assert os.path.isdir(directory), repr(directory)
        score_directory = self._path_to_score_directory(directory)
        replacements = {}
        width, height, unit = self._parse_paper_dimensions(score_directory)
        if width and height:
            old = '{PAPER_SIZE}'
            new = '{{{}{}, {}{}}}'
            new = new.format(width, unit, height, unit)
            replacements[old] = new
        self._copy_boilerplate(
            'preface.tex',
            os.path.join(score_directory, 'build'),
            replacements=replacements,
            )

    @Command(
        'sg',
        argument_name='current_directory',
        directories=('build'),
        outside_score=False,
        section='build',
        )
    def generate_score_source(self, directory):
        r'''Generates ``score.tex``.

        Returns none.
        '''
        assert os.path.isdir(directory)
        score_directory = self._path_to_score_directory(directory)
        replacements = {}
        width, height, unit = self._parse_paper_dimensions(score_directory)
        if width and height:
            old = '{PAPER_SIZE}'
            new = '{{{}{}, {}{}}}'
            new = new.format(width, unit, height, unit)
            replacements[old] = new
        self._copy_boilerplate(
            'score.tex',
            os.path.join(score_directory, 'build'),
            replacements=replacements,
            )

    @Command(
        'add*',
        argument_name='current_directory',
        in_score=False,
        outside_score='home',
        section='git',
        )
    def git_add_every_package(self, directory):
        r'''Adds every asset to repository.

        Returns none.
        '''
        assert os.path.isdir(directory), repr(directory)
        directory_name = self._path_to_directory_name(directory)
        directories = self._list_visible_asset_paths(directory_name)
        self._session._attempted_method = 'git_add_every_package'
        if self._session.is_test:
            return
        inputs, outputs = [], []
        method_name = '_git_add'
        for directory in directories:
            inputs_, outputs_ = self._git_add(
                directory,
                dry_run=True,
                )
            inputs.extend(inputs_)
            outputs.extend(outputs_)
        messages = self._format_messaging(inputs, outputs, verb='add')
        self._io_manager._display(messages)
        if not inputs:
            return
        result = self._io_manager._confirm()
        if not result:
            return
        for directory in directories:
            self._git_add(directory)
        count = len(inputs)
        identifier = stringtools.pluralize('file', count)
        message = 'added {} {} to repository.'
        message = message.format(count, identifier)
        self._io_manager._display(message)

    @Command(
        'ci*',
        argument_name='current_directory',
        in_score=False,
        outside_score='home',
        section='git',
        )
    def git_commit_every_package(self, directory):
        r'''Commits every asset to repository.

        Returns none.
        '''
        assert os.path.isdir(directory), repr(directory)
        directory_name = self._path_to_directory_name(directory)
        directories = self._list_visible_asset_paths(directory_name)
        self._session._attempted_method = 'git_commit_every_package'
        if self._session.is_test:
            return
        getter = self._io_manager._make_getter()
        getter.append_string('commit message')
        commit_message = getter._run(io_manager=self._io_manager)
        if commit_message is None:
            return
        line = 'commit message will be: "{}"'.format(commit_message)
        self._io_manager._display(line)
        result = self._io_manager._confirm()
        if not result:
            return
        for directory in directories:
            self._git_commit(
                directory,
                commit_message=commit_message,
                )

    @Command(
        'st*',
        argument_name='current_directory',
        in_score=False,
        outside_score='home',
        section='git',
        )
    def git_status_every_package(self, directory):
        r'''Displays Git status of every package.

        Returns none.
        '''
        assert os.path.isdir(directory), repr(directory)
        directory_name = self._path_to_directory_name(directory)
        directories = self._list_visible_asset_paths(directory_name)
        self._session._attempted_method = 'git_status_every_package'
        directories.sort()
        for directory in directories:
            self._git_status(directory)

    @Command(
        'up*',
        argument_name='current_directory',
        in_score=False,
        outside_score='home',
        section='git',
        )
    def git_update_every_package(self, directory):
        r'''Updates every asset from repository.

        Returns none.
        '''
        assert os.path.isdir(directory), repr(directory)
        directory_name = self._path_to_directory_name(directory)
        directories = self._list_visible_asset_paths(directory_name)
        self._session._attempted_method = 'git_update_every_package'
        for directory in directories:
            messages = []
            message = self._path_to_asset_menu_display_string(directory)
            message = self._strip_annotation(message)
            message = message + ':'
            messages_ = self._git_update(
                directory,
                messages_only=True,
                )
            if len(messages_) == 1:
                message = message + ' ' + messages_[0]
                messages.append(message)
            else:
                messages_ = [self._tab + _ for _ in messages_]
                messages.extend(messages_)
            self._io_manager._display(messages, capitalize=False)

    @Command('h', description='home', section='back-home-quit')
    def go_home(self):
        r'''Goes home.

        Returns none.
        '''
        self._run_wrangler_menu('scores')

    @Command(
        'bb',
        argument_name='current_directory',
        outside_score=False,
        section='navigation',
        )
    def go_to_build_directory(self, directory):
        r'''Goes to build directory.

        Returns none.
        '''
        assert os.path.isdir(directory)
        self._run_wrangler_menu('build')

    @Command(
        'dd',
        argument_name='current_directory',
        outside_score=False,
        section='navigation',
        )
    def go_to_distribution_directory(self, directory):
        r'''Goes to distribution directory.

        Returns none.
        '''
        assert os.path.isdir(directory)
        self._run_wrangler_menu('distribution')

    @Command(
        'ee',
        argument_name='current_directory',
        outside_score=False,
        section='navigation',
        )
    def go_to_etc_directory(self, directory):
        r'''Goes to etc directory.

        Returns none.
        '''
        assert os.path.isdir(directory)
        self._run_wrangler_menu('etc')

    @Command(
        'kk',
        argument_name='current_directory',
        outside_score=False,
        section='navigation',
        )
    def go_to_makers_directory(self, directory):
        r'''Goes to makers directory.

        Returns none.
        '''
        assert os.path.isdir(directory)
        self._run_wrangler_menu('makers')

    @Command(
        'mm',
        argument_name='current_directory',
        outside_score=False,
        section='navigation',
        )
    def go_to_materials_directory(self, directory):
        r'''Goes to materials directory.

        Returns none.
        '''
        assert os.path.isdir(directory)
        self._run_wrangler_menu('materials')

    @Command(
        'ss',
        argument_name='current_directory',
        outside_score=False,
        section='navigation',
        )
    def go_to_score_directory(self, directory):
        r'''Goes to score directory.

        Returns none.
        '''
        assert os.path.isdir(directory)
        current_score_directory = self._session.current_score_directory
        self._run_package_manager_menu(current_score_directory)

    @Command(
        'gg',
        argument_name='current_directory',
        outside_score=False,
        section='navigation',
        )
    def go_to_segments_directory(self, directory):
        r'''Goes to segments directory.

        Returns none.
        '''
        assert os.path.isdir(directory)
        self._run_wrangler_menu('segments')

    @Command(
        'yy',
        argument_name='current_directory',
        outside_score=False,
        section='navigation',
        )
    def go_to_stylesheets_directory(self, directory):
        r'''Goes to stylesheets directory.

        Returns none.
        '''
        assert os.path.isdir(directory)
        self._run_wrangler_menu('stylesheets')

    @Command(
        'tt',
        argument_name='current_directory',
        outside_score=False,
        section='navigation',
        )
    def go_to_test_directory(self, directory):
        r'''Goes to test directory.

        Returns none.
        '''
        assert os.path.isdir(directory)
        self._run_wrangler_menu('test')

    @Command(
        'i',
        argument_name='current_directory',
        file_='definition.py',
        outside_score=False,
        parent_directories=('segments',),
        section='pdf',
        )
    def illustrate_definition(self, directory, dry_run=False):
        r'''Illustrates definition.

        Returns none.
        '''
        assert os.path.isdir(directory), repr(directory)
        definition_path = os.path.join(directory, 'definition.py')
        if not os.path.isfile(definition_path):
            message = 'File not found: {}.'
            message = message.format(definition_path)
            self._io_manager._display(message)
            return
        self._update_order_dependent_segment_metadata()
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
        illustration_source_path = os.path.join(
            directory,
            'illustration.ly',
            )
        illustration_pdf_path = os.path.join(
            directory,
            'illustration.pdf',
            )
        inputs, outputs = [], []
        if dry_run:
            inputs.append(definition_path)
            outputs.append((illustration_source_path, illustration_pdf_path))
            return inputs, outputs
        with systemtools.FilesystemState(remove=temporary_files):
            shutil.copyfile(boilerplate_path, illustrate_path)
            previous_segment_path = self._get_previous_segment_path(directory)
            if previous_segment_path is None:
                statement = 'previous_segment_metadata = None'
            else:
                score_directory = self._path_to_score_directory(directory)
                score_name = os.path.basename(score_directory)
                previous_segment_name = previous_segment_path
                previous_segment_name = os.path.basename(previous_segment_path)
                statement = 'from {}.segments.{}.__metadata__'
                statement += ' import metadata as previous_segment_metadata'
                statement = statement.format(score_name, previous_segment_name)
            self._replace_in_file(
                illustrate_path,
                'PREVIOUS_SEGMENT_METADATA_IMPORT_STATEMENT',
                statement,
                )
            result = self._io_manager.interpret_file(
                illustrate_path,
                strip=False,
                )
            stdout_lines, stderr_lines = result
            if stderr_lines:
                self._io_manager._display_errors(stderr_lines)
                return
            if not os.path.exists(illustration_pdf_path):
                messages = []
                messages.append('Wrote ...')
                if os.path.exists(candidate_ly_path):
                    shutil.move(candidate_ly_path, illustration_source_path)
                    messages.append(self._tab + illustration_source_path)
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
                    if not result:
                        return
                    try:
                        shutil.move(candidate_ly_path, illustration_source_path)
                    except IOError:
                        pass
                    try:
                        shutil.move(candidate_pdf_path, illustration_pdf_path)
                    except IOError:
                        pass

    @Command(
        'di*',
        argument_name='current_directory',
        directories=('segments'),
        outside_score=False,
        section='star',
        )
    def illustrate_every_definition(self, directories):
        r'''Illustrates every definition.

        Returns none.
        '''
        assert os.path.isdir(directory), repr(directory)
        directory_name = self._path_to_directory_name(directory)
        directories = self._list_visible_asset_paths(directory_name)
        inputs, outputs = [], []
        method_name = 'illustrate_definition'
        for directory in directories:
            inputs_, outputs_ = self.illustrate_definition(
                directory,
                dry_run=True,
                )
            inputs.extend(inputs_)
            outputs.extend(outputs_)
        messages = self._format_messaging(inputs, outputs, verb='illustrate')
        self._io_manager._display(messages)
        result = self._io_manager._confirm()
        if not result:
            return
        for directory in directories:
            self.illustrate_definition(directory)

    @Command(
        'bci',
        argument_name='current_directory',
        directories=('build'),
        section='build',
        outside_score=False,
        )
    def interpret_back_cover(self, directory):
        r'''Interprets ``back-cover.tex``.

        Returns none.
        '''
        assert os.path.isdir(directory), repr(directory)
        score_directory = self._path_to_score_directory(directory)
        build_directory = os.path.join(score_directory, 'build')
        self._interpret_file_ending_with(build_directory, 'back-cover.tex')

    @Command(
        'lyi*',
        argument_name='current_directory',
        directories=('materials', 'segments'),
        outside_score=False,
        section='star',
        )
    def interpret_every_ly(self, directory, open_every_illustration_pdf=True):
        r'''Interprets illustration ly in every package.

        Makes illustration PDF in every package.

        Returns none.
        '''
        assert os.path.isdir(directory), repr(directory)
        directory_name = self._path_to_directory_name(directory)
        directories = self._list_visible_asset_paths(directory_name)
        inputs, outputs = [], []
        method_name = 'interpret_illustration_source'
        for directory in directories:
            inputs_, outputs_ = self.interpret_ly(
                directory,
                dry_run=True,
                )
            inputs.extend(inputs_)
            outputs.extend(outputs_)
        messages = self._format_messaging(inputs, outputs)
        self._io_manager._display(messages)
        result = self._io_manager._confirm()
        if not result:
            return
        for directory in directories:
            result = self.interpret_ly(
                directory,
                confirm=False,
                )
            subprocess_messages, candidate_messages = result
            if subprocess_messages:
                self._io_manager._display(subprocess_messages)
                self._io_manager._display(candidate_messages)
                self._io_manager._display('')

    @Command(
        'fci',
        argument_name='current_directory',
        directories=('build'),
        outside_score=False,
        section='build',
        )
    def interpret_front_cover(self, directory):
        r'''Interprets ``front-cover.tex``.

        Returns none.
        '''
        assert os.path.isdir(directory), repr(directory)
        score_directory = self._path_to_score_directory(directory)
        build_directory = os.path.join(score_directory, 'build')
        self._interpret_file_ending_with(build_directory, 'front-cover.tex')

    @Command(
        'lyi',
        argument_name='current_directory',
        description='ly - interpret',
        file_='illustration.ly',
        outside_score=False,
        section='ly',
        )
    def interpret_ly(self, directory, confirm=True, dry_run=False):
        r'''Interprets illustration ly in `directory`.

        Makes illustration PDF.

        Returns a pair.
        
        Pairs equals list of STDERR messages from LilyPond together
        with list of candidate messages.
        '''
        assert os.path.isdir(directory), repr(directory)
        illustration_source_path = os.path.join(directory, 'illustration.ly')
        illustration_pdf_path = os.path.join(directory, 'illustration.pdf')
        inputs, outputs = [], []
        if os.path.isfile(illustration_source_path):
            inputs.append(illustration_source_path)
            outputs.append((illustration_pdf_path,))
        if dry_run:
            return inputs, outputs
        if not os.path.isfile(illustration_source_path):
            message = 'the file {} does not exist.'
            message = message.format(illustration_source_path)
            self._io_manager._display(message)
            return [], []
        messages = self._format_messaging(inputs, outputs)
        self._io_manager._display(messages)
        if confirm:
            result = self._io_manager._confirm()
            if not result:
                return [], []
        result = self._io_manager.run_lilypond(illustration_source_path)
        subprocess_messages, candidate_messages = result
        return subprocess_messages, candidate_messages

    @Command(
        'mi',
        argument_name='current_directory',
        directories=('build'),
        outside_score=False,
        section='build',
        )
    def interpret_music(self, directory):
        r'''Interprets ``music.ly``.

        Returns none.
        '''
        assert os.path.isdir(directory), repr(directory)
        score_directory = self._path_to_score_directory(directory)
        build_directory = os.path.join(score_directory, 'build')
        self._call_lilypond_on_file_ending_with(
            build_directory,
            'music.ly',
            )

    @Command(
        'pi',
        argument_name='current_directory',
        directories=('build'),
        outside_score=False,
        section='build',
        )
    def interpret_preface(self, directory):
        r'''Interprets ``preface.tex``.

        Returns none.
        '''
        assert os.path.isdir(directory), repr(directory)
        score_directory = self._path_to_score_directory(directory)
        build_directory = os.path.join(score_directory, 'build')
        self._interpret_file_ending_with(build_directory, 'preface.tex')

    @Command(
        'si',
        argument_name='current_directory',
        directories=('build'),
        outside_score=False,
        section='build',
        )
    def interpret_score(self, directory):
        r'''Interprets ``score.tex``.

        Returns none.
        '''
        assert os.path.isdir(directory), repr(directory)
        score_directory = self._path_to_score_directory(directory)
        build_directory = os.path.join(score_directory, 'build')
        self._interpret_file_ending_with(build_directory, 'score.tex')

    @Command('!', section='system')
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

    @Command(
        'illm',
        argument_name='current_directory',
        description='illustrate file - make',
        file_='__illustrate__.py',
        outside_score=False,
        section='illustrate_file',
        )
    def make_illustrate_file(self, directory):
        r'''Makes illustrate file.

        Returns none.
        '''
        assert os.path.isdir(directory), repr(directory)
        score_directory = self._path_to_score_directory(directory)
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
        self._session._pending_redraw = True

    @Command(
        'lym',
        argument_name='current_directory',
        description='ly - make',
        file_='definition.py',
        outside_score=False,
        parent_directories=('materials',),
        section='ly',
        )
    def make_ly(self, directory, dry_run=False):
        r'''Makes illustration ly.

        Returns none.
        '''
        assert os.path.isdir(directory), repr(directory)
        definition_path = os.path.join(directory, 'definition.py')
        if not os.path.isfile(definition_path):
            message = 'File not found: {}.'
            message = message.format(definition_path)
            self._io_manager._display(message)
            return
        illustrate_file_path = os.path.join(directory, '__illustrate__.py')
        if not os.path.isfile(illustrate_file_path):
            message = 'File not found: {}.'
            message = message.format(illustrate_file_path)
            self._io_manager._display(message)
            return
        candidate_ly_path = os.path.join(
            directory,
            'illustration.candidate.ly'
            )
        source_make_ly_file = os.path.join(
            configuration.abjad_ide_boilerplate_directory,
            '__make_ly__.py',
            )
        target_make_ly_file = os.path.join(directory, '__make_ly__.py')
        temporary_files = (
            candidate_ly_path,
            target_make_ly_file,
            )
        for path in temporary_files:
            if os.path.exists(path):
                os.remove(path)
        ly_path = os.path.join(directory, 'illustration.ly')
        inputs, outputs = [], []
        if dry_run:
            inputs.append(definition_path)
            outputs.append(ly_path)
            return inputs, outputs
        with systemtools.FilesystemState(remove=temporary_files):
            shutil.copyfile(source_make_ly_file, target_make_ly_file)
            result = self._io_manager.interpret_file(
                target_make_ly_file,
                strip=False,
                )
            stdout_lines, stderr_lines = result
            if stderr_lines:
                self._io_manager._display_errors(stderr_lines)
                return
            if not os.path.isfile(candidate_ly_path):
                message = 'could not make {}.'
                message = message.format(candidate_ly_path)
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
                message = 'preserved {}.'.format(ly_path)
                self._io_manager._display(message)
                return
            else:
                message = 'overwriting {} ...'
                message = message.format(ly_path)
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
                    message = message.format(ly_path)
                    self._io_manager._display(message)
                    self._io_manager.open_file(ly_path)

    @Command(
        'pdfm',
        argument_name='current_directory',
        description='pdf - make',
        file_='definition.py',
        outside_score=False,
        parent_directories=('materials',),
        section='pdf',
        )
    def make_pdf(self, directory, dry_run=False):
        r'''Makes illustration PDF.

        Returns none.
        '''
        assert os.path.isdir(directory), repr(directory)
        definition_path = os.path.join(directory, 'definition.py')
        if not os.path.isfile(definition_path):
            message = 'File not found: {}.'
            message = message.format(definition_path)
            self._io_manager._display(message)
            return
        illustrate_file_path = os.path.join(directory, '__illustrate__.py')
        if not os.path.isfile(illustrate_file_path):
            message = 'File not found: {}.'
            message = message.format(illustrate_file_path)
            self._io_manager._display(message)
            return
        candidate_ly_path = os.path.join(
            directory,
            'illustration.candidate.ly'
            )
        ly_path = os.path.join(directory, 'illustration.ly')
        candidate_pdf_path = os.path.join(
            directory,
            'illustration.candidate.pdf'
            )
        pdf_path = os.path.join(directory, 'illustration.pdf')
        source_make_pdf_file = os.path.join(
            configuration.abjad_ide_boilerplate_directory,
            '__make_pdf__.py',
            )
        target_make_pdf_file = os.path.join(directory, '__make_pdf__.py')
        temporary_files = (
            candidate_ly_path,
            candidate_pdf_path,
            target_make_pdf_file,
            )
        for path in temporary_files:
            if os.path.exists(path):
                os.remove(path)
        inputs, outputs = [], []
        if dry_run:
            inputs.append(definition_path)
            outputs.append((ly_path, pdf_path))
            return inputs, outputs
        with systemtools.FilesystemState(remove=temporary_files):
            shutil.copyfile(source_make_pdf_file, target_make_pdf_file)
            message = 'interpreting {} ...'
            message = message.format(target_make_pdf_file)
            self._io_manager._display(message)
            result = self._io_manager.interpret_file(
                target_make_pdf_file,
                strip=False,
                )
            stdout_lines, stderr_lines = result
            if stderr_lines:
                self._io_manager._display_errors(stderr_lines)
                return
                
            if not os.path.isfile(candidate_ly_path):
                message = 'could not make {}.'
                message = message.format(candidate_ly_path)
                self._io_manager._display(message)
                return
            result = systemtools.TestManager.compare_files(
                candidate_ly_path,
                ly_path,
                )
            if result:
                messages = []
                messages.append('preserving {} ...'.format(ly_path))
                messages.append('preserving {} ...'.format(pdf_path))
                self._io_manager._display(messages)
                return
            else:
                message = 'overwriting {} ...'
                message = message.format(ly_path)
                self._io_manager._display(message)
                try:
                    shutil.move(candidate_ly_path, ly_path)
                except IOError:
                    message = 'could not overwrite {} with {}.'
                    message = message.format(ly_path, candidate_ly_path)
                    self._io_manager._display(message)
            if not os.path.isfile(candidate_pdf_path):
                message = 'could not make {}.'
                message = message.format(candidate_pdf_path)
                self._io_manager._display(message)
                return
            result = systemtools.TestManager.compare_files(
                candidate_pdf_path,
                pdf_path,
                )
            if result:
                message = 'preserving {} ...'.format(pdf_path)
                self._io_manager._display(message)
                return
            else:
                message = 'overwriting {} ...'
                message = message.format(pdf_path)
                self._io_manager._display(message)
                try:
                    shutil.move(candidate_pdf_path, pdf_path)
                except IOError:
                    message = 'could not overwrite {} with {}.'
                    message = message.format(pdf_path, candidate_pdf_path)
                    self._io_manager._display(message)
            if not self._session.is_test:
                message = 'opening {} ...'
                message = message.format(pdf_path)
                self._io_manager._display(message)
                self._io_manager.open_file(pdf_path)

    @Command(
        'new',
        argument_name='current_directory',
        is_hidden=False,
        never_in_score_directory=True,
        section='basic',
        )
    def new(self, directory):
        r'''Makes new asset.

        Returns none.
        '''
        assert os.path.isdir(directory), repr(directory)
        asset_identifier = self._directory_to_asset_identifier(directory)
        if self._is_scores_directory(directory):
            self._make_score_package()
        elif asset_identifier == 'file':
            self._make_file(directory)
        elif asset_identifier == 'package':
            self._make_material_or_segment_package(directory)
        else:
            raise ValueError(directory)
        self._session._pending_menu_rebuild = True
        self._session._pending_redraw = True

    @Command(
        'io*',
        argument_name='current_directory',
        directories=('materials', 'segments'),
        outside_score=False,
        section='star',
        )
    def open_every_illustration_pdf(self, directory):
        r'''Opens ``illustration.pdf`` in every package.

        Returns none.
        '''
        assert os.path.isdir(directory), repr(directory)
        directory_name = self._path_to_directory_name(directory)
        directories = self._list_visible_asset_paths(directory_name)
        self._open_in_every_package(directories, 'illustration.pdf')

    @Command(
        'so*',
        argument_name='current_directory',
        in_score=False,
        outside_score='home',
        section='star',
        )
    def open_every_score_pdf(self, directory):
        r'''Opens ``score.pdf`` in every package.

        Returns none.
        '''
        assert os.path.isdir(directory), repr(directory)
        directory_name = self._path_to_directory_name(directory)
        directories = self._list_visible_asset_paths(directory_name)
        paths = []
        for directory in directories:
            inputs, outputs = self.open_score_pdf(directory, dry_run=True)
            paths.extend(inputs)
        messages = ['will open ...']
        paths = [self._tab + _ for _ in paths]
        messages.extend(paths)
        self._io_manager._display(messages)
        result = self._io_manager._confirm()
        if not result:
            return
        if paths:
            self._io_manager.open_file(paths)

    @Command(
        'pdf',
        argument_name='current_directory',
        description='pdf - open',
        file_='illustration.pdf',
        outside_score=False,
        section='pdf',
        )
    def open_pdf(self, directory):
        r'''Opens illustration PDF.

        Returns none.
        '''
        assert os.path.isdir(directory), repr(directory)
        file_path = os.path.join(directory, 'illustration.pdf')
        self._io_manager.open_file(file_path)

    @Command(
        'so',
        argument_name='current_directory',
        in_score_directory_only=True,
        outside_score=False,
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
        'sp',
        argument_name='current_directory',
        directories=('build'),
        outside_score=False,
        section='build',
        )
    def push_score_pdf_to_distribution_directory(self, directory):
        r'''Pushes ``score.pdf`` to distribution directory.

        Returns none.
        '''
        assert os.path.isdir(directory), repr(directory)
        score_directory = self._path_to_score_directory(directory)
        path = os.path.join(score_directory, 'build')
        build_score_path = os.path.join(path, 'score.pdf')
        if not os.path.exists(build_score_path):
            message = 'does not exist: {!r}.'
            message = message.format(build_score_path)
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
        is_hidden=False,
        never_in_score_directory=True,
        section='basic',
        )
    def remove(self, directory):
        r'''Removes asset(s).

        Returns none.
        '''
        assert os.path.isdir(directory), repr(directory)
        directory_name = self._path_to_directory_name(directory)
        paths = self._select_visible_asset_paths(directory_name)
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
            result = getter._run(io_manager=self._io_manager)
            if result is None:
                return
            if not result == confirmation_string:
                return
        for path in paths:
            self._remove(path)
        self._session._pending_menu_rebuild = True
        self._session._pending_redraw = True

    @Command(
        'ren',
        argument_name='current_directory',
        is_hidden=False,
        never_in_score_directory=True,
        section='basic',
        )
    def rename(self, directory):
        r'''Renames asset.

        Returns none.
        '''
        assert os.path.isdir(directory), repr(directory)
        source_path = self._select_visible_asset_path(
            directory,
            infinitive_phrase='to rename',
            )
        if self._is_inner_score_directory(source_path):
            source_path = os.path.dirname(source_path)
        if not source_path:
            return
        getter = self._io_manager._make_getter()
        getter.append_string('new name')
        original_target_name = getter._run(io_manager=self._io_manager)
        if original_target_name is None:
            return
        target_name = stringtools.strip_diacritics(original_target_name)
        target_name = target_name.replace(' ', '_')
        if not 'makers' in source_path.split(os.path.sep):
            target_name = target_name.lower()
        source_name = os.path.basename(source_path)
        target_path = os.path.join(
            os.path.dirname(source_path),
            target_name,
            )
        if os.path.exists(target_path):
            message = 'path already exists: {!r}.'
            message = message.format(target_path)
            self._io_manager._display(message)
            return
        messages = []
        messages.append('will rename ...')
        message = ' FROM: {}'.format(source_path)
        messages.append(message)
        message = '   TO: {}'.format(target_path)
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
        if self._is_outer_score_directory(target_path):
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
        'ws',
        argument_name='current_directory',
        directories=(
            'build',
            'distribution',
            'etc',
            'makers',
            'materials',
            'scores',
            'segments',
            'stylesheets',
            'test',
            ),
        outside_score='home',
        section='view',
        )
    def set_view(self, directory):
        r'''Sets view.

        Returns none.
        '''
        assert os.path.isdir(directory), repr(directory)
        directory_name = os.path.basename(directory)
        view_name = self._select_view(directory_name)
        if view_name is None:
            return
        if view_name == 'none':
            view_name = None
        if self._session.is_in_score:
            view_directory = self._session.manifest_current_directory
            metadatum_name = 'view_name'
        else:
            view_directory = configuration.abjad_ide_views_directory
            metadatum_name = '{}_view_name'.format(directory_name)
        self._add_metadatum(
            view_directory,
            metadatum_name,
            view_name,
            )

    @staticmethod
    def start_abjad_ide(is_test=False):
        r'''Starts Abjad IDE.

        Returns none.
        '''
        import ide
        abjad_ide = ide.tools.idetools.AbjadIDE(is_test=is_test)
        input_ = ' '.join(sys.argv[1:])
        abjad_ide._run_main_menu(input_=input_)