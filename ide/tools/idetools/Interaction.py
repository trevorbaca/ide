# -*- coding: utf-8 -*-
import abjad


class Interaction(abjad.abctools.ContextManager):
    r'''Interaction context manager.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_io_manager',
        )

    ### INITIALIZER ###

    def __init__(self, io_manager=None):
        self._io_manager = io_manager

    ### SPECIAL METHODS ###

    def __enter__(self):
        r'''Enters context manager.
        '''
        pass

    def __exit__(self, exc_type, exc_value, traceback):
        r'''Exits context manager.
        '''
        self._io_manager._display('')

    def __repr__(self):
        r'''Gets interpreter representation of context manager.

        Returns string.
        '''
        return '<{}()>'.format(type(self).__name__)

    ### PUBLIC PROPERTIES ###

    @property
    def io_manager(self):
        r'''Gets io manager.
        '''
        return self._io_manager
