import abjad


class MenuEntry(abjad.AbjadObject):
    r'''Menu entry.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_command',
        '_display',
        '_number',
        '_value',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        command=None,
        display=None,
        number=None,
        value=None,
        ):
        self._command = command
        self._display = abjad.String(display)
        self._number = number
        self._value = value

    ### SPECIAL METHODS ###

    def __lt__(self, argument):
        r'''Is true when `argument` is a menu entry with display greater than
        that of this menu entry. Otherwise false.

        Returns true or false.
        '''
        if not isinstance(argument, type(self)):
            raise TypeError(argument)
        return self.display < argument.display

    ### PUBLIC PROPERTIES ###

    @property
    def command(self):
        r'''Gets name of command section.

        Returns string or none.
        '''
        return self._command

    @property
    def display(self):
        r'''Gets display.

        Returns string.
        '''
        return self._display

    @property
    def number(self):
        r'''Gets number.

        Returns positive integer or none.
        '''
        return self._number

    @property
    def value(self):
        r'''Gets value.

        Returns value.
        '''
        return self._value

    ### PUBLIC METHODS ###

    def make_line(self, left_margin_width):
        r'''Makes line.

        Returns string.
        '''
        if self.number is not None:
            line = str(self.number) + ': '
            line = line.rjust(left_margin_width)
        else:
            line = left_margin_width * ' '
        line += self.display
        return line
