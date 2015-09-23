# -*- coding: utf-8 -*-
from abjad import *
import ide
abjad_ide = ide.tools.idetools.AbjadIDE(is_test=True)


def test_AbjadIDE_go_back_01():

    input_ = 'red~example~score mm tempo~inventory kk - - q'
    abjad_ide._start(input_=input_)

    titles = [
        'Abjad IDE - all score directories',
        'Red Example Score (2013)',
        'Red Example Score (2013) - materials directory',
        'Red Example Score (2013) - materials directory - tempo inventory',
        'Red Example Score (2013) - makers directory',
        'Red Example Score (2013) - materials directory - tempo inventory',
        'Red Example Score (2013) - makers directory',
        ]
    assert abjad_ide._io_manager._transcript.titles == titles


def test_AbjadIDE_go_back_02():

    input_ = 'red~example~score gg A bb - - q'
    abjad_ide._start(input_=input_)
    titles = [
        'Abjad IDE - all score directories',
        'Red Example Score (2013)',
        'Red Example Score (2013) - segments directory',
        'Red Example Score (2013) - segments directory - A',
        'Red Example Score (2013) - build directory',
        'Red Example Score (2013) - segments directory - A',
        'Red Example Score (2013) - build directory',
        ]
    assert abjad_ide._io_manager._transcript.titles == titles


def test_AbjadIDE_go_back_03():

    input_ = '- q'
    abjad_ide._start(input_=input_)

    titles = [
        'Abjad IDE - all score directories',
        ]
    assert abjad_ide._io_manager._transcript.titles == titles


def test_AbjadIDE_go_back_04():

    input_ = 'red~example~score - - - q'
    abjad_ide._start(input_=input_)

    titles = [
        'Abjad IDE - all score directories',
        'Red Example Score (2013)',
        'Abjad IDE - all score directories',
        'Red Example Score (2013)',
        'Abjad IDE - all score directories',
        ]
    assert abjad_ide._io_manager._transcript.titles == titles