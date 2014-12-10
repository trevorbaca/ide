# -*- encoding: utf-8 -*-
from abjad import *
import abjad_ide
abjad_ide = abjad_ide.idetools.AbjadIDE(is_test=True)


def test_DistributionFileWrangler_display_available_commands_01():
    
    input_ = 'red~example~score d ?? q'
    abjad_ide._run(input_=input_)
    contents = abjad_ide._transcript.contents

    assert 'distribution directory - available commands' in contents


def test_DistributionFileWrangler_display_available_commands_02():
    
    input_ = 'dd ?? q'
    abjad_ide._run(input_=input_)
    contents = abjad_ide._transcript.contents

    string = 'Abjad IDE - distribution depot - available commands'
    assert string in contents