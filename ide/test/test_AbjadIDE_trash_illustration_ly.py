import ide

abjad_ide = ide.AbjadIDE(test=True)


def test_AbjadIDE_trash_illustration_ly_01():
    """
    In material directory.
    """

    with ide.Test():
        path = ide.Path("red_score")
        path = path / "materials" / "red_pitch_classes" / "illustration.ly"
        assert path.is_file()

        abjad_ide("red %rpc ilt q")
        transcript = abjad_ide.io.transcript
        assert f"Trashing {path.trim()} ..." in transcript
        assert not path.exists()

        abjad_ide("red %rpc ilt q")
        transcript = abjad_ide.io.transcript
        assert f"Missing {path.trim()} ..." in transcript


def test_AbjadIDE_trash_illustration_ly_02():
    """
    In segment directory.
    """

    with ide.Test():
        path = ide.Path("red_score", "segments", "A", "illustration.ly")
        assert path.is_file()

        abjad_ide("red %A ilt q")
        transcript = abjad_ide.io.transcript
        assert f"Trashing {path.trim()} ..." in transcript
        assert not path.exists()

        abjad_ide("red %A ilt q")
        transcript = abjad_ide.io.transcript
        assert f"Missing {path.trim()} ..." in transcript


def test_AbjadIDE_trash_illustration_ly_03():
    """
    In segments directory.
    """

    with ide.Test():
        paths = []
        for name in ["_", "A", "B"]:
            path = ide.Path("red_score", "segments", name, "illustration.ly")
            assert path.is_file()
            paths.append(path)

        abjad_ide("red gg ilt q")
        transcript = abjad_ide.io.transcript
        for path in paths:
            assert f"Trashing {path.trim()} ..." in transcript
            assert not path.exists()

        abjad_ide("red gg ilt q")
        transcript = abjad_ide.io.transcript
        for path in paths:
            assert f"Missing {path.trim()} ..." in transcript
