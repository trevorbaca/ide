# -*- coding: utf-8 -*-
from abjad import *
import ide
abjad_ide = ide.tools.idetools.AbjadIDE(is_test=True)


def test_AbjadIDE_go_to_distribution_directory_01():
    r'''From material package.
    '''

    input_ = 'red~example~score mm tempo~inventory dd q'
    abjad_ide._start_abjad_ide(input_=input_)

    titles = [
        'Abjad IDE - all score directories',
        'Red Example Score (2013)',
        'Red Example Score (2013) - materials directory',
        'Red Example Score (2013) - materials directory - tempo inventory',
        'Red Example Score (2013) - distribution directory',
        ]
    assert abjad_ide._io_manager._transcript.titles == titles


def test_AbjadIDE_go_to_distribution_directory_02():
    r'''From segment package.
    '''

    input_ = 'red~example~score gg A dd q'
    abjad_ide._start_abjad_ide(input_=input_)

    titles = [
        'Abjad IDE - all score directories',
        'Red Example Score (2013)',
        'Red Example Score (2013) - segments directory',
        'Red Example Score (2013) - segments directory - A',
        'Red Example Score (2013) - distribution directory',
        ]
    assert abjad_ide._io_manager._transcript.titles == titles


def test_AbjadIDE_go_to_distribution_directory_03():
    r'''From score package.
    '''

    input_ = 'red~example~score dd q'
    abjad_ide._start_abjad_ide(input_=input_)

    titles = [
        'Abjad IDE - all score directories',
        'Red Example Score (2013)',
        'Red Example Score (2013) - distribution directory',
        ]
    assert abjad_ide._io_manager._transcript.titles == titles


def test_AbjadIDE_go_to_distribution_directory_04():
    r'''From build directory to distribution directory.
    '''

    input_ = 'red~example~score bb dd q'
    abjad_ide._start_abjad_ide(input_=input_)
    titles = [
        'Abjad IDE - all score directories',
        'Red Example Score (2013)',
        'Red Example Score (2013) - build directory',
        'Red Example Score (2013) - distribution directory',
        ]
    assert abjad_ide._io_manager._transcript.titles == titles