# -*- encoding: utf-8 -*-
from abjad import *
import ide
abjad_ide = abjad_ide.idetools.AbjadIDE(is_test=True)


def test_BuildFileWrangler_go_to_score_distribution_files_01():
    r'''From build directory to distribution directory.
    '''

    input_ = 'red~example~score u d q'
    abjad_ide._run(input_=input_)
    titles = [
        'Abjad IDE - scores',
        'Red Example Score (2013)',
        'Red Example Score (2013) - build directory',
        'Red Example Score (2013) - distribution directory',
        ]
    assert abjad_ide._transcript.titles == titles