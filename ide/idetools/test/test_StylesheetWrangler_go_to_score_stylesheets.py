# -*- encoding: utf-8 -*-
from abjad import *
import ide
abjad_ide = ide.idetools.AbjadIDE(is_test=True)


def test_StylesheetWrangler_go_to_score_stylesheets_01():
    r'''From stylesheets directory to stylesheets directory.
    '''

    input_ = 'red~example~score y y q'
    abjad_ide._run(input_=input_)
    titles = [
        'Abjad IDE - scores',
        'Red Example Score (2013)',
        'Red Example Score (2013) - stylesheets directory',
        'Red Example Score (2013) - stylesheets directory',
        ]
    assert abjad_ide._transcript.titles == titles