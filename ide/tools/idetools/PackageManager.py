# -*- encoding: utf-8 -*-
from __future__ import print_function
import os
from ide.tools.idetools.Controller import Controller


class PackageManager(Controller):
    r'''Package manager.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_path',
        )

    ### INITIALIZER ###

    def __init__(self, path=None, session=None):
        assert session is not None
        assert path is not None and os.path.sep in path
        superclass = super(PackageManager, self)
        superclass.__init__(session=session)
        self._path = path