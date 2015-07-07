# -*- encoding: utf-8 -*-
import os
from abjad import *
import ide
abjad_ide = ide.idetools.AbjadIDE(is_test=True)


def test_ScorePackageManager_remove_unadded_assets_01():

    wrangler = abjad_ide._score_package_wrangler
    manager = wrangler._find_git_manager()

    assert manager._test_remove_unadded_assets()