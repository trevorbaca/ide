# -*- encoding: utf-8 -*-
from abjad import *
import ide
abjad_ide = abjad_ide.idetools.AbjadIDE(is_test=True)


def test_MakerFileWrangler_go_to_next_score_01():

    input_ = 'red~example~score k >> q'
    abjad_ide._run(input_=input_)

    titles = [
        'Abjad IDE - scores',
        'Red Example Score (2013)',
        'Red Example Score (2013) - makers directory',
        'Blue Example Score (2013)',
        ]
    assert abjad_ide._transcript.titles == titles


def test_MakerFileWrangler_go_to_next_score_02():

    input_ = 'kk >> q'
    abjad_ide._run(input_=input_)

    titles = [
        'Abjad IDE - scores',
        'Abjad IDE - makers depot',
        'Blue Example Score (2013)',
        ]
    assert abjad_ide._transcript.titles == titles