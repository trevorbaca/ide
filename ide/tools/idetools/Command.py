# -*- encoding: utf-8 -*-
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
        'display navigation',
        'git',
        'global files',
        'navigation',
        'package',
        'sibling package',
        'sibling score',
        'star',
        'system',
        'view',
        )

    _navigation_section_names = (
        'display navigation',
        'back-home-quit',
        'comparison',
        'navigation',
        'sibling package',
        'sibling score',
        'view',
        )

    ### INITIALIZER ###

    def __init__(
        self, 
        command_name, 
        description=None, 
        section=None,
        is_navigation=False,
        is_hidden=True,
        in_score=True,
        outside_score=True,
        ):
        assert isinstance(command_name, str), repr(command_name)
        assert Command._is_valid_command_name(command_name), repr(command_name)
        self.command_name = command_name
        self.description = description
        assert section in self._allowable_sections, repr(
            section)
        self.section = section
        assert isinstance(is_hidden, bool), repr(is_hidden)
        self.is_hidden = is_hidden
        assert isinstance(is_navigation, bool), repr(is_navigation)
        self.is_navigation = is_navigation
        assert isinstance(in_score, bool), repr(in_score)
        self.in_score = in_score
        assert isinstance(outside_score, bool), repr(outside_score)
        self.outside_score = outside_score

    ### SPECIAL METHODS ###

    def __call__(self, method):
        r'''Calls command decorator on `method`.

        Returns `method` with command name metadatum attached.
        '''
        method.command_name = self.command_name
        if self.description is not None:
            method.description = self.description
        else:
            method.description = method.__name__.replace('_', ' ')
        method.section = self.section
        method.is_hidden = self.is_hidden
        method.is_navigation = self.section in self._navigation_section_names
        method.in_score = self.in_score
        method.outside_score = self.outside_score
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