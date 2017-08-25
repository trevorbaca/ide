import ide
abjad_ide = ide.AbjadIDE(is_test=True)


def test_AbjadIDE_display_action_command_help_01():
    r'''In scores directory.
    '''

    lines = [
        'Abjad IDE - scores directory - action commands',
        '',
        '    every file - edit (ff*)',
        '    every pdf - open (pdf*)',
        '    every string - edit (ee*)',
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
    r'''In wrapper directory.
    '''

    lines = [
        'Red Score (2017) - package wrapper - action commands',
        '',
        '    every file - edit (ff*)',
        '    every string - edit (ee*)',
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
        '    tests - run (tests)',
        '',
        '    copy (cp)',
        '    new (new)',
        '    remove (rm)',
        '    rename (ren)',
        '',
        '    git - commit (ci)',
        '    git - diff (diff)',
        '    git - status (st)',
        '    git - update (up)',
        '',
        '>',
        ]

    input_ = 'red~score ww ? q'
    abjad_ide._start(input_=input_)
    transcript_entry = abjad_ide._io_manager._transcript.entries[-3]
    for line, actual_line in zip(lines, transcript_entry.lines):
        assert line == actual_line


def test_AbjadIDE_display_action_command_help_03():
    r'''In contents directory.
    '''

    lines = [
        'Red Score (2017) - action commands',
        '',
        '    every file - edit (ff*)',
        '    every string - edit (ee*)',
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
        '    tests - run (tests)',
        '',
        '    score pdf - open (so)',
        '',
        '    git - commit (ci)',
        '    git - diff (diff)',
        '    git - status (st)',
        '    git - update (up)',
        '',
        '>',
        ]

    input_ = 'red~score ? q'
    abjad_ide._start(input_=input_)
    transcript_entry = abjad_ide._io_manager._transcript.entries[-3]
    for line, actual_line in zip(lines, transcript_entry.lines):
        assert line == actual_line


def test_AbjadIDE_display_action_command_help_04():
    r'''In build directory.
    '''

    lines = [
        'Red Score (2017) - build directory - action commands',
        '',
        '    every file - edit (ff*)',
        '    every string - edit (ee*)',
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
        '    tests - run (tests)',
        '',
        '    segment lys - collect (lyc)',
        '',
        '    copy (cp)',
        '    new (new)',
        '    remove (rm)',
        '    rename (ren)',
        '',
        '    git - commit (ci)',
        '    git - diff (diff)',
        '    git - status (st)',
        '    git - update (up)',
        '',
        '>',
        ]

    input_ = 'red~score bb ? q'
    abjad_ide._start(input_=input_)
    transcript_entry = abjad_ide._io_manager._transcript.entries[-3]
    for line, actual_line in zip(lines, transcript_entry.lines):
        assert line == actual_line


def test_AbjadIDE_display_action_command_help_05():
    r'''In build subdirectory.
    '''

    lines = [
        'Red Score (2017) - build directory - letter - action commands',
        '',
        '    every file - edit (ff*)',
        '    every string - edit (ee*)',
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
        '    tests - run (tests)',
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
        '    git - diff (diff)',
        '    git - status (st)',
        '    git - update (up)',
        '',
        '>',
        ]

    input_ = 'red~score bb letter ? q'
    abjad_ide._start(input_=input_)
    transcript_entry = abjad_ide._io_manager._transcript.entries[-3]
    for line, actual_line in zip(lines, transcript_entry.lines):
        assert line == actual_line


def test_AbjadIDE_display_action_command_help_06():
    r'''In distribution directory.
    '''

    lines = [
        'Red Score (2017) - distribution directory - action commands',
        '',
        '    every file - edit (ff*)',
        '    every string - edit (ee*)',
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
        '    tests - run (tests)',
        '',
        '    copy (cp)',
        '    new (new)',
        '    remove (rm)',
        '    rename (ren)',
        '',
        '    git - commit (ci)',
        '    git - diff (diff)',
        '    git - status (st)',
        '    git - update (up)',
        '',
        '>',
        ]

    input_ = 'red~score dd ? q'
    abjad_ide._start(input_=input_)
    transcript_entry = abjad_ide._io_manager._transcript.entries[-3]
    for line, actual_line in zip(lines, transcript_entry.lines):
        assert line == actual_line


def test_AbjadIDE_display_action_command_help_07():
    r'''In tools directory.
    '''

    lines = [
        'Red Score (2017) - tools directory - action commands',
        '',
        '    every file - edit (ff*)',
        '    every string - edit (ee*)',
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
        '    tests - run (tests)',
        '',
        '    copy (cp)',
        '    new (new)',
        '    remove (rm)',
        '    rename (ren)',
        '',
        '    git - commit (ci)',
        '    git - diff (diff)',
        '    git - status (st)',
        '    git - update (up)',
        '',
        '>',
        ]

    input_ = 'red~score oo ? q'
    abjad_ide._start(input_=input_)
    transcript_entry = abjad_ide._io_manager._transcript.entries[-3]
    for line, actual_line in zip(lines, transcript_entry.lines):
        assert line == actual_line


def test_AbjadIDE_display_action_command_help_08():
    r'''In materials directory.
    '''

    lines = [
        'Red Score (2017) - materials directory - action commands',
        '',
        '    every definition file - check (dfk*)',
        '    every definition file - edit (df*)',
        '    every file - edit (ff*)',
        '    every ly - interpret (lyi*)',
        '    every pdf - make (pdfm*)',
        '    every pdf - open (pdf*)',
        '    every string - edit (ee*)',
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
        '    tests - run (tests)',
        '',
        '    copy (cp)',
        '    new (new)',
        '    remove (rm)',
        '    rename (ren)',
        '',
        '    git - commit (ci)',
        '    git - diff (diff)',
        '    git - status (st)',
        '    git - update (up)',
        '',
        '>',
        ]

    input_ = 'red~score mm ? q'
    abjad_ide._start(input_=input_)
    transcript_entry = abjad_ide._io_manager._transcript.entries[-3]
    for line, actual_line in zip(lines, transcript_entry.lines):
        assert line == actual_line


def test_AbjadIDE_display_action_command_help_09():
    r'''In material directory.
    '''

    lines = [
        'Red Score (2017) - materials directory - magic numbers - action commands',
        '',
        '    every file - edit (ff*)',
        '    every string - edit (ee*)',
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
        '    tests - run (tests)',
        '',
        '    definition file - check (dfk)',
        '    definition file - edit (df)',
        '',
        '    illustrate file - edit (ill)',
        '    illustrate file - make (illm)',
        '    illustrate file - trash (illt)',
        '',
        '    ly - edit (ly)',
        '    ly - interpret (lyi)',
        '    ly - make (lym)',
        '    ly - trash (lyt)',
        '',
        '    pdf - make (pdfm)',
        '    pdf - open (pdf)',
        '    pdf - trash (pdft)',
        '',
        '    ly & pdf - trash (trash)',
        '',
        '    copy (cp)',
        '    new (new)',
        '    remove (rm)',
        '    rename (ren)',
        '',
        '    git - commit (ci)',
        '    git - diff (diff)',
        '    git - status (st)',
        '    git - update (up)',
        '',
        '>',
    ]

    input_ = 'red~score mm magic~numbers ? q'
    abjad_ide._start(input_=input_)
    transcript_entry = abjad_ide._io_manager._transcript.entries[-3]
    for line, actual_line in zip(lines, transcript_entry.lines):
        assert line == actual_line


def test_AbjadIDE_display_action_command_help_10():
    r'''In segments directory.
    '''

    lines = [
        'Red Score (2017) - segments directory - action commands',
        '',
        '    every definition file - check (dfk*)',
        '    every definition file - edit (df*)',
        '    every file - edit (ff*)',
        '    every ly - interpret (lyi*)',
        '    every pdf - make (pdfm*)',
        '    every pdf - open (pdf*)',
        '    every string - edit (ee*)',
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
        '    tests - run (tests)',
        '',
        '    copy (cp)',
        '    new (new)',
        '    remove (rm)',
        '    rename (ren)',
        '',
        '    git - commit (ci)',
        '    git - diff (diff)',
        '    git - status (st)',
        '    git - update (up)',
        '',
        '>',
        ]

    input_ = 'red~score gg ? q'
    abjad_ide._start(input_=input_)
    transcript_entry = abjad_ide._io_manager._transcript.entries[-3]
    for line, actual_line in zip(lines, transcript_entry.lines):
        assert line == actual_line


def test_AbjadIDE_display_action_command_help_11():
    r'''In segment directory.
    '''

    lines = [
        'Red Score (2017) - segments directory - A - action commands',
        '',
        '    every file - edit (ff*)',
        '    every string - edit (ee*)',
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
        '    tests - run (tests)',
        '',
        '    definition file - check (dfk)',
        '    definition file - edit (df)',
        '',
        '    ly - edit (ly)',
        '    ly - interpret (lyi)',
        '    ly - make (lym)',
        '    ly - trash (lyt)',
        '',
        '    pdf - make (pdfm)',
        '    pdf - open (pdf)',
        '    pdf - trash (pdft)',
        '',
        '    ly & pdf - trash (trash)',
        '',
        '    copy (cp)',
        '    new (new)',
        '    remove (rm)',
        '    rename (ren)',
        '',
        '    git - commit (ci)',
        '    git - diff (diff)',
        '    git - status (st)',
        '    git - update (up)',
        '',
        '>',
    ]

    input_ = 'red~score gg A ? q'
    abjad_ide._start(input_=input_)
    transcript_entry = abjad_ide._io_manager._transcript.entries[-3]
    for line, actual_line in zip(lines, transcript_entry.lines):
        assert line == actual_line


def test_AbjadIDE_display_action_command_help_12():
    r'''In stylesheets directory.
    '''

    lines = [
        'Red Score (2017) - stylesheets directory - action commands',
        '',
        '    every file - edit (ff*)',
        '    every string - edit (ee*)',
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
        '    tests - run (tests)',
        '',
        '    copy (cp)',
        '    new (new)',
        '    remove (rm)',
        '    rename (ren)',
        '',
        '    git - commit (ci)',
        '    git - diff (diff)',
        '    git - status (st)',
        '    git - update (up)',
        '',
        '>',
        ]

    input_ = 'red~score yy ? q'
    abjad_ide._start(input_=input_)
    transcript_entry = abjad_ide._io_manager._transcript.entries[-3]
    for line, actual_line in zip(lines, transcript_entry.lines):
        assert line == actual_line


def test_AbjadIDE_display_action_command_help_13():
    r'''In test directory.
    '''

    lines = [
        'Red Score (2017) - test directory - action commands',
        '',
        '    every file - edit (ff*)',
        '    every string - edit (ee*)',
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
        '    tests - run (tests)',
        '',
        '    copy (cp)',
        '    new (new)',
        '    remove (rm)',
        '    rename (ren)',
        '',
        '    git - commit (ci)',
        '    git - diff (diff)',
        '    git - status (st)',
        '    git - update (up)',
        '',
        '>',
        ]

    input_ = 'red~score tt ? q'
    abjad_ide._start(input_=input_)
    transcript_entry = abjad_ide._io_manager._transcript.entries[-3]
    for line, actual_line in zip(lines, transcript_entry.lines):
        assert line == actual_line
