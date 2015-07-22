# -*- encoding: utf-8 -*-
from abjad import *
import ide
abjad_ide = ide.idetools.AbjadIDE(is_test=True)


def test_ScorePackageManager_go_to_all_scores_01():

    input_ = 'red~example~score h q'
    abjad_ide._run(input_=input_)

    titles = [
        'Abjad IDE - scores',
        'Red Example Score (2013)',
        'Abjad IDE - scores',
        ]
    assert abjad_ide._transcript.titles == titles