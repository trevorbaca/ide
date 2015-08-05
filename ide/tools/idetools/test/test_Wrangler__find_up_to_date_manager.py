# -*- encoding: utf-8 -*-
import os
from abjad import *
import ide
configuration = ide.tools.idetools.AbjadIDEConfiguration()
session = ide.tools.idetools.Session()
abjad_ide = ide.tools.idetools.AbjadIDE(is_test=True)


def test_Wrangler__find_up_to_date_manager_01():
    r'''Finds up-to-date score package manger.
    '''

    wrangler = abjad_ide._score_package_wrangler
    manager = wrangler._find_up_to_date_manager(
        inside_score=False,
        system=True,
        )

    storehouse = configuration.abjad_ide_example_scores_directory

    assert isinstance(manager, ide.tools.idetools.PackageManager)
    assert manager._basic_breadcrumb == 'SCORES'
    assert manager._is_git_versioned(manager._session, manager._path)
    assert manager._is_up_to_date(manager._session, manager._path)
    assert manager._path.startswith(storehouse)
    assert not manager._path == storehouse


def test_Wrangler__find_up_to_date_manager_02():
    r'''Finds up-to-date material package manager.
    '''

    wrangler = abjad_ide._material_package_wrangler
    manager = wrangler._find_up_to_date_manager(
        system=True,
        )

    assert isinstance(manager, ide.tools.idetools.PackageManager)
    assert manager._basic_breadcrumb == 'MATERIALS'
    assert manager._is_git_versioned(manager._session, manager._path)
    assert manager._is_up_to_date(manager._session, manager._path)
    assert os.path.basename(os.path.dirname(manager._path)) == 'materials'
    assert not os.path.dirname(manager._path) == 'materials'


def test_Wrangler__find_up_to_date_manager_03():
    r'''Finds up-to-date segment package manager.
    '''

    wrangler = abjad_ide._segment_package_wrangler
    manager = wrangler._find_up_to_date_manager(
        system=True,
        )

    assert isinstance(manager, ide.tools.idetools.PackageManager)
    assert manager._basic_breadcrumb == 'SEGMENTS'
    assert manager._is_git_versioned(manager._session, manager._path)
    assert manager._is_up_to_date(manager._session, manager._path)
    assert os.path.basename(os.path.dirname(manager._path)) == 'segments'
    assert not os.path.basename(manager._path) == 'segments'