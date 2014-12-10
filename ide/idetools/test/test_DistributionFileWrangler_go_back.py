# -*- encoding: utf-8 -*-
from abjad import *
import ide
abjad_ide = abjad_ide.idetools.AbjadIDE(is_test=True)


def test_DistributionFileWrangler_go_back_01():

    input_ = 'red~example~score d b q'
    abjad_ide._run(input_=input_)

    titles = [
        'Abjad IDE - scores',
        'Red Example Score (2013)',
        'Red Example Score (2013) - distribution directory',
        'Red Example Score (2013)',
        ]
    assert abjad_ide._transcript.titles == titles


def test_DistributionFileWrangler_go_back_02():

    input_ = 'dd b q'
    abjad_ide._run(input_=input_)

    titles = [
        'Abjad IDE - scores',
        'Abjad IDE - distribution depot',
        'Abjad IDE - scores',
        ]
    assert abjad_ide._transcript.titles == titles