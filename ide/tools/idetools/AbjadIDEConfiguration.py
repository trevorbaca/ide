from __future__ import print_function
import abjad
import pathlib
import sys


class AbjadIDEConfiguration(abjad.Configuration):
    r'''Abjad IDE configuration.

    ..  container:: example

        ::

            >>> configuration = ide.tools.idetools.AbjadIDEConfiguration()

        ::

            >>> configuration
            AbjadIDEConfiguration()

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_aliases',
        '_abjad_ide_directory',
        '_abjad_ide_example_scores_directory',
        '_composer_scores_directory',
        '_composer_scores_directory_override',
        )

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
            '-*- coding: utf-8 -*-',
            '',
            'Abjad IDE configuration file created on {}.'.format(current_time),
            "This file is interpreted by ConfigParser and follows ini sytax.",
            ]

    ### PRIVATE METHODS ###

    def _add_example_score_to_sys_path(self):
        import ide
        configuration = ide.tools.idetools.AbjadIDEConfiguration()
        directory = configuration.abjad_ide_example_scores_directory
        for path in directory.glob('*'):
            if path.is_dir():
                sys.path.insert(0, str(path))

    def _cache_paths(self):
        import ide
        abjad_ide_directory = pathlib.Path(ide.__path__[0])
        self._abjad_ide_directory = abjad_ide_directory
        self._abjad_ide_example_scores_directory = \
            abjad_ide_directory / 'scores'
        directory = self._settings['composer_scores_directory']
        directory = pathlib.Path(directory).expanduser()
        self._composer_scores_directory = directory

    def _get_option_definitions(self):
        options = {
            'composer_email': {
                'comment': [
                    '',
                    'Your email.',
                    ],
                'default': 'first.last@domain.com',
                'validator': str,
                },
            'composer_full_name': {
                'comment': [
                    '',
                    'Your full name.',
                    ],
                'default': 'Full Name',
                'validator': str,
                },
            'composer_github_username': {
                'comment': [
                    '',
                    'Your GitHub username.',
                    ],
                'default': 'username',
                'validator': str,
                },
            'composer_last_name': {
                'comment': [
                    '',
                    'Your last name.',
                    ],
                'default': 'Name',
                'validator': str,
                },
            'composer_library_package_name': {
                'comment': [
                    '',
                    'Your library package name.',
                    ],
                'default': 'my_library',
                'validator': str,
                },
            'composer_scores_directory': {
                'comment': [
                    '',
                    'Your scores directory. Defaults to $HOME/scores/.',
                    ],
                'default': pathlib.Path(self.home_directory) / 'scores',
                'validator': str,
                },
            'composer_uppercase_name': {
                'comment': [
                    '',
                    'Your full name in uppercase for score covers.',
                    ],
                'default': 'FULL NAME',
                'validator': str,
                },
            'composer_website': {
                'comment': [
                    '',
                    'Your website.',
                    ],
                'default': 'www.composername.com',
                'validator': str,
                },
            }
        return options

    def _make_missing_directories(self):
        directories = (
            self.composer_scores_directory,
            self.abjad_ide_transcripts_directory,
            )
        for directory in directories:
            if not directory.exists():
                directory.mkdir()

    def _read_aliases_file(self):
        globals_ = globals()
        file_path = self.abjad_ide_aliases_file_path
        if file_path.is_file():
            with file_path.open() as file_pointer:
                file_contents_string = file_pointer.read()
            exec(file_contents_string, globals_)
        aliases = globals_.get('aliases') or abjad.TypedOrderedDict()
        self._aliases = aliases

    ### PUBLIC PROPERTIES ###

    @property
    def abjad_ide_aliases_file_path(self):
        r'''Gets Abjad IDE aliases file path.

        ..  container:: example

            ::

                >>> configuration.abjad_ide_aliases_file_path
                PosixPath('.../.abjad/ide/__aliases__.py')

        Returns string.
        '''
        return pathlib.Path(
            self.configuration_directory_path,
            '__aliases__.py',
            )

    @property
    def abjad_ide_boilerplate_directory(self):
        r'''Gets Abjad IDE boilerplate directory.

        ..  container:: example

            >>> configuration.abjad_ide_boilerplate_directory
            PosixPath('.../ide/boilerplate')

        Returns path.
        '''
        return self.abjad_ide_directory / 'boilerplate'

    @property
    def abjad_ide_directory(self):
        r'''Gets Abjad IDE directory.

        Returns string.
        '''
        return self._abjad_ide_directory

    @property
    def abjad_ide_example_scores_directory(self):
        r'''Gets Abjad IDE example scores directory.

        ..  container:: example

            ::

                >>> configuration.abjad_ide_example_scores_directory
                PosixPath('.../ide/scores')

        Returns path.
        '''
        return self._abjad_ide_example_scores_directory

    @property
    def abjad_ide_transcripts_directory(self):
        r'''Gets Abjad IDE transcripts directory.

        ..  container:: example

            ::

                >>> configuration.abjad_ide_transcripts_directory
                PosixPath('.../.abjad/ide/transcripts')

        Returns string.
        '''
        return pathlib.Path(self.configuration_directory_path, 'transcripts')

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
    def composer_email(self):
        r'''Gets composer email.

        ..  container:: example

            ::

                >>> configuration.composer_email
                '...'

        Aliases `composer_email` setting in Abjad IDE configuration file.

        Returns string.
        '''
        return self._settings['composer_email']

    @property
    def composer_full_name(self):
        r'''Gets composer full name.

        ..  container:: example

            ::

                >>> configuration.composer_full_name
                '...'

        Aliases `composer` setting in Abjad IDE configuration
        file.

        Returns string.
        '''
        return self._settings['composer_full_name']

    @property
    def composer_github_username(self):
        r'''Gets GitHub username.

        ..  container:: example

            ::

                >>> configuration.composer_github_username
                '...'

        Aliases `composer_github_username` setting in Abjad IDE configuration
        file.

        Returns string.
        '''
        return self._settings['composer_github_username']

    @property
    def composer_last_name(self):
        r'''Gets composer last name.

        ..  container:: example

            ::

                >>> configuration.composer_last_name
                '...'

        Aliases `composer` setting in Abjad IDE configuration
        file.

        Returns string.
        '''
        return self._settings['composer_last_name']

    @property
    def composer_library_package_name(self):
        r'''Gets composer library packagename.

        ..  container:: example

            ::

                >>> configuration.composer_library_package_name
                '...'

        Aliases `composer_library_package_name` setting in Abjad IDE
        configuration file.

        Returns string.
        '''
        return self._settings['composer_library_package_name']

    @property
    def composer_scores_directory(self):
        r'''Gets composer scores directory.

        ..  container:: example

            ::

                >>> configuration.composer_scores_directory
                PosixPath('...')

        Aliases `composer_scores_directory` setting in Abjad IDE configuration
        file.

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

                >>> configuration.composer_uppercase_name
                '...'

        Aliases `composer_uppercase_name` setting in Abjad IDE
        configuration file.

        Returns string.
        '''
        return self._settings['composer_uppercase_name']

    @property
    def composer_website(self):
        r'''Gets composer website.

        ..  container:: example

            ::

                >>> configuration.composer_website  # doctest: +SKIP
                'My website address'

        Aliases `composer_website` setting in Abjad IDE configuration
        file.

        Returns string.
        '''
        return self._settings['composer_website']

    @property
    def configuration_directory_name(self):
        r'''Gets configuration directory name.

        ..  container:: example

            ::

                >>> configuration.configuration_directory_name
                'ide'

        Returns string.
        '''
        return 'ide'

    @property
    def configuration_directory_path(self):
        r'''Gets configuration directory path.

        ..  container:: example

            ::

                >>> configuration.configuration_directory_path
                '.../.abjad/ide'

        Returns string.
        '''
        path = pathlib.Path(
            abjad.abjad_configuration.configuration_directory_path,
            self.configuration_directory_name,
            )
        return str(path)

    @property
    def configuration_file_name(self):
        r'''Configuration file name.

        ..  container:: example

            ::

                >>> configuration.configuration_file_name
                'ide.cfg'

        Returns string.
        '''
        return 'ide.cfg'

    @property
    def latex_log_file_path(self):
        r'''Gets LaTeX log file path.

        ..  container:: example

            ::

                >>> configuration.latex_log_file_path
                PosixPath('.../.abjad/ide/latex.log')

        Returns string.
        '''
        return pathlib.Path(self.configuration_directory_path, 'latex.log')
