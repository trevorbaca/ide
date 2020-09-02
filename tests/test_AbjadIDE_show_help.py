import ide

abjad_ide = ide.AbjadIDE(test=True)


def test_AbjadIDE_show_help_01():
    """
    In _assets directory.
    """

    abjad_ide("red bb _assets ? q")
    menu = abjad_ide.io.transcript.menus[-1]
    assert menu == [
        "Red Score (2017) : builds : _assets (empty) : help",
        "",
        "    clipboard - copy (cbc)",
        "    clipboard - empty (cbe)",
        "    clipboard - paste (cbv)",
        "    clipboard - show (cbs)",
        "",
        "    directory - builds (bb)",
        "    directory - contents (cc)",
        "    directory - distribution (dd)",
        "    directory - etc (ee)",
        "    directory - scores (ss)",
        "    directory - segments (gg)",
        "    directory - stylesheets (yy)",
        "    directory - wrapper (ww)",
        "",
        "    edit - files (ef)",
        "    edit - string (es)",
        "",
        "    go - back (-)",
        "    go - quit (q)",
        "    go - up (..)",
        "",
        "    hop - next score (>>)",
        "    hop - previous score (<<)",
        "",
        "    show - column (;)",
        "    show - help (?)",
        "",
    ]


def test_AbjadIDE_show_help_02():
    """
    In _segments directory.
    """

    abjad_ide("red bb letter _segments ? q")
    menu = abjad_ide.io.transcript.menus[-1]
    assert menu == [
        "Red Score (2017) : builds : letter-score : _segments (empty) : help",
        "",
        "    back-cover.pdf - open (bcpo)",
        "    back-cover.tex - edit (bcte)",
        "    back-cover.tex - interpret (bcti)",
        "",
        "    clipboard - copy (cbc)",
        "    clipboard - empty (cbe)",
        "    clipboard - paste (cbv)",
        "    clipboard - show (cbs)",
        "",
        "    directory - builds (bb)",
        "    directory - contents (cc)",
        "    directory - distribution (dd)",
        "    directory - etc (ee)",
        "    directory - scores (ss)",
        "    directory - segments (gg)",
        "    directory - stylesheets (yy)",
        "    directory - wrapper (ww)",
        "",
        "    edit - files (ef)",
        "    edit - string (es)",
        "",
        "    front-cover.pdf - open (fcpo)",
        "    front-cover.tex - edit (fcte)",
        "    front-cover.tex - interpret (fcti)",
        "",
        "    go - back (-)",
        "    go - quit (q)",
        "    go - up (..)",
        "",
        "    hop - next score (>>)",
        "    hop - previous score (<<)",
        "",
        "    layout.ly - edit (lle)",
        "    layout.ly - make (llm)",
        "    layout.py - edit (lpe)",
        "",
        "    music.ly - edit (mle)",
        "    music.ly - generate (mlg)",
        "    music.ly - interpret (mli)",
        "    music.ly - xinterpret (mlx)",
        "    music.pdf - open (mpo)",
        "",
        "    hide (hide)",
        "    show (show)",
        "    tag - hide (th)",
        "    tag - show (ts)",
        "",
        "    color (color)",
        "    uncolor (uncolor)",
        "",
        "    preface.pdf - open (pfpo)",
        "    preface.tex - edit (pfte)",
        "    preface.tex - interpret (pfti)",
        "",
        "    score.pdf - build (spb)",
        "    score.tex - edit (ste)",
        "    score.tex - generate (stg)",
        "    score.tex - interpret (sti)",
        "",
        "    segments - collect (ggc)",
        "    segments - handle build tags (btags)",
        "    segments - handle part tags (ptags)",
        "",
        "    show - column (;)",
        "    show - help (?)",
        "",
        "    stylesheet.ily - edit (ssie)",
        "    stylesheet.ily - generate (ssig)",
        "",
    ]


