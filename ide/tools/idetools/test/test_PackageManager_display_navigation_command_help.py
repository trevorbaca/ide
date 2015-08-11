# -*- encoding: utf-8 -*-
from abjad import *
import ide
abjad_ide = ide.tools.idetools.AbjadIDE(is_test=True)


def test_PackageManager_display_navigation_command_help_01():
    r'''Works in score directory.
    '''

    lines = [
        'Red Example Score (2013) - view & navigation commands',
        '',
        '    display navigation command help (;)',
        '',
        '    back (b)',
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
        '>',
        ]

    input_ = 'red~example~score ; q'
    abjad_ide._run(input_=input_)
    transcript_entry = abjad_ide._io_manager._transcript.entries[-3]


    for line, actual_line in zip(lines, transcript_entry.lines):
        assert line == actual_line


def test_PackageManager_display_navigation_command_help_02():
    r'''Works in material package.
    '''

    lines = [
        'Red Example Score (2013) - materials directory - magic numbers - view & navigation commands',
        '',
        '    display navigation command help (;)',
        '',
        '    back (b)',
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
        '>',
    ]

    input_ = 'red~example~score m magic~numbers ; q'
    abjad_ide._run(input_=input_)
    transcript_entry = abjad_ide._io_manager._transcript.entries[-3]


    for line, actual_line in zip(lines, transcript_entry.lines):
        assert line == actual_line


def test_PackageManager_display_navigation_command_help_03():
    r'''Works in segment package.
    '''

    lines = [
        'Red Example Score (2013) - segments directory - A - view & navigation commands',
        '',
        '    display navigation command help (;)',
        '',
        '    back (b)',
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
        '>',
    ]

    input_ = 'red~example~score g A ; q'
    abjad_ide._run(input_=input_)
    transcript_entry = abjad_ide._io_manager._transcript.entries[-3]


    for line, actual_line in zip(lines, transcript_entry.lines):
        assert line == actual_line