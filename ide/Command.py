import string
import typing


class Command(object):
    """
    Command.

    Decorates IDE methods.
    """

    ### CLASS VARIABLES ###

    known_sections = (
        "all",
        "back cover",
        "build",
        "clipboard",
        "definition",
        "definitions",
        "directory",
        "front cover",
        "git",
        "go",
        "hop",
        "illustration",
        "layout",
        "log",
        "music",
        "music annotations",
        "package",
        "parts",
        "path",
        "persistent indicators",
        "preface",
        "score",
        "segment.midi",
        "segments",
        "shell",
        "show",
        "smart",
        "stylesheet",
        "text",
    )

    ### INITIALIZER ###

    def __init__(
        self,
        command_name: str,
        score_package_path_blacklist: typing.Tuple[str, ...] = (),
        description: str = None,
        external_directories: bool = None,
        menu_section: str = None,
        score_package_paths: typing.Union[bool, typing.Tuple[str, ...]] = None,
        scores_directory: bool = None,
    ) -> None:
        assert isinstance(command_name, str), repr(command_name)
        assert Command._is_valid_command_name(command_name), repr(command_name)
        self.score_package_path_blacklist = score_package_path_blacklist
        self.command_name = command_name
        self.description = description
        if external_directories is not None:
            external_directories = bool(external_directories)
        self.external_directories = external_directories
        score_package_paths = score_package_paths or ()
        if isinstance(score_package_paths, str):
            score_package_paths = (score_package_paths,)
        self.score_package_paths = score_package_paths
        if scores_directory is not None:
            scores_directory = bool(scores_directory)
        self.scores_directory = scores_directory
        assert menu_section in self.known_sections, repr(menu_section)
        self.menu_section = menu_section

    ### SPECIAL METHODS ###

    def __call__(self, method):
        """
        Calls command decorator on ``method``.

        Returns ``method`` with metadata attached.
        """
        method.score_package_path_blacklist = self.score_package_path_blacklist
        method.command_name = self.command_name
        if self.description is not None:
            method.description = self.description
        else:
            method.description = method.__name__.replace("_", " ")
        method.external_directories = self.external_directories
        method.menu_section = self.menu_section
        method.score_package_paths = self.score_package_paths
        method.scores_directory = self.scores_directory
        return method

    ### PRIVATE METHODS ###

    @staticmethod
    def _is_valid_command_name(argument):
        if not isinstance(argument, str):
            return False
        for character in argument:
            if character.islower():
                continue
            if character in string.punctuation:
                continue
            return False
        return True
