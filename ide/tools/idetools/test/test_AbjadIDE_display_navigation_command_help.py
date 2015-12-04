# -*- coding: utf-8 -*-
from abjad import *
import ide
abjad_ide = ide.tools.idetools.AbjadIDE(is_test=True)


def test_AbjadIDE_display_navigation_command_help_01():
    r'''In score directory.
    '''

    lines = [
        'Red Example Score (2013) - navigation commands',
        '',
        '    display navigation command help (;)',
        '',
        '    back (-)',
        '    home (h)',
        '    quit (q)',
        '',
        '    go to build directory (bb)',
        '    go to distribution directory (dd)',
        '    go to etc directory (ee)',
        '    go to materials directory (mm)',
        '    go to score directory (ss)',
        '    go to score package wrapper (ww)',
        '    go to segments directory (gg)',
        '    go to stylesheets directory (yy)',
        '    go to test directory (tt)',
        '    go to tools directory (oo)',
        '',
        '>',
        ]

    input_ = 'red~example~score ; q'
    abjad_ide._start(input_=input_)
    transcript_entry = abjad_ide._io_manager._transcript.entries[-3]

    for line, actual_line in zip(lines, transcript_entry.lines):
        assert line == actual_line


def test_AbjadIDE_display_navigation_command_help_02():
    r'''In material directory.
    '''

    lines = [
        'Red Example Score (2013) - materials directory - magic numbers - navigation commands',
        '',
        '    display navigation command help (;)',
        '',
        '    back (-)',
        '    home (h)',
        '    quit (q)',
        '',
        '    go to build directory (bb)',
        '    go to distribution directory (dd)',
        '    go to etc directory (ee)',
        '    go to materials directory (mm)',
        '    go to score directory (ss)',
        '    go to score package wrapper (ww)',
        '    go to segments directory (gg)',
        '    go to stylesheets directory (yy)',
        '    go to test directory (tt)',
        '    go to tools directory (oo)',
        '',
        '    go to next package (>)',
        '    go to previous package (<)',
        '',
        '>',
    ]

    input_ = 'red~example~score mm magic~numbers ; q'
    abjad_ide._start(input_=input_)
    transcript_entry = abjad_ide._io_manager._transcript.entries[-3]


    for line, actual_line in zip(lines, transcript_entry.lines):
        assert line == actual_line


def test_AbjadIDE_display_navigation_command_help_03():
    r'''In segment directory.
    '''

    lines = [
        'Red Example Score (2013) - segments directory - A - navigation commands',
        '',
        '    display navigation command help (;)',
        '',
        '    back (-)',
        '    home (h)',
        '    quit (q)',
        '',
        '    go to build directory (bb)',
        '    go to distribution directory (dd)',
        '    go to etc directory (ee)',
        '    go to materials directory (mm)',
        '    go to score directory (ss)',
        '    go to score package wrapper (ww)',
        '    go to segments directory (gg)',
        '    go to stylesheets directory (yy)',
        '    go to test directory (tt)',
        '    go to tools directory (oo)',
        '',
        '    go to next package (>)',
        '    go to previous package (<)',
        '',
        '>',
    ]

    input_ = 'red~example~score gg A ; q'
    abjad_ide._start(input_=input_)
    transcript_entry = abjad_ide._io_manager._transcript.entries[-3]


    for line, actual_line in zip(lines, transcript_entry.lines):
        assert line == actual_line


def test_AbjadIDE_display_navigation_command_help_04():
    r'''In scores directory.
    '''

    lines = [
        'Abjad IDE - all score directories - navigation commands',
        '',
        '    display navigation command help (;)',
        '',
        '    back (-)',
        '    home (h)',
        '    quit (q)',
        '',
        '>',
        ]

    input_ = '; q'
    abjad_ide._start(input_=input_)
    transcript_entry = abjad_ide._io_manager._transcript.entries[-3]

    for line, actual_line in zip(lines, transcript_entry.lines):
        assert line == actual_line


def test_AbjadIDE_display_navigation_command_help_05():
    r'''In materials directory.
    '''

    lines = [
        'Red Example Score (2013) - materials directory - navigation commands',
        '',
        '    display navigation command help (;)',
        '',
        '    back (-)',
        '    home (h)',
        '    quit (q)',
        '',
        '    go to build directory (bb)',
        '    go to distribution directory (dd)',
        '    go to etc directory (ee)',
        '    go to materials directory (mm)',
        '    go to score directory (ss)',
        '    go to score package wrapper (ww)',
        '    go to segments directory (gg)',
        '    go to stylesheets directory (yy)',
        '    go to test directory (tt)',
        '    go to tools directory (oo)',
        '',
        '    go to next package (>)',
        '    go to previous package (<)',
        '',
        '>',
        ]

    input_ = 'red~example~score mm ; q'
    abjad_ide._start(input_=input_)
    transcript_entry = abjad_ide._io_manager._transcript.entries[-3]

    for line, actual_line in zip(lines, transcript_entry.lines):
        assert line == actual_line


def test_AbjadIDE_display_navigation_command_help_06():
    r'''In segments directory.
    '''

    lines = [
        'Red Example Score (2013) - segments directory - navigation commands',
        '',
        '    display navigation command help (;)',
        '',
        '    back (-)',
        '    home (h)',
        '    quit (q)',
        '',
        '    go to build directory (bb)',
        '    go to distribution directory (dd)',
        '    go to etc directory (ee)',
        '    go to materials directory (mm)',
        '    go to score directory (ss)',
        '    go to score package wrapper (ww)',
        '    go to segments directory (gg)',
        '    go to stylesheets directory (yy)',
        '    go to test directory (tt)',
        '    go to tools directory (oo)',
        '',
        '    go to next package (>)',
        '    go to previous package (<)',
        '',
        '>',
        ]

    input_ = 'red~example~score gg ; q'
    abjad_ide._start(input_=input_)
    transcript_entry = abjad_ide._io_manager._transcript.entries[-3]

    for line, actual_line in zip(lines, transcript_entry.lines):
        assert line == actual_line


def test_AbjadIDE_display_navigation_command_help_07():
    r'''In stylesheets directory.
    '''

    lines = [
        'Red Example Score (2013) - stylesheets directory - navigation commands',
        '',
        '    display navigation command help (;)',
        '',
        '    back (-)',
        '    home (h)',
        '    quit (q)',
        '',
        '    go to build directory (bb)',
        '    go to distribution directory (dd)',
        '    go to etc directory (ee)',
        '    go to materials directory (mm)',
        '    go to score directory (ss)',
        '    go to score package wrapper (ww)',
        '    go to segments directory (gg)',
        '    go to stylesheets directory (yy)',
        '    go to test directory (tt)',
        '    go to tools directory (oo)',
        '',
        '>',
        ]

    input_ = 'red~example~score yy ; q'
    abjad_ide._start(input_=input_)
    transcript_entry = abjad_ide._io_manager._transcript.entries[-3]

    for line, actual_line in zip(lines, transcript_entry.lines):
        assert line == actual_line