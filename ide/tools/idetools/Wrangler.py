# -*- encoding: utf-8 -*-
from ide.tools.idetools.Controller import Controller


class Wrangler(Controller):
    r'''Wrangler.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_directory_name',
        )

    ### INITIALIZER ###

    def __init__(self, session=None, io_manager=None):
        assert session is not None
        assert io_manager is not None
        superclass = super(Wrangler, self)
        superclass.__init__(session=session, io_manager=io_manager)
        self._directory_name = None