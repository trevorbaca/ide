# -*- encoding: utf-8 -*-
from abjad import *
import ide
abjad_ide = ide.tools.idetools.AbjadIDE(is_test=True)


def test_Wrangler_go_back_01():

    input_ = 'b q'
    abjad_ide._run(input_=input_)

    titles = [
        'Abjad IDE - all score directories',
        'Abjad IDE - all score directories',
        ]
    assert abjad_ide._session._transcript.titles == titles


def test_Wrangler_go_back_02():

    input_ = 'red~example~score u b q'
    abjad_ide._run(input_=input_)

    titles = [
        'Abjad IDE - all score directories',
        'Red Example Score (2013)',
        'Red Example Score (2013) - build directory',
        'Red Example Score (2013)',
        ]
    assert abjad_ide._session._transcript.titles == titles


def test_Wrangler_go_back_03():

    input_ = 'uu b q'
    abjad_ide._run(input_=input_)

    titles = [
        'Abjad IDE - all score directories',
        'Abjad IDE - all build directories',
        'Abjad IDE - all score directories',
        ]
    assert abjad_ide._session._transcript.titles == titles