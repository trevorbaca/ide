import ide

abjad_ide = ide.AbjadIDE(test=True)


def test_AbjadIDE_trash_layout_ly_01():

    with ide.Test():
        path = ide.Path("red_score", "builds", "letter-score", "layout.ly")
        assert path.is_file()

        abjad_ide("red %let llt q")
        transcript = abjad_ide.io.transcript
        assert f"Trashing {path.trim()} ..." in transcript
        assert not path.exists()