def test_AbjadIDE_show_help_03():
    """
    In build directory.
    """

    abjad_ide("red bb letter ? q")
    menu = abjad_ide.io.transcript.menus[-1]

    assert menu == [
        "Red Score (2017) : builds : letter-score : help",
        "",
        "    back-cover.pdf - open (bcpo)",
        "    back-cover.tex - edit (bcte)",
        "    back-cover.tex - interpret (bcti)",
        "",
        "    clipboard - copy (cbc)",
        "    clipboard - empty (cbe)",
        "    clipboard - paste (cbv)",
        "    clipboard - show (cbs)",
        "",
        "    directory - builds (bb)",
        "    directory - contents (cc)",
        "    directory - distribution (dd)",
        "    directory - etc (ee)",
        "    directory - scores (ss)",
        "    directory - segments (gg)",
        "    directory - stylesheets (yy)",
        "    directory - wrapper (ww)",
        "",
        "    edit - files (ef)",
        "    edit - string (es)",
        "",
        "    front-cover.pdf - open (fcpo)",
        "    front-cover.tex - edit (fcte)",
        "    front-cover.tex - interpret (fcti)",
        "",
        "    go - back (-)",
        "    go - quit (q)",
        "    go - up (..)",
        "",
        "    hop - next score (>>)",
        "    hop - previous score (<<)",
        "",
        "    layout.ly - edit (lle)",
        "    layout.ly - make (llm)",
        "    layout.py - edit (lpe)",
        "",
        "    music.ly - edit (mle)",
        "    music.ly - generate (mlg)",
        "    music.ly - interpret (mli)",
        "    music.ly - xinterpret (mlx)",
        "    music.pdf - open (mpo)",
        "",
        "    hide (hide)",
        "    show (show)",
        "    tag - hide (th)",
        "    tag - show (ts)",
        "",
        "    color (color)",
        "    uncolor (uncolor)",
        "",
        "    preface.pdf - open (pfpo)",
        "    preface.tex - edit (pfte)",
        "    preface.tex - interpret (pfti)",
        "",
        "    score.pdf - build (spb)",
        "    score.tex - edit (ste)",
        "    score.tex - generate (stg)",
        "    score.tex - interpret (sti)",
        "",
        "    segments - collect (ggc)",
        "    segments - handle build tags (btags)",
        "    segments - handle part tags (ptags)",
        "",
        "    show - column (;)",
        "    show - help (?)",
        "",
        "    stylesheet.ily - edit (ssie)",
        "    stylesheet.ily - generate (ssig)",
        "",
    ]


def test_AbjadIDE_show_help_04():
    """
    In builds directory.
    """

    abjad_ide("red bb ? q")
    menu = abjad_ide.io.transcript.menus[-1]
    assert menu == [
        "Red Score (2017) : builds : help",
        "",
        "    clipboard - copy (cbc)",
        "    clipboard - empty (cbe)",
        "    clipboard - paste (cbv)",
        "    clipboard - show (cbs)",
        "",
        "    directory - builds (bb)",
        "    directory - contents (cc)",
        "    directory - distribution (dd)",
        "    directory - etc (ee)",
        "    directory - scores (ss)",
        "    directory - segments (gg)",
        "    directory - stylesheets (yy)",
        "    directory - wrapper (ww)",
        "",
        "    edit - files (ef)",
        "    edit - string (es)",
        "",
        "    go - back (-)",
        "    go - quit (q)",
        "    go - up (..)",
        "",
        "    hop - next score (>>)",
        "    hop - previous score (<<)",
        "",
        "    layout.ly - edit (lle)",
        "    layout.ly - make (llm)",
        "    layout.py - edit (lpe)",
        "",
        "    hide (hide)",
        "    show (show)",
        "    tag - hide (th)",
        "    tag - show (ts)",
        "",
        "    path - new (new)",
        "",
        "    color (color)",
        "    uncolor (uncolor)",
        "",
        "    show - column (;)",
        "    show - help (?)",
        "",
    ]


