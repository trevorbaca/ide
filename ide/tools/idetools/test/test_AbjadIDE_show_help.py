import abjad
import ide
abjad_ide = ide.AbjadIDE(test=True)


def test_AbjadIDE_show_help_01():
    r'''In build directory.
    '''

    abjad_ide('red %letter ? q')
    menu = abjad_ide.io.transcript.menus[-1]
    assert menu == [
        'Red Score (2017) : builds : letter : help',
        '',
        '    all - doctest (^^)',
        '    all - edit (@@)',
        '    all - pdfs (**)',
        '    all - pytest (++)',
        '',
        '    back cover - edit (bce)',
        '    back cover - generate (bcg)',
        '    back cover - interpret (bci)',
        '    back cover - open (bco)',
        '    back cover - trash (bct)',
        '',
        '    build - build (bld)',
        '',
        '    clipboard - copy (cp)',
        '    clipboard - empty (cx)',
        '    clipboard - paste (cv)',
        '    clipboard - show (cs)',
        '',
        '    front cover - edit (fce)',
        '    front cover - generate (fcg)',
        '    front cover - interpret (fci)',
        '    front cover - open (fco)',
        '    front cover - trash (fct)',
        '',
        '    git - commit (ci)',
        '    git - diff (diff)',
        '    git - pull (pull)',
        '    git - push (push)',
        '    git - status (st)',
        '',
        '    go - back (-)',
        '    go - directory (%)',
        '    go - library (ll)',
        '    go - quit (q)',
        '    go - scores (ss)',
        '    go - up (..)',
        '',
        '    hop - next score (>>)',
        '    hop - previous score (<<)',
        '',
        '    log - aliases (al)',
        '    log - latex (lx)',
        '    log - lilypond (lp)',
        '',
        '    lys - collect (lyc*)',
        '',
        '    music - edit (me)',
        '    music - generate (mg)',
        '    music - interpret (mi)',
        '    music - open (mo)',
        '    music - trash (mt)',
        '',
        '    package - builds (bb)',
        '    package - builds segments (nn)',
        '    package - contents (cc)',
        '    package - distribution (dd)',
        '    package - etc (ee)',
        '    package - materials (mm)',
        '    package - segments (gg)',
        '    package - stylesheets (yy)',
        '    package - test (tt)',
        '    package - tools (oo)',
        '    package - wrapper (ww)',
        '',
        '    path - duplicate (dup)',
        '    path - get (get)',
        '    path - new (new)',
        '    path - remove (rm)',
        '    path - rename (ren)',
        '',
        '    preface - edit (pe)',
        '    preface - generate (pg)',
        '    preface - interpret (pi)',
        '    preface - open (po)',
        '    preface - trash (pt)',
        '',
        '    score - edit (re)',
        '    score - generate (rg)',
        '    score - interpret (ri)',
        '    score - open (ro)',
        '    score - trash (rt)',
        '',
        '    shell - call (!)',
        '',
        '    show - column (;)',
        '    show - help (?)',
        '',
        '    smart - doctest (^)',
        '    smart - edit (@)',
        '    smart - pdf (*)',
        '    smart - pytest (+)',
        '',
        '    stylesheet - edit (ye)',
        '    stylesheet - generate (yg)',
        '    stylesheet - trash (yt)',
        '',
        '    text - edit (it)',
        '    text - replace (rp)',
        '    text - search (sr)',
        '',
        ]


