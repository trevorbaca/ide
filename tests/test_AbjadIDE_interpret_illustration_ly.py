import ide

abjad_ide = ide.AbjadIDE(test=True)
scores = ide.configuration.test_scores_directory


def test_AbjadIDE_interpret_illustration_ly_01():
    """
    In segments directory.
    """

    with ide.Test():
        sources = []
        for name in ["01", "02", "03"]:
            path = ide.Path(
                scores, "red_score", "red_score", "segments", name, "illustration.ly"
            )
            sources.append(path)
        targets = [_.with_suffix(".pdf") for _ in sources]
        for target in targets:
            target.remove()

        abjad_ide("red gg ili q")
        transcript = abjad_ide.io.transcript
        for source, target in zip(sources, targets):
            assert "Interpreting ly ..." in transcript
            assert f"Removing {target.trim()} ..." not in transcript
            assert f"Interpreting {source.trim()} ..." in transcript
            assert f"Found {target.trim()} ..." in transcript
            assert f"Opening {target.trim()} ..." not in transcript
        assert "Total time" in transcript
        assert all(_.is_file() for _ in targets)

        abjad_ide("red gg ili q")
        transcript = abjad_ide.io.transcript
        for source, target in zip(sources, targets):
            assert "Interpreting ly ..." in transcript
            assert f"Removing {target.trim()} ..." in transcript
            assert f"Interpreting {source.trim()} ..." in transcript
            assert f"Found {target.trim()} ..." in transcript
            assert f"Opening {target.trim()} ..." not in transcript
        assert "Total time" in transcript
        assert all(_.is_file() for _ in targets)


def test_AbjadIDE_interpret_illustration_ly_02():
    """
    In segment directory.
    """

    with ide.Test():
        source = ide.Path(
            scores, "red_score", "red_score", "segments", "02", "illustration.ly"
        )
        target = source.with_suffix(".pdf")
        target.remove()

        abjad_ide("red gg 02 ili q")
        transcript = abjad_ide.io.transcript
        assert "Interpreting ly ..." in transcript
        assert f"Interpreting {source.trim()} ..." in transcript
        assert f"Removing {target.trim()} ..." not in transcript
        assert f"Found {target.trim()} ..." in transcript
        assert f"Opening {target.trim()} ..." in transcript
        assert target.is_file()

        abjad_ide("red gg 02 ili q")
        transcript = abjad_ide.io.transcript
        assert "Interpreting ly ..." in transcript
        assert f"Interpreting {source.trim()} ..." in transcript
        assert f"Removing {target.trim()} ..." in transcript
        assert f"Found {target.trim()} ..." in transcript
        assert f"Opening {target.trim()} ..." in transcript
        assert target.is_file()
