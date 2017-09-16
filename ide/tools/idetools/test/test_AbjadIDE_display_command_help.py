import abjad
import ide
abjad_ide = ide.AbjadIDE(is_test=True)


def test_AbjadIDE_display_command_help_01():
    r'''In build directory.
    '''

    abjad_ide('red~score bb letter ? q')
    menu = abjad_ide.io.transcript.menus[-1]
    menu_ = [
        'Red Score (2017) : builds : letter : commands',
        '',
        '    every file - edit (ff*)',
        '    every pdf - open (pdf*)',
        '    every string - edit (ee*)',
        '',
        '    call shell (!)',
        '    display command help (?)',
        '    force single column (!!)',
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
        '    copy to clipboard (cp)',
        '    empty clipboard (ce)',
        '    paste from clipboard (cv)',
        '    show clipboard (cs)',
        '',
        '    score pdf - open (spdfo)',
        '',
        '    segment lys - collect (lyc)',
        '',
        '    back cover - generate (bcg)',
        '    front cover - generate (fcg)',
        '    music - generate (mg)',
        '    preface - generate (rg)',
        '    score - generate (sg)',
        '    stylesheet - generate (stg)',
        '',
        '    back cover - edit (bce)',
        '    front cover - edit (fce)',
        '    music - edit (me)',
        '    preface - edit (re)',
        '    score - edit (se)',
        '    stylesheet - edit (ste)',
        '',
        '    back cover - interpret (bci)',
        '    front cover - interpret (fci)',
        '    music - interpret (mi)',
        '    preface - interpret (ri)',
        '    score - interpret (si)',
        '',
        '    back cover - open (bco)',
        '    front cover - open (fco)',
        '    music - open (mo)',
        '    preface - open (ro)',
        '    score - open (so)',
        '',
        '    score pdf - build (bld)',
        '',
        '    get (get)',
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
        ]
    for line, line_ in zip(menu, menu_):
        assert line == line_


def test_AbjadIDE_display_command_help_02():
    r'''In builds directory.
    '''

    abjad_ide('red~score bb ? q')
    menu = abjad_ide.io.transcript.menus[-1]
    menu_ = [
        'Red Score (2017) : builds : commands',
        '',
        '    every file - edit (ff*)',
        '    every pdf - open (pdf*)',
        '    every string - edit (ee*)',
        '',
        '    call shell (!)',
        '    display command help (?)',
        '    force single column (!!)',
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
        '    copy to clipboard (cp)',
        '    empty clipboard (ce)',
        '    paste from clipboard (cv)',
        '    show clipboard (cs)',
        '',
        '    score pdf - open (spdfo)',
        '',
        '    segment lys - collect (lyc)',
        '',
        '    get (get)',
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
        ]
    for line, line_ in zip(menu, menu_):
        assert line == line_


def test_AbjadIDE_display_command_help_03():
    r'''In contents directory.
    '''

    abjad_ide('red~score ? q')
    menu = abjad_ide.io.transcript.menus[-1]
    menu_ = [
        'Red Score (2017) : commands',
        '',
        '    every file - edit (ff*)',
        '    every pdf - open (pdf*)',
        '    every string - edit (ee*)',
        '',
        '    call shell (!)',
        '    display command help (?)',
        '    force single column (!!)',
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
        '    copy to clipboard (cp)',
        '    empty clipboard (ce)',
        '    paste from clipboard (cv)',
        '    show clipboard (cs)',
        '',
        '    score pdf - open (spdfo)',
        '',
        '    git - commit (ci)',
        '    git - diff (diff)',
        '    git - pull (pull)',
        '    git - push (push)',
        '    git - status (st)',
        '',
        ]
    for line, line_ in zip(menu, menu_):
        assert line == line_


def test_AbjadIDE_display_command_help_04():
    r'''In distribution directory.
    '''

    abjad_ide('red~score dd ? q')
    menu = abjad_ide.io.transcript.menus[-1]
    menu_ = [
        'Red Score (2017) : distribution : commands',
        '',
        '    every file - edit (ff*)',
        '    every pdf - open (pdf*)',
        '    every string - edit (ee*)',
        '',
        '    call shell (!)',
        '    display command help (?)',
        '    force single column (!!)',
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
        '    copy to clipboard (cp)',
        '    empty clipboard (ce)',
        '    paste from clipboard (cv)',
        '    show clipboard (cs)',
        '',
        '    score pdf - open (spdfo)',
        '',
        '    get (get)',
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
        ]
    for line, line_ in zip(menu, menu_):
        assert line == line_


