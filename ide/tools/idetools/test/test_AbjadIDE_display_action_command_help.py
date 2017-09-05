import abjad
import ide
abjad_ide = ide.AbjadIDE(is_test=True)


def test_AbjadIDE_display_action_command_help_01():
    r'''In scores directory.
    '''

    abjad_ide('? q')
    block = abjad_ide._io_manager._transcript.blocks[-4]
    block_ = [
        'Abjad IDE : scores : action commands',
        '',
        '    every file - edit (ff*)',
        '    every pdf - open (pdf*)',
        '    every string - edit (ee*)',
        '',
        '    display action command help (?)',
        '    invoke shell (!)',
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
        '    every package - git commit (ci*)',
        '    every package - git pull (pull*)',
        '    every package - git push (push*)',
        '    every package - git status (st*)',
        '',
        '>',
        ]
    for line, line_ in zip(block, block_):
        assert line == line_


def test_AbjadIDE_display_action_command_help_02():
    r'''In wrapper directory.
    '''

    abjad_ide('red ww ? q')
    block = abjad_ide._io_manager._transcript.blocks[-6]
    block_ = [
        'Red Score (2017) : wrapper : action commands',
        '',
        '    every file - edit (ff*)',
        '    every pdf - open (pdf*)',
        '    every string - edit (ee*)',
        '',
        '    display action command help (?)',
        '    invoke shell (!)',
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
        '    score pdf - open (spdfo)',
        '',
        '    copy (cp)',
        '    new (new)',
        '    remove (rm)',
        '    rename (ren)',
        '',
        '    git - commit (ci)',
        '    git - diff (diff)',
        '    git - pull (pull)',
        '    git - push (push)',
        '    git - status (st)',
        '',
        '>',
        ]
    for line, line_ in zip(block, block_):
        assert line == line_


def test_AbjadIDE_display_action_command_help_03():
    r'''In contents directory.
    '''

    abjad_ide('red~score ? q')
    block = abjad_ide._io_manager._transcript.blocks[-5]
    block_ = [
        'Red Score (2017) : action commands',
        '',
        '    every file - edit (ff*)',
        '    every pdf - open (pdf*)',
        '    every string - edit (ee*)',
        '',
        '    display action command help (?)',
        '    invoke shell (!)',
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
        '    score pdf - open (spdfo)',
        '',
        '    git - commit (ci)',
        '    git - diff (diff)',
        '    git - pull (pull)',
        '    git - push (push)',
        '    git - status (st)',
        '',
        '>',
        ]
    for line, line_ in zip(block, block_):
        assert line == line_


def test_AbjadIDE_display_action_command_help_04():
    r'''In builds directory.
    '''

    abjad_ide('red~score bb ? q')
    block = abjad_ide._io_manager._transcript.blocks[-6]
    block_ = [
        'Red Score (2017) : builds : action commands',
        '',
        '    every file - edit (ff*)',
        '    every pdf - open (pdf*)',
        '    every string - edit (ee*)',
        '',
        '    display action command help (?)',
        '    invoke shell (!)',
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
        '    score pdf - open (spdfo)',
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
        '    git - pull (pull)',
        '    git - push (push)',
        '    git - status (st)',
        '',
        '>',
        ]
    for line, line_ in zip(block, block_):
        assert line == line_


def test_AbjadIDE_display_action_command_help_05():
    r'''In build directory.
    '''

    abjad_ide('red~score bb letter ? q')
    block = abjad_ide._io_manager._transcript.blocks[-7]
    block_ = [
        'Red Score (2017) : builds : letter : action commands',
        '',
        '    every file - edit (ff*)',
        '    every pdf - open (pdf*)',
        '    every string - edit (ee*)',
        '',
        '    display action command help (?)',
        '    invoke shell (!)',
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
        '    score pdf - open (spdfo)',
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
        '    back cover - open (bco)',
        '    front cover - open (fco)',
        '    music - open (mo)',
        '    preface - open (po)',
        '    score - open (so)',
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
        '    git - pull (pull)',
        '    git - push (push)',
        '    git - status (st)',
        '',
        '>',
        ]
    for line, line_ in zip(block, block_):
        assert line == line_


