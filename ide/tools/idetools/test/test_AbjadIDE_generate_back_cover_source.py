# -*- coding: utf-8 -*-
import os
from abjad import *
import ide
abjad_ide = ide.tools.idetools.AbjadIDE(is_test=True)
configuration = ide.tools.idetools.AbjadIDEConfiguration()


def test_AbjadIDE_generate_back_cover_source_01():
    r'''Works when back cover source doesn't yet exist.

    Supplies papersize={8.5in, 11in} as a.
    '''

    source_path = os.path.join(
        configuration.abjad_ide_directory,
        'boilerplate',
        'back-cover.tex',
        )
    destination_path = os.path.join(
        configuration.abjad_ide_example_scores_directory,
        'blue_example_score',
        'blue_example_score',
        'build',
        'back-cover.tex',
        )

    with open(source_path) as file_pointer:
        source_contents = ''.join(file_pointer.readlines())
    assert 'paper_size' in source_contents
    assert '{8.5in, 11in}' not in source_contents

    with systemtools.FilesystemState(
        keep=[source_path], remove=[destination_path]):
        input_ = 'blue~example~score bb bcg q'
        abjad_ide._start(input_=input_)
        assert os.path.isfile(destination_path)
        with open(destination_path) as file_pointer:
            destination_contents = ''.join(file_pointer.readlines())
        assert 'paper_size' not in destination_contents
        assert '{8.5in, 11in}' in destination_contents

    contents = abjad_ide._io_manager._transcript.contents
    assert 'Writing' in contents


def test_AbjadIDE_generate_back_cover_source_02():
    r'''Preserves existing source when candidate doesn't differ.
    '''

    source_path = os.path.join(
        configuration.abjad_ide_directory,
        'boilerplate',
        'back-cover.tex',
        )
    destination_path = os.path.join(
        configuration.abjad_ide_example_scores_directory,
        'red_example_score',
        'red_example_score',
        'build',
        'back-cover.tex',
        )

    with open(source_path) as file_pointer:
        source_contents = ''.join(file_pointer.readlines())
    assert 'paper_size' in source_contents
    assert '{8.5in, 11in}' not in source_contents

    with systemtools.FilesystemState(keep=[source_path, destination_path]):
        os.remove(destination_path)
        # generate first time
        input_ = 'red~example~score bb bcg q'
        abjad_ide._start(input_=input_)
        # attempt to generate second time
        input_ = 'red~example~score bb bcg q'
        abjad_ide._start(input_=input_)
        assert os.path.isfile(destination_path)

    with open(destination_path) as file_pointer:
        destination_contents = ''.join(file_pointer.readlines())
    assert 'paper_size' not in destination_contents
    assert '{8.5in, 11in}' in destination_contents
    contents = abjad_ide._io_manager._transcript.contents
    assert 'Preserving' in contents