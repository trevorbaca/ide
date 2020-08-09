import ide

abjad_ide = ide.AbjadIDE(test=True)
scores = ide.configuration.test_scores_directory


def test_AbjadIDE_generate_layout_py_01():
    """In segment directory."""

    with ide.Test():
        target = ide.Path(
            scores, "red_score", "red_score", "segments", "A", "layout.py"
        )
        assert target.is_file()
        target.remove()
        assert not target.exists()

        abjad_ide("red A lpg q")
        transcript = abjad_ide.io.transcript
        assert f"Writing {target.trim()} ..." in transcript
        assert target.is_file()
