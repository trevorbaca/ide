# -*- encoding: utf-8 -*-
import os
import shutil
import sys
from abjad.tools import systemtools
from ide.tools.idetools.AbjadIDEConfiguration import AbjadIDEConfiguration
from ide.tools.idetools.Controller import Controller
configuration = AbjadIDEConfiguration()


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
        session._abjad_ide = self
        superclass = super(AbjadIDE, self)
        superclass.__init__(session=session)
        for directory_name in self._known_directory_names:
            self._supply_global_views_file(directory_name)
        self._supply_global_metadata_py()

    ### SPECIAL METHODS ###

    def __repr__(self):
        r'''Gets interpreter representation of Abjad IDE.

        Returns string.
        '''
        return '{}()'.format(type(self).__name__)

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
        views = os.path.join(
            configuration.abjad_ide_views_directory,
            '__metadata__.py',
            )
        if self._session.is_test:
            paths_to_keep = []
            paths_to_keep.append(views)
            state = systemtools.FilesystemState(keep=paths_to_keep)
        interaction = self._session._io_manager._make_interaction(task=False)
        with controller, directory_change, state, interaction:
            self._session._pending_redraw = True
            if self._session.is_test:
                empty_views = os.path.join(
                    configuration.abjad_ide_boilerplate_directory,
                    '__views_metadata__.py',
                    )
                shutil.copyfile(empty_views, views)
            score_package_wrangler = self._initialize_wrangler('scores')
            while True:
                result = score_package_wrangler._get_sibling_score_path()
                if result is None:
                    result = \
                        self._directory_name_to_navigation_command_name.get(
                        self._session.navigation_target)
                if result:
                    score_package_wrangler._handle_input(result)
                else:
                    score_package_wrangler._run_wrangler()
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