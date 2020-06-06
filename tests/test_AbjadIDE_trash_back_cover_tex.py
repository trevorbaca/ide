import ide

abjad_ide = ide.AbjadIDE(test=True)
scores = ide.Configuration().test_scores_directory


def test_AbjadIDE_trash_back_cover_tex_01():

    with ide.Test():
        path = ide.Path(
            scores, "red_score", "red_score", "builds", "letter-score", "back-cover.tex"
        )
        assert path.is_file()

        abjad_ide("red %letter bctt q")
        transcript = abjad_ide.io.transcript
        assert f"Trashing {path.trim()} ..." in transcript
        assert not path.exists()

        abjad_ide("red %letter bctt q")
        transcript = abjad_ide.io.transcript
        assert "No files matching back-cover.tex ..." in transcript
