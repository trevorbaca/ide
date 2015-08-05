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
from ide.tools.idetools.AbjadIDEConfiguration import AbjadIDEConfiguration
from ide.tools.idetools.Controller import Controller
from ide.tools.idetools.Command import Command
configuration = AbjadIDEConfiguration()


class Wrangler(Controller):
    r'''Wrangler.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_allow_asset_name_underscores',
        '_asset_identifier',
        '_copy_target_directory',
        '_directory_entry_predicate',
        '_directory_name',
        '_file_extension',
        '_file_name_predicate',
        '_force_dash_case_file_name',
        '_force_lowercase_file_name',
        '_group_asset_section_by_annotation',
        '_hide_breadcrumb_while_in_score',
        '_new_file_contents',
        '_only_example_scores_during_test',
        '_sort_by_annotation',
        )

    ### INITIALIZER ###

    def __init__(self, session=None):
        from ide.tools import idetools
        assert session is not None
        superclass = super(Wrangler, self)
        superclass.__init__(session=session)
        self._allow_asset_name_underscores = False
        self._asset_identifier = None
        self._basic_breadcrumb = None
        self._copy_target_directory = None
        self._directory_entry_predicate = self._is_valid_directory_entry
        self._directory_name = None
        self._file_extension = ''
        self._file_name_predicate = None
        self._force_dash_case_file_name = False
        self._force_lowercase_file_name = True
        self._group_asset_section_by_annotation = True
        self._hide_breadcrumb_while_in_score = False
        self._new_file_contents = ''
        self._only_example_scores_during_test = False
        self._sort_by_annotation = True

    ### PRIVATE PROPERTIES ###

    @property
    def _breadcrumb(self):
        if self._session.is_in_score and self._hide_breadcrumb_while_in_score:
            return
        breadcrumb = self._basic_breadcrumb
        if self._session.is_in_score:
            breadcrumb = '{} directory'.format(breadcrumb)
        else:
            if breadcrumb == 'scores':
                breadcrumb = 'score'
            breadcrumb = 'all {} directories'.format(breadcrumb)
        view_name = self._read_view_name()
        if not view_name:
            return breadcrumb
        view_inventory = self._read_view_inventory()
        if view_inventory is not None and view_name in view_inventory:
            breadcrumb = '{} [{}]'.format(breadcrumb, view_name)
        return breadcrumb

    @property
    def _current_package_manager(self):
        path = self._get_current_directory()
        if path is None:
            return
        return self._session._io_manager._make_package_manager(path)

    @property
    def _current_storehouse_path(self):
        if self._session.is_in_score:
            return os.path.join(
                self._session.current_score_directory,
                self._directory_name,
                )
        return configuration.composer_scores_directory

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
            manager = self._get_views_package_manager()
        return manager._metadata_py_path

    ### PRIVATE METHODS ###

    def _call_lilypond_on_file_ending_with(self, string):
        directory_path = self._get_current_directory()
        file_path = self._get_file_path_ending_with(directory_path, string)
        if file_path:
            self._session._io_manager.run_lilypond(file_path)
        else:
            message = 'file ending in {!r} not found.'
            message = message.format(string)
            self._session._io_manager._display(message)
            
    def _check_every_file(self):
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
            tab = self._session._io_manager._tab
            message = tab + message
            messages.append(message)
            for invalid_path in invalid_paths:
                message = tab + tab + invalid_path
                messages.append(message)
        self._session._io_manager._display(messages)
        missing_files, missing_directories = [], []
        return messages, missing_files, missing_directories

    def _clear_view(self):
        if self._session.is_in_score:
            manager = self._current_package_manager
            metadatum_name = 'view_name'
        else:
            manager = self._get_views_package_manager()
            metadatum_name = '{}_view_name'.format(type(self).__name__)
        manager._add_metadatum(
            manager._session,
            manager._metadata_py_path,
            metadatum_name,
            None,
            )

    def _collect_segment_files(self, file_name):
        segments_directory = self._session.current_segments_directory
        build_directory = self._session.current_build_directory
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
            score_path = self._session.current_score_directory
            score_package = self._path_to_package(score_path)
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
            self._session._io_manager._display(messages)
            if not self._session._io_manager._confirm():
                return
            if self._session.is_backtracking:
                return
        if not os.path.exists(build_directory):
            os.mkdir(build_directory)
        pairs = zip(source_file_paths, target_file_paths)
        return pairs

    def _configure_as_build_file_wrangler(self):
        self._asset_identifier = 'file'
        self._basic_breadcrumb = 'build'
        self._directory_entry_predicate = self._is_valid_file_directory_entry
        self._directory_name = 'build'
        self._file_name_predicate = stringtools.is_dash_case
        self._force_dash_case_file_name = True
        return self

    def _configure_as_distribution_file_wrangler(self):
        self._asset_identifier = 'file'
        self._basic_breadcrumb = 'distribution'
        self._directory_entry_predicate = self._is_valid_file_directory_entry
        self._directory_name = 'distribution'
        self._file_name_predicate = stringtools.is_dash_case
        self._force_dash_case_file_name = True

    def _configure_as_etc_file_wrangler(self):
        self._asset_identifier = 'file'
        self._basic_breadcrumb = 'etc'
        self._directory_entry_predicate = self._is_valid_file_directory_entry
        self._directory_name = 'etc'
        self._file_name_predicate = stringtools.is_dash_case
        self._force_dash_case_file_name = True

    def _configure_as_maker_file_wrangler(self):
        self._asset_identifier = 'file'
        self._basic_breadcrumb = 'makers'
        self._directory_entry_predicate = self._is_valid_file_directory_entry
        self._directory_name = 'makers'
        self._file_extension = '.py'
        self._file_name_predicate = stringtools.is_upper_camel_case
        self._force_lowercase_file_name = False

    def _configure_as_material_package_wrangler(self):
        self._asset_identifier = 'package'
        self._basic_breadcrumb = 'materials'
        self._directory_entry_predicate = \
            self._is_valid_package_directory_entry
        self._directory_name = 'materials'

    def _configure_as_score_package_wrangler(self):
        self._asset_identifier = 'package'
        self._basic_breadcrumb = 'scores'
        self._copy_target_directory = configuration.composer_scores_directory
        self._directory_entry_predicate = \
            self._is_valid_package_directory_entry
        self._group_asset_section_by_annotation = False
        self._hide_breadcrumb_while_in_score = True
        self._only_example_scores_during_test = True
        self._sort_by_annotation = False

    def _configure_as_segment_package_wrangler(self):
        self._asset_identifier = 'package'
        self._basic_breadcrumb = 'segments'
        self._directory_entry_predicate = \
            self._is_valid_package_directory_entry
        self._directory_name = 'segments'

    def _configure_as_stylesheet_wrangler(self):
        self._asset_identifier = 'file'
        self._basic_breadcrumb = 'stylesheets'
        self._directory_entry_predicate = self._is_valid_file_directory_entry
        self._directory_name = 'stylesheets'
        self._file_extension = '.ily'
        self._file_name_predicate = stringtools.is_dash_case
        self._force_dash_case_file_name = True

    def _configure_as_test_file_wrangler(self):
        self._asset_identifier = 'file'
        self._basic_breadcrumb = 'test'
        self._directory_entry_predicate = self._is_valid_file_directory_entry
        self._directory_name = 'test'
        self._allow_asset_name_underscores = True
        self._file_extension = '.py'
        self._file_name_predicate = stringtools.is_snake_case
        return self

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
        self._session._io_manager._display(messages)
        result = self._session._io_manager._confirm()
        if self._session.is_backtracking or not result:
            return False
        return segment_names

    def _edit_file_ending_with(self, string):
        directory_path = self._get_current_directory()
        file_path = self._get_file_path_ending_with(directory_path, string)
        if file_path:
            self._session._io_manager.edit(file_path)
        else:
            message = 'file ending in {!r} not found.'
            message = message.format(string)
            self._session._io_manager._display(message)

    def _extract_common_parent_directories(self, paths):
        parent_directories = []
        abjad_ide_example_scores_directory = \
            configuration.abjad_ide_example_scores_directory
        scores_directory = configuration.composer_scores_directory
        for path in paths:
            parent_directory = os.path.dirname(path)
            if parent_directory == scores_directory:
                parent_directories.append(path)
            elif parent_directory == abjad_ide_example_scores_directory:
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
        from ide.tools import idetools
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
                    configuration.abjad_ide_example_scores_directory
            else:
                scores_directory = configuration.composer_scores_directory
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
            if (manager._is_git_versioned(manager._session, manager._path) and
                manager._is_up_to_date(manager._session, manager._path) and
                (not must_have_file or
                manager._find_first_file_name(manager._path))):
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
            getter = self._session._io_manager._make_getter()
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
                self._session._io_manager._display(line)
            else:
                return path

    def _get_current_directory(self):
        score_directory = self._session.current_score_directory
        if score_directory is not None:
            directory = os.path.join(
                score_directory,
                self._directory_name,
                )
            directory = os.path.abspath(directory)
            return directory

    def _get_manager(self, path):
        from ide.tools import idetools
        assert os.path.sep in path, repr(path)
        manager = idetools.PackageManager(
            path=path,
            session=self._session,
            )
        if self._asset_identifier == 'file':
            return manager
        else:
            assert self._asset_identifier == 'package'
        if self._basic_breadcrumb == 'materials':
            manager._configure_as_material_package_manager()
        elif self._basic_breadcrumb == 'scores':
            manager._configure_as_score_package_manager()
        elif self._basic_breadcrumb == 'segments':
            manager._configure_as_segment_package_manager()
        else:
            raise ValueError(self._basic_breadcrumb)
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
            storehouse = self._path_to_storehouse(path)
            storehouses.add(storehouse)
        storehouses = list(sorted(storehouses))
        return storehouses

    def _interpret_file_ending_with(self, string):
        r'''Typesets TeX file.
        Calls ``pdflatex`` on file TWICE.
        Some LaTeX packages like ``tikz`` require two passes.
        '''
        directory_path = self._get_current_directory()
        file_path = self._get_file_path_ending_with(directory_path, string)
        if not file_path:
            message = 'file ending in {!r} not found.'
            message = message.format(string)
            self._session._io_manager._display(message)
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
            self._session._io_manager.spawn_subprocess(command_called_twice)
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
            name, file_extension = os.path.splitext(expr)
            if self._file_name_predicate(name):
                if self._file_extension == '':
                    return True
                elif self._file_extension == file_extension:
                    return True
        return False

    def _is_valid_package_directory_entry(self, expr):
        superclass = super(Wrangler, self)
        if superclass._is_valid_directory_entry(expr):
            if '.' not in expr:
                return True
        return False

    def _list_all_directories_with_metadata_pys(self):
        directories = []
        paths = self._list_visible_asset_paths()
        for path in paths:
            result = self._list_directories_with_metadata_pys(path)
            directories.extend(result)
        return directories

    def _list_asset_paths(
        self,
        example_score_packages=True,
        user_score_packages=True,
        valid_only=True,
        ):
        result = []
        directories = self._list_storehouse_paths(
            example_score_packages=example_score_packages,
            user_score_packages=user_score_packages,
            )
        for directory in directories:
            if not directory:
                continue
            if not os.path.exists(directory):
                continue
            directory_entries = sorted(os.listdir(directory))
            for directory_entry in directory_entries:
                if valid_only:
                    if not self._directory_entry_predicate(directory_entry):
                        continue
                path = os.path.join(directory, directory_entry)
                if self._basic_breadcrumb == 'scores':
                    # test for installable python package structure
                    outer_init_path = os.path.join(path, '__init__.py')
                    inner_directory = os.path.join(path, directory_entry)
                    inner_init_path = os.path.join(
                        inner_directory, '__init__.py')
                    if not os.path.exists(outer_init_path):
                        if os.path.exists(inner_init_path):
                            path = inner_directory
                result.append(path)
        return result

    def _list_score_directories(
        self,
        abjad=False,
        user=False,
        ):
        result = []
        if abjad:
            scores_directory = configuration.abjad_ide_example_scores_directory
            directory_entries = sorted(os.listdir(scores_directory))
            for directory_entry in directory_entries:
                if directory_entry[0].isalpha():
                    path = os.path.join(
                        configuration.abjad_ide_example_scores_directory,
                        directory_entry,
                        )
                    result.append(path)
        if user:
            scores_directory = configuration.composer_scores_directory
            directory_entries = sorted(os.listdir(scores_directory))
            for directory_entry in directory_entries:
                if not directory_entry[0].isalpha():
                    continue
                path = os.path.join(
                    configuration.composer_scores_directory,
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

    def _list_storehouse_paths(
        self,
        example_score_packages=True,
        user_score_packages=True,
        ):
        result = []
        if user_score_packages:
            result.append(configuration.composer_scores_directory)
        if (example_score_packages and self._directory_name):
            for score_directory in self._list_score_directories(abjad=True):
                score_directory = self._path_to_score_path(score_directory)
                path = os.path.join(
                    score_directory,
                    self._directory_name,
                    )
                result.append(path)
        elif (example_score_packages and not self._directory_name):
            result.append(configuration.abjad_ide_example_scores_directory)
        if user_score_packages and self._directory_name:
            for score_directory in self._list_score_directories(user=True):
                path = os.path.join(
                    score_directory,
                    self._directory_name,
                    )
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
        with self._session._io_manager._silent(self._session):
            manager.check_package(
                return_supply_messages=True,
                supply_missing=True,
                )
        paths = self._list_visible_asset_paths()
        if path not in paths:
            with self._session._io_manager._silent(self._session):
                self._clear_view()
        self._session._pending_redraw = True

    def _make_asset_menu_entries(
        self,
        apply_current_directory=True,
        set_view=True,
        ):
        paths = self._list_asset_paths()
        current_directory = self._get_current_directory()
        if (apply_current_directory or set_view) and current_directory:
            paths = [_ for _ in paths if _.startswith(current_directory)]
        strings = [self._path_to_asset_menu_display_string(_) for _ in paths]
        pairs = list(zip(strings, paths))
        if not self._session.is_in_score and self._sort_by_annotation:
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
            entries = self._filter_asset_menu_entries_by_view(entries)
        if self._session.is_test and self._only_example_scores_during_test:
            entries = [_ for _ in entries if 'Example Score' in _[0]]
        elif not self._session.is_test:
            entries = [_ for _ in entries if 'Example Score' not in _[0]]
        return entries

    def _make_asset_menu_section(self, menu):
        menu_entries = []
        menu_entries.extend(self._make_secondary_asset_menu_entries())
        menu_entries.extend(self._make_asset_menu_entries())
        if menu_entries:
            section = menu.make_asset_section(menu_entries=menu_entries)
            assert section is not None
            section._group_by_annotation = \
                self._group_asset_section_by_annotation

    def _make_asset_selection_breadcrumb(
        self,
        infinitival_phrase=None,
        is_storehouse=False,
        ):
        if infinitival_phrase:
            return 'select {} {}:'.format(
                self._asset_identifier,
                infinitival_phrase,
                )
        elif is_storehouse:
            return 'select storehouse'
        else:
            return 'select {}:'.format(self._asset_identifier)

    def _make_asset_selection_menu(self):
        menu = self._session._io_manager._make_menu(name='asset selection')
        menu_entries = self._make_asset_menu_entries()
        menu.make_asset_section(menu_entries=menu_entries)
        return menu

    def _make_file(self, message='file name'):
        file_extension = self._file_extension
        contents = ''
        if file_extension == '.py':
            contents == self._unicode_directive
        if self._session.is_in_score:
            path = self._get_current_directory()
        else:
            path = self._select_storehouse_path()
            if self._session.is_backtracking or path is None:
                return
        getter = self._session._io_manager._make_getter()
        getter.append_string(message)
        name = getter._run()
        if self._session.is_backtracking or name is None:
            return
        name = stringtools.strip_diacritics(name)
        if self._force_dash_case_file_name:
            name = self._to_dash_case(name)
        name = name.replace(' ', '_')
        if self._force_lowercase_file_name:
            name = name.lower()
        if not name.endswith(file_extension):
            name = name + file_extension
        path = os.path.join(path, name)
        self._session._io_manager.write(path, contents)
        self._session._io_manager.edit(path)

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
        self._session._io_manager._display(message)
        result = self._session._io_manager._confirm()
        if self._session.is_backtracking or not result:
            return
        manager = self._get_manager(path)
        manager._make_package()
        paths = self._list_visible_asset_paths()
        if path not in paths:
            with self._session._io_manager._silent(self._session):
                self._clear_view()
        manager._run()

    def _make_score_package(self):
        message = 'enter title'
        getter = self._session._io_manager._make_getter()
        getter.append_string(message)
        title = getter._run()
        if self._session.is_backtracking or not title:
            return
        package_name = stringtools.strip_diacritics(title)
        package_name = stringtools.to_snake_case(package_name)
        confirmed = False 
        while not confirmed:
            package_path = os.path.join(
                configuration.composer_scores_directory,
                package_name,
                )
            message = 'path will be {}.'.format(package_path)
            self._session._io_manager._display(message)
            result = self._session._io_manager._confirm()
            if self._session.is_backtracking:
                return
            confirmed = result
            if confirmed:
                break
            message = 'enter package name'
            getter = self._session._io_manager._make_getter()
            getter.append_string(message)
            package_name = getter._run()
            if self._session.is_backtracking or not package_name:
                return
            package_name = stringtools.strip_diacritics(package_name)
            package_name = stringtools.to_snake_case(package_name)
        manager = self._get_manager(package_path)
        manager._make_package()
        manager._add_metadatum(
            manager._session,
            manager._metadata_py_path,
            'title',
            title,
            )
        year = datetime.date.today().year
        manager._add_metadatum(
            manager._session,
            manager._metadata_py_path,
            'year',
            year,
            )
        package_paths = self._list_visible_asset_paths()
        if package_path not in package_paths:
            with self._session._io_manager._silent(self._session):
                self._clear_view()
        manager._run()

    def _make_storehouse_menu_entries(
        self,
        example_score_packages=True,
        user_score_packages=True,
        ):
        from ide.tools import idetools
        display_strings, keys = [], []
        wrangler = self._session._abjad_ide._score_package_wrangler
        paths = wrangler._list_asset_paths(
            example_score_packages=example_score_packages,
            user_score_packages=user_score_packages,
            )
        for path in paths:
            manager = wrangler._get_manager(path)
            title = manager._get_title_metadatum(
                manager._session,
                manager._metadata_py_path,
                year=False,
                )
            display_strings.append(title)
            key = os.path.join(
                manager._path,
                self._directory_name,
                )
            keys.append(key)
        assert len(display_strings) == len(keys), repr((display_strings, keys))
        sequences = [display_strings, [None], [None], keys]
        return sequencetools.zip_sequences(sequences, cyclic=True)

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
        manager = self._session._io_manager._make_package_manager(path)
        count = pattern.count('md:')
        for _ in range(count+1):
            parts = pattern.split()
            for part in parts:
                if part.startswith('md:'):
                    metadatum_name = part[3:]
                    metadatum = manager._get_metadatum(
                        manager._session,
                        manager._metadata_py_path,
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
        directory_path = self._get_current_directory()
        path = self._get_file_path_ending_with(directory_path, string)
        if path:
            self._session._io_manager.open_file(path)
        else:
            message = 'file ending in {!r} not found.'
            message = message.format(string)
            self._session._io_manager._display(message)

    def _open_in_every_package(self, file_name, verb='open'):
        paths = []
        for path in self._list_visible_asset_paths():
            path = os.path.join(path, file_name)
            if os.path.isfile(path):
                paths.append(path)
        if not paths:
            message = 'no {} files found.'
            message = message.format(file_name)
            self._session._io_manager._display(message)
            return
        messages = []
        message = 'will {} ...'.format(verb)
        messages.append(message)
        for path in paths:
            message = '   ' + path
            messages.append(message)
        self._session._io_manager._display(messages)
        result = self._session._io_manager._confirm()
        if self._session.is_backtracking or not result:
            return
        self._session._io_manager.open_file(paths)

    def _path_to_package(self, path):
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

    def _path_to_storehouse(self, path):
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
        storehouse_path = os.path.join(path_prefix, *path_parts)
        return storehouse_path

    def _run(self):
        controller = self._session._io_manager._controller(
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
                    self._handle_pending_redraw_directive(result)
                    self._handle_wrangler_navigation_directive(result)
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

    def _select_storehouse_path(self, example_score_packages=False):
        menu_entries = self._make_storehouse_menu_entries(
            example_score_packages=example_score_packages,
            user_score_packages=False,
            )
        selector = self._session._io_manager._make_selector(
            menu_entries=menu_entries,
            target_name='storehouse',
            )
        result = selector._run()
        if self._session.is_backtracking or result is None:
            return
        return result

    def _select_view(self, infinitive_phrase=None, is_ranged=False):
        from ide.tools import idetools
        view_inventory = self._read_view_inventory()
        if view_inventory is None:
            message = 'no views found.'
            self._session._io_manager._display(message)
            return
        view_names = list(view_inventory.keys())
        view_names.append('none')
        if is_ranged:
            target_name = 'view(s)'
        else:
            target_name = 'view'
        if infinitive_phrase:
            target_name = '{} {}'.format(target_name, infinitive_phrase)
        selector = self._session._io_manager._make_selector(
            target_name=target_name,
            is_ranged=is_ranged,
            items=view_names,
            )
        result = selector._run()
        if self._session.is_backtracking or result is None:
            return
        return result

    def _select_visible_asset_path(self, infinitive_phrase=None):
        getter = self._session._io_manager._make_getter()
        message = 'enter {}'.format(self._asset_identifier)
        if infinitive_phrase:
            message = message + ' ' + infinitive_phrase
        if hasattr(self, '_make_asset_menu_section'):
            dummy_menu = self._session._io_manager._make_menu()
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
        getter = self._session._io_manager._make_getter()
        message = 'enter {}(s) to remove'
        message = message.format(self._asset_identifier)
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

    def _supply_missing_views_files(self):
        from ide.tools import idetools
        if not os.path.exists(self._views_py_path):
            view_inventory = idetools.ViewInventory()
            with self._session._io_manager._silent(self._session):
                self._write_view_inventory(view_inventory)
        if not os.path.exists(self._metadata_py_path):
            metadata = self._get_metadata()
            with self._session._io_manager._silent(self._session):
                self._write_metadata_py(self._metadata_py_path, metadata)
        if self._session.is_test:
            with self._session._io_manager._silent(self._session):
                for wrangler in self._session._abjad_ide._wranglers:
                    if not os.path.exists(wrangler._views_py_path):
                        wrangler.write_views_py()
        else:
            with self._session._io_manager._silent(self._session):
                for wrangler in self._session._abjad_ide._wranglers:
                    view_inventory = idetools.ViewInventory()
                    wrangler._write_view_inventory(view_inventory)

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
            manager._add_metadatum(
                manager._session,
                manager._metadata_py_path,
                'segment_number',
                segment_number,
                )
            manager._add_metadatum(
                manager._session,
                manager._metadata_py_path,
                'segment_count', 
                segment_count,
                )
        # update first bar numbers and measure counts
        manager = managers[0]
        first_bar_number = 1
        manager._add_metadatum(
            manager._session,
            manager._metadata_py_path,
            'first_bar_number',
            first_bar_number,
            )
        measure_count = manager._get_metadatum(
            manager._session,
            manager._metadata_py_path,
            'measure_count',
            )
        if not measure_count:
            return
        next_bar_number = first_bar_number + measure_count
        for manager in managers[1:]:
            first_bar_number = next_bar_number
            manager._add_metadatum(
                manager._session,
                manager._metadata_py_path,
                'first_bar_number',
                next_bar_number,
                )
            measure_count = manager._get_metadatum(
                manager._session,
                manager._metadata_py_path,
                'measure_count',
                )
            if not measure_count:
                return
            next_bar_number = first_bar_number + measure_count
            
    ### PUBLIC METHODS ###

    @Command(
        'dc*',
        directories=('materials', 'segments'),
        outside_score=False,
        section='star',
        )
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
        self._session._io_manager._display(messages)
        result = self._session._io_manager._confirm()
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
        self._session._io_manager._display(message)

    @Command('ck*', section='star', in_score=False, outside_score='home')
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
        tab = indent * self._session._io_manager._tab
        if problems_only is None:
            prompt = 'show problem assets only?'
            result = self._session._io_manager._confirm(prompt)
            if self._session.is_backtracking or result is None:
                return messages, missing_directories, missing_files
            problems_only = bool(result)
        managers = self._list_visible_asset_managers()
        found_problem = False
        for manager in managers:
            with self._session._io_manager._silent(self._session):
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
        self._session._io_manager._display(messages)
        if not found_problem:
            return messages, missing_directories, missing_files
        if supply_missing is None:
            prompt = 'supply missing directories and files?'
            result = self._session._io_manager._confirm(prompt)
            if self._session.is_backtracking or result is None:
                return messages, missing_directories, missing_files
            supply_missing = bool(result)
        if not supply_missing:
            return messages, missing_directories, missing_files
        messages = []
        for manager in managers:
            with self._session._io_manager._silent(self._session):
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
        self._session._io_manager._display(messages)
        return messages, supplied_directories, supplied_files

    @Command(
        'mc',
        directories=('build'),
        outside_score=False,
        section='build',
        )
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
                self._session._io_manager._display('')

    @Command('cp', section='basic', is_hidden=False)
    def copy(
        self, 
        file_extension=None,
        new_storehouse=None
        ):
        r'''Copies asset.

        Returns none.
        '''
        visible_asset_paths = self._list_visible_asset_paths()
        if not visible_asset_paths:
            messages = ['nothing to copy.']
            messages.append('')
            self._session._io_manager._display(messages)
            return
        file_extension = self._file_extension
        old_path = self._select_visible_asset_path(infinitive_phrase='to copy')
        if not old_path:
            return
        old_name = os.path.basename(old_path)
        new_storehouse = self._copy_target_directory
        if new_storehouse:
            pass
        elif self._session.is_in_score:
            new_storehouse = self._get_current_directory()
        else:
            new_storehouse = self._select_storehouse_path()
            if self._session.is_backtracking or new_storehouse is None:
                return
        message = 'existing {} name> {}'
        message = message.format(
            self._asset_identifier,
            old_name,
            )
        self._session._io_manager._display(message)
        message = 'new {} name'
        message = message.format(self._asset_identifier)
        getter = self._session._io_manager._make_getter()
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
        if self._force_dash_case_file_name:
            new_name = self._to_dash_case(new_name)
        new_name = new_name.replace(' ', '_')
        if self._force_lowercase_file_name:
            new_name = new_name.lower()
        if file_extension and not new_name.endswith(file_extension):
            new_name = new_name + file_extension
        new_path = os.path.join(new_storehouse, new_name)
        if os.path.exists(new_path):
            message = 'already exists: {}'.format(new_path)
            self._session._io_manager._display(message)
            self._session._io_manager._acknowledge()
            return
        messages = []
        messages.append('will copy ...')
        messages.append(' FROM: {}'.format(old_path))
        messages.append('   TO: {}'.format(new_path))
        self._session._io_manager._display(messages)
        result = self._session._io_manager._confirm()
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

    @Command('de*', directories=('materials', 'segments'), section='star')
    def edit_every_definition_py(self):
        r'''Opens ``definition.py`` in every package.

        Returns none.
        '''
        self._open_in_every_package('definition.py')

    @Command(
        'bcg', 
        directories=('build'),
        outside_score=False,
        section='build',
        )
    def generate_back_cover_source(self):
        r'''Generates ``back-cover.tex``.

        Returns none.
        '''
        replacements = {}
        manager = self._session.current_score_package_manager
        catalog_number = manager._get_metadatum(
            manager._session,
            manager._metadata_py_path,
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
        price = manager._get_metadatum(
            manager._session,
            manager._metadata_py_path,
            'price',
            )
        if price:
            old = 'PRICE'
            new = str(price)
            replacements[old] = new
        width, height, unit = manager._parse_paper_dimensions(manager._session)
        if width and height:
            old = '{PAPER_SIZE}'
            new = '{{{}{}, {}{}}}'
            new = new.format(width, unit, height, unit)
            replacements[old] = new
        self._copy_boilerplate(
            self._session,
            'back-cover.tex',
            self._session.current_build_directory,
            replacements=replacements,
            )

    @Command(
        'fcg',
        directories=('build'),
        section='build',
        outside_score=False,
        )
    def generate_front_cover_source(self):
        r'''Generates ``front-cover.tex``.

        Returns none.
        '''
        file_name = 'front-cover.tex'
        replacements = {}
        manager = self._session.current_score_package_manager
        score_title = manager._get_title_metadatum(
            manager._session,
            manager._metadata_py_path,
            year=False,
            )
        if score_title:
            old = 'TITLE'
            new = str(score_title.upper())
            replacements[old] = new
        forces_tagline = manager._get_metadatum(
            manager._session,
            manager._metadata_py_path,
            'forces_tagline',
            )
        if forces_tagline:
            old = 'FOR INSTRUMENTS'
            new = str(forces_tagline)
            replacements[old] = new
        year = manager._get_metadatum(
            manager._session,
            manager._metadata_py_path,
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
        width, height, unit = manager._parse_paper_dimensions(manager._session)
        if width and height:
            old = '{PAPER_SIZE}'
            new = '{{{}{}, {}{}}}'
            new = new.format(width, unit, height, unit)
            replacements[old] = new
        self._copy_boilerplate(
            self._session,
            file_name,
            self._session.current_build_directory,
            replacements=replacements,
            )

    @Command(
        'mg',
        directories=('build'),
        outside_score=False,
        section='build',
        )
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
            configuration.abjad_ide_boilerplate_directory,
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
            width, height, unit = manager._parse_paper_dimensions(
                manager._session)
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
            score_title = manager._get_title_metadatum(
                manager._session,
                manager._metadata_py_path,
                year=False,
                )
            if score_title:
                old = 'SCORE_NAME'
                new = score_title
                self._replace_in_file(candidate_path, old, new)
            annotated_title = manager._get_title_metadatum(
                manager._session,
                manager._metadata_py_path,
                year=True,
                )
            if annotated_title:
                old = 'SCORE_TITLE'
                new = annotated_title
                self._replace_in_file(candidate_path, old, new)
            forces_tagline = manager._get_metadatum(
                manager._session,
                manager._metadata_py_path,
                'forces_tagline',
                )
            if forces_tagline:
                old = 'FORCES_TAGLINE'
                new = forces_tagline
                self._replace_in_file(candidate_path, old, new)
            self._handle_candidate(candidate_path, destination_path)

    @Command(
        'pg',
        directories=('build'),
        outside_score=False,
        section='build',
        )
    def generate_preface_source(self):
        r'''Generates ``preface.tex``.

        Returns none.
        '''
        replacements = {}
        manager = self._session.current_score_package_manager
        width, height, unit = manager._parse_paper_dimensions(manager._session)
        if width and height:
            old = '{PAPER_SIZE}'
            new = '{{{}{}, {}{}}}'
            new = new.format(width, unit, height, unit)
            replacements[old] = new
        self._copy_boilerplate(
            self._session,
            'preface.tex',
            self._session.current_build_directory,
            replacements=replacements,
            )

    @Command(
        'sg',
        directories=('build'),
        outside_score=False,
        section='build',
        )
    def generate_score_source(self):
        r'''Generates ``score.tex``.

        Returns none.
        '''
        replacements = {}
        manager = self._session.current_score_package_manager
        width, height, unit = manager._parse_paper_dimensions(manager._session)
        if width and height:
            old = '{PAPER_SIZE}'
            new = '{{{}{}, {}{}}}'
            new = new.format(width, unit, height, unit)
            replacements[old] = new
        self._copy_boilerplate(
            self._session,
            'score.tex',
            self._session.current_build_directory,
            replacements=replacements,
            )

    @Command('add*', section='git', in_score=False, outside_score='home')
    def git_add_every_package(self):
        r'''Adds every asset to repository.

        Returns none.
        '''
        self._session._attempted_to_add = True
        if self._session.is_repository_test:
            return
        managers = self._list_visible_asset_managers()
        inputs, outputs = [], []
        method_name = '_git_add'
        for manager in managers:
            method = getattr(manager, method_name)
            inputs_, outputs_ = method(
                manager._session,
                manager._path,
                dry_run=True,
                )
            inputs.extend(inputs_)
            outputs.extend(outputs_)
        messages = self._format_messaging(inputs, outputs, verb='add')
        self._session._io_manager._display(messages)
        if not inputs:
            return
        result = self._session._io_manager._confirm()
        if self._session.is_backtracking or not result:
            return
        with self._session._io_manager._silent(self._session):
            for manager in managers:
                method = getattr(manager, method_name)
                method()
        count = len(inputs)
        identifier = stringtools.pluralize('file', count)
        message = 'added {} {} to repository.'
        message = message.format(count, identifier)
        self._session._io_manager._display(message)
        
    @Command('ci*', section='git', in_score=False, outside_score='home')
    def git_commit_every_package(self):
        r'''Commits every asset to repository.

        Returns none.
        '''
        self._session._attempted_to_commit = True
        if self._session.is_repository_test:
            return
        getter = self._session._io_manager._make_getter()
        getter.append_string('commit message')
        commit_message = getter._run()
        if self._session.is_backtracking or commit_message is None:
            return
        line = 'commit message will be: "{}"'.format(commit_message)
        self._session._io_manager._display(line)
        result = self._session._io_manager._confirm()
        if self._session.is_backtracking or not result:
            return
        paths = self._list_visible_asset_paths()
        for path in paths:
            manager = self._get_manager(path)
            with self._session._io_manager._silent(self._session):
                manager._git_commit(commit_message=commit_message)

    @Command('revert*', section='git', in_score=False, outside_score='home')
    def git_revert_every_package(self):
        r'''Reverts every asset to repository.

        Returns none.
        '''
        self._session._attempted_to_revert = True
        if self._session.is_repository_test:
            return
        paths = self._list_visible_asset_paths()
        for path in paths:
            manager = self._session._io_manager._make_package_manager(path)
            manager._git_revert()

    @Command('st*', section='git', in_score=False, outside_score='home')
    def git_status_every_package(self):
        r'''Displays repository status of every asset.

        Returns none.
        '''
        self._session._attempted_display_status = True
        paths = self._list_visible_asset_paths()
        paths = self._extract_common_parent_directories(paths)
        paths.sort()
        for path in paths:
            manager = self._session._io_manager._make_package_manager(path)
            manager._git_status()
        if not paths:
            message = 'Repository status for {} ... OK'
            directory = self._get_current_directory()
            message = message.format(directory)
            self._session._io_manager._display(message)

    @Command('up*', section='git', in_score=False, outside_score='home')
    def git_update_every_package(self):
        r'''Updates every asset from repository.

        Returns none.
        '''
        tab = self._session._io_manager._tab
        managers = self._list_visible_asset_managers()
        for manager in managers:
            messages = []
            message = self._path_to_asset_menu_display_string(manager._path)
            message = self._strip_annotation(message)
            message = message + ':'
            messages_ = manager._git_update(messages_only=True)
            if len(messages_) == 1:
                message = message + ' ' + messages_[0]
                messages.append(message)
            else:
                messages_ = [tab + _ for _ in messages_]
                messages.extend(messages_)
            self._session._io_manager._display(messages, capitalize=False)

    @Command(
        'di*',
        directories=('segments'),
        outside_score=False,
        section='star',
        )
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
        self._session._io_manager._display(messages)
        result = self._session._io_manager._confirm()
        if self._session.is_backtracking or not result:
            return
        for manager in managers:
            method = getattr(manager, method_name)
            method()

    @Command(
        'bci',
        directories=('build'),
        section='build',
        outside_score=False,
        )
    def interpret_back_cover(self):
        r'''Interprets ``back-cover.tex``.

        Returns none.
        '''
        self._interpret_file_ending_with('back-cover.tex')

    @Command(
        'ii*',
        directories=('materials', 'segments'),
        outside_score=False,
        section='star',
        )
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
        self._session._io_manager._display(messages)
        result = self._session._io_manager._confirm()
        if self._session.is_backtracking or not result:
            return
        for manager in managers:
            with self._session._io_manager._silent(self._session):
                method = getattr(manager, method_name)
                subprocess_messages, candidate_messages = method()
            if subprocess_messages:
                self._session._io_manager._display(subprocess_messages)
                self._session._io_manager._display(candidate_messages)
                self._session._io_manager._display('')
                
    @Command(
        'fci',
        directories=('build'),
        outside_score=False,
        section='build',
        )
    def interpret_front_cover(self):
        r'''Interprets ``front-cover.tex``.

        Returns none.
        '''
        self._interpret_file_ending_with('front-cover.tex')

    @Command(
        'mi',
        directories=('build'),
        outside_score=False,
        section='build',
        )
    def interpret_music(self):
        r'''Interprets ``music.ly``.

        Returns none.
        '''
        self._call_lilypond_on_file_ending_with('music.ly')

    @Command(
        'pi',
        directories=('build'),
        outside_score=False,
        section='build',
        )
    def interpret_preface(self):
        r'''Interprets ``preface.tex``.

        Returns none.
        '''
        self._interpret_file_ending_with('preface.tex')

    @Command(
        'si',
        directories=('build'),
        outside_score=False,
        section='build',
        )
    def interpret_score(self):
        r'''Interprets ``score.tex``.

        Returns none.
        '''
        self._interpret_file_ending_with('score.tex')

    @Command('new', description='new', section='basic', is_hidden=False)
    def make(self):
        r'''Makes asset.

        Returns none.
        '''
        if self._asset_identifier == 'file':
            self._make_file()
        elif self._basic_breadcrumb == 'scores':
            self._make_score_package()
        else:
            self._make_package()

    @Command(
        'io*',
        directories=('materials', 'segments'),
        outside_score=False,
        section='star',
        )
    def open_every_illustration_pdf(self):
        r'''Opens ``illustration.pdf`` in every package.

        Returns none.
        '''
        self._open_in_every_package('illustration.pdf')

    @Command('so*', section='star', in_score=False, outside_score='home')
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
        tab = self._session._io_manager._tab
        paths = [tab + _ for _ in paths]
        messages.extend(paths)
        self._session._io_manager._display(messages)
        result = self._session._io_manager._confirm()
        if self._session.is_backtracking or not result:
            return
        if paths:
            self._session._io_manager.open_file(paths)

    @Command(
        'sp', 
        directories=('build'),
        outside_score=False,
        section='build',
        )
    def push_score_pdf_to_distribution_directory(self):
        r'''Pushes ``score.pdf`` to distribution directory.

        Returns none.
        '''
        path = self._session.current_build_directory
        build_score_path = os.path.join(path, 'score.pdf')
        if not os.path.exists(build_score_path):
            message = 'does not exist: {!r}.'
            message = message.format(build_score_path)
            self._session._io_manager._display(message)
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
        self._session._io_manager._display(messages)

    @Command('rm', section='basic', is_hidden=False)
    def remove(self):
        r'''Removes asset.

        Returns none.
        '''
        from ide.tools import idetools
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
        self._session._io_manager._display(messages)
        if count == 1:
            confirmation_string = 'remove'
        else:
            confirmation_string = 'remove {}'
            confirmation_string = confirmation_string.format(count)
        message = "type {!r} to proceed"
        message = message.format(confirmation_string)
        getter = self._session._io_manager._make_getter()
        getter.append_string(message)
        if self._session.confirm:
            result = getter._run()
            if self._session.is_backtracking or result is None:
                return
            if not result == confirmation_string:
                return
        for path in paths:
            manager = self._get_manager(path)
            with self._session._io_manager._silent(self._session):
                manager._remove(manager._session, manager._path)
        self._session._pending_redraw = True

    @Command('ren', section='basic', is_hidden=False)
    def rename(
        self,
        file_extension=None,
        file_name_callback=None, 
        ):
        r'''Renames asset.

        Returns none.
        '''
        file_extension = self._file_extension
        path = self._select_visible_asset_path(infinitive_phrase='to rename')
        if not path:
            return
        file_name = os.path.basename(path)
        message = 'existing file name> {}'
        message = message.format(file_name)
        self._session._io_manager._display(message)
        manager = self._get_manager(path)
        new_path = manager._rename(
            manager._session,
            manager._path,
            file_extension=file_extension,
            file_name_callback=file_name_callback,
            force_lowercase=self._force_lowercase_file_name,
            )
        if new_path is not None:
            manager._path = new_path
        self._session._is_backtracking_locally = False

    @Command('ws', section='view', outside_score='home')
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
            manager = self._get_views_package_manager()
            metadatum_name = '{}_view_name'.format(type(self).__name__)
        manager._add_metadatum(
            manager._session,
            manager._metadata_py_path,
            metadatum_name,
            view_name,
            )