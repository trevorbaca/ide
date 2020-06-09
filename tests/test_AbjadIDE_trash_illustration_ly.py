import abjad
import ide

abjad_ide = ide.AbjadIDE(test=True)
scores = ide.Configuration().test_scores_directory


def test_AbjadIDE_trash_illustration_ly_01():
    """
    In segment directory.
    """

    with ide.Test():
        path = abjad.Path(
            scores, "red_score", "red_score", "segments", "A", "illustration.ly"
        )
        assert path.is_file()

        abjad_ide("red A ilt q")
        transcript = abjad_ide.io.transcript
        assert f"Trashing {path.trim()} ..." in transcript
        assert not path.exists()

        abjad_ide("red A ilt q")
        transcript = abjad_ide.io.transcript
        assert f"Missing {path.trim()} ..." in transcript


def test_AbjadIDE_trash_illustration_ly_02():
    """
    In segments directory.
    """

    with ide.Test():
        paths = []
        for name in ["_", "A", "B"]:
            path = abjad.Path(
                scores, "red_score", "red_score", "segments", name, "illustration.ly"
            )
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