def test_AbjadIDE_show_help_02():
    r'''In builds directory.
    '''

    abjad_ide('red bb ? q')
    menu = abjad_ide.io.transcript.menus[-1]
    assert menu == [
        'Red Score (2017) : builds : help',
        '',
        '    all - doctest (^^)',
        '    all - edit (@@)',
        '    all - pdfs (**)',
        '    all - pytest (++)',
        '',
        '    clipboard - copy (cp)',
        '    clipboard - empty (cx)',
        '    clipboard - paste (cv)',
        '    clipboard - show (cs)',
        '',
        '    git - commit (ci)',
        '    git - diff (diff)',
        '    git - pull (pull)',
        '    git - push (push)',
        '    git - status (st)',
        '',
        '    go - back (-)',
        '    go - directory (%)',
        '    go - library (ll)',
        '    go - quit (q)',
        '    go - scores (ss)',
        '    go - up (..)',
        '',
        '    hop - next score (>>)',
        '    hop - previous score (<<)',
        '',
        '    log - aliases (al)',
        '    log - latex (lx)',
        '    log - lilypond (lp)',
        '',
        '    lys - collect (lyc*)',
        '',
        '    package - builds (bb)',
        '    package - builds segments (nn)',
        '    package - contents (cc)',
        '    package - distribution (dd)',
        '    package - etc (ee)',
        '    package - materials (mm)',
        '    package - segments (gg)',
        '    package - stylesheets (yy)',
        '    package - test (tt)',
        '    package - tools (oo)',
        '    package - wrapper (ww)',
        '',
        '    path - duplicate (dup)',
        '    path - get (get)',
        '    path - new (new)',
        '    path - remove (rm)',
        '    path - rename (ren)',
        '',
        '    score - open (ro)',
        '',
        '    shell - call (!)',
        '',
        '    show - column (;)',
        '    show - help (?)',
        '',
        '    smart - doctest (^)',
        '    smart - edit (@)',
        '    smart - pdf (*)',
        '    smart - pytest (+)',
        '',
        '    text - edit (it)',
        '    text - replace (rp)',
        '    text - search (sr)',
        '',
        ]


def test_AbjadIDE_show_help_03():
    r'''In builds segments directory.
    '''

    abjad_ide('red nn ? q')
    menu = abjad_ide.io.transcript.menus[-1]
    assert menu == [
        'Red Score (2017) : builds : _segments : help',
        '',
        '    all - doctest (^^)',
        '    all - edit (@@)',
        '    all - pdfs (**)',
        '    all - pytest (++)',
        '',
        '    clipboard - copy (cp)',
        '    clipboard - empty (cx)',
        '    clipboard - paste (cv)',
        '    clipboard - show (cs)',
        '',
        '    git - commit (ci)',
        '    git - diff (diff)',
        '    git - pull (pull)',
        '    git - push (push)',
        '    git - status (st)',
        '',
        '    go - back (-)',
        '    go - directory (%)',
        '    go - library (ll)',
        '    go - quit (q)',
        '    go - scores (ss)',
        '    go - up (..)',
        '',
        '    hop - next score (>>)',
        '    hop - previous score (<<)',
        '',
        '    log - aliases (al)',
        '    log - latex (lx)',
        '    log - lilypond (lp)',
        '',
        '    lys - collect (lyc*)',
        '',
        '    package - builds (bb)',
        '    package - builds segments (nn)',
        '    package - contents (cc)',
        '    package - distribution (dd)',
        '    package - etc (ee)',
        '    package - materials (mm)',
        '    package - segments (gg)',
        '    package - stylesheets (yy)',
        '    package - test (tt)',
        '    package - tools (oo)',
        '    package - wrapper (ww)',
        '',
        '    path - duplicate (dup)',
        '    path - get (get)',
        '    path - new (new)',
        '    path - remove (rm)',
        '    path - rename (ren)',
        '',
        '    score - open (ro)',
        '',
        '    shell - call (!)',
        '',
        '    show - column (;)',
        '    show - help (?)',
        '',
        '    smart - doctest (^)',
        '    smart - edit (@)',
        '    smart - pdf (*)',
        '    smart - pytest (+)',
        '',
        '    text - edit (it)',
        '    text - replace (rp)',
        '    text - search (sr)',
        '',
        ]


