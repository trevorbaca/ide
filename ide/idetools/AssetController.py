# -*- encoding: utf-8 -*-
from __future__ import print_function
import os
import shutil
from abjad.tools import datastructuretools
from abjad.tools import developerscripttools
from abjad.tools import stringtools
from abjad.tools import systemtools
from ide.idetools.Controller import Controller


class AssetController(Controller):
    r'''Asset controller.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_annotate_year',
        '_asset_identifier',
        '_basic_breadcrumb',
        '_commands',
        '_group_asset_section_by_annotation',
        '_has_breadcrumb_in_score',
        '_human_readable',
        '_include_asset_name',
        '_include_extensions',
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
        self._annotate_year = False
        self._asset_identifier = None
        self._basic_breadcrumb = None
        self._commands = {}
        self._group_asset_section_by_annotation = True
        self._has_breadcrumb_in_score = True
        self._human_readable = True
        self._include_asset_name = True
        self._include_extensions = False

    ### PRIVATE PROPERTIES ###

    @property
    def _command_to_method(self):
        superclass = super(AssetController, self)
        result = superclass._command_to_method
        result = result.copy()
        result.update({
            'dd': self.go_to_all_distribution_files,
            'ee': self.go_to_all_etc_files,
            'gg': self.go_to_all_segments,
            'kk': self.go_to_all_maker_files,
            'mm': self.go_to_all_materials,
            'uu': self.go_to_all_build_files,
            'yy': self.go_to_all_stylesheets,
            #
            'cc': self.check_contents,
            #
            '!': self.invoke_shell,
            '?': self.display_available_commands,
            'l': self.open_lilypond_log,
            #
            '<<': self.go_to_previous_score,
            '>>': self.go_to_next_score,
            #
            'd': self.go_to_score_distribution_files,
            'e': self.go_to_score_etc_files,
            'g': self.go_to_score_segments,
            'k': self.go_to_score_maker_files,
            'm': self.go_to_score_materials,
            'u': self.go_to_score_build_files,
            'y': self.go_to_score_stylesheets,
            #
            'abb': self.edit_abbreviations_file,
            'sse': self.edit_score_stylesheet,
            })
        result.update(self._commands)
        return result

    @property
    def _navigation_commands(self):
        result = (
            'b', 'q',
            'dd', 'ee', 'gg', 'kk', 'mm', 'h', 'uu', 'yy',
            'd', 'e', 'g', 'k', 'm', 's', 'u', 'y',
            )
        return result

    @property
    def _views_package_manager(self):
        path = self._configuration.wrangler_views_directory
        return self._io_manager._make_package_manager(path)

    ### PRIVATE METHODS ###

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
            parts = (score_directory,)
            parts += self._score_storehouse_path_infix_parts
            directory = os.path.join(*parts)
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
        score_path = self._configuration._path_to_score_path(self._path)
        if score_path is None:
            return datastructuretools.TypedOrderedDict()
        score_package_manager = self._io_manager._make_package_manager(
            path=score_path)
        return score_package_manager._get_metadata()

    def _go_to_next_package(self):
        self._session._is_navigating_to_next_asset = True
        self._session._display_available_commands = False
        self._set_is_navigating_to_sibling_asset()

    def _go_to_previous_package(self):
        self._session._is_navigating_to_previous_asset = True
        self._session._display_available_commands = False
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
            elif result in self._command_to_method:
                self._command_to_method[result]()
            elif (result.endswith('!') and 
                result[:-1] in self._command_to_method):
                result = result[:-1]
                with self._io_manager._make_interaction(confirm=False):
                    self._command_to_method[result]()
            else:
                self._handle_numeric_user_input(result)

    def _handle_numeric_user_input(self, result):
        if os.path.isfile(result):
            self._io_manager.open_file(result)
        elif os.path.isdir(result):
            basename = os.path.basename(result)
            if basename == 'build':
                self.go_to_score_build_files()
            elif basename == 'distribution':
                self.go_to_score_distribution_files()
            elif basename == 'etc':
                self.go_to_score_etc_files()
            elif basename == 'makers':
                self.go_to_score_maker_files()
            elif basename == 'materials':
                self.go_to_score_materials()
            elif basename == 'segments':
                self.go_to_score_segments()
            elif basename == 'stylesheets':
                self.go_to_score_stylesheets()
            elif basename == 'test':
                self.go_to_score_test_files()
            else:
                manager = self._initialize_manager(result)
                manager._run()
        else:
            message = 'must be file or directory: {!r}.'
            message = message.format(result)
            raise Exception(message)

    def _is_valid_directory_entry(self, directory_entry):
        if directory_entry[0].isalpha():
            if not directory_entry.endswith('.pyc'):
                return True
        return False

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
        if self._session.is_test:
            if getattr(self, '_only_example_scores_during_test', False):
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

    def _make_go_menu_section(self, menu, commands_only=False, packages=False):
        commands = []
        if packages:
            commands.append(('next package', '>'))
            commands.append(('previous package', '<'))
        commands.append(('next score', '>>'))
        commands.append(('previous score', '<<'))
        if commands_only:
            return commands
        if commands:
            menu.make_command_section(
                is_hidden=True,
                commands=commands,
                name='go',
                )

    def _make_navigation_menu_section(self, menu):
        commands = []
        if self._session.is_in_score:
            commands.append(('score', 's'))
            commands.append(('build', 'u'))
            commands.append(('distribution', 'd'))
            commands.append(('etc', 'e'))
            commands.append(('makers', 'k'))
            commands.append(('materials', 'm'))
            commands.append(('segments', 'g'))
            commands.append(('stylesheets', 'y'))
        if commands:
            menu.make_command_section(
                is_hidden=True,
                commands=commands,
                name='navigation',
                )

    def _make_main_menu(self):
        name = self._spaced_class_name
        menu = self._io_manager._make_menu(name=name)
        if self._session.is_in_score:
            self._make_score_stylesheet_menu_section(menu)
        self._make_go_menu_section(menu)
        self._make_navigation_menu_section(menu)
        self._make_system_menu_section(menu)
        return menu

    def _make_score_stylesheet_menu_section(self, menu):
        commands = []
        commands.append(('edit abbreviations', 'abb'))
        commands.append(('edit stylesheet', 'sse'))
        menu.make_command_section(
            is_hidden=True,
            commands=commands,
            name='score stylesheet',
            )

    def _make_sibling_asset_tour_menu_section(self, menu):
        section = menu['go']
        menu.menu_sections.remove(section)
        self._make_go_menu_section(menu, packages=True)

    def _make_system_menu_section(self, menu):
        commands = []
        commands.append(('back', 'b'))
        commands.append(('help', '?'))
        commands.append(('home', 'h'))
        commands.append(('log', 'l'))
        commands.append(('quit', 'q'))
        commands.append(('shell', '!'))
        menu.make_command_section(
            is_hidden=True,
            commands=commands,
            name='aaa',
            )

    def _open_file(self, path):
        if os.path.isfile(path):
            self._io_manager.open_file(path)
        else:
            message = 'can not find file: {}.'
            message = message.format(path)
            self._io_manager._display(message)

    def _path_to_annotation(self, path):
        score_storehouses = (
            self._configuration.example_score_packages_directory,
            self._configuration.user_score_packages_directory,
            )
        if (path.startswith(score_storehouses) and
            not getattr(self, '_simple_score_annotation', False)):
            score_path = self._configuration._path_to_score_path(path)
            manager = self._io_manager._make_package_manager(path=score_path)
            metadata = manager._get_metadata()
            if metadata:
                year = metadata.get('year')
                title = metadata.get('title')
                if self._annotate_year and year:
                    annotation = '{} ({})'.format(title, year)
                else:
                    annotation = str(title)
            else:
                package_name = os.path.basename(path)
                annotation = package_name
        elif (path.startswith(score_storehouses) and
            getattr(self, '_simple_score_annotation', False)):
            if self._configuration.example_score_packages_directory in path:
                annotation = 'example scores'
            else:
                annotation = 'scores'
        elif path.startswith(self._configuration.abjad_root_directory):
            annotation = 'Abjad'
        else:
            annotation = None
        return annotation

    def _path_to_asset_menu_display_string(self, path):
        if self._human_readable:
            asset_name = self._path_to_human_readable_name(path)
        else:
            asset_name = os.path.basename(path)
        if 'segments' in path:
            manager = self._io_manager._make_package_manager(path=path)
            name = manager._get_metadatum('name')
            asset_name = name or asset_name
        if self._session.is_in_score:
            string = asset_name
        else:
            annotation = self._path_to_annotation(path)
            if self._include_asset_name:
                string = '{} ({})'.format(asset_name, annotation)
            else:
                string = annotation
        return string

    def _path_to_human_readable_name(self, path):
        path = os.path.normpath(path)
        name = os.path.basename(path)
        include_extensions = self._include_extensions
        if not include_extensions:
            name, extension = os.path.splitext(name)
        return stringtools.to_space_delimited_lowercase(name)

    def _read_view(self):
        view_name = self._read_view_name()
        if not view_name:
            return
        view_inventory = self._read_view_inventory()
        if not view_inventory:
            return
        return view_inventory.get(view_name)

    def _read_view_inventory(self):
        from ide import idetools
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

    def _remove_unadded_assets(self, dry_run=False):
        paths = self._get_unadded_asset_paths()
        inputs, outputs = [], []
        if dry_run:
            inputs, outputs = paths, []
            return inputs, outputs
        elif not paths:
            message = 'no unadded assets.'
            self._io_manager._display(message)
            return
        messages = []
        messages.append('will remove ...')
        for path in paths:
            message = '    ' + path
            messages.append(message)
        self._io_manager._display(messages)
        result = self._io_manager._confirm()
        if self._session.is_backtracking or not result:
            return
        remove_command = self._shell_remove_command
        paths = ' '.join(paths)
        command = '{} {}'
        command = command.format(remove_command, paths)
        self._io_manager.run_command(command)

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

    def _write_metadata_py(self, metadata, metadata_py_path=None):
        lines = []
        lines.append(self._configuration.unicode_directive)
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

    ### PUBLIC METHODS ###

    def add(self, dry_run=False):
        r'''Adds files to repository.

        Returns none.
        '''
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

    def check_contents(self):
        r'''Checks contents.

        Returns none.
        '''
        pass

    def commit(self, commit_message=None):
        r'''Commits files to repository.

        Returns none.
        '''
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

    def display_available_commands(self):
        r'''Displays available commands.

        Returns none.
        '''
        if not self._session.is_in_confirmation_environment:
            show = self._session.display_available_commands
            self._session._display_available_commands = not show

    def display_status(self):
        r'''Displays repository status.

        Returns none.
        '''
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

    def edit_abbreviations_file(self):
        r'''Edits abbreviations file.

        Returns none.
        '''
        path = self._session.current_abbreviations_file_path
        if not path or not os.path.isfile(path):
            with open(path, 'w') as file_pointer:
                file_pointer.write('')
        self._io_manager.edit(path)

    def edit_score_stylesheet(self):
        r'''Edits score stylesheet.

        Returns none.
        '''
        path = self._session.current_stylesheet_path
        if not path or not os.path.isfile(path):
            with open(path, 'w') as file_pointer:
                file_pointer.write('')
        self._io_manager.edit(path)

    def go_to_all_build_files(self):
        r'''Goes to all build files.

        Returns none.
        '''
        self.go_to_all_scores()
        self._session._is_navigating_to_build_files = True

    def go_to_all_distribution_files(self):
        r'''Goes to all distribution files.

        Returns none.
        '''
        self.go_to_all_scores()
        self._session._is_navigating_to_distribution_files = True

    def go_to_all_etc_files(self):
        r'''Goes to all etc files.

        Returns none.
        '''
        self.go_to_all_scores()
        self._session._is_navigating_to_etc_files = True

    def go_to_all_maker_files(self):
        r'''Goes to all maker files.

        Returns none.
        '''
        self.go_to_all_scores()
        self._session._is_navigating_to_maker_files = True

    def go_to_all_materials(self):
        r'''Goes to all materials.

        Returns none.
        '''
        self.go_to_all_scores()
        self._session._is_navigating_to_materials = True

    def go_to_all_segments(self):
        r'''Goes to all segments.

        Returns none.
        '''
        self.go_to_all_scores()
        self._session._is_navigating_to_segments = True

    def go_to_all_stylesheets(self):
        r'''Goes to all stylesheets.

        Returns none.
        '''
        self.go_to_all_scores()
        self._session._is_navigating_to_stylesheets = True

    def go_to_next_score(self):
        r'''Goes to next score.

        Returns none.
        '''
        self._session._is_navigating_to_next_score = True
        self._session._is_navigating_to_scores = True
        self._session._display_available_commands = False

    def go_to_previous_score(self):
        r'''Goes to previous score.

        Returns none.
        '''
        self._session._is_navigating_to_previous_score = True
        self._session._is_navigating_to_scores = True
        self._session._display_available_commands = False

    def go_to_score_build_files(self):
        r'''Goes to build files.

        Returns none.
        '''
        self._session._abjad_ide._build_file_wrangler._run()

    def go_to_score_distribution_files(self):
        r'''Goes to distribution files.

        Returns none.
        '''
        self._session._abjad_ide._distribution_file_wrangler._run()

    def go_to_score_etc_files(self):
        r'''Goes to etc files.

        Returns none.
        '''
        self._session._abjad_ide._etc_file_wrangler._run()

    def go_to_score_maker_files(self):
        r'''Goes to maker files.

        Returns none.
        '''
        self._session._abjad_ide._maker_file_wrangler._run()

    def go_to_score_materials(self):
        r'''Goes to material packages.

        Returns none.
        '''
        self._session._abjad_ide._material_package_wrangler._run()

    def go_to_score_segments(self):
        r'''Goes to segment packages.

        Returns none.
        '''
        self._session._abjad_ide._segment_package_wrangler._run()

    def go_to_score_stylesheets(self):
        r'''Goes to stylesheets.

        Returns none.
        '''
        self._session._abjad_ide._stylesheet_wrangler._run()

    def go_to_score_test_files(self):
        r'''Geots to score test files.

        Returns none.
        '''
        raise NotImplementedError

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

    def open_lilypond_log(self):
        r'''Opens LilyPond log.

        Returns none.
        '''
        from abjad.tools import systemtools
        self._session._attempted_to_open_file = True
        if self._session.is_test:
            return
        systemtools.IOManager.open_last_log()

    def remove_unadded_assets(self, dry_run=False):
        r'''Removes files not yet added to repository.

        Returns none.
        '''
        return self._remove_unadded_assets(dry_run=dry_run)

    def revert(self):
        r'''Reverts files to repository.

        Returns none.
        '''
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

    def update(self, messages_only=False):
        r'''Updates files from repository.

        Returns none.
        '''
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