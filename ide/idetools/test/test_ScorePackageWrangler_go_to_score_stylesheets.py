# -*- encoding: utf-8 -*-
from abjad import *
import abjad_ide
abjad_ide = abjad_ide.idetools.AbjadIDE(is_test=True)


def test_ScorePackageWrangler_go_to_score_stylesheets_01():
    r'''From scores to stylesheets depot.
    '''

    input_ = 'yy q'
    abjad_ide._run(input_=input_)
    titles = [
        'Abjad IDE - scores',
        'Abjad IDE - stylesheets depot',
        ]
    assert abjad_ide._transcript.titles == titles