import typing

from . import pathx


class Response:
    """
    Response.
    """

    ### CLASS VARIABLES ###

    __slots__ = ("_payload", "_string")

    ### INITIALIZER ###

    def __init__(
        self,
        payload: typing.Union[str, list, pathx.Path] = None,
        string: str = None,
    ) -> None:
        self._payload = payload
        self._string = string

    ### PUBLIC PROPERTIES ###

    @property
    def payload(self) -> typing.Optional[typing.Union[str, list, pathx.Path]]:
        """
        Gets payload.
        """
        return self._payload

    @property
    def string(self) -> typing.Optional[str]:
        """
        Gets string.
        """
        return self._string

    ### PUBLIC METHODS ###

    def get_path(self) -> typing.Optional[pathx.Path]:
        """
        Gets path.
        """
        if isinstance(self.payload, pathx.Path):
            return self.payload
        if isinstance(self.payload, list) and isinstance(self.payload[0], pathx.Path):
            return self.payload[0]
        return None

    def is_command(self, commands) -> bool:
        """
        Is true when response is command.
        """
        return str(self.payload) in commands and self.string != "!"

    def is_path(self) -> bool:
        """
        Is true when response is path.
        """
        if isinstance(self.payload, pathx.Path):
            return True
        if isinstance(self.payload, list) and isinstance(self.payload[0], pathx.Path):
            return True
        return False

    def is_segment_name(self) -> bool:
        """
        Is true when response is segment name.
        """
        return pathx.Path.is_segment_name(self.string)

    def is_shell(self) -> bool:
        """
        Is true when response is shell command.
        """
        if self.string and self.string.startswith("!") and not self.string == "!!":
            return True
        return False
