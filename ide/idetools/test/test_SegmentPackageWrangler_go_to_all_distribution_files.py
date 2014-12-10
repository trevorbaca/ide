# -*- encoding: utf-8 -*-
from abjad import *
import abjad_ide
abjad_ide = abjad_ide.idetools.AbjadIDE(is_test=True)


def test_SegmentPackageWrangler_go_to_all_distribution_files_01():
    r'''From segments directory to distribution depot.
    '''

    input_ = 'red~example~score g dd q'
    abjad_ide._run(input_=input_)
    titles = [
        'Abjad IDE - scores',
        'Red Example Score (2013)',
        'Red Example Score (2013) - segments directory',
        'Abjad IDE - distribution depot',
        ]
    assert abjad_ide._transcript.titles == titles


def test_SegmentPackageWrangler_go_to_all_distribution_files_02():
    r'''From segments depot to distribution depot.
    '''

    input_ = 'gg dd q'
    abjad_ide._run(input_=input_)
    titles = [
        'Abjad IDE - scores',
        'Abjad IDE - segments depot',
        'Abjad IDE - distribution depot',
        ]
    assert abjad_ide._transcript.titles == titles