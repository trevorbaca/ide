import abjad

from .IO import IO


class Interaction(abjad.ContextManager):
    """
    Interaction context manager.
    """

    ### CLASS VARIABLES ###

    __slots__ = ("_io",)

    ### INITIALIZER ###

    def __init__(self, io=None) -> None:
        self._io = io

    ### SPECIAL METHODS ###

    def __enter__(self) -> None:
        """
        Enters context manager.
        """
        pass

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        """
        Exits context manager.
        """
        self.io.display("")

    def __repr__(self) -> str:
        """
        Gets interpreter representation of context manager.
        """
        return f"<{type(self).__name__}()>"

    ### PUBLIC PROPERTIES ###

    @property
    def io(self) -> IO:
        """
        Gets IO manager.
        """
        return self._io
