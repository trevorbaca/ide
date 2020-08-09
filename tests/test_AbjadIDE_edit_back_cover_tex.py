import ide

abjad_ide = ide.AbjadIDE(test=True)
scores = ide.configuration.test_scores_directory


def test_AbjadIDE_edit_back_cover_tex_01():

    abjad_ide("red bb letter bcte q")
    transcript = abjad_ide.io.transcript
    path = ide.Path(
        scores, "red_score", "red_score", "builds", "letter-score", "back-cover.tex"
    )
    assert f"Editing {path.trim()} ..." in transcript
