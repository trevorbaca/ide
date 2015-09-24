# -*- coding: utf-8 -*-
import os
from abjad import *
import ide
abjad_ide = ide.tools.idetools.AbjadIDE(is_test=True)
configuration = ide.tools.idetools.AbjadIDEConfiguration()
scores_directory = configuration.abjad_ide_example_scores_directory


def test_AbjadIDE_copy_01():
    r'''Into build directory.
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
        input_ = 'Blue~Example~Score bb cp'
        input_ += ' {}'.format(source_file)
        input_ += ' y q'
        abjad_ide._start(input_=input_)
        assert os.path.exists(target_file)


def test_AbjadIDE_copy_02():
    r'''Into distribution directory.
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
        input_ = 'Blue~Example~Score dd cp'
        input_ += ' {}'.format(source_file)
        input_ += ' y q'
        abjad_ide._start(input_=input_)
        assert os.path.exists(target_file)


def test_AbjadIDE_copy_03():
    r'''Into etc directory.
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
        input_ = 'Blue~Example~Score ee cp'
        input_ += ' {}'.format(source_file)
        input_ += ' y q'
        abjad_ide._start(input_=input_)
        assert os.path.exists(target_file)


def test_AbjadIDE_copy_04():
    r'''Into makers directory.
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
        input_ = 'Blue~Example~Score kk cp'
        input_ += ' {}'.format(source_file)
        input_ += ' y q'
        abjad_ide._start(input_=input_)
        assert os.path.exists(target_file)


def test_AbjadIDE_copy_05():
    r'''Into material directory.
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
        input_ = 'Blue~Example~Score mm articulation~handler cp'
        input_ += ' {}'.format(source_file)
        input_ += ' y q'
        abjad_ide._start(input_=input_)
        assert os.path.exists(target_file)


def test_AbjadIDE_copy_06():
    r'''Into materials directory.
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
        input_ = 'Blue~Example~Score mm cp'
        input_ += ' {}'.format(source_package)
        input_ += ' y q'
        abjad_ide._start(input_=input_)
        assert os.path.exists(target_package)


def test_AbjadIDE_copy_07():
    r'''Into segment directory.
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
        input_ = 'Blue~Example~Score gg segment~01 cp'
        input_ += ' {}'.format(source_file)
        input_ += ' y q'
        abjad_ide._start(input_=input_)
        assert os.path.exists(target_file)


def test_AbjadIDE_copy_08():
    r'''Into segments directory.
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
        input_ = 'Blue~Example~Score gg cp'
        input_ += ' {}'.format(source_package)
        input_ += ' y q'
        abjad_ide._start(input_=input_)
        assert os.path.exists(target_package)


def test_AbjadIDE_copy_09():
    r'''Into stylesheets directory.
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
        input_ = 'Blue~Example~Score yy cp'
        input_ += ' {}'.format(source_file)
        input_ += ' y q'
        abjad_ide._start(input_=input_)
        assert os.path.exists(target_file)


def test_AbjadIDE_copy_10():
    r'''Into test directory.
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
        input_ = 'Blue~Example~Score tt cp'
        input_ += ' {}'.format(source_file)
        input_ += ' y q'
        abjad_ide._start(input_=input_)
        assert os.path.exists(target_file)