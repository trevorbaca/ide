# -*- encoding: utf-8 -*-
import os
from abjad import *
import ide
abjad_ide = ide.idetools.AbjadIDE(is_test=True)


def test_SegmentPackageManager_add_01():
    r'''Add two files to Git-managed segment package.
    Make sure Git recognizes the files as added.
    Then unadd the files and leave the segment package as found.
    '''

    wrangler = abjad_ide._segment_package_wrangler
    manager = wrangler._find_git_manager()

    assert manager._test_add()