def test_AbjadIDE_display_command_help_05():
    r'''In library.
    '''

    if not abjad_ide._test_external_directory():
        return

    abjad_ide('lib ? q')
    menu = abjad_ide.io.transcript.menus[-1]
    menu_ = [
        'Abjad IDE : library : commands',
        '',
        '    every file - edit (ff*)',
        '    every pdf - open (pdf*)',
        '    every string - edit (ee*)',
        '',
        '    call shell (!)',
        '    display command help (?)',
        '    force single column (!!)',
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
        '    copy to clipboard (cp)',
        '    empty clipboard (ce)',
        '    paste from clipboard (cv)',
        '    show clipboard (cs)',
        '',
        '    get (get)',
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
        ]
    for line, line_ in zip(menu, menu_):
        assert line == line_


def test_AbjadIDE_display_command_help_06():
    r'''In material directory.
    '''

    abjad_ide('red~score mm magic ? q')
    menu = abjad_ide.io.transcript.menus[-1]
    menu_ = [
        'Red Score (2017) : materials : magic_numbers : commands',
        '',
        '    every file - edit (ff*)',
        '    every pdf - open (pdf*)',
        '    every string - edit (ee*)',
        '',
        '    call shell (!)',
        '    display command help (?)',
        '    force single column (!!)',
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
        '    copy to clipboard (cp)',
        '    empty clipboard (ce)',
        '    paste from clipboard (cv)',
        '    show clipboard (cs)',
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
        '    pdf - open (pdfo)',
        '    score pdf - open (spdfo)',
        '',
        '    get (get)',
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
        ]
    for line, line_ in zip(menu, menu_):
        assert line == line_


def test_AbjadIDE_display_command_help_07():
    r'''In materials directory.
    '''

    abjad_ide('red~score mm ? q')
    menu = abjad_ide.io.transcript.menus[-1]
    menu_ = [
        'Red Score (2017) : materials : commands',
        '',
        '    every definition file - check (dfk*)',
        '    every definition file - edit (df*)',
        '    every file - edit (ff*)',
        '    every ly - interpret (lyi*)',
        '    every pdf - make (pdfm*)',
        '    every pdf - open (pdf*)',
        '    every string - edit (ee*)',
        '',
        '    call shell (!)',
        '    display command help (?)',
        '    force single column (!!)',
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
        '    copy to clipboard (cp)',
        '    empty clipboard (ce)',
        '    paste from clipboard (cv)',
        '    show clipboard (cs)',
        '',
        '    score pdf - open (spdfo)',
        '',
        '    get (get)',
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
        ]
    for line, line_ in zip(menu, menu_):
        assert line == line_


def test_AbjadIDE_display_command_help_08():
    r'''In scores directory.
    '''

    abjad_ide('? q')
    menu = abjad_ide.io.transcript.menus[-1]
    menu_ = [
        'Abjad IDE : scores : commands',
        '',
        '    every file - edit (ff*)',
        '    every pdf - open (pdf*)',
        '    every string - edit (ee*)',
        '',
        '    call shell (!)',
        '    display command help (?)',
        '    force single column (!!)',
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
        '    copy to clipboard (cp)',
        '    empty clipboard (ce)',
        '    paste from clipboard (cv)',
        '    show clipboard (cs)',
        '',
        '    get (get)',
        '    new (new)',
        '    remove (rm)',
        '    rename (ren)',
        '',
        '    every package - git commit (ci*)',
        '    every package - git pull (pull*)',
        '    every package - git push (push*)',
        '    every package - git status (st*)',
        '',
        ]
    for line, line_ in zip(menu, menu_):
        assert line == line_


def test_AbjadIDE_display_command_help_09():
    r'''In segment directory.
    '''

    abjad_ide('red~score gg A ? q')
    menu = abjad_ide.io.transcript.menus[-1]
    menu_ = [
        'Red Score (2017) : segments : A : commands',
        '',
        '    every file - edit (ff*)',
        '    every pdf - open (pdf*)',
        '    every string - edit (ee*)',
        '',
        '    call shell (!)',
        '    display command help (?)',
        '    force single column (!!)',
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
        '    copy to clipboard (cp)',
        '    empty clipboard (ce)',
        '    paste from clipboard (cv)',
        '    show clipboard (cs)',
        '',
        '    definition file - check (dfk)',
        '    definition file - edit (df)',
        '',
        '    ly - edit (ly)',
        '    ly - interpret (lyi)',
        '    ly - make (lym)',
        '',
        '    pdf - make (pdfm)',
        '    pdf - open (pdfo)',
        '    score pdf - open (spdfo)',
        '',
        '    midi - make (midim)',
        '',
        '    get (get)',
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
        ]
    for line, line_ in zip(menu, menu_):
        assert line == line_


