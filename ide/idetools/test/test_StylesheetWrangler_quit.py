# -*- encoding: utf-8 -*-
from abjad import *
import ide
abjad_ide = ide.idetools.AbjadIDE(is_test=True)


def test_StylesheetWrangler_quit_01():
    
    input_ = 'red~example~score y q'
    abjad_ide._run(input_=input_)
    contents = abjad_ide._transcript.contents

    assert contents


def test_StylesheetWrangler_quit_02():
    
    input_ = 'yy q'
    abjad_ide._run(input_=input_)
    contents = abjad_ide._transcript.contents

    assert contents