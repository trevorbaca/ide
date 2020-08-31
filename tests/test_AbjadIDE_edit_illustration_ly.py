import ide

abjad_ide = ide.AbjadIDE(test=True)
scores = ide.configuration.test_scores_directory


def test_AbjadIDE_edit_illustration_ly_01():
    """
    In segment directory.
    """

    abjad_ide("red gg 02 ile q")
    transcript = abjad_ide.io.transcript
    path = ide.Path(
        scores, "red_score", "red_score", "segments", "02", "illustration.ly"
    )
    assert f"Editing {path.trim()} ..." in transcript


def test_AbjadIDE_edit_illustration_ly_02():
    """
    In segments directory.
    """

    abjad_ide("red gg ile q")
    transcript = abjad_ide.io.transcript

    for name in ["01", "02", "03"]:
        path = ide.Path(
            scores, "red_score", "red_score", "segments", name, "illustration.ly"
        )
        assert f"Editing {path.trim()} ..." in transcript
