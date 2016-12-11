# -*- coding: utf-8 -*-
import abjad
import ide
abjad_ide = ide.tools.idetools.AbjadIDE(is_test=True)


def test_AbjadIDE_display_action_command_help_01():
    r'''In scores directory.
    '''

    lines = [
        'Abjad IDE - all score directories - action commands',
        '',
        '    edit every file (ff*)',
        '    open every score pdf (so*)',
        '',
        '    display action command help (?)',
        '    invoke shell (!)',
        '    refresh (rf)',
        '    replace (rp)',
        '    search (sr)',
        '',
        '    aliases - edit (als)',
        '    latex log - edit (lxg)',
        '    lilypond log - edit (lpg)',
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


def test_AbjadIDE_display_action_command_help_02():
    r'''In outer score directory.
    '''

    lines = [
        'Red Example Score (2013) - package wrapper - action commands',
        '',
        '    edit every file (ff*)',
        '',
        '    display action command help (?)',
        '    invoke shell (!)',
        '    refresh (rf)',
        '    replace (rp)',
        '    search (sr)',
        '',
        '    aliases - edit (als)',
        '    latex log - edit (lxg)',
        '    lilypond log - edit (lpg)',
        '',
        '    doctest - run (dt)',
        '    pytest - run (pt)',
        '',
        '    copy (cp)',
        '    new (new)',
        '    remove (rm)',
        '    rename (ren)',
        '',
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


def test_AbjadIDE_display_action_command_help_03():
    r'''In inner score directory.
    '''
    
    lines = [
        'Red Example Score (2013) - action commands',
        '',
        '    edit every file (ff*)',
        '',
        '    display action command help (?)',
        '    invoke shell (!)',
        '    refresh (rf)',
        '    replace (rp)',
        '    search (sr)',
        '',
        '    aliases - edit (als)',
        '    latex log - edit (lxg)',
        '    lilypond log - edit (lpg)',
        '',
        '    doctest - run (dt)',
        '    pytest - run (pt)',
        '',
        '    score pdf - open (so)',
        '',
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


def test_AbjadIDE_display_action_command_help_04():
    r'''In build directory.
    '''
    
    lines = [
        'Red Example Score (2013) - build directory - action commands',
        '',
        '    edit every file (ff*)',
        '',
        '    display action command help (?)',
        '    invoke shell (!)',
        '    refresh (rf)',
        '    replace (rp)',
        '    search (sr)',
        '',
        '    aliases - edit (als)',
        '    latex log - edit (lxg)',
        '    lilypond log - edit (lpg)',
        '',
        '    doctest - run (dt)',
        '    pytest - run (pt)',
        '',
        '    segment lys - collect (lyc)',
        '',
        '    copy (cp)',
        '    new (new)',
        '    remove (rm)',
        '    rename (ren)',
        '',
        '    git - commit (ci)',
        '    git - status (st)',
        '    git - update (up)',
        '',
        '>',
        ]

    input_ = 'red~example~score bb ? q'
    abjad_ide._start(input_=input_)
    transcript_entry = abjad_ide._io_manager._transcript.entries[-3]

    for line, actual_line in zip(lines, transcript_entry.lines):
        assert line == actual_line


def test_AbjadIDE_display_action_command_help_05():
    r'''In build subdirectory.
    '''
    
    lines = [
        'Red Example Score (2013) - build directory - letter-portrait - action commands',
        '',
        '    edit every file (ff*)',
        '',
        '    display action command help (?)',
        '    invoke shell (!)',
        '    refresh (rf)',
        '    replace (rp)',
        '    search (sr)',
        '',
        '    aliases - edit (als)',
        '    latex log - edit (lxg)',
        '    lilypond log - edit (lpg)',
        '',
        '    doctest - run (dt)',
        '    pytest - run (pt)',
        '',
        '    segment lys - collect (lyc)',
        '',
        '    back cover - generate (bcg)',
        '    front cover - generate (fcg)',
        '    music - generate (mg)',
        '    preface - generate (pg)',
        '    score - generate (sg)',
        '    stylesheet - generate (stg)',
        '',
        '    back cover - edit (bce)',
        '    front cover - edit (fce)',
        '    music - edit (me)',
        '    preface - edit (pe)',
        '    score - edit (se)',
        '    stylesheet - edit (ste)',
        '',
        '    back cover - interpret (bci)',
        '    front cover - interpret (fci)',
        '    music - interpret (mi)',
        '    preface - interpret (pi)',
        '    score - interpret (si)',
        '',
        '    back cover - open (bc)',
        '    front cover - open (fc)',
        '    music - open (m)',
        '    preface - open (p)',
        '    score - open (s)',
        '',
        '    score pdf - build (bld)',
        '    score pdf - publish (spp)',
        '',
        '    copy (cp)',
        '    new (new)',
        '    remove (rm)',
        '    rename (ren)',
        '',
        '    git - commit (ci)',
        '    git - status (st)',
        '    git - update (up)',
        '',
        '>',
        ]

    input_ = 'red~example~score bb letter-portrait ? q'
    abjad_ide._start(input_=input_)
    transcript_entry = abjad_ide._io_manager._transcript.entries[-3]

    for line, actual_line in zip(lines, transcript_entry.lines):
        assert line == actual_line
        

def test_AbjadIDE_display_action_command_help_06():
    r'''In distribution directory.
    '''
    
    lines = [
        'Red Example Score (2013) - distribution directory - action commands',
        '',
        '    edit every file (ff*)',
        '',
        '    display action command help (?)',
        '    invoke shell (!)',
        '    refresh (rf)',
        '    replace (rp)',
        '    search (sr)',
        '',
        '    aliases - edit (als)',
        '    latex log - edit (lxg)',
        '    lilypond log - edit (lpg)',
        '',
        '    doctest - run (dt)',
        '    pytest - run (pt)',
        '',
        '    copy (cp)',
        '    new (new)',
        '    remove (rm)',
        '    rename (ren)',
        '',
        '    git - commit (ci)',
        '    git - status (st)',
        '    git - update (up)',
        '',
        '>',
        ]

    input_ = 'red~example~score dd ? q'
    abjad_ide._start(input_=input_)
    transcript_entry = abjad_ide._io_manager._transcript.entries[-3]

    for line, actual_line in zip(lines, transcript_entry.lines):
        assert line == actual_line


def test_AbjadIDE_display_action_command_help_07():
    r'''In tools directory.
    '''
    
    lines = [
        'Red Example Score (2013) - tools directory - action commands',
        '',
        '    edit every file (ff*)',
        '',
        '    display action command help (?)',
        '    invoke shell (!)',
        '    refresh (rf)',
        '    replace (rp)',
        '    search (sr)',
        '',
        '    aliases - edit (als)',
        '    latex log - edit (lxg)',
        '    lilypond log - edit (lpg)',
        '',
        '    doctest - run (dt)',
        '    pytest - run (pt)',
        '',
        '    copy (cp)',
        '    new (new)',
        '    remove (rm)',
        '    rename (ren)',
        '',
        '    git - commit (ci)',
        '    git - status (st)',
        '    git - update (up)',
        '',
        '>',
        ]

    input_ = 'red~example~score oo ? q'
    abjad_ide._start(input_=input_)
    transcript_entry = abjad_ide._io_manager._transcript.entries[-3]

    for line, actual_line in zip(lines, transcript_entry.lines):
        assert line == actual_line


def test_AbjadIDE_display_action_command_help_08():
    r'''In materials directory.
    '''

    lines = [
        'Red Example Score (2013) - materials directory - action commands',
        '',
        '    edit every file (ff*)',
        '    every definition file - check (dfk*)',
        '    every definition file - edit (df*)',
        '    every ly - interpret (lyi*)',
        '    every pdf - make (pdfm*)',
        '    every pdf - open (pdf*)',
        '',
        '    display action command help (?)',
        '    invoke shell (!)',
        '    refresh (rf)',
        '    replace (rp)',
        '    search (sr)',
        '',
        '    aliases - edit (als)',
        '    latex log - edit (lxg)',
        '    lilypond log - edit (lpg)',
        '',
        '    doctest - run (dt)',
        '    pytest - run (pt)',
        '',
        '    copy (cp)',
        '    new (new)',
        '    remove (rm)',
        '    rename (ren)',
        '',
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


def test_AbjadIDE_display_action_command_help_09():
    r'''In material directory.
    '''

    lines = [
        'Red Example Score (2013) - materials directory - magic numbers - action commands',
        '',
        '    edit every file (ff*)',
        '',
        '    display action command help (?)',
        '    invoke shell (!)',
        '    refresh (rf)',
        '    replace (rp)',
        '    search (sr)',
        '',
        '    aliases - edit (als)',
        '    latex log - edit (lxg)',
        '    lilypond log - edit (lpg)',
        '',
        '    doctest - run (dt)',
        '    pytest - run (pt)',
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
        '    ly & pdf - trash (trash)',
        '',
        '    copy (cp)',
        '    new (new)',
        '    remove (rm)',
        '    rename (ren)',
        '',
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


def test_AbjadIDE_display_action_command_help_10():
    r'''In segments directory.
    '''

    lines = [
        'Red Example Score (2013) - segments directory - action commands',
        '',
        '    edit every file (ff*)',
        '    every definition file - check (dfk*)',
        '    every definition file - edit (df*)',
        '    every ly - interpret (lyi*)',
        '    every pdf - make (pdfm*)',
        '    every pdf - open (pdf*)',
        '',
        '    display action command help (?)',
        '    invoke shell (!)',
        '    refresh (rf)',
        '    replace (rp)',
        '    search (sr)',
        '',
        '    aliases - edit (als)',
        '    latex log - edit (lxg)',
        '    lilypond log - edit (lpg)',
        '',
        '    doctest - run (dt)',
        '    pytest - run (pt)',
        '',
        '    copy (cp)',
        '    new (new)',
        '    remove (rm)',
        '    rename (ren)',
        '',
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


def test_AbjadIDE_display_action_command_help_11():
    r'''In segment directory.
    '''

    lines = [
        'Red Example Score (2013) - segments directory - A - action commands',
        '',
        '    edit every file (ff*)',
        '',
        '    display action command help (?)',
        '    invoke shell (!)',
        '    refresh (rf)',
        '    replace (rp)',
        '    search (sr)',
        '',
        '    aliases - edit (als)',
        '    latex log - edit (lxg)',
        '    lilypond log - edit (lpg)',
        '',
        '    doctest - run (dt)',
        '    pytest - run (pt)',
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
        '    ly & pdf - trash (trash)',
        '',
        '    copy (cp)',
        '    new (new)',
        '    remove (rm)',
        '    rename (ren)',
        '',
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


def test_AbjadIDE_display_action_command_help_12():
    r'''In stylesheets directory.
    '''

    lines = [
        'Red Example Score (2013) - stylesheets directory - action commands',
        '',
        '    edit every file (ff*)',
        '',
        '    display action command help (?)',
        '    invoke shell (!)',
        '    refresh (rf)',
        '    replace (rp)',
        '    search (sr)',
        '',
        '    aliases - edit (als)',
        '    latex log - edit (lxg)',
        '    lilypond log - edit (lpg)',
        '',
        '    doctest - run (dt)',
        '    pytest - run (pt)',
        '',
        '    copy (cp)',
        '    new (new)',
        '    remove (rm)',
        '    rename (ren)',
        '',
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


def test_AbjadIDE_display_action_command_help_13():
    r'''In test directory.
    '''

    lines = [
        'Red Example Score (2013) - test directory - action commands',
        '',
        '    edit every file (ff*)',
        '',
        '    display action command help (?)',
        '    invoke shell (!)',
        '    refresh (rf)',
        '    replace (rp)',
        '    search (sr)',
        '',
        '    aliases - edit (als)',
        '    latex log - edit (lxg)',
        '    lilypond log - edit (lpg)',
        '',
        '    doctest - run (dt)',
        '    pytest - run (pt)',
        '',
        '    copy (cp)',
        '    new (new)',
        '    remove (rm)',
        '    rename (ren)',
        '',
        '    git - commit (ci)',
        '    git - status (st)',
        '    git - update (up)',
        '',
        '>',
        ]

    input_ = 'red~example~score tt ? q'
    abjad_ide._start(input_=input_)
    transcript_entry = abjad_ide._io_manager._transcript.entries[-3]

    for line, actual_line in zip(lines, transcript_entry.lines):
        assert line == actual_line
