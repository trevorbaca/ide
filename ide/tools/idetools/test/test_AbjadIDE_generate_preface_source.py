# -*- coding: utf-8 -*-
import os
from abjad import *
import ide
abjad_ide = ide.tools.idetools.AbjadIDE(is_test=True)
configuration = ide.tools.idetools.AbjadIDEConfiguration()


def test_AbjadIDE_generate_preface_source_01():
    r'''Works when preface source doesn't yet exist.

    Supplies papersize={8.5in, 11in} as a.
    '''

    source_path = os.path.join(
        configuration.abjad_ide_directory,
        'boilerplate',
        'preface.tex',
        )
    destination_path = os.path.join(
        configuration.abjad_ide_example_scores_directory,
        'blue_example_score',
        'blue_example_score',
        'build',
        'preface.tex',
        )

    with open(source_path) as file_pointer:
        source_contents = ''.join(file_pointer.readlines())
    assert 'PAPER_SIZE' in source_contents
    assert '{8.5in, 11in}' not in source_contents

    with systemtools.FilesystemState(
        keep=[source_path], remove=[destination_path]):
        input_ = 'blue~example~score bb pg q'
        abjad_ide._run_main_menu(input_=input_)
        assert os.path.isfile(destination_path)
        with open(destination_path) as file_pointer:
            destination_contents = ''.join(file_pointer.readlines())
        assert 'PAPER_SIZE' not in destination_contents
        assert '{8.5in, 11in}' in destination_contents

    contents = abjad_ide._io_manager._transcript.contents
    assert 'Overwrite' not in contents
    assert 'Overwrote' not in contents


def test_AbjadIDE_generate_preface_source_02():
    r'''Works when preface source already exists.
    '''

    source_path = os.path.join(
        configuration.abjad_ide_directory,
        'boilerplate',
        'preface.tex',
        )
    destination_path = os.path.join(
        configuration.abjad_ide_example_scores_directory,
        'red_example_score',
        'red_example_score',
        'build',
        'preface.tex',
        )

    with open(source_path) as file_pointer:
        source_contents = ''.join(file_pointer.readlines())
    assert 'PAPER_SIZE' in source_contents
    assert '{8.5in, 11in}' not in source_contents

    with systemtools.FilesystemState(keep=[source_path, destination_path]):
        input_ = 'red~example~score bb pg q'
        abjad_ide._run_main_menu(input_=input_)
        assert os.path.isfile(destination_path)
        with open(destination_path) as file_pointer:
            destination_contents = ''.join(file_pointer.readlines())
        assert 'PAPER_SIZE' not in destination_contents
        assert '{8.5in, 11in}' in destination_contents

    contents = abjad_ide._io_manager._transcript.contents
    assert 'The files ...' in contents
    assert '... compare the same.' in contents
    assert 'Preserved' in contents