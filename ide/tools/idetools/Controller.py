# -*- encoding: utf -*-
import inspect
from abjad.tools import stringtools
from ide.tools.idetools.Command import Command


class Controller(object):
    r'''Controller.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_configuration',
        '_controller_commands',
        '_io_manager',
        '_session',
        '_transcript',
        )

    ### INTIIALIZER ###

    def __init__(self, session=None):
        from ide.tools import idetools
        self._configuration = idetools.AbjadIDEConfiguration()
        self._controller_commands = []
        self._session = session or idetools.Session()
        self._io_manager = idetools.IOManager(
            client=self,
            session=self._session,
            )
        self._transcript = self._session.transcript

    ### SPECIAL METHODS ###

    def __repr__(self):
        r'''Gets interpreter representation of controller.

        Returns string.
        '''
        return '{}()'.format(type(self).__name__)

    ### PRIVATE PROPERTIES ###

    @property
    def _command_name_to_method(self):
        result = {}
        methods = self._get_decorated_methods()
        for method in methods:
            result[method.command_name] = method
        return result

    @property
    def _spaced_class_name(self):
        return stringtools.to_space_delimited_lowercase(type(self).__name__)

    ### PRIVATE METHODS ###

    def _get_decorated_methods(self, only_my_methods=False):
        result = []
        for name in dir(self):
            if not name.startswith('_'):
                value = getattr(self, name)
                if inspect.ismethod(value):
                    if hasattr(value, 'command_name'):
                        if not only_my_methods:
                            result.append(value)
                        elif value in self._controller_commands:
                            result.append(value)
        return result