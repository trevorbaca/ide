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
        self._breadcrumb_callback = None
        self._path = path

    ### PRIVATE METHODS ###

    def _configure_as_material_package_manager(self):
        pass

    def _configure_as_score_package_manager(self):
        self._breadcrumb_callback = self._get_title_metadatum

    def _configure_as_segment_package_manager(self):
        self._breadcrumb_callback = self._get_name_metadatum