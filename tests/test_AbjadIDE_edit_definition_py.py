import ide

abjad_ide = ide.AbjadIDE(test=True)
scores = ide.Configuration().test_scores_directory


def test_AbjadIDE_edit_definition_py_02():
    """
    In segment directory.
    """

    abjad_ide("red A dpe q")
    transcript = abjad_ide.io.transcript
    path = ide.Path(scores, "red_score", "red_score", "segments", "A", "definition.py")
    assert f"Editing {path.trim()} ..." in transcript
