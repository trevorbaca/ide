import ide

abjad_ide = ide.AbjadIDE(test=True)


def test_AbjadIDE_edit_music_ly_01():

    abjad_ide("red %letter mle q")
    transcript = abjad_ide.io.transcript
    path = ide.Path("red_score", "builds", "letter-score", "music.ly")
    assert f"Editing {path.trim()} ..." in transcript
