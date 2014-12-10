# -*- encoding: utf-8 -*-
from abjad import *
import abjad_ide
abjad_ide = abjad_ide.idetools.AbjadIDE(is_test=True)


def test_ScorePackageWrangler_go_to_next_score_01():

    input_ = '>> >> q'
    abjad_ide._run(input_=input_)
    titles = [
        'Abjad IDE - scores',
        'Blue Example Score (2013)',
        'Étude Example Score (2013)',
        ]
    assert abjad_ide._transcript.titles == titles