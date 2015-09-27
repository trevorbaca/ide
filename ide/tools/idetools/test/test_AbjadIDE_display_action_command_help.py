# -*- coding: utf-8 -*-
from abjad import *
import ide
abjad_ide = ide.tools.idetools.AbjadIDE(is_test=True)


def test_AbjadIDE_display_action_command_help_01():
    r'''In package wrapper.
    '''

    lines = [
        'Red Example Score (2013) - package wrapper - action commands',
        '',
        '    display action command help (?)',
        '    invoke shell (!)',
        '',
        '    aliases - edit (als)',
        '    log - edit (log)',
        '',
        '    copy (cp)',
        '    new (new)',
        '    remove (rm)',
        '    rename (ren)',
        '',
        '    git - add (add)',
        '    git - commit (ci)',
        '    git - status (st)',
        '    git - update (up)',
        '',
        '>',
        ]

    input_ = 'red~example~score ww ? q'
    abjad_ide._start(input_=input_)
    transcript_entry = abjad_ide._io_manager._transcript.entries[-3]

    for line, actual_line in zip(lines, transcript_entry.lines):
        assert line == actual_line


def test_AbjadIDE_display_action_command_help_02():
    r'''In material directory.
    '''
    
    input_ = 'red~example~score mm tempo~inventory ? q'
    abjad_ide._start(input_=input_)
    contents = abjad_ide._io_manager._transcript.contents

    assert 'tempo inventory - action commands' in contents


def test_AbjadIDE_display_action_command_help_03():
    r'''In segment directory.
    '''
    
    input_ = 'red~example~score gg A ? q'
    abjad_ide._start(input_=input_)
    contents = abjad_ide._io_manager._transcript.contents

    assert 'segments directory - A - action commands' in contents


def test_AbjadIDE_display_action_command_help_04():
    r'''In score directory.
    '''
    
    input_ = 'red~example~score ? q'
    abjad_ide._start(input_=input_)
    contents = abjad_ide._io_manager._transcript.contents

    assert 'Red Example Score (2013) - action commands' in contents


def test_AbjadIDE_display_action_command_help_05():
    r'''In score directory.
    '''

    lines = [
        'Red Example Score (2013) - action commands',
        '',
        '    display action command help (?)',
        '    invoke shell (!)',
        '',
        '    aliases - edit (als)',
        '    log - edit (log)',
        '',
        '    open score pdf (so)',
        '',
        '    git - add (add)',
        '    git - commit (ci)',
        '    git - status (st)',
        '    git - update (up)',
        '',
        '>',
    ]

    input_ = 'red~example~score ? q'
    abjad_ide._start(input_=input_)
    transcript_entry = abjad_ide._io_manager._transcript.entries[-3]


    for line, actual_line in zip(lines, transcript_entry.lines):
        assert line == actual_line


def test_AbjadIDE_display_action_command_help_06():
    r'''In material directory.
    '''

    lines = [
        'Red Example Score (2013) - materials directory - magic numbers - action commands',
        '',
        '    display action command help (?)',
        '    invoke shell (!)',
        '',
        '    aliases - edit (als)',
        '    log - edit (log)',
        '',
        '    definition file - check (dfk)',
        '    definition file - edit (df)',
        '',
        '    illustrate file - edit (ill)',
        '    illustrate file - make (illm)',
        '',
        '    ly - edit (ly)',
        '    ly - interpret (lyi)',
        '    ly - make (lym)',
        '',
        '    pdf - make (pdfm)',
        '    pdf - open (pdf)',
        '',
        '    copy (cp)',
        '    new (new)',
        '    remove (rm)',
        '    rename (ren)',
        '',
        '    git - add (add)',
        '    git - commit (ci)',
        '    git - status (st)',
        '    git - update (up)',
        '',
        '>',
    ]

    input_ = 'red~example~score mm magic~numbers ? q'
    abjad_ide._start(input_=input_)
    transcript_entry = abjad_ide._io_manager._transcript.entries[-3]


    for line, actual_line in zip(lines, transcript_entry.lines):
        assert line == actual_line


def test_AbjadIDE_display_action_command_help_07():
    r'''In segment directory.
    '''

    lines = [
        'Red Example Score (2013) - segments directory - A - action commands',
        '',
        '    display action command help (?)',
        '    invoke shell (!)',
        '',
        '    aliases - edit (als)',
        '    log - edit (log)',
        '',
        '    definition file - check (dfk)',
        '    definition file - edit (df)',
        '',
        '    ly - edit (ly)',
        '    ly - interpret (lyi)',
        '    ly - make (lym)',
        '',
        '    pdf - make (pdfm)',
        '    pdf - open (pdf)',
        '',
        '    copy (cp)',
        '    new (new)',
        '    remove (rm)',
        '    rename (ren)',
        '',
        '    git - add (add)',
        '    git - commit (ci)',
        '    git - status (st)',
        '    git - update (up)',
        '',
        '>',
    ]

    input_ = 'red~example~score gg A ? q'
    abjad_ide._start(input_=input_)
    transcript_entry = abjad_ide._io_manager._transcript.entries[-3]


    for line, actual_line in zip(lines, transcript_entry.lines):
        assert line == actual_line


