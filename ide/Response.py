import typing

from .Path import Path


class Response(object):
    """
    Response.

    :param payload: delivered to IDE.

    :param string: user input.
    """

    ### CLASS VARIABLES ###

    __slots__ = ("_payload", "_string")

    ### INITIALIZER ###

    def __init__(
        self, payload: typing.Union[str, list, Path] = None, string: str = None
    ) -> None:
        self._payload = payload
        self._string = string

    ### PRIVATE METHODS ###

    def _is_double_address(self):
        if (
            2 <= len(self.string)
            and self.string[0] == "@"
            and self.string[0] == self.string[1]
        ):
            return True
        return False

    def _is_single_address(self):
        if len(self.string) == 1 and self.string[0] == "@":
            return True
        if (
            2 <= len(self.string)
            and self.string[0] == "@"
            and self.string[0] != self.string[1]
        ):
            return True
        return False

    ### PUBLIC PROPERTIES ###

    @property
    def pair(self) -> typing.Tuple[str, typing.Optional[str]]:
        """
        Gets prefix / pattern pair.
        """
        return self.prefix, self.pattern

    @property
    def pattern(self) -> typing.Optional[str]:
        """
        Gets pattern.
        """
        if self._is_single_address():
            assert self.string is not None
            return self.string[1:]
        if self._is_double_address():
            assert self.string is not None
            return self.string[2:]
        return self.string

    @property
    def payload(self) -> typing.Optional[typing.Union[str, list, Path]]:
        """
        Gets payload.
        """
        return self._payload

    @property
    def prefix(self) -> str:
        """
        Gets prefix.
        """
        if self._is_single_address():
            assert self.string is not None
            return self.string[:1]
        if self._is_double_address():
            assert self.string is not None
            return self.string[:2]
        return ""

    @property
    def string(self) -> typing.Optional[str]:
        """
        Gets string.
        """
        return self._string

    ### PUBLIC METHODS ###

    def get_path(self) -> typing.Optional[Path]:
        """
        Gets path.
        """
        if isinstance(self.payload, Path):
            return self.payload
        if isinstance(self.payload, list) and isinstance(self.payload[0], Path):
            return self.payload[0]
        return None

    def is_address(self) -> bool:
        """
        Is true when response is address.
        """
        return bool(self.prefix)

    def is_command(self, commands) -> bool:
        """
        Is true when response is command.
        """
        return str(self.payload) in commands and self.string != "!"

    def is_path(self) -> bool:
        """
        Is true when response is path.
        """
        if isinstance(self.payload, Path):
            return True
        if isinstance(self.payload, list) and isinstance(self.payload[0], Path):
            return True
        return False

    def is_segment_name(self) -> bool:
        """
        Is true when response is segment name.
        """
        return Path.is_segment_name(self.string)

    def is_shell(self) -> bool:
        """
        Is true when response is shell command.
        """
        if self.string and self.string.startswith("!") and not self.string == "!!":
            return True
        return False
