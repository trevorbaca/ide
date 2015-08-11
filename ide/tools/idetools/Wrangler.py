# -*- encoding: utf-8 -*-
import datetime
import os
import shutil
import traceback
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
        self._copy_target_directory = None
        self._directory_entry_predicate = self._is_valid_directory_entry
        self._directory_name = None
        self._file_extension = ''
        self._file_name_predicate = None
        self._force_dash_case_file_name = False
        self._force_lowercase_file_name = True
        self._group_asset_section_by_annotation = True
        self._new_file_contents = ''
        self._only_example_scores_during_test = False
        self._sort_by_annotation = True

    ### SPECIAL METHODS ###

    def __repr__(self):
        r'''Gets interpreter representation of wrangler.

        Returns string.
        '''
        return '{}({!r})'.format(type(self).__name__, self._directory_name)

    ### PRIVATE METHODS ###

    def _configure_as_build_file_wrangler(self):
        self._asset_identifier = 'file'
        self._directory_entry_predicate = self._is_valid_file_directory_entry
        self._directory_name = 'build'
        self._file_name_predicate = stringtools.is_dash_case
        self._force_dash_case_file_name = True
        return self

    def _configure_as_distribution_file_wrangler(self):
        self._asset_identifier = 'file'
        self._directory_entry_predicate = self._is_valid_file_directory_entry
        self._directory_name = 'distribution'
        self._file_name_predicate = stringtools.is_dash_case
        self._force_dash_case_file_name = True

    def _configure_as_etc_file_wrangler(self):
        self._asset_identifier = 'file'
        self._directory_entry_predicate = self._is_valid_file_directory_entry
        self._directory_name = 'etc'
        self._file_name_predicate = stringtools.is_dash_case
        self._force_dash_case_file_name = True

    def _configure_as_maker_file_wrangler(self):
        self._asset_identifier = 'file'
        self._directory_entry_predicate = self._is_valid_file_directory_entry
        self._directory_name = 'makers'
        self._file_extension = '.py'
        self._file_name_predicate = stringtools.is_upper_camel_case
        self._force_lowercase_file_name = False

    def _configure_as_material_package_wrangler(self):
        self._asset_identifier = 'package'
        self._directory_entry_predicate = \
            self._is_valid_package_directory_entry
        self._directory_name = 'materials'

    def _configure_as_score_package_wrangler(self):
        self._asset_identifier = 'package'
        self._copy_target_directory = configuration.composer_scores_directory
        self._directory_entry_predicate = \
            self._is_valid_package_directory_entry
        self._directory_name = 'scores'
        self._group_asset_section_by_annotation = False
        self._only_example_scores_during_test = True
        self._sort_by_annotation = False

    def _configure_as_segment_package_wrangler(self):
        self._asset_identifier = 'package'
        self._directory_entry_predicate = \
            self._is_valid_package_directory_entry
        self._directory_name = 'segments'

    def _configure_as_stylesheet_wrangler(self):
        self._asset_identifier = 'file'
        self._directory_entry_predicate = self._is_valid_file_directory_entry
        self._directory_name = 'stylesheets'
        self._file_extension = '.ily'
        self._file_name_predicate = stringtools.is_dash_case
        self._force_dash_case_file_name = True

    def _configure_as_test_file_wrangler(self):
        self._asset_identifier = 'file'
        self._directory_entry_predicate = self._is_valid_file_directory_entry
        self._directory_name = 'test'
        self._allow_asset_name_underscores = True
        self._file_extension = '.py'
        self._file_name_predicate = stringtools.is_snake_case
        return self

    def _confirm_segment_names(self, score_directory):
        segment_package_wrangler = \
            self._session._abjad_ide._segment_package_wrangler
        segments_directory = os.path.join(score_directory, 'segments')
        view_name = segment_package_wrangler._read_view_name(
            segments_directory,
            )
        view_inventory = segment_package_wrangler._read_view_inventory(
            'segments',
            )
        if not view_inventory or view_name not in view_inventory:
            view_name = None
        segment_paths = segment_package_wrangler._list_visible_asset_paths()
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
        if self._io_manager._is_backtracking or not result:
            return False
        return segment_names

    def _edit_file_ending_with(self, string):
        directory_path = self._get_current_directory()
        file_path = self._get_file_path_ending_with(directory_path, string)
        if file_path:
            self._io_manager.edit(file_path)
        else:
            message = 'file ending in {!r} not found.'
            message = message.format(string)
            self._io_manager._display(message)

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
        if self._directory_name == 'scores':
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
        composer_score_packages = False
        if system and inside_score:
            example_score_packages = True
        elif not system and inside_score:
            composer_score_packages = True
        else:
            Exception
        asset_paths = self._list_asset_paths(
            self._directory_name,
            self._directory_entry_predicate,
            example_score_packages=example_score_packages,
            composer_score_packages=composer_score_packages,
            )
        if self._directory_name == 'scores':
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
            if (manager._is_git_versioned(manager._path)
                and manager._is_up_to_date(manager._path)
                and
                (not must_have_file or 
                manager._find_first_file_name(manager._path))):
                return manager

    def _get_available_path(
        self,
        message=None,
        storehouse=None,
        ):
        if storehouse is None:
            storehouse = self._get_current_storehouse(
                self._session,
                self._directory_name,
                )
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
            path = os.path.join(storehouse, name)
            if os.path.exists(path):
                line = 'path already exists: {!r}.'
                line = line.format(path)
                self._io_manager._display(line)
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

    @classmethod
    def _get_current_package_manager(class_, io_manager, directory_token):
        if os.path.sep in directory_token:
            return io_manager._make_package_manager(directory_token)

    @staticmethod
    def _get_current_storehouse(session, directory_name):
        if session.is_in_score:
            return os.path.join(
                session.current_score_directory,
                directory_name,
                )
        return configuration.composer_scores_directory

    def _get_manager(self, path):
        from ide.tools import idetools
        assert os.path.sep in path, repr(path)
        manager = idetools.PackageManager(
            path=path,
            session=self._session,
            )
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

    def _list_visible_asset_managers(self):
        paths = self._list_visible_asset_paths()
        managers = []
        for path in paths:
            manager = self._get_manager(path)
            managers.append(manager)
        return managers

    def _make_asset(self, asset_name):
        if os.path.sep in asset_name:
            asset_name = os.path.basename(asset_name)
        assert stringtools.is_snake_case(asset_name)
        current_storehouse = self._get_current_storehouse(
            self._session,
            self._directory_name,
            )
        path = os.path.join(
            current_storehouse,
            asset_name,
            )
        manager = self._get_manager(path)
        with self._io_manager._silent():
            manager.check_package(
                return_supply_messages=True,
                supply_missing=True,
                )
        paths = self._list_visible_asset_paths()
        if path not in paths:
            with self._io_manager._silent():
                self._clear_view(self._io_manager, self._directory_name)
        self._session._pending_redraw = True

    def _make_asset_menu_entries(
        self,
        apply_current_directory=True,
        set_view=True,
        ):
        paths = self._list_asset_paths(
            self._directory_name,
            self._directory_entry_predicate,
            )
        current_directory = self._get_current_directory()
        if (apply_current_directory or set_view) and current_directory:
            paths = [_ for _ in paths if _.startswith(current_directory)]
        strings = []
        for path in paths:
            string = self._path_to_asset_menu_display_string(
                path,
                self._allow_asset_name_underscores,
                )
            strings.append(string)
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
            directory_token = self._get_current_directory_token(
                self._session,
                self._directory_name,
                )
            entries = self._filter_asset_menu_entries_by_view(
                directory_token,
                entries,
                )
        if self._session.is_test and self._only_example_scores_during_test:
            entries = [_ for _ in entries if 'Example Score' in _[0]]
        elif not self._session.is_test:
            entries = [_ for _ in entries if 'Example Score' not in _[0]]
        return entries

    def _make_wrangler_asset_menu_section(self, menu, directory=None):
        menu_entries = []
        if directory is not None:
            current_directory = directory
        else:
            current_directory = self._get_current_directory()
        if current_directory:
            menu_entries_ = self._make_secondary_asset_menu_entries(
                current_directory)
            menu_entries.extend(menu_entries_)
        menu_entries.extend(self._make_asset_menu_entries())
        if menu_entries:
            section = menu.make_asset_section(menu_entries=menu_entries)
            assert section is not None
            section._group_by_annotation = \
                self._group_asset_section_by_annotation

    def _make_asset_selection_menu(self):
        menu = self._io_manager._make_menu(name='asset selection')
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
            path = self._select_storehouse()
            if self._session.is_backtracking or path is None:
                return
        getter = self._io_manager._make_getter()
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
        self._io_manager.write(path, contents)
        self._io_manager.edit(path)

    def _make_package(self):
        if self._session.is_in_score:
            storehouse = self._get_current_storehouse(
                self._session,
                self._directory_name,
                )
        else:
            example_score_packages = self._session.is_test
            storehouse = self._select_storehouse(
                example_score_packages=example_score_packages,
                )
            if self._session.is_backtracking or storehouse is None:
                return
        path = self._get_available_path(storehouse=storehouse)
        if self._session.is_backtracking or not path:
            return
        message = 'path will be {}.'.format(path)
        self._io_manager._display(message)
        result = self._io_manager._confirm()
        if self._session.is_backtracking or not result:
            return
        manager = self._get_manager(path)
        new_path = manager._make_package(manager._path)
        if new_path is not None:
            manager._new_path = new_path
        paths = self._list_visible_asset_paths()
        if path not in paths:
            with self._io_manager._silent():
                self._clear_view(self._io_manager, self._directory_name)
        manager._run_package_manager_menu(manager._path)

    def _make_score_package(self):
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
                configuration.composer_scores_directory,
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
        new_path = manager._make_package(manager._path)
        if new_path is not None:
            manager._path = new_path
        manager._add_metadatum(
            manager._path,
            'title',
            title,
            )
        year = datetime.date.today().year
        manager._add_metadatum(
            manager._path,
            'year',
            year,
            )
        package_paths = self._list_visible_asset_paths()
        if package_path not in package_paths:
            with self._io_manager._silent():
                self._clear_view(self._io_manager, self._directory_name)
        manager._run_package_manager_menu(manager._path)

    def _make_storehouse_menu_entries(
        self,
        example_score_packages=True,
        composer_score_packages=True,
        ):
        from ide.tools import idetools
        display_strings, keys = [], []
        wrangler = self._session._abjad_ide._score_package_wrangler
        paths = wrangler._list_asset_paths(
            self._directory_name,
            self._directory_entry_predicate,
            example_score_packages=example_score_packages,
            composer_score_packages=composer_score_packages,
            )
        for path in paths:
            manager = wrangler._get_manager(path)
            title = manager._get_title_metadatum(
                manager._path,
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
        manager = self._io_manager._make_package_manager(path)
        count = pattern.count('md:')
        for _ in range(count+1):
            parts = pattern.split()
            for part in parts:
                if part.startswith('md:'):
                    metadatum_name = part[3:]
                    metadatum = manager._get_metadatum(
                        manager._path,
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

    def _open_file_ending_with(self, string):
        directory_path = self._get_current_directory()
        path = self._get_file_path_ending_with(directory_path, string)
        if path:
            self._io_manager.open_file(path)
        else:
            message = 'file ending in {!r} not found.'
            message = message.format(string)
            self._io_manager._display(message)

    def _run_wrangler(self, directory=None):
        controller = self._io_manager._controller(
            consume_local_backtrack=True,
            controller=self,
            on_enter_callbacks=(self._enter_run,),
            )
        directory_change = systemtools.NullContextManager()
        if directory is not None:
            directory_change = systemtools.TemporaryDirectoryChange(directory)
        elif self._session.is_in_score:
            path = self._get_current_directory()
            directory_change = systemtools.TemporaryDirectoryChange(path)
        with controller, directory_change:
            result = None
            self._session._pending_redraw = True
            while True:
                result = self._get_sibling_asset_path()
                if not result:
                    current_directory = self._get_current_directory()
                    if current_directory is not None:
                        menu_header = self._path_to_menu_header(
                            current_directory)
                    elif self._directory_name == 'scores':
                        menu_header = 'Abjad IDE - all score directories'
                    else:
                        menu_header = 'Abjad IDE - all {} directories'
                        menu_header = menu_header.format(self._directory_name)
                    menu = self._make_main_menu(
                        explicit_header=menu_header,
                        _path=directory,
                        )
                    result = menu._run()
                    self._handle_pending_redraw_directive(
                        self._session,
                        result,
                        )
                    self._handle_wrangler_navigation_directive(
                        self._session,
                        result,
                        )
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

    def _select_storehouse(self, example_score_packages=False):
        menu_entries = self._make_storehouse_menu_entries(
            example_score_packages=example_score_packages,
            composer_score_packages=False,
            )
        current_directory = self._get_current_directory()
        if current_directory is not None:
            menu_header = self._path_to_menu_header(current_directory)
        elif self._directory_name == 'scores':
            menu_header = 'Abjad IDE - all score directories'
        else:
            menu_header = 'Abjad IDE - all {} directories'
            menu_header = menu_header.format(self._directory_name)
        selector = self._io_manager._make_selector(
            menu_entries=menu_entries,
            menu_header=menu_header,
            target_name='storehouse',
            )
        result = selector._run()
        if self._session.is_backtracking or result is None:
            return
        return result

    def _select_view(self, infinitive_phrase=None, is_ranged=False):
        from ide.tools import idetools
        directory_token = self._get_current_directory_token(
            self._session,
            self._directory_name,
            )
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
        if infinitive_phrase:
            target_name = '{} {}'.format(target_name, infinitive_phrase)
        current_directory = self._get_current_directory()
        if current_directory is not None:
            menu_header = self._path_to_menu_header(current_directory)
        elif self._directory_name == 'scores':
            menu_header = 'Abjad IDE - all score directories'
        else:
            menu_header = 'Abjad IDE - all {} directories'
            menu_header = menu_header.format(self._directory_name)
        selector = self._io_manager._make_selector(
            is_ranged=is_ranged,
            items=view_names,
            menu_header=menu_header,
            target_name=target_name,
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
        if hasattr(self, '_make_wrangler_asset_menu_section'):
            dummy_menu = self._io_manager._make_menu()
            self._make_wrangler_asset_menu_section(dummy_menu)
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
        message = 'enter {}(s) to remove'
        message = message.format(self._asset_identifier)
        menu = self._make_asset_selection_menu()
        asset_section = menu['assets']
        getter.append_menu_section_range(
            message, 
            asset_section,
            )
        numbers = getter._run()
        if self._io_manager._is_backtracking or numbers is None:
            return
        indices = [_ - 1 for _ in numbers]
        paths = [_.return_value for _ in asset_section.menu_entries]
        paths = sequencetools.retain_elements(paths, indices)
        return paths