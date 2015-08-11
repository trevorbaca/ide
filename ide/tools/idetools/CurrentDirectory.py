# -*- encoding: utf-8 -*-
from abjad.tools.abctools.ContextManager import ContextManager


class CurrentDirectory(ContextManager):
    r'''Current directory context manager.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_current_directory',
        )

    ### INITIALIZER ###

    def __init__(
        self, 
        current_directory=None,
        session=None,
        ):
        assert current_directory is not None
        self._current_directory = current_directory
        assert session is not None
        self._session = session

    ### SPECIAL METHODS ###

    def __enter__(self):
        r'''Enters current directory manager.

        Returns none.
        '''
        self.session._manifest_current_directory = self.current_directory

    def __exit__(self, exg_type, exc_value, trackeback):
        r'''Exits current directory manager.

        Returns none.
        '''
        self.session._manifest_current_directory = None

    ### PUBLIC PROPERTIES ###

    @property
    def current_directory(self):
        r'''Gets current directory.

        Returns string.
        '''
        return self._current_directory

    @property
    def session(self):
        r'''Gets session.

        Returns session.
        '''
        return self._session