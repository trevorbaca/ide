# -*- encoding: utf-8 -*-
from abjad import *
import ide
abjad_ide = ide.idetools.AbjadIDE(is_test=True)


def test_MaterialPackageWrangler_display_session_variables_01():
    
    input_ = 'red~example~score m sv q'
    abjad_ide._run(input_=input_)
    contents = abjad_ide._transcript.contents

    assert 'command_history' in contents
    assert 'controller_stack' in contents


def test_MaterialPackageWrangler_display_session_variables_02():
    
    input_ = 'mm sv q'
    abjad_ide._run(input_=input_)
    contents = abjad_ide._transcript.contents

    assert 'command_history' in contents
    assert 'controller_stack' in contents