# -*- encoding: utf-8 -*-
from abjad import *
import ide


def test_IOManager_handle_input_01():
    r'''Command repetition works.
    '''

    abjad_ide = ide.tools.idetools.AbjadIDE(is_test=True)
    input_ = '>> . . . q'
    abjad_ide._run(input_=input_)
    titles = [
        'Abjad IDE - scores',
        'Blue Example Score (2013)',
        'Étude Example Score (2013)',
        'Red Example Score (2013)',
        'Blue Example Score (2013)',
        ]
    assert abjad_ide._transcript.titles == titles