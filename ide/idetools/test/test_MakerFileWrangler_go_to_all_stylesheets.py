# -*- encoding: utf-8 -*-
from abjad import *
import ide
abjad_ide = abjad_ide.idetools.AbjadIDE(is_test=True)


def test_MakerFileWrangler_go_to_all_stylesheets_01():
    r'''From makers directory to stylesheets depot.
    '''

    input_ = 'red~example~score k yy q'
    abjad_ide._run(input_=input_)
    titles = [
        'Abjad IDE - scores',
        'Red Example Score (2013)',
        'Red Example Score (2013) - makers directory',
        'Abjad IDE - stylesheets depot',
        ]
    assert abjad_ide._transcript.titles == titles


def test_MakerFileWrangler_go_to_all_stylesheets_02():
    r'''From makers depot to stylesheets depot.
    '''

    input_ = 'kk yy q'
    abjad_ide._run(input_=input_)
    titles = [
        'Abjad IDE - scores',
        'Abjad IDE - makers depot',
        'Abjad IDE - stylesheets depot',
        ]
    assert abjad_ide._transcript.titles == titles