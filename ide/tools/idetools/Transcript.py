import abjad


class Transcript(abjad.AbjadObject):
    r'''Transcript.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_blocks',
        '_lines',
        '_menus',
        '_titles',
        )

    ### INITIALIZER ###

    def __init__(self):
        self._blocks = []
        self._lines = []
        self._menus = []
        self._titles = []

    ### SPECIAL METHODS ###

    def __contains__(self, argument):
        r'''Is true when `argument` appears in transcript.

        Returns true or false.
        '''
        return argument in '\n'.join(self.lines)

    ### PUBLIC PROPERTIES ###

    @property
    def blocks(self):
        r'''Gets blocks.

        Returns list.
        '''
        return self._blocks

    @property
    def lines(self):
        r'''Gets lines.

        Returns list.
        '''
        return self._lines

    @property
    def menus(self):
        r'''Gets menus.

        Returns list.
        '''
        return self._menus

    @property
    def titles(self):
        r'''Gets titles.

        Returns list.
        '''
        return self._titles

    ### PUBLIC METHODS ###

    def append(self, block, is_menu=False):
        r'''Appends `block`.

        Returns none.
        '''
        self._lines.extend(block)
        self._blocks.append(block)
        if is_menu:
            self._menus.append(block)
            self._titles.append(block[0])

    def trim(self):
        r'''Trims transcript.

        Returns none.
        '''
        for line in reversed(self.lines):
            if line == '':
                self.lines.pop(-1)
            else:
                break
        self.lines.append('')
