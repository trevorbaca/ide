# -*- encoding: utf-8 -*-
from abjad import *
import ide
abjad_ide = ide.idetools.AbjadIDE(is_test=True)


def test_Wrangler_go_to_score_maker_files_01():
    r'''From build directory to makers directory.
    '''

    input_ = 'red~example~score u k q'
    abjad_ide._run(input_=input_)
    titles = [
        'Abjad IDE - scores',
        'Red Example Score (2013)',
        'Red Example Score (2013) - build directory',
        'Red Example Score (2013) - makers directory',
        ]
    assert abjad_ide._transcript.titles == titles