# -*- encoding: utf-8 -*-
from abjad import *
import abjad_ide


def test_ScorePackageWrangler_go_to_previous_score_01():

    abjad_ide = abjad_ide.idetools.AbjadIDE(is_test=True)
    input_ = '<< << q'
    abjad_ide._run(input_=input_)
    titles = [
        'Abjad IDE - scores',
        'Red Example Score (2013)',
        'Étude Example Score (2013)',
        ]
    assert abjad_ide._transcript.titles == titles