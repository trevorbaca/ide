# -*- encoding: utf-8 -*-
import os
from abjad import *
import ide
configuration = ide.tools.idetools.AbjadIDEConfiguration()
session = ide.tools.idetools.Session()
abjad_ide = ide.tools.idetools.AbjadIDE(is_test=True)


def test_AbjadIDE__find_up_to_date_path_01():
    r'''Finds up-to-date score package manger.
    '''

    wrangler = abjad_ide._initialize_wrangler('scores')
    path = wrangler._find_up_to_date_path(
        inside_score=False,
        system=True,
        )

    storehouse = configuration.abjad_ide_example_scores_directory

    assert abjad_ide._is_score_package_outer_path(path)
    assert abjad_ide._is_git_versioned(path)
    assert abjad_ide._is_up_to_date(path)
    assert path.startswith(storehouse)
    assert not path == storehouse


def test_AbjadIDE__find_up_to_date_path_02():
    r'''Finds up-to-date material package manager.
    '''

    wrangler = abjad_ide._initialize_wrangler('materials')
    path = wrangler._find_up_to_date_path(system=True)

    assert abjad_ide._is_material_package_path(path)
    assert abjad_ide._is_git_versioned(path)
    assert abjad_ide._is_up_to_date(path)
    assert os.path.basename(os.path.dirname(path)) == 'materials'
    assert not os.path.dirname(path) == 'materials'


def test_AbjadIDE__find_up_to_date_path_03():
    r'''Finds up-to-date segment package manager.
    '''

    wrangler = abjad_ide._initialize_wrangler('segments')
    path = wrangler._find_up_to_date_path(system=True)

    assert abjad_ide._is_segment_package_path(path)
    assert abjad_ide._is_git_versioned(path)
    assert abjad_ide._is_up_to_date(path)
    assert os.path.basename(os.path.dirname(path)) == 'segments'
    assert not os.path.basename(path) == 'segments'