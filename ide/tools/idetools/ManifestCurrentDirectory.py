# -*- encoding: utf-8 -*-
import os
from abjad.tools.abctools.ContextManager import ContextManager


class ManifestCurrentDirectory(ContextManager):
    r'''Current directory context manager.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_manifest_current_directory',
        '_old_directory',
        '_session',
        )

    ### INITIALIZER ###

    def __init__(
        self, 
        manifest_current_directory=None,
        session=None,
        ):
        assert manifest_current_directory is not None
        assert os.path.sep in manifest_current_directory
        self._manifest_current_directory = manifest_current_directory
        assert session is not None
        self._session = session

    ### SPECIAL METHODS ###

    def __enter__(self):
        r'''Enters manifest current directory manager.

        Returns none.
        '''
        self._old_directory = self.session.manifest_current_directory
        self.session._manifest_current_directory = \
            self.manifest_current_directory

    def __exit__(self, exg_type, exc_value, trackeback):
        r'''Exits manifest current directory manager.

        Returns none.
        '''
        self.session._manifest_current_directory = self._old_directory

    ### PUBLIC PROPERTIES ###

    @property
    def manifest_current_directory(self):
        r'''Gets manifest current directory.

        Returns string.
        '''
        return self._manifest_current_directory

    @property
    def session(self):
        r'''Gets session.

        Returns session.
        '''
        return self._session