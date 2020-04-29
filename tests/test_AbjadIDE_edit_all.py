import abjad
import ide

abjad_ide = ide.AbjadIDE(test=True)


def test_AbjadIDE_edit_all_01():
    """
    Edits material definition files.
    """

    abjad_ide("red mm @@fini q")
    transcript = abjad_ide.io.transcript
    assert "Matching '@@fini' to 5 files ..." in transcript
    for name in [
        "instruments",
        "red_pitch_classes",
        "metronome_marks",
        "ranges",
        "time_signatures",
    ]:
        path = ide.Path("red_score", "materials", name, "definition.py")
        assert f"Editing {path.trim()} ..." in transcript


def test_AbjadIDE_edit_all_02():
    """
    Edits segment definition files.
    """

    abjad_ide("red gg @@efin q")
    transcript = abjad_ide.io.transcript
    assert "Matching '@@efin' to 3 files ..." in transcript
    for name in ["_", "A", "B"]:
        path = ide.Path("red_score", "segments", name, "definition.py")
        assert f"Editing {path.trim()} ..." in transcript

    abjad_ide("red gg @@ q")
    transcript = abjad_ide.io.transcript
    assert "Matching '@@' to 15 files ..." in transcript


def test_AbjadIDE_edit_all_03():
    """
    Handles nonexisting numeric input.
    """

    abjad_ide("red mm @@0 q")
    transcript = abjad_ide.io.transcript
    assert f"Matching '@@0' to 0 files ..." in transcript

    abjad_ide("red mm @@1 q")
    transcript = abjad_ide.io.transcript
    assert f"Matching '@@1' to 0 files ..." in transcript

    abjad_ide("red mm @@99 q")
    transcript = abjad_ide.io.transcript
    assert f"Matching '@@99' to 0 files ..." in transcript


def test_AbjadIDE_edit_all_04():
    """
    Handles empty input, junk input and nonfile input.
    """

    abjad_ide("@@asdf q")
    transcript = abjad_ide.io.transcript
    assert "Matching '@@asdf' to 0 files ..." in transcript


def test_AbjadIDE_edit_all_05():
    """
    Provides warning with <= 20 files.
    """

    abjad_ide("red @@ <return> q")
    transcript = abjad_ide.io.transcript
    assert f"Matching '@@' to " in transcript
    assert " files ok?> " in transcript