def test_AbjadIDE_display_action_command_help_06():
    r'''In distribution directory.
    '''

    abjad_ide('red~score dd ? q')
    block = abjad_ide._io_manager._transcript.blocks[-6]
    block_ = [
        'Red Score (2017) : distribution : action commands',
        '',
        '    every file - edit (ff*)',
        '    every pdf - open (pdf*)',
        '    every string - edit (ee*)',
        '',
        '    display action command help (?)',
        '    invoke shell (!)',
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
        '    score pdf - open (spdfo)',
        '',
        '    copy (cp)',
        '    new (new)',
        '    remove (rm)',
        '    rename (ren)',
        '',
        '    git - commit (ci)',
        '    git - diff (diff)',
        '    git - pull (pull)',
        '    git - push (push)',
        '    git - status (st)',
        '',
        '>',
        ]
    for line, line_ in zip(block, block_):
        assert line == line_


def test_AbjadIDE_display_action_command_help_07():
    r'''In tools directory.
    '''

    abjad_ide('red~score oo ? q')
    block = abjad_ide._io_manager._transcript.blocks[-6]
    block_ = [
        'Red Score (2017) : tools : action commands',
        '',
        '    every file - edit (ff*)',
        '    every pdf - open (pdf*)',
        '    every string - edit (ee*)',
        '',
        '    display action command help (?)',
        '    invoke shell (!)',
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
        '    score pdf - open (spdfo)',
        '',
        '    keep (kp)',
        '',
        '    copy (cp)',
        '    new (new)',
        '    remove (rm)',
        '    rename (ren)',
        '',
        '    git - commit (ci)',
        '    git - diff (diff)',
        '    git - pull (pull)',
        '    git - push (push)',
        '    git - status (st)',
        '',
        '>',
        ]
    for line, line_ in zip(block, block_):
        assert line == line_


def test_AbjadIDE_display_action_command_help_08():
    r'''In materials directory.
    '''

    abjad_ide('red~score mm ? q')
    block = abjad_ide._io_manager._transcript.blocks[-6]
    block_ = [
        'Red Score (2017) : materials : action commands',
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
        '    score pdf - open (spdfo)',
        '',
        '    copy (cp)',
        '    new (new)',
        '    remove (rm)',
        '    rename (ren)',
        '',
        '    git - commit (ci)',
        '    git - diff (diff)',
        '    git - pull (pull)',
        '    git - push (push)',
        '    git - status (st)',
        '',
        '>',
        ]
    for line, line_ in zip(block, block_):
        assert line == line_


def test_AbjadIDE_display_action_command_help_09():
    r'''In material directory.
    '''

    abjad_ide('red~score mm magic ? q')
    block = abjad_ide._io_manager._transcript.blocks[-7]
    block_ = [
        'Red Score (2017) : materials : magic_numbers : action commands',
        '',
        '    every file - edit (ff*)',
        '    every pdf - open (pdf*)',
        '    every string - edit (ee*)',
        '',
        '    display action command help (?)',
        '    invoke shell (!)',
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
        '    pdf - open (pdfo)',
        '    pdf - trash (pdft)',
        '    score pdf - open (spdfo)',
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
        '    git - pull (pull)',
        '    git - push (push)',
        '    git - status (st)',
        '',
        '>',
        ]
    for line, line_ in zip(block, block_):
        assert line == line_


def test_AbjadIDE_display_action_command_help_10():
    r'''In segments directory.
    '''

    abjad_ide('red~score gg ? q')
    block = abjad_ide._io_manager._transcript.blocks[-6]
    block_ = [
        'Red Score (2017) : segments : action commands',
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
        '    score pdf - open (spdfo)',
        '',
        '    copy (cp)',
        '    new (new)',
        '    remove (rm)',
        '    rename (ren)',
        '',
        '    git - commit (ci)',
        '    git - diff (diff)',
        '    git - pull (pull)',
        '    git - push (push)',
        '    git - status (st)',
        '',
        '>',
        ]
    for line, line_ in zip(block, block_):
        assert line == line_


