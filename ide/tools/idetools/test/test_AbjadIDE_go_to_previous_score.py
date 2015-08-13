# -*- encoding: utf-8 -*-
import pytest
from abjad import *
import ide
abjad_ide = ide.tools.idetools.AbjadIDE(is_test=True)
pytest.skip('reimplement nonstatally')


def test_AbjadIDE_go_to_previous_score_01():
    r'''From material package.
    '''

    input_ = 'red~example~score m tempo~inventory << q'
    abjad_ide._run_main_menu(input_=input_)
    titles = [
        'Abjad IDE - all score directories',
        'Red Example Score (2013)',
        'Red Example Score (2013) - materials directory',
        'Red Example Score (2013) - materials directory - tempo inventory',
        'Étude Example Score (2013)',
        ]
    assert abjad_ide._io_manager._transcript.titles == titles


def test_AbjadIDE_go_to_previous_score_02():
    r'''From segment package.
    '''

    input_ = 'red~example~score g A << q'
    abjad_ide._run_main_menu(input_=input_)
    titles = [
        'Abjad IDE - all score directories',
        'Red Example Score (2013)',
        'Red Example Score (2013) - segments directory',
        'Red Example Score (2013) - segments directory - A',
        'Étude Example Score (2013)',
        ]
    assert abjad_ide._io_manager._transcript.titles == titles


def test_AbjadIDE_go_to_previous_score_03():
    r'''From score package.
    '''

    input_ = 'red~example~score << q'
    abjad_ide._run_main_menu(input_=input_)
    titles = [
        'Abjad IDE - all score directories',
        'Red Example Score (2013)',
        'Étude Example Score (2013)',
        ]
    assert abjad_ide._io_manager._transcript.titles == titles