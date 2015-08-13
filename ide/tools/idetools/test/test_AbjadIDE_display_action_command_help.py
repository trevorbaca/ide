# -*- encoding: utf-8 -*-
import pytest
from abjad import *
import ide
abjad_ide = ide.tools.idetools.AbjadIDE(is_test=True)
pytest.skip('reimplement nonstatally')


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