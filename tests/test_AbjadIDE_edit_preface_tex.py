import ide

abjad_ide = ide.AbjadIDE(test=True)
scores = ide.Configuration().test_scores_directory


def test_AbjadIDE_edit_preface_tex_01():

    abjad_ide("red bb letter pfte q")
    transcript = abjad_ide.io.transcript
    path = ide.Path(
        scores, "red_score", "red_score", "builds", "letter-score", "preface.tex"
    )
    assert f"Editing {path.trim()} ..." in transcript
