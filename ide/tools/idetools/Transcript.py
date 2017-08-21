import abjad
import datetime
import time
from ide.tools.idetools.AbjadIDEConfiguration import AbjadIDEConfiguration
configuration = AbjadIDEConfiguration()


class Transcript(abjad.AbjadObject):
    r'''Transcript.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_entries',
        '_start_time',
        )

    ### INITIALIZER ###

    def __init__(self):
        self._entries = []
        current_time = datetime.datetime.fromtimestamp(time.time())
        self._start_time = current_time

    ### SPECIAL METHODS ###

    def __getitem__(self, argument):
        r'''Gets transcript entry matching `argument`.

        Returns transcript entry.
        '''
        return self.entries.__getitem__(argument)

    ### PRIVATE METHODS ###

    def _append_entry(self, lines, is_menu=False):
        from ide.tools import idetools
        entry = idetools.TranscriptEntry(lines, is_menu=is_menu)
        self.entries.append(entry)

    def _write(self, transcripts_directory=None):
        if transcripts_directory is None:
            transcripts_directory = \
                configuration.abjad_ide_transcripts_directory
        start_time = self.start_time.strftime('%Y-%m-%d-%H-%M-%S')
        file_name = 'session-{}.txt'.format(start_time)
        file_path = transcripts_directory / file_name
        with file_path.open('w') as file_pointer:
            for entry in self.entries:
                line = entry._format()
                file_pointer.write(line)
                file_pointer.write('\n\n')

    ### PUBLIC PROPERTIES ###

    @property
    def contents(self):
        r'''Gets all transcript contents joined together as a single string.

        Returns string.
        '''
        return '\n'.join(self.lines)

    @property
    def entries(self):
        r'''Gets transcript entries.

        Returns list of transcript entries.
        '''
        return self._entries

    @property
    def lines(self):
        r'''Gets all transcript lines.

        Returns list.
        '''
        lines = []
        for entry in self:
            lines.extend(entry.lines)
        return lines

    @property
    def start_time(self):
        r'''Gets transcript start time.

        Returns date / time.
        '''
        return self._start_time

    @property
    def titles(self):
        r'''Gets titles of system display entries in transcript.

        Returns list.
        '''
        result = [_.lines[0] for _ in self if _.is_menu]
        return result
