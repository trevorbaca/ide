import abjad
import ide

abjad_ide = ide.AbjadIDE(test=True)
scores = ide.Configuration().test_scores_directory


def test_AbjadIDE_trash_front_cover_tex_01():

    with ide.Test():
        path = abjad.Path(scores, "red_score", "red_score", "builds", "letter-score")
        path /= "front-cover.tex"
        assert path.is_file()

        abjad_ide("red bb letter fctt q")
        transcript = abjad_ide.io.transcript
        assert f"Trashing {path.trim()} ..." in transcript
        assert not path.exists()

        abjad_ide("red bb letter fctt q")
        transcript = abjad_ide.io.transcript
        assert "No files matching front-cover.tex ..." in transcript
