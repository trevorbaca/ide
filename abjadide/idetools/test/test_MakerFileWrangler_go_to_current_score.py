# -*- encoding: utf-8 -*-
from abjad import *
import abjadide
ide = abjadide.idetools.AbjadIDE(is_test=True)


def test_MakerFileWrangler_go_to_current_score_01():

    input_ = 'red~example~score k s q'
    ide._run(input_=input_)

    titles = [
        'Abjad IDE - scores',
        'Red Example Score (2013)',
        'Red Example Score (2013) - makers directory',
        'Red Example Score (2013)',
        ]
    assert ide._transcript.titles == titles