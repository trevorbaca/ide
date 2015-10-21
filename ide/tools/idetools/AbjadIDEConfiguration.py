# -*- coding: utf-8 -*-
from __future__ import print_function
import collections
import os
import sys
from abjad.tools.systemtools.AbjadConfiguration import AbjadConfiguration


class AbjadIDEConfiguration(AbjadConfiguration):
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
        '_composer_scores_directory_override',
        )

    ### INITIALIZER ###

    def __init__(self):
        AbjadConfiguration.__init__(self)
        self._read_aliases_file()
        self._composer_scores_directory_override = None
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
        from ide.tools import idetools
        configuration = idetools.AbjadIDEConfiguration()
        directory = configuration.abjad_ide_example_scores_directory
        for name in os.listdir(directory):
            path = os.path.join(directory, name)
            if os.path.isdir(path):
                sys.path.insert(0, path)

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
                'default': os.path.join(self.home_directory, 'scores'),
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
            if not os.path.exists(directory):
                os.makedirs(directory)

    def _read_aliases_file(self):
        aliases = None
        file_path = self.abjad_ide_aliases_file_path
        if os.path.isfile(file_path):
            with open(file_path, 'r') as file_pointer:
                file_contents_string = file_pointer.read()
            exec(file_contents_string)
        aliases = aliases or collections.OrderedDict()
        self._aliases = aliases

    ### PUBLIC PROPERTIES ###

    @property
    def abjad_ide_aliases_file_path(self):
        r'''Gets Abjad IDE aliases file path.

        ..  container:: example

            ::

                >>> configuration.abjad_ide_aliases_file_path
                '.../.abjad/ide/__aliases__.py'

        Returns string.
        '''
        return os.path.join(
            self.abjad_ide_configuration_directory,
            '__aliases__.py',
            )

    @property
    def abjad_ide_boilerplate_directory(self):
        r'''Gets Abjad IDE boilerplate directory.

        ..  container:: example

            >>> configuration.abjad_ide_boilerplate_directory
            '.../ide/boilerplate'

        Returns string.
        '''
        path = os.path.join(
            self.abjad_ide_directory,
            'boilerplate',
            )
        return path

    @property
    def abjad_ide_configuration_directory(self):
        r'''Gets Abjad IDE configuration directory.

        ..  container:: example

            ::

                >>> configuration.abjad_ide_configuration_directory
                '.../.abjad/ide'

        Returns string.
        '''
        return os.path.join(self.abjad_configuration_directory, 'ide')

    @property
    def abjad_ide_configuration_file_path(self):
        r'''Gets Abjad IDE configuration file path.

        ..  container:: example

            ::

                >>> configuration.abjad_ide_configuration_file_path
                '.../.abjad/ide/ide.cfg'

        Returns string.
        '''
        return os.path.join(
            self.abjad_ide_configuration_directory,
            'ide.cfg',
            )

    @property
    def abjad_ide_example_scores_directory(self):
        r'''Gets Abjad IDE example scores directory.

        ..  container:: example

            ::

                >>> configuration.abjad_ide_example_scores_directory
                '.../ide/scores'

        Returns string.
        '''
        path = os.path.join(
            self.abjad_ide_directory,
            'scores',
            )
        return path

    @property
    def abjad_ide_transcripts_directory(self):
        r'''Gets Abjad IDE transcripts directory.

        ..  container:: example

            ::

                >>> configuration.abjad_ide_transcripts_directory
                '.../.abjad/ide/transcripts'

        Returns string.
        '''
        path = os.path.join(
            self.abjad_ide_configuration_directory,
            'transcripts',
            )
        return path

    @property
    def aliases(self):
        r'''Gets aliases.

        ..  container:: example

            ::

                >>> configuration.aliases
                OrderedDict(...)

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
                '...'

        Aliases `composer_scores_directory` setting in Abjad IDE configuration
        file.

        Returns string.
        '''
        if self._composer_scores_directory_override is not None:
            return self._composer_scores_directory_override
        path = self._settings['composer_scores_directory']
        path = os.path.expanduser(path)
        return path

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
    def configuration_directory(self):
        r'''Gets configuration directory.

        ..  container:: example

            ::

                >>> configuration.configuration_directory
                '.../.abjad/ide'

        Aliases `abjad_ide_configuration_directory`.

        Returns string.
        '''
        return self.abjad_ide_configuration_directory

    @property
    def configuration_file_path(self):
        r'''Gets configuration file path.

        ..  container:: example

            ::

                >>> configuration.configuration_file_path
                '.../.abjad/ide/ide.cfg'

        Aliases `abjad_ide_configuration_file_path`.

        Returns string.
        '''
        return self.abjad_ide_configuration_file_path

    @property
    def latex_log_file_path(self):
        r'''Gets LaTeX log file path.

        ..  container:: example

            ::

                >>> configuration.latex_log_file_path
                '.../.abjad/ide/latex.log'

        Returns string.
        '''
        return os.path.join(
            self.abjad_ide_configuration_directory,
            'latex.log',
            )