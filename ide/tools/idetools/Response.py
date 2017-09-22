import abjad
from ide.tools.idetools.Path import Path


class Response(abjad.AbjadObject):
    r'''Response.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_payload',
        '_source',
        '_string',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        payload=None,
        source=None,
        string=None,
        ):
        assert isinstance(payload, (str, list, Path, type(None)))
        self._payload = payload
        assert isinstance(source, (str, type(None))), repr(source)
        self._source = source
        assert isinstance(string, (str, type(None))), repr(string)
        self._string = string

    ### PRIVATE METHODS ###

    def _is_double_address(self):
        if (2 <= len(self.string) and
            self.string[0] in Path.address_characters and
            self.string[0] == self.string[1]):
            return True
        return False

    def _is_single_address(self):
        if (len(self.string) == 1 and
            self.string[0] in Path.address_characters):
            return True
        if (2 <= len(self.string) and
            self.string[0] in Path.address_characters and
            self.string[0] != self.string[1]):
            return True
        return False
        
    ### PUBLIC PROPERTIES ###

    @property
    def pair(self):
        r'''Gets prefix / pattern pair.

        Returns tuple.
        '''
        return self.prefix, self.pattern

    @property
    def pattern(self):
        r'''Gets pattern.

        Returns string or none.
        '''
        if self._is_single_address():
            return self.string[1:]
        if self._is_double_address():
            return self.string[2:]
        return self.string

    @property
    def payload(self):
        r'''Gets payload.

        Returns object or none.
        '''
        return self._payload

    @property
    def prefix(self):
        r'''Gets prefix.

        Returns string.
        '''
        if self._is_single_address():
            return self.string[:1]
        if self._is_double_address():
            return self.string[:2]
        return ''

    @property
    def source(self):
        r'''Gets source.

        Returns string or none.
        '''
        return self._source

    @property
    def string(self):
        r'''Gets string.

        Returns string.
        '''
        return self._string

    ### PUBLIC METHODS ###

    def is_shell(self):
        r'''Is true when response is shell command.

        Returns true or false.
        '''
        if (self.string and
            self.string.startswith('!') and
            not self.string == '!!'):
            return True
        return False
