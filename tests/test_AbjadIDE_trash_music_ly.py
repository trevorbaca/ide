import abjad
import ide

abjad_ide = ide.AbjadIDE(test=True)
scores = ide.Configuration().test_scores_directory


def test_AbjadIDE_trash_music_ly_01():

    with ide.Test():
        path = abjad.Path(
            scores, "red_score", "red_score", "builds", "letter-score", "music.ly"
        )
        assert path.is_file()

        abjad_ide("red bb letter mlt q")
        transcript = abjad_ide.io.transcript
        assert f"Trashing {path.trim()} ..." in transcript
        assert not path.exists()

        abjad_ide("red bb letter mlt q")
        transcript = abjad_ide.io.transcript
        assert "No files matching music.ly ..." in transcript
