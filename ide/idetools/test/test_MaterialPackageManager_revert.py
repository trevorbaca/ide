# -*- encoding: utf-8 -*-
import os
from abjad import *
import abjad_ide
abjad_ide = abjad_ide.idetools.AbjadIDE(is_test=True)


def test_MaterialPackageManager_revert_01():

    wrangler = abjad_ide._material_package_wrangler
    manager = wrangler._find_up_to_date_manager(
        repository='git',
        system=True,
        )

    assert manager._test_revert()


def test_MaterialPackageManager_revert_02():

    wrangler = abjad_ide._material_package_wrangler
    manager = wrangler._find_up_to_date_manager(
        repository='svn',
        system=False,
        )

    if not manager:
        return

    assert manager._test_revert()