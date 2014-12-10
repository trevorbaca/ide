# -*- encoding: utf-8 -*-
from abjad import *
import abjad_ide
abjad_ide = abjad_ide.idetools.AbjadIDE(is_test=True)


def test_MakerFileWrangler_go_to_all_materials_01():
    r'''From makers directory to materials depot.
    '''

    input_ = 'red~example~score k mm q'
    abjad_ide._run(input_=input_)
    titles = [
        'Abjad IDE - scores',
        'Red Example Score (2013)',
        'Red Example Score (2013) - makers directory',
        'Abjad IDE - materials depot',
        ]
    assert abjad_ide._transcript.titles == titles


def test_MakerFileWrangler_go_to_all_materials_02():
    r'''From makers depot to materials depot.
    '''

    input_ = 'kk mm q'
    abjad_ide._run(input_=input_)
    titles = [
        'Abjad IDE - scores',
        'Abjad IDE - makers depot',
        'Abjad IDE - materials depot',
        ]
    assert abjad_ide._transcript.titles == titles