def test_AbjadIDE_show_help_04():
    r'''In contents directory.
    '''

    abjad_ide('red ? q')
    menu = abjad_ide.io.transcript.menus[-1]
    assert menu == [
        'Red Score (2017) : help',
        '',
        '    all - doctest (^^)',
        '    all - edit (@@)',
        '    all - pdfs (**)',
        '    all - pytest (++)',
        '',
        '    clipboard - copy (cp)',
        '    clipboard - empty (cx)',
        '    clipboard - paste (cv)',
        '    clipboard - show (cs)',
        '',
        '    git - commit (ci)',
        '    git - diff (diff)',
        '    git - pull (pull)',
        '    git - push (push)',
        '    git - status (st)',
        '',
        '    go - back (-)',
        '    go - directory (%)',
        '    go - library (ll)',
        '    go - quit (q)',
        '    go - scores (ss)',
        '    go - up (..)',
        '',
        '    hop - next score (>>)',
        '    hop - previous score (<<)',
        '',
        '    log - aliases (al)',
        '    log - latex (lx)',
        '    log - lilypond (lp)',
        '',
        '    lys - collect (lyc*)',
        '',
        '    package - builds (bb)',
        '    package - builds segments (nn)',
        '    package - contents (cc)',
        '    package - distribution (dd)',
        '    package - etc (ee)',
        '    package - materials (mm)',
        '    package - segments (gg)',
        '    package - stylesheets (yy)',
        '    package - test (tt)',
        '    package - tools (oo)',
        '    package - wrapper (ww)',
        '',
        '    score - open (ro)',
        '',
        '    shell - call (!)',
        '',
        '    show - column (;)',
        '    show - help (?)',
        '',
        '    smart - doctest (^)',
        '    smart - edit (@)',
        '    smart - pdf (*)',
        '    smart - pytest (+)',
        '',
        '    text - edit (it)',
        '    text - replace (rp)',
        '    text - search (sr)',
        '',
        ]


def test_AbjadIDE_show_help_05():
    r'''In distribution directory.
    '''

    abjad_ide('red dd ? q')
    menu = abjad_ide.io.transcript.menus[-1]
    assert menu == [
        'Red Score (2017) : distribution : help',
        '',
        '    all - doctest (^^)',
        '    all - edit (@@)',
        '    all - pdfs (**)',
        '    all - pytest (++)',
        '',
        '    clipboard - copy (cp)',
        '    clipboard - empty (cx)',
        '    clipboard - paste (cv)',
        '    clipboard - show (cs)',
        '',
        '    git - commit (ci)',
        '    git - diff (diff)',
        '    git - pull (pull)',
        '    git - push (push)',
        '    git - status (st)',
        '',
        '    go - back (-)',
        '    go - directory (%)',
        '    go - library (ll)',
        '    go - quit (q)',
        '    go - scores (ss)',
        '    go - up (..)',
        '',
        '    hop - next score (>>)',
        '    hop - previous score (<<)',
        '',
        '    log - aliases (al)',
        '    log - latex (lx)',
        '    log - lilypond (lp)',
        '',
        '    lys - collect (lyc*)',
        '',
        '    package - builds (bb)',
        '    package - builds segments (nn)',
        '    package - contents (cc)',
        '    package - distribution (dd)',
        '    package - etc (ee)',
        '    package - materials (mm)',
        '    package - segments (gg)',
        '    package - stylesheets (yy)',
        '    package - test (tt)',
        '    package - tools (oo)',
        '    package - wrapper (ww)',
        '',
        '    path - duplicate (dup)',
        '    path - get (get)',
        '    path - new (new)',
        '    path - remove (rm)',
        '    path - rename (ren)',
        '',
        '    score - open (ro)',
        '',
        '    shell - call (!)',
        '',
        '    show - column (;)',
        '    show - help (?)',
        '',
        '    smart - doctest (^)',
        '    smart - edit (@)',
        '    smart - pdf (*)',
        '    smart - pytest (+)',
        '',
        '    text - edit (it)',
        '    text - replace (rp)',
        '    text - search (sr)',
        '',
        ]


def test_AbjadIDE_show_help_06():
    r'''In library.
    '''

    if not abjad_ide.test_baca_directories():
        return

    abjad_ide('ll ? q')
    menu = abjad_ide.io.transcript.menus[-1]
    assert menu == [
        'Abjad IDE : library : help',
        '',
        '    all - doctest (^^)',
        '    all - edit (@@)',
        '    all - pdfs (**)',
        '    all - pytest (++)',
        '',
        '    clipboard - copy (cp)',
        '    clipboard - empty (cx)',
        '    clipboard - paste (cv)',
        '    clipboard - show (cs)',
        '',
        '    git - commit (ci)',
        '    git - diff (diff)',
        '    git - pull (pull)',
        '    git - push (push)',
        '    git - status (st)',
        '',
        '    go - back (-)',
        '    go - directory (%)',
        '    go - library (ll)',
        '    go - quit (q)',
        '    go - scores (ss)',
        '    go - up (..)',
        '',
        '    log - aliases (al)',
        '    log - latex (lx)',
        '    log - lilypond (lp)',
        '',
        '    path - duplicate (dup)',
        '    path - new (new)',
        '    path - remove (rm)',
        '    path - rename (ren)',
        '',
        '    shell - call (!)',
        '',
        '    show - column (;)',
        '    show - help (?)',
        '',
        '    smart - doctest (^)',
        '    smart - edit (@)',
        '    smart - pdf (*)',
        '    smart - pytest (+)',
        '',
        '    text - edit (it)',
        '    text - replace (rp)',
        '    text - search (sr)',
        '',
        ]


