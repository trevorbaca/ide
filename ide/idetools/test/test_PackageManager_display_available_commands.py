# -*- encoding: utf-8 -*-
from abjad import *
import ide
abjad_ide = ide.idetools.AbjadIDE(is_test=True)


def test_PackageManager_display_available_commands_01():
    r'''In material package.
    '''
    
    input_ = 'red~example~score m tempo~inventory ? q'
    abjad_ide._run(input_=input_)
    contents = abjad_ide._transcript.contents

    assert 'tempo inventory - available commands' in contents


def test_PackageManager_display_available_commands_02():
    r'''In segment package.
    '''
    
    input_ = 'red~example~score g A ? q'
    abjad_ide._run(input_=input_)
    contents = abjad_ide._transcript.contents

    assert 'segments directory - A - available commands' in contents