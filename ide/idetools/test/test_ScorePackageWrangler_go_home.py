# -*- encoding: utf-8 -*-
from abjad import *
import abjad_ide
abjad_ide = abjad_ide.idetools.AbjadIDE(is_test=True)


def test_ScorePackageWrangler_go_home_01():
    r'''From scores.
    '''

    input_ = 'hh q'
    abjad_ide._run(input_=input_)
    titles = [
        'Abjad IDE - scores',
        'Abjad IDE - home',
        ]
    assert abjad_ide._transcript.titles == titles