# -*- encoding: utf-8 -*-
from __future__ import print_function
import os
from abjad.tools.systemtools.AbjadConfiguration import AbjadConfiguration


class Configuration(AbjadConfiguration):
    r'''Abjad IDE configuration.

    ..  container:: example

        ::

            >>> abjad_ide = ide.tools.idetools.AbjadIDE(is_test=True)
            >>> configuration = abjad_ide._configuration
            >>> configuration
            Configuration()

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        )

    ### INITIALIZER ###

    def __init__(self):
        AbjadConfiguration.__init__(self)
        self._make_missing_directories()

    ### PRIVATE PROPERTIES ###

    @property
    def _initial_comment(self):
        current_time = self._current_time
        return [
            '-*- coding: utf-8 -*-',
            '',
            'Abjad IDE configuration file created on {}.'.format(current_time),
            'This file is interpreted by ConfigObj and follows ini sytnax.',
        ]

    ### PRIVATE METHODS ###

    def _get_option_definitions(self):
        options = {
            'composer_full_name': {
                'comment': [
                    '',
                    'Your full name.',
                ],
                'spec': "string(default='Full Name')",
            },
            'composer_last_name': {
                'comment': [
                    '',
                    'Your last name.',
                ],
                'spec': "string(default='Name')",
            },
            'composer_uppercase_name': {
                'comment': [
                    '',
                    'Your full name in uppercase for score covers.',
                ],
                'spec': "string(default='FULL NAME')",
            },
            'composer_email': {
                'comment': [
                    '',
                    'Your email.',
                ],
                'spec': "string(default=first.last@domain.com)",
            },
            'composer_website': {
                'comment': [
                    '',
                    'Your website.',
                ],
                'spec': "string(default=www.composername.com)",
            },
            'github_username': {
                'comment': [
                    '',
                    'Your GitHub username.',
                ],
                'spec': "string(default=None)",
            },
            'scores_directory': {
                'comment': [
                    '',
                    'Your scores directory. Defaults to $HOME/scores/.',
                ],
                'spec': 'string(default={!r})'.format(
                    os.path.join(
                        self.home_directory,
                        'scores',
                        )
                    ),
            },
        }
        return options

    def _make_missing_directories(self):
        directories = (
            self.scores_directory,
            self.abjad_ide_transcripts_directory,
            )
        for directory in directories:
            if not os.path.exists(directory):
                os.makedirs(directory)

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
    def abjad_ide_wrangler_views_directory(self):
        r'''Gets Abjad IDE wrangler views directory.

        ..  container::

            >>> configuration.abjad_ide_wrangler_views_directory
            '.../views'

        Defined equal to views/ subdirectory of Abjad IDE configuration 
        directory.

        Returns string.
        '''
        return os.path.join(self.abjad_ide_configuration_directory, 'views')

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
    def example_scores_directory(self):
        r'''Gets example scores directory.

        ..  container:: example

            ::

                >>> configuration.example_scores_directory
                '.../ide/scores'

        Returns string.
        '''
        path = os.path.join(
            self.abjad_ide_directory,
            'scores',
            )
        return path

    @property
    def github_username(self):
        r'''Gets GitHub username.

        ..  container:: example

            ::

                >>> configuration.github_username
                '...'

        Aliases `github_username` setting in Abjad IDE configuration file.

        Returns string.
        '''
        return self._settings['github_username']

    @property
    def home_directory(self):
        r'''Gets home directory.

        ..  container:: example

            ::

                >>> configuration.home_directory
                '...'

        Returns string.
        '''
        superclass = super(Configuration, self)
        return superclass.home_directory

    @property
    def scores_directory(self):
        r'''Gets scores directory.

        ..  container:: example

            ::

                >>> configuration.scores_directory
                '...'

        Aliases `scores_directory` setting in Abjad IDE configuration file.

        Returns string.
        '''
        path = self._settings['scores_directory']
        path = os.path.expanduser(path)
        path = os.path.normpath(path)
        return path