# -*- encoding: utf -*-
import inspect
from abjad.tools import stringtools
from ide.tools.idetools.Command import Command


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
    def _command_name_to_method(self):
        result = {}
        methods = self._get_decorated_methods()
        for method in methods:
            result[method.command_name] = method
        return result

    @property
    def _spaced_class_name(self):
        return stringtools.to_space_delimited_lowercase(type(self).__name__)

    ### PRIVATE METHODS ###

    def _get_decorated_methods(self):
        result = []
        for name in dir(self):
            if not name.startswith('_'):
                value = getattr(self, name)
                if inspect.ismethod(value):
                    if hasattr(value, 'command_name'):
                        result.append(value)
        return result

    ### PUBLIC METHODS ###

    @Command('b', 'back', 'back-home-quit', True)
    def go_back(self):
        r'''Goes back.

        Returns none.
        '''
        self._session._is_backtracking_locally = True
        self._session._display_action_commands = False
        self._session._display_navigation_commands = False

    @Command('h', 'home', 'back-home-quit', True)
    def go_to_all_score_directories(self):
        r'''Goes to all score directories.

        Returns none.
        '''
        self._session._is_navigating_home = False
        self._session._is_navigating_to_scores = True
        self._session._display_action_commands = False
        self._session._display_navigation_commands = False

    @Command('s', 'go to score', 'system', True)
    def go_to_score_directory(self):
        r'''Goes to current score.

        Returns none.
        '''
        if self._session.is_in_score:
            self._session._is_backtracking_to_score = True
            self._session._display_action_commands = False
            self._session._display_navigation_commands = False

    @Command('q', 'quit', 'back-home-quit', True)
    def quit_abjad_ide(self):
        r'''Quits Abjad IDE.

        Returns none.
        '''
        self._session._is_quitting = True
        self._session._display_action_commands = False
        self._session._display_navigation_commands = False