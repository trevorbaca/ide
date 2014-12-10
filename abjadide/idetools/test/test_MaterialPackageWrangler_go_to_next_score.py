# -*- encoding: utf-8 -*-
from abjad import *
import abjadide
ide = abjadide.idetools.AbjadIDE(is_test=True)


def test_MaterialPackageWrangler_go_to_next_score_01():

    input_ = 'red~example~score m >> q'
    ide._run(input_=input_)

    titles = [
        'Abjad IDE - scores',
        'Red Example Score (2013)',
        'Red Example Score (2013) - materials directory',
        'Blue Example Score (2013)',
        ]
    assert ide._transcript.titles == titles


def test_MaterialPackageWrangler_go_to_next_score_02():

    input_ = 'mm >> q'
    ide._run(input_=input_)

    titles = [
        'Abjad IDE - scores',
        'Abjad IDE - materials depot',
        'Blue Example Score (2013)',
        ]
    assert ide._transcript.titles == titles