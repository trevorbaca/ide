# -*- coding: utf-8 -*-
from abjad import *
import ide
abjad_ide = ide.tools.idetools.AbjadIDE(is_test=True)


def test_AbjadIDE_go_to_makers_directory_01():
    r'''From material directory.
    '''

    input_ = 'red~example~score mm tempo~inventory kk q'
    abjad_ide._start(input_=input_)

    titles = [
        'Abjad IDE - all score directories',
        'Red Example Score (2013)',
        'Red Example Score (2013) - materials directory',
        'Red Example Score (2013) - materials directory - tempo inventory',
        'Red Example Score (2013) - makers directory',
        ]
    assert abjad_ide._io_manager._transcript.titles == titles
    contents = abjad_ide._io_manager._transcript.contents
    assert 'adjust_spacing_sections.py' in contents


def test_AbjadIDE_go_to_makers_directory_02():
    r'''From segment directory.
    '''

    input_ = 'red~example~score gg A kk q'
    abjad_ide._start(input_=input_)

    titles = [
        'Abjad IDE - all score directories',
        'Red Example Score (2013)',
        'Red Example Score (2013) - segments directory',
        'Red Example Score (2013) - segments directory - A',
        'Red Example Score (2013) - makers directory',
        ]
    assert abjad_ide._io_manager._transcript.titles == titles


def test_AbjadIDE_go_to_makers_directory_03():
    r'''From score directory.
    '''

    input_ = 'red~example~score kk q'
    abjad_ide._start(input_=input_)

    titles = [
        'Abjad IDE - all score directories',
        'Red Example Score (2013)',
        'Red Example Score (2013) - makers directory',
        ]
    assert abjad_ide._io_manager._transcript.titles == titles


def test_AbjadIDE_go_to_makers_directory_04():
    r'''From build directory to makers directory.
    '''

    input_ = 'red~example~score bb kk q'
    abjad_ide._start(input_=input_)
    titles = [
        'Abjad IDE - all score directories',
        'Red Example Score (2013)',
        'Red Example Score (2013) - build directory',
        'Red Example Score (2013) - makers directory',
        ]
    assert abjad_ide._io_manager._transcript.titles == titles