import abjad
import types
from ide.tools.idetools.Configuration import Configuration
from ide.tools.idetools.MenuEntry import MenuEntry
from ide.tools.idetools.Path import Path


class MenuSection(abjad.AbjadObject):
    r'''Menu section.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_command',
        '_entries',
        '_help',
        '_force_single_column',
        '_multiple',
        '_secondary',
        )

    configuration = Configuration()

    ### INITIALIZER ###

    def __init__(
        self,
        command=None,
        entries=None,
        force_single_column=None,
        help=None,
        multiple=None,
        secondary=None,
        ):
        abjad.AbjadObject.__init__(self)
        if command and multiple:
            raise Exception('command sections can not select multiple.')
        self._command = command
        self._entries = []
        self._force_single_column = force_single_column
        self._help = help
        self._multiple = multiple
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
    def help(self):
        r'''Gets help section.

        Returns `'command'`, `'navigation'` or none.
        '''
        return self._help

    @property
    def multiple(self):
        r'''Is true when section is multiple. Otherwise false.

        Returns true or false.
        '''
        return self._multiple

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
            displays = [_.display for _ in self]
            display = Path.smart_match(displays, string)
            if display is not None:
                entry = self[displays.index(display)]
                return entry

    def range_string_to_numbers(self, range_string):
        r'''Changes `range_string` to numbers.

        Returns list.
        '''
        range_string = range_string.strip()
        assert self.entries
        numbers = []
        if ',' in range_string:
            range_parts = range_string.split(',')
        else:
            range_parts = [range_string]
        for range_part in range_parts:
            range_part = range_part.strip()
            entry = self.match(range_part)
            if entry is not None:
                numbers.append(entry.number)
                continue
            if range_part == 'all':
                numbers.extend(range(1, len(self.entries) + 1))
            elif '-' in range_part:
                start, stop = range_part.split('-')
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
                entry = self.match(range_part)
                if entry is None:
                    break
                numbers.append(entry.number)
        return numbers
