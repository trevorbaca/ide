# -*- encoding: utf-8 -*-
import os
from ide.idetools.PackageManager import PackageManager


class MaterialPackageManager(PackageManager):
    r'''Material package manager.
    '''

    ### INTIALIZER ###

    def __init__(self, path=None, session=None):
        superclass = super(MaterialPackageManager, self)
        superclass.__init__(path=path, session=session)
        self._basic_breadcrumb = 'MATERIALS'
        self._optional_files = (
            '__illustrate__.py',
            'illustration.ly',
            'illustration.pdf',
            'maker.py',
            )
        commands = []
        commands.append(('check package', 'ck'))
        commands.append(('definition.py - check', 'dc'))
        commands.append(('definition.py - edit', 'de'))
        commands.append(('next package', '>'))
        commands.append(('previous package', '<'))
        string = '__illustrate__.py - edit'
        commands.append((string, 'le'))
        string = '__illustrate__.py - stub'
        commands.append((string, 'ls'))
        commands.append(('illustration.ly - interpret', 'ii'))
        commands.append(('illustration.ly - edit', 'ie'))
        commands.append(('illustration.pdf - open', 'io'))
        self._other_commands = commands
        self._required_files = (
            '__init__.py',
            '__metadata__.py',
            'definition.py',
            )