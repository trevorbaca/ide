# -*- encoding: utf-8 -*-
from abjad import *
import ide
abjad_ide = ide.idetools.AbjadIDE(is_test=True)


def test_FileWrangler_go_to_next_score_01():

    input_ = 'red~example~score u >> q'
    abjad_ide._run(input_=input_)

    titles = [
        'Abjad IDE - scores',
        'Red Example Score (2013)',
        'Red Example Score (2013) - build directory',
        'Blue Example Score (2013)',
        ]
    assert abjad_ide._transcript.titles == titles


def test_FileWrangler_go_to_next_score_02():

    input_ = 'uu >> q'
    abjad_ide._run(input_=input_)

    titles = [
        'Abjad IDE - scores',
        'Abjad IDE - build depot',
        'Blue Example Score (2013)',
        ]
    assert abjad_ide._transcript.titles == titles