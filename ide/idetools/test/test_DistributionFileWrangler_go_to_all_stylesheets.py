# -*- encoding: utf-8 -*-
from abjad import *
import abjad_ide
abjad_ide = abjad_ide.idetools.AbjadIDE(is_test=True)


def test_DistributionFileWrangler_go_to_all_stylesheets_01():
    r'''From distribution directory to stylesheets depot.
    '''

    input_ = 'red~example~score d yy q'
    abjad_ide._run(input_=input_)
    titles = [
        'Abjad IDE - scores',
        'Red Example Score (2013)',
        'Red Example Score (2013) - distribution directory',
        'Abjad IDE - stylesheets depot',
        ]
    assert abjad_ide._transcript.titles == titles


def test_DistributionFileWrangler_go_to_all_stylesheets_02():
    r'''From distribution depot to stylesheets depot.
    '''

    input_ = 'dd yy q'
    abjad_ide._run(input_=input_)
    titles = [
        'Abjad IDE - scores',
        'Abjad IDE - distribution depot',
        'Abjad IDE - stylesheets depot',
        ]
    assert abjad_ide._transcript.titles == titles