# -*- encoding: utf-8 -*-
from abjad import *
import abjadide
ide = abjadide.idetools.AbjadIDE(is_test=True)


def test_ScorePackageWrangler_go_to_all_materials_01():
    r'''From scores to materials depot.
    '''

    input_ = 'mm q'
    ide._run(input_=input_)
    titles = [
        'Abjad IDE - scores',
        'Abjad IDE - materials depot',
        ]
    assert ide._transcript.titles == titles