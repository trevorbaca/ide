# -*- encoding: utf-8 -*-
from abjad import *
import abjad_ide


def test_Getter_go_to_current_score_01():

    abjad_ide = abjad_ide.idetools.AbjadIDE(is_test=True)
    input_ = 'red~example~score m tempo~inventory da 1 d s q'
    abjad_ide._run(input_=input_)

    titles = [
        'Abjad IDE - scores',
        'Red Example Score (2013)',
        'Red Example Score (2013) - materials directory',
        'Red Example Score (2013) - materials directory - tempo inventory',
        'Red Example Score (2013) - materials directory - tempo inventory (EDIT)',
        'Red Example Score (2013) - materials directory - tempo inventory - tempo (EDIT)',
        'Red Example Score (2013)',
        ]
    assert abjad_ide._transcript.titles == titles