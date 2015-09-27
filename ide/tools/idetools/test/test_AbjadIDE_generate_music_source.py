# -*- coding: utf-8 -*-
import os
from abjad import *
import ide
abjad_ide = ide.tools.idetools.AbjadIDE(is_test=True)
configuration = ide.tools.idetools.AbjadIDEConfiguration()


def test_AbjadIDE_generate_music_source_01():
    r'''When music does not exist yet.

    (Can't use filecmp because music.ly file contains LilyPond version
    directive, LilyPond language directive and file paths. All depend
    on user environment.)
    '''

    music_path = os.path.join(
        configuration.abjad_ide_example_scores_directory,
        'red_example_score',
        'red_example_score',
        'build',
        'music.ly',
        )

    with systemtools.FilesystemState(keep=[music_path]):
        os.remove(music_path)
        input_ = 'red~example~score bb mg q'
        abjad_ide._start(input_=input_)
        assert os.path.isfile(music_path)
        with open(music_path, 'r') as file_pointer:
            file_lines = file_pointer.readlines()
            file_contents = ''.join(file_lines)
        assert 'Red Example Score (2013) for piano' in file_contents
        assert r'\language' in file_contents
        assert r'\version' in file_contents


def test_AbjadIDE_generate_music_source_02():
    r'''When music already exists.
    '''

    music_path = os.path.join(
        configuration.abjad_ide_example_scores_directory,
        'red_example_score',
        'red_example_score',
        'build',
        'music.ly',
        )

    with systemtools.FilesystemState(keep=[music_path]):
        os.remove(music_path)
        # generate first time
        input_ = 'red~example~score bb mg q'
        abjad_ide._start(input_=input_)
        # attempt to generate second time
        input_ = 'red~example~score bb mg q'
        abjad_ide._start(input_=input_)
        contents = abjad_ide._io_manager._transcript.contents

    assert 'Preserving' in contents


def test_AbjadIDE_generate_music_source_03():
    r'''Indents include files exacty four spaces.
    '''

    music_path = os.path.join(
        configuration.abjad_ide_example_scores_directory,
        'red_example_score',
        'red_example_score',
        'build',
        'music.ly',
        )

    with systemtools.FilesystemState(keep=[music_path]):
        input_ = 'red~example~score bb mg q'
        abjad_ide._start(input_=input_)

    with open(music_path, 'r') as file_pointer:
        file_lines = file_pointer.readlines()
        file_contents = ''.join(file_lines)
        tab = 4 * ' '
        line = '\n' + tab + r'\include'
        assert line in file_contents