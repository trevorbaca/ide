# -*- encoding: utf-8 -*-
import os
from abjad import *
import ide
abjad_ide = ide.idetools.AbjadIDE(is_test=True)


def test_PackageWrangler_remove_packages_01():
    r'''Removes one score package.
    '''

    outer_path = os.path.join(
        abjad_ide._configuration.user_score_packages_directory,
        'example_score_100',
        )
    inner_path = os.path.join(
        abjad_ide._configuration.user_score_packages_directory,
        'example_score_100',
        'example_score_100',
        )

    with systemtools.FilesystemState(remove=[outer_path, inner_path]):
        input_ = 'new example~score~100 y q'
        abjad_ide._run(input_=input_)
        assert os.path.exists(outer_path)
        manager = ide.idetools.ScorePackageManager
        manager = manager(path=inner_path, session=abjad_ide._session)
        title = 'Example Score 100'
        manager._add_metadatum('title', title)
        input_ = 'rm Example~Score~100 remove q'
        abjad_ide._run(input_=input_)
        assert not os.path.exists(outer_path)


def test_PackageWrangler_remove_packages_02():
    r'''Removes range of score packages.
    '''

    path_100_outer = os.path.join(
        abjad_ide._configuration.user_score_packages_directory,
        'example_score_100',
        'example_score_100',
        )
    path_100_inner = os.path.join(
        abjad_ide._configuration.user_score_packages_directory,
        'example_score_100',
        'example_score_100',
        )
    path_101_outer = os.path.join(
        abjad_ide._configuration.user_score_packages_directory,
        'example_score_101',
        'example_score_101',
        )
    path_101_inner = os.path.join(
        abjad_ide._configuration.user_score_packages_directory,
        'example_score_101',
        'example_score_101',
        )
    paths = [path_100_outer, path_100_inner, path_101_outer, path_101_inner]

    with systemtools.FilesystemState(remove=paths):
        input_ = 'new example~score~100 y q'
        abjad_ide._run(input_=input_)
        assert os.path.exists(path_100_outer)
        input_ = 'new example~score~101 y q'
        abjad_ide._run(input_=input_)
        assert os.path.exists(path_101_outer)
        manager = ide.idetools.ScorePackageManager
        manager = manager(path=path_100_inner, session=abjad_ide._session)
        title = 'Example Score 100'
        manager._add_metadatum('title', title)
        manager = ide.idetools.ScorePackageManager
        manager = manager(path=path_101_inner, session=abjad_ide._session)
        title = 'Example Score 101'
        manager._add_metadatum('title', title)
        input_ = 'rm Example~Score~100~-~Example~Score~101 remove~2 q'
        abjad_ide._run(input_=input_)
        assert not os.path.exists(path_100_outer)
        assert not os.path.exists(path_101_outer)