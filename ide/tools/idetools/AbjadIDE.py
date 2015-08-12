# -*- encoding: utf-8 -*-
from ide.tools.idetools.Controller import Controller


class AbjadIDE(Controller):
    r'''Abjad IDE.

    ..  container:: example

        ::

            >>> ide.tools.idetools.AbjadIDE(is_test=True)
            AbjadIDE()

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        )

    ### INITIALIZER ###

    def __init__(self, session=None, is_test=False):
        from ide.tools import idetools
        if session is None:
            session = idetools.Session()
            session._is_test = is_test
        io_manager = idetools.IOManager(session=session)
        superclass = super(AbjadIDE, self)
        superclass.__init__(session=session, io_manager=io_manager)