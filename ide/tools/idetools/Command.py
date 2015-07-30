# -*- encoding: utf-8 -*-


class Command(object):
    r'''Command decorator.
    '''

    def __init__(self, command):
        assert isinstance(command, str), repr(command)
        self.command = command

    def __call__(self, method):
        method.command = self.command
        return method