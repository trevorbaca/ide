import abjad
from .Configuration import Configuration
from .MenuEntry import MenuEntry


class MenuSection(abjad.AbjadObject):
    r'''Menu section.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_command',
        '_entries',
        '_force_single_column',
        '_secondary',
        )

    configuration = Configuration()

    ### INITIALIZER ###

    def __init__(
        self,
        command=None,
        entries=None,
        force_single_column=None,
        secondary=None,
        ):
        abjad.AbjadObject.__init__(self)
        self._command = command
        self._entries = []
        self._force_single_column = force_single_column
        self._secondary = secondary
        self._initialize_entries(entries)

    ### SPECIAL METHODS ###

    def __getitem__(self, argument):
        r'''Gets entry indexed by `argument`.

        Returns entry.
        '''
        return self.entries.__getitem__(argument)

    ### PRIVATE METHODS ###

    def _initialize_entries(self, entries):
        for i, entry in enumerate(entries):
            if not self.command and not self.secondary:
                number = i + 1
            else:
                number = None
            if isinstance(entry, MenuEntry):
                display = entry.display
                value = entry.value
            elif isinstance(entry, tuple):
                assert len(entry) == 2, repr(entry)
                display = entry[0]
                value = entry[1]
            else:
                raise TypeError(entry)
            entry = MenuEntry(
                display=display,
                command=self.command,
                number=number,
                value=value,
                )
            self.entries.append(entry)
        if self.command:
            self.entries.sort()

    ### PUBLIC PROPERTIES ###

    @property
    def command(self):
        r'''Is true when section lists commands. Otherwise false.

        Returns true or false.
        '''
        return self._command

    @property
    def entries(self):
        r'''Gets entries.

        Returns list.
        '''
        return self._entries

    @property
    def force_single_column(self):
        r'''Is true when section forces single column.

        Returns true or false.
        '''
        return self._force_single_column

    @property
    def secondary(self):
        r'''Is true when section lists secondary assets. Otherwise false.

        Returns true or false.
        '''
        return self._secondary

    ### PUBLIC METHODS ###

    def make_lines(self, left_margin_width):
        r'''Makes lines.
        
        Returns list.
        '''
        left_margin_width = left_margin_width or self.left_margin_width
        lines = [_.make_line(left_margin_width) for _ in self]
        if lines:
            lines.append('')
        return lines

    def match(self, string):
        r'''Gets entry that matches `string`.

        Returns entry or none.
        '''
        if self.command:
            for entry in self:
                if entry.value == string:
                    return entry
        elif abjad.mathtools.is_integer_equivalent(string):
            for entry in self:
                if str(entry.number) == string:
                    return entry
        else:
            strings = [_.display for _ in self]
            for i in abjad.String.match_strings(strings, string):
                return self[i]

    def range_string_to_numbers(self, string):
        r'''Changes range `string` to numbers.

        Returns list.
        '''
        string = string.strip()
        assert self.entries
        if not self.entries[0].number:
            return
        numbers = []
        if ',' in string:
            parts = string.split(',')
        else:
            parts = [string]
        for part in parts:
            part = part.strip()
            entry = self.match(part)
            if entry is not None:
                numbers.append(entry.number)
                continue
            if part == 'all':
                numbers.extend(range(1, len(self.entries) + 1))
            elif part.count('-') == 1:
                start, stop = part.split('-')
                start = start.strip()
                stop = stop.strip()
                entry = self.match(start)
                if entry is not None:
                    start = entry.number
                else:
                    start = None
                entry = self.match(stop)
                if entry is not None:
                    stop = entry.number
                else:
                    stop = None
                if start is None or stop is None:
                    break
                if start <= stop:
                    new_numbers = range(start, stop + 1)
                    numbers.extend(new_numbers)
                else:
                    new_numbers = range(start, stop - 1, -1)
                    numbers.extend(new_numbers)
            else:
                entry = self.match(part)
                if entry is None:
                    break
                numbers.append(entry.number)
        return numbers
