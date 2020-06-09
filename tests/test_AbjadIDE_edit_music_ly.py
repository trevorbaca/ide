import abjad
import ide

abjad_ide = ide.AbjadIDE(test=True)
scores = ide.Configuration().test_scores_directory


def test_AbjadIDE_edit_music_ly_01():

    abjad_ide("red bb letter mle q")
    transcript = abjad_ide.io.transcript
    path = abjad.Path(
        scores, "red_score", "red_score", "builds", "letter-score", "music.ly"
    )
    assert f"Editing {path.trim()} ..." in transcript
