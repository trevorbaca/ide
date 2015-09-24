# -*- coding: utf-8 -*-
from abjad import *
import os
import ide
abjad_ide = ide.tools.idetools.AbjadIDE(is_test=True)
configuration = ide.tools.idetools.AbjadIDEConfiguration()


def test_AbjadIDE_make_ly_01():
    r'''Creates LilyPond file when none exists.
    '''

    segment_directory = os.path.join(
        configuration.abjad_ide_example_scores_directory,
        'red_example_score',
        'red_example_score',
        'materials',
        'magic_numbers',
        )
    ly_path = os.path.join(segment_directory, 'illustration.ly')

    with systemtools.FilesystemState(keep=[ly_path]):
        os.remove(ly_path)
        input_ = 'red~example~score mm magic~numbers lym q'
        abjad_ide._start(input_=input_)
        assert os.path.isfile(ly_path)
        assert systemtools.TestManager._compare_backup(ly_path)

    contents = abjad_ide._io_manager._transcript.contents
    assert 'Overwriting' in contents
    assert abjad_ide._trim_path(ly_path) in contents


def test_AbjadIDE_make_ly_02():
    r'''Preserves existing LilyPond file when candidate compares the same.
    '''

    segment_directory = os.path.join(
        configuration.abjad_ide_example_scores_directory,
        'red_example_score',
        'red_example_score',
        'materials',
        'magic_numbers',
        )
    ly_path = os.path.join(segment_directory, 'illustration.ly')
    candidate_ly_path = os.path.join(
        segment_directory,
        'illustration.candidate.ly',
        )

    with systemtools.FilesystemState(keep=[ly_path]):
        # remove existing ly
        os.remove(ly_path)
        assert not os.path.exists(ly_path)
        # generate ly first time
        input_ = 'red~example~score mm magic~numbers lym q'
        abjad_ide._start(input_=input_)
        assert os.path.isfile(ly_path)
        # attempt to generate ly second time (but blocked)
        input_ = 'red~example~score mm magic~numbers lym q'
        abjad_ide._start(input_=input_)

    contents = abjad_ide._io_manager._transcript.contents
    assert 'The files ...' in contents
    assert abjad_ide._trim_path(ly_path) in contents
    assert abjad_ide._trim_path(candidate_ly_path) in contents
    assert '... compare the same.' in contents


def test_AbjadIDE_make_ly_03():
    r'''Prompts composer to overwrite existing PDF when candidate compares
    differently.
    '''

    segment_directory = os.path.join(
        configuration.abjad_ide_example_scores_directory,
        'red_example_score',
        'red_example_score',
        'materials',
        'magic_numbers',
        )
    ly_path = os.path.join(segment_directory, 'illustration.ly')
    candidate_ly_path = os.path.join(
        segment_directory,
        'illustration.candidate.ly',
        )

    with systemtools.FilesystemState(keep=[ly_path]):
        with open(ly_path, 'w') as file_pointer:
            file_pointer.write('text')
        input_ = 'red~example~score mm magic~numbers lym q'
        abjad_ide._start(input_=input_)
        assert os.path.isfile(ly_path)
        assert systemtools.TestManager._compare_backup(ly_path)

    contents = abjad_ide._io_manager._transcript.contents
    assert 'The files ...' in contents
    assert abjad_ide._trim_path(ly_path) in contents
    assert abjad_ide._trim_path(candidate_ly_path) in contents
    assert '... compare differently.' in contents