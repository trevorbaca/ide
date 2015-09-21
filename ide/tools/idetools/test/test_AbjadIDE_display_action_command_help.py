# -*- coding: utf-8 -*-
from abjad import *
import ide
abjad_ide = ide.tools.idetools.AbjadIDE(is_test=True)


def test_AbjadIDE_display_action_command_help_01():
    r'''In material package.
    '''
    
    input_ = 'red~example~score mm tempo~inventory ? q'
    abjad_ide._start(input_=input_)
    contents = abjad_ide._io_manager._transcript.contents

    assert 'tempo inventory - action commands' in contents


def test_AbjadIDE_display_action_command_help_02():
    r'''In segment package.
    '''
    
    input_ = 'red~example~score gg A ? q'
    abjad_ide._start(input_=input_)
    contents = abjad_ide._io_manager._transcript.contents

    assert 'segments directory - A - action commands' in contents


def test_AbjadIDE_display_action_command_help_03():
    r'''In score directory.
    '''
    
    input_ = 'red~example~score ? q'
    abjad_ide._start(input_=input_)
    contents = abjad_ide._io_manager._transcript.contents

    assert 'Red Example Score (2013) - action commands' in contents


def test_AbjadIDE_display_action_command_help_04():
    r'''Works in score directory.
    '''

    lines = [
        'Red Example Score (2013) - action commands',
        '',
        '    display action command help (?)',
        '    invoke shell (!)',
        '',
        '    abbreviations - edit (abb)',
        '    log - edit (log)',
        '    stylesheet - edit (sty)',
        '',
        '    open score pdf (so)',
        '',
        '>',
    ]

    input_ = 'red~example~score ? q'
    abjad_ide._start(input_=input_)
    transcript_entry = abjad_ide._io_manager._transcript.entries[-3]


    for line, actual_line in zip(lines, transcript_entry.lines):
        assert line == actual_line


def test_AbjadIDE_display_action_command_help_05():
    r'''Works in material package.
    '''

    lines = [
        'Red Example Score (2013) - materials directory - magic numbers - action commands',
        '',
        '    display action command help (?)',
        '    invoke shell (!)',
        '',
        '    abbreviations - edit (abb)',
        '    log - edit (log)',
        '    stylesheet - edit (sty)',
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
        '>',
    ]

    input_ = 'red~example~score mm magic~numbers ? q'
    abjad_ide._start(input_=input_)
    transcript_entry = abjad_ide._io_manager._transcript.entries[-3]


    for line, actual_line in zip(lines, transcript_entry.lines):
        assert line == actual_line


def test_AbjadIDE_display_action_command_help_06():
    r'''Works in segment package.
    '''

    lines = [
        'Red Example Score (2013) - segments directory - A - action commands',
        '',
        '    display action command help (?)',
        '    invoke shell (!)',
        '',
        '    abbreviations - edit (abb)',
        '    log - edit (log)',
        '    stylesheet - edit (sty)',
        '',
        '    definition file - check (dfk)',
        '    definition file - edit (df)',
        '',
        '    ly - edit (ly)',
        '    ly - interpret (lyi)',
        '',
        '    illustrate definition (i)',
        '    pdf - open (pdf)',
        '',
        '    copy (cp)',
        '    new (new)',
        '    remove (rm)',
        '    rename (ren)',
        '',
        '>',
    ]

    input_ = 'red~example~score gg A ? q'
    abjad_ide._start(input_=input_)
    transcript_entry = abjad_ide._io_manager._transcript.entries[-3]


    for line, actual_line in zip(lines, transcript_entry.lines):
        assert line == actual_line


def test_AbjadIDE_display_action_command_help_07():
    r'''Displays correct title at home.
    '''
    
    input_ = '? q'
    abjad_ide._start(input_=input_)
    contents = abjad_ide._io_manager._transcript.contents

    assert 'Abjad IDE - all score directories - action commands' in contents


def test_AbjadIDE_display_action_command_help_08():
    r'''Displays correct title in build directory.
    '''
    
    input_ = 'red~example~score bb ? q'
    abjad_ide._start(input_=input_)
    contents = abjad_ide._io_manager._transcript.contents

    assert 'build directory - action commands' in contents


