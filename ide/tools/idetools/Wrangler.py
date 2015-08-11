# -*- encoding: utf-8 -*-
import os
from abjad.tools import sequencetools
from abjad.tools import stringtools
from abjad.tools import systemtools
from ide.tools.idetools.AbjadIDEConfiguration import AbjadIDEConfiguration
from ide.tools.idetools.Controller import Controller
configuration = AbjadIDEConfiguration()


class Wrangler(Controller):
    r'''Wrangler.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_directory_name',
        )

    ### INITIALIZER ###

    def __init__(self, session=None, io_manager=None):
        assert session is not None
        assert io_manager is not None
        superclass = super(Wrangler, self)
        superclass.__init__(session=session, io_manager=io_manager)
        self._directory_name = None

    ### SPECIAL METHODS ###

    def __repr__(self):
        r'''Gets interpreter representation of wrangler.

        Returns string.
        '''
        return '{}({!r})'.format(type(self).__name__, self._directory_name)

    ### PRIVATE METHODS ###

    def _get_current_storehouse(self):
        if self._session.is_in_score:
            return os.path.join(
                self._session.current_score_directory,
                self._directory_name,
                )
        return configuration.composer_scores_directory

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

    def _make_asset_menu_entries(
        self,
        apply_current_directory=True,
        set_view=True,
        ):
        paths = self._list_asset_paths(self._directory_name)
        current_directory = self._get_current_directory()
        if (apply_current_directory or set_view) and current_directory:
            paths = [_ for _ in paths if _.startswith(current_directory)]
        strings = []
        for path in paths:
            string = self._path_to_asset_menu_display_string(path)
            strings.append(string)
        pairs = list(zip(strings, paths))
        if (not self._session.is_in_score and
            not self._directory_name == 'scores'):
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
            directory_token = self._get_current_directory_token()
            entries = self._filter_asset_menu_entries_by_view(
                directory_token,
                entries,
                )
        if self._session.is_test and self._directory_name == 'scores':
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
            section._group_by_annotation = not self._directory_name == 'scores'

    def _make_asset_selection_menu(self):
        menu = self._io_manager._make_menu(name='asset selection')
        menu_entries = self._make_asset_menu_entries()
        menu.make_asset_section(menu_entries=menu_entries)
        return menu

    def _run_wrangler(self, directory_name):
        from ide.tools import idetools
        assert (directory_name in self._known_directory_names or
            directory_name == 'scores'), repr(directory_name)
        controller = self._io_manager._controller(
            consume_local_backtrack=True,
            controller=self,
            on_enter_callbacks=(self._enter_run,),
            )
        current_directory = configuration.composer_scores_directory
        if not self._session.manifest_current_directory == current_directory:
            current_directory = os.path.join(
                self._session.manifest_current_directory,
                directory_name,
                )
        directory_change = systemtools.TemporaryDirectoryChange(
            current_directory)
        current_directory = idetools.CurrentDirectory(
            current_directory=current_directory,
            session=self._session,
            )
        with controller, directory_change, current_directory:
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
                        _path=None,
                        )
                    result = menu._run(io_manager=self._io_manager)
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

    def _select_storehouse(self, example_score_packages=False):
        menu_entries = self._make_storehouse_menu_entries(
            self._directory_name,
            composer_score_packages=False,
            example_score_packages=example_score_packages,
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
        result = selector._run(io_manager=self._io_manager)
        if self._session.is_backtracking or result is None:
            return
        return result

    def _select_view(self, infinitive_phrase=None, is_ranged=False):
        from ide.tools import idetools
        directory_token = self._get_current_directory_token()
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
        result = selector._run(io_manager=self._io_manager)
        if self._session.is_backtracking or result is None:
            return
        return result

    def _select_visible_asset_path(self, infinitive_phrase=None):
        getter = self._io_manager._make_getter()
        asset_identifier = self._directory_name_to_asset_identifier[
            self._directory_name]
        message = 'enter {}'.format(asset_identifier)
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
        numbers = getter._run(io_manager=self._io_manager)
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
        asset_identifier = self._directory_name_to_asset_identifier[
            self._directory_name]
        message = 'enter {}(s) to remove'
        message = message.format(asset_identifier)
        menu = self._make_asset_selection_menu()
        asset_section = menu['assets']
        getter.append_menu_section_range(
            message, 
            asset_section,
            )
        numbers = getter._run(io_manager=self._io_manager)
        if self._io_manager._is_backtracking or numbers is None:
            return
        indices = [_ - 1 for _ in numbers]
        paths = [_.return_value for _ in asset_section.menu_entries]
        paths = sequencetools.retain_elements(paths, indices)
        return paths