def test_AbjadIDE_display_action_command_help_11():
    r'''In segment directory.
    '''

    abjad_ide('red~score gg A ? q')
    block = abjad_ide._io_manager._transcript.blocks[-7]
    block_ = [
        'Red Score (2017) : segments : A : action commands',
        '',
        '    every file - edit (ff*)',
        '    every pdf - open (pdf*)',
        '    every string - edit (ee*)',
        '',
        '    display action command help (?)',
        '    invoke shell (!)',
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
        '    pdf - open (pdfo)',
        '    pdf - trash (pdft)',
        '    score pdf - open (spdfo)',
        '',
        '    ly & pdf - trash (trash)',
        '',
        '    midi - make (midim)',
        '',
        '    copy (cp)',
        '    new (new)',
        '    remove (rm)',
        '    rename (ren)',
        '',
        '    git - commit (ci)',
        '    git - diff (diff)',
        '    git - pull (pull)',
        '    git - push (push)',
        '    git - status (st)',
        '',
        '>',
        ]
    for line, line_ in zip(block, block_):
        assert line == line_


def test_AbjadIDE_display_action_command_help_12():
    r'''In stylesheets directory.
    '''

    abjad_ide('red~score yy ? q')
    block = abjad_ide._io_manager._transcript.blocks[-6]
    block_ = [
        'Red Score (2017) : stylesheets : action commands',
        '',
        '    every file - edit (ff*)',
        '    every pdf - open (pdf*)',
        '    every string - edit (ee*)',
        '',
        '    display action command help (?)',
        '    invoke shell (!)',
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
        '    score pdf - open (spdfo)',
        '',
        '    copy (cp)',
        '    new (new)',
        '    remove (rm)',
        '    rename (ren)',
        '',
        '    git - commit (ci)',
        '    git - diff (diff)',
        '    git - pull (pull)',
        '    git - push (push)',
        '    git - status (st)',
        '',
        '>',
        ]
    for line, line_ in zip(block, block_):
        assert line == line_


def test_AbjadIDE_display_action_command_help_13():
    r'''In test directory.
    '''

    abjad_ide('red~score tt ? q')
    block = abjad_ide._io_manager._transcript.blocks[-6]
    block_ = [
        'Red Score (2017) : test : action commands',
        '',
        '    every file - edit (ff*)',
        '    every pdf - open (pdf*)',
        '    every string - edit (ee*)',
        '',
        '    display action command help (?)',
        '    invoke shell (!)',
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
        '    score pdf - open (spdfo)',
        '',
        '    copy (cp)',
        '    new (new)',
        '    remove (rm)',
        '    rename (ren)',
        '',
        '    git - commit (ci)',
        '    git - diff (diff)',
        '    git - pull (pull)',
        '    git - push (push)',
        '    git - status (st)',
        '',
        '>',
        ]
    for line, line_ in zip(block, block_):
        assert line == line_


def test_AbjadIDE_display_action_command_help_14():
    r'''In external directory.
    '''

    scores = abjad.abjad_configuration.composer_scores_directory
    if 'trevorbaca' not in scores:
        return

    abjad_ide('cdk ? q')
    block = abjad_ide._io_manager._transcript.blocks[-5]
    block_ = [
        'Abjad IDE : /Users/trevorbaca/Desktop : action commands',
        '',
        '    every file - edit (ff*)',
        '    every pdf - open (pdf*)',
        '    every string - edit (ee*)',
        '',
        '    display action command help (?)',
        '    invoke shell (!)',
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
        '    new (new)',
        '    remove (rm)',
        '    rename (ren)',
        '',
        '    git - commit (ci)',
        '    git - diff (diff)',
        '    git - pull (pull)',
        '    git - push (push)',
        '    git - status (st)',
        '',
        '>',
        ]
    for line, line_ in zip(block, block_):
        assert line == line_
