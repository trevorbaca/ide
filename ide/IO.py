import abjad
import os
import typing
from .Transcript import Transcript


class IO(object):
    """
    IO.

    ..  container:: example

        >>> ide.IO()
        IO()

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Classes'

    __slots__ = (
        '_pending_input',
        '_transcript',
        )

    ### SPECIAL METHODS ###

    def __repr__(self) -> str:
        """
        Gets interpreter representation.
        """
        return abjad.StorageFormatManager(self).get_repr_format()

    ### INITIALIZER ###

    def __init__(self) -> None:
        self._pending_input: typing.Optional[str] = None
        self._transcript = Transcript()

    ### PUBLIC PROPERTIES ###

    @property
    def transcript(self) -> Transcript:
        """
        Gets transcript.
        """
        return self._transcript

    ### PUBLIC METHODS ###

    def display(
        self,
        lines: typing.Union[
            str, abjad.String, typing.List[str], typing.List[abjad.String]
            ],
        indent: int = 0,
        is_menu: bool = False,
        raw: bool = False,
        ) -> None:
        """
        Displays lines.
        """
        assert isinstance(lines, (str, list)), repr(lines)
        if isinstance(lines, str):
            lines = [lines]
        if not raw:
            lines = [abjad.String(_).capitalize_start() for _ in lines]
        if indent:
            whitespace = indent * ' '
            lines = [whitespace + _ for _ in lines]
        if lines:
            self.transcript.append(lines, is_menu=is_menu)
        result = os.popen('stty size', 'r').read().split()
        if result:
            width = int(result[1])
            lines = [_[:width] for _ in lines]
        for line in lines:
            print(line)

    def get(
        self,
        prompt: str = None,
        split_input: bool = False,
        ) -> typing.Optional[str]:
        """
        Gets user input.

        Returns none when user enters lone return.

        Returns string when user types input and then hits return.
        """
        prompt = prompt or ''
        prompt = abjad.String(prompt).capitalize_start() + '> '
        if self._pending_input:
            parts = self._pending_input.split()
            pending_input = ' '.join(parts[1:])
            self._pending_input = pending_input
            string = parts[0].replace('~', ' ')
            string = string.replace('<return>', '')
            print(f'{prompt}{string}')
        else:
            string = input(prompt)
            if (string and
                not string.isspace() and
                split_input and
                not string.startswith('!')):
                parts = string.split()
                string = parts[0]
                pending_input = ' '.join(parts[1:])
                if pending_input:
                    self._pending_input = pending_input
        assert not string == '<return>'
        self.transcript.append([f'{prompt}{string}', ''])
        if string:
            return abjad.String(string)
        return None

    def pending_input(self, string: str) -> None:
        """
        Sets pending input.
        """
        self._pending_input = string
