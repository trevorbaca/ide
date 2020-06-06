import ide

abjad_ide = ide.AbjadIDE(test=True)
scores = ide.Configuration().test_scores_directory


def test_AbjadIDE_edit_layout_py_01():

    abjad_ide("red %let lpe q")
    transcript = abjad_ide.io.transcript
    path = ide.Path(
        scores, "red_score", "red_score", "builds", "letter-score", "layout.py"
    )
    assert f"Editing {path.trim()} ..." in transcript
