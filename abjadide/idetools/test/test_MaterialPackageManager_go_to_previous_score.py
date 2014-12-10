# -*- encoding: utf-8 -*-
from abjad import *
import abjadide
ide = abjadide.idetools.AbjadIDE(is_test=True)


def test_MaterialPackageManager_go_to_previous_score_01():

    input_ = 'red~example~score m tempo~inventory << q'
    ide._run(input_=input_)
    titles = [
        'Abjad IDE - scores',
        'Red Example Score (2013)',
        'Red Example Score (2013) - materials directory',
        'Red Example Score (2013) - materials directory - tempo inventory',
        'Étude Example Score (2013)',
        ]
    assert ide._transcript.titles == titles