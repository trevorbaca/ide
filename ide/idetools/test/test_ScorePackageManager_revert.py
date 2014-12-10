# -*- encoding: utf-8 -*-
import os
from abjad import *
import abjad_ide
abjad_ide = abjad_ide.idetools.AbjadIDE(is_test=True)


def test_ScorePackageManager_revert_01():

    manager = abjad_ide._score_package_wrangler._find_up_to_date_manager(
        repository='git',
        system=True,
        )

    assert manager._test_revert()


def test_ScorePackageManager_revert_02():

    manager = abjad_ide._score_package_wrangler._find_up_to_date_manager(
        repository='svn',
        system=False,
        )

    if not manager:
        return

    assert manager._test_revert()