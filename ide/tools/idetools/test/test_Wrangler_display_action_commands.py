# -*- encoding: utf-8 -*-
from abjad import *
import ide
abjad_ide = ide.tools.idetools.AbjadIDE(is_test=True)


def test_Wrangler_display_action_commands_01():
    r'''Displays correct title at home.
    '''
    
    input_ = '? q'
    abjad_ide._run(input_=input_)
    contents = abjad_ide._transcript.contents

    assert 'Abjad IDE - all score directories - action commands' in contents


def test_Wrangler_display_action_commands_02():
    r'''Displays correct title in build directory.
    '''
    
    input_ = 'red~example~score u ? q'
    abjad_ide._run(input_=input_)
    contents = abjad_ide._transcript.contents

    assert 'build directory - action commands' in contents


def test_Wrangler_display_action_commands_03():
    r'''Displays correct title with all build files.
    '''
    
    input_ = 'uu ? q'
    abjad_ide._run(input_=input_)
    contents = abjad_ide._transcript.contents

    assert 'Abjad IDE - all build directories - action commands' in contents


def test_Wrangler_display_action_commands_04():
    r'''Displays only one blank line after title.
    '''
    
    input_ = '? q'
    abjad_ide._run(input_=input_)
    contents = abjad_ide._transcript.contents

    title = 'Abjad IDE - all score directories - action commands'
    first_blank_line = ''
    first_real_line = '    copy (cp)'
    string = '\n'.join([title, first_blank_line, first_real_line])
    assert string in contents