def test_AbjadIDE_show_help_07():
    r'''In material directory.
    '''

    abjad_ide('red %magic ? q')
    menu = abjad_ide.io.transcript.menus[-1]
    assert menu == [
        'Red Score (2017) : materials : magic_numbers : help',
        '',
        '    all - doctest (^^)',
        '    all - edit (@@)',
        '    all - pdfs (**)',
        '    all - pytest (++)',
        '',
        '    clipboard - copy (cp)',
        '    clipboard - empty (cx)',
        '    clipboard - paste (cv)',
        '    clipboard - show (cs)',
        '',
        '    definition - check (dfk)',
        '    definition - edit (dfe)',
        '    definition - trash (dft)',
        '',
        '    git - commit (ci)',
        '    git - diff (diff)',
        '    git - pull (pull)',
        '    git - push (push)',
        '    git - status (st)',
        '',
        '    go - back (-)',
        '    go - directory (%)',
        '    go - library (ll)',
        '    go - quit (q)',
        '    go - scores (ss)',
        '    go - up (..)',
        '',
        '    hop - next package (>)',
        '    hop - next score (>>)',
        '    hop - previous package (<)',
        '    hop - previous score (<<)',
        '',
        '    log - aliases (al)',
        '    log - latex (lx)',
        '    log - lilypond (lp)',
        '',
        '    illustrate - edit (ill)',
        '    illustrate - make (illm)',
        '',
        '    ly - edit (lye)',
        '    ly - interpret (lyi)',
        '    ly - make (lym)',
        '    ly - trash (lyt)',
        '',
        '    lys - collect (lyc*)',
        '',
        '    package - builds (bb)',
        '    package - builds segments (nn)',
        '    package - contents (cc)',
        '    package - distribution (dd)',
        '    package - etc (ee)',
        '    package - materials (mm)',
        '    package - segments (gg)',
        '    package - stylesheets (yy)',
        '    package - test (tt)',
        '    package - tools (oo)',
        '    package - wrapper (ww)',
        '',
        '    path - get (get)',
        '    path - new (new)',
        '    path - remove (rm)',
        '    path - rename (ren)',
        '',
        '    pdf - make (pdfm)',
        '    pdf - open (pdfo)',
        '    pdf - trash (pdft)',
        '',
        '    score - open (ro)',
        '',
        '    shell - call (!)',
        '',
        '    show - column (;)',
        '    show - help (?)',
        '',
        '    smart - doctest (^)',
        '    smart - edit (@)',
        '    smart - pdf (*)',
        '    smart - pytest (+)',
        '',
        '    text - edit (it)',
        '    text - replace (rp)',
        '    text - search (sr)',
        '',
        ]


