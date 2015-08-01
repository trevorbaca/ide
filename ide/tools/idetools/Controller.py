# -*- encoding: utf -*-
from ide.tools.idetools.Command import Command


class Controller(object):
    r'''Controller.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_configuration',
        '_io_manager',
        '_session',
        )

    ### INTIIALIZER ###

    def __init__(self, session=None):
        from ide.tools import idetools
        self._configuration = idetools.AbjadIDEConfiguration()
        self._session = session or idetools.Session()
        self._io_manager = idetools.IOManager(
            client=self,
            session=self._session,
            )

    ### SPECIAL METHODS ###

    def __repr__(self):
        r'''Gets interpreter representation of controller.

        Returns string.
        '''
        return '{}()'.format(type(self).__name__)