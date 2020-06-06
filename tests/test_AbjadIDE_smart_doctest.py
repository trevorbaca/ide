import ide

abjad_ide = ide.AbjadIDE(test=True)
scores = ide.Configuration().test_scores_directory


def test_AbjadIDE_smart_doctest_01():
    """
    In contents directory.
    """

    abjad_ide("red ^ q")
    transcript = abjad_ide.io.transcript
    assert "Missing '^' pattern ..." in transcript

    abjad_ide("red ^def q")
    transcript = abjad_ide.io.transcript
    assert "Matching '^def' to 0 files ..." in transcript

    abjad_ide("red ^A q")
    transcript = abjad_ide.io.transcript
    path = ide.Path(scores, "red_score", "red_score", "segments", "A", "definition.py")
    assert f"Matching '^A' to {path.trim()} ..." in transcript


def test_AbjadIDE_smart_doctest_02():
    """
    In segments directory.
    """

    abjad_ide("red gg ^ q")
    transcript = abjad_ide.io.transcript
    assert "Missing '^' pattern ..." in transcript

    abjad_ide("red gg ^def q")
    transcript = abjad_ide.io.transcript
    assert "Matching '^def' to 0 files ..." in transcript

    abjad_ide("red gg ^A q")
    transcript = abjad_ide.io.transcript
    path = ide.Path("red_score", "segments", "A", "definition.py")
    assert f"Matching '^A' to {path.trim()} ..." in transcript


def test_AbjadIDE_smart_doctest_03():
    """
    Missing pattern.
    """

    abjad_ide("^ q")
    transcript = abjad_ide.io.transcript
    assert "Missing '^' pattern ..." in transcript


def test_AbjadIDE_smart_doctest_04():
    """
    Unmatched pattern.
    """

    abjad_ide("^asdf q")
    transcript = abjad_ide.io.transcript
    assert "Matching '^asdf' to 0 files ..." in transcript
