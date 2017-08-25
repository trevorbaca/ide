from __future__ import print_function
import abjad
import pathlib
import sys


class Configuration(abjad.Configuration):
    r'''Configuration.

    ..  container:: example

        ::

            >>> configuration = ide.Configuration()
            >>> configuration
            Configuration()

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Classes'

    __slots__ = (
        '_aliases',
        '_composer_scores_directory',
        '_composer_scores_directory_override',
        '_example_scores_directory',
        '_ide_directory',
        )

    _configuration_directory_name = 'ide'

    _configuration_file_name = 'ide.cfg'

    ### INITIALIZER ###

    def __init__(self):
        abjad.Configuration.__init__(self)
        self._composer_scores_directory_override = None
        self._cache_paths()
        self._read_aliases_file()
        self._make_missing_directories()

    ### PRIVATE PROPERTIES ###

    @property
    def _initial_comment(self):
        current_time = self._current_time
        return [
            f'Abjad IDE configuration file created on {current_time}.',
            "This file is interpreted by ConfigParser and follows ini sytax.",
            ]

    ### PRIVATE METHODS ###

    def _add_example_score_to_sys_path(self):
        import ide
        configuration = ide.Configuration()
        directory = configuration.example_scores_directory
        for path in directory.glob('*'):
            if path.is_dir():
                sys.path.insert(0, str(path))

    def _cache_paths(self):
        import ide
        ide_directory = pathlib.Path(ide.__path__[0])
        self._ide_directory = ide_directory
        self._example_scores_directory = ide_directory / 'scores'
        directory = self._settings['composer_scores_directory']
        directory = pathlib.Path(directory).expanduser()
        self._composer_scores_directory = directory

    def _get_option_definitions(self):
        options = {
            'composer_email': {
                'comment': ['Your email.'],
                'default': 'first.last@domain.com',
                'validator': str,
                },
            'composer_full_name': {
                'comment': ['Your full name.'],
                'default': 'Full Name',
                'validator': str,
                },
            'composer_github_username': {
                'comment': ['Your GitHub username.'],
                'default': 'username',
                'validator': str,
                },
            'composer_last_name': {
                'comment': ['Your last name.'],
                'default': 'Name',
                'validator': str,
                },
            'composer_library': {
                'comment': ['Your library.'],
                'default': 'my_library',
                'validator': str,
                },
            'composer_scores_directory': {
                'comment': ['Your scores directory.'],
                'default': self.home_directory / 'scores',
                'validator': str,
                },
            'composer_uppercase_name': {
                'comment': ['Your full name in uppercase for score covers.'],
                'default': 'FULL NAME',
                'validator': str,
                },
            'composer_website': {
                'comment': ['Your website.'],
                'default': 'www.composername.com',
                'validator': str,
                },
            }
        return options

    def _make_missing_directories(self):
        directories = (
            self.composer_scores_directory,
            self.transcripts_directory,
            )
        for directory in directories:
            if not directory.exists():
                directory.mkdir()

    def _read_aliases_file(self):
        globals_ = globals()
        file_path = self.aliases_file_path
        if file_path.is_file():
            file_contents_string = file_path.read_text()
            exec(file_contents_string, globals_)
        aliases = globals_.get('aliases') or abjad.TypedOrderedDict()
        self._aliases = aliases

    ### PUBLIC PROPERTIES ###

    @property
    def aliases(self):
        r'''Gets aliases.

        ..  container:: example

            ::

                >>> configuration.aliases
                TypedOrderedDict(...)

        Returns ordered dictionary.
        '''
        return self._aliases

    @property
    def aliases_file_path(self):
        r'''Gets aliases file path.

        ..  container:: example

            ::

                >>> configuration.aliases_file_path
                PosixPath('.../.abjad/ide/__aliases__.py')

        Returns string.
        '''
        return self.configuration_directory / '__aliases__.py'

    @property
    def boilerplate_directory(self):
        r'''Gets boilerplate directory.

        ..  container:: example

            >>> configuration.boilerplate_directory
            PosixPath('.../ide/boilerplate')

        Returns path.
        '''
        return self.ide_directory / 'boilerplate'

    @property
    def composer_email(self):
        r'''Gets composer email.

        ..  container:: example

            ::

                >>> configuration.composer_email # doctest: +SKIP
                'trevor.baca@gmail.com'

        Returns string.
        '''
        return self._settings['composer_email']

    @property
    def composer_full_name(self):
        r'''Gets composer full name.

        ..  container:: example

            ::

                >>> configuration.composer_full_name # doctest: +SKIP
                'Trevor Bača'

        Returns string.
        '''
        return self._settings['composer_full_name']

    @property
    def composer_github_username(self):
        r'''Gets GitHub username.

        ..  container:: example

            ::

                >>> configuration.composer_github_username # doctest: +SKIP
                'trevorbaca'

        Returns string.
        '''
        return self._settings['composer_github_username']

    @property
    def composer_last_name(self):
        r'''Gets composer last name.

        ..  container:: example

            ::

                >>> configuration.composer_last_name # doctest: +SKIP
                'Bača'

        Returns string.
        '''
        return self._settings['composer_last_name']

    @property
    def composer_library(self):
        r'''Gets composer library package name.

        ..  container:: example

            ::

                >>> configuration.composer_library # doctest: +SKIP
                'baca'

        Returns string.
        '''
        return self._settings['composer_library']

    @property
    def composer_scores_directory(self):
        r'''Gets composer scores directory.

        ..  container:: example

            ::

                >>> configuration.composer_scores_directory # doctest: +SKIP
                PosixPath('/Users/trevorbaca/Scores')

        Returns path.
        '''
        if self._composer_scores_directory_override is not None:
            return self._composer_scores_directory_override
        return self._composer_scores_directory

    @property
    def composer_uppercase_name(self):
        r'''Gets composer uppercase name.

        ..  container:: example

            ::

                >>> configuration.composer_uppercase_name # doctest: +SKIP
                'TREVOR BAČA'

        Returns string.
        '''
        return self._settings['composer_uppercase_name']

    @property
    def composer_website(self):
        r'''Gets composer website.

        ..  container:: example

            ::

                >>> configuration.composer_website  # doctest: +SKIP
                'www.trevobaca.com'

        Returns string.
        '''
        return self._settings['composer_website']

    @property
    def configuration_directory(self):
        r'''Gets configuration directory path.

        ..  container:: example

            ::

                >>> configuration.configuration_directory
                PosixPath('.../.abjad/ide')

        Returns string.
        '''
        path = abjad.abjad_configuration.configuration_directory
        path = path / self._configuration_directory_name
        return path

    @property
    def example_scores_directory(self):
        r'''Gets example scores directory.

        ..  container:: example

            ::

                >>> configuration.example_scores_directory
                PosixPath('.../ide/scores')

        Returns path.
        '''
        return self._example_scores_directory

    @property
    def ide_directory(self):
        r'''Gets IDE directory.

        ..  container:: example

            ::

                >>> configuration.ide_directory
                PosixPath('.../ide')

        Returns string.
        '''
        return self._ide_directory

    @property
    def latex_log_file_path(self):
        r'''Gets LaTeX log file path.

        ..  container:: example

            ::

                >>> configuration.latex_log_file_path
                PosixPath('.../.abjad/ide/latex.log')

        Returns string.
        '''
        return self.configuration_directory / 'latex.log'

    @property
    def transcripts_directory(self):
        r'''Gets transcripts directory.

        ..  container:: example

            ::

                >>> configuration.transcripts_directory
                PosixPath('.../.abjad/ide/transcripts')

        Returns string.
        '''
        return self.configuration_directory / 'transcripts'
