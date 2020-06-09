import abjad
import ide

abjad_ide = ide.AbjadIDE(test=True)
scores = ide.Configuration().test_scores_directory


def test_AbjadIDE_edit_illustration_ily_01():
    """
    In segment directory.
    """

    with ide.Test():

        path = abjad.Path(
            scores, "red_score", "red_score", "segments", "A", "illustration.ily"
        )
        path.write_text("")
        assert path.is_file()

        abjad_ide("red A iie q")
        transcript = abjad_ide.io.transcript
        assert f"Editing {path.trim()} ..." in transcript


def test_AbjadIDE_edit_illustration_ily_02():
    """
    In segments directory.
    """

    with ide.Test():

        for name in ["_", "A", "B"]:
            path = abjad.Path(
                scores, "red_score", "red_score", "segments", name, "illustration.ily"
            )
            path.write_text("")
            assert path.is_file()

        abjad_ide("red gg iie q")
        transcript = abjad_ide.io.transcript

        for name in ["_", "A", "B"]:
            path = abjad.Path(
                scores, "red_score", "red_score", "segments", name, "illustration.ily"
            )
            assert f"Editing {path.trim()} ..." in transcript
