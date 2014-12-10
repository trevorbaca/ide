# -*- encoding: utf-8 -*-
from abjad import *
import abjad_ide
abjad_ide = abjad_ide.idetools.AbjadIDE(is_test=True)


def test_MakerFileWrangler_go_to_all_scores_01():

    input_ = 'red~example~score k ss q'
    abjad_ide._run(input_=input_)

    titles = [
        'Abjad IDE - scores',
        'Red Example Score (2013)',
        'Red Example Score (2013) - makers directory',
        'Abjad IDE - scores',
        ]
    assert abjad_ide._transcript.titles == titles


def test_MakerFileWrangler_go_to_all_scores_02():

    input_ = 'kk ss q'
    abjad_ide._run(input_=input_)

    titles = [
        'Abjad IDE - scores',
        'Abjad IDE - makers depot',
        'Abjad IDE - scores',
        ]
    assert abjad_ide._transcript.titles == titles