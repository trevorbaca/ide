import abjad


class Response(abjad.AbjadObject):
    r'''Response.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_known',
        '_payload',
        '_string',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        known=None,
        payload=None,
        string=None,
        ):
        import ide
        self._known = known
        if not known:
            assert not payload, repr(payload)
        assert isinstance(payload, (str, list, ide.Path, type(None)))
        self._payload = payload
        assert isinstance(string, str), repr(string)
        self._string = string

    ### PUBLIC PROPERTIES ###

    @property
    def known(self):
        r'''Is true when response is known.

        Returns true, false or none.
        '''
        return self._known

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
