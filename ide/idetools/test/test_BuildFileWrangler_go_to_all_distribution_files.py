# -*- encoding: utf-8 -*-
from abjad import *
import ide
abjad_ide = abjad_ide.idetools.AbjadIDE(is_test=True)


def test_BuildFileWrangler_go_to_all_distribution_files_01():
    r'''From score build files to all distribution files.
    '''

    input_ = 'red~example~score u dd q'
    abjad_ide._run(input_=input_)
    titles = [
        'Abjad IDE - scores',
        'Red Example Score (2013)',
        'Red Example Score (2013) - build directory',
        'Abjad IDE - distribution depot',
        ]
    assert abjad_ide._transcript.titles == titles


def test_BuildFileWrangler_go_to_all_distribution_files_02():
    r'''From all build files to all distribution files.
    '''

    input_ = 'uu dd q'
    abjad_ide._run(input_=input_)
    titles = [
        'Abjad IDE - scores',
        'Abjad IDE - build depot',
        'Abjad IDE - distribution depot',
        ]
    assert abjad_ide._transcript.titles == titles