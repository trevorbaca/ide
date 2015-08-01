# -*- encoding: utf-8 -*-
from abjad import *
import ide
abjad_ide = ide.tools.idetools.AbjadIDE(is_test=True)


def test_Wrangler_go_to_previous_score_01():
    r'''Works at home.
    '''

    abjad_ide = ide.tools.idetools.AbjadIDE(is_test=True)
    input_ = '<< << q'
    abjad_ide._run(input_=input_)
    titles = [
        'Abjad IDE - all score directories',
        'Red Example Score (2013)',
        'Étude Example Score (2013)',
        ]
    assert abjad_ide._session._transcript.titles == titles


def test_Wrangler_go_to_previous_score_02():
    r'''Works in build directory.
    '''

    input_ = 'red~example~score u << q'
    abjad_ide._run(input_=input_)

    titles = [
        'Abjad IDE - all score directories',
        'Red Example Score (2013)',
        'Red Example Score (2013) - build directory',
        'Étude Example Score (2013)',
        ]
    assert abjad_ide._session._transcript.titles == titles


def test_Wrangler_go_to_previous_score_03():
    r'''Works with all build files.
    '''

    input_ = 'uu << q'
    abjad_ide._run(input_=input_)

    titles = [
        'Abjad IDE - all score directories',
        'Abjad IDE - all build directories',
        'Red Example Score (2013)',
        ]
    assert abjad_ide._session._transcript.titles == titles