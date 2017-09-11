import abjad


class Interaction(abjad.ContextManager):
    r'''Interaction context manager.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_io',
        )

    ### INITIALIZER ###

    def __init__(self, io=None):
        self._io = io

    ### SPECIAL METHODS ###

    def __enter__(self):
        r'''Enters context manager.
        '''
        pass

    def __exit__(self, exc_type, exc_value, traceback):
        r'''Exits context manager.
        '''
        self.io.display('')

    def __repr__(self):
        r'''Gets interpreter representation of context manager.

        Returns string.
        '''
        return f'<{type(self).__name__}()>'

    ### PUBLIC PROPERTIES ###

    @property
    def io(self):
        r'''Gets IO manager.
        '''
        return self._io
