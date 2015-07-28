# -*- encoding: utf-8 -*-
from abjad import *
import ide
abjad_ide = ide.idetools.AbjadIDE(is_test=True)


def test_PackageManager_go_to_next_package_01():
    r'''From material package.
    '''

    input_ = 'red~example~score m tempo~inventory > q'
    abjad_ide._run(input_=input_)
    titles = [
        'Abjad IDE - scores',
        'Red Example Score (2013)',
        'Red Example Score (2013) - materials directory',
        'Red Example Score (2013) - materials directory - tempo inventory',
        'Red Example Score (2013) - materials directory - time signatures',
        ]
    assert abjad_ide._transcript.titles == titles


def test_PackageManager_go_to_next_package_02():
    r'''From segment package.
    '''

    input_ = 'red~example~score g A > q'
    abjad_ide._run(input_=input_)
    titles = [
        'Abjad IDE - scores',
        'Red Example Score (2013)',
        'Red Example Score (2013) - segments directory',
        'Red Example Score (2013) - segments directory - A',
        'Red Example Score (2013) - segments directory - B',
        ]
    assert abjad_ide._transcript.titles == titles