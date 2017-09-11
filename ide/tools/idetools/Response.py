import abjad
from ide.tools.idetools.Path import Path


class Response(abjad.AbjadObject):
    r'''Response.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_payload',
        '_string',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        payload=None,
        string=None,
        ):
        assert isinstance(payload, (str, list, Path, type(None)))
        self._payload = payload
        assert isinstance(string, (str, type(None))), repr(string)
        self._string = string

    ### PUBLIC PROPERTIES ###

    @property
    def payload(self):
        r'''Gets payload.

        Returns object or none.
        '''
        return self._payload

    @property
    def string(self):
        r'''Gets string.

        Returns string.
        '''
        return self._string
