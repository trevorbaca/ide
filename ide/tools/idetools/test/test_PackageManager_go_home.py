# -*- encoding: utf-8 -*-
from abjad import *
import ide
abjad_ide = ide.tools.idetools.AbjadIDE(is_test=True)


def test_PackageManager_go_home_01():
    r'''From material package.
    '''

    input_ = 'red~example~score m tempo~inventory h q'
    abjad_ide._run(input_=input_)

    titles = [
        'Abjad IDE - all score directories',
        'Red Example Score (2013)',
        'Red Example Score (2013) - materials directory',
        'Red Example Score (2013) - materials directory - tempo inventory',
        'Abjad IDE - all score directories',
        ]
    assert abjad_ide._io_manager._transcript.titles == titles


def test_PackageManager_go_home_02():
    r'''From segment package.
    '''

    input_ = 'red~example~score g A h q'
    abjad_ide._run(input_=input_)
    titles = [
        'Abjad IDE - all score directories',
        'Red Example Score (2013)',
        'Red Example Score (2013) - segments directory',
        'Red Example Score (2013) - segments directory - A',
        'Abjad IDE - all score directories',
        ]
    assert abjad_ide._io_manager._transcript.titles == titles


def test_PackageManager_go_home_03():
    r'''From score package.
    '''

    input_ = 'red~example~score h q'
    abjad_ide._run(input_=input_)

    titles = [
        'Abjad IDE - all score directories',
        'Red Example Score (2013)',
        'Abjad IDE - all score directories',
        ]
    assert abjad_ide._io_manager._transcript.titles == titles