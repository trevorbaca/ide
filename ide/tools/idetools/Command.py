# -*- encoding: utf-8 -*-


class Command(object):
    r'''Command decorator.
    '''

    def __init__(self, command_name):
        assert isinstance(command_name, str), repr(command_name)
        assert command_name.islower(), repr(command_name)
        self.command_name = command_name

    def __call__(self, method):
        r'''Calls command decorator on `method`.

        Returns `method` with command name metadatum attached.
        '''
        method.command_name = self.command_name
        return method