def test_AbjadIDE_show_help_05():
    """
    In contents directory.
    """

    abjad_ide("red ? q")
    menu = abjad_ide.io.transcript.menus[-1]
    assert menu == [
        "Red Score (2017) : help",
        "",
        "    clipboard - copy (cbc)",
        "    clipboard - empty (cbe)",
        "    clipboard - paste (cbv)",
        "    clipboard - show (cbs)",
        "",
        "    directory - builds (bb)",
        "    directory - contents (cc)",
        "    directory - distribution (dd)",
        "    directory - etc (ee)",
        "    directory - scores (ss)",
        "    directory - segments (gg)",
        "    directory - stylesheets (yy)",
        "    directory - wrapper (ww)",
        "",
        "    edit - files (ef)",
        "    edit - string (es)",
        "",
        "    go - back (-)",
        "    go - quit (q)",
        "    go - up (..)",
        "",
        "    hop - next score (>>)",
        "    hop - previous score (<<)",
        "",
        "    show - column (;)",
        "    show - help (?)",
        "",
    ]


def test_AbjadIDE_show_help_06():
    """
    In distribution directory.
    """

    abjad_ide("red dd ? q")
    menu = abjad_ide.io.transcript.menus[-1]
    assert menu == [
        "Red Score (2017) : distribution : help",
        "",
        "    clipboard - copy (cbc)",
        "    clipboard - empty (cbe)",
        "    clipboard - paste (cbv)",
        "    clipboard - show (cbs)",
        "",
        "    directory - builds (bb)",
        "    directory - contents (cc)",
        "    directory - distribution (dd)",
        "    directory - etc (ee)",
        "    directory - scores (ss)",
        "    directory - segments (gg)",
        "    directory - stylesheets (yy)",
        "    directory - wrapper (ww)",
        "",
        "    edit - files (ef)",
        "    edit - string (es)",
        "",
        "    go - back (-)",
        "    go - quit (q)",
        "    go - up (..)",
        "",
        "    hop - next score (>>)",
        "    hop - previous score (<<)",
        "",
        "    show - column (;)",
        "    show - help (?)",
        "",
    ]


def test_AbjadIDE_show_help_07():
    """
    In parts directory.
    """

    with ide.Test():

        abjad_ide("gre bb new parts arch-a-parts arch~a ARCH-A y q")
        abjad_ide("gre bb arch-a-parts ? q")

    menu = abjad_ide.io.transcript.menus[-1]
    assert menu == [
        "Green Score (2018) : builds : arch-a-parts : help",
        "",
        "    back-cover.pdf - open (bcpo)",
        "    back-cover.tex - edit (bcte)",
        "    back-cover.tex - interpret (bcti)",
        "",
        "    clipboard - copy (cbc)",
        "    clipboard - empty (cbe)",
        "    clipboard - paste (cbv)",
        "    clipboard - show (cbs)",
        "",
        "    directory - builds (bb)",
        "    directory - contents (cc)",
        "    directory - distribution (dd)",
        "    directory - etc (ee)",
        "    directory - scores (ss)",
        "    directory - segments (gg)",
        "    directory - stylesheets (yy)",
        "    directory - wrapper (ww)",
        "",
        "    edit - files (ef)",
        "    edit - string (es)",
        "",
        "    front-cover.pdf - open (fcpo)",
        "    front-cover.tex - edit (fcte)",
        "    front-cover.tex - interpret (fcti)",
        "",
        "    go - back (-)",
        "    go - quit (q)",
        "    go - up (..)",
        "",
        "    hop - next score (>>)",
        "    hop - previous score (<<)",
        "",
        "    layout.ly - edit (lle)",
        "    layout.ly - make (llm)",
        "    layout.py - edit (lpe)",
        "    layout.py - propagate (lpp)",
        "",
        "    music.ly - edit (mle)",
        "    music.ly - generate (mlg)",
        "    music.ly - interpret (mli)",
        "    music.ly - xinterpret (mlx)",
        "    music.pdf - open (mpo)",
        "",
        "    hide (hide)",
        "    show (show)",
        "    tag - hide (th)",
        "    tag - show (ts)",
        "",
        "    part.pdf - build (ppb)",
        "    part.pdf - open (ppo)",
        "    part.tex - edit (pte)",
        "    part.tex - interpret (pti)",
        "",
        "    color (color)",
        "    uncolor (uncolor)",
        "",
        "    preface.pdf - open (pfpo)",
        "    preface.tex - edit (pfte)",
        "    preface.tex - interpret (pfti)",
        "",
        "    segments - collect (ggc)",
        "    segments - handle build tags (btags)",
        "    segments - handle part tags (ptags)",
        "",
        "    show - column (;)",
        "    show - help (?)",
        "",
        "    stylesheet.ily - edit (ssie)",
        "    stylesheet.ily - generate (ssig)",
        "",
    ]


