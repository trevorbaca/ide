# -*- coding: utf-8 -*-
import os
from abjad import *
import ide
abjad_ide = ide.tools.idetools.AbjadIDE(is_test=True)
configuration = ide.tools.idetools.AbjadIDEConfiguration()


def test_AbjadIDE_remove_01():
    r'''Removes one score package.
    '''

    outer_path = os.path.join(
        configuration.composer_scores_directory,
        'example_score_100',
        )
    inner_path = os.path.join(
        configuration.composer_scores_directory,
        'example_score_100',
        'example_score_100',
        )

    with systemtools.FilesystemState(remove=[outer_path, inner_path]):
        input_ = 'new example~score~100 q'
        abjad_ide._run_main_menu(input_=input_)
        assert os.path.exists(outer_path)
        title = 'Example Score 100'
        abjad_ide._add_metadatum(
            inner_path,
            'title',
            title,
            )
        input_ = 'rm Example~Score~100 remove q'
        abjad_ide._run_main_menu(input_=input_)
        assert not os.path.exists(outer_path)


def test_AbjadIDE_remove_02():
    r'''Removes range of score packages.
    '''

    path_100_outer = os.path.join(
        configuration.composer_scores_directory,
        'example_score_100',
        'example_score_100',
        )
    path_100_inner = os.path.join(
        configuration.composer_scores_directory,
        'example_score_100',
        'example_score_100',
        )
    path_101_outer = os.path.join(
        configuration.composer_scores_directory,
        'example_score_101',
        'example_score_101',
        )
    path_101_inner = os.path.join(
        configuration.composer_scores_directory,
        'example_score_101',
        'example_score_101',
        )
    paths = [path_100_outer, path_100_inner, path_101_outer, path_101_inner]

    with systemtools.FilesystemState(remove=paths):
        input_ = 'new example~score~100 q'
        abjad_ide._run_main_menu(input_=input_)
        assert os.path.exists(path_100_outer)
        input_ = 'new example~score~101 q'
        abjad_ide._run_main_menu(input_=input_)
        assert os.path.exists(path_101_outer)
        title = 'Example Score 100'
        abjad_ide._add_metadatum(
            path_100_inner,
            'title',
            title,
            )
        title = 'Example Score 101'
        abjad_ide._add_metadatum(
            path_101_inner,
            'title',
            title,
            )
        input_ = 'rm Example~Score~100~-~Example~Score~101 remove~2 q'
        abjad_ide._run_main_menu(input_=input_)
        assert not os.path.exists(path_100_outer)
        assert not os.path.exists(path_101_outer)