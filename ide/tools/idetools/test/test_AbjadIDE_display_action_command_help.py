# -*- encoding: utf-8 -*-
from abjad import *
import ide
abjad_ide = ide.tools.idetools.AbjadIDE(is_test=True)


def test_AbjadIDE_display_action_command_help_01():
    r'''In material package.
    '''
    
    input_ = 'red~example~score m tempo~inventory ? q'
    abjad_ide._run_main_menu(input_=input_)
    contents = abjad_ide._io_manager._transcript.contents

    assert 'tempo inventory - action commands' in contents


def test_AbjadIDE_display_action_command_help_02():
    r'''In segment package.
    '''
    
    input_ = 'red~example~score g A ? q'
    abjad_ide._run_main_menu(input_=input_)
    contents = abjad_ide._io_manager._transcript.contents

    assert 'segments directory - A - action commands' in contents


def test_AbjadIDE_display_action_command_help_03():
    r'''In score directory.
    '''
    
    input_ = 'red~example~score ? q'
    abjad_ide._run_main_menu(input_=input_)
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
        '    edit abbreviations file (abb)',
        '    edit score stylesheet (sty)',
        '    open lilypond log (log)',
        '',
        '    check package (ck)',
        '    open score pdf (so)',
        '',
        '>',
    ]

    input_ = 'red~example~score ? q'
    abjad_ide._run_main_menu(input_=input_)
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
        '    edit abbreviations file (abb)',
        '    edit score stylesheet (sty)',
        '    open lilypond log (log)',
        '',
        '    check definition py (dc)',
        '    check package (ck)',
        '    edit __illustrate__.py (le)',
        '    edit definition py (de)',
        '    edit illustration ly (ie)',
        '    generate __illustrate__.py (gl)',
        '    interpret illustration ly (ii)',
        '    open illustration pdf (io)',
        '',
        '>',
    ]

    input_ = 'red~example~score m magic~numbers ? q'
    abjad_ide._run_main_menu(input_=input_)
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
        '    edit abbreviations file (abb)',
        '    edit score stylesheet (sty)',
        '    open lilypond log (log)',
        '',
        '    check definition py (dc)',
        '    check package (ck)',
        '    edit definition py (de)',
        '    edit illustration ly (ie)',
        '    illustrate definition py (i)',
        '    interpret illustration ly (ii)',
        '    open illustration pdf (io)',
        '',
        '>',
    ]

    input_ = 'red~example~score g A ? q'
    abjad_ide._run_main_menu(input_=input_)
    transcript_entry = abjad_ide._io_manager._transcript.entries[-3]


    for line, actual_line in zip(lines, transcript_entry.lines):
        assert line == actual_line


def test_AbjadIDE_display_action_command_help_07():
    r'''Displays correct title at home.
    '''
    
    input_ = '? q'
    abjad_ide._run_main_menu(input_=input_)
    contents = abjad_ide._io_manager._transcript.contents

    assert 'Abjad IDE - all score directories - action commands' in contents


def test_AbjadIDE_display_action_command_help_08():
    r'''Displays correct title in build directory.
    '''
    
    input_ = 'red~example~score u ? q'
    abjad_ide._run_main_menu(input_=input_)
    contents = abjad_ide._io_manager._transcript.contents

    assert 'build directory - action commands' in contents


def test_AbjadIDE_display_action_command_help_09():
    r'''Displays correct title with all build files.
    '''
    
    input_ = 'uu ? q'
    abjad_ide._run_main_menu(input_=input_)
    contents = abjad_ide._io_manager._transcript.contents

    assert 'Abjad IDE - all build directories - action commands' in contents


def test_AbjadIDE_display_action_command_help_10():
    r'''Displays only one blank line after title.
    '''
    
    input_ = '? q'
    abjad_ide._run_main_menu(input_=input_)
    contents = abjad_ide._io_manager._transcript.contents

    title = 'Abjad IDE - all score directories - action commands'
    first_blank_line = ''
    first_real_line = '    display action command help (?)'
    string = '\n'.join([title, first_blank_line, first_real_line])
    assert string in contents


