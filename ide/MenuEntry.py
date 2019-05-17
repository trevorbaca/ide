import abjad
import typing


class MenuEntry(object):
    """
    Menu entry.
    """

    ### CLASS VARIABLES ###

    __slots__ = ("_command", "_display", "_number", "_value")

    ### INITIALIZER ###

    def __init__(
        self,
        command: str = None,
        display: str = None,
        number: int = None,
        value: str = None,
    ) -> None:
        self._command = command
        self._display = abjad.String(display)
        self._number = number
        self._value = value

    ### SPECIAL METHODS ###

    def __lt__(self, argument) -> bool:
        """
        Is true when `argument` is a menu entry with display greater than
        that of this menu entry.
        """
        if not isinstance(argument, type(self)):
            raise TypeError(argument)
        return (self.display or "") < (argument.display or "")

    ### PUBLIC PROPERTIES ###

    @property
    def command(self) -> typing.Optional[str]:
        """
        Gets name of command section.
        """
        return self._command

    @property
    def display(self) -> typing.Optional[str]:
        """
        Gets display.
        """
        return self._display

    @property
    def number(self) -> typing.Optional[int]:
        """
        Gets number.
        """
        return self._number

    @property
    def value(self) -> typing.Optional[str]:
        """
        Gets value.
        """
        return self._value

    ### PUBLIC METHODS ###

    def make_line(self, left_margin_width: int) -> str:
        """
        Makes line.
        """
        if self.number is not None:
            line = str(self.number) + ": "
            line = line.rjust(left_margin_width)
        else:
            line = left_margin_width * " "
        line += self.display or ""
        return line