def test_AbjadIDE_show_help_08():
    r'''In materials directory.
    '''

    abjad_ide('red mm ? q')
    menu = abjad_ide.io.transcript.menus[-1]
    assert menu == [
        'Red Score (2017) : materials : help',
        '',
        '    all - doctest (^^)',
        '    all - edit (@@)',
        '    all - pdfs (**)',
        '    all - pytest (++)',
        '',
        '    clipboard - copy (cp)',
        '    clipboard - empty (cx)',
        '    clipboard - paste (cv)',
        '    clipboard - show (cs)',
        '',
        '    definitions - check (dfk*)',
        '    definitions - edit (dfe*)',
        '    definitions - trash (dft*)',
        '',
        '    git - commit (ci)',
        '    git - diff (diff)',
        '    git - pull (pull)',
        '    git - push (push)',
        '    git - status (st)',
        '',
        '    go - back (-)',
        '    go - directory (%)',
        '    go - library (ll)',
        '    go - quit (q)',
        '    go - scores (ss)',
        '    go - up (..)',
        '',
        '    hop - next package (>)',
        '    hop - next score (>>)',
        '    hop - previous package (<)',
        '    hop - previous score (<<)',
        '',
        '    log - aliases (al)',
        '    log - latex (lx)',
        '    log - lilypond (lp)',
        '',
        '    lys - collect (lyc*)',
        '    lys - interpret (lyi*)',
        '    lys - make (lym*)',
        '    lys - trash (lyt*)',
        '',
        '    package - builds (bb)',
        '    package - builds segments (nn)',
        '    package - contents (cc)',
        '    package - distribution (dd)',
        '    package - etc (ee)',
        '    package - materials (mm)',
        '    package - segments (gg)',
        '    package - stylesheets (yy)',
        '    package - test (tt)',
        '    package - tools (oo)',
        '    package - wrapper (ww)',
        '',
        '    path - duplicate (dup)',
        '    path - get (get)',
        '    path - new (new)',
        '    path - remove (rm)',
        '    path - rename (ren)',
        '',
        '    pdfs - make (pdfm*)',
        '    pdfs - trash (pdft*)',
        '',
        '    score - open (ro)',
        '',
        '    shell - call (!)',
        '',
        '    show - column (;)',
        '    show - help (?)',
        '',
        '    smart - doctest (^)',
        '    smart - edit (@)',
        '    smart - pdf (*)',
        '    smart - pytest (+)',
        '',
        '    text - edit (it)',
        '    text - replace (rp)',
        '    text - search (sr)',
        '',
        ]


def test_AbjadIDE_show_help_09():
    r'''In scores directory.
    '''

    abjad_ide('? q')
    menu = abjad_ide.io.transcript.menus[-1]
    assert menu == [
        'Abjad IDE : scores : help',
        '',
        '    all - doctest (^^)',
        '    all - edit (@@)',
        '    all - pdfs (**)',
        '    all - pytest (++)',
        '',
        '    clipboard - copy (cp)',
        '    clipboard - empty (cx)',
        '    clipboard - paste (cv)',
        '    clipboard - show (cs)',
        '',
        '    git - commit (ci*)',
        '    git - diff (diff*)',
        '    git - pull (pull*)',
        '    git - push (push*)',
        '    git - status (st*)',
        '',
        '    go - back (-)',
        '    go - directory (%)',
        '    go - library (ll)',
        '    go - quit (q)',
        '    go - scores (ss)',
        '    go - up (..)',
        '',
        '    hop - next score (>>)',
        '    hop - previous score (<<)',
        '',
        '    log - aliases (al)',
        '    log - latex (lx)',
        '    log - lilypond (lp)',
        '',
        '    path - duplicate (dup)',
        '    path - new (new)',
        '    path - remove (rm)',
        '    path - rename (ren)',
        '',
        '    scores - open (ro*)',
        '',
        '    shell - call (!)',
        '',
        '    show - column (;)',
        '    show - help (?)',
        '',
        '    text - edit (it)',
        '    text - replace (rp)',
        '    text - search (sr)',
        '',
        ]


