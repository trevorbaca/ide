# -*- encoding: utf-8 -*-
from abjad import *
import ide
abjad_ide = ide.tools.idetools.AbjadIDE(is_test=True)


def test_Wrangler_go_to_all_maker_files_01():
    r'''From scores to makers depot.
    '''

    input_ = 'kk q'
    abjad_ide._run(input_=input_)
    titles = [
        'Abjad IDE - scores',
        'Abjad IDE - makers depot',
        ]
    assert abjad_ide._transcript.titles == titles