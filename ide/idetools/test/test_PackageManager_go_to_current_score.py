# -*- encoding: utf-8 -*-
from abjad import *
import ide
abjad_ide = ide.idetools.AbjadIDE(is_test=True)


def test_PackageManager_go_to_current_score_01():
    r'''From material package.
    '''

    input_ = 'red~example~score m tempo~inventory s q'
    abjad_ide._run(input_=input_)

    titles = [
        'Abjad IDE - scores',
        'Red Example Score (2013)',
        'Red Example Score (2013) - materials directory',
        'Red Example Score (2013) - materials directory - tempo inventory',
        'Red Example Score (2013)',
        ]
    assert abjad_ide._transcript.titles == titles


def test_PackageManager_go_to_current_score_02():
    r'''From segment package.
    '''

    input_ = 'red~example~score g A s q'
    abjad_ide._run(input_=input_)
    titles = [
        'Abjad IDE - scores',
        'Red Example Score (2013)',
        'Red Example Score (2013) - segments directory',
        'Red Example Score (2013) - segments directory - A',
        'Red Example Score (2013)',
        ]
    assert abjad_ide._transcript.titles == titles


def test_PackageManager_go_to_current_score_03():
    r'''From score package.
    '''

    input_ = 'red~example~score s q'
    abjad_ide._run(input_=input_)

    titles = [
        'Abjad IDE - scores',
        'Red Example Score (2013)',
        'Red Example Score (2013)',
        ]
    assert abjad_ide._transcript.titles == titles