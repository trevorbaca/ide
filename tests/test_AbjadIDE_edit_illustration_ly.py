import ide

abjad_ide = ide.AbjadIDE(test=True)
scores = ide.Configuration().test_scores_directory


def test_AbjadIDE_edit_illustration_ly_01():
    """
    In segment directory.
    """

    abjad_ide("red %A ile q")
    transcript = abjad_ide.io.transcript
    path = ide.Path(
        scores, "red_score", "red_score", "segments", "A", "illustration.ly"
    )
    assert f"Editing {path.trim()} ..." in transcript


def test_AbjadIDE_edit_illustration_ly_02():
    """
    In segments directory.
    """

    abjad_ide("red gg ile q")
    transcript = abjad_ide.io.transcript

    for name in ["_", "A", "B"]:
        path = ide.Path(
            scores, "red_score", "red_score", "segments", name, "illustration.ly"
        )
        assert f"Editing {path.trim()} ..." in transcript
