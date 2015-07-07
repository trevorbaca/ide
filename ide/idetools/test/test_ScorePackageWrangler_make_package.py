# -*- encoding: utf-8 -*-
import os
from abjad import *
import ide
abjad_ide = ide.idetools.AbjadIDE(is_test=True)


def test_ScorePackageWrangler_make_package_01():
    r'''Makes score package.
    '''

    path = os.path.join(
        abjad_ide._configuration.user_score_packages_directory,
        'example_score',
        'example_score',
        )
    directory_entries = [
        '__init__.py',
        '__metadata__.py',
        'build',
        'distribution',
        'makers',
        'materials',
        'segments',
        'stylesheets',
        ]

    with systemtools.FilesystemState(remove=[path]):
        input_ = 'new example~score y q'
        abjad_ide._run(input_=input_)
        contents = abjad_ide._transcript.contents
        assert os.path.exists(path)
        session = ide.idetools.Session(is_test=True)
        manager = ide.idetools.ScorePackageManager
        manager = manager(path=path, session=session)
        assert manager._list() == directory_entries

    assert 'Enter score package name]>' in contents


def test_ScorePackageWrangler_make_package_02():
    r'''Accepts flexible package name input.
    '''

    score_package = os.path.join(
        abjad_ide._configuration.user_score_packages_directory,
        'example_score_1',
        )

    with systemtools.FilesystemState(remove=[score_package]):
        input_ = 'new ExampleScore1 y q'
        abjad_ide._run(input_=input_)
        assert os.path.exists(score_package)

    with systemtools.FilesystemState(remove=[score_package]):
        input_ = 'new exampleScore1 y q'
        abjad_ide._run(input_=input_)
        assert os.path.exists(score_package)

    with systemtools.FilesystemState(remove=[score_package]):
        input_ = 'new EXAMPLE_SCORE_1 y q'
        abjad_ide._run(input_=input_)
        assert os.path.exists(score_package)

    with systemtools.FilesystemState(remove=[score_package]):
        input_ = 'new example_score_1 y q'
        abjad_ide._run(input_=input_)
        assert os.path.exists(score_package)