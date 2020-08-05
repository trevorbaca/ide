import abjad


class Configuration(abjad.Configuration):
    """
    Configuration.

    ..  container:: example

        >>> ide.Configuration()
        Configuration()

    """

    ### CLASS VARIABLES ###

    __slots__ = (
        "_aliases",
        "_composer_scores_directory",
        "_composer_scores_directory_override",
        "_test_scores_directory",
        "_ide_directory",
    )

    _configuration_directory_name = "ide"

    _configuration_file_name = "ide.cfg"

    abjad_configuration = abjad.Configuration()

    editor_suffixes = (
        ".cfg",
        ".ily",
        ".log",
        ".ly",
        ".md",
        ".py",
        ".tex",
        ".txt",
    )

    noneditor_suffixes = (".mid", ".midi", ".pdf")

    ### INITIALIZER ###

    def __init__(self):
        abjad.Configuration.__init__(self)
        self._aliases = None
        self._composer_scores_directory = None
        self._composer_scores_directory_override = None
        self._test_scores_directory = None
        self._ide_directory = None
        self._read_aliases_file()

    ### PRIVATE METHODS ###

    def _get_initial_comment(self):
        current_time = self._get_current_time()
        return [
            f"Abjad IDE configuration file created on {current_time}.",
            "This file is interpreted by ConfigParser and follows ini sytax.",
        ]

    def _get_option_definitions(self):
        return {}

    def _make_missing_directories(self):
        directory = self.abjad_configuration.composer_scores_directory
        if not directory.exists():
            directory.mkdir()

    def _read_aliases_file(self):
        globals_ = globals()
        path = self.configuration_directory / "__aliases__.py"
        if path.is_file():
            text = path.read_text()
            exec(text, globals_)
        aliases = globals_.get("aliases") or abjad.OrderedDict()
        self._aliases = aliases

    ### PUBLIC PROPERTIES ###

    @property
    def aliases(self) -> abjad.OrderedDict:
        """
        Gets aliases.

        ..  container:: example

            >>> ide.Configuration().aliases
            OrderedDict(...)

        """
        return self._aliases

    @property
    def aliases_file_path(self) -> abjad.Path:
        """
        Gets aliases file path.

        ..  container:: example

            >>> ide.Configuration().aliases_file_path
            Path('.../.abjad/__aliases__.py')

        """
        return abjad.Path(self.configuration_directory / "__aliases__.py")

    @property
    def boilerplate_directory(self) -> abjad.Path:
        """
        Gets boilerplate directory.

        ..  container:: example

            >>> ide.Configuration().boilerplate_directory
            Path('.../ide/boilerplate')

        """
        return abjad.Path(__file__).parent.parent / "boilerplate"

    @property
    def configuration_directory(self) -> abjad.Path:
        """
        Gets configuration directory path.

        ..  container:: example

            >>> ide.Configuration().configuration_directory
            Path('.../.abjad')

        """
        return abjad.Path(self.abjad_configuration.configuration_directory)

    @property
    def ide_directory(self) -> abjad.Path:
        """
        Gets IDE directory.

        ..  container:: example

            >>> ide.Configuration().ide_directory
            Path('.../ide')

        """
        if self._ide_directory is None:
            self._ide_directory = abjad.Path(__file__).parent
        return self._ide_directory

    @property
    def latex_log_file_path(self) -> abjad.Path:
        """
        Gets LaTeX log file path.

        ..  container:: example

            >>> ide.Configuration().latex_log_file_path
            Path('.../.abjad/latex.log')

        """
        return abjad.Path(self.configuration_directory / "latex.log")

    @property
    def test_scores_directory(self) -> abjad.Path:
        """
        Gets test scores directory.

        ..  container:: example

            >>> ide.Configuration().test_scores_directory
            Path('.../ide/scores')

        """
        return abjad.Path(__file__).parent.parent / "scores"