def test_AbjadIDE_display_action_command_help_09():
    r'''Displays only one blank line after title.
    '''
    
    input_ = '? q'
    abjad_ide._start(input_=input_)
    contents = abjad_ide._io_manager._transcript.contents

    title = 'Abjad IDE - all score directories - action commands'
    first_blank_line = ''
    first_real_line = '    display action command help (?)'
    string = '\n'.join([title, first_blank_line, first_real_line])
    assert string in contents


def test_AbjadIDE_display_action_command_help_10():
    r'''Works at home screen.
    '''

    lines = [
        'Abjad IDE - all score directories - action commands',
        '',
        '    display action command help (?)',
        '    invoke shell (!)',
        '',
        '    log - edit (log)',
        '',
        '    open every score pdf (so*)',
        '',
        '    git add every package (add*)',
        '    git commit every package (ci*)',
        '    git status every package (st*)',
        '    git update every package (up*)',
        '',
        '    copy (cp)',
        '    new (new)',
        '    remove (rm)',
        '    rename (ren)',
        '',
        '>',
        ]

    input_ = '? q'
    abjad_ide._start(input_=input_)
    transcript_entry = abjad_ide._io_manager._transcript.entries[-3]

    for line, actual_line in zip(lines, transcript_entry.lines):
        assert line == actual_line


def test_AbjadIDE_display_action_command_help_11():
    r'''Works in materials directory.
    '''

    lines = [
        'Red Example Score (2013) - materials directory - action commands',
        '',
        '    display action command help (?)',
        '    invoke shell (!)',
        '',
        '    abbreviations - edit (abb)',
        '    log - edit (log)',
        '    stylesheet - edit (sty)',
        '',
        '    check every definition file (dfk*)',
        '    edit every definition file (df*)',
        '    interpret every ly (lyi*)',
        '    open every illustration pdf (io*)',
        '',
        '    copy (cp)',
        '    new (new)',
        '    remove (rm)',
        '    rename (ren)',
        '',
        '>',
        ]

    input_ = 'red~example~score mm ? q'
    abjad_ide._start(input_=input_)
    transcript_entry = abjad_ide._io_manager._transcript.entries[-3]

    for line, actual_line in zip(lines, transcript_entry.lines):
        assert line == actual_line


def test_AbjadIDE_display_action_command_help_12():
    r'''Works in segments directory.
    '''

    lines = [
        'Red Example Score (2013) - segments directory - action commands',
        '',
        '    display action command help (?)',
        '    invoke shell (!)',
        '',
        '    abbreviations - edit (abb)',
        '    log - edit (log)',
        '    stylesheet - edit (sty)',
        '',
        '    check every definition file (dfk*)',
        '    edit every definition file (df*)',
        '    illustrate every definition (di*)',
        '    interpret every ly (lyi*)',
        '    open every illustration pdf (io*)',
        '',
        '    copy (cp)',
        '    new (new)',
        '    remove (rm)',
        '    rename (ren)',
        '',
        '>',
        ]

    input_ = 'red~example~score gg ? q'
    abjad_ide._start(input_=input_)
    transcript_entry = abjad_ide._io_manager._transcript.entries[-3]

    for line, actual_line in zip(lines, transcript_entry.lines):
        assert line == actual_line


def test_AbjadIDE_display_action_command_help_13():
    r'''Works in stylesheets directory.
    '''

    lines = [
        'Red Example Score (2013) - stylesheets directory - action commands',
        '',
        '    display action command help (?)',
        '    invoke shell (!)',
        '',
        '    abbreviations - edit (abb)',
        '    log - edit (log)',
        '    stylesheet - edit (sty)',
        '',
        '    copy (cp)',
        '    new (new)',
        '    remove (rm)',
        '    rename (ren)',
        '',
        '>',
        ]

    input_ = 'red~example~score yy ? q'
    abjad_ide._start(input_=input_)
    transcript_entry = abjad_ide._io_manager._transcript.entries[-3]

    for line, actual_line in zip(lines, transcript_entry.lines):
        assert line == actual_line