# -*- encoding: utf-8 -*-
from abjad import *
import ide
abjad_ide = ide.tools.idetools.AbjadIDE(is_test=True)


def test_Wrangler_go_to_score_makers_directory_01():
    r'''From build directory to makers directory.
    '''

    input_ = 'red~example~score u k q'
    abjad_ide._run(input_=input_)
    titles = [
        'Abjad IDE - all score directories',
        'Red Example Score (2013)',
        'Red Example Score (2013) - build directory',
        'Red Example Score (2013) - makers directory',
        ]
    assert abjad_ide._io_manager._transcript.titles == titles