def test_AbjadIDE_show_help_10():
    r'''In segment directory.
    '''

    abjad_ide('red %A ? q')
    menu = abjad_ide.io.transcript.menus[-1]
    assert menu == [
        'Red Score (2017) : segments : A : help',
        '',
        '    all - doctest (^^)',
        '    all - edit (@@)',
        '    all - pdfs (**)',
        '    all - pytest (++)',
        '',
        '    clipboard - copy (cp)',
        '    clipboard - empty (cx)',
        '    clipboard - paste (cv)',
        '    clipboard - show (cs)',
        '',
        '    definition - check (dfk)',
        '    definition - edit (dfe)',
        '    definition - trash (dft)',
        '',
        '    git - commit (ci)',
        '    git - diff (diff)',
        '    git - pull (pull)',
        '    git - push (push)',
        '    git - status (st)',
        '',
        '    go - back (-)',
        '    go - directory (%)',
        '    go - library (ll)',
        '    go - quit (q)',
        '    go - scores (ss)',
        '    go - up (..)',
        '',
        '    hop - next package (>)',
        '    hop - next score (>>)',
        '    hop - previous package (<)',
        '    hop - previous score (<<)',
        '',
        '    log - aliases (al)',
        '    log - latex (lx)',
        '    log - lilypond (lp)',
        '',
        '    ly - edit (lye)',
        '    ly - interpret (lyi)',
        '    ly - make (lym)',
        '    ly - trash (lyt)',
        '',
        '    lys - collect (lyc*)',
        '',
        '    midi - make (midm)',
        '',
        '    package - builds (bb)',
        '    package - builds segments (nn)',
        '    package - contents (cc)',
        '    package - distribution (dd)',
        '    package - etc (ee)',
        '    package - materials (mm)',
        '    package - segments (gg)',
        '    package - stylesheets (yy)',
        '    package - test (tt)',
        '    package - tools (oo)',
        '    package - wrapper (ww)',
        '',
        '    path - get (get)',
        '    path - new (new)',
        '    path - remove (rm)',
        '    path - rename (ren)',
        '',
        '    pdf - make (pdfm)',
        '    pdf - open (pdfo)',
        '    pdf - trash (pdft)',
        '',
        '    score - open (ro)',
        '',
        '    shell - call (!)',
        '',
        '    show - column (;)',
        '    show - help (?)',
        '',
        '    smart - doctest (^)',
        '    smart - edit (@)',
        '    smart - pdf (*)',
        '    smart - pytest (+)',
        '',
        '    text - edit (it)',
        '    text - replace (rp)',
        '    text - search (sr)',
        '',
        ]


def test_AbjadIDE_show_help_11():
    r'''In segments directory.
    '''

    abjad_ide('red gg ? q')
    menu = abjad_ide.io.transcript.menus[-1]
    assert menu == [
        'Red Score (2017) : segments : help',
        '',
        '    all - doctest (^^)',
        '    all - edit (@@)',
        '    all - pdfs (**)',
        '    all - pytest (++)',
        '',
        '    clipboard - copy (cp)',
        '    clipboard - empty (cx)',
        '    clipboard - paste (cv)',
        '    clipboard - show (cs)',
        '',
        '    definitions - check (dfk*)',
        '    definitions - edit (dfe*)',
        '    definitions - trash (dft*)',
        '',
        '    git - commit (ci)',
        '    git - diff (diff)',
        '    git - pull (pull)',
        '    git - push (push)',
        '    git - status (st)',
        '',
        '    go - back (-)',
        '    go - directory (%)',
        '    go - library (ll)',
        '    go - quit (q)',
        '    go - scores (ss)',
        '    go - up (..)',
        '',
        '    hop - next package (>)',
        '    hop - next score (>>)',
        '    hop - previous package (<)',
        '    hop - previous score (<<)',
        '',
        '    log - aliases (al)',
        '    log - latex (lx)',
        '    log - lilypond (lp)',
        '',
        '    lys - collect (lyc*)',
        '    lys - interpret (lyi*)',
        '    lys - make (lym*)',
        '    lys - trash (lyt*)',
        '',
        '    package - builds (bb)',
        '    package - builds segments (nn)',
        '    package - contents (cc)',
        '    package - distribution (dd)',
        '    package - etc (ee)',
        '    package - materials (mm)',
        '    package - segments (gg)',
        '    package - stylesheets (yy)',
        '    package - test (tt)',
        '    package - tools (oo)',
        '    package - wrapper (ww)',
        '',
        '    path - duplicate (dup)',
        '    path - get (get)',
        '    path - new (new)',
        '    path - remove (rm)',
        '    path - rename (ren)',
        '',
        '    pdfs - make (pdfm*)',
        '    pdfs - trash (pdft*)',
        '',
        '    score - open (ro)',
        '',
        '    shell - call (!)',
        '',
        '    show - column (;)',
        '    show - help (?)',
        '',
        '    smart - doctest (^)',
        '    smart - edit (@)',
        '    smart - pdf (*)',
        '    smart - pytest (+)',
        '',
        '    text - edit (it)',
        '    text - replace (rp)',
        '    text - search (sr)',
        '',
        ]


