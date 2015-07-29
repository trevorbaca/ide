# -*- encoding: utf-8 -*-
from abjad import *
import ide
abjad_ide = ide.tools.idetools.AbjadIDE(is_test=True)


def test_Wrangler_go_to_all_stylesheets_01():
    r'''From scores to all stylesheets directories.
    '''

    input_ = 'yy q'
    abjad_ide._run(input_=input_)
    titles = [
        'Abjad IDE - all score directories',
        'Abjad IDE - all stylesheets directories',
        ]
    assert abjad_ide._transcript.titles == titles