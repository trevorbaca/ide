import ide

abjad_ide = ide.AbjadIDE(test=True)


def test_AbjadIDE_trash_layout_py_01():

    with ide.Test():
        path = ide.Path("red_score", "builds", "letter-score", "layout.py")
        assert path.is_file()

        abjad_ide("red %let lpt q")
        transcript = abjad_ide.io.transcript
        assert f"Trashing {path.trim()} ..." in transcript
        assert not path.exists()
