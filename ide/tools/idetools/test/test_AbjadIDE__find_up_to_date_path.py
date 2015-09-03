# -*- encoding: utf-8 -*-
import os
from abjad import *
import ide
configuration = ide.tools.idetools.AbjadIDEConfiguration()
session = ide.tools.idetools.Session()
abjad_ide = ide.tools.idetools.AbjadIDE(is_test=True)


def test_AbjadIDE__find_up_to_date_path_01():
    r'''Finds up-to-date score package path.
    '''

    path = abjad_ide._find_up_to_date_path(
        'scores',
        inside_score=False,
        system=True,
        )

    scores_directory = configuration.abjad_ide_example_scores_directory

    assert abjad_ide._is_score_package_outer_path(path)
    assert abjad_ide._is_git_versioned(path)
    assert abjad_ide._is_up_to_date(path)
    assert path.startswith(scores_directory)
    assert not path == scores_directory


def test_AbjadIDE__find_up_to_date_path_02():
    r'''Finds up-to-date material package path.
    '''

    path = abjad_ide._find_up_to_date_path('materials', system=True)

    assert abjad_ide._is_material_package_path(path)
    assert abjad_ide._is_git_versioned(path)
    assert abjad_ide._is_up_to_date(path)
    assert os.path.basename(os.path.dirname(path)) == 'materials'
    assert not os.path.dirname(path) == 'materials'


def test_AbjadIDE__find_up_to_date_path_03():
    r'''Finds up-to-date segment package path.
    '''

    path = abjad_ide._find_up_to_date_path('segments', system=True)

    assert abjad_ide._is_segment_package_path(path)
    assert abjad_ide._is_git_versioned(path)
    assert abjad_ide._is_up_to_date(path)
    assert os.path.basename(os.path.dirname(path)) == 'segments'
    assert not os.path.basename(path) == 'segments'