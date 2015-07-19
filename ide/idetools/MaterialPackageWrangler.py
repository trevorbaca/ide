# -*- encoding: utf-8 -*-
import os
import traceback
from abjad.tools import systemtools
from ide.idetools.PackageWrangler import PackageWrangler


class MaterialPackageWrangler(PackageWrangler):
    r'''Material package wrangler.

    ..  container:: example

        ::

            >>> session = ide.idetools.Session()
            >>> wrangler = ide.idetools.MaterialPackageWrangler(
            ...     session=session,
            ...     )
            >>> wrangler
            MaterialPackageWrangler()

    ..  container:: example

        ::

            >>> session = ide.idetools.Session()
            >>> session._set_test_score('red_example_score')
            >>> wrangler_in_score = ide.idetools.MaterialPackageWrangler(
            ...     session=session,
            ...     )
            >>> wrangler_in_score
            MaterialPackageWrangler()

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        )

    ### INITIALIZER ###

    def __init__(self, session=None):
        from ide import idetools
        superclass = super(MaterialPackageWrangler, self)
        superclass.__init__(session=session)
        configuration = self._configuration
        self._asset_identifier = 'material package'
        self._basic_breadcrumb = 'materials'
        self._in_library = True
        self._manager_class = idetools.MaterialPackageManager
        self._score_storehouse_path_infix_parts = ('materials',)

    ### PRIVATE PROPERTIES ###

    @property
    def _breadcrumb(self):
        superclass = super(MaterialPackageWrangler, self)
        breadcrumb = superclass._breadcrumb
        if self._session.is_in_library:
            breadcrumb = '{} - library'.format(breadcrumb)
        return breadcrumb

    @property
    def _command_to_method(self):
        superclass = super(MaterialPackageWrangler, self)
        result = superclass._command_to_method
        result = result.copy()
        result.update({
            })
        return result

    ### PRIVATE METHODS ###

    def _enter_run(self):
        self._session._is_navigating_to_materials = False

    def _is_valid_directory_entry(self, expr):
        superclass = super(MaterialPackageWrangler, self)
        if superclass._is_valid_directory_entry(expr):
            if '.' not in expr:
                return True
        return False

    def _list_asset_paths(
        self,
        abjad_material_packages_and_stylesheets=True,
        library=True,
        example_score_packages=True,
        user_score_packages=True,
        output_material_class_name='',
        ):
        from ide import idetools
        superclass = super(MaterialPackageWrangler, self)
        paths = superclass._list_asset_paths(
            abjad_material_packages_and_stylesheets=abjad_material_packages_and_stylesheets,
            library=library,
            example_score_packages=example_score_packages,
            user_score_packages=user_score_packages,
            )
        if not output_material_class_name:
            return paths
        result = []
        for path in paths:
            manager = idetools.PackageManager(
                path=path,
                session=self._session,
                )
            metadatum = manager._get_metadatum('output_material_class_name')
            if metadatum and metadatum == output_material_class_name:
                result.append(path)
        return result

    def _make_main_menu(self):
        superclass = super(MaterialPackageWrangler, self)
        menu = superclass._make_main_menu()
        self._make_all_packages_menu_section(menu)
        self._make_material_command_menu_section(menu)
        self._make_sibling_asset_tour_menu_section(menu)
        return menu

    def _make_material_command_menu_section(self, menu):
        commands = []
        commands.append(('materials - copy', 'cp'))
        commands.append(('materials - new', 'new'))
        commands.append(('materials - remove', 'rm'))
        commands.append(('materials - rename', 'ren'))
        menu.make_command_section(
            commands=commands,
            name='material',
            )

    def _set_is_navigating_to_sibling_asset(self):
        self._session._is_navigating_to_materials = True

    ### PUBLIC METHODS ###

    def copy_package(self):
        r'''Copies package.

        Returns none.
        '''
        self._copy_asset()

#    def edit_every_definition_py(self):
#        r'''Opens ``definition.py`` in every package.
#
#        Returns none.
#        '''
#        self._open_in_every_package('definition.py')

#    def open_every_illustration_pdf(self):
#        r'''Opens ``illustration.pdf`` in every package.
#
#        Returns none.
#        '''
#        self._open_in_every_package('illustration.pdf')

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