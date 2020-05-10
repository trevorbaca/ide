import ide

abjad_ide = ide.AbjadIDE(test=True)


def test_AbjadIDE_smart_pytest_01():
    """
    In contents directory.
    """

    abjad_ide("red + q")
    transcript = abjad_ide.io.transcript
    assert "Missing '+' pattern ..." in transcript

    abjad_ide("red +def q")
    transcript = abjad_ide.io.transcript
    assert "Matching '+def' to 0 files ..." in transcript

    abjad_ide("red +rpc q")
    transcript = abjad_ide.io.transcript
    assert f"Matching '+rpc' to 0 files ..." in transcript

    abjad_ide("red +A q")
    transcript = abjad_ide.io.transcript
    assert f"Matching '+A' to 0 files ..." in transcript

    abjad_ide("red +ST q")
    transcript = abjad_ide.io.transcript
    assert f"Matching '+ST' to 0 files ..." in transcript


def test_AbjadIDE_smart_pytest_02():
    """
    In test directory.
    """

    abjad_ide("red tt + q")
    transcript = abjad_ide.io.transcript
    assert "Missing '+' pattern ..." in transcript

    abjad_ide("red tt +ts q")
    transcript = abjad_ide.io.transcript
    path = ide.Path("red_score", "test", "test_segments.py")
    assert f"Matching '+ts' to {path.trim()} ..." in transcript


def test_AbjadIDE_smart_pytest_03():
    """
    Handles numbers.
    """

    abjad_ide("red tt +0 q")
    transcript = abjad_ide.io.transcript
    assert "Matching '+0' to 0 files ..." in transcript

    abjad_ide("red tt +1 q")
    transcript = abjad_ide.io.transcript
    path = ide.Path("red_score", "test", "test_segments.py")
    assert f"Matching '+1' to {path.trim()} ..." in transcript

    abjad_ide("red tt +99 q")
    transcript = abjad_ide.io.transcript
    assert "Matching '+99' to 0 files ..." in transcript


def test_AbjadIDE_smart_pytest_04():
    """
    Missing pattern.
    """

    abjad_ide("+ q")
    transcript = abjad_ide.io.transcript
    assert "Missing '+' pattern ..." in transcript


def test_AbjadIDE_smart_pytest_05():
    """
    Unmatched pattern.
    """

    abjad_ide("+asdf q")
    transcript = abjad_ide.io.transcript
    assert "Matching '+asdf' to 0 files ..." in transcript
