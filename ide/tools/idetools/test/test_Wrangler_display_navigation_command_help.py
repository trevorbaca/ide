# -*- encoding: utf-8 -*-
from abjad import *
import ide
abjad_ide = ide.tools.idetools.AbjadIDE(is_test=True)


def test_Wrangler_display_navigation_command_help_01():
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
        '    go to all build directories (uu)',
        '    go to all distribution directories (dd)',
        '    go to all etc directories (ee)',
        '    go to all makers directories (kk)',
        '    go to all materials directories (mm)',
        '    go to all segments directories (gg)',
        '    go to all stylesheets directories (yy)',
        '    go to all test directories (tt)',
        '',
        '    go to next score (>>)',
        '    go to previous score (<<)',
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


def test_Wrangler_display_navigation_command_help_02():
    r'''Works at all materials directories.
    '''

    lines = [
        'Abjad IDE - all materials directories - view & navigation commands',
        '',
        '    display navigation command help (;)',
        '',
        '    home (h)',
        '    quit (q)',
        '',
        '    go to all build directories (uu)',
        '    go to all distribution directories (dd)',
        '    go to all etc directories (ee)',
        '    go to all makers directories (kk)',
        '    go to all materials directories (mm)',
        '    go to all segments directories (gg)',
        '    go to all stylesheets directories (yy)',
        '    go to all test directories (tt)',
        '',
        '>',
        ]

    input_ = 'mm ; q'
    abjad_ide._run_main_menu(input_=input_)
    transcript_entry = abjad_ide._io_manager._transcript.entries[-3]

    for line, actual_line in zip(lines, transcript_entry.lines):
        assert line == actual_line


def test_Wrangler_display_navigation_command_help_03():
    r'''Works at all stylesheets directories.
    '''

    lines = [
        'Abjad IDE - all stylesheets directories - view & navigation commands',
        '',
        '    display navigation command help (;)',
        '',
        '    home (h)',
        '    quit (q)',
        '',
        '    go to all build directories (uu)',
        '    go to all distribution directories (dd)',
        '    go to all etc directories (ee)',
        '    go to all makers directories (kk)',
        '    go to all materials directories (mm)',
        '    go to all segments directories (gg)',
        '    go to all stylesheets directories (yy)',
        '    go to all test directories (tt)',
        '',
        '>',
        ]

    input_ = 'yy ; q'
    abjad_ide._run_main_menu(input_=input_)
    transcript_entry = abjad_ide._io_manager._transcript.entries[-3]

    for line, actual_line in zip(lines, transcript_entry.lines):
        assert line == actual_line


def test_Wrangler_display_navigation_command_help_04():
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
        '    go to score build directory (u)',
        '    go to score directory (s)',
        '    go to score distribution directory (d)',
        '    go to score etc directory (e)',
        '    go to score makers directory (k)',
        '    go to score materials directory (m)',
        '    go to score segments directory (g)',
        '    go to score stylesheets directory (y)',
        '    go to score test directory (t)',
        '',
        '    go to next package (>)',
        '    go to previous package (<)',
        '',
        '    go to next score (>>)',
        '    go to previous score (<<)',
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


def test_Wrangler_display_navigation_command_help_05():
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
        '    go to score build directory (u)',
        '    go to score directory (s)',
        '    go to score distribution directory (d)',
        '    go to score etc directory (e)',
        '    go to score makers directory (k)',
        '    go to score materials directory (m)',
        '    go to score segments directory (g)',
        '    go to score stylesheets directory (y)',
        '    go to score test directory (t)',
        '',
        '    go to next package (>)',
        '    go to previous package (<)',
        '',
        '    go to next score (>>)',
        '    go to previous score (<<)',
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


def test_Wrangler_display_navigation_command_help_06():
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
        '    go to score build directory (u)',
        '    go to score directory (s)',
        '    go to score distribution directory (d)',
        '    go to score etc directory (e)',
        '    go to score makers directory (k)',
        '    go to score materials directory (m)',
        '    go to score segments directory (g)',
        '    go to score stylesheets directory (y)',
        '    go to score test directory (t)',
        '',
        '    go to next score (>>)',
        '    go to previous score (<<)',
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