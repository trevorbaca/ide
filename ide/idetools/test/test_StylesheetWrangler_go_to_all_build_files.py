# -*- encoding: utf-8 -*-
from abjad import *
import abjad_ide
abjad_ide = abjad_ide.idetools.AbjadIDE(is_test=True)


def test_StylesheetWrangler_go_to_all_build_files_01():
    r'''From stylesheets directory to build depot.
    '''

    input_ = 'red~example~score y uu q'
    abjad_ide._run(input_=input_)
    titles = [
        'Abjad IDE - scores',
        'Red Example Score (2013)',
        'Red Example Score (2013) - stylesheets directory',
        'Abjad IDE - build depot',
        ]
    assert abjad_ide._transcript.titles == titles


def test_StylesheetWrangler_go_to_all_build_files_02():
    r'''From stylesheets depot to build depot.
    '''

    input_ = 'yy uu q'
    abjad_ide._run(input_=input_)
    titles = [
        'Abjad IDE - scores',
        'Abjad IDE - stylesheets depot',
        'Abjad IDE - build depot',
        ]
    assert abjad_ide._transcript.titles == titles