# -*- encoding: utf-8 -*-
import os
import shutil
import sys
from abjad.tools import stringtools
from abjad.tools import systemtools
from ide.tools.idetools.Controller import Controller


class AbjadIDE(Controller):
    r'''Abjad IDE.

    ..  container:: example

        ::

            >>> ide.tools.idetools.AbjadIDE(is_test=True)
            AbjadIDE()

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        )

    ### INITIALIZER ###

    def __init__(self, session=None, is_test=False):
        from ide.tools import idetools
        if session is None:
            session = idetools.Session()
            session._is_test = is_test
        superclass = super(AbjadIDE, self)
        superclass.__init__(session=session)
        self._session._abjad_ide = self
        self._score_package_wrangler._supply_missing_views_files()

    ### PRIVATE PROPERTIES ###

    @property
    def _breadcrumb(self):
        if not self._session.is_in_score:
            return 'Abjad IDE'

    @property
    @systemtools.Memoize
    def _build_file_wrangler(self):
        from ide.tools import idetools
        wrangler = idetools.Wrangler(session=self._session)
        wrangler._asset_identifier = 'file'
        wrangler._basic_breadcrumb = 'build'
        commands = []
        commands.append(wrangler.collect_segment_lilypond_files)
        commands.append(wrangler.generate_back_cover_source)
        commands.append(wrangler.generate_front_cover_source)
        commands.append(wrangler.generate_music_source)
        commands.append(wrangler.generate_preface_source)
        commands.append(wrangler.generate_score_source)
        commands.append(wrangler.interpret_back_cover)
        commands.append(wrangler.interpret_front_cover)
        commands.append(wrangler.interpret_music)
        commands.append(wrangler.interpret_preface)
        commands.append(wrangler.interpret_score)
        commands.append(wrangler.push_score_pdf_to_distribution_directory)
        wrangler._controller_commands = commands
        wrangler._directory_entry_predicate = \
            wrangler._is_valid_file_directory_entry
        wrangler._directory_name = 'build'
        wrangler._file_name_predicate = stringtools.is_dash_case
        wrangler._force_dash_case_file_name = True
        return wrangler

    @property
    @systemtools.Memoize
    def _distribution_file_wrangler(self):
        from ide.tools import idetools
        wrangler = idetools.Wrangler(session=self._session)
        wrangler._asset_identifier = 'file'
        wrangler._basic_breadcrumb = 'distribution'
        wrangler._directory_entry_predicate = \
            wrangler._is_valid_file_directory_entry
        wrangler._directory_name = 'distribution'
        wrangler._file_name_predicate = stringtools.is_dash_case
        wrangler._force_dash_case_file_name = True
        return wrangler

    @property
    @systemtools.Memoize
    def _etc_file_wrangler(self):
        from ide.tools import idetools
        wrangler = idetools.Wrangler(session=self._session)
        wrangler._asset_identifier = 'file'
        wrangler._basic_breadcrumb = 'etc'
        wrangler._directory_entry_predicate = \
            wrangler._is_valid_file_directory_entry
        wrangler._directory_name = 'etc'
        wrangler._file_name_predicate = stringtools.is_dash_case
        wrangler._force_dash_case_file_name = True
        return wrangler

    @property
    @systemtools.Memoize
    def _maker_file_wrangler(self):
        from ide.tools import idetools
        wrangler = idetools.Wrangler(session=self._session)
        wrangler._asset_identifier = 'maker'
        wrangler._basic_breadcrumb = 'makers'
        wrangler._directory_entry_predicate = \
            wrangler._is_valid_file_directory_entry
        wrangler._directory_name = 'makers'
        wrangler._file_extension = '.py'
        wrangler._file_name_predicate = stringtools.is_upper_camel_case
        wrangler._force_lowercase_file_name = False
        return wrangler

    @property
    @systemtools.Memoize
    def _material_package_wrangler(self):
        from ide.tools import idetools
        wrangler = idetools.Wrangler(session=self._session)
        wrangler._asset_identifier = 'material package'
        wrangler._basic_breadcrumb = 'materials'
        commands = []
        commands.append(wrangler.check_every_definition_py)
        commands.append(wrangler.edit_every_definition_py)
        commands.append(wrangler.interpret_every_illustration_ly)
        commands.append(wrangler.open_every_illustration_pdf)
        commands.append(wrangler.go_to_next_package)
        commands.append(wrangler.go_to_previous_package)
        wrangler._controller_commands = commands
        wrangler._directory_entry_predicate = \
            wrangler._is_valid_package_directory_entry
        wrangler._directory_name = 'materials'
        return wrangler

    @property
    @systemtools.Memoize
    def _score_package_wrangler(self):
        from ide.tools import idetools
        wrangler = idetools.Wrangler(session=self._session)
        wrangler._asset_identifier = 'score package'
        wrangler._basic_breadcrumb = 'scores'
        wrangler._copy_target_directory = \
            wrangler._configuration.composer_scores_directory
        wrangler._directory_entry_predicate = \
            wrangler._is_valid_package_directory_entry
        commands = []
        commands.append(wrangler.check_every_package)
        commands.append(wrangler.add_every_asset)
        commands.append(wrangler.commit_every_asset)
        commands.append(wrangler.revert_every_asset)
        commands.append(wrangler.display_every_asset_status)
        commands.append(wrangler.update_every_asset)
        commands.append(wrangler.open_every_score_pdf)
        commands.append(wrangler.go_to_all_build_directories)
        commands.append(wrangler.go_to_all_distribution_directories)
        commands.append(wrangler.go_to_all_etc_directories)
        commands.append(wrangler.go_to_all_makers_directories)
        commands.append(wrangler.go_to_all_materials_directories)
        commands.append(wrangler.go_to_all_segments_directories)
        commands.append(wrangler.go_to_all_stylesheets_directories)
        wrangler._controller_commands = commands
        wrangler._group_asset_section_by_annotation = False
        wrangler._hide_breadcrumb_while_in_score = True
        wrangler._only_example_scores_during_test = True
        wrangler._sort_by_annotation = False
        return wrangler

    @property
    @systemtools.Memoize
    def _segment_package_wrangler(self):
        from ide.tools import idetools
        wrangler = idetools.Wrangler(session=self._session)
        wrangler._asset_identifier = 'segment package'
        wrangler._basic_breadcrumb = 'segments'
        commands = []
        commands.append(wrangler.check_every_definition_py)
        commands.append(wrangler.edit_every_definition_py)
        commands.append(wrangler.illustrate_every_definition_py)
        commands.append(wrangler.interpret_every_illustration_ly)
        commands.append(wrangler.open_every_illustration_pdf)
        commands.append(wrangler.go_to_next_package)
        commands.append(wrangler.go_to_previous_package)
        wrangler._controller_commands = commands
        wrangler._directory_entry_predicate = \
            wrangler._is_valid_package_directory_entry
        wrangler._directory_name = 'segments'
        return wrangler

    @property
    @systemtools.Memoize
    def _stylesheet_wrangler(self):
        from ide.tools import idetools
        wrangler = idetools.Wrangler(session=self._session)
        wrangler._asset_identifier = 'stylesheet'
        wrangler._basic_breadcrumb = 'stylesheets'
        wrangler._directory_entry_predicate = \
            wrangler._is_valid_file_directory_entry
        wrangler._directory_name = 'stylesheets'
        wrangler._file_extension = '.ily'
        wrangler._file_name_predicate = stringtools.is_dash_case
        wrangler._force_dash_case_file_name = True
        return wrangler

    @property
    def _wranglers(self):
        return (
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

    def _run(self, input_=None):
        from ide.tools import idetools
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
            self._configuration.abjad_ide_configuration_directory,
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
                    self._configuration.abjad_ide_boilerplate_directory,
                    '__views_metadata__.py',
                    )
                shutil.copyfile(empty_views, wrangler_views)
            while True:
                result = self._score_package_wrangler._get_sibling_score_path()
                if not result:
                    result = self._session.wrangler_navigation_directive
                if result:
                    self._score_package_wrangler._handle_input(result)
                else:
                    self._score_package_wrangler._run()
                self._session._is_backtracking_to_score = False
                self._session._is_navigating_to_scores = False
                if self._session.is_quitting:
                    if not self._transcript[-1][-1] == '':
                        self._io_manager._display('')
                    if self._session._clear_terminal_after_quit:
                        self._io_manager.clear_terminal()
                    return

    ### PUBLIC METHODS ###

    @staticmethod
    def start_abjad_ide():
        r'''Starts Abjad IDE.

        Returns none.
        '''
        import ide
        abjad_ide = ide.tools.idetools.AbjadIDE(is_test=False)
        input_ = ' '.join(sys.argv[1:])
        abjad_ide._run(input_=input_)