def test_AbjadIDE_display_action_command_help_11():
    r'''Works at home screen.
    '''

    lines = [
        'Abjad IDE - all score directories - action commands',
        '',
        '    display action command help (?)',
        '    invoke shell (!)',
        '',
        '    open lilypond log (log)',
        '',
        '    check every package (ck*)',
        '    open every score pdf (so*)',
        '',
        '    git add every package (add*)',
        '    git commit every package (ci*)',
        '    git revert every package (revert*)',
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
    abjad_ide._run_main_menu(input_=input_)
    transcript_entry = abjad_ide._io_manager._transcript.entries[-3]

    for line, actual_line in zip(lines, transcript_entry.lines):
        assert line == actual_line


def test_AbjadIDE_display_action_command_help_12():
    r'''Works at all materials directories.
    '''

    lines = [
        'Abjad IDE - all materials directories - action commands',
        '',
        '    display action command help (?)',
        '    invoke shell (!)',
        '',
        '    open lilypond log (log)',
        '',
        '    copy (cp)',
        '    new (new)',
        '    remove (rm)',
        '    rename (ren)',
        '',
        '>',
        ]

    input_ = 'mm ? q'
    abjad_ide._run_main_menu(input_=input_)
    transcript_entry = abjad_ide._io_manager._transcript.entries[-3]

    for line, actual_line in zip(lines, transcript_entry.lines):
        assert line == actual_line



def test_AbjadIDE_display_action_command_help_13():
    r'''Works at all stylesheets directories.
    '''

    lines = [
        'Abjad IDE - all stylesheets directories - action commands',
        '',
        '    display action command help (?)',
        '    invoke shell (!)',
        '',
        '    open lilypond log (log)',
        '',
        '    copy (cp)',
        '    new (new)',
        '    remove (rm)',
        '    rename (ren)',
        '',
        '>',
        ]

    input_ = 'yy ? q'
    abjad_ide._run_main_menu(input_=input_)
    transcript_entry = abjad_ide._io_manager._transcript.entries[-3]

    for line, actual_line in zip(lines, transcript_entry.lines):
        assert line == actual_line


def test_AbjadIDE_display_action_command_help_14():
    r'''Works in materials directory.
    '''

    lines = [
        'Red Example Score (2013) - materials directory - action commands',
        '',
        '    display action command help (?)',
        '    invoke shell (!)',
        '',
        '    edit abbreviations file (abb)',
        '    edit score stylesheet (sty)',
        '    open lilypond log (log)',
        '',
        '    check every definition py (dc*)',
        '    edit every definition py (de*)',
        '    interpret every illustration ly (ii*)',
        '    open every illustration pdf (io*)',
        '',
        '    copy (cp)',
        '    new (new)',
        '    remove (rm)',
        '    rename (ren)',
        '',
        '>',
        ]

    input_ = 'red~example~score m ? q'
    abjad_ide._run_main_menu(input_=input_)
    transcript_entry = abjad_ide._io_manager._transcript.entries[-3]

    for line, actual_line in zip(lines, transcript_entry.lines):
        assert line == actual_line


def test_AbjadIDE_display_action_command_help_15():
    r'''Works in segments directory.
    '''

    lines = [
        'Red Example Score (2013) - segments directory - action commands',
        '',
        '    display action command help (?)',
        '    invoke shell (!)',
        '',
        '    edit abbreviations file (abb)',
        '    edit score stylesheet (sty)',
        '    open lilypond log (log)',
        '',
        '    check every definition py (dc*)',
        '    edit every definition py (de*)',
        '    illustrate every definition py (di*)',
        '    interpret every illustration ly (ii*)',
        '    open every illustration pdf (io*)',
        '',
        '    copy (cp)',
        '    new (new)',
        '    remove (rm)',
        '    rename (ren)',
        '',
        '>',
        ]

    input_ = 'red~example~score g ? q'
    abjad_ide._run_main_menu(input_=input_)
    transcript_entry = abjad_ide._io_manager._transcript.entries[-3]

    for line, actual_line in zip(lines, transcript_entry.lines):
        assert line == actual_line


def test_AbjadIDE_display_action_command_help_16():
    r'''Works in stylesheets directory.
    '''

    lines = [
        'Red Example Score (2013) - stylesheets directory - action commands',
        '',
        '    display action command help (?)',
        '    invoke shell (!)',
        '',
        '    edit abbreviations file (abb)',
        '    edit score stylesheet (sty)',
        '    open lilypond log (log)',
        '',
        '    copy (cp)',
        '    new (new)',
        '    remove (rm)',
        '    rename (ren)',
        '',
        '>',
        ]

    input_ = 'red~example~score y ? q'
    abjad_ide._run_main_menu(input_=input_)
    transcript_entry = abjad_ide._io_manager._transcript.entries[-3]

    for line, actual_line in zip(lines, transcript_entry.lines):
        assert line == actual_line