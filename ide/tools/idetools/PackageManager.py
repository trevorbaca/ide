# -*- encoding: utf-8 -*-
from __future__ import print_function
import os
from ide.tools.idetools.AbjadIDEConfiguration import AbjadIDEConfiguration
from ide.tools.idetools.Controller import Controller
from ide.tools.idetools.Command import Command
configuration = AbjadIDEConfiguration()


class PackageManager(Controller):
    r'''Package manager.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_optional_directories',
        '_optional_files',
        '_package_creation_callback',
        '_path',
        '_required_directories',
        '_required_files',
        )

    _directory_name_to_package_contents = {
        'materials': {
            'optional_directories': (
                '__pycache__',
                'test',
                ),
            'optional_files': (
                '__illustrate__.py',
                'illustration.ly',
                'illustration.pdf',
                'maker.py',
                ),
            'required_directories': (),
            'required_files': (
                '__init__.py',
                '__metadata__.py',
                'definition.py',
                ),
            },
        'score': {
            'optional_directories': (
                '__pycache__',
                'etc',
                'test',
                ),
            'optional_files': (),
            'required_directories': (
                'build',
                'distribution',
                'makers',
                'materials',
                'segments',
                'stylesheets',
                ),
            'required_files': (
                '__init__.py',
                '__metadata__.py',
                os.path.join('makers', '__init__.py'),
                os.path.join('materials', '__init__.py'),
                os.path.join('segments', '__init__.py'),
                ),
            },
        'segments': {
            'optional_directories': (
                '__pycache__',
                'test',
                ),
            'optional_files': (
                'illustration.ly',
                'illustration.pdf',
                ),
            'required_directories': (),
            'required_files': (
                '__init__.py',
                '__metadata__.py',
                'definition.py',
                ),
            },
        }

    ### INITIALIZER ###

    def __init__(self, path=None, session=None):
        assert session is not None
        assert path is not None and os.path.sep in path
        superclass = super(PackageManager, self)
        superclass.__init__(session=session)
        self._breadcrumb_callback = None
        self._optional_directories = (
            '__pycache__',
            'test',
            )
        self._optional_files = ()
        self._package_creation_callback = None
        self._path = path
        self._required_directories = ()
        self._required_files = (
            '__init__.py',
            '__metadata__.py',
            )

    ### PRIVATE METHODS ###

    def _configure_as_material_package_manager(self):
        self._optional_files = (
            '__illustrate__.py',
            'illustration.ly',
            'illustration.pdf',
            'maker.py',
            )
        self._required_files = (
            '__init__.py',
            '__metadata__.py',
            'definition.py',
            )

    def _configure_as_score_package_manager(self):
        self._breadcrumb_callback = self._get_title_metadatum
        self._optional_directories = (
            '__pycache__',
            'etc',
            'test',
            )
        self._package_creation_callback = \
            self._make_score_into_installable_package
        self._required_directories = (
            'build',
            'distribution',
            'makers',
            'materials',
            'segments',
            'stylesheets',
            )
        self._required_files = (
            '__init__.py',
            '__metadata__.py',
            os.path.join('makers', '__init__.py'),
            os.path.join('materials', '__init__.py'),
            os.path.join('segments', '__init__.py'),
            )

    def _configure_as_segment_package_manager(self):
        self._breadcrumb_callback = self._get_name_metadatum
        self._optional_files = (
            'illustration.ly',
            'illustration.pdf',
            )
        self._required_files = (
            '__init__.py',
            '__metadata__.py',
            'definition.py',
            )