# -*- encoding: utf-8 -*-
import os
from abjad import *
import ide
abjad_ide = abjad_ide.idetools.AbjadIDE(is_test=True)


def test_SegmentPackageWrangler__find_up_to_date_manager_01():
    r'''Works with Git.
    '''

    wrangler = abjad_ide._segment_package_wrangler
    manager = wrangler._find_up_to_date_manager(
        repository='git',
        system=True,
        )

    assert isinstance(manager, abjad_ide.idetools.SegmentPackageManager)
    assert manager._is_git_versioned()
    assert manager._is_up_to_date()
    assert os.path.basename(os.path.dirname(manager._path)) == 'segments'
    assert not os.path.basename(manager._path) == 'segments'


def test_SegmentPackageWrangler__find_up_to_date_manager_02():
    r'''Works with Subversion.
    '''

    wrangler = abjad_ide._segment_package_wrangler
    manager = wrangler._find_up_to_date_manager(
        system=False,
        repository='svn',
        )

    if not manager:
        return

    assert isinstance(manager, abjad_ide.idetools.SegmentPackageManager)
    assert manager._is_svn_versioned()
    assert manager._is_up_to_date()
    assert os.path.basename(os.path.dirname(manager._path)) == 'segments'
    assert not os.path.basename(manager._path) == 'segments'