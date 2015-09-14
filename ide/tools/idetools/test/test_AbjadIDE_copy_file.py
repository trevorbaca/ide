# -*- coding: utf-8 -*-
import os
from abjad import *
import ide
abjad_ide = ide.tools.idetools.AbjadIDE(is_test=True)
configuration = ide.tools.idetools.AbjadIDEConfiguration()
scores_directory = configuration.abjad_ide_example_scores_directory


def test_AbjadIDE_copy_file_01():
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
        input_ = 'Blue~Example~Score u from'
        input_ += ' {}'.format(source_file)
        input_ += ' y q'
        abjad_ide._run_main_menu(input_=input_)
        assert os.path.exists(target_file)


def test_AbjadIDE_copy_file_02():
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
        input_ = 'Blue~Example~Score d from'
        input_ += ' {}'.format(source_file)
        input_ += ' y q'
        abjad_ide._run_main_menu(input_=input_)
        assert os.path.exists(target_file)


def test_AbjadIDE_copy_file_03():
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
        input_ = 'Blue~Example~Score c from'
        input_ += ' {}'.format(source_file)
        input_ += ' y q'
        abjad_ide._run_main_menu(input_=input_)
        assert os.path.exists(target_file)


def test_AbjadIDE_copy_file_04():
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
        input_ = 'Blue~Example~Score k from'
        input_ += ' {}'.format(source_file)
        input_ += ' y q'
        abjad_ide._run_main_menu(input_=input_)
        assert os.path.exists(target_file)


def test_AbjadIDE_copy_file_05():
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
        input_ = 'Blue~Example~Score m articulation~handler from'
        input_ += ' {}'.format(source_file)
        input_ += ' y q'
        abjad_ide._run_main_menu(input_=input_)
        assert os.path.exists(target_file)


def test_AbjadIDE_copy_file_06():
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
        input_ = 'Blue~Example~Score g segment~01 from'
        input_ += ' {}'.format(source_file)
        input_ += ' y q'
        abjad_ide._run_main_menu(input_=input_)
        assert os.path.exists(target_file)


def test_AbjadIDE_copy_file_07():
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
        input_ = 'Blue~Example~Score y from'
        input_ += ' {}'.format(source_file)
        input_ += ' y q'
        abjad_ide._run_main_menu(input_=input_)
        assert os.path.exists(target_file)


def test_AbjadIDE_copy_file_08():
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
        input_ = 'Blue~Example~Score t from'
        input_ += ' {}'.format(source_file)
        input_ += ' y q'
        abjad_ide._run_main_menu(input_=input_)
        assert os.path.exists(target_file)