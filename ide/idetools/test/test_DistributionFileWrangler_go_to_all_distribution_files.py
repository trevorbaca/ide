# -*- encoding: utf-8 -*-
from abjad import *
import ide
abjad_ide = ide.idetools.AbjadIDE(is_test=True)


def test_DistributionFileWrangler_go_to_all_distribution_files_01():
    r'''From distribution directory to distribution depot.
    '''

    input_ = 'red~example~score d dd q'
    abjad_ide._run(input_=input_)
    titles = [
        'Abjad IDE - scores',
        'Red Example Score (2013)',
        'Red Example Score (2013) - distribution directory',
        'Abjad IDE - distribution depot',
        ]
    assert abjad_ide._transcript.titles == titles


def test_DistributionFileWrangler_go_to_all_distribution_files_02():
    r'''From distribution depot to distribution depot.
    '''

    input_ = 'dd dd q'
    abjad_ide._run(input_=input_)
    titles = [
        'Abjad IDE - scores',
        'Abjad IDE - distribution depot',
        'Abjad IDE - distribution depot',
        ]
    assert abjad_ide._transcript.titles == titles