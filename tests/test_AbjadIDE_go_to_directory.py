import ide

abjad_ide = ide.AbjadIDE(test=True)
scores = ide.Configuration().test_scores_directory


def test_AbjadIDE_go_to_directory_01():
    """
    Goes to assets directory.
    """

    abjad_ide("red %_ass q")
    transcript = abjad_ide.io.transcript
    assert "Red Score (2017) : builds : _assets (empty)" in transcript.titles


def test_AbjadIDE_go_to_directory_02():
    """
    Goes to build directory.
    """

    abjad_ide("red %ette q")
    transcript = abjad_ide.io.transcript
    assert "Red Score (2017) : builds : letter-score" in transcript.titles


def test_AbjadIDE_go_to_directory_03():
    """
    Goes to distribution directory.
    """

    abjad_ide("red %istri q")
    transcript = abjad_ide.io.transcript
    assert "Red Score (2017) : distribution" in transcript.titles


def test_AbjadIDE_go_to_directory_04():
    """
    Goes to etc directory.
    """

    abjad_ide("red %etc q")
    transcript = abjad_ide.io.transcript
    assert "Red Score (2017) : etc" in transcript.titles


def test_AbjadIDE_go_to_directory_05():
    """
    Goes to segment directory.
    """

    abjad_ide("red %A q")
    transcript = abjad_ide.io.transcript
    assert "Red Score (2017) : segments : A" in transcript.titles


def test_AbjadIDE_go_to_directory_06():
    """
    Goes to segments directory.
    """

    abjad_ide("red %egmen q")
    transcript = abjad_ide.io.transcript
    assert "Editing red_score/PianoStaffSegmentMaker.py ..." in transcript


def test_AbjadIDE_go_to_directory_07():
    """
    Goes to stylesheet directory.
    """

    abjad_ide("red %yles q")
    transcript = abjad_ide.io.transcript
    assert "Red Score (2017) : stylesheets" in transcript.titles


def test_AbjadIDE_go_to_directory_08():
    """
    Goes to test directory.
    """

    abjad_ide("red %est q")
    transcript = abjad_ide.io.transcript
    assert "Red Score (2017) : test" in transcript.titles


def test_AbjadIDE_go_to_directory_09():
    """
    Handles numeric input.
    """

    abjad_ide("red gg %0 q")
    transcript = abjad_ide.io.transcript
    assert "Matching '%0' to 0 directories ..." in transcript

    abjad_ide("red gg %1 q")
    transcript = abjad_ide.io.transcript
    path = ide.Path(scores, "red_score", "red_score", "segments", "_")
    assert f"Matching '%1' to {path.trim()} ..." in transcript

    abjad_ide("red gg %99 q")
    transcript = abjad_ide.io.transcript
    assert "Matching '%99' to 0 directories ..." in transcript


def test_AbjadIDE_go_to_directory_10():
    """
    Handles empty input and junk input.
    """

    abjad_ide("% q")
    transcript = abjad_ide.io.transcript
    assert "Matching '%' to 0 directories ..." in transcript

    abjad_ide("%asdf q")
    transcript = abjad_ide.io.transcript
    assert "Matching '%asdf' to 0 directories ..." in transcript


def test_AbjadIDE_go_to_directory_11():
    """
    Handles double input.
    """

    abjad_ide("%% q")
    transcript = abjad_ide.io.transcript
    assert "Matching '%%' to 0 directories ..." in transcript

    abjad_ide("%%asdf q")
    transcript = abjad_ide.io.transcript
    assert "Matching '%%asdf' to 0 directories ..." in transcript
