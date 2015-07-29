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
                'spec': "string(default='Last Name')",
            },
            'composer_email': {
                'comment': [
                    '',
                    'Your email.',
                ],
                'spec': "string(default=None)",
            },
            'composer_website': {
                'comment': [
                    '',
                    'Your website.',
                ],
                'spec': "string(default=None)",
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
                    'The directory where you house your scores.',
                    'Defaults to $HOME/scores/.'
                ],
                'spec': 'string(default={!r})'.format(
                    os.path.join(
                        self.home_directory,
                        'scores',
                        )
                    ),
            },
            'upper_case_composer_full_name': {
                'comment': [
                    '',
                    'Upper case version of your full name for score covers.',
                ],
                'spec': "string(default='Upper Case Full Name')",
            },
        }
        return options

    def _make_missing_directories(self):
        directories = (
            self.user_score_packages_directory,
            self.transcripts_directory,
            )
        for directory in directories:
            if not os.path.exists(directory):
                os.makedirs(directory)

    def _path_to_score_path(self, path):
        is_user_score = False
        if path.startswith(self.user_score_packages_directory):
            is_user_score = True
            prefix = len(self.user_score_packages_directory)
        elif path.startswith(self.example_score_packages_directory):
            prefix = len(self.example_score_packages_directory)
        else:
            return
        path_prefix = path[:prefix]
        path_suffix = path[prefix + 1:]
        score_name = path_suffix.split(os.path.sep)[0]
        score_path = os.path.join(path_prefix, score_name)
        # test for installable Python package structure
        outer_init_path = os.path.join(score_path, '__init__.py')
        inner_init_path = os.path.join(
            score_path, 
            score_name, 
            '__init__.py',
            )
        if (not os.path.exists(outer_init_path) and
            os.path.exists(inner_init_path)):
            score_path = os.path.join(score_path, score_name)
        return score_path

    def _path_to_storehouse(self, path):
        is_in_score = False
        if path.startswith(self.user_score_packages_directory):
            is_in_score = True
            prefix = len(self.user_score_packages_directory)
        elif path.startswith(self.example_score_packages_directory):
            is_in_score = True
            prefix = len(self.example_score_packages_directory)
        else:
            message = 'unidentifiable path: {!r}.'
            message = message.format(path)
            raise Exception(message)
        path_prefix = path[:prefix]
        remainder = path[prefix+1:]
        path_parts = remainder.split(os.path.sep)
        assert 1 <= len(path_parts)
        if is_in_score:
            path_parts = path_parts[:3]
        else:
            assert 1 <= len(path_parts)
            path_parts = path_parts[:1]
        storehouse_path = os.path.join(path_prefix, *path_parts)
        return storehouse_path

    ### PUBLIC PROPERTIES ###

    @property
    def aliases_file_path(self):
        r'''Gets aliases file path.

        ..  container:: example

            ::

                >>> configuration.aliases_file_path
                '.../.abjad/ide/__aliases__.py'

        Returns string.
        '''
        return os.path.join(
            self.configuration_directory,
            '__aliases__.py',
            )

    @property
    def boilerplate_directory(self):
        r'''Gets boilerplate directory.

        ..  container:: example

            >>> configuration.boilerplate_directory
            '.../ide/boilerplate'

        Returns string.
        '''
        path = os.path.join(
            self.abjad_ide_directory,
            'boilerplate',
            )
        return path

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

        Returns string.
        '''
        return os.path.join(self.abjad_configuration_directory, 'ide')

    @property
    def configuration_file_name(self):
        r'''Gets configuration file name.

        ..  container:: example

            ::

                >>> configuration.configuration_file_name
                'ide.cfg'

        Returns string.
        '''
        return 'ide.cfg'

    @property
    def configuration_file_path(self):
        r'''Gets configuration file path.

        ..  container:: example

            ::

                >>> configuration.configuration_file_path
                '.../.abjad/ide/ide.cfg'

        Returns string.
        '''
        return os.path.join(
            self.configuration_directory,
            self.configuration_file_name,
            )

    @property
    def example_score_packages_directory(self):
        r'''Gets Abjad score packages directory.

        ..  container:: example

            ::

                >>> configuration.example_score_packages_directory
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
    def transcripts_directory(self):
        r'''Gets Abjad IDE transcripts directory.

        ..  container:: example

            ::

                >>> configuration.transcripts_directory
                '.../.abjad/ide/transcripts'

        Returns string.
        '''
        path = os.path.join(
            self.configuration_directory,
            'transcripts',
            )
        return path

    @property
    def unicode_directive(self):
        r'''Gets Unicode directive.

        ..  container:: example

            ::

                >>> configuration.unicode_directive
                '# -*- encoding: utf-8 -*-'

        Returns string.
        '''
        return '# -*- encoding: utf-8 -*-'

    @property
    def upper_case_composer_full_name(self):
        r'''Gets upper case composer full name.

        ..  container:: example

            ::

                >>> configuration.composer_full_name
                '...'

        Aliases `upper_case_composer_full_name` setting in Abjad IDE 
        configuration file.

        Returns string.
        '''
        return self._settings['upper_case_composer_full_name']

    @property
    def user_score_packages_directory(self):
        r'''Gets user score packages directory.

        ..  container:: example

            ::

                >>> configuration.user_score_packages_directory
                '...'

        Aliases `scores_directory` setting in Abjad IDE configuration file.

        Returns string.
        '''
        path = self._settings['scores_directory']
        path = os.path.expanduser(path)
        path = os.path.normpath(path)
        return path

    @property
    def wrangler_views_directory(self):
        r'''Gets wrangler views directory.

        ..  container::

            >>> configuration.wrangler_views_directory
            '.../views'

        Defined equal to views/ subdirectory of Abjad IDE directory.

        Returns string.
        '''
        return os.path.join(self.configuration_directory, 'views')

    ### PUBLIC METHODS ###

    def list_score_directories(
        self,
        abjad=False,
        user=False,
        ):
        r'''Lists score directories.

        ..  container:: example

            Lists Abjad score directories:

            ::

                >>> for x in configuration.list_score_directories(
                ...     abjad=True,
                ...     ):
                ...     x
                '.../ide/scores/blue_example_score'
                '.../ide/scores/etude_example_score'
                '.../ide/scores/red_example_score'

        Returns list.
        '''
        result = []
        if abjad:
            scores_directory = self.example_score_packages_directory
            directory_entries = sorted(os.listdir(scores_directory))
            for directory_entry in directory_entries:
                if directory_entry[0].isalpha():
                    path = os.path.join(
                        self.example_score_packages_directory,
                        directory_entry,
                        )
                    result.append(path)
        if user:
            scores_directory = self.user_score_packages_directory
            directory_entries = sorted(os.listdir(scores_directory))
            for directory_entry in directory_entries:
                if not directory_entry[0].isalpha():
                    continue
                path = os.path.join(
                    self.user_score_packages_directory,
                    directory_entry,
                    )
                init_path = os.path.join(path, '__init__.py')
                if not os.path.exists(init_path):
                    path = os.path.join(path, directory_entry)
                    init_path = os.path.join(path, '__init__.py')
                    if not os.path.exists(init_path):
                        continue
                result.append(path)
        return result

    def path_to_package(self, path):
        r'''Changes `path` to package.

        Returns string.
        '''
        if path is None:
            return
        assert isinstance(path, str), repr(path)
        path = os.path.normpath(path)
        if path.endswith('.py'):
            path, file_extension = os.path.splitext(path)
        if path.startswith(self.example_score_packages_directory):
            prefix = len(self.example_score_packages_directory) + 1
        elif path.startswith(self.abjad_ide_directory):
            prefix = len(os.path.dirname(self.abjad_ide_directory)) + 1
        elif path.startswith(self.user_score_packages_directory):
            prefix = len(self.user_score_packages_directory) + 1
        else:
            message = 'can not change path to package: {!r}.'
            message = message.format(path)
            raise Exception(message)
        package = path[prefix:]
        if path.startswith(self.example_score_packages_directory):
            # change red_example_score/red_example_score/materials/foo
            # to red_example_score/materials/foo
            parts = package.split(os.path.sep)
            parts = parts[1:]
            package = os.path.sep.join(parts)
        package = package.replace(os.path.sep, '.')
        return package