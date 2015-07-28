# -*- encoding: utf-8 -*-
import os
from ide.idetools.PackageManager import PackageManager


class ScorePackageManager(PackageManager):
    r'''Score package manager.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        )

    ### INITIALIZER ###

    def __init__(self, path=None, session=None):
        superclass = super(ScorePackageManager, self)
        superclass.__init__(path=path, session=session)
        self._annotate_year = True
        self._asset_identifier = 'score package manager'
        self._breadcrumb_callback = self._get_title
        self._directory_names = (
            'build',
            'distribution',
            'etc',
            'makers',
            'materials',
            'segments',
            'stylesheets',
            )
        self._include_asset_name = False
        self._optional_directories = (
            '__pycache__',
            'etc',
            'test',
            )
        commands = []
        commands.append(('check package', 'ck'))
        commands.append(('open score.pdf', 'so'))
        self._other_commands = commands
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