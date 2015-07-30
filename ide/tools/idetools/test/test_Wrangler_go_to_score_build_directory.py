# -*- encoding: utf-8 -*-
from abjad import *
import ide
abjad_ide = ide.tools.idetools.AbjadIDE(is_test=True)


def test_Wrangler_go_to_score_build_directory_01():
    r'''From build directory to build directory.
    '''

    input_ = 'red~example~score u u q'
    abjad_ide._run(input_=input_)
    titles = [
        'Abjad IDE - all score directories',
        'Red Example Score (2013)',
        'Red Example Score (2013) - build directory',
        'Red Example Score (2013) - build directory',
        ]
    assert abjad_ide._transcript.titles == titles