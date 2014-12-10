# -*- encoding: utf-8 -*-
from abjad import *
import abjadide
ide = abjadide.idetools.AbjadIDE(is_test=True)


def test_StylesheetWrangler_go_to_score_materials_01():
    r'''From stylesheets directory to materials directory.
    '''

    input_ = 'red~example~score y m q'
    ide._run(input_=input_)
    titles = [
        'Abjad IDE - scores',
        'Red Example Score (2013)',
        'Red Example Score (2013) - stylesheets directory',
        'Red Example Score (2013) - materials directory',
        ]
    assert ide._transcript.titles == titles