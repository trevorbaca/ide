# -*- coding: utf-8 -*-
from abjad.tools.abctools.ContextManager import ContextManager


class ControllerContext(ContextManager):
    r'''AbjadIDE context manager.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_clear_terminal',
        '_controller',
        '_directory_name',
        '_is_in_confirmation_environment',
        '_session',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        clear_terminal=False,
        controller=None,
        directory_name=None,
        is_in_confirmation_environment=False,
        ):
        self._clear_terminal = clear_terminal
        self._controller = controller
        self._directory_name = directory_name
        self._is_in_confirmation_environment = is_in_confirmation_environment
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

    def __exit__(self, exg_type, exc_value, trackeback):
        r'''Exits controller stack context manager.

        Returns none.
        '''
        self._session._is_in_confirmation_environment = False
        if self._clear_terminal:
            self._session._pending_redraw = True

    def __repr__(self):
        r'''Gets interpreter representation of context manager.

        Returns string.
        '''
        return '<{}({!r})>'.format(type(self).__name__, self._controller)