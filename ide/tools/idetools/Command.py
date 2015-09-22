# -*- coding: utf-8 -*-
import string


class Command(object):
    r'''Command decorator.
    '''

    ### CLASS VARIABLES ###

    _allowable_sections = (
        'back-home-quit',
        'basic',
        'build',
        'comparison',
        'definition_file',
        'display navigation',
        'git',
        'global files',
        'illustrate_file',
        'ly',
        'pdf',
        'navigation',
        'star',
        'system',
        'view',
        )

    _navigation_section_names = (
        'display navigation',
        'back-home-quit',
        'comparison',
        'navigation',
        'view',
        )

    ### INITIALIZER ###

    def __init__(
        self, 
        command_name, 
        argument_name=None,
        description=None, 
        directories=None,
        file_=None,
        forbidden_directories=(),
        in_score_directory_only=False,
        is_hidden=True,
        never_in_score_directory=False,
        outside_score=True,
        section=None,
        ):
        assert isinstance(argument_name, (str, type(None)))
        self.argument_name = argument_name
        assert isinstance(command_name, str), repr(command_name)
        assert Command._is_valid_command_name(command_name), repr(command_name)
        self.command_name = command_name
        self.description = description
        directories = directories or ()
        if isinstance(directories, str):
            directories = (directories,)
        self.directories = directories
        assert isinstance(file_, (str, type(None)))
        self.file_ = file_
        self.forbidden_directories = forbidden_directories
        assert isinstance(in_score_directory_only, bool)
        self.in_score_directory_only = in_score_directory_only
        assert isinstance(is_hidden, bool), repr(is_hidden)
        self.is_hidden = is_hidden
        assert isinstance(never_in_score_directory, bool)
        self.never_in_score_directory = never_in_score_directory
        assert isinstance(outside_score, bool) or outside_score == 'home'
        self.outside_score = outside_score
        assert section in self._allowable_sections, repr(section)
        self.section = section

    ### SPECIAL METHODS ###

    def __call__(self, method):
        r'''Calls command decorator on `method`.

        Returns `method` with metadata attached.
        '''
        method.argument_name = self.argument_name
        method.command_name = self.command_name
        if self.description is not None:
            method.description = self.description
        else:
            method.description = method.__name__.replace('_', ' ')
        method.directories = self.directories
        method.file_ = self.file_
        method.forbidden_directories = self.forbidden_directories
        method.in_score_directory_only = self.in_score_directory_only
        method.is_hidden = self.is_hidden
        method.is_navigation = self.section in self._navigation_section_names
        method.outside_score = self.outside_score
        method.never_in_score_directory = self.never_in_score_directory
        method.section = self.section
        return method

    ### PRIVATE METHODS ###

    @staticmethod
    def _is_valid_command_name(expr):
        if not isinstance(expr, str):
            return False
        for character in expr:
            if character.islower():
                continue
            if character in string.punctuation:
                continue
            return False
        return True