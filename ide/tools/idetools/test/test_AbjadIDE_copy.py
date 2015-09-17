# -*- coding: utf-8 -*-
import os
from abjad import *
import ide
abjad_ide = ide.tools.idetools.AbjadIDE(is_test=True)
configuration = ide.tools.idetools.AbjadIDEConfiguration()
scores_directory = configuration.abjad_ide_example_scores_directory


def test_AbjadIDE_copy_external_asset_01():
    r'''Copies file between build directories.
    '''

    source_file = os.path.join(
        scores_directory,
        'red_example_score',
        'red_example_score',
        'build',
        'front-cover.tex',
        )
    target_file = os.path.join(
        scores_directory,
        'blue_example_score',
        'blue_example_score',
        'build',
        'front-cover.tex',
        )

    with systemtools.FilesystemState(keep=[scores_directory]):
        assert not os.path.exists(target_file)
        input_ = 'Blue~Example~Score u cp'
        input_ += ' {}'.format(source_file)
        input_ += ' y q'
        abjad_ide._run_main_menu(input_=input_)
        assert os.path.exists(target_file)


def test_AbjadIDE_copy_external_asset_02():
    r'''Copies file between distribution directories.
    '''

    source_file = os.path.join(
        scores_directory,
        'red_example_score',
        'red_example_score',
        'distribution',
        'red-example-score-score.pdf',
        )
    target_file = os.path.join(
        scores_directory,
        'blue_example_score',
        'blue_example_score',
        'distribution',
        'red-example-score-score.pdf',
        )

    with systemtools.FilesystemState(keep=[scores_directory]):
        assert not os.path.exists(target_file)
        input_ = 'Blue~Example~Score d cp'
        input_ += ' {}'.format(source_file)
        input_ += ' y q'
        abjad_ide._run_main_menu(input_=input_)
        assert os.path.exists(target_file)


def test_AbjadIDE_copy_external_asset_03():
    r'''Copies file between etc directories.
    '''

    source_file = os.path.join(
        scores_directory,
        'red_example_score',
        'red_example_score',
        'etc',
        'notes.txt',
        )
    target_file = os.path.join(
        scores_directory,
        'blue_example_score',
        'blue_example_score',
        'etc',
        'notes.txt',
        )

    with systemtools.FilesystemState(keep=[scores_directory]):
        assert not os.path.exists(target_file)
        input_ = 'Blue~Example~Score c cp'
        input_ += ' {}'.format(source_file)
        input_ += ' y q'
        abjad_ide._run_main_menu(input_=input_)
        assert os.path.exists(target_file)


def test_AbjadIDE_copy_external_asset_04():
    r'''Copies file between makers directories.
    '''

    source_file = os.path.join(
        scores_directory,
        'red_example_score',
        'red_example_score',
        'makers',
        'ScoreTemplate.py',
        )
    target_file = os.path.join(
        scores_directory,
        'blue_example_score',
        'blue_example_score',
        'makers',
        'ScoreTemplate.py',
        )

    with systemtools.FilesystemState(keep=[scores_directory]):
        assert not os.path.exists(target_file)
        input_ = 'Blue~Example~Score k cp'
        input_ += ' {}'.format(source_file)
        input_ += ' y q'
        abjad_ide._run_main_menu(input_=input_)
        assert os.path.exists(target_file)


def test_AbjadIDE_copy_external_asset_05():
    r'''Copies file between material directories.
    '''

    source_file = os.path.join(
        scores_directory,
        'red_example_score',
        'red_example_score',
        'materials',
        'magic_numbers',
        'definition.py',
        )
    target_file = os.path.join(
        scores_directory,
        'blue_example_score',
        'blue_example_score',
        'materials',
        'articulation_handler',
        'definition.py',
        )

    with systemtools.FilesystemState(keep=[scores_directory]):
        os.remove(target_file)
        assert not os.path.exists(target_file)
        input_ = 'Blue~Example~Score m articulation~handler cp'
        input_ += ' {}'.format(source_file)
        input_ += ' y q'
        abjad_ide._run_main_menu(input_=input_)
        assert os.path.exists(target_file)


