# -*- encoding: utf-8 -*-
from abjad import *
import abjadide
ide = abjadide.idetools.AbjadIDE(is_test=True)


def test_BuildFileWrangler_go_to_score_distribution_files_01():
    r'''From build directory to distribution directory.
    '''

    input_ = 'red~example~score u d q'
    ide._run(input_=input_)
    titles = [
        'Abjad IDE - scores',
        'Red Example Score (2013)',
        'Red Example Score (2013) - build directory',
        'Red Example Score (2013) - distribution directory',
        ]
    assert ide._transcript.titles == titles