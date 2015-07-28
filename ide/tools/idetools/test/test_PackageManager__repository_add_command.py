# -*- encoding: utf-8 -*-
import os
from abjad import *
import ide
abjad_ide = ide.tools.idetools.AbjadIDE(is_test=True)


def test_PackageManager__repository_add_command_01():

    manager = abjad_ide._score_package_wrangler._find_up_to_date_manager(
        system=True,
        )

    command = 'git add -A {}'.format(manager._path)
    assert manager._repository_add_command == command