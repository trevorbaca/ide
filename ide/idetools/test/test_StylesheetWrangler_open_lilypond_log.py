# -*- encoding: utf-8 -*-
from abjad import *
import ide
abjad_ide = ide.idetools.AbjadIDE(is_test=True)


def test_StylesheetWrangler_open_lilypond_log_01():
    r'''In score.
    '''

    input_ = 'red~example~score y ll q'
    abjad_ide._run(input_=input_)
    
    assert abjad_ide._session._attempted_to_open_file


def test_StylesheetWrangler_open_lilypond_log_02():
    r'''Out of score.
    '''

    input_ = 'yy ll q'
    abjad_ide._run(input_=input_)
    
    assert abjad_ide._session._attempted_to_open_file