# -*- encoding: utf-8 -*-
import os
from abjad import *
import ide
abjad_ide = abjad_ide.idetools.AbjadIDE(is_test=True)


def test_SegmentPackageManager_revert_01():

    wrangler = abjad_ide._segment_package_wrangler
    manager = wrangler._find_git_manager(must_have_file=True)

    assert manager._test_revert()


def test_SegmentPackageManager_revert_02():

    wrangler = abjad_ide._segment_package_wrangler
    manager = wrangler._find_svn_manager(must_have_file=True)

    if not manager:
        return

    assert manager._test_revert()