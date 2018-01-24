import abjad
import importlib
import pathlib
import sys


class Configuration(abjad.Configuration):
    r'''Configuration.

    ..  container:: example

        >>> ide.Configuration()
        Configuration()

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Classes'

    __slots__ = (
        '_aliases',
        '_composer_scores_directory',
        '_composer_scores_directory_override',
        '_test_scores_directory',
        '_ide_directory',
        )

    _configuration_directory_name = 'ide'

    _configuration_file_name = 'ide.cfg'

    always_ignore = (
        '__pycache__',
        )

    editor_suffixes = (
        '.cfg',
        '.ily',
        '.log',
        '.ly',
        '.md',
        '.py',
        '.tex',
        '.txt',
        )

    noneditor_suffixes = (
        '.mid',
        '.midi',
        '.pdf',
        )

    ### INITIALIZER ###

    def __init__(self):
        abjad.Configuration.__init__(self)
        self._aliases = None
        self._composer_scores_directory = None
        self._composer_scores_directory_override = None
        self._test_scores_directory = None
        self._ide_directory = None
        self._read_aliases_file()
        self._make_missing_directories()

    ### PRIVATE METHODS ###

    @staticmethod
    def _add_test_score_to_sys_path():
        import ide
        configuration = ide.Configuration()
        directory = configuration.test_scores_directory
        for path in directory.iterdir():
            if path.is_dir():
                sys.path.insert(0, str(path))

    def _get_initial_comment(self):
        current_time = self._get_current_time()
        return [
            f'Abjad IDE configuration file created on {current_time}.',
            "This file is interpreted by ConfigParser and follows ini sytax.",
            ]

    def _get_option_definitions(self):
        return {}

    def _make_missing_directories(self):
        directory = pathlib.Path(
            abjad.abjad_configuration.composer_scores_directory
            )
        if not directory.exists():
            directory.mkdir()

    def _read_aliases_file(self):
        globals_ = globals()
        path = self.configuration_directory / '__aliases__.py'
        if path.is_file():
            text = path.read_text()
            exec(text, globals_)
        aliases = globals_.get('aliases') or abjad.OrderedDict()
        self._aliases = aliases

    ### PUBLIC PROPERTIES ###

    @property
    def aliases(self):
        r'''Gets aliases.

        ..  container:: example

            >>> ide.Configuration().aliases
            OrderedDict(...)

        Returns ordered dictionary.
        '''
        return self._aliases

    @property
    def aliases_file_path(self):
        r'''Gets aliases file path.

        ..  container:: example

            >>> ide.Configuration().aliases_file_path
            Path('.../.abjad/ide/__aliases__.py')

        Returns package path.
        '''
        import ide
        return ide.Path(self.configuration_directory / '__aliases__.py')

    @property
    def boilerplate_directory(self):
        r'''Gets boilerplate directory.

        ..  container:: example

            >>> ide.Configuration().boilerplate_directory
            Path('.../abjad/abjad/boilerplate')

        Returns package path.
        '''
        import ide
        return ide.Path(abjad.abjad_configuration.boilerplate_directory)

    @property
    def composer_scores_directory(self):
        r'''Gets composer scores directory.

        Returns package path.
        '''
        import ide
        if self._composer_scores_directory_override is not None:
            return self._composer_scores_directory_override
        if self._composer_scores_directory is None:
            scores = abjad.abjad_configuration.composer_scores_directory
            scores = ide.Path(scores).expanduser()
            self._composer_scores_directory = scores
        return self._composer_scores_directory

    @property
    def configuration_directory(self):
        r'''Gets configuration directory path.

        ..  container:: example

            >>> ide.Configuration().configuration_directory
            PosixPath('.../.abjad/ide')

        Returns path.
        '''
        path = abjad.abjad_configuration.configuration_directory
        path = path / self._configuration_directory_name
        return path

    @property
    def ide_directory(self):
        r'''Gets IDE directory.

        ..  container:: example

            >>> ide.Configuration().ide_directory
            Path('.../ide')

        Returns package path.
        '''
        import ide
        if self._ide_directory is None:
            ide_directory = ide.Path(ide.__path__[0])
            self._ide_directory = ide_directory
        return self._ide_directory

    @property
    def latex_log_file_path(self):
        r'''Gets LaTeX log file path.

        ..  container:: example

            >>> ide.Configuration().latex_log_file_path
            Path('.../.abjad/ide/latex.log')

        Returns package path.
        '''
        import ide
        return ide.Path(self.configuration_directory / 'latex.log')

    @property
    def test_scores_directory(self):
        r'''Gets test scores directory.

        ..  container:: example

            >>> ide.Configuration().test_scores_directory
            Path('.../ide/scores')

        Returns package path.
        '''
        import ide
        try:
            ide = importlib.import_module('ide')
        except ImportError:
            return
        return ide.Path(ide.__path__[0]) / 'scores'