def test_AbjadIDE_display_command_help_10():
    r'''In segments directory.
    '''

    abjad_ide('red~score gg ? q')
    menu = abjad_ide.io.transcript.menus[-1]
    menu_ = [
        'Red Score (2017) : segments : commands',
        '',
        '    every definition file - check (dfk*)',
        '    every definition file - edit (df*)',
        '    every file - edit (ff*)',
        '    every ly - interpret (lyi*)',
        '    every pdf - make (pdfm*)',
        '    every pdf - open (pdf*)',
        '    every string - edit (ee*)',
        '',
        '    call shell (!)',
        '    display command help (?)',
        '    force single column (!!)',
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
        '    copy to clipboard (cp)',
        '    empty clipboard (ce)',
        '    paste from clipboard (cv)',
        '    show clipboard (cs)',
        '',
        '    score pdf - open (spdfo)',
        '',
        '    get (get)',
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
        ]
    for line, line_ in zip(menu, menu_):
        assert line == line_


def test_AbjadIDE_display_command_help_11():
    r'''In stylesheets directory.
    '''

    abjad_ide('red~score yy ? q')
    menu = abjad_ide.io.transcript.menus[-1]
    menu_ = [
        'Red Score (2017) : stylesheets : commands',
        '',
        '    every file - edit (ff*)',
        '    every pdf - open (pdf*)',
        '    every string - edit (ee*)',
        '',
        '    call shell (!)',
        '    display command help (?)',
        '    force single column (!!)',
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
        '    copy to clipboard (cp)',
        '    empty clipboard (ce)',
        '    paste from clipboard (cv)',
        '    show clipboard (cs)',
        '',
        '    score pdf - open (spdfo)',
        '',
        '    get (get)',
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
        ]
    for line, line_ in zip(menu, menu_):
        assert line == line_


def test_AbjadIDE_display_command_help_12():
    r'''In test directory.
    '''

    abjad_ide('red~score tt ? q')
    menu = abjad_ide.io.transcript.menus[-1]
    menu_ = [
        'Red Score (2017) : test : commands',
        '',
        '    every file - edit (ff*)',
        '    every pdf - open (pdf*)',
        '    every string - edit (ee*)',
        '',
        '    call shell (!)',
        '    display command help (?)',
        '    force single column (!!)',
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
        '    copy to clipboard (cp)',
        '    empty clipboard (ce)',
        '    paste from clipboard (cv)',
        '    show clipboard (cs)',
        '',
        '    score pdf - open (spdfo)',
        '',
        '    get (get)',
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
        ]
    for line, line_ in zip(menu, menu_):
        assert line == line_


def test_AbjadIDE_display_command_help_13():
    r'''In tools directory.
    '''

    abjad_ide('red~score oo ? q')
    menu = abjad_ide.io.transcript.menus[-1]
    menu_ = [
        'Red Score (2017) : tools : commands',
        '',
        '    every file - edit (ff*)',
        '    every pdf - open (pdf*)',
        '    every string - edit (ee*)',
        '',
        '    call shell (!)',
        '    display command help (?)',
        '    force single column (!!)',
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
        '    copy to clipboard (cp)',
        '    empty clipboard (ce)',
        '    paste from clipboard (cv)',
        '    show clipboard (cs)',
        '',
        '    score pdf - open (spdfo)',
        '',
        '    get (get)',
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
        ]
    for line, line_ in zip(menu, menu_):
        assert line == line_


def test_AbjadIDE_display_command_help_14():
    r'''In wrapper directory.
    '''

    abjad_ide('red ww ? q')
    menu = abjad_ide.io.transcript.menus[-1]
    menu_ = [
        'Red Score (2017) : wrapper : commands',
        '',
        '    every file - edit (ff*)',
        '    every pdf - open (pdf*)',
        '    every string - edit (ee*)',
        '',
        '    call shell (!)',
        '    display command help (?)',
        '    force single column (!!)',
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
        '    copy to clipboard (cp)',
        '    empty clipboard (ce)',
        '    paste from clipboard (cv)',
        '    show clipboard (cs)',
        '',
        '    score pdf - open (spdfo)',
        '',
        '    get (get)',
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
        ]
    for line, line_ in zip(menu, menu_):
        assert line == line_
