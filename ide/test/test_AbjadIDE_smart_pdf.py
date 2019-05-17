import ide

abjad_ide = ide.AbjadIDE(test=True)


def test_AbjadIDE_smart_pdf_01():
    """
    In segment directory.
    """

    with ide.Test():
        path = ide.Path("red_score", "segments", "A", "illustration.pdf")

        abjad_ide("red %A ipm q")
        assert path.is_file()

        abjad_ide("red *A q")
        transcript = abjad_ide.io.transcript
        assert f"Opening {path.trim()} ..." in transcript


def test_AbjadIDE_smart_pdf_02():
    """
    Handles numbers.
    """

    with ide.Test():
        path = ide.Path("red_score", "segments", "_", "illustration.pdf")

        abjad_ide("red %_ ipm q")
        assert path.is_file()

        abjad_ide("red gg *0 q")
        transcript = abjad_ide.io.transcript
        assert f"Matching '*0' to 0 files ..." in transcript

        abjad_ide("red gg *1 q")
        transcript = abjad_ide.io.transcript
        assert f"Opening {path.trim()} ..." in transcript


def test_AbjadIDE_smart_pdf_03():
    """
    Missing pattern.
    """

    abjad_ide("* q")
    transcript = abjad_ide.io.transcript
    assert "Missing '*' pattern ..." in transcript


def test_AbjadIDE_smart_pdf_04():
    """
    Unmatched pattern.
    """

    abjad_ide("*asdf q")
    transcript = abjad_ide.io.transcript
    assert "Matching '*asdf' to 0 files ..." in transcript
