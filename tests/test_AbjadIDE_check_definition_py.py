import abjad
import ide

abjad_ide = ide.AbjadIDE(test=True)
scores = ide.configuration.test_scores_directory


def test_AbjadIDE_check_definition_py_03():
    """
    In segment directory.
    """

    path = abjad.Path(scores, "red_score", "red_score", "segments", "A", "definition.py")
    abjad_ide("red A dpc q")
    transcript = abjad_ide.io.transcript
    assert f"{path.trim()} ... OK" in transcript
    assert "Total time " in transcript


def test_AbjadIDE_check_definition_py_04():
    """
    In segments directory.
    """

    abjad_ide("red gg dpc q")
    transcript = abjad_ide.io.transcript
    for name in ["_", "A", "B"]:
        path = abjad.Path(
            scores, "red_score", "red_score", "segments", name, "definition.py"
        )
        assert f"{path.trim()} ... OK" in transcript
    assert "Total time " in transcript
