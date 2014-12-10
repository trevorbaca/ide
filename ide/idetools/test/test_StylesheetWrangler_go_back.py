# -*- encoding: utf-8 -*-
from abjad import *
import ide
abjad_ide = ide.idetools.AbjadIDE(is_test=True)


def test_StylesheetWrangler_go_back_01():

    input_ = 'red~example~score y b q'
    abjad_ide._run(input_=input_)

    titles = [
        'Abjad IDE - scores',
        'Red Example Score (2013)',
        'Red Example Score (2013) - stylesheets directory',
        'Red Example Score (2013)',
        ]
    assert abjad_ide._transcript.titles == titles


def test_StylesheetWrangler_go_back_02():

    input_ = 'yy b q'
    abjad_ide._run(input_=input_)

    titles = [
        'Abjad IDE - scores',
        'Abjad IDE - stylesheets depot',
        'Abjad IDE - scores',
        ]
    assert abjad_ide._transcript.titles == titles