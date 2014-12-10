# -*- encoding: utf-8 -*-
from abjad import *
import ide
abjad_ide = ide.idetools.AbjadIDE(is_test=True)


def test_ScorePackageWrangler_display_session_variables_01():
    
    input_ = 'sv q'
    abjad_ide._run(input_=input_)
    contents = abjad_ide._transcript.contents

    assert 'command_history' in contents
    assert 'controller_stack' in contents