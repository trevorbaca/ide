import abjad
import ide

abjad_ide = ide.AbjadIDE(test=True)
scores = ide.Configuration().test_scores_directory


def test_AbjadIDE_trash_stylesheet_ily_01():

    with ide.Test():
        path = abjad.Path(scores, "red_score", "red_score", "builds", "letter-score")
        path /= "stylesheet.ily"
        assert path.is_file()

        abjad_ide("red bb letter ssit q")
        transcript = abjad_ide.io.transcript
        assert f"Trashing {path.trim()} ..." in transcript
        assert not path.exists()

        abjad_ide("red bb letter ssit q")
        transcript = abjad_ide.io.transcript
        assert f"Missing {path.trim()} ..." in transcript