def test_AbjadIDE_copy_external_asset_06():
    r'''Copies package between materials directories.
    '''

    source_package = os.path.join(
        scores_directory,
        'red_example_score',
        'red_example_score',
        'materials',
        'magic_numbers',
        )
    source_package = os.path.normpath(source_package)
    target_package = os.path.join(
        scores_directory,
        'blue_example_score',
        'blue_example_score',
        'materials',
        'magic_numbers',
        )

    with systemtools.FilesystemState(keep=[scores_directory]):
        assert os.path.isdir(source_package)
        assert not os.path.exists(target_package)
        input_ = 'Blue~Example~Score m cp'
        input_ += ' {}'.format(source_package)
        input_ += ' y q'
        abjad_ide._run_main_menu(input_=input_)
        assert os.path.exists(target_package)


def test_AbjadIDE_copy_external_asset_07():
    r'''Copies file between segment directories.
    '''

    source_file = os.path.join(
        scores_directory,
        'red_example_score',
        'red_example_score',
        'segments',
        'segment_01',
        'definition.py',
        )
    target_file = os.path.join(
        scores_directory,
        'blue_example_score',
        'blue_example_score',
        'segments',
        'segment_01',
        'definition.py',
        )

    with systemtools.FilesystemState(keep=[scores_directory]):
        os.remove(target_file)
        assert not os.path.exists(target_file)
        input_ = 'Blue~Example~Score g segment~01 cp'
        input_ += ' {}'.format(source_file)
        input_ += ' y q'
        abjad_ide._run_main_menu(input_=input_)
        assert os.path.exists(target_file)


def test_AbjadIDE_copy_external_asset_08():
    r'''Copies package between segments directories.
    '''

    source_package = os.path.join(
        scores_directory,
        'red_example_score',
        'red_example_score',
        'segments',
        'segment_03',
        )
    source_package = os.path.normpath(source_package)
    target_package = os.path.join(
        scores_directory,
        'blue_example_score',
        'blue_example_score',
        'segments',
        'segment_03',
        )

    with systemtools.FilesystemState(keep=[scores_directory]):
        assert os.path.isdir(source_package)
        assert not os.path.exists(target_package)
        input_ = 'Blue~Example~Score g cp'
        input_ += ' {}'.format(source_package)
        input_ += ' y q'
        abjad_ide._run_main_menu(input_=input_)
        assert os.path.exists(target_package)


def test_AbjadIDE_copy_external_asset_09():
    r'''Copies file between stylesheets directories.
    '''

    source_file = os.path.join(
        scores_directory,
        'red_example_score',
        'red_example_score',
        'stylesheets',
        'stylesheet.ily',
        )
    target_file = os.path.join(
        scores_directory,
        'blue_example_score',
        'blue_example_score',
        'stylesheets',
        'stylesheet.ily',
        )

    with systemtools.FilesystemState(keep=[scores_directory]):
        assert not os.path.exists(target_file)
        input_ = 'Blue~Example~Score y cp'
        input_ += ' {}'.format(source_file)
        input_ += ' y q'
        abjad_ide._run_main_menu(input_=input_)
        assert os.path.exists(target_file)


def test_AbjadIDE_copy_external_asset_10():
    r'''Copies file between test directories.
    '''

    source_file = os.path.join(
        scores_directory,
        'red_example_score',
        'red_example_score',
        'test',
        'test_import.py',
        )
    target_file = os.path.join(
        scores_directory,
        'blue_example_score',
        'blue_example_score',
        'test',
        'test_import.py',
        )

    with systemtools.FilesystemState(keep=[scores_directory]):
        assert not os.path.exists(target_file)
        input_ = 'Blue~Example~Score t cp'
        input_ += ' {}'.format(source_file)
        input_ += ' y q'
        abjad_ide._run_main_menu(input_=input_)
        assert os.path.exists(target_file)