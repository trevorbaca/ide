import typing


class Transcript:
    """
    Transcript.
    """

    ### CLASS VARIABLES ###

    __slots__ = ("_blocks", "_lines", "_menus", "_titles")

    ### INITIALIZER ###

    def __init__(self):
        self._blocks = []
        self._lines = []
        self._menus = []
        self._titles = []

    ### SPECIAL METHODS ###

    def __contains__(self, argument) -> bool:
        """
        Is true when ``argument`` appears in transcript.
        """
        return argument in "\n".join(self.lines)

    ### PUBLIC PROPERTIES ###

    @property
    def blocks(self) -> typing.List:
        """
        Gets blocks.
        """
        return self._blocks

    @property
    def lines(self) -> typing.List[str]:
        """
        Gets lines.
        """
        return self._lines

    @property
    def menus(self) -> typing.List:
        """
        Gets menus.
        """
        return self._menus

    @property
    def titles(self) -> typing.List[str]:
        """
        Gets titles.
        """
        return self._titles

    ### PUBLIC METHODS ###

    def append(self, block, is_menu: bool = False) -> None:
        """
        Appends ``block``.
        """
        self._lines.extend(block)
        self._blocks.append(block)
        if is_menu:
            self._menus.append(block)
            self._titles.append(block[0])

    def trim(self) -> None:
        """
        Trims transcript.
        """
        for line in reversed(self.lines):
            if line == "":
                self.lines.pop(-1)
            else:
                break
        self.lines.append("")
