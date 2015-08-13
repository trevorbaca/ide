# -*- encoding: utf-8 -*-
import os
import pytest
import shutil
from abjad import *
import ide
abjad_ide = ide.tools.idetools.AbjadIDE(is_test=True)
configuration = ide.tools.idetools.AbjadIDEConfiguration()


def test_AbjadIDE_check_every_package_01():
    r'''Checks every score package.
    '''
    pytest.skip()

    lines = [
        'Étude Example Score (2013):',
        '    Top level (10 assets): OK',
        '    Build directory (1 files): OK',
        '    Distribution directory (0 files): OK',
        '    Makers directory (0 files): OK',
        '    Materials directory (0 packages): OK',
        '    Segments directory (0 packages): OK',
        '    Stylesheets directory (0 files): OK',
        'Red Example Score (2013):',
        '    Top level (10 assets): OK',
        '    Build directory (18 files): OK',
        '    Distribution directory (2 files): OK',
        '    Makers directory (2 files): OK',
        '    Materials directory (5 packages):',
        '        Magic numbers: OK',
        '        Performer inventory: OK',
        '        Pitch range inventory: OK',
        '        Tempo inventory: OK',
        '        Time signatures: OK',
        '    Segments directory (3 packages):',
        '        A: OK',
        '        B: OK',
        '        C: OK',
        '    Stylesheets directory (4 files): OK',
        ]

    input_ = 'ck* y n q'
    abjad_ide._run_main_menu(input_=input_)
    contents = abjad_ide._io_manager._transcript.contents
    for line in lines:
        assert line in contents


def test_AbjadIDE_check_every_package_02():
    r'''Supplies missing build directory.
    '''

    score_directory = os.path.join(
        configuration.abjad_ide_example_scores_directory,
        'red_example_score',
        'red_example_score',
        )
    build_directory = os.path.join(score_directory, 'build')
        
    with systemtools.FilesystemState(keep=[build_directory]):
        shutil.rmtree(build_directory)
        input_ = 'ck* y y q'
        abjad_ide._run_main_menu(input_=input_)
        assert os.path.isdir(build_directory)


def test_AbjadIDE_check_every_package_03():
    r'''Supplies missing initializer.
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
        input_ = 'ck* y y q'
        abjad_ide._run_main_menu(input_=input_)
        assert os.path.isfile(initializer)