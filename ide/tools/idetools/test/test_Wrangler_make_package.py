# -*- encoding: utf-8 -*-
import os
from abjad import *
import ide
abjad_ide = ide.tools.idetools.AbjadIDE(is_test=True)


def test_Wrangler_make_package_01():
    r'''Makes score package.
    '''

    outer_path = os.path.join(
        abjad_ide._configuration.scores_directory,
        'example_score',
        )
    inner_path = os.path.join(outer_path, 'example_score')
    outer_directory_entries = [
        'README.md',
        'requirements.txt',
        'setup.cfg',
        'setup.py',
        ]
    inner_directory_entries = [
        '__init__.py',
        '__metadata__.py',
        'build',
        'distribution',
        'makers',
        'materials',
        'segments',
        'stylesheets',
        ]

    with systemtools.FilesystemState(remove=[outer_path]):
        input_ = 'new Example~Score y q'
        abjad_ide._run(input_=input_)
        contents = abjad_ide._transcript.contents
        assert os.path.exists(outer_path)
        session = ide.tools.idetools.Session(is_test=True)
        manager = ide.tools.idetools.PackageManager(
            path=inner_path,
            session=session,
            )
        assert manager._list() == inner_directory_entries
        for file_name in outer_directory_entries:
            path = os.path.join(outer_path, file_name)
            assert os.path.exists(path)

    assert 'Enter title]> Example Score' in contents


def test_Wrangler_make_package_02():
    r'''Accepts flexible package name input for score packages.
    '''

    score_package = os.path.join(
        abjad_ide._configuration.scores_directory,
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


def test_Wrangler_make_package_03():
    r'''Creates material package.
    '''

    session = ide.tools.idetools.Session(is_test=True)
    configuration = abjad_ide._configuration
    path = os.path.join(
        abjad_ide._configuration.example_scores_directory,
        'red_example_score',
        'red_example_score',
        'materials',
        'testnotes',
        )
    directory_entries = [
        '__init__.py',
        '__metadata__.py',
        'definition.py',
        ]

    with systemtools.FilesystemState(remove=[path]):
        input_ = 'mm new Red~Example~Score testnotes y q'
        abjad_ide._run(input_=input_)
        assert os.path.exists(path)
        session = ide.tools.idetools.Session(is_test=True)
        manager = ide.tools.idetools.PackageManager(path=path, session=session)
        assert manager._list() == directory_entries


def test_Wrangler_make_package_04():
    r'''Makes segment package.
    '''

    path = os.path.join(
        abjad_ide._configuration.example_scores_directory,
        'red_example_score',
        'red_example_score',
        'segments',
        'segment_04',
        )
    directory_entries = [
        '__init__.py',
        '__metadata__.py',
        'definition.py',
        ]

    with systemtools.FilesystemState(remove=[path]):
        input_ = 'red~example~score g new segment~04 y q'
        abjad_ide._run(input_=input_)
        contents = abjad_ide._transcript.contents
        assert os.path.exists(path)
        session = ide.tools.idetools.Session(is_test=True)
        manager = ide.tools.idetools.PackageManager
        manager = manager(path=path, session=session)
        assert manager._list() == directory_entries