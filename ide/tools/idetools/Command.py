import abjad
import string


class Command(abjad.AbjadObject):
    r'''Command decorator.
    '''

    ### CLASS VARIABLES ###

    known_sections = (
        'back cover',
        'build',
        'clipboard',
        'definition',
        'definitions',
        'files',
        'front cover',
        'git',
        'go',
        'hop',
        'log',
        'illustrate',
        'ly',
        'lys',
        'midi',
        'music',
        'package',
        'path',
        'pdf',
        'pdfs',
        'preface',
        'score',
        'shell',
        'show',
        'strings',
        'stylesheet',
        'tests',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        command_name,
        argument_name=None,
        description=None,
        directories=None,
        external=None,
        blacklist=(),
        section=None,
        scores=None,
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
        if external is not None:
            external = bool(external)
        self.external = external
        self.blacklist = blacklist
        if scores is not None:
            scores = bool(scores)
        self.scores = scores
        assert section in self.known_sections, repr(section)
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
        method.external = self.external
        method.blacklist = self.blacklist
        method.scores = self.scores
        method.section = self.section
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
