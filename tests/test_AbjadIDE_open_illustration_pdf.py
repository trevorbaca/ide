import ide

abjad_ide = ide.AbjadIDE(test=True)
scores = ide.configuration.test_scores_directory


def test_AbjadIDE_open_illustration_pdf_01():
    """
    In segment directory.
    """

    with ide.Test():

        path = ide.Path(
            scores, "red_score", "red_score", "segments", "A", "illustration.pdf"
        )
        assert not path.exists()

        path.write_text("")
        assert path.is_file()

        abjad_ide("red gg A ipo q")
        transcript = abjad_ide.io.transcript
        assert f"Opening {path.trim()} ..." in transcript


def test_AbjadIDE_open_illustration_pdf_02():
    """
    In segments directory.
    """

    with ide.Test():

        paths = []
        for name in ["_", "A", "B"]:
            path = ide.Path(
                scores, "red_score", "red_score", "segments", name, "illustration.pdf"
            )
            paths.append(path)
            assert not path.exists()
            path.write_text("")
            assert path.is_file()

        abjad_ide("red gg ipo q")
        transcript = abjad_ide.io.transcript
        for path in paths:
            assert f"Opening {path.trim()} ..." in transcript


def test_AbjadIDE_open_illustration_pdf_03():
    """
    Displays message when PDF does not exist.
    """

    abjad_ide("blu gg 02 ipo q")
    path = ide.Path("blue_score", "segments", "02", "illustration.pdf")
    transcript = abjad_ide.io.transcript
    assert f"Missing {path.trim()} ..." in transcript
