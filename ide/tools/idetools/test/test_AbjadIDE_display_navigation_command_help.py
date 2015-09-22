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
        '    go to build directory (bb)',
        '    go to distribution directory (dd)',
        '    go to etc directory (ee)',
        '    go to makers directory (kk)',
        '    go to materials directory (mm)',
        '    go to score directory (ss)',
        '    go to score package wrapper (ww)',
        '    go to segments directory (gg)',
        '    go to stylesheets directory (yy)',
        '    go to test directory (tt)',
        '',
        '>',
        ]

    input_ = 'red~example~score ; q'
    abjad_ide._start(input_=input_)
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
        '    go to build directory (bb)',
        '    go to distribution directory (dd)',
        '    go to etc directory (ee)',
        '    go to makers directory (kk)',
        '    go to materials directory (mm)',
        '    go to score directory (ss)',
        '    go to score package wrapper (ww)',
        '    go to segments directory (gg)',
        '    go to stylesheets directory (yy)',
        '    go to test directory (tt)',
        '',
        '>',
    ]

    input_ = 'red~example~score mm magic~numbers ; q'
    abjad_ide._start(input_=input_)
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
        '    go to build directory (bb)',
        '    go to distribution directory (dd)',
        '    go to etc directory (ee)',
        '    go to makers directory (kk)',
        '    go to materials directory (mm)',
        '    go to score directory (ss)',
        '    go to score package wrapper (ww)',
        '    go to segments directory (gg)',
        '    go to stylesheets directory (yy)',
        '    go to test directory (tt)',
        '',
        '>',
    ]

    input_ = 'red~example~score gg A ; q'
    abjad_ide._start(input_=input_)
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
    abjad_ide._start(input_=input_)
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
        '    go to build directory (bb)',
        '    go to distribution directory (dd)',
        '    go to etc directory (ee)',
        '    go to makers directory (kk)',
        '    go to materials directory (mm)',
        '    go to score directory (ss)',
        '    go to score package wrapper (ww)',
        '    go to segments directory (gg)',
        '    go to stylesheets directory (yy)',
        '    go to test directory (tt)',
        '',
        '    set view (ws)',
        '',
        '>',
        ]

    input_ = 'red~example~score mm ; q'
    abjad_ide._start(input_=input_)
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
        '    go to build directory (bb)',
        '    go to distribution directory (dd)',
        '    go to etc directory (ee)',
        '    go to makers directory (kk)',
        '    go to materials directory (mm)',
        '    go to score directory (ss)',
        '    go to score package wrapper (ww)',
        '    go to segments directory (gg)',
        '    go to stylesheets directory (yy)',
        '    go to test directory (tt)',
        '',
        '    set view (ws)',
        '',
        '>',
        ]

    input_ = 'red~example~score gg ; q'
    abjad_ide._start(input_=input_)
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
        '    go to build directory (bb)',
        '    go to distribution directory (dd)',
        '    go to etc directory (ee)',
        '    go to makers directory (kk)',
        '    go to materials directory (mm)',
        '    go to score directory (ss)',
        '    go to score package wrapper (ww)',
        '    go to segments directory (gg)',
        '    go to stylesheets directory (yy)',
        '    go to test directory (tt)',
        '',
        '    set view (ws)',
        '',
        '>',
        ]

    input_ = 'red~example~score yy ; q'
    abjad_ide._start(input_=input_)
    transcript_entry = abjad_ide._io_manager._transcript.entries[-3]

    for line, actual_line in zip(lines, transcript_entry.lines):
        assert line == actual_line