# -*- encoding: utf-8 -*-
import datetime
import os
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
        )

    ### PRIVATE METHODS ###

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
        self._make_all_packages_repository_menu_section(menu)
        self._make_show_all_menu_section(menu)
        return menu

    ### PUBLIC METHODS ###

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