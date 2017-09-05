import abjad


class Transcript(abjad.AbjadObject):
    r'''Transcript.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_blocks',
        '_lines',
        '_titles',
        )

    ### INITIALIZER ###

    def __init__(self):
        self._blocks = []
        self._lines = []
        self._titles = []

    ### SPECIAL METHODS ###

    def __contains__(self, argument):
        r'''Is true when `argument` appears in transcript.

        Returns true or false.
        '''
        return argument in '\n'.join(self.lines)

    ### PRIVATE METHODS ###

    def _append_block(self, block, is_menu=False):
        self._lines.extend(block)
        self.blocks.append(block)
        if is_menu:
            self._titles.append(block[0])

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
    def titles(self):
        r'''Gets titles.

        Returns list.
        '''
        return self._titles