def test_AbjadIDE_display_action_command_help_08():
    r'''Displays correct title at home.
    '''
    
    input_ = '? q'
    abjad_ide._start(input_=input_)
    contents = abjad_ide._io_manager._transcript.contents

    assert 'Abjad IDE - all score directories - action commands' in contents


def test_AbjadIDE_display_action_command_help_09():
    r'''Displays correct title in build directory.
    '''
    
    input_ = 'red~example~score bb ? q'
    abjad_ide._start(input_=input_)
    contents = abjad_ide._io_manager._transcript.contents

    assert 'build directory - action commands' in contents


def test_AbjadIDE_display_action_command_help_10():
    r'''Displays only one blank line after title.
    '''
    
    input_ = '? q'
    abjad_ide._start(input_=input_)
    contents = abjad_ide._io_manager._transcript.contents

    title = 'Abjad IDE - all score directories - action commands'
    first_blank_line = ''
    first_real_line = '    open every score pdf (so*)'
    string = '\n'.join([title, first_blank_line, first_real_line])
    assert string in contents


def test_AbjadIDE_display_action_command_help_11():
    r'''In scores directory.
    '''

    lines = [
        'Abjad IDE - all score directories - action commands',
        '',
        '    open every score pdf (so*)',
        '',
        '    display action command help (?)',
        '    invoke shell (!)',
        '',
        '    aliases - edit (als)',
        '    log - edit (log)',
        '',
        '    copy (cp)',
        '    new (new)',
        '    remove (rm)',
        '    rename (ren)',
        '',
        '    git add every package (add*)',
        '    git commit every package (ci*)',
        '    git status every package (st*)',
        '    git update every package (up*)',
        '',
        '>',
        ]

    input_ = '? q'
    abjad_ide._start(input_=input_)
    transcript_entry = abjad_ide._io_manager._transcript.entries[-3]

    for line, actual_line in zip(lines, transcript_entry.lines):
        assert line == actual_line


def test_AbjadIDE_display_action_command_help_12():
    r'''In materials directory.
    '''

    lines = [
        'Red Example Score (2013) - materials directory - action commands',
        '',
        '    every definition file - check (dfk*)',
        '    every definition file - edit (df*)',
        '    every ly - interpret (lyi*)',
        '    every pdf - make (pdfm*)',
        '    every pdf - open (pdf*)',
        '',
        '    display action command help (?)',
        '    invoke shell (!)',
        '',
        '    aliases - edit (als)',
        '    log - edit (log)',
        '',
        '    copy (cp)',
        '    new (new)',
        '    remove (rm)',
        '    rename (ren)',
        '',
        '    git - add (add)',
        '    git - commit (ci)',
        '    git - status (st)',
        '    git - update (up)',
        '',
        '>',
        ]

    input_ = 'red~example~score mm ? q'
    abjad_ide._start(input_=input_)
    transcript_entry = abjad_ide._io_manager._transcript.entries[-3]

    for line, actual_line in zip(lines, transcript_entry.lines):
        assert line == actual_line


def test_AbjadIDE_display_action_command_help_13():
    r'''In segments directory.
    '''

    lines = [
        'Red Example Score (2013) - segments directory - action commands',
        '',
        '    every definition file - check (dfk*)',
        '    every definition file - edit (df*)',
        '    every ly - interpret (lyi*)',
        '    every pdf - make (pdfm*)',
        '    every pdf - open (pdf*)',
        '',
        '    display action command help (?)',
        '    invoke shell (!)',
        '',
        '    aliases - edit (als)',
        '    log - edit (log)',
        '',
        '    copy (cp)',
        '    new (new)',
        '    remove (rm)',
        '    rename (ren)',
        '',
        '    git - add (add)',
        '    git - commit (ci)',
        '    git - status (st)',
        '    git - update (up)',
        '',
        '>',
        ]

    input_ = 'red~example~score gg ? q'
    abjad_ide._start(input_=input_)
    transcript_entry = abjad_ide._io_manager._transcript.entries[-3]

    for line, actual_line in zip(lines, transcript_entry.lines):
        assert line == actual_line


def test_AbjadIDE_display_action_command_help_14():
    r'''In stylesheets directory.
    '''

    lines = [
        'Red Example Score (2013) - stylesheets directory - action commands',
        '',
        '    display action command help (?)',
        '    invoke shell (!)',
        '',
        '    aliases - edit (als)',
        '    log - edit (log)',
        '',
        '    copy (cp)',
        '    new (new)',
        '    remove (rm)',
        '    rename (ren)',
        '',
        '    git - add (add)',
        '    git - commit (ci)',
        '    git - status (st)',
        '    git - update (up)',
        '',
        '>',
        ]

    input_ = 'red~example~score yy ? q'
    abjad_ide._start(input_=input_)
    transcript_entry = abjad_ide._io_manager._transcript.entries[-3]

    for line, actual_line in zip(lines, transcript_entry.lines):
        assert line == actual_line