# -*- encoding: utf-8 -*-
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
        self._manager_class = idetools.MaterialPackageManager
        self._score_storehouse_path_infix_parts = ('materials',)

    ### PRIVATE METHODS ###

    def _make_all_packages_menu_section(self, menu, commands_only=False):
        superclass = super(MaterialPackageWrangler, self)
        commands = superclass._make_all_packages_menu_section(
            menu, commands_only=True)
        commands.append(('check all definition.py files', 'dc*'))
        commands.append(('edit all definition.py files', 'de*'))
        commands.append(('interpret all illustration.ly files', 'ii*'))
        commands.append(('open all illustration.pdf files', 'io*'))
        if commands_only:
            return commands
        menu.make_command_section(
            commands=commands,
            is_hidden=True,
            name='zzz',
            )

    def _make_main_menu(self):
        superclass = super(MaterialPackageWrangler, self)
        menu = superclass._make_main_menu()
        self._make_sibling_asset_tour_menu_section(menu)
        return menu

    def _set_is_navigating_to_sibling_asset(self):
        self._session._is_navigating_to_materials = True