# -*- coding: utf-8 -*-
from abjad import *
import ide
abjad_ide = ide.tools.idetools.AbjadIDE(is_test=True)


def test_AbjadIDE_display_navigation_command_help_01():
    r'''Works in score directory.
    '''

    lines = [
        'Red Example Score (2013) - view & navigation commands',
        '',
        '    display navigation command help (;)',
        '',
        '    home (h)',
        '    quit (q)',
        '',
        '    go to build directory (u)',
        '    go to distribution directory (d)',
        '    go to etc directory (c)',
        '    go to makers directory (k)',
        '    go to materials directory (m)',
        '    go to score directory (s)',
        '    go to segments directory (g)',
        '    go to stylesheets directory (y)',
        '    go to test directory (t)',
        '',
        '>',
        ]

    input_ = 'red~example~score ; q'
    abjad_ide._run_main_menu(input_=input_)
    transcript_entry = abjad_ide._io_manager._transcript.entries[-3]


    for line, actual_line in zip(lines, transcript_entry.lines):
        assert line == actual_line


def test_AbjadIDE_display_navigation_command_help_02():
    r'''Works in material package.
    '''

    lines = [
        'Red Example Score (2013) - materials directory - magic numbers - view & navigation commands',
        '',
        '    display navigation command help (;)',
        '',
        '    home (h)',
        '    quit (q)',
        '',
        '    go to build directory (u)',
        '    go to distribution directory (d)',
        '    go to etc directory (c)',
        '    go to makers directory (k)',
        '    go to materials directory (m)',
        '    go to score directory (s)',
        '    go to segments directory (g)',
        '    go to stylesheets directory (y)',
        '    go to test directory (t)',
        '',
        '>',
    ]

    input_ = 'red~example~score m magic~numbers ; q'
    abjad_ide._run_main_menu(input_=input_)
    transcript_entry = abjad_ide._io_manager._transcript.entries[-3]


    for line, actual_line in zip(lines, transcript_entry.lines):
        assert line == actual_line


def test_AbjadIDE_display_navigation_command_help_03():
    r'''Works in segment package.
    '''

    lines = [
        'Red Example Score (2013) - segments directory - A - view & navigation commands',
        '',
        '    display navigation command help (;)',
        '',
        '    home (h)',
        '    quit (q)',
        '',
        '    go to build directory (u)',
        '    go to distribution directory (d)',
        '    go to etc directory (c)',
        '    go to makers directory (k)',
        '    go to materials directory (m)',
        '    go to score directory (s)',
        '    go to segments directory (g)',
        '    go to stylesheets directory (y)',
        '    go to test directory (t)',
        '',
        '>',
    ]

    input_ = 'red~example~score g A ; q'
    abjad_ide._run_main_menu(input_=input_)
    transcript_entry = abjad_ide._io_manager._transcript.entries[-3]


    for line, actual_line in zip(lines, transcript_entry.lines):
        assert line == actual_line


def test_AbjadIDE_display_navigation_command_help_04():
    r'''Works at home screen.
    '''

    lines = [
        'Abjad IDE - all score directories - view & navigation commands',
        '',
        '    display navigation command help (;)',
        '',
        '    home (h)',
        '    quit (q)',
        '',
        '    set view (ws)',
        '',
        '>',
        ]

    input_ = '; q'
    abjad_ide._run_main_menu(input_=input_)
    transcript_entry = abjad_ide._io_manager._transcript.entries[-3]

    for line, actual_line in zip(lines, transcript_entry.lines):
        assert line == actual_line


def test_AbjadIDE_display_navigation_command_help_05():
    r'''Works in materials directory.
    '''

    lines = [
        'Red Example Score (2013) - materials directory - view & navigation commands',
        '',
        '    display navigation command help (;)',
        '',
        '    home (h)',
        '    quit (q)',
        '',
        '    go to build directory (u)',
        '    go to distribution directory (d)',
        '    go to etc directory (c)',
        '    go to makers directory (k)',
        '    go to materials directory (m)',
        '    go to score directory (s)',
        '    go to segments directory (g)',
        '    go to stylesheets directory (y)',
        '    go to test directory (t)',
        '',
        '    set view (ws)',
        '',
        '>',
        ]

    input_ = 'red~example~score m ; q'
    abjad_ide._run_main_menu(input_=input_)
    transcript_entry = abjad_ide._io_manager._transcript.entries[-3]

    for line, actual_line in zip(lines, transcript_entry.lines):
        assert line == actual_line


def test_AbjadIDE_display_navigation_command_help_06():
    r'''Works in segments directory.
    '''

    lines = [
        'Red Example Score (2013) - segments directory - view & navigation commands',
        '',
        '    display navigation command help (;)',
        '',
        '    home (h)',
        '    quit (q)',
        '',
        '    go to build directory (u)',
        '    go to distribution directory (d)',
        '    go to etc directory (c)',
        '    go to makers directory (k)',
        '    go to materials directory (m)',
        '    go to score directory (s)',
        '    go to segments directory (g)',
        '    go to stylesheets directory (y)',
        '    go to test directory (t)',
        '',
        '    set view (ws)',
        '',
        '>',
        ]

    input_ = 'red~example~score g ; q'
    abjad_ide._run_main_menu(input_=input_)
    transcript_entry = abjad_ide._io_manager._transcript.entries[-3]

    for line, actual_line in zip(lines, transcript_entry.lines):
        assert line == actual_line


def test_AbjadIDE_display_navigation_command_help_07():
    r'''Works in stylesheets directory.
    '''

    lines = [
        'Red Example Score (2013) - stylesheets directory - view & navigation commands',
        '',
        '    display navigation command help (;)',
        '',
        '    home (h)',
        '    quit (q)',
        '',
        '    go to build directory (u)',
        '    go to distribution directory (d)',
        '    go to etc directory (c)',
        '    go to makers directory (k)',
        '    go to materials directory (m)',
        '    go to score directory (s)',
        '    go to segments directory (g)',
        '    go to stylesheets directory (y)',
        '    go to test directory (t)',
        '',
        '    set view (ws)',
        '',
        '>',
        ]

    input_ = 'red~example~score y ; q'
    abjad_ide._run_main_menu(input_=input_)
    transcript_entry = abjad_ide._io_manager._transcript.entries[-3]

    for line, actual_line in zip(lines, transcript_entry.lines):
        assert line == actual_line