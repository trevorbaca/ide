# -*- encoding: utf -*-
from abjad.tools import stringtools


class Controller(object):
    r'''Controller.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_configuration',
        '_io_manager',
        '_session',
        '_transcript',
        )

    ### INTIIALIZER ###

    def __init__(self, session=None):
        from ide.tools import idetools
        self._configuration = idetools.AbjadIDEConfiguration()
        self._session = session or idetools.Session()
        self._io_manager = idetools.IOManager(
            client=self,
            session=self._session,
            )
        self._transcript = self._session.transcript

    ### SPECIAL METHODS ###

    def __repr__(self):
        r'''Gets interpreter representation of controller.

        Returns string.
        '''
        return '{}()'.format(type(self).__name__)

    ### PRIVATE PROPERTIES ###

    @property
    def _command_to_method(self):
        result = {
            'b': self.go_back,
            'q': self.quit_abjad_ide,
            's': self.go_to_current_score,
            'h': self.go_to_all_score_directories,
            }
        return result

    @property
    def _spaced_class_name(self):
        return stringtools.to_space_delimited_lowercase(type(self).__name__)

    ### PUBLIC METHODS ###

    def go_back(self):
        r'''Goes back.

        Returns none.
        '''
        self._session._is_backtracking_locally = True
        self._session._display_available_commands = False

    def go_to_all_score_directories(self):
        r'''Goes to all scores.

        Returns none.
        '''
        self._session._is_navigating_home = False
        self._session._is_navigating_to_scores = True
        self._session._display_available_commands = False

    def go_to_current_score(self):
        r'''Goes to current score.

        Returns none.
        '''
        if self._session.is_in_score:
            self._session._is_backtracking_to_score = True
            self._session._display_available_commands = False

    def quit_abjad_ide(self):
        r'''Quits Abjad IDE.

        Returns none.
        '''
        self._session._is_quitting = True
        self._session._display_available_commands = False