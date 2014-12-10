# -*- encoding: utf-8 -*-
from abjad import *
import ide
abjad_ide = ide.idetools.AbjadIDE(is_test=True)


def test_MakerFileWrangler_display_avialable_commands_01():
    
    input_ = 'red~example~score k ?? q'
    abjad_ide._run(input_=input_)
    contents = abjad_ide._transcript.contents

    assert 'makers directory - available commands' in contents


def test_MakerFileWrangler_display_avialable_commands_02():
    
    input_ = 'kk ?? q'
    abjad_ide._run(input_=input_)
    contents = abjad_ide._transcript.contents

    assert 'Abjad IDE - makers depot - available commands' in contents