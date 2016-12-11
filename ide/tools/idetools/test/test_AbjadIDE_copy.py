# -*- coding: utf-8 -*-
import abjad
import ide
import os
abjad_ide = ide.tools.idetools.AbjadIDE(is_test=True)
configuration = ide.tools.idetools.AbjadIDEConfiguration()
scores_directory = configuration.abjad_ide_example_scores_directory


def test_AbjadIDE_copy_01():
    r'''Into build subdirectory.
    '''

    source_file = os.path.join(
        scores_directory,
        'red_example_score',
        'red_example_score',
        'build',
        'letter-portrait',
        'front-cover.tex',
        )
    assert os.path.isfile(source_file)
    target_file = os.path.join(
        scores_directory,
        'blue_example_score',
        'blue_example_score',
        'build',
        'letter-portrait',
        'front-cover.tex',
        )
    assert not os.path.exists(target_file)
    trimmed_source_file = abjad_ide._trim_path(source_file)
    trimmed_target_file = abjad_ide._trim_path(target_file)

    with abjad.systemtools.FilesystemState(keep=[scores_directory]):
        input_ = 'Blue~Example~Score bb letter-portrait cp'
        input_ += ' {}'.format(trimmed_source_file)
        input_ += ' y q'
        abjad_ide._start(input_=input_)
        assert os.path.exists(target_file)

    contents = abjad_ide._io_manager._transcript.contents
    header = 'Blue Example Score (2013) - build directory'
    header += ' - letter-portrait - select:'
    assert header in contents


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
    trimmed_source_file = abjad_ide._trim_path(source_file)
    trimmed_target_file = abjad_ide._trim_path(target_file)

    with abjad.systemtools.FilesystemState(keep=[scores_directory]):
        assert not os.path.exists(target_file)
        input_ = 'Blue~Example~Score dd cp'
        input_ += ' {}'.format(trimmed_source_file)
        input_ += ' y q'
        abjad_ide._start(input_=input_)
        assert os.path.exists(target_file)

    contents = abjad_ide._io_manager._transcript.contents
    assert 'Blue Example Score (2013) - distribution directory - select:' in contents


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
    trimmed_source_file = abjad_ide._trim_path(source_file)
    trimmed_target_file = abjad_ide._trim_path(target_file)

    with abjad.systemtools.FilesystemState(keep=[scores_directory]):
        assert not os.path.exists(target_file)
        input_ = 'Blue~Example~Score ee cp'
        input_ += ' {}'.format(trimmed_source_file)
        input_ += ' y q'
        abjad_ide._start(input_=input_)
        assert os.path.exists(target_file)

    contents = abjad_ide._io_manager._transcript.contents
    assert 'Blue Example Score (2013) - etc directory - select:' in contents


def test_AbjadIDE_copy_04():
    r'''Into tools directory.
    '''

    source_file = os.path.join(
        scores_directory,
        'red_example_score',
        'red_example_score',
        'tools',
        'ScoreTemplate.py',
        )
    target_file = os.path.join(
        scores_directory,
        'blue_example_score',
        'blue_example_score',
        'tools',
        'ScoreTemplate.py',
        )
    trimmed_source_file = abjad_ide._trim_path(source_file)
    trimmed_target_file = abjad_ide._trim_path(target_file)

    with abjad.systemtools.FilesystemState(keep=[scores_directory]):
        assert not os.path.exists(target_file)
        input_ = 'Blue~Example~Score oo cp'
        input_ += ' {}'.format(trimmed_source_file)
        input_ += ' y q'
        abjad_ide._start(input_=input_)
        assert os.path.exists(target_file)

    contents = abjad_ide._io_manager._transcript.contents
    assert 'Blue Example Score (2013) - tools directory - select:' in contents


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
    trimmed_source_file = abjad_ide._trim_path(source_file)
    trimmed_target_file = abjad_ide._trim_path(target_file)

    with abjad.systemtools.FilesystemState(keep=[scores_directory]):
        os.remove(target_file)
        assert not os.path.exists(target_file)
        input_ = 'Blue~Example~Score mm articulation~handler cp'
        input_ += ' {}'.format(trimmed_source_file)
        input_ += ' y q'
        abjad_ide._start(input_=input_)
        assert os.path.exists(target_file)

    contents = abjad_ide._io_manager._transcript.contents
    assert 'Blue Example Score (2013) - materials directory - articulation handler - select:' in contents


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
    trimmed_source_package = abjad_ide._trim_path(source_package)
    trimmed_target_package = abjad_ide._trim_path(target_package)

    with abjad.systemtools.FilesystemState(keep=[scores_directory]):
        assert os.path.isdir(source_package)
        assert not os.path.exists(target_package)
        input_ = 'Blue~Example~Score mm cp'
        input_ += ' {}'.format(trimmed_source_package)
        input_ += ' y q'
        abjad_ide._start(input_=input_)
        assert os.path.exists(target_package)

    contents = abjad_ide._io_manager._transcript.contents
    assert 'Blue Example Score (2013) - materials directory - select:' in contents


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
    trimmed_source_file = abjad_ide._trim_path(source_file)
    trimmed_target_file = abjad_ide._trim_path(target_file)

    with abjad.systemtools.FilesystemState(keep=[scores_directory]):
        os.remove(target_file)
        assert not os.path.exists(target_file)
        input_ = 'Blue~Example~Score gg segment~01 cp'
        input_ += ' {}'.format(trimmed_source_file)
        input_ += ' y q'
        abjad_ide._start(input_=input_)
        assert os.path.exists(target_file)

    contents = abjad_ide._io_manager._transcript.contents
    assert 'Blue Example Score (2013) - segments directory - segment 01 - select:' in contents


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
    trimmed_source_package = abjad_ide._trim_path(source_package)
    trimmed_target_package = abjad_ide._trim_path(target_package)

    with abjad.systemtools.FilesystemState(keep=[scores_directory]):
        assert os.path.isdir(source_package)
        assert not os.path.exists(target_package)
        input_ = 'Blue~Example~Score gg cp'
        input_ += ' {}'.format(trimmed_source_package)
        input_ += ' y q'
        abjad_ide._start(input_=input_)
        assert os.path.exists(target_package)

    contents = abjad_ide._io_manager._transcript.contents
    assert 'Blue Example Score (2013) - segments directory - select:' in contents


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
    trimmed_source_file = abjad_ide._trim_path(source_file)
    trimmed_target_file = abjad_ide._trim_path(target_file)

    with abjad.systemtools.FilesystemState(keep=[scores_directory]):
        assert not os.path.exists(target_file)
        input_ = 'Blue~Example~Score yy cp'
        input_ += ' {}'.format(trimmed_source_file)
        input_ += ' y q'
        abjad_ide._start(input_=input_)
        assert os.path.exists(target_file)

    contents = abjad_ide._io_manager._transcript.contents
    assert 'Blue Example Score (2013) - stylesheets directory - select:' in contents


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
    trimmed_source_file = abjad_ide._trim_path(source_file)
    trimmed_target_file = abjad_ide._trim_path(target_file)

    with abjad.systemtools.FilesystemState(keep=[scores_directory]):
        assert not os.path.exists(target_file)
        input_ = 'Blue~Example~Score tt cp'
        input_ += ' {}'.format(trimmed_source_file)
        input_ += ' y q'
        abjad_ide._start(input_=input_)
        assert os.path.exists(target_file)

    contents = abjad_ide._io_manager._transcript.contents
    assert 'Blue Example Score (2013) - test directory - select:' in contents
