# -*- encoding: utf-8 -*-
from abjad import *
import ide
abjad_ide = ide.idetools.AbjadIDE(is_test=True)


def test_AbjadIDE_go_to_all_scores_01():
    r'''From top level to all scores.
    '''

    input_ = 'hh ss q'
    abjad_ide._run(input_=input_)
    titles = [
        'Abjad IDE - scores',
        'Abjad IDE - home',
        'Abjad IDE - scores',
        ]
    assert abjad_ide._transcript.titles == titles