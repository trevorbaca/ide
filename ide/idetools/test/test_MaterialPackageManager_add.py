# -*- encoding: utf-8 -*-
import os
from abjad import *
import ide
abjad_ide = ide.idetools.AbjadIDE(is_test=True)


def test_MaterialPackageManager_add_01():
    r'''Add two files to Git-managed material package.
    Make sure Git recognizes the files as added.
    Then unadd the files and leave the material package as found.
    '''

    wrangler = abjad_ide._material_package_wrangler
    manager = wrangler._find_up_to_date_manager(
        repository='git',
        system=True,
        )

    assert manager._test_add()