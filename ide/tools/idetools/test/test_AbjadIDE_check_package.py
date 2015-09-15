# -*- coding: utf-8 -*-
import os
import shutil
from abjad import *
import ide
abjad_ide = ide.tools.idetools.AbjadIDE(is_test=True)
configuration = ide.tools.idetools.AbjadIDEConfiguration()


def test_AbjadIDE_check_package_01():
    r'''Reports problems only in score package.
    '''

    input_ = 'red~example~score ck y q'
    abjad_ide._run_main_menu(input_=input_)
    contents = abjad_ide._io_manager._transcript.contents

    lines = [
        'Build directory (18 files): OK',
        'Distribution directory (2 files): OK',
        'Makers directory (2 files): OK',
        'Materials directory (5 packages):',
        'Segments directory (3 packages):',
        'Stylesheets directory (4 files): OK',
        ]
    for line in lines:
        assert line in contents
    assert 'found' not in contents


def test_AbjadIDE_check_package_02():
    r'''Reports everything in score package.
    '''

    input_ = 'red~example~score ck n q'
    abjad_ide._run_main_menu(input_=input_)
    contents = abjad_ide._io_manager._transcript.contents

    lines = [
        'Top level (10 assets): OK',
        '8 of 8 required directories found:',
        '8 of 8 required files found:',
        'Build directory (18 files): OK',
        'Distribution directory (2 files): OK',
        'Makers directory (2 files): OK',
        'Materials directory (5 packages):',
        'Segments directory (3 packages):',
        'Stylesheets directory (4 files): OK',
        'Test directory (1 files): OK',
        ]
    for line in lines:
        assert line in contents


def test_AbjadIDE_check_package_03():
    r'''Reports unrecognized file in score package.
    '''

    extra_file = os.path.join(
        configuration.abjad_ide_example_scores_directory,
        'red_example_score',
        'red_example_score',
        'extra_file.txt',
        )

    with systemtools.FilesystemState(remove=[extra_file]):
        with open(extra_file, 'w') as file_pointer:
            file_pointer.write('')
        input_ = 'red~example~score ck y q'
        abjad_ide._run_main_menu(input_=input_)
        contents = abjad_ide._io_manager._transcript.contents

    line = '1 unrecognized file found:'
    assert line in contents


def test_AbjadIDE_check_package_04():
    r'''Supplies missing directory in score package.
    '''

    score_directory = os.path.join(
        configuration.abjad_ide_example_scores_directory,
        'red_example_score',
        'red_example_score',
        )
    build_directory = os.path.join(score_directory, 'build')
        
    with systemtools.FilesystemState(keep=[build_directory]):
        shutil.rmtree(build_directory)
        input_ = 'red~example~score ck y y q'
        abjad_ide._run_main_menu(input_=input_)
        assert os.path.isdir(build_directory)


def test_AbjadIDE_check_package_05():
    r'''Supplies missing file in subdirectory.
    '''

    segment_directory = os.path.join(
        configuration.abjad_ide_example_scores_directory,
        'red_example_score',
        'red_example_score',
        'segments',
        'segment_02',
        )
    initializer = os.path.join(segment_directory, '__init__.py')
        
    with systemtools.FilesystemState(keep=[initializer]):
        os.remove(initializer)
        input_ = 'red~example~score ck y y q'
        abjad_ide._run_main_menu(input_=input_)
        assert os.path.isfile(initializer)