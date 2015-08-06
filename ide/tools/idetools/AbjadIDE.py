# -*- encoding: utf-8 -*-
import os
import shutil
import sys
from abjad.tools import systemtools
from ide.tools.idetools.AbjadIDEConfiguration import AbjadIDEConfiguration
configuration = AbjadIDEConfiguration()


class AbjadIDE(object):
    r'''Abjad IDE.

    ..  container:: example

        ::

            >>> ide.tools.idetools.AbjadIDE(is_test=True)
            AbjadIDE()

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_session',
        )

    ### INITIALIZER ###

    def __init__(self, session=None, is_test=False):
        from ide.tools import idetools
        if session is None:
            session = idetools.Session()
            session._is_test = is_test
        self._session = session
        self._session._abjad_ide = self
        for wrangler in self._wranglers:
            wrangler._supply_missing_view_file(
                wrangler._io_manager,
                wrangler._directory_name,
                )
        self._score_package_wrangler._supply_views_metadata_py(
            self._session._io_manager)

    ### SPECIAL METHODS ###

    def __repr__(self):
        r'''Gets interpreter representation of Abjad IDE.

        Returns string.
        '''
        return '{}()'.format(type(self).__name__)

    ### PRIVATE PROPERTIES ###

    @property
    def _breadcrumb(self):
        if not self._session.is_in_score:
            return 'Abjad IDE'

    @property
    def _build_file_wrangler(self):
        from ide.tools import idetools
        wrangler = idetools.Wrangler(session=self._session)
        wrangler._configure_as_build_file_wrangler()
        return wrangler

    @property
    def _distribution_file_wrangler(self):
        from ide.tools import idetools
        wrangler = idetools.Wrangler(session=self._session)
        wrangler._configure_as_distribution_file_wrangler()
        return wrangler

    @property
    def _etc_file_wrangler(self):
        from ide.tools import idetools
        wrangler = idetools.Wrangler(session=self._session)
        wrangler._configure_as_etc_file_wrangler()
        return wrangler

    @property
    def _maker_file_wrangler(self):
        from ide.tools import idetools
        wrangler = idetools.Wrangler(session=self._session)
        wrangler._configure_as_maker_file_wrangler()
        return wrangler

    @property
    def _material_package_wrangler(self):
        from ide.tools import idetools
        wrangler = idetools.Wrangler(session=self._session)
        wrangler._configure_as_material_package_wrangler()
        return wrangler

    @property
    def _score_package_wrangler(self):
        from ide.tools import idetools
        wrangler = idetools.Wrangler(session=self._session)
        wrangler._configure_as_score_package_wrangler()
        return wrangler

    @property
    def _segment_package_wrangler(self):
        from ide.tools import idetools
        wrangler = idetools.Wrangler(session=self._session)
        wrangler._configure_as_segment_package_wrangler()
        return wrangler

    @property
    def _stylesheet_wrangler(self):
        from ide.tools import idetools
        wrangler = idetools.Wrangler(session=self._session)
        wrangler._configure_as_stylesheet_wrangler()
        return wrangler

    @property
    def _test_file_wrangler(self):
        from ide.tools import idetools
        wrangler = idetools.Wrangler(session=self._session)
        wrangler._configure_as_test_file_wrangler()
        return wrangler

    # TODO: derive introspectively
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
            self._test_file_wrangler,
            )

    ### PRIVATE METHODS ###

    def _run(self, input_=None):
        from ide.tools import idetools
        self._session._reinitialize()
        type(self).__init__(self, session=self._session)
        if input_:
            self._session._pending_input = input_
        controller = self._session._io_manager._controller(
            controller=self,
            consume_local_backtrack=True,
            on_exit_callbacks=(self._session._clean_up,)
            )
        path = configuration.abjad_ide_directory
        directory_change = systemtools.TemporaryDirectoryChange(path)
        state = systemtools.NullContextManager()
        wrangler_views = os.path.join(
            configuration.abjad_ide_wrangler_views_directory,
            '__metadata__.py',
            )
        if self._session.is_test:
            paths_to_keep = []
            paths_to_keep.append(wrangler_views)
            state = systemtools.FilesystemState(keep=paths_to_keep)
        interaction = self._session._io_manager._make_interaction(
            self._session,
            task=False,
            )
        with controller, directory_change, state, interaction:
            self._session._pending_redraw = True
            if self._session.is_test:
                empty_views = os.path.join(
                    configuration.abjad_ide_boilerplate_directory,
                    '__views_metadata__.py',
                    )
                shutil.copyfile(empty_views, wrangler_views)
            while True:
                result = self._score_package_wrangler._get_sibling_score_path()
                result = result or self._session.navigation_command_name
                if result:
                    self._score_package_wrangler._handle_input(result)
                else:
                    self._score_package_wrangler._run()
                self._session._is_backtracking_to_score = False
                self._session._is_navigating_to_scores = False
                if self._session.is_quitting:
                    if not self._session._transcript[-1][-1] == '':
                        self._session._io_manager._display('')
                    if self._session._clear_terminal_after_quit:
                        self._session._io_manager.clear_terminal()
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