def test_AbjadIDE_show_help_08():
    """
    In scores directory.
    """

    abjad_ide("? q")
    menu = abjad_ide.io.transcript.menus[-1]
    assert menu == [
        "Abjad IDE : scores : help",
        "",
        "    clipboard - copy (cbc)",
        "    clipboard - empty (cbe)",
        "    clipboard - paste (cbv)",
        "    clipboard - show (cbs)",
        "",
        "    directory - scores (ss)",
        "",
        "    edit - files (ef)",
        "    edit - string (es)",
        "",
        "    go - back (-)",
        "    go - quit (q)",
        "    go - up (..)",
        "",
        "    hop - next score (>>)",
        "    hop - previous score (<<)",
        "",
        "    show - column (;)",
        "    show - help (?)",
        "",
    ]


def test_AbjadIDE_show_help_09():
    """
    In segment directory.
    """

    abjad_ide("red gg 02 ? q")
    menu = abjad_ide.io.transcript.menus[-1]
    assert menu == [
        "Red Score (2017) : segments : 02 : help",
        "",
        "    clipboard - copy (cbc)",
        "    clipboard - empty (cbe)",
        "    clipboard - paste (cbv)",
        "    clipboard - show (cbs)",
        "",
        "    definition.py - check (dpc)",
        "    definition.py - edit (dpe)",
        "",
        "    directory - builds (bb)",
        "    directory - contents (cc)",
        "    directory - distribution (dd)",
        "    directory - etc (ee)",
        "    directory - scores (ss)",
        "    directory - segments (gg)",
        "    directory - stylesheets (yy)",
        "    directory - wrapper (ww)",
        "",
        "    edit - files (ef)",
        "    edit - string (es)",
        "",
        "    go - back (-)",
        "    go - quit (q)",
        "    go - up (..)",
        "",
        "    hop - next package (>)",
        "    hop - next score (>>)",
        "    hop - previous package (<)",
        "    hop - previous score (<<)",
        "",
        "    illustration.ily - edit (iie)",
        "    illustration.ly - edit (ile)",
        "    illustration.ly - interpret (ili)",
        "    illustration.ly - make (ilm)",
        "    illustration.pdf - make (ipm)",
        "    illustration.pdf - nake (ipn)",
        "    illustration.pdf - open (ipo)",
        "",
        "    layout.ly - edit (lle)",
        "    layout.ly - make (llm)",
        "    layout.py - edit (lpe)",
        "",
        "    hide (hide)",
        "    show (show)",
        "    tag - hide (th)",
        "    tag - show (ts)",
        "",
        "    color (color)",
        "    uncolor (uncolor)",
        "",
        "    clicktrack - make (ctm)",
        "    segment.midi - make (midm)",
        "",
        "    show - column (;)",
        "    show - help (?)",
        "",
    ]


