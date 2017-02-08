# -*- coding: utf-8 -*-
import abjad
import ide
abjad_ide = ide.tools.idetools.AbjadIDE(is_test=True)


def test_AbjadIDE_go_to_score_package_wrapper_01():
    r'''From material directory.
    '''

    input_ = 'red~example~score mm tempi ww q'
    abjad_ide._start(input_=input_)

    titles = [
        'Abjad IDE - all score directories',
        'Red Example Score (2013)',
        'Red Example Score (2013) - materials directory',
        'Red Example Score (2013) - materials directory - tempi',
        'Red Example Score (2013) - package wrapper',
        ]
    assert abjad_ide._io_manager._transcript.titles == titles
    contents = abjad_ide._io_manager._transcript.contents
    assert 'red_example_score' in contents


def test_AbjadIDE_go_to_score_package_wrapper_02():
    r'''From segment directory.
    '''

    input_ = 'red~example~score gg A ww q'
    abjad_ide._start(input_=input_)

    titles = [
        'Abjad IDE - all score directories',
        'Red Example Score (2013)',
        'Red Example Score (2013) - segments directory',
        'Red Example Score (2013) - segments directory - A',
        'Red Example Score (2013) - package wrapper',
        ]
    assert abjad_ide._io_manager._transcript.titles == titles


def test_AbjadIDE_go_to_score_package_wrapper_03():
    r'''From build directory.
    '''

    input_ = 'red~example~score bb ww q'
    abjad_ide._start(input_=input_)
    titles = [
        'Abjad IDE - all score directories',
        'Red Example Score (2013)',
        'Red Example Score (2013) - build directory',
        'Red Example Score (2013) - package wrapper',
        ]
    assert abjad_ide._io_manager._transcript.titles == titles