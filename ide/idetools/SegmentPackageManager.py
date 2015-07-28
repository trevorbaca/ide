# -*- encoding: utf-8 -*-
import os
import shutil
from abjad.tools import systemtools
from ide.idetools.PackageManager import PackageManager


class SegmentPackageManager(PackageManager):
    r'''Segment package manager.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        )

    ### INITIALIZER ###

    def __init__(self, path=None, session=None):
        superclass = super(SegmentPackageManager, self)
        superclass.__init__(path=path, session=session)
        self._basic_breadcrumb = 'SEGMENTS'
        self._breadcrumb_callback = self._get_name_metadatum
        self._optional_files = (
            'illustration.ly',
            'illustration.pdf',
            )
        commands = []
        commands.append(('check package', 'ck'))
        commands.append(('illustration.ly - edit', 'ie'))
        commands.append(('illustration.ly - interpret', 'ii'))
        commands.append(('definition.py - check', 'dc'))
        commands.append(('definition.py - edit', 'de'))
        commands.append(('definition.py - illustrate', 'i'))
        commands.append(('illustration.pdf - open', 'o'))
        commands.append(('next package', '>'))
        commands.append(('previous package', '<'))
        self._other_commands = commands
        self._required_files = (
            '__init__.py',
            '__metadata__.py',
            'definition.py',
            )