# -*- encoding: utf-8 -*-
from abjad import *
import ide
abjad_ide = abjad_ide.idetools.AbjadIDE(is_test=True)


def test_MaterialPackageWrangler_go_to_all_stylesheets_01():
    r'''From score materials to all stylesheets.
    '''

    input_ = 'red~example~score m yy q'
    abjad_ide._run(input_=input_)
    titles = [
        'Abjad IDE - scores',
        'Red Example Score (2013)',
        'Red Example Score (2013) - materials directory',
        'Abjad IDE - stylesheets depot',
        ]
    assert abjad_ide._transcript.titles == titles


def test_MaterialPackageWrangler_go_to_all_stylesheets_02():
    r'''From all materials to all stylesheets.
    '''

    input_ = 'mm yy q'
    abjad_ide._run(input_=input_)
    titles = [
        'Abjad IDE - scores',
        'Abjad IDE - materials depot',
        'Abjad IDE - stylesheets depot',
        ]
    assert abjad_ide._transcript.titles == titles