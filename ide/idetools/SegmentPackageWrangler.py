# -*- encoding: utf-8 -*-
import os
from abjad.tools import datastructuretools
from abjad.tools import systemtools
from ide.idetools.PackageWrangler import PackageWrangler


class SegmentPackageWrangler(PackageWrangler):
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

    ### PRIVATE METHODS ###

    def _make_all_packages_menu_section(self, menu, commands_only=False):
        superclass = super(SegmentPackageWrangler, self)
        commands = superclass._make_all_packages_menu_section(
            menu, commands_only=True)
        commands.append(('check all definition.py files', 'dc*'))
        commands.append(('edit all definition.py files', 'de*'))
        commands.append(('illustrate all definition.py files', 'di*'))
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
        superclass = super(SegmentPackageWrangler, self)
        menu = superclass._make_main_menu()
        self._make_sibling_asset_tour_menu_section(menu)
        return menu

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