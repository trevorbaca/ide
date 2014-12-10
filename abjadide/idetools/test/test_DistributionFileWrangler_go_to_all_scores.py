# -*- encoding: utf-8 -*-
from abjad import *
import abjadide
ide = abjadide.idetools.AbjadIDE(is_test=True)


def test_DistributionFileWrangler_go_to_all_scores_01():

    input_ = 'red~example~score d ss q'
    ide._run(input_=input_)

    titles = [
        'Abjad IDE - scores',
        'Red Example Score (2013)',
        'Red Example Score (2013) - distribution directory',
        'Abjad IDE - scores',
        ]
    assert ide._transcript.titles == titles


def test_DistributionFileWrangler_go_to_all_scores_02():

    input_ = 'dd ss q'
    ide._run(input_=input_)

    titles = [
        'Abjad IDE - scores',
        'Abjad IDE - distribution depot',
        'Abjad IDE - scores',
        ]
    assert ide._transcript.titles == titles