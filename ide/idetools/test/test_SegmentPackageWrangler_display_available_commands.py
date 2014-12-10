# -*- encoding: utf-8 -*-
from abjad import *
import ide
abjad_ide = ide.idetools.AbjadIDE(is_test=True)


def test_SegmentPackageWrangler_display_available_commands_01():
    
    input_ = 'red~example~score g ?? q'
    abjad_ide._run(input_=input_)
    contents = abjad_ide._transcript.contents

    assert 'segments directory - available commands' in contents


def test_SegmentPackageWrangler_display_available_commands_02():
    
    input_ = 'gg ?? q'
    abjad_ide._run(input_=input_)
    contents = abjad_ide._transcript.contents

    assert 'Abjad IDE - segments depot - available commands' in contents