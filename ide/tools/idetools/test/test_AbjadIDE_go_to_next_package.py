# -*- encoding: utf-8 -*-
import pytest
from abjad import *
import ide
abjad_ide = ide.tools.idetools.AbjadIDE(is_test=True)
pytest.skip('reimplement nonstatally')


def test_AbjadIDE_go_to_next_package_01():
    r'''From material package.
    '''

    input_ = 'red~example~score m tempo~inventory > q'
    abjad_ide._run_main_menu(input_=input_)
    titles = [
        'Abjad IDE - all score directories',
        'Red Example Score (2013)',
        'Red Example Score (2013) - materials directory',
        'Red Example Score (2013) - materials directory - tempo inventory',
        'Red Example Score (2013) - materials directory - time signatures',
        ]
    assert abjad_ide._io_manager._transcript.titles == titles


def test_AbjadIDE_go_to_next_package_02():
    r'''From segment package.
    '''

    input_ = 'red~example~score g A > q'
    abjad_ide._run_main_menu(input_=input_)
    titles = [
        'Abjad IDE - all score directories',
        'Red Example Score (2013)',
        'Red Example Score (2013) - segments directory',
        'Red Example Score (2013) - segments directory - A',
        'Red Example Score (2013) - segments directory - B',
        ]
    assert abjad_ide._io_manager._transcript.titles == titles