def test_AbjadIDE_show_help_12():
    r'''In stylesheets directory.
    '''

    abjad_ide('red yy ? q')
    menu = abjad_ide.io.transcript.menus[-1]
    assert menu == [
        'Red Score (2017) : stylesheets : help',
        '',
        '    all - doctest (^^)',
        '    all - edit (@@)',
        '    all - pdfs (**)',
        '    all - pytest (++)',
        '',
        '    clipboard - copy (cp)',
        '    clipboard - empty (cx)',
        '    clipboard - paste (cv)',
        '    clipboard - show (cs)',
        '',
        '    git - commit (ci)',
        '    git - diff (diff)',
        '    git - pull (pull)',
        '    git - push (push)',
        '    git - status (st)',
        '',
        '    go - back (-)',
        '    go - directory (%)',
        '    go - library (ll)',
        '    go - quit (q)',
        '    go - scores (ss)',
        '    go - up (..)',
        '',
        '    hop - next score (>>)',
        '    hop - previous score (<<)',
        '',
        '    log - aliases (al)',
        '    log - latex (lx)',
        '    log - lilypond (lp)',
        '',
        '    lys - collect (lyc*)',
        '',
        '    package - builds (bb)',
        '    package - builds segments (nn)',
        '    package - contents (cc)',
        '    package - distribution (dd)',
        '    package - etc (ee)',
        '    package - materials (mm)',
        '    package - segments (gg)',
        '    package - stylesheets (yy)',
        '    package - test (tt)',
        '    package - tools (oo)',
        '    package - wrapper (ww)',
        '',
        '    path - duplicate (dup)',
        '    path - get (get)',
        '    path - new (new)',
        '    path - remove (rm)',
        '    path - rename (ren)',
        '',
        '    score - open (ro)',
        '',
        '    shell - call (!)',
        '',
        '    show - column (;)',
        '    show - help (?)',
        '',
        '    smart - doctest (^)',
        '    smart - edit (@)',
        '    smart - pdf (*)',
        '    smart - pytest (+)',
        '',
        '    text - edit (it)',
        '    text - replace (rp)',
        '    text - search (sr)',
        '',
        ]


def test_AbjadIDE_show_help_13():
    r'''In test directory.
    '''

    abjad_ide('red tt ? q')
    menu = abjad_ide.io.transcript.menus[-1]
    assert menu == [
        'Red Score (2017) : test : help',
        '',
        '    all - doctest (^^)',
        '    all - edit (@@)',
        '    all - pdfs (**)',
        '    all - pytest (++)',
        '',
        '    clipboard - copy (cp)',
        '    clipboard - empty (cx)',
        '    clipboard - paste (cv)',
        '    clipboard - show (cs)',
        '',
        '    git - commit (ci)',
        '    git - diff (diff)',
        '    git - pull (pull)',
        '    git - push (push)',
        '    git - status (st)',
        '',
        '    go - back (-)',
        '    go - directory (%)',
        '    go - library (ll)',
        '    go - quit (q)',
        '    go - scores (ss)',
        '    go - up (..)',
        '',
        '    hop - next score (>>)',
        '    hop - previous score (<<)',
        '',
        '    log - aliases (al)',
        '    log - latex (lx)',
        '    log - lilypond (lp)',
        '',
        '    lys - collect (lyc*)',
        '',
        '    package - builds (bb)',
        '    package - builds segments (nn)',
        '    package - contents (cc)',
        '    package - distribution (dd)',
        '    package - etc (ee)',
        '    package - materials (mm)',
        '    package - segments (gg)',
        '    package - stylesheets (yy)',
        '    package - test (tt)',
        '    package - tools (oo)',
        '    package - wrapper (ww)',
        '',
        '    path - duplicate (dup)',
        '    path - get (get)',
        '    path - new (new)',
        '    path - remove (rm)',
        '    path - rename (ren)',
        '',
        '    score - open (ro)',
        '',
        '    shell - call (!)',
        '',
        '    show - column (;)',
        '    show - help (?)',
        '',
        '    smart - doctest (^)',
        '    smart - edit (@)',
        '    smart - pdf (*)',
        '    smart - pytest (+)',
        '',
        '    text - edit (it)',
        '    text - replace (rp)',
        '    text - search (sr)',
        '',
        ]


