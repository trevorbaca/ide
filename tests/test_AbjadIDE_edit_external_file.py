import ide

abjad_ide = ide.AbjadIDE(test=True)
scores = ide.configuration.test_scores_directory


def test_AbjadIDE_edit_external_file_01():

    abjad_ide("red ww .gitignore q")
    transcript = abjad_ide.io.transcript
    path = ide.Path(scores, "red_score", ".gitignore")
    assert f"Editing {path.trim()} ..." in transcript