def test_AbjadIDE_show_help_10():
    """
    In segments directory.
    """

    abjad_ide("red gg ? q")
    menu = abjad_ide.io.transcript.menus[-1]
    assert menu == [
        "Red Score (2017) : segments : help",
        "",
        "    clipboard - copy (cbc)",
        "    clipboard - empty (cbe)",
        "    clipboard - paste (cbv)",
        "    clipboard - show (cbs)",
        "",
        "    definition.py - check (dpc)",
        "    definition.py - edit (dpe)",
        "",
        "    directory - builds (bb)",
        "    directory - contents (cc)",
        "    directory - distribution (dd)",
        "    directory - etc (ee)",
        "    directory - scores (ss)",
        "    directory - segments (gg)",
        "    directory - stylesheets (yy)",
        "    directory - wrapper (ww)",
        "",
        "    edit - files (ef)",
        "    edit - string (es)",
        "",
        "    go - back (-)",
        "    go - quit (q)",
        "    go - up (..)",
        "",
        "    hop - next package (>)",
        "    hop - next score (>>)",
        "    hop - previous package (<)",
        "    hop - previous score (<<)",
        "",
        "    illustration.ily - edit (iie)",
        "    illustration.ly - edit (ile)",
        "    illustration.ly - interpret (ili)",
        "    illustration.ly - make (ilm)",
        "    illustration.pdf - make (ipm)",
        "    illustration.pdf - nake (ipn)",
        "    illustration.pdf - open (ipo)",
        "",
        "    layout.ly - edit (lle)",
        "    layout.ly - make (llm)",
        "    layout.py - edit (lpe)",
        "",
        "    hide (hide)",
        "    show (show)",
        "    tag - hide (th)",
        "    tag - show (ts)",
        "",
        "    color (color)",
        "    uncolor (uncolor)",
        "",
        "    clicktrack - make (ctm)",
        "    segment.midi - make (midm)",
        "",
        "    show - column (;)",
        "    show - help (?)",
        "",
    ]


def test_AbjadIDE_show_help_11():
    """
    In stylesheets directory.
    """

    abjad_ide("red yy ? q")
    menu = abjad_ide.io.transcript.menus[-1]
    assert menu == [
        "Red Score (2017) : stylesheets : help",
        "",
        "    clipboard - copy (cbc)",
        "    clipboard - empty (cbe)",
        "    clipboard - paste (cbv)",
        "    clipboard - show (cbs)",
        "",
        "    directory - builds (bb)",
        "    directory - contents (cc)",
        "    directory - distribution (dd)",
        "    directory - etc (ee)",
        "    directory - scores (ss)",
        "    directory - segments (gg)",
        "    directory - stylesheets (yy)",
        "    directory - wrapper (ww)",
        "",
        "    edit - files (ef)",
        "    edit - string (es)",
        "",
        "    go - back (-)",
        "    go - quit (q)",
        "    go - up (..)",
        "",
        "    hop - next score (>>)",
        "    hop - previous score (<<)",
        "",
        "    show - column (;)",
        "    show - help (?)",
        "",
    ]


def test_AbjadIDE_show_help_12():
    """
    In wrapper directory.
    """

    abjad_ide("red ww ? q")
    menu = abjad_ide.io.transcript.menus[-1]
    assert menu == [
        "Red Score (2017) : wrapper : help",
        "",
        "    clipboard - copy (cbc)",
        "    clipboard - empty (cbe)",
        "    clipboard - paste (cbv)",
        "    clipboard - show (cbs)",
        "",
        "    directory - builds (bb)",
        "    directory - contents (cc)",
        "    directory - distribution (dd)",
        "    directory - etc (ee)",
        "    directory - scores (ss)",
        "    directory - segments (gg)",
        "    directory - stylesheets (yy)",
        "    directory - wrapper (ww)",
        "",
        "    edit - files (ef)",
        "    edit - string (es)",
        "",
        "    go - back (-)",
        "    go - quit (q)",
        "    go - up (..)",
        "",
        "    hop - next score (>>)",
        "    hop - previous score (<<)",
        "",
        "    show - column (;)",
        "    show - help (?)",
        "",
    ]
