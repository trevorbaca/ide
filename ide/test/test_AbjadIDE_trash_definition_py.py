import ide

abjad_ide = ide.AbjadIDE(test=True)


def test_AbjadIDE_trash_definition_py_01():
    """
    In segment directory.
    """

    with ide.Test():
        path = ide.Path("red_score", "segments", "A", "definition.py")
        assert path.is_file()

        abjad_ide("red %A dpt q")
        transcript = abjad_ide.io.transcript
        assert f"Trashing {path.trim()} ..." in transcript
        assert not path.exists()

        abjad_ide("red %A dpt q")
        transcript = abjad_ide.io.transcript
        assert f"Missing {path.trim()} ..." in transcript


def test_AbjadIDE_trash_definition_py_02():
    """
    In segments directory.
    """

    with ide.Test():
        paths = [
            ide.Path("red_score", "segments", name, "definition.py")
            for name in ["_", "A", "B"]
        ]
        for path in paths:
            assert path.is_file()

        abjad_ide("red gg dpt q")
        transcript = abjad_ide.io.transcript
        for path in paths:
            assert not path.exists()
            assert f"Trashing {path.trim()} ..." in transcript

        abjad_ide("red gg dpt q")
        transcript = abjad_ide.io.transcript
        for path in paths:
            assert f"Missing {path.trim()} ..." in transcript
