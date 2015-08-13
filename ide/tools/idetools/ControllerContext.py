# -*- encoding: utf-8 -*-
from abjad.tools.abctools.ContextManager import ContextManager


class ControllerContext(ContextManager):
    r'''AbjadIDE context manager.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_clear_terminal',
        '_consume_local_backtrack',
        '_controller',
        '_current_score_directory',
        '_directory_name',
        '_is_in_confirmation_environment',
        '_old_current_score_directory',
        '_on_enter_callbacks',
        '_on_exit_callbacks',
        '_session',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        clear_terminal=False,
        consume_local_backtrack=False,
        controller=None,
        current_score_directory=None,
        directory_name=None,
        is_in_confirmation_environment=False,
        on_enter_callbacks=None,
        on_exit_callbacks=None,
        ):
        self._clear_terminal = clear_terminal
        self._consume_local_backtrack = consume_local_backtrack
        self._controller = controller
        self._current_score_directory = current_score_directory
        self._directory_name = directory_name
        self._is_in_confirmation_environment = is_in_confirmation_environment
        self._on_enter_callbacks = on_enter_callbacks or ()
        self._on_exit_callbacks = on_exit_callbacks or ()
        self._session = self._controller._io_manager._session

    ### SPECIAL METHODS ###

    def __enter__(self):
        r'''Enters controller stack context manager.

        Returns none.
        '''
        self._session._is_in_confirmation_environment = \
            self._is_in_confirmation_environment
        if self._clear_terminal:
            self._session._pending_redraw = True
        if self._current_score_directory is not None:
            self._old_current_score_directory = \
                self._session._current_score_directory
            self._session._current_score_directory = \
                self._current_score_directory
        for on_enter_callback in self._on_enter_callbacks:
            on_enter_callback(directory_name=self._directory_name)

    def __exit__(self, exg_type, exc_value, trackeback):
        r'''Exits controller stack context manager.

        Returns none.
        '''
        self._session._is_in_confirmation_environment = False
        if self._consume_local_backtrack:
            self._session._is_backtracking_locally = False
        if self._current_score_directory is not None:
            self._session._current_score_directory = \
                self._old_current_score_directory
        for on_exit_callback in self._on_exit_callbacks:
            on_exit_callback()
        if self._clear_terminal:
            self._session._pending_redraw = True

    def __repr__(self):
        r'''Gets interpreter representation of context manager.

        Returns string.
        '''
        return '<{}({!r})>'.format(type(self).__name__, self._controller)