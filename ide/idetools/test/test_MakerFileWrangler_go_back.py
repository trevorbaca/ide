# -*- encoding: utf-8 -*-
from abjad import *
import ide
abjad_ide = abjad_ide.idetools.AbjadIDE(is_test=True)


def test_MakerFileWrangler_go_back_01():

    input_ = 'red~example~score k b q'
    abjad_ide._run(input_=input_)

    titles = [
        'Abjad IDE - scores',
        'Red Example Score (2013)',
        'Red Example Score (2013) - makers directory',
        'Red Example Score (2013)',
        ]
    assert abjad_ide._transcript.titles == titles


def test_MakerFileWrangler_go_back_02():

    input_ = 'kk b q'
    abjad_ide._run(input_=input_)

    titles = [
        'Abjad IDE - scores',
        'Abjad IDE - makers depot',
        'Abjad IDE - scores',
        ]
    assert abjad_ide._transcript.titles == titles