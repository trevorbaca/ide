# -*- encoding: utf -*-
from ide.tools.idetools.Command import Command


class Controller(object):
    r'''Controller.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_session',
        )

    ### INTIIALIZER ###

    def __init__(self, session=None):
        from ide.tools import idetools
        self._session = session or idetools.Session()