import ide

abjad_ide = ide.AbjadIDE(test=True)
scores = ide.configuration.test_scores_directory


def test_AbjadIDE_edit_illustration_ily_01():
    """
    In segment directory.
    """

    with ide.Test():

        path = ide.Path(
            scores, "red_score", "red_score", "segments", "02", "illustration.ily"
        )
        path.write_text("")
        assert path.is_file()

        abjad_ide("red gg 02 iie q")
        transcript = abjad_ide.io.transcript
        assert f"Editing {path.trim()} ..." in transcript


def test_AbjadIDE_edit_illustration_ily_02():
    """
    In segments directory.
    """

    with ide.Test():

        for name in ["01", "02", "03"]:
            path = ide.Path(
                scores, "red_score", "red_score", "segments", name, "illustration.ily"
            )
            path.write_text("")
            assert path.is_file()

        abjad_ide("red gg iie q")
        transcript = abjad_ide.io.transcript

        for name in ["01", "02", "03"]:
            path = ide.Path(
                scores, "red_score", "red_score", "segments", name, "illustration.ily"
            )
            assert f"Editing {path.trim()} ..." in transcript
