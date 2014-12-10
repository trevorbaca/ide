# -*- encoding: utf-8 -*-
from abjad import *
import ide
abjad_ide = abjad_ide.idetools.AbjadIDE(is_test=True)


def test_MaterialPackageWrangler_go_home_01():
    r'''From materials directory.
    '''

    input_ = 'red~example~score m hh q'
    abjad_ide._run(input_=input_)
    titles = [
        'Abjad IDE - scores',
        'Red Example Score (2013)',
        'Red Example Score (2013) - materials directory',
        'Abjad IDE - home',
        ]
    assert abjad_ide._transcript.titles == titles


def test_MaterialPackageWrangler_go_home_02():
    r'''From materials depot.
    '''

    input_ = 'mm hh q'
    abjad_ide._run(input_=input_)
    titles = [
        'Abjad IDE - scores',
        'Abjad IDE - materials depot',
        'Abjad IDE - home',
        ]
    assert abjad_ide._transcript.titles == titles