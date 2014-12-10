# -*- encoding: utf-8 -*-
import os
from abjad import *
import ide
ide = ide.idetools.AbjadIDE(is_test=True)


def test_ScorePackageManager_remove_unadded_assets_01():

    wrangler = ide._score_package_wrangler
    manager = wrangler._find_git_manager()

    assert manager._test_remove_unadded_assets()


def test_ScorePackageManager_remove_unadded_assets_02():

    wrangler = ide._score_package_wrangler
    manager = wrangler._find_svn_manager()

    if not manager:
        return

    assert manager._test_remove_unadded_assets()