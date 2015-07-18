# -*- encoding: utf-8 -*-
import os
from abjad.tools import datastructuretools
from abjad.tools import systemtools
from ide.idetools.ScoreInternalPackageWrangler import \
    ScoreInternalPackageWrangler


class SegmentPackageWrangler(ScoreInternalPackageWrangler):
    r'''Segment package wrangler.

    ..  container:: example

        ::

            >>> abjad_ide = ide.idetools.AbjadIDE(is_test=True)
            >>> wrangler = abjad_ide._segment_package_wrangler
            >>> wrangler
            SegmentPackageWrangler()

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        )

    ### INITIALIZER ###

    def __init__(self, session=None):
        from ide import idetools
        superclass = super(SegmentPackageWrangler, self)
        superclass.__init__(session=session)
        self._asset_identifier = 'segment package'
        self._basic_breadcrumb = 'segments'
        self._manager_class = idetools.SegmentPackageManager
        self._score_storehouse_path_infix_parts = ('segments',)

    ### PRIVATE PROPERTIES ###

    @property
    def _command_to_method(self):
        superclass = super(SegmentPackageWrangler, self)
        result = superclass._command_to_method
        result = result.copy()
        result.update({
            })
        return result

    ### PRIVATE METHODS ###

    def _enter_run(self):
        self._session._is_navigating_to_segments = False

    def _get_first_segment_name(self):
        managers = self._list_visible_asset_managers()
        if managers:
            return managers[0]._get_metadatum('name')

    def _handle_numeric_user_input(self, result):
        manager = self._initialize_manager(result)
        manager._run()

    def _is_valid_directory_entry(self, expr):
        superclass = super(SegmentPackageWrangler, self)
        if superclass._is_valid_directory_entry(expr):
            if '.' not in expr:
                return True
        return False

    def _make_all_packages_menu_section(self, menu, commands_only=False):
        superclass = super(SegmentPackageWrangler, self)
        commands = superclass._make_all_packages_menu_section(
            menu, commands_only=True)
        commands.append(('all packages - definition.py - illustrate', 'di*'))
        if commands_only:
            return commands
        menu.make_command_section(
            commands=commands,
            is_hidden=True,
            name='all packages',
            )

    def _make_asset(self, path, metadata=None):
        metadata = datastructuretools.TypedOrderedDict(metadata or {})
        assert not os.path.exists(path)
        os.mkdir(path)
        manager = self._manager_class(
            path=path,
            session=self._session,
            )
        manager.write_init_py()
        manager.write_definition_py()

    def _make_main_menu(self):
        superclass = super(SegmentPackageWrangler, self)
        menu = superclass._make_main_menu()
        self._make_all_packages_menu_section(menu)
        self._make_segments_menu_section(menu)
        self._make_sibling_asset_tour_menu_section(menu)
        return menu

    def _make_segments_menu_section(self, menu):
        commands = []
        commands.append(('segments - copy', 'cp'))
        commands.append(('segments - new', 'new'))
        commands.append(('segments - rename', 'ren'))
        commands.append(('segments - remove', 'rm'))
        menu.make_command_section(
            commands=commands,
            name='segments',
            )

    def _set_is_navigating_to_sibling_asset(self):
        self._session._is_navigating_to_segments = True

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

    ### PUBLIC METHODS ###

    def copy_package(self):
        r'''Copies package.

        Returns none.
        '''
        self._copy_asset()

    def edit_every_definition_py(self):
        r'''Edits ``definition.py`` in every package.

        Returns none.
        '''
        self._open_in_every_package('definition.py', verb='edit')

#    def illustrate_every_definition_py(self):
#        r'''Illustrates ``definition.py`` in every package.
#
#        Returns none.
#        '''
#        managers = self._list_visible_asset_managers()
#        inputs, outputs = [], []
#        method_name = 'illustrate_definition_py'
#        for manager in managers:
#            method = getattr(manager, method_name)
#            inputs_, outputs_ = method(dry_run=True)
#            inputs.extend(inputs_)
#            outputs.extend(outputs_)
#        messages = self._format_messaging(inputs, outputs, verb='illustrate')
#        self._io_manager._display(messages)
#        result = self._io_manager._confirm()
#        if self._session.is_backtracking or not result:
#            return
#        for manager in managers:
#            method = getattr(manager, method_name)
#            method()

    def open_every_illustration_pdf(self):
        r'''Opens ``illustration.pdf`` file in every package.

        Returns none.
        '''
        self._open_in_every_package('illustration.pdf')

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