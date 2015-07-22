# -*- encoding: utf-8 -*-
import datetime
import os
import sys
from abjad.tools import stringtools
from ide.idetools.PackageWrangler import PackageWrangler


class ScorePackageWrangler(PackageWrangler):
    r'''Score package wrangler.

    ..  container:: example

        ::

            >>> session = ide.idetools.Session()
            >>> wrangler = ide.idetools.ScorePackageWrangler(
            ...     session=session,
            ...     )
            >>> wrangler
            ScorePackageWrangler()

    ..  container:: example

        ::

            >>> session = ide.idetools.Session()
            >>> session._set_test_score('red_example_score')
            >>> wrangler_in_score = ide.idetools.ScorePackageWrangler(
            ...     session=session,
            ...     )
            >>> wrangler_in_score
            ScorePackageWrangler()

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_only_example_scores_during_test',
        )

    ### INITIALIZER ###

    def __init__(self, session=None):
        from ide import idetools
        superclass = super(ScorePackageWrangler, self)
        superclass.__init__(session=session)
        self._asset_identifier = 'score package'
        self._basic_breadcrumb = 'scores'
        self._include_asset_name = False
        self._annotate_year = True
        self._allow_depot = False
        self._manager_class = idetools.ScorePackageManager
        self._only_example_scores_during_test = True
        self._sort_by_annotation = False
        path = self._configuration.user_score_packages_directory
        self._user_storehouse_path = path

    ### PRIVATE PROPERTIES ###

    @property
    def _breadcrumb(self):
        if not self._session.is_in_score:
            superclass = super(ScorePackageWrangler, self)
            breadcrumb = superclass._breadcrumb
            return breadcrumb

    @property
    def _command_to_method(self):
        superclass = super(ScorePackageWrangler, self)
        result = superclass._command_to_method
        result = result.copy()
        result.update({
            'so*': self.open_every_score_pdf,
            })
        return result

    @property
    def _current_storehouse_path(self):
        return self._configuration.user_score_packages_directory

    ### PRIVATE METHODS ###

    def _find_git_manager(self, must_have_file=False):
        superclass = super(ScorePackageWrangler, self)
        manager = superclass._find_git_manager(
            inside_score=False,
            must_have_file=must_have_file,
            )
        return manager

    def _get_scores_to_display_string(self):
        view = self._read_view()
        if view:
            view_name = self._read_view_name()
            return 'scores ({})'.format(view_name)
        return 'scores'

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

    def _list_asset_paths(
        self,
        abjad_material_packages_and_stylesheets=True,
        example_score_packages=True,
        user_score_packages=True,
        valid_only=True,
        ):
        result = []
        directories = self._list_storehouse_paths(
            abjad_material_packages_and_stylesheets=abjad_material_packages_and_stylesheets,
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
                    if not self._is_valid_directory_entry(directory_entry):
                        continue
                path = os.path.join(directory, directory_entry)
                # test for installable Python package structure
                outer_init_path = os.path.join(path, '__init__.py')
                inner_directory = os.path.join(path, directory_entry)
                inner_init_path = os.path.join(inner_directory, '__init__.py')
                if not os.path.exists(outer_init_path):
                    if os.path.exists(inner_init_path):
                        path = inner_directory
                result.append(path)
        return result

    def _make_all_packages_menu_section(self, menu):
        superclass = super(ScorePackageWrangler, self)
        commands = superclass._make_all_packages_menu_section(
            menu, commands_only=True)
        commands.append(('open all distribution score.pdf files', 'so*'))
        menu.make_command_section(
            is_hidden=True,
            commands=commands,
            name='zzz',
            )

    def _make_all_packages_repository_menu_section(self, menu):
        commands = []
        commands.append(('git add all score packages', 'add*'))
        commands.append(('git clean all score packages', 'clean*'))
        commands.append(('git commit all score packages', 'ci*'))
        commands.append(('git revert all score packages', 'revert*'))
        commands.append(('git status all score packages', 'st*'))
        commands.append(('git update all score packages', 'up*'))
        menu.make_command_section(
            is_hidden=True,
            commands=commands,
            name='zzz2',
            )

    def _make_show_all_menu_section(self, menu):
        commands = []
        commands.append(('show all build files', 'uu'))
        commands.append(('show all distribution', 'dd'))
        commands.append(('show all etc files', 'ee'))
        commands.append(('show all maker files', 'kk'))
        commands.append(('show all material packages', 'mm'))
        commands.append(('show all segment packages', 'gg'))
        commands.append(('show all stylesheets', 'yy'))
        menu.make_command_section(
            is_hidden=True,
            commands=commands,
            name='show all',
            )

    def _make_main_menu(self):
        superclass = super(ScorePackageWrangler, self)
        menu = superclass._make_main_menu()
        try:
            asset_section = menu['assets']
            asset_section._group_by_annotation = False
        except KeyError:
            pass
        self._make_all_packages_menu_section(menu)
        self._make_all_packages_repository_menu_section(menu)
        self._make_scores_menu_section(menu)
        self._make_show_all_menu_section(menu)
        return menu

    def _make_scores_menu_section(self, menu):
        commands = []
        commands.append(('copy', 'cp'))
        commands.append(('new', 'new'))
        commands.append(('remove', 'rm'))
        commands.append(('rename', 'ren'))
        menu.make_command_section(
            commands=commands,
            name='scores',
            )

    ### PUBLIC METHODS ###

    def copy_package(self):
        r'''Copies package.

        Returns none.
        '''
        path = self._configuration.user_score_packages_directory
        self._copy_asset(new_storehouse=path)

    def make_package(self):
        r'''Makes package.

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

    def remove_packages(self):
        r'''Removes one or more packages.

        Returns none.
        '''
        self._remove_assets()

    def rename_package(self):
        r'''Renames package.

        Returns none.
        '''
        self._rename_asset()