# -*- encoding: utf-8 -*-
import os
from abjad import *
import ide
configuration = ide.idetools.Configuration()
session = ide.idetools.Session()
abjad_ide = ide.idetools.AbjadIDE(is_test=True)


def test_PackageWrangler__find_up_to_date_manager_01():
    r'''Works with Git.
    '''

    wrangler = abjad_ide._score_package_wrangler
    manager = wrangler._find_up_to_date_manager(
        inside_score=False,
        system=True,
        repository='git',
        )

    storehouse = configuration.example_score_packages_directory

    assert isinstance(manager, ide.idetools.ScorePackageManager)
    assert manager._is_git_versioned()
    assert manager._is_up_to_date()
    assert manager._path.startswith(storehouse)
    assert not manager._path == storehouse