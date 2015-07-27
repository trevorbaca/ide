# -*- encoding: utf-8 -*-
import os
import shutil
import sys
from abjad.tools import stringtools
from abjad.tools import systemtools
from ide.idetools.Wrangler import Wrangler


class AbjadIDE(Wrangler):
    r'''Abjad IDE.

    ..  container:: example

        ::

            >>> abjad_ide = ide.idetools.AbjadIDE(is_test=True)
            >>> abjad_ide
            AbjadIDE()


    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_simple_score_annotation',
        '_sort_by_annotation',
        )

    ### INITIALIZER ###

    def __init__(self, session=None, is_test=False):
        from ide import idetools
        if session is None:
            session = idetools.Session()
            session._is_test = is_test
        superclass = super(AbjadIDE, self)
        superclass.__init__(session=session)
        self._basic_breadcrumb = 'Abjad IDE'
        self._session._abjad_ide = self
        self._simple_score_annotation = True
        self._sort_by_annotation = True
        self._supply_missing_views_files()

    ### PRIVATE PROPERTIES ###

    @property
    def _breadcrumb(self):
        if not self._session.is_in_score:
            return self._basic_breadcrumb

    @property
    @systemtools.Memoize
    def _build_file_wrangler(self):
        from ide import idetools
        wrangler = idetools.FileWrangler(session=self._session)
        wrangler._basic_breadcrumb = 'build'
        wrangler._validator = wrangler._is_valid_file_directory_entry
        wrangler._score_storehouse_path_infix_parts = ('build',)
        wrangler._commands['bcg'] = wrangler.generate_back_cover_source
        wrangler._commands['bci'] = wrangler.interpret_back_cover
        wrangler._commands['dc'] = wrangler.collect_segment_pdfs
        wrangler._commands['fcg'] = wrangler.generate_front_cover_source
        wrangler._commands['fci'] = wrangler.interpret_front_cover
        wrangler._commands['mc'] = wrangler.collect_segment_lilypond_files
        wrangler._commands['mg'] = wrangler.generate_music_source
        wrangler._commands['mi'] = wrangler.interpret_music
        wrangler._commands['pg'] = wrangler.generate_preface_source
        wrangler._commands['pi'] = wrangler.interpret_preface
        wrangler._commands['sg'] = wrangler.generate_score_source
        wrangler._commands['si'] = wrangler.interpret_score
        wrangler._commands['sp'] = wrangler.push_score_pdf_to_distribution_directory
        commands = []
        commands.append(('collect music segment files', 'mc'))
        commands.append(('generate back-cover.tex', 'bcg'))
        commands.append(('generate front-cover.tex', 'fcg'))
        commands.append(('generate music.ly', 'mg'))
        commands.append(('generate preface.tex', 'pg'))
        commands.append(('generate score.tex', 'sg'))
        commands.append(('interpret back-cover.tex', 'bci'))
        commands.append(('interpret front-cover.tex', 'fci'))
        commands.append(('interpret music.ly', 'mi'))
        commands.append(('interpret preface.tex', 'pi'))
        commands.append(('interpret score.tex', 'si'))
        commands.append(('push score to distribution directory', 'sp'))
        wrangler._in_score_commands = commands
        return wrangler

    @property
    @systemtools.Memoize
    def _distribution_file_wrangler(self):
        from ide import idetools
        wrangler = idetools.FileWrangler(session=self._session)
        wrangler._basic_breadcrumb = 'distribution'
        wrangler._validator = wrangler._is_valid_file_directory_entry
        wrangler._score_storehouse_path_infix_parts = ('distribution',)
        return wrangler

    @property
    @systemtools.Memoize
    def _etc_file_wrangler(self):
        from ide import idetools
        wrangler = idetools.FileWrangler(session=self._session)
        wrangler._basic_breadcrumb = 'etc'
        wrangler._validator = wrangler._is_valid_file_directory_entry
        wrangler._score_storehouse_path_infix_parts = ('etc',)
        return wrangler

    @property
    @systemtools.Memoize
    def _maker_file_wrangler(self):
        from ide import idetools
        wrangler = idetools.FileWrangler(session=self._session)
        wrangler._asset_identifier = 'maker'
        wrangler._basic_breadcrumb = 'makers'
        wrangler._validator = wrangler._is_valid_file_directory_entry
        wrangler._extension = '.py'
        wrangler._file_name_predicate = stringtools.is_upper_camel_case
        wrangler._force_lowercase = False
        wrangler._new_file_contents = self._configuration.unicode_directive
        wrangler._score_storehouse_path_infix_parts = ('makers',)
        return wrangler

    @property
    @systemtools.Memoize
    def _material_package_wrangler(self):
        from ide import idetools
        wrangler = idetools.PackageWrangler(session=self._session)
        wrangler._asset_identifier = 'material package'
        wrangler._basic_breadcrumb = 'materials'
        wrangler._validator = wrangler._is_valid_package_directory_entry
        wrangler._manager_class = idetools.MaterialPackageManager
        wrangler._score_storehouse_path_infix_parts = ('materials',)
        commands = []
        commands.append(('check every definition.py files', 'dc*'))
        commands.append(('edit every definition.py files', 'de*'))
        commands.append(('interpret all illustration.ly files', 'ii*'))
        commands.append(('open all illustration.pdf files', 'io*'))
        commands.append(('next package', '>'))
        commands.append(('previous package', '<'))
        commands.append(('next score', '>>'))
        commands.append(('previous score', '<<'))
        wrangler._extra_commands = commands
        return wrangler

    @property
    @systemtools.Memoize
    def _score_package_wrangler(self):
        from ide import idetools
        wrangler = idetools.PackageWrangler(session=self._session)
        wrangler._asset_identifier = 'score package'
        wrangler._basic_breadcrumb = 'scores'
        wrangler._annotate_year = True
        wrangler._allow_depot = False
        wrangler._group_asset_section_by_annotation = False
        wrangler._has_breadcrumb_in_score = False
        wrangler._include_asset_name = False
        wrangler._manager_class = idetools.ScorePackageManager
        wrangler._mandatory_copy_target_storehouse = \
            wrangler._configuration.user_score_packages_directory
        wrangler._only_example_scores_during_test = True
        wrangler._sort_by_annotation = False
        wrangler._user_storehouse_path = \
            wrangler._configuration.user_score_packages_directory
        wrangler._validator = wrangler._is_valid_package_directory_entry
        commands = []
        commands.append(('check every score packages', 'ck*'))
        commands.append(('git add all score packages', 'add*'))
        commands.append(('git clean all score packages', 'clean*'))
        commands.append(('git commit all score packages', 'ci*'))
        commands.append(('git revert all score packages', 'revert*'))
        commands.append(('git status all score packages', 'st*'))
        commands.append(('git update all score packages', 'up*'))
        commands.append(('open all distribution score.pdf files', 'so*'))
        commands.append(('show all build files', 'uu'))
        commands.append(('show all distribution', 'dd'))
        commands.append(('show all etc files', 'ee'))
        commands.append(('show all maker files', 'kk'))
        commands.append(('show all material packages', 'mm'))
        commands.append(('show all segment packages', 'gg'))
        commands.append(('show all stylesheets', 'yy'))
        wrangler._extra_commands = commands
        commands = {
            'add*': wrangler.add_every_asset,
            'ci*': wrangler.commit_every_asset,
            'clean*': wrangler.remove_every_unadded_asset,
            'st*': wrangler.display_every_asset_status,
            'revert*': wrangler.revert_every_asset,
            'up*': wrangler.update_every_asset,
            'new': wrangler.make_score_package,
            }
        wrangler._commands = commands
        return wrangler

    @property
    @systemtools.Memoize
    def _segment_package_wrangler(self):
        from ide import idetools
        wrangler = idetools.PackageWrangler(session=self._session)
        wrangler._asset_identifier = 'segment package'
        wrangler._basic_breadcrumb = 'segments'
        wrangler._manager_class = idetools.SegmentPackageManager
        wrangler._score_storehouse_path_infix_parts = ('segments',)
        wrangler._validator = wrangler._is_valid_package_directory_entry
        commands = []
        commands.append(('check every definition.py files', 'dc*'))
        commands.append(('edit every definition.py files', 'de*'))
        commands.append(('illustrate all definition.py files', 'di*'))
        commands.append(('interpret all illustration.ly files', 'ii*'))
        commands.append(('open all illustration.pdf files', 'io*'))
        commands.append(('next package', '>'))
        commands.append(('previous package', '<'))
        commands.append(('next score', '>>'))
        commands.append(('previous score', '<<'))
        wrangler._extra_commands = commands
        return wrangler

    @property
    @systemtools.Memoize
    def _stylesheet_wrangler(self):
        from ide import idetools
        wrangler = idetools.FileWrangler(session=self._session)
        wrangler._asset_identifier = 'stylesheet'
        wrangler._basic_breadcrumb = 'stylesheets'
        wrangler._extension = '.ily'
        wrangler._score_storehouse_path_infix_parts = ('stylesheets',)
        wrangler._validator = wrangler._is_valid_file_directory_entry
        return wrangler

    @property
    def _wranglers(self):
        return (
            self,
            self._build_file_wrangler,
            self._distribution_file_wrangler,
            self._etc_file_wrangler,
            self._maker_file_wrangler,
            self._material_package_wrangler,
            self._score_package_wrangler,
            self._segment_package_wrangler,
            self._stylesheet_wrangler,
            )

    ### PRIVATE METHODS ###

    def _list_storehouse_paths(self):
        paths = []
        paths.append(self._configuration.example_score_packages_directory)
        paths.append(self._configuration.user_score_packages_directory)
        return paths

    def _list_visible_asset_paths(self):
        entries = self._make_asset_menu_entries()
        paths = [_[-1] for _ in entries]
        return paths

    def _make_main_menu(self):
        from ide import idetools
        menu = idetools.AssetController._make_main_menu(self)
        self._make_asset_menu_section(menu)
        self._make_views_menu_section(menu)
        return menu

    def _run(self, input_=None):
        from ide import idetools
        self._session._reinitialize()
        type(self).__init__(self, session=self._session)
        if input_:
            self._session._pending_input = input_
        controller = self._io_manager._controller(
            controller=self,
            consume_local_backtrack=True,
            on_exit_callbacks=(self._session._clean_up,)
            )
        path = self._configuration.abjad_ide_directory
        directory_change = systemtools.TemporaryDirectoryChange(path)
        state = systemtools.NullContextManager()
        wrangler_views = os.path.join(
            self._configuration.configuration_directory,
            'views',
            '__metadata__.py',
            )
        if self._session.is_test:
            paths_to_keep = []
            paths_to_keep.append(wrangler_views)
            state = systemtools.FilesystemState(keep=paths_to_keep)
        interaction = self._io_manager._make_interaction(task=False)
        with controller, directory_change, state, interaction:
            self._session._pending_redraw = True
            if self._session.is_test:
                empty_views = os.path.join(
                    self._configuration.boilerplate_directory,
                    '__views_metadata__.py',
                    )
                shutil.copyfile(empty_views, wrangler_views)
            while True:
                result = self._score_package_wrangler._get_sibling_score_path()
                if not result:
                    result = self._session.wrangler_navigation_directive
                if result:
                    self._score_package_wrangler._handle_input(
                        result)
                elif not self._session.is_navigating_home:
                    self._score_package_wrangler._run()
                else:
                    menu = self._make_main_menu()
                    result = menu._run()
                    if result:
                        self._handle_input(result)
                self._update_session_variables()
                if self._session.is_quitting:
                    if not self._transcript[-1][-1] == '':
                        self._io_manager._display('')
                    if self._session._clear_terminal_after_quit:
                        self._io_manager.clear_terminal()
                    return

    def _supply_missing_views_files(self):
        from ide import idetools
        if not os.path.exists(self._views_py_path):
            view_inventory = idetools.ViewInventory()
            with self._io_manager._silent():
                self._write_view_inventory(view_inventory)
        if not os.path.exists(self._metadata_py_path):
            metadata = self._get_metadata()
            with self._io_manager._silent():
                self._write_metadata_py(metadata)
        if self._session.is_test:
            with self._io_manager._silent():
                for wrangler in self._wranglers:
                    if not os.path.exists(wrangler._views_py_path):
                        wrangler.write_views_py()
        else:
            with self._io_manager._silent():
                for wrangler in self._wranglers:
                    view_inventory = idetools.ViewInventory()
                    wrangler._write_view_inventory(view_inventory)

    def _update_session_variables(self):
        self._session._is_backtracking_to_score = False
        self._session._is_navigating_to_scores = False

    ### PUBLIC METHODS ###

    @staticmethod
    def start_abjad_ide():
        r'''Starts Abjad IDE.

        Returns none.
        '''
        import ide
        abjad_ide = ide.idetools.AbjadIDE(is_test=False)
        input_ = ' '.join(sys.argv[1:])
        abjad_ide._run(input_=input_)