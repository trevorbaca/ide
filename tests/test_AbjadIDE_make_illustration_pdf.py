import ide

abjad_ide = ide.AbjadIDE(test=True)
scores = ide.Configuration().test_scores_directory


def test_AbjadIDE_make_illustration_pdf_01():
    """
    In segment directory.
    """

    with ide.Test():
        directory = ide.Path(scores, "red_score", "red_score", "segments", "A")
        ly = directory / "illustration.ly"
        ly.remove()
        pdf = directory / "illustration.pdf"
        pdf.remove()
        maker = directory / "__make_segment_pdf__.py"
        maker.remove()

        abjad_ide("red A ipm q")
        transcript = abjad_ide.io.transcript
        assert "Making segment A PDF ..." in transcript
        assert f"Removing {ly.trim()} ..." not in transcript
        assert f"Removing {pdf.trim()} ..." not in transcript
        assert f"Writing {maker.trim()} ..." in transcript
        assert f"Interpreting {maker.trim()} ..." in transcript
        assert f"Found {ly.trim()} ..." in transcript
        assert f"Found {pdf.trim()} ..." in transcript
        assert f"Removing {maker.trim()} ..." in transcript
        assert f"Opening {pdf.trim()} ..." in transcript
        assert ly.is_file()
        assert pdf.is_file()
        assert not maker.exists()

        abjad_ide("red A ipm q")
        transcript = abjad_ide.io.transcript
        assert "Making segment A PDF ..." in transcript
        assert f"Removing {ly.trim()} ..." in transcript
        assert f"Removing {pdf.trim()} ..." in transcript
        assert f"Writing {maker.trim()} ..." in transcript
        assert f"Interpreting {maker.trim()} ..." in transcript
        assert f"Found {ly.trim()} ..." in transcript
        assert f"Found {pdf.trim()} ..." in transcript
        assert f"Removing {maker.trim()} ..." in transcript
        assert f"Opening {pdf.trim()} ..." in transcript
        assert ly.is_file()
        assert pdf.is_file()
        assert not maker.exists()


def test_AbjadIDE_make_illustration_pdf_02():
    """
    In segments directory.
    """

    with ide.Test():
        directory = ide.Path(scores, "red_score", "red_score", "segments")
        names = ["_", "A", "B"]
        for name in names:
            ly = directory / "illustration.ly"
            ly.remove()
            pdf = directory / "illustration.pdf"
            pdf.remove()
            maker = directory / "__make_segment_pdf__.py"
            maker.remove()

        abjad_ide("red gg ipm q")
        transcript = abjad_ide.io.transcript
        for name in names:
            ly = directory / name / "illustration.ly"
            pdf = directory / name / "illustration.pdf"
            maker = directory / name / "__make_segment_pdf__.py"
            assert f"Making segment {name} PDF ..." in transcript
            assert f"Writing {maker.trim()} ..." in transcript
            assert f"Interpreting {maker.trim()} ..." in transcript
            assert f"Found {ly.trim()} ..." in transcript
            assert f"Found {pdf.trim()} ..." in transcript
            assert f"Removing {maker.trim()} ..." in transcript
            assert "Opening" not in transcript
            assert ly.is_file()
            assert pdf.is_file()
            assert not maker.exists()