def test_AbjadIDE_show_help_14():
    r'''In tools directory.
    '''

    abjad_ide('red oo ? q')
    menu = abjad_ide.io.transcript.menus[-1]
    assert menu == [
        'Red Score (2017) : tools : help',
        '',
        '    all - doctest (^^)',
        '    all - edit (@@)',
        '    all - pdfs (**)',
        '    all - pytest (++)',
        '',
        '    clipboard - copy (cp)',
        '    clipboard - empty (cx)',
        '    clipboard - paste (cv)',
        '    clipboard - show (cs)',
        '',
        '    git - commit (ci)',
        '    git - diff (diff)',
        '    git - pull (pull)',
        '    git - push (push)',
        '    git - status (st)',
        '',
        '    go - back (-)',
        '    go - directory (%)',
        '    go - library (ll)',
        '    go - quit (q)',
        '    go - scores (ss)',
        '    go - up (..)',
        '',
        '    hop - next score (>>)',
        '    hop - previous score (<<)',
        '',
        '    log - aliases (al)',
        '    log - latex (lx)',
        '    log - lilypond (lp)',
        '',
        '    lys - collect (lyc*)',
        '',
        '    package - builds (bb)',
        '    package - builds segments (nn)',
        '    package - contents (cc)',
        '    package - distribution (dd)',
        '    package - etc (ee)',
        '    package - materials (mm)',
        '    package - segments (gg)',
        '    package - stylesheets (yy)',
        '    package - test (tt)',
        '    package - tools (oo)',
        '    package - wrapper (ww)',
        '',
        '    path - duplicate (dup)',
        '    path - get (get)',
        '    path - new (new)',
        '    path - remove (rm)',
        '    path - rename (ren)',
        '',
        '    score - open (ro)',
        '',
        '    shell - call (!)',
        '',
        '    show - column (;)',
        '    show - help (?)',
        '',
        '    smart - doctest (^)',
        '    smart - edit (@)',
        '    smart - pdf (*)',
        '    smart - pytest (+)',
        '',
        '    text - edit (it)',
        '    text - replace (rp)',
        '    text - search (sr)',
        '',
        ]


def test_AbjadIDE_show_help_15():
    r'''In wrapper directory.
    '''

    abjad_ide('red ww ? q')
    menu = abjad_ide.io.transcript.menus[-1]
    assert menu == [
        'Red Score (2017) : wrapper : help',
        '',
        '    all - doctest (^^)',
        '    all - edit (@@)',
        '    all - pdfs (**)',
        '    all - pytest (++)',
        '',
        '    clipboard - copy (cp)',
        '    clipboard - empty (cx)',
        '    clipboard - paste (cv)',
        '    clipboard - show (cs)',
        '',
        '    git - commit (ci)',
        '    git - diff (diff)',
        '    git - pull (pull)',
        '    git - push (push)',
        '    git - status (st)',
        '',
        '    go - back (-)',
        '    go - directory (%)',
        '    go - library (ll)',
        '    go - quit (q)',
        '    go - scores (ss)',
        '    go - up (..)',
        '',
        '    hop - next score (>>)',
        '    hop - previous score (<<)',
        '',
        '    log - aliases (al)',
        '    log - latex (lx)',
        '    log - lilypond (lp)',
        '',
        '    lys - collect (lyc*)',
        '',
        '    package - builds (bb)',
        '    package - builds segments (nn)',
        '    package - contents (cc)',
        '    package - distribution (dd)',
        '    package - etc (ee)',
        '    package - materials (mm)',
        '    package - segments (gg)',
        '    package - stylesheets (yy)',
        '    package - test (tt)',
        '    package - tools (oo)',
        '    package - wrapper (ww)',
        '',
        '    path - duplicate (dup)',
        '    path - get (get)',
        '    path - new (new)',
        '    path - remove (rm)',
        '    path - rename (ren)',
        '',
        '    score - open (ro)',
        '',
        '    shell - call (!)',
        '',
        '    show - column (;)',
        '    show - help (?)',
        '',
        '    smart - doctest (^)',
        '    smart - edit (@)',
        '    smart - pdf (*)',
        '    smart - pytest (+)',
        '',
        '    text - edit (it)',
        '    text - replace (rp)',
        '    text - search (sr)',
        '',
        ]
