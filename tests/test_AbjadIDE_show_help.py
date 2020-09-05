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
        "    directory - builds (bb)",
        "    directory - contents (cc)",
        "    directory - distribution (dd)",
        "    directory - etc (ee)",
        "    directory - scores (ss)",
        "    directory - segments (gg)",
        "    directory - stylesheets (yy)",
        "    directory - wrapper (ww)",
        "",
        "    go - back (-)",
        "    go - quit (q)",
        "    go - up (..)",
        "",
        "    hop - next score (MM)",
        "    hop - previous score (NN)",
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
        "    directory - builds (bb)",
        "    directory - contents (cc)",
        "    directory - distribution (dd)",
        "    directory - etc (ee)",
        "    directory - scores (ss)",
        "    directory - segments (gg)",
        "    directory - stylesheets (yy)",
        "    directory - wrapper (ww)",
        "",
        "    go - back (-)",
        "    go - quit (q)",
        "    go - up (..)",
        "",
        "    hop - next score (MM)",
        "    hop - previous score (NN)",
        "",
        "    layout.ly - make (llm)",
        "",
        "    music.ly - generate (mlg)",
        "    music.ly - interpret (mli)",
        "    music.ly - xinterpret (mlx)",
        "",
        "    hide (hide)",
        "    show (show)",
        "    tag - hide (th)",
        "    tag - show (ts)",
        "",
        "    color (color)",
        "    uncolor (uncolor)",
        "",
        "    score.pdf - build (spb)",
        "",
        "    segments - collect (ggc)",
        "    segments - handle build tags (btags)",
        "    segments - handle part tags (ptags)",
        "",
        "    show - column (;)",
        "    show - help (?)",
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
        "    directory - builds (bb)",
        "    directory - contents (cc)",
        "    directory - distribution (dd)",
        "    directory - etc (ee)",
        "    directory - scores (ss)",
        "    directory - segments (gg)",
        "    directory - stylesheets (yy)",
        "    directory - wrapper (ww)",
        "",
        "    go - back (-)",
        "    go - quit (q)",
        "    go - up (..)",
        "",
        "    hop - next score (MM)",
        "    hop - previous score (NN)",
        "",
        "    layout.ly - make (llm)",
        "",
        "    music.ly - generate (mlg)",
        "    music.ly - interpret (mli)",
        "    music.ly - xinterpret (mlx)",
        "",
        "    hide (hide)",
        "    show (show)",
        "    tag - hide (th)",
        "    tag - show (ts)",
        "",
        "    color (color)",
        "    uncolor (uncolor)",
        "",
        "    score.pdf - build (spb)",
        "",
        "    segments - collect (ggc)",
        "    segments - handle build tags (btags)",
        "    segments - handle part tags (ptags)",
        "",
        "    show - column (;)",
        "    show - help (?)",
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
        "    directory - builds (bb)",
        "    directory - contents (cc)",
        "    directory - distribution (dd)",
        "    directory - etc (ee)",
        "    directory - scores (ss)",
        "    directory - segments (gg)",
        "    directory - stylesheets (yy)",
        "    directory - wrapper (ww)",
        "",
        "    go - back (-)",
        "    go - quit (q)",
        "    go - up (..)",
        "",
        "    hop - next score (MM)",
        "    hop - previous score (NN)",
        "",
        "    layout.ly - make (llm)",
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
        "    directory - builds (bb)",
        "    directory - contents (cc)",
        "    directory - distribution (dd)",
        "    directory - etc (ee)",
        "    directory - scores (ss)",
        "    directory - segments (gg)",
        "    directory - stylesheets (yy)",
        "    directory - wrapper (ww)",
        "",
        "    go - back (-)",
        "    go - quit (q)",
        "    go - up (..)",
        "",
        "    hop - next score (MM)",
        "    hop - previous score (NN)",
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
        "    directory - builds (bb)",
        "    directory - contents (cc)",
        "    directory - distribution (dd)",
        "    directory - etc (ee)",
        "    directory - scores (ss)",
        "    directory - segments (gg)",
        "    directory - stylesheets (yy)",
        "    directory - wrapper (ww)",
        "",
        "    go - back (-)",
        "    go - quit (q)",
        "    go - up (..)",
        "",
        "    hop - next score (MM)",
        "    hop - previous score (NN)",
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
        "    directory - builds (bb)",
        "    directory - contents (cc)",
        "    directory - distribution (dd)",
        "    directory - etc (ee)",
        "    directory - scores (ss)",
        "    directory - segments (gg)",
        "    directory - stylesheets (yy)",
        "    directory - wrapper (ww)",
        "",
        "    go - back (-)",
        "    go - quit (q)",
        "    go - up (..)",
        "",
        "    hop - next score (MM)",
        "    hop - previous score (NN)",
        "",
        "    layout.ly - make (llm)",
        "    layout.py - propagate (lpp)",
        "",
        "    music.ly - generate (mlg)",
        "    music.ly - interpret (mli)",
        "    music.ly - xinterpret (mlx)",
        "",
        "    hide (hide)",
        "    show (show)",
        "    tag - hide (th)",
        "    tag - show (ts)",
        "",
        "    part.pdf - build (ppb)",
        "",
        "    color (color)",
        "    uncolor (uncolor)",
        "",
        "    segments - collect (ggc)",
        "    segments - handle build tags (btags)",
        "    segments - handle part tags (ptags)",
        "",
        "    show - column (;)",
        "    show - help (?)",
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
        "    directory - scores (ss)",
        "",
        "    go - back (-)",
        "    go - quit (q)",
        "    go - up (..)",
        "",
        "    hop - next score (MM)",
        "    hop - previous score (NN)",
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
        "    directory - builds (bb)",
        "    directory - contents (cc)",
        "    directory - distribution (dd)",
        "    directory - etc (ee)",
        "    directory - scores (ss)",
        "    directory - segments (gg)",
        "    directory - stylesheets (yy)",
        "    directory - wrapper (ww)",
        "",
        "    go - back (-)",
        "    go - quit (q)",
        "    go - up (..)",
        "",
        "    hop - next package (M)",
        "    hop - next score (MM)",
        "    hop - previous package (N)",
        "    hop - previous score (NN)",
        "",
        "    illustration.ly - interpret (ili)",
        "    illustration.ly - make (ilm)",
        "    illustration.pdf - make (ipm)",
        "    illustration.pdf - nake (ipn)",
        "",
        "    layout.ly - make (llm)",
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
        "    directory - builds (bb)",
        "    directory - contents (cc)",
        "    directory - distribution (dd)",
        "    directory - etc (ee)",
        "    directory - scores (ss)",
        "    directory - segments (gg)",
        "    directory - stylesheets (yy)",
        "    directory - wrapper (ww)",
        "",
        "    go - back (-)",
        "    go - quit (q)",
        "    go - up (..)",
        "",
        "    hop - next package (M)",
        "    hop - next score (MM)",
        "    hop - previous package (N)",
        "    hop - previous score (NN)",
        "",
        "    illustration.ly - interpret (ili)",
        "    illustration.ly - make (ilm)",
        "    illustration.pdf - make (ipm)",
        "    illustration.pdf - nake (ipn)",
        "",
        "    layout.ly - make (llm)",
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
        "    directory - builds (bb)",
        "    directory - contents (cc)",
        "    directory - distribution (dd)",
        "    directory - etc (ee)",
        "    directory - scores (ss)",
        "    directory - segments (gg)",
        "    directory - stylesheets (yy)",
        "    directory - wrapper (ww)",
        "",
        "    go - back (-)",
        "    go - quit (q)",
        "    go - up (..)",
        "",
        "    hop - next score (MM)",
        "    hop - previous score (NN)",
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
        "    directory - builds (bb)",
        "    directory - contents (cc)",
        "    directory - distribution (dd)",
        "    directory - etc (ee)",
        "    directory - scores (ss)",
        "    directory - segments (gg)",
        "    directory - stylesheets (yy)",
        "    directory - wrapper (ww)",
        "",
        "    go - back (-)",
        "    go - quit (q)",
        "    go - up (..)",
        "",
        "    hop - next score (MM)",
        "    hop - previous score (NN)",
        "",
        "    show - column (;)",
        "    show - help (?)",